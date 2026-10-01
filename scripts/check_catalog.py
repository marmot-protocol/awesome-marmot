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
GENERATIONS = {"v2", "v1", "unknown", "adjacent"}
ACTIVITIES = {"active", "inactive", "archived", "unverified"}
MONOREPOS = {
    "https://github.com/marmot-protocol/mdk",
    "https://github.com/vitorpamplona/amethyst",
}


def canonical_repository(url: str) -> str:
    parts = urlsplit(url)
    path = parts.path.strip("/")
    if parts.netloc.lower() == "gitlab.com":
        path = path.split("/-/")[0]
    else:
        path = "/".join(path.split("/")[:2])
    path = path.removesuffix(".git")
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
        if not isinstance(record, dict):
            errors.append("invalid audit record: expected an object")
            continue
        try:
            url = record["repository"]
            key = canonical_repository(url)
            if not url.startswith("https://") or key in repositories:
                raise ValueError("invalid or duplicate repository URL")
            generation, activity = record["generation"], record["activity"]
            if generation not in GENERATIONS or activity not in ACTIVITIES:
                raise ValueError("invalid labels")
            if activity == "active" and generation == "unknown" and record.get("source_kind") != "store-metadata":
                raise ValueError("active source implementation needs a verified protocol generation")
            if not record["source"].startswith("https://") or not record["note"]:
                raise ValueError("missing primary source or note")
            evidence = record.get("generation_evidence")
            if evidence is not None:
                if not isinstance(evidence, list) or not evidence:
                    raise ValueError("generation evidence must be a nonempty list")
                for target in evidence:
                    if not isinstance(target, str) or not target.startswith("https://"):
                        raise ValueError("invalid generation evidence URL")
                    if urlsplit(target).netloc.lower() == "github.com":
                        if not re.search(r"/(blob|tree)/[0-9a-f]{40}(/|$)", target):
                            raise ValueError("generation evidence must be immutable")
                    elif urlsplit(target).netloc.lower() == "registry.npmjs.org":
                        if not re.fullmatch(r"sha512-[A-Za-z0-9+/]{86}==", record.get("dependency_integrity", "")):
                            raise ValueError("registry evidence needs package integrity")
            if activity == "unverified":
                if generation != "unknown" or any(
                    field in record for field in ("commit", "last_commit_at", "default_branch")
                ):
                    raise ValueError("unverified source must not claim commit or generation")
                repositories[key] = record
                continue
            committed = dt.datetime.fromisoformat(record["last_commit_at"].replace("Z", "+00:00"))
            if committed.tzinfo is None or committed > checked:
                raise ValueError("invalid or future commit timestamp")
            if not re.fullmatch(r"[0-9a-f]{40}", record["commit"]) or not record["default_branch"]:
                raise ValueError("missing immutable commit or default branch")
            if record["commit"] not in record["source"]:
                raise ValueError("source must be pinned to the checked commit")
            if evidence and not any(record["commit"] in target for target in evidence):
                raise ValueError("generation evidence must include the checked repository commit")
            archived = record["archived"]
            deprecated = record.get("deprecation_evidence")
            if not isinstance(archived, bool) and not (
                archived is None and urlsplit(url).netloc.lower() != "github.com"
            ):
                raise ValueError("invalid archive flag")
            if deprecated and (record["commit"] not in deprecated or not deprecated.startswith(url + "/")):
                raise ValueError("deprecation needs pinned maintainer evidence")
            expected = (
                "archived" if archived or deprecated else
                "active" if committed >= checked - dt.timedelta(days=90) else "inactive"
            )
            if activity != expected:
                raise ValueError(f"activity should be {expected}, not {activity}")
            historical = record.get("historical_source")
            if historical and not re.fullmatch(
                re.escape(url) + r"/blob/[0-9a-f]{40}/.+", historical
            ):
                raise ValueError("historical source must be immutable and in the same repository")
            repositories[key] = record
        except (KeyError, TypeError, ValueError, AttributeError) as error:
            errors.append(f"invalid audit record: {record.get('repository', 'unknown')}: {error}")

    seen = set()
    entry_urls = set()
    section = ""
    section_for = {
        ("active", "v2"): "Marmot v2 — recently updated",
        ("active", "v1"): "Marmot v1 — recently updated",
        ("active", "unknown"): "Closed-source apps",
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
        normalized_entry = url.lower().rstrip("/")
        if normalized_entry in entry_urls:
            errors.append(f"duplicate entry: {url}")
        entry_urls.add(normalized_entry)
        labels = [label.strip() for label in label_text.split(",")]
        if len(labels) < 2 or labels[0] not in GENERATIONS or labels[1] not in ACTIVITIES:
            errors.append(f"invalid exact generation/activity labels at line {number}")
            continue
        key = canonical_repository(url)
        if key in seen and key not in MONOREPOS:
            errors.append(f"duplicate canonical repository entry: {url}")
        seen.add(key)
        record = repositories.get(key)
        if not record:
            errors.append(f"entry missing from audit: {url}")
            continue
        if labels[:2] != [record.get("generation"), record.get("activity")]:
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
                     "Migrating or version not yet verified", "**transitional",
                     "https://github.com/marmot-protocol/mdk-web",
                     "https://github.com/marmot-protocol/mdk-ruby-example"):
        if obsolete in text:
            errors.append(f"obsolete catalog content: {obsolete}")
    return errors


def check_local_links(text: str, root: Path) -> list[str]:
    """Check README relative destinations and fragment targets offline."""
    errors = []
    anchors = {
        re.sub(r"[^\w -]", "", line.lstrip("# ").lower()).replace(" ", "-")
        for line in text.splitlines() if line.startswith("#")
    }
    for target in re.findall(r"\]\(([^)]+)\)", text):
        if target.startswith("#") and target[1:] not in anchors:
            errors.append(f"broken README anchor: {target}")
        elif not target.startswith(("https://", "#")) and not (root / target).is_file():
            errors.append(f"missing local README destination: {target}")
    return errors


def main() -> int:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    audit = json.loads((ROOT / "data/catalog-audit.json").read_text(encoding="utf-8"))
    errors = check_catalog(text, audit) + check_local_links(text, ROOT)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"catalog OK: {len(audit['repositories'])} repositories, 90-day evidence and labels checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
