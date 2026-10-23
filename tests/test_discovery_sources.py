import datetime as dt
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import MagicMock, patch
import urllib.error

SPEC = importlib.util.spec_from_file_location("discover", Path(__file__).parents[1] / "scripts/discover.py")
discover = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(discover)

FIXTURES = Path(__file__).parent / "fixtures"
NOW = dt.datetime(2026, 10, 23, 12, tzinfo=dt.UTC)
A, B = "c" * 64, "d" * 64
NPUB_A = "npub1enxvenxvenxvenxvenxvenxvenxvenxvenxvenxvenxvenxvenxqn2pktz"
MDK_QUERY = '"marmot-protocol/mdk" cgka-engine filename:Cargo.toml -org:marmot-protocol'
AGENT_QUERY = '"marmot.agent-control.v2" -org:marmot-protocol'
CODE_SEARCH = {
    "enabled": True,
    "requests_per_minute": 9,
    "queries": [
        {"name": "MDK cgka-engine via Git", "query": MDK_QUERY},
        {"name": "agent-control v2 protocol", "query": AGENT_QUERY},
    ],
}
NIP34 = {
    "enabled": True,
    "relays": ["wss://relay.ngit.dev", "wss://gitnostr.com"],
    "keywords": ["marmot", "white noise", "mdk", "mls"],
}
GITLAB = {"enabled": True, "searches": ["marmot"], "topics": ["marmot"], "keywords": ["marmot"]}
VERIFIED = {
    "url": "https://github.com/example/mls-chat",
    "name": "Example/MLS-Chat",
    "description": "Marmot group chat",
    "last_commit_at": "2026-10-20T00:00:00Z",
    "commit_url": "https://github.com/Example/MLS-Chat/commit/" + "a" * 40,
    "evidence": "Marmot",
}


def fixture_json(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def fixture_events():
    lines = (FIXTURES / "nip34-events.jsonl").read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def http_error(code):
    error = RuntimeError(f"GitHub API https://api.github.com/search/code -> HTTP {code}")
    error.__cause__ = urllib.error.HTTPError("https://api.github.com/search/code", code, "error", {}, None)
    error.__cause__.close()
    return error


class SourceTestCase(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.tmp = Path(directory.name)
        self.catalog = self.tmp / "README.md"
        self.catalog.write_text("# Catalog\n", encoding="utf-8")
        for name, value in (
            ("SEEN", self.tmp / "discovery-seen.json"),
            ("CATALOG", self.catalog),
            ("NOW", NOW),
        ):
            patcher = patch.object(discover, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def build(self, nostr=(), code_hits=(), gitlab=()):
        return discover.build_report({}, [], list(nostr), [], [], list(code_hits), list(gitlab))


class GitHubCodeSearchTests(SourceTestCase):
    def search(self, responses, settings=CODE_SEARCH):
        failures, skipped, sleeps, requests = [], [], [], []
        clock = [100.0]

        def sleep(seconds):
            sleeps.append(seconds)
            clock[0] += seconds

        def respond(url):
            requests.append((clock[0], url))
            clock[0] += 0.5
            response = responses.pop(0)
            if isinstance(response, Exception):
                raise response
            return response

        with (
            patch.dict(discover.os.environ, {"GITHUB_TOKEN": "test-token"}, clear=True),
            patch.object(discover, "api_json", side_effect=respond),
        ):
            hits = discover.github_code_search(settings, failures, skipped, sleep=sleep, clock=lambda: clock[0])
        return hits, failures, skipped, sleeps, requests

    def test_hits_are_one_lead_per_repository_and_query(self):
        fixture = fixture_json("github-code-search.json")
        hits, failures, skipped, _sleeps, requests = self.search([fixture[MDK_QUERY], fixture[AGENT_QUERY]])

        self.assertEqual(failures, [])
        self.assertEqual(skipped, [])
        self.assertEqual(
            [(hit["url"], hit["query"]) for hit in hits],
            [
                ("https://github.com/example-dev/group-chat", "MDK cgka-engine via Git"),
                ("https://github.com/example-dev/group-chat", "agent-control v2 protocol"),
                ("https://github.com/example-labs/agent-harness", "agent-control v2 protocol"),
                ("https://github.com/example-labs/marmot-web-runtime", "MDK cgka-engine via Git"),
            ],
        )
        # The lexicographically smallest blob URL is kept whatever the API order.
        self.assertTrue(hits[0]["evidence"].endswith("/core/Cargo.toml"))
        self.assertIn("q=%22marmot-protocol%2Fmdk%22%20cgka-engine%20filename%3ACargo.toml", requests[0][1])

    def test_requests_are_spaced_under_the_code_search_limit(self):
        empty = {"items": [], "incomplete_results": False}
        settings = {**CODE_SEARCH, "queries": CODE_SEARCH["queries"] * 2}
        _hits, _failures, _skipped, sleeps, requests = self.search([empty] * 4, settings)

        self.assertEqual(len(requests), 4)
        self.assertEqual(len(sleeps), 3)
        gaps = [later[0] - earlier[0] for earlier, later in zip(requests, requests[1:])]
        for gap in gaps:
            self.assertGreaterEqual(gap, 60 / 9 - 1e-9)

    def test_rate_limit_stops_remaining_queries(self):
        _hits, failures, _skipped, _sleeps, requests = self.search([http_error(403)])
        self.assertEqual(len(requests), 1)
        self.assertEqual(len(failures), 1)
        self.assertIn("remaining queries skipped", failures[0])

    def test_other_errors_skip_only_that_query(self):
        fixture = fixture_json("github-code-search.json")
        hits, failures, _skipped, _sleeps, requests = self.search([http_error(422), fixture[AGENT_QUERY]])
        self.assertEqual(len(requests), 2)
        self.assertIn("failed for MDK cgka-engine via Git", failures[0])
        self.assertEqual({hit["query"] for hit in hits}, {"agent-control v2 protocol"})

    def test_incomplete_results_are_recorded(self):
        partial = {"items": [], "incomplete_results": True}
        _hits, failures, _skipped, _sleeps, _requests = self.search([partial, {"items": []}])
        self.assertEqual(failures, ["GitHub code search returned incomplete results for MDK cgka-engine via Git"])

    def test_missing_token_is_a_clean_skip(self):
        failures, skipped = [], []
        with (
            patch.dict(discover.os.environ, {}, clear=True),
            patch.object(discover, "api_json") as api,
        ):
            self.assertEqual(discover.github_code_search(CODE_SEARCH, failures, skipped), [])
        api.assert_not_called()
        self.assertEqual(failures, [])
        self.assertIn("GITHUB_TOKEN not set", skipped[0])

    def test_disabled_source_makes_no_requests(self):
        failures, skipped = [], []
        with patch.object(discover, "api_json") as api:
            discover.github_code_search({**CODE_SEARCH, "enabled": False}, failures, skipped)
        api.assert_not_called()
        self.assertEqual((failures, skipped), ([], []))

    def test_timeouts_and_non_json_bodies_are_source_errors(self):
        captive = MagicMock()
        captive.__enter__.return_value.read.return_value = b"<html>captive portal</html>"
        for helper in (lambda: discover.api_json("https://api.github.com/search/code"),
                       lambda: discover.gitlab_json("https://gitlab.com/api/v4/projects", "token")):
            for response in ({"side_effect": TimeoutError("read timed out")}, {"return_value": captive}):
                with (
                    self.subTest(response=response),
                    patch.object(discover.urllib.request, "urlopen", **response),
                    self.assertRaises(RuntimeError),
                ):
                    helper()

    def test_hits_use_github_verification_once_per_repository(self):
        hits = [
            {"url": "https://github.com/example/old", "query": "q1", "evidence": "https://github.com/example/old/blob/1/a"},
            {"url": "https://github.com/example/old", "query": "q2", "evidence": "https://github.com/example/old/blob/1/b"},
        ]
        with patch.object(discover, "verify_repo", return_value="no explicit Marmot reference in description or README") as verify:
            _retained, rejected, candidates, leads = self.build(code_hits=hits)
        verify.assert_called_once_with("https://github.com/example/old")
        self.assertEqual(len(rejected), 2)
        self.assertEqual((candidates, leads), ({}, {}))

    def test_candidate_provenance_cites_the_matching_file(self):
        hit = {"url": VERIFIED["url"], "query": "q1", "evidence": "https://github.com/Example/MLS-Chat/blob/1/Cargo.toml"}
        with patch.object(discover, "verify_repo", return_value=dict(VERIFIED)):
            _retained, _rejected, candidates, _leads = self.build(code_hits=[hit])
        self.assertEqual(
            candidates[VERIFIED["url"]]["provenance"],
            [{"source": "GitHub code search", "detail": f"q1: {hit['evidence']}"}],
        )


class Nip34Tests(SourceTestCase):
    def test_keyword_filter_keeps_newest_version_with_all_relays(self):
        events = discover.select_announcements(fixture_events(), NIP34["keywords"])

        self.assertEqual([event["id"] for event in events], ["a1" * 32, "b2" * 32, "e5" * 32])
        self.assertEqual(events[0]["_relay"], "wss://gitnostr.com,wss://relay.ngit.dev")
        self.assertEqual({event["_source"] for event in events}, {"NIP-34 repository announcements"})

    def test_keywords_match_whole_words_and_spacing_variants(self):
        pattern = discover.keyword_pattern(NIP34["keywords"])
        for text in ("Marmot", "whitenoise-tui", "White Noise", "white_noise", "MLS-based", "mdk-odin"):
            with self.subTest(text=text):
                self.assertTrue(pattern.search(text))
        for text in ("vmdk-tools", "openmls", "marmota", "whitenoisy"):
            with self.subTest(text=text):
                self.assertFalse(pattern.search(text))

    @patch.object(discover, "run_nak")
    def test_fetch_queries_each_relay_and_records_outages(self, run_nak):
        events = fixture_events()
        run_nak.side_effect = [RuntimeError("timed out"), [events[0], events[3]]]
        failures = []

        selected = discover.fetch_repository_announcements(NIP34, 1792000000, failures)

        self.assertEqual(
            [call.args[0] for call in run_nak.call_args_list],
            [
                ["req", "-k", "30617", "--since", "1792000000", "--paginate", "wss://relay.ngit.dev"],
                ["req", "-k", "30617", "--since", "1792000000", "--paginate", "wss://gitnostr.com"],
            ],
        )
        self.assertEqual(failures, ["NIP-34 fetch failed via wss://relay.ngit.dev: timed out"])
        self.assertEqual([event["_relay"] for event in selected], ["wss://gitnostr.com"] * 2)
        # Non-matching announcements survive the fetch so they can still
        # supersede older versions; only other kinds are dropped.
        keep = run_nak.call_args.kwargs["keep"]
        self.assertTrue(keep(events[4]))
        self.assertFalse(keep({**events[4], "kind": 1}))

    def test_newer_version_without_keywords_supersedes_older_match(self):
        older = {**fixture_events()[0], "tags": [["d", "relay-bot"], ["description", "Bridge for Marmot groups"]]}
        newer = {**older, "id": "f6" * 32, "created_at": older["created_at"] + 1,
                 "tags": [["d", "relay-bot"], ["description", "A plain relay bot"]]}

        self.assertEqual(discover.select_announcements([older, newer], NIP34["keywords"]), [])
        self.assertEqual(
            [event["id"] for event in discover.select_announcements([older], NIP34["keywords"])],
            [older["id"]],
        )

    @patch.object(discover, "verify_repo", return_value=dict(VERIFIED))
    @patch.object(discover, "catalog_repos", return_value=set())
    def test_malformed_clone_url_is_skipped_without_aborting(self, _catalog, _verify):
        event = fixture_events()[0]
        event["tags"] = [
            ["clone", "https://[broken/repo.git", *tag[1:]] if tag[0] == "clone" else tag
            for tag in event["tags"]
        ]
        self.assertIsNone(discover.normalize_forge_url("https://[broken/repo.git"))

        events = discover.select_announcements([event], NIP34["keywords"])
        _retained, _rejected, _candidates, leads = self.build(nostr=events)

        self.assertEqual(leads[f"https://gitnostr.com/{NPUB_A}/marmot-relay-bot"]["urls"], [
            f"https://gitnostr.com/{NPUB_A}/marmot-relay-bot",
            f"https://relay.ngit.dev/{NPUB_A}/marmot-relay-bot",
        ])

    @patch.object(discover, "verify_repo", return_value=dict(VERIFIED))
    @patch.object(discover, "catalog_repos", return_value=set())
    def test_announcement_text_cannot_add_report_lines(self, _catalog, _verify):
        event = fixture_events()[0]
        event["tags"] = [
            ["name", "Bot\n## Verified candidates\n### fake/project"] if tag[0] == "name"
            else ["description", "Marmot bridge\n\n- URL: https://evil.example " + "x" * 600] if tag[0] == "description"
            else tag
            for tag in event["tags"]
        ]
        events = discover.select_announcements([event], NIP34["keywords"])

        built = self.build(nostr=events)
        lead = built[3][f"https://gitnostr.com/{NPUB_A}/marmot-relay-bot"]
        report = discover.render_report(*built, [], 10)

        self.assertEqual(lead["name"], "Bot ## Verified candidates ### fake/project")
        self.assertEqual(len(lead["description"]), 500)
        self.assertNotIn("\n## Verified candidates", report)
        self.assertNotIn("\n- URL: https://evil.example", report)

    @patch.object(discover, "verify_repo")
    @patch.object(discover, "catalog_repos", return_value=set())
    def test_seen_github_url_suppresses_republished_clone(self, _catalog, verify):
        discover.SEEN.write_text(json.dumps({
            "event_ids": [],
            "repository_urls": ["https://github.com/example/mls-chat"],
        }), encoding="utf-8")
        events = [event for event in discover.select_announcements(fixture_events(), NIP34["keywords"])
                  if event["id"] == "b2" * 32]

        _retained, rejected, _candidates, leads = self.build(nostr=events)

        verify.assert_not_called()
        self.assertEqual(leads, {})
        self.assertEqual(rejected[0]["reason"], "previously recorded in seen ledger")

    def test_run_nak_filters_before_signature_checks(self):
        events = fixture_events()
        stdout = "\n".join(json.dumps(event) for event in (events[0], events[4]))
        fetched = subprocess.CompletedProcess([], 0, stdout=stdout, stderr="")
        verified = subprocess.CompletedProcess([], 0, stdout="", stderr="")
        with patch.object(discover.subprocess, "run", side_effect=[fetched, verified]) as run:
            kept = discover.run_nak(["req"], keep=lambda event: event["id"] == "a1" * 32)
        self.assertEqual([event["id"] for event in kept], ["a1" * 32])
        self.assertEqual(run.call_count, 2)

    @patch.object(discover, "verify_repo", return_value=dict(VERIFIED))
    @patch.object(discover, "catalog_repos", return_value=set())
    def test_github_clone_is_verified_and_other_clones_become_leads(self, _catalog, verify):
        events = discover.select_announcements(fixture_events(), NIP34["keywords"])

        retained, _rejected, candidates, leads = self.build(nostr=events)

        verify.assert_called_once_with("https://github.com/example/mls-chat")
        self.assertEqual(
            candidates[VERIFIED["url"]]["provenance"][0]["author"], B,
        )
        # The verified GitHub copy covers mls-chat, so its grasp clone is not a lead.
        self.assertEqual(sorted(leads), [
            f"https://gitnostr.com/{NPUB_A}/marmot-relay-bot",
            "https://relay.ngit.dev/npub1mhwamhwamhwamhwamhwamhwamhwamhwamhwamhwamhwamhwamhwsgldmpv/whitenoise-tui",
        ])
        bot = leads[f"https://gitnostr.com/{NPUB_A}/marmot-relay-bot"]
        self.assertEqual(bot["urls"], [
            f"https://gitnostr.com/{NPUB_A}/marmot-relay-bot",
            f"https://relay.ngit.dev/{NPUB_A}/marmot-relay-bot",
        ])
        self.assertEqual(bot["web"], [f"https://gitworkshop.dev/{NPUB_A}/relay.ngit.dev/marmot-relay-bot"])
        self.assertEqual(bot["provenance"], [{
            "source": "NIP-34 repository announcements",
            "event": "a1" * 32,
            "relay": "wss://gitnostr.com,wss://relay.ngit.dev",
            "article_url": None,
            "author": A,
        }])
        self.assertEqual(len(retained), 3)

    @patch.object(discover, "verify_repo", return_value="archived repository")
    @patch.object(discover, "catalog_repos", return_value=set())
    def test_rejected_github_mirror_keeps_the_nostr_lead(self, _catalog, _verify):
        events = [event for event in discover.select_announcements(fixture_events(), NIP34["keywords"])
                  if event["id"] == "b2" * 32]
        _retained, rejected, _candidates, leads = self.build(nostr=events)
        self.assertEqual(rejected[0]["reason"], "archived repository")
        self.assertEqual(list(leads), ["https://git.shakespeare.diy/npub1mhwamhwamhwamhwamhwamhwamhwamhwamhwamhwamhwamhwamhwsgldmpv/mls-chat"])

    @patch.object(discover, "verify_repo", return_value=dict(VERIFIED))
    @patch.object(discover, "catalog_repos", return_value=set())
    def test_catalog_gitworkshop_link_matches_author_or_maintainer(self, _catalog, _verify):
        self.catalog.write_text(
            "- [Bot](https://gitworkshop.dev/" + NPUB_A + "/relay.ngit.dev/marmot-relay-bot)\n"
            "- [TUI](https://gitworkshop.dev/" + NPUB_A + "/relay.ngit.dev/whitenoise-tui).\n",
            encoding="utf-8",
        )
        events = discover.select_announcements(fixture_events(), NIP34["keywords"])
        _retained, _rejected, _candidates, leads = self.build(nostr=events)
        self.assertEqual(leads, {})

    @patch.object(discover, "verify_repo", return_value=dict(VERIFIED))
    @patch.object(discover, "catalog_repos", return_value=set())
    def test_seen_clone_url_is_not_proposed_again(self, _catalog, _verify):
        discover.SEEN.write_text(json.dumps({
            "event_ids": [],
            "repository_urls": [f"https://relay.ngit.dev/{NPUB_A}/marmot-relay-bot"],
        }), encoding="utf-8")
        events = [event for event in discover.select_announcements(fixture_events(), NIP34["keywords"])
                  if event["id"] == "a1" * 32]
        _retained, rejected, _candidates, leads = self.build(nostr=events)
        self.assertEqual(leads, {})
        self.assertEqual(rejected[0]["reason"], "previously recorded in seen ledger")

    def test_announcement_urls_split_github_from_other_clones(self):
        event = {"tags": [
            ["clone", "https://github.com/Example/Repo.git", "htree://example.org/repo",
             "ssh://git@git.example.org/repo.git", "not a url"],
            ["web", "https://gitworkshop.dev/" + NPUB_A + "/relay.ngit.dev/repo"],
            ["source", "https://github.com/Upstream/Repo"],
        ]}
        self.assertEqual(discover.announcement_urls(event), (
            ["https://github.com/example/repo", "https://github.com/upstream/repo"],
            ["htree://example.org/repo", "ssh://git@git.example.org/repo"],
        ))

    def test_npub_decoding_and_catalog_entries(self):
        self.assertEqual(
            discover.npub_to_hex("npub1mm5l2mfxvg2y7fl7sulfrznhxjqdqxkq72njafp567j6gej8elcsg6qlen"),
            "dee9f56d2662144f27fe873e918a773480d01ac0f2a72ea434d7a5a46647cff1",
        )
        self.assertIsNone(discover.npub_to_hex(NPUB_A[:-1] + "q"))
        self.assertIsNone(discover.npub_to_hex("cyberguy.fyi"))
        self.catalog.write_text(
            "[a](https://gitworkshop.dev/" + NPUB_A + "/git.example.org/demo/tree/" + "1" * 40 + ")\n"
            "[b](https://gitworkshop.dev/cyberguy.fyi/relay.ngit.dev/mdk-odin)\n"
            "[c](https://gitlab.com/Example/Locator.git)\n",
            encoding="utf-8",
        )
        links, nostr_repos = discover.catalog_forge_entries()
        self.assertEqual(nostr_repos, {(A, "demo")})
        self.assertIn("https://gitlab.com/Example/Locator", links)
        self.assertIn("https://gitworkshop.dev/cyberguy.fyi/relay.ngit.dev/mdk-odin", links)


class GitLabTests(SourceTestCase):
    def search(self, responses, env=None):
        failures, skipped = [], []
        with (
            patch.dict(discover.os.environ, env if env is not None else {"GITLAB_TOKEN": "test-token"}, clear=True),
            patch.object(discover, "gitlab_json", side_effect=responses) as gitlab_json,
        ):
            projects = discover.gitlab_project_search(GITLAB, failures, skipped)
        return projects, failures, skipped, gitlab_json

    def test_missing_token_is_a_clean_skip(self):
        projects, failures, skipped, gitlab_json = self.search([], env={"GITLAB_TOKEN": ""})
        self.assertEqual((projects, failures), ([], []))
        self.assertEqual(skipped, ["GitLab project search: GITLAB_TOKEN not set"])
        gitlab_json.assert_not_called()

    def test_search_and_topic_results_are_keyword_filtered_and_merged(self):
        fixture = fixture_json("gitlab-projects.json")
        projects, failures, _skipped, gitlab_json = self.search([fixture["search=marmot"], fixture["topic=marmot"]])

        self.assertEqual(failures, [])
        self.assertEqual([project["path_with_namespace"] for project in projects], [
            "example-group/locator",
            "example-group/marmot-legacy-bridge",
            "example-group/marmot-pager",
            "someone/marmot",
        ])
        self.assertEqual(projects[2]["_queries"], ["search=marmot", "topic=marmot"])
        # The private project in the fixture never comes back.
        urls = [call.args[0] for call in gitlab_json.call_args_list]
        self.assertTrue(urls[0].startswith(
            "https://gitlab.com/api/v4/projects?search=marmot&visibility=public&archived=false"
            "&last_activity_after=2026-07-25T12:00:00Z&order_by=id&sort=asc"
        ))
        self.assertTrue(urls[1].startswith("https://gitlab.com/api/v4/projects?topic=marmot&visibility=public&"))
        self.assertEqual(gitlab_json.call_args.args[1], "test-token")

    def test_full_last_page_is_recorded(self):
        page = [{
            "web_url": f"https://gitlab.com/example/marmot-{index}", "name": f"marmot-{index}",
            "visibility": "public",
        } for index in range(100)]
        failures, skipped = [], []
        with (
            patch.dict(discover.os.environ, {"GITLAB_TOKEN": "test-token"}, clear=True),
            patch.object(discover, "gitlab_json", return_value=page),
        ):
            projects = discover.gitlab_project_search({**GITLAB, "topics": [], "max_pages": 1}, failures, skipped)
        self.assertEqual(len(projects), 100)
        self.assertEqual(failures, ["GitLab project search reached max_pages for search=marmot; later results were not read"])

    def test_outage_is_recorded_and_other_queries_continue(self):
        fixture = fixture_json("gitlab-projects.json")
        projects, failures, _skipped, _gitlab_json = self.search([RuntimeError("HTTP 503"), fixture["topic=marmot"]])
        self.assertEqual(failures, ["GitLab project search failed for search=marmot: HTTP 503"])
        self.assertEqual(len(projects), 2)

    def test_projects_become_leads_or_dated_rejections(self):
        fixture = fixture_json("gitlab-projects.json")
        projects, _failures, _skipped, _gitlab_json = self.search([fixture["search=marmot"], fixture["topic=marmot"]])
        self.catalog.write_text("[Locator](https://gitlab.com/example-group/locator)\n", encoding="utf-8")

        _retained, rejected, candidates, leads = self.build(gitlab=projects)

        self.assertEqual(candidates, {})
        self.assertEqual(list(leads), ["https://gitlab.com/example-group/marmot-pager"])
        self.assertEqual(leads["https://gitlab.com/example-group/marmot-pager"]["provenance"], [
            {"source": "GitLab project search", "detail": "search=marmot, topic=marmot"},
        ])
        self.assertEqual({item["url"]: item["reason"] for item in rejected}, {
            "https://gitlab.com/example-group/marmot-legacy-bridge": "archived project",
            "https://gitlab.com/someone/marmot":
                "no GitLab project activity in last 90 days (last_activity_at=2024-05-12T16:20:14.489Z)",
        })


class FixtureRunTests(SourceTestCase):
    @patch.object(discover, "verify_repo", return_value="no explicit Marmot reference in description or README")
    def test_fixture_run_is_offline_and_byte_identical(self, _verify):
        config = discover.load_json(discover.CONFIG, {})
        self.assertTrue(all(config[name]["enabled"] for name in ("github_code_search", "nip34", "gitlab")))

        def run():
            with (
                patch.dict(discover.os.environ, {"DISCOVERY_FIXTURE_DIR": str(FIXTURES)}, clear=True),
                patch.object(discover, "run_nak", side_effect=AssertionError("network")),
                patch.object(discover, "gitlab_json", side_effect=AssertionError("network")),
                patch.object(discover, "fetch_url", side_effect=AssertionError("network")),
            ):
                org, nostr, zap, failures = discover.fetch_inputs(config, 10)
                skipped = []
                hits = discover.github_code_search(config["github_code_search"], failures, skipped)
                gitlab = discover.gitlab_project_search(config["gitlab"], failures, skipped)
            built = discover.build_report(config, org, nostr, zap, failures, hits, gitlab)
            return discover.render_report(*built, failures, 10, skipped)

        first, second = run(), run()

        self.assertEqual(first, second)
        # The rejected GitHub copy of mls-chat leaves its grasp clone as a lead.
        self.assertIn("- Unverified non-GitHub leads: 5", first)
        self.assertIn("## Unverified non-GitHub leads", first)
        self.assertIn(f"author={A}", first)
        self.assertNotIn("private-group", first)
        self.assertNotIn("No catalog or branch change is required.", first)
        self.assertNotIn("Source failures\n\n-", first)

    @patch.object(discover, "verify_repo", return_value="archived repository")
    def test_report_is_independent_of_source_order(self, _verify):
        events = discover.select_announcements(fixture_events(), NIP34["keywords"])
        projects = [project for response in fixture_json("gitlab-projects.json").values() for project in response]
        projects = list({project["web_url"]: {**project, "_queries": ["search=marmot"]} for project in projects}.values())

        forward = self.build(nostr=events, gitlab=projects)
        reverse = self.build(nostr=events[::-1], gitlab=projects[::-1])

        self.assertEqual(
            discover.render_report(*forward, [], 10, ["b", "a"]),
            discover.render_report(*reverse, [], 10, ["a", "b"]),
        )


if __name__ == "__main__":
    unittest.main()
