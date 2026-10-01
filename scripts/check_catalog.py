#!/usr/bin/env python3
"""Offline catalog checks against the dated, reviewed evidence snapshot."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
GENERATIONS = {"v2", "v1", "transitional", "unknown", "adjacent"}
ACTIVITIES = {"active", "inactive", "archived", "unverified"}


def canonical_repository(url: str) -> str:
    parts = urlsplit(url)
    path = "/".join(parts.path.strip("/").split("/")[:2]).removesuffix(".git")
    return f"{parts.scheme.lower()}://{parts.netloc.lower()}/{path.lower()}"


def check_catalog(text: str, audit: dict) -> list[str]:
    errors = []
    try:
        checked = dt.datetime.fromisoformat(audit["checked_at"].replace("Z", "+00:00"))
        if checked.tzinfo is None or audit["activity_window_days"] != 90:
            raise ValueError("expected timezone and 90-day window")
        records = audit["repositories"]
        if not isinstance(records, list) or not records:
            raise ValueError("empty repository inventory")
    except (KeyError, TypeError, ValueError, AttributeError):
        return ["invalid audit timestamp, window, or inventory"]

    repositories = {}
    for record in records:
        try:
            url = record["repository"]
            key = canonical_repository(url)
            if not url.startswith("https://") or key in repositories:
                raise ValueError("invalid or duplicate repository URL")
            repositories[key] = record
            generation, activity = record["generation"], record["activity"]
            if generation not in GENERATIONS or activity not in ACTIVITIES:
                raise ValueError("invalid labels")
            if not record["source"].startswith("https://") or not record["note"]:
                raise ValueError("missing primary source or note")
            if activity == "unverified":
                if generation != "unknown" or any(
                    field in record for field in ("commit", "last_commit_at", "default_branch")
                ):
                    raise ValueError("unverified source must not claim commit or generation")
                continue
            committed = dt.datetime.fromisoformat(record["last_commit_at"].replace("Z", "+00:00"))
            if committed.tzinfo is None or committed > checked:
                raise ValueError("invalid or future commit timestamp")
            if not re.fullmatch(r"[0-9a-f]{40}", record["commit"]) or not record["default_branch"]:
                raise ValueError("missing immutable commit or default branch")
            if record["commit"] not in record["source"]:
                raise ValueError("source must be pinned to the checked commit")
            archived = record["github_archived"]
            deprecated = record.get("deprecation_evidence")
            if not isinstance(archived, bool):
                raise ValueError("invalid archive flag")
            if deprecated and (record["commit"] not in deprecated or not deprecated.startswith(url + "/")):
                raise ValueError("deprecation needs pinned maintainer evidence")
            expected = (
                "archived" if archived or deprecated else
                "active" if committed >= checked - dt.timedelta(days=90) else "inactive"
            )
            if activity != expected:
                raise ValueError(f"activity should be {expected}, not {activity}")
        except (KeyError, TypeError, ValueError, AttributeError) as error:
            errors.append(f"invalid audit record: {record.get('repository', 'unknown')}: {error}")

    seen = set()
    entry_urls = set()
    section = ""
    section_for = {
        ("active", "v2"): "Marmot v2 — recently updated",
        ("active", "v1"): "Marmot v1 — recently updated",
        ("active", "transitional"): "Migrating or version not yet verified",
        ("active", "unknown"): "Migrating or version not yet verified",
        ("active", "adjacent"): "Supporting tools — recently updated",
    }
    for number, line in enumerate(text.splitlines(), 1):
        if line.startswith("## "):
            section = line[3:]
        if not (line.startswith("- [") and "](https://" in line):
            continue
        match = re.match(r"- \[[^\]]+\]\((https://[^)]+)\) — \*\*([^*]+)\*\* — ", line)
        if not match:
            errors.append(f"entry needs a link, explicit labels and description at line {number}")
            continue
        url, label_text = match.groups()
        if url.lower() in entry_urls:
            errors.append(f"duplicate entry: {url}")
        entry_urls.add(url.lower())
        labels = [label.strip() for label in label_text.split(",")]
        if len(labels) < 2 or labels[0] not in GENERATIONS or labels[1] not in ACTIVITIES:
            errors.append(f"invalid exact generation/activity labels at line {number}")
            continue
        key = canonical_repository(url)
        seen.add(key)
        record = repositories.get(key)
        if not record:
            errors.append(f"entry missing from audit: {url}")
            continue
        if labels[:2] != [record["generation"], record["activity"]]:
            errors.append(f"entry labels disagree with evidence: {url}")
        if labels[1] == "inactive" and record.get("last_commit_at", "")[:10] not in line:
            errors.append(f"inactive entry must show last commit date: {url}")
        expected_section = section_for.get(tuple(reversed(labels[:2]))) or {
            "inactive": "No recent public commits",
            "archived": "Archived and superseded",
            "unverified": "Source unavailable at the last check",
        }.get(labels[1])
        if section != expected_section:
            errors.append(f"entry in wrong section: {url}")
    for key in repositories.keys() - seen:
        errors.append(f"audited repository missing from catalog: {key}")

    required = (
        "Marmot for Hermes", "Marmot for OpenClaw", "wn-codex", "wn-claude",
        "wn-opencode", "wn-pi", "https://github.com/marmot-protocol/mdk/tree/master/crates/cli",
    )
    for fragment in required:
        if fragment not in text:
            errors.append(f"missing current first-party entry: {fragment}")
    legend = text.find("## What the labels mean")
    if legend < text.find("## Archived and superseded") or legend < 0:
        errors.append("legend must follow the catalog")
    if f"**Checked {checked.date().isoformat()}.**" not in text:
        errors.append("README audit date must match the snapshot")
    for obsolete in ("current-spec", "legacy-spec", "365-day", "last 12 months",
                     "https://github.com/marmot-protocol/mdk-web",
                     "https://github.com/marmot-protocol/mdk-ruby-example"):
        if obsolete in text:
            errors.append(f"obsolete catalog content: {obsolete}")
    return errors


def main() -> int:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    audit = json.loads((ROOT / "data/catalog-audit.json").read_text(encoding="utf-8"))
    errors = check_catalog(text, audit)
    # Check relative README links and fragment targets without network access.
    anchors = {
        re.sub(r"[^\w -]", "", line.lstrip("# ").lower()).replace(" ", "-")
        for line in text.splitlines() if line.startswith("#")
    }
    for target in re.findall(r"\]\(([^)]+)\)", text):
        if target.startswith("#") and target[1:] not in anchors:
            errors.append(f"broken README anchor: {target}")
        elif not target.startswith(("https://", "#")) and not (ROOT / target).is_file():
            errors.append(f"missing local README destination: {target}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"catalog OK: {len(audit['repositories'])} repositories, 90-day evidence and labels checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
