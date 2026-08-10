import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location("discover", Path(__file__).parents[1] / "scripts/discover.py")
discover = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(discover)


NOSTR_SOURCE = {
    "name": "NostrMag weekly issues",
    "pubkey": "e" * 64,
    "kinds": [1],
    "required_tags": ["nostrmag"],
}


def make_event(event_id="a" * 64, source="NostrMag weekly issues", **overrides):
    event = {
        "id": event_id,
        "pubkey": "b" * 64,
        "content": "Marmot https://github.com/Example/Marmot-App",
        "tags": [["t", "nostrmag"]],
        "_source": source,
    }
    event.update(overrides)
    return event


VERIFIED = {
    "url": "https://github.com/example/marmot-app",
    "name": "example/marmot-app",
    "description": "Marmot client",
    "pushed_at": "2026-08-01T00:00:00Z",
    "evidence": "Marmot",
}


def build(config, org, nostr, zap):
    return discover.build_report(config, org, nostr, zap, [])


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self._temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self._temporary_directory.cleanup)
        seen = Path(self._temporary_directory.name) / "discovery-seen.json"
        self._seen_patch = patch.object(discover, "SEEN", seen)
        self._seen_patch.start()
        self.addCleanup(self._seen_patch.stop)

    def test_normalize_repository_variants(self):
        self.assertEqual(
            discover.normalize_repo("https://github.com/Example/Marmot-App.git"),
            "https://github.com/example/marmot-app",
        )

    def test_repo_urls_are_read_from_markdown_destinations(self):
        text = "[repo](https://github.com/Example/Linked)"
        self.assertEqual(
            discover.REPO_URL.findall(text),
            ["https://github.com/Example/Linked"],
        )

    def test_zapstore_repository_comes_from_tags(self):
        event = make_event(
            "f" * 64,
            "Zapstore signed app metadata",
            content="",
            tags=[
                ["d", "com.example.app"],
                ["repository", "https://github.com/Example/Zap-App"],
                ["homepage", "https://example.com"],
            ],
        )
        self.assertEqual(
            discover.extract_zapstore_repos(event),
            ["https://github.com/example/zap-app"],
        )

    def test_html_to_text_surfaces_link_targets(self):
        body = (
            '<html><body>'
            '<a href="https://github.com/Example/From-Article">repo</a>'
            '<script>var ignored = "https://github.com/Example/Hidden";</script>'
            "</body></html>"
        )
        text = discover.html_to_text(body)
        self.assertIn("https://github.com/Example/From-Article", text)
        self.assertNotIn("Hidden", text)

    @patch.object(discover, "verify_repo", return_value=dict(VERIFIED))
    @patch.object(discover, "catalog_repos", return_value=set())
    def test_cross_source_candidate_is_deduplicated_and_keeps_provenance(self, _catalog, _verify):
        event = make_event()
        zap = make_event("c" * 64, "Zapstore signed app metadata")

        retained, rejected, candidates = build({"nostr_sources": [NOSTR_SOURCE]}, [], [event], [zap])

        self.assertEqual(len(candidates), 1)
        candidate = candidates["https://github.com/example/marmot-app"]
        self.assertEqual(len(candidate["provenance"]), 2)
        self.assertEqual({item["id"] for item in retained}, {"a" * 64, "c" * 64})

    @patch.object(discover, "verify_repo")
    @patch.object(discover, "catalog_repos", return_value={"https://github.com/example/marmot-app"})
    def test_catalog_entry_is_not_proposed_again(self, _catalog, verify):
        retained, rejected, candidates = build({"nostr_sources": [NOSTR_SOURCE]}, [], [make_event()], [])
        self.assertFalse(candidates)
        verify.assert_not_called()

    @patch.object(discover, "verify_repo")
    @patch.object(discover, "catalog_repos", return_value=set())
    def test_seen_event_is_not_processed_again(self, _catalog, verify):
        discover.SEEN.write_text(
            '{"event_ids":["' + "a" * 64 + '"],"repository_urls":[]}',
            encoding="utf-8",
        )

        retained, rejected, candidates = build({"nostr_sources": [NOSTR_SOURCE]}, [], [make_event()], [])

        self.assertFalse(candidates)
        self.assertFalse(retained)
        verify.assert_not_called()

    @patch.object(
        discover,
        "verify_repo",
        side_effect=["README.md not found and description lacks explicit Marmot evidence"],
    )
    @patch.object(discover, "catalog_repos", return_value=set())
    def test_readme_404_is_recorded_as_rejected(self, _catalog, _verify):
        retained, rejected, candidates = build({"nostr_sources": [NOSTR_SOURCE]}, [], [make_event()], [])
        self.assertFalse(candidates)
        self.assertEqual(rejected[0]["url"], "https://github.com/example/marmot-app")
        self.assertIn("README.md not found", rejected[0]["reason"])

    @patch.object(discover, "verify_repo", return_value=dict(VERIFIED))
    @patch.object(discover, "catalog_repos", return_value=set())
    def test_report_is_deterministic_regardless_of_event_order(self, _catalog, _verify):
        first = make_event("1" * 64, "Nostr Recap weekly review", tags=[])
        second = make_event("2" * 64, "NostrMag weekly issues")

        forward = build({"nostr_sources": [NOSTR_SOURCE]}, [], [first, second], [])
        reverse = build({"nostr_sources": [NOSTR_SOURCE]}, [], [second, first], [])

        self.assertEqual(forward[0], reverse[0])
        self.assertEqual(forward[2], reverse[2])

    @patch.object(discover, "verify_repo", return_value=dict(VERIFIED))
    @patch.object(discover, "catalog_repos", return_value=set())
    def test_report_digest_is_independent_of_relay_return_order(self, _catalog, _verify):
        first = make_event(_relay="wss://one.example")
        second = make_event(_relay="wss://two.example")

        forward = build({"nostr_sources": [NOSTR_SOURCE]}, [], [first, second], [])
        reverse = build({"nostr_sources": [NOSTR_SOURCE]}, [], [second, first], [])

        self.assertEqual(
            discover.render_report(*forward, [], 10),
            discover.render_report(*reverse, [], 10),
        )

    @patch.object(discover, "run_nak", return_value=[])
    @patch.dict(discover.os.environ, {}, clear=True)
    @patch.object(discover, "api_json", return_value=[])
    def test_multiple_nostr_kinds_use_repeated_flags(self, _api, run_nak):
        config = {
            "github_organization": "marmot-protocol",
            "relays": ["wss://relay.example"],
            "nostr_sources": [{
                "name": "Weekly review",
                "pubkey": "e" * 64,
                "kinds": [1, 30023],
                "required_tags": [],
            }],
            "zapstore": {},
        }

        discover.fetch_inputs(config, 10)

        request = run_nak.call_args_list[0].args[0]
        self.assertEqual(request[:5], ["req", "-k", "1", "-k", "30023"])

    @patch.object(discover, "run_nak")
    @patch.dict(discover.os.environ, {}, clear=True)
    @patch.object(discover, "api_json", return_value=[])
    @patch.object(discover, "fetch_anchor_articles", return_value=[])
    def test_anchor_event_is_fetched_outside_rolling_window(self, _articles, _api, run_nak):
        anchor = "d" * 64
        anchored_event = make_event(anchor, "NostrMag", pubkey="e" * 64, kind=1)
        run_nak.side_effect = [[], [anchored_event], [], [], [], []]
        config = {
            "github_organization": "marmot-protocol",
            "relays": ["wss://relay.example"],
            "nostr_sources": [{**NOSTR_SOURCE, "name": "NostrMag", "anchor_event": anchor}],
            "zapstore": {"app_kind": 32267, "relay": "wss://zap.example"},
        }

        _org, events, _zap, _failures = discover.fetch_inputs(config, 10)

        self.assertEqual([event["id"] for event in events], [anchor])
        self.assertIn(
            ["req", "-i", anchor, "wss://relay.example"],
            [call.args[0] for call in run_nak.call_args_list],
        )


if __name__ == "__main__":
    unittest.main()
