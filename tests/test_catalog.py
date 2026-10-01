import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location("check_catalog", ROOT / "scripts/check_catalog.py")
catalog = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(catalog)


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.audit = json.loads((ROOT / "data/catalog-audit.json").read_text(encoding="utf-8"))

    def check(self, text=None, audit=None):
        return catalog.check_catalog(
            self.text if text is None else text,
            self.audit if audit is None else audit,
        )

    def test_reviewed_inventory_passes(self):
        self.assertEqual(self.check(), [])

    def test_all_previous_repositories_are_retained(self):
        urls = [r["repository"] for r in self.audit["repositories"]]
        self.assertEqual(len(set(urls)), len(urls))
        baseline = json.loads((ROOT / "tests/fixtures/catalog-repositories-20260909.json").read_text())
        current = {catalog.canonical_repository(url) for url in urls}
        self.assertTrue(set(baseline).issubset(current))

    def test_activity_is_an_exact_label_not_a_substring(self):
        text = self.text.replace("**v1, inactive, alpha**", "**v1, inactiveish, alpha**", 1)
        self.assertTrue(any("exact" in error for error in self.check(text=text)))

    def test_labels_and_last_dates_must_match_snapshot(self):
        for old, new in (
            ("**v1, inactive, alpha**", "**v2, active, alpha**"),
            ("**2026-04-01**", "**2026-09-30**"),
        ):
            with self.subTest(new=new):
                self.assertTrue(self.check(text=self.text.replace(old, new, 1)))

    def test_generation_is_not_inferred_from_name(self):
        record = next(r for r in self.audit["repositories"] if "Tubestr" in r["repository"])
        self.assertEqual(record["generation"], "v1")
        self.assertTrue(any("native/mdk_bridge/Cargo.toml" in url for url in record["generation_evidence"]))

    def test_source_verified_generations_replace_catch_all(self):
        expected = {
            "Haven-App": "v2", "marmots-web-chat": "v2", "whistle": "v1",
            "tubestr-v2": "v1", "marmot-server": "v1", "openclaw-marmot": "v1",
            "quartz": "adjacent",
        }
        for name, generation in expected.items():
            with self.subTest(name=name):
                record = next(r for r in self.audit["repositories"] if r["repository"].endswith("/" + name))
                self.assertEqual(record["generation"], generation)
                self.assertTrue(record["generation_evidence"])
                self.assertTrue(any(record["commit"] in url for url in record["generation_evidence"]))
        self.assertNotIn("Migrating or version not yet verified", self.text)
        self.assertNotIn("transitional", catalog.GENERATIONS)

    def test_unknown_active_implementation_is_rejected(self):
        record = next(r for r in self.audit["repositories"] if r["repository"].endswith("/whistle"))
        record["generation"] = "unknown"
        self.assertTrue(any("verified protocol generation" in e for e in self.check()))

    def test_private_source_is_not_fabricated_as_verified(self):
        record = next(r for r in self.audit["repositories"] if r["repository"].endswith("/mafrend-zapstore"))
        self.assertEqual(record["source_kind"], "store-metadata")
        self.assertEqual(record["generation"], "unknown")

    def test_removed_catch_all_cannot_return(self):
        text = self.text.replace("## Closed-source apps", "## Migrating or version not yet verified")
        self.assertTrue(any("obsolete catalog" in e for e in self.check(text=text)))

    def test_classification_evidence_requires_immutable_source(self):
        record = next(r for r in self.audit["repositories"] if r["repository"].endswith("/Haven-App"))
        record["generation_evidence"][0] = record["repository"] + "/blob/main/haven-core/Cargo.toml"
        self.assertTrue(any("immutable" in e for e in self.check()))

    def test_registry_classification_requires_integrity(self):
        record = next(r for r in self.audit["repositories"] if r["repository"].endswith("/marmot-server"))
        del record["dependency_integrity"]
        self.assertTrue(any("package integrity" in e for e in self.check()))

    def test_deleted_entry_and_missing_audit_record_fail(self):
        lines = self.text.splitlines()
        removed = "\n".join(l for l in lines if not l.startswith("- [Pika]"))
        self.assertTrue(any("missing from catalog" in e for e in self.check(text=removed)))
        self.audit["repositories"].pop(0)
        self.assertTrue(any("missing from audit" in e for e in self.check()))

    def test_legend_belongs_below_catalog(self):
        text = "## What the labels mean\n\n" + self.text
        self.assertTrue(any("legend" in e for e in self.check(text=text)))

    def test_archived_overrides_recent_commit(self):
        record = next(r for r in self.audit["repositories"] if r["repository"].endswith("/whitenoise"))
        self.assertEqual(record["activity"], "archived")
        record["activity"] = "active"
        self.assertTrue(any("activity should be archived" in e for e in self.check()))

    def test_maintainer_deprecation_requires_pinned_evidence(self):
        record = next(r for r in self.audit["repositories"] if r["repository"].endswith("/wn-tui"))
        del record["deprecation_evidence"]
        self.assertTrue(any("activity should be active" in e for e in self.check()))

    def test_bad_or_future_commit_dates_fail(self):
        for value in ("not-a-date", "2026-10-02T00:00:00Z", "2026-09-30T00:00:00"):
            with self.subTest(value=value):
                audit = copy.deepcopy(self.audit)
                audit["repositories"][0]["last_commit_at"] = value
                self.assertTrue(self.check(audit=audit))

    def test_unavailable_source_has_no_invented_commit(self):
        record = next(r for r in self.audit["repositories"] if r["activity"] == "unverified")
        self.assertEqual(record["generation"], "unknown")
        record["commit"] = "a" * 40
        self.assertTrue(any("unverified source" in e for e in self.check()))

    def test_active_entry_cannot_be_hidden_in_legacy_section(self):
        text = self.text.replace("## Supporting tools — recently updated", "## No recent public commits")
        self.assertTrue(any("wrong section" in e for e in self.check(text=text)))

    def test_duplicate_entry_is_rejected(self):
        line = next(l for l in self.text.splitlines() if l.startswith("- [Pika]"))
        self.assertTrue(any("duplicate entry" in e for e in self.check(text=self.text + "\n" + line)))

    def test_window_is_fixed_at_ninety_days(self):
        self.audit["activity_window_days"] = 365
        self.assertTrue(self.check())

    def test_canonical_duplicate_with_trailing_slash_is_rejected(self):
        line = next(l for l in self.text.splitlines() if l.startswith("- [Pika]"))
        alias = line.replace("/justinmoon/pika)", "/justinmoon/pika/)")
        self.assertTrue(any("duplicate canonical" in e for e in self.check(text=self.text + "\n" + alias)))

    def test_missing_generation_and_non_object_records_report_errors(self):
        for change in ("missing_generation", "not_an_object"):
            with self.subTest(change=change):
                audit = copy.deepcopy(self.audit)
                if change == "missing_generation":
                    del audit["repositories"][0]["generation"]
                else:
                    audit["repositories"][0] = None
                self.assertTrue(self.check(audit=audit))

    def test_current_readme_links_pass(self):
        self.assertEqual(catalog.check_local_links(self.text, ROOT), [])

    def test_broken_anchor_is_rejected(self):
        errors = catalog.check_local_links("[missing](#does-not-exist)", ROOT)
        self.assertTrue(any("broken README anchor" in e for e in errors))

    def test_missing_local_file_is_rejected(self):
        errors = catalog.check_local_links("[missing](docs/not-a-real-file.md)", ROOT)
        self.assertTrue(any("missing local" in e for e in errors))

    def test_historical_source_must_be_immutable_and_same_repo(self):
        record = next(r for r in self.audit["repositories"] if "historical_source" in r)
        record["historical_source"] = record["repository"] + "/tree/flutter-final"
        self.assertTrue(any("historical source" in e for e in self.check()))

    def test_gitlab_subgroups_keep_distinct_repository_identities(self):
        first = catalog.canonical_repository("https://gitlab.com/team/subgroup/first/-/tree/master")
        second = catalog.canonical_repository("https://gitlab.com/team/subgroup/second")
        self.assertEqual(first, "https://gitlab.com/team/subgroup/first")
        self.assertNotEqual(first, second)

    def test_github_archive_metadata_cannot_be_unknown(self):
        self.audit["repositories"][0]["archived"] = None
        self.assertTrue(any("archive flag" in e for e in self.check()))

    def test_caveats_stay_at_bottom(self):
        notes = self.text.index("## Notes")
        last_entry = self.text.rindex("\n- [")
        self.assertGreater(notes, last_entry)
        for phrase in ("**Checked ", "maintenance guarantee", "not interchangeable", "security endorsement"):
            with self.subTest(phrase=phrase):
                self.assertGreater(self.text.index(phrase), notes)

    def test_older_sections_are_collapsible_without_dropping_entries(self):
        self.assertEqual(self.text.count("<details>"), 2)
        self.assertEqual(self.text.count("</details>"), 2)
        inactive = sum(r["activity"] == "inactive" for r in self.audit["repositories"])
        archived = sum(r["activity"] == "archived" for r in self.audit["repositories"])
        self.assertIn(f"<summary>{inactive} projects · last commit dates</summary>", self.text)
        self.assertIn(f"<summary>{archived} historical projects</summary>", self.text)
        self.assertEqual(self.check(), [])

    def test_linux_client_platforms_match_verified_evidence(self):
        record = next(r for r in self.audit["repositories"] if r["repository"].endswith("/whitenoise-linux"))
        self.assertEqual(record["platforms"], ["Linux", "Windows", "macOS", "OpenBSD"])
        self.assertIn(record["commit"], record["platform_evidence"])
        entry = next(l for l in self.text.splitlines() if l.startswith("- [White Noise for Linux]"))
        for platform in record["platforms"]:
            self.assertIn(platform, entry)
        self.assertNotIn("FreeBSD", entry)


if __name__ == "__main__":
    unittest.main()
