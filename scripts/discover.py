#!/usr/bin/env python3
"""Weekly Marmot discovery: collect, verify, and report catalog candidates.

Inputs arrive in deterministic order (sorted by event id / repository name) so
repeated runs over identical source data produce byte-identical reports.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.error
import urllib.request
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/discovery-sources.json"
SEEN = ROOT / "data/discovery-seen.json"
CATALOG = ROOT / "README.md"
NOW = dt.datetime.now(dt.UTC)
CUTOFF = NOW - dt.timedelta(days=365)
GITHUB_API = "https://api.github.com"
USER_AGENT = "awesome-marmot-discovery/1.0 (+https://github.com/marmot-protocol/awesome-marmot)"

GITHUB_REPO = re.compile(r"https?://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)")
REPO_URL = re.compile(
    r"https?://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?",
    re.I,
)


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default


def api_json(url: str, fixture_name: str | None = None):
    fixture_dir = os.environ.get("DISCOVERY_FIXTURE_DIR")
    if fixture_dir and fixture_name:
        fixture = Path(fixture_dir) / fixture_name
        if fixture.exists():
            return json.loads(fixture.read_text(encoding="utf-8"))
    request = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
    })
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"GitHub API {url} -> HTTP {error.code}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"GitHub API {url} -> {error.reason}") from error


def github_org_repositories(organization: str) -> list[dict]:
    repositories: list[dict] = []
    page = 1
    while True:
        batch = api_json(
            f"{GITHUB_API}/orgs/{organization}/repos?per_page=100&type=public&page={page}",
            "github-org.json" if page == 1 else f"github-org-{page}.json",
        )
        repositories.extend(batch)
        if len(batch) < 100 or os.environ.get("DISCOVERY_FIXTURE_DIR"):
            return repositories
        page += 1


def run_nak(args: list[str]) -> list[dict]:
    """Run pinned nak and return verified Nostr events."""
    try:
        proc = subprocess.run(
            ["nak", *args], capture_output=True, text=True, check=False, timeout=45
        )
    except subprocess.TimeoutExpired as error:
        raise RuntimeError(f"nak {' '.join(args)} timed out after 45 seconds") from error
    if proc.returncode != 0:
        raise RuntimeError(f"nak {' '.join(args)} failed: {proc.stderr.strip()}")
    events = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        event = json.loads(line)
        # Belt-and-braces: verify each event signature with nak itself.
        try:
            check = subprocess.run(
                ["nak", "verify"], input=line, capture_output=True, text=True,
                check=False, timeout=10,
            )
        except subprocess.TimeoutExpired:
            continue
        if check.returncode != 0:
            continue
        events.append(event)
    events.sort(key=lambda event: event.get("id", ""))
    return events


def normalize_repo(url: str) -> str | None:
    match = GITHUB_REPO.search(url)
    if not match:
        return None
    owner, name = match.groups()
    name = name.removesuffix(".git")
    return f"https://github.com/{owner.lower()}/{name.lower()}"


def extract_repo_urls(event: dict) -> list[str]:
    """Return normalized GitHub repository URLs from an event.

    Covers plain-text content, Zapstore-style ``repository``/``homepage`` tags,
    and NIP-19 ``naddr`` references that encode an ``r`` URL hint.
    """
    found: set[str] = set()
    haystacks = [event.get("content", "")]
    for tag in event.get("tags", []):
        if tag and tag[0] in {"r", "repository", "homepage"} and len(tag) > 1:
            haystacks.append(str(tag[1]))
        if tag and tag[0] == "a" and len(tag) > 1 and "github.com" in str(tag[1]):
            haystacks.append(str(tag[1]))
    for text in haystacks:
        for candidate in REPO_URL.findall(text):
            normalized = normalize_repo(candidate)
            if normalized:
                found.add(normalized)
    return sorted(found)


def extract_zapstore_repos(event: dict) -> list[str]:
    """Extract candidate repositories from a kind-32267 Zapstore app event.

    Repository and homepage URLs live in event tags (``repository``,
    ``homepage``, ``r``); ``content`` is the app description and usually
    contains no repository URL.
    """
    return extract_repo_urls(event)


def fetch_url(url: str) -> str:
    """Fetch a URL and return the response body as text."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"HTTP {error.code}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(str(error.reason)) from error


def http_head_status(url: str) -> int | None:
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return response.status
    except urllib.error.HTTPError as error:
        return error.code
    except (urllib.error.URLError, ValueError):
        return None


def html_to_text(raw: str) -> str:
    raw = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(
        r'''(?is)<a\b[^>]*\bhref=["']([^"']+)["'][^>]*>''',
        lambda match: f" {html.unescape(match.group(1))} ",
        raw,
    )
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", raw))).strip()


def fetch_anchor_articles(events: list[dict], failures: list[str]) -> list[dict]:
    """Fetch article bodies linked from NostrMag-style anchor events.

    Anchor events are signed article shares whose ``r`` tags (and content)
    point to the weekly roundup page. The repository leads live in that
    article body, so it is fetched, HTML-stripped, and kept as a synthetic
    event for downstream extraction. The source event id is retained so the
    seen-ledger and report still reference the signed event, never the URL.
    """
    articles: list[dict] = []
    fixture_dir = os.environ.get("DISCOVERY_FIXTURE_DIR")
    for event in events:
        if event.get("_source") != "NostrMag weekly issues":
            continue
        article_urls: set[str] = set()
        for tag in event.get("tags", []):
            if tag and tag[0] == "r" and len(tag) > 1 and str(tag[1]).startswith("http"):
                article_urls.add(str(tag[1]))
        for candidate in re.findall(r"https?://nostrmag\.com/\S+", event.get("content", "")):
            article_urls.add(candidate.rstrip(").,]"))
        for url in sorted(article_urls):
            try:
                if fixture_dir:
                    fixture = Path(fixture_dir) / "nostrmag-article.html"
                    body = fixture.read_text(encoding="utf-8")
                else:
                    body = fetch_url(url)
                text = html_to_text(body)
            except RuntimeError as error:
                failures.append(f"NostrMag article fetch failed for {url}: {error}")
                continue
            articles.append({
                "id": event["id"],
                "pubkey": event.get("pubkey", ""),
                "content": text,
                "tags": event.get("tags", []),
                "_source": "NostrMag weekly issues",
                "_article_url": url,
            })
    return articles


def fetch_inputs(config: dict, days: int):
    failures: list[str] = []
    fixture_dir = os.environ.get("DISCOVERY_FIXTURE_DIR")

    # GitHub organization inventory.
    try:
        org_repos = github_org_repositories(config["github_organization"])
        org_repos = sorted(org_repos, key=lambda repo: repo.get("full_name", "").lower())
    except RuntimeError as error:
        failures.append(f"GitHub organization fetch failed: {error}")
        org_repos = []

    # Nostr sources via pinned nak.
    since = int((NOW - dt.timedelta(days=days)).timestamp())
    nostr_events: list[dict] = []
    if fixture_dir and (Path(fixture_dir) / "nostr-events.jsonl").exists():
        sources_by_pubkey = {s["pubkey"]: s for s in config.get("nostr_sources", [])}
        for line in (Path(fixture_dir) / "nostr-events.jsonl").read_text(encoding="utf-8").splitlines():
            if line.strip():
                event = json.loads(line)
                source = sources_by_pubkey.get(event.get("pubkey"))
                if source:
                    event["_source"] = source["name"]
                nostr_events.append(event)
    else:
        relays = config["relays"]
        for source in config.get("nostr_sources", []):
            cmd = ["req"]
            for kind in source["kinds"]:
                cmd.extend(["-k", str(kind)])
            cmd.extend(["-a", source["pubkey"], "--since", str(since)])
            for relay in relays:
                try:
                    events = run_nak([*cmd, relay])
                    for event in events:
                        if event.get("pubkey") != source["pubkey"] or event.get("kind") not in source["kinds"]:
                            continue
                        event["_relay"] = relay
                        event["_source"] = source["name"]
                        nostr_events.append(event)
                except RuntimeError as error:
                    failures.append(f"nak fetch failed for {source['name']} via {relay}: {error}")
            anchor = source.get("anchor_event")
            if anchor:
                try:
                    anchored = run_nak(["req", "-i", anchor, relays[0]])
                    for event in anchored:
                        if (event.get("id") != anchor or event.get("pubkey") != source["pubkey"]
                                or event.get("kind") not in source["kinds"]):
                            continue
                        event["_relay"] = relays[0]
                        event["_source"] = source["name"]
                        nostr_events.append(event)
                except RuntimeError as error:
                    failures.append(f"anchor fetch failed for {source['name']}: {error}")

    # Fetch article bodies linked by anchor/share events so their repository
    # references become candidates (signed-event provenance is preserved).
    nostr_events.extend(fetch_anchor_articles(nostr_events, failures))

    # Zapstore app metadata.
    zapstore_events: list[dict] = []
    zap_fixture = Path(fixture_dir) / "zapstore-events.jsonl" if fixture_dir else None
    if zap_fixture and zap_fixture.exists():
        for line in zap_fixture.read_text(encoding="utf-8").splitlines():
            if line.strip():
                zapstore_events.append(json.loads(line))
    else:
        zapstore = config.get("zapstore", {})
        if zapstore:
            try:
                zapstore_events = run_nak([
                    "req", "-k", str(zapstore["app_kind"]), "-l", "200", zapstore["relay"],
                ])
                for event in zapstore_events:
                    event["_relay"] = zapstore["relay"]
                    event["_source"] = "Zapstore signed app metadata"
            except RuntimeError as error:
                failures.append(f"Zapstore fetch failed: {error}")

    return org_repos, nostr_events, zapstore_events, failures


def catalog_repos() -> set[str]:
    text = CATALOG.read_text(encoding="utf-8")
    return {normalized for url in REPO_URL.findall(text) if (normalized := normalize_repo(url))}


def verify_repo(url: str) -> dict | str:
    """Return verified repo metadata, or a rejection reason string."""
    match = GITHUB_REPO.search(url)
    if not match:
        return "not a GitHub repository URL"
    owner, name = match.groups()
    try:
        repo = api_json(f"{GITHUB_API}/repos/{owner}/{name.removesuffix('.git')}")
    except RuntimeError as error:
        return f"GitHub lookup failed: {error}"
    if repo.get("archived"):
        return "archived repository"
    if repo.get("private"):
        return "private repository"
    pushed_at = repo.get("pushed_at", "")
    try:
        pushed = dt.datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
    except ValueError:
        pushed = None
    if pushed is None or pushed < CUTOFF:
        return f"no activity in last 365 days (pushed_at={pushed_at or 'unknown'})"

    # Require an explicit Marmot mention in description or README.
    evidence = repo.get("description") or ""
    readme_status = http_head_status(
        f"https://raw.githubusercontent.com/{repo['full_name']}/{repo['default_branch']}/README.md"
    )
    if readme_status == 200:
        readme = fetch_url(
            f"https://raw.githubusercontent.com/{repo['full_name']}/{repo['default_branch']}/README.md"
        )[:200_000]
        evidence += "\n" + readme
    elif readme_status == 404:
        if "marmot" not in evidence.lower():
            return "README.md not found and description lacks explicit Marmot evidence"
    # Any other status: fall back to the description evidence only.

    if "marmot" not in evidence.lower():
        return "no explicit Marmot reference in description or README"
    return {
        "url": normalize_repo(repo["html_url"]),
        "name": repo["full_name"],
        "description": repo.get("description") or "",
        "pushed_at": pushed_at,
        "evidence": evidence[:4000],
    }


def build_report(config, org_repos, nostr_events, zapstore_events, failures=None):
    failures = failures if failures is not None else []
    known = catalog_repos()
    seen = load_json(SEEN, {"event_ids": [], "repository_urls": []})
    seen_events = set(seen.get("event_ids", []))
    seen_repos = set(seen.get("repository_urls", []))

    retained: list[dict] = []
    rejected: list[dict] = []
    candidates: dict[str, dict] = {}

    def consider(url: str, origin: dict):
        normalized = normalize_repo(url)
        if not normalized:
            return
        if normalized in known:
            return
        if normalized in seen_repos:
            rejected.append({"url": normalized, "reason": "previously recorded in seen ledger", "origin": origin})
            return
        if normalized in candidates:
            candidates[normalized]["provenance"].append(origin)
            return
        verdict = verify_repo(normalized)
        if isinstance(verdict, str):
            rejected.append({"url": normalized, "reason": verdict, "origin": origin})
            return
        candidates[normalized] = {**verdict, "provenance": [origin]}

    for repo in org_repos:
        url = repo.get("html_url", "")
        normalized = normalize_repo(url)
        if not normalized or normalized in known or normalized in seen_repos:
            continue
        if normalized in candidates:
            candidates[normalized]["provenance"].append({
                "source": "GitHub organization inventory",
                "detail": repo.get("full_name"),
            })
            continue
        verdict = verify_repo(normalized)
        if isinstance(verdict, str):
            rejected.append({"url": normalized, "reason": verdict,
                             "origin": {"source": "GitHub organization inventory", "detail": repo.get("full_name")}})
            continue
        candidates[normalized] = {**verdict, "provenance": [{
            "source": "GitHub organization inventory",
            "detail": repo.get("full_name"),
        }]}

    events = sorted(
        [*nostr_events, *zapstore_events],
        key=lambda event: (
            event.get("id", ""),
            event.get("_source", ""),
            event.get("_relay", ""),
            event.get("_article_url", ""),
            json.dumps(event, sort_keys=True),
        ),
    )
    for event in events:
        event_id = event.get("id", "")
        if event_id in seen_events:
            continue
        if event.get("_source") != "Zapstore signed app metadata":
            required = next(
                (s for s in config.get("nostr_sources", []) if s["name"] == event.get("_source")), {}
            ).get("required_tags", [])
            tags = {tag[0] for tag in event.get("tags", []) if tag}
            values = {str(tag[1]).lower() for tag in event.get("tags", []) if len(tag) > 1}
            if any(req.lower() not in tags and req.lower() not in values for req in required):
                rejected.append({"event": event_id, "reason": "missing required tag", "source": event.get("_source")})
                continue
        repos = extract_zapstore_repos(event) if event.get("_source") == "Zapstore signed app metadata" else extract_repo_urls(event)
        retained.append({
            "id": event_id,
            "pubkey": event.get("pubkey"),
            "relay": event.get("_relay"),
            "source": event.get("_source"),
            "article_url": event.get("_article_url"),
            "repos": repos,
        })
        for repo_url in repos:
            consider(repo_url, {
                "source": event.get("_source"),
                "event": event_id,
                "relay": event.get("_relay"),
                "article_url": event.get("_article_url"),
            })

    return retained, rejected, candidates


def render_report(retained, rejected, candidates, failures, days):
    lines = [
        "# Weekly Marmot discovery report",
        "",
        f"Window: last {days} days. Generated: {NOW.date().isoformat()} UTC.",
        "",
        "## Summary",
        "",
        f"- Retained source events: {len(retained)}",
        f"- Rejected leads: {len(rejected)}",
        f"- Verified new candidates: {len(candidates)}",
        f"- Source failures: {len(failures)}",
        "",
    ]
    if failures:
        lines += ["## Source failures", ""]
        for failure in sorted(failures):
            lines.append(f"- {failure}")
        lines.append("")
    if candidates:
        lines += ["## Verified candidates", ""]
        for url in sorted(candidates):
            candidate = candidates[url]
            lines.append(f"### {candidate['name']}")
            lines.append("")
            lines.append(f"- URL: {url}")
            lines.append(f"- Last push: {candidate['pushed_at']}")
            lines.append(f"- Description: {candidate['description']}")
            lines.append("- Provenance:")
            for origin in sorted(candidate["provenance"], key=lambda o: json.dumps(o, sort_keys=True)):
                detail = origin.get("event") or origin.get("detail") or ""
                relay = origin.get("relay") or ""
                article = f" article={origin['article_url']}" if origin.get("article_url") else ""
                lines.append(f"  - {origin['source']} {detail} {relay}{article}".rstrip())
            lines.append("")
    else:
        lines += ["No catalog or branch change is required.", ""]
    if rejected:
        lines += ["## Rejected leads", ""]
        for item in sorted(rejected, key=lambda r: json.dumps(r, sort_keys=True)):
            label = item.get("url") or item.get("event")
            origin = item.get("origin") or {}
            source = origin.get("source") or item.get("source") or "unknown"
            lines.append(f"- {label}: {item['reason']} ({source})")
        lines.append("")
    if retained:
        lines += ["## Retained source events (audit trail)", ""]
        for event in sorted(retained, key=lambda e: json.dumps(e, sort_keys=True)):
            article = f" article={event['article_url']}" if event.get("article_url") else ""
            lines.append(f"- {event['id']} source={event['source']} relay={event['relay']}{article}")
        lines.append("")
    digest = hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()
    lines.append(f"Report digest: {digest}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days", type=int, default=10, help="rolling Nostr fetch window")
    parser.add_argument("--output", default="discovery-report.md")
    parser.add_argument("--write-seen", action="store_true", help="update data/discovery-seen.json")
    args = parser.parse_args()

    config = load_json(CONFIG, {})
    org_repos, nostr_events, zapstore_events, failures = fetch_inputs(config, args.days)
    if any(item.startswith("GitHub organization fetch failed:") for item in failures):
        print(json.dumps({"error": "primary GitHub source failed", "failures": failures}))
        return 2

    retained, rejected, candidates = build_report(
        config, org_repos, nostr_events, zapstore_events, failures
    )
    report = render_report(retained, rejected, candidates, failures, args.days)
    Path(args.output).write_text(report, encoding="utf-8")

    if args.write_seen:
        seen = load_json(SEEN, {"event_ids": [], "repository_urls": []})
        seen["event_ids"] = sorted({*seen.get("event_ids", []), *[event["id"] for event in retained]})
        seen["repository_urls"] = sorted({*seen.get("repository_urls", []), *candidates.keys()})
        SEEN.write_text(json.dumps(seen, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"candidates": len(candidates), "retained": len(retained), "rejected": len(rejected)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
