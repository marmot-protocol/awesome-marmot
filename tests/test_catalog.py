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
            ("Last commit: **2026-04-01**", "Last commit: **2026-09-30**"),
        ):
            with self.subTest(new=new):
                self.assertTrue(self.check(text=self.text.replace(old, new, 1)))

    def test_generation_is_not_inferred_from_name(self):
        record = next(r for r in self.audit["repositories"] if "Tubestr" in r["repository"])
        self.assertEqual(record["generation"], "unknown")

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


if __name__ == "__main__":
    unittest.main()
