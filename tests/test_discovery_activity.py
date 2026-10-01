import copy
import datetime as dt
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("discover", Path(__file__).parents[1] / "scripts/discover.py")
discover = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(discover)
NOW = dt.datetime(2026, 10, 1, 12, tzinfo=dt.UTC)
REPO = {
    "archived": False, "private": False,
    "full_name": "example/marmot-app", "default_branch": "feature/default",
    "html_url": "https://github.com/example/marmot-app",
    "description": "Marmot client",
    "pushed_at": "2026-10-01T12:00:00Z",
}


def commit(date):
    return [{"sha": "a" * 40, "commit": {"committer": {"date": date}}}]


class ActivityTests(unittest.TestCase):
    def verify(self, commits, repo=None, status=404):
        with (
            patch.object(discover, "NOW", NOW),
            patch.object(discover, "api_json", side_effect=[repo or REPO, commits]) as api,
            patch.object(discover, "http_head_status", return_value=status),
        ):
            verdict = discover.verify_repo(REPO["html_url"])
        return verdict, api

    def test_ninety_day_boundary_is_inclusive(self):
        date = (NOW - dt.timedelta(days=90)).isoformat()
        verdict, api = self.verify(commit(date))
        self.assertIsInstance(verdict, dict)
        self.assertEqual(verdict["last_commit_at"], date)
        self.assertIn("sha=feature%2Fdefault&per_page=1", api.call_args_list[1].args[0])
        self.assertTrue(verdict["commit_url"].endswith("a" * 40))

    def test_recent_push_does_not_rescue_old_default_branch(self):
        date = (NOW - dt.timedelta(days=90, seconds=1)).isoformat()
        verdict, _ = self.verify(commit(date))
        self.assertIn("no default-branch commit in last 90 days", verdict)

    def test_old_push_does_not_override_fresh_commit(self):
        repo = {**REPO, "pushed_at": "2020-01-01T00:00:00Z"}
        verdict, _ = self.verify(commit(NOW.isoformat()), repo)
        self.assertIsInstance(verdict, dict)

    def test_future_naive_malformed_and_empty_dates_fail_closed(self):
        for value in (
            "2026-10-02T00:00:00Z", "2026-09-30T00:00:00",
            "invalid", None, "",
        ):
            with self.subTest(value=value):
                verdict, _ = self.verify(commit(value))
                self.assertIsInstance(verdict, str)

    def test_missing_or_malformed_commit_metadata_is_unverified(self):
        for commits in ([], {}, [None], [{"sha": "a" * 40}], commit(NOW.isoformat())):
            broken = copy.deepcopy(commits)
            if isinstance(broken, list) and broken and isinstance(broken[0], dict) and "commit" in broken[0]:
                broken[0]["sha"] = "not-a-commit"
            with self.subTest(commits=broken):
                verdict, _ = self.verify(broken)
                self.assertIsInstance(verdict, str)

    def test_archive_and_private_gates_precede_commit_lookup(self):
        for field in ("archived", "private"):
            verdict, api = self.verify(commit(NOW.isoformat()), {**REPO, field: True})
            self.assertIsInstance(verdict, str)
            self.assertEqual(api.call_count, 1)

    def test_commit_lookup_outage_is_a_rejection_not_abandonment(self):
        verdict, _ = self.verify(RuntimeError("HTTP 503"))
        self.assertIn("lookup failed", verdict)
        self.assertNotIn("no default-branch commit", verdict)

    def test_readme_fetch_failure_is_bounded(self):
        with patch.object(discover, "fetch_url", side_effect=RuntimeError("HTTP 503")):
            verdict, _ = self.verify(commit(NOW.isoformat()), status=200)
        self.assertIn("README lookup failed", verdict)

    def test_readme_is_pinned_to_the_checked_commit(self):
        with patch.object(discover, "fetch_url", return_value="Marmot") as fetch:
            verdict, _ = self.verify(commit(NOW.isoformat()), status=200)
        self.assertIsInstance(verdict, dict)
        self.assertIn("/" + "a" * 40 + "/README.md", fetch.call_args.args[0])

    def test_missing_default_branch_is_not_active(self):
        verdict, api = self.verify(commit(NOW.isoformat()), {**REPO, "default_branch": None})
        self.assertIn("default branch unavailable", verdict)
        self.assertEqual(api.call_count, 1)


if __name__ == "__main__":
    unittest.main()
