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
import time
import urllib.error
import urllib.request
from urllib.parse import quote, urlparse

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/discovery-sources.json"
SEEN = ROOT / "data/discovery-seen.json"
CATALOG = ROOT / "README.md"
NOW = dt.datetime.now(dt.UTC)
ACTIVITY_WINDOW_DAYS = 90
GITHUB_API = "https://api.github.com"
USER_AGENT = "awesome-marmot-discovery/1.0 (+https://github.com/marmot-protocol/awesome-marmot)"
CODE_SEARCH_SOURCE = "GitHub code search"
NIP34_SOURCE = "NIP-34 repository announcements"
GITLAB_SOURCE = "GitLab project search"

GITHUB_REPO = re.compile(r"https?://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)")
REPO_URL = re.compile(
    r"https?://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?",
    re.I,
)
LINK = re.compile(r"https?://[^\s<>()\[\]\"'`]+")
BECH32 = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default


def fixture_file(name: str) -> Path | None:
    fixture_dir = os.environ.get("DISCOVERY_FIXTURE_DIR")
    if fixture_dir and (Path(fixture_dir) / name).exists():
        return Path(fixture_dir) / name
    return None


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


def github_code_search(settings: dict, failures: list[str], skipped: list[str],
                       sleep=time.sleep, clock=time.monotonic) -> list[dict]:
    """Find GitHub repositories whose manifests or code reference Marmot directly.

    Registries miss projects that pin MDK or marmot-ts through Git, so each
    configured query yields repository leads for the normal verification gate.
    Requests are spaced to stay under GitHub's code-search limit (about 10 per
    minute); a 403 or 429 stops the source for this run.
    """
    if not settings.get("enabled"):
        return []
    fixture = fixture_file("github-code-search.json")
    responses = json.loads(fixture.read_text(encoding="utf-8")) if fixture else None
    if responses is None and not os.environ.get("GITHUB_TOKEN"):
        skipped.append(f"{CODE_SEARCH_SOURCE}: GITHUB_TOKEN not set (code search requires authentication)")
        return []
    interval = 60 / settings.get("requests_per_minute", 9)
    per_page = 100
    last_request = None
    hits: dict[tuple[str, str], dict] = {}
    for query in settings.get("queries", []):
        for page in range(1, settings.get("max_pages", 1) + 1):
            if responses is not None:
                result = responses.get(query["query"], {}) if page == 1 else {}
            else:
                if last_request is not None:
                    wait = interval - (clock() - last_request)
                    if wait > 0:
                        sleep(wait)
                last_request = clock()
                try:
                    result = api_json(
                        f"{GITHUB_API}/search/code?q={quote(query['query'], safe='')}"
                        f"&per_page={per_page}&page={page}"
                    )
                except RuntimeError as error:
                    if getattr(error.__cause__, "code", None) in {403, 429}:
                        failures.append(
                            f"{CODE_SEARCH_SOURCE} rate limited at {query['name']}: {error}; remaining queries skipped"
                        )
                        return sorted(hits.values(), key=lambda hit: (hit["url"], hit["query"]))
                    failures.append(f"{CODE_SEARCH_SOURCE} failed for {query['name']}: {error}")
                    break
            if result.get("incomplete_results"):
                failures.append(f"{CODE_SEARCH_SOURCE} returned incomplete results for {query['name']}")
            items = result.get("items") or []
            for item in items:
                url = normalize_repo((item.get("repository") or {}).get("html_url", ""))
                if not url:
                    continue
                # One lead per repository and query; the smallest blob URL is a
                # stable evidence pointer whatever order GitHub returns.
                evidence = item.get("html_url", "")
                key = (url, query["name"])
                if key not in hits or evidence < hits[key]["evidence"]:
                    hits[key] = {"url": url, "query": query["name"], "evidence": evidence}
            if len(items) < per_page:
                break
    return sorted(hits.values(), key=lambda hit: (hit["url"], hit["query"]))


def run_nak(args: list[str], timeout: int = 45, keep=None) -> list[dict]:
    """Run pinned nak and return verified Nostr events.

    ``keep`` drops unwanted events before the per-event signature check.
    """
    try:
        proc = subprocess.run(
            ["nak", *args], capture_output=True, text=True, check=False, timeout=timeout
        )
    except subprocess.TimeoutExpired as error:
        raise RuntimeError(f"nak {' '.join(args)} timed out after {timeout} seconds") from error
    if proc.returncode != 0:
        raise RuntimeError(f"nak {' '.join(args)} failed: {proc.stderr.strip()}")
    events = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        event = json.loads(line)
        if keep is not None and not keep(event):
            continue
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


def normalize_forge_url(url: str) -> str | None:
    """Normalize a non-GitHub repository URL for deduplication and the seen ledger.

    Any scheme with a host is kept: many NIP-34 repositories announce only
    ``htree://`` or ``ssh://`` clone URLs. Malformed URLs (signed events do
    not validate them) return None rather than aborting the run.
    """
    try:
        parsed = urlparse(url.strip())
    except ValueError:
        return None
    if not parsed.scheme or not parsed.netloc:
        return None
    path = parsed.path.split("/-/", 1)[0].rstrip("/").removesuffix(".git").rstrip("/")
    return f"{parsed.scheme.lower()}://{parsed.netloc.lower()}{path}"


def bech32_polymod(values: list[int]) -> int:
    generator = [0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3]
    checksum = 1
    for value in values:
        top = checksum >> 25
        checksum = (checksum & 0x1FFFFFF) << 5 ^ value
        for bit in range(5):
            if (top >> bit) & 1:
                checksum ^= generator[bit]
    return checksum


def npub_to_hex(value: str) -> str | None:
    """Decode a NIP-19 ``npub`` to a hex public key, or None if malformed."""
    hrp, _, data = value.lower().rpartition("1")
    if hrp != "npub" or len(data) < 7 or any(char not in BECH32 for char in data):
        return None
    words = [BECH32.index(char) for char in data]
    expanded = [ord(char) >> 5 for char in hrp] + [0] + [ord(char) & 31 for char in hrp]
    if bech32_polymod(expanded + words) != 1:
        return None
    accumulator, bits, key = 0, 0, bytearray()
    for word in words[:-6]:
        accumulator = ((accumulator << 5) | word) & 0x1FFF
        bits += 5
        if bits >= 8:
            bits -= 8
            key.append((accumulator >> bits) & 0xFF)
    return key.hex() if len(key) == 32 else None


def keyword_pattern(terms: list[str]) -> re.Pattern:
    """Case-insensitive whole-word match; a space in a term also matches '-', '_' or nothing."""
    parts = [r"[\s_-]?".join(re.escape(word) for word in term.split()) for term in terms if term.strip()]
    return re.compile(r"\b(?:" + "|".join(parts) + r")\b", re.I) if parts else re.compile(r"(?!)")


def tag_values(event: dict, name: str) -> list[str]:
    return [str(value) for tag in event.get("tags", []) if tag and tag[0] == name for value in tag[1:]]


def announcement_mentions(event: dict, pattern: re.Pattern) -> bool:
    fields = [*tag_values(event, "d"), *tag_values(event, "name"),
              *tag_values(event, "description"), *tag_values(event, "t")]
    return any(pattern.search(value) for value in fields)


def announcement_urls(event: dict) -> tuple[list[str], list[str]]:
    """Split a kind-30617 announcement into GitHub repositories and other clone URLs.

    GitHub URLs may appear in ``clone``, ``web`` or a mirror's ``source`` tag
    and go through normal verification. Other forges are reported from
    ``clone`` only, since ``web`` points at a browsing UI.
    """
    github: set[str] = set()
    others: set[str] = set()
    for name in ("clone", "web", "source"):
        for value in tag_values(event, name):
            repo = normalize_repo(value)
            if repo:
                github.add(repo)
            elif name == "clone" and (url := normalize_forge_url(value)):
                others.add(url)
    return sorted(github), sorted(others)


def select_announcements(events: list[dict], keywords: list[str]) -> list[dict]:
    """Keep the newest version of each announced repository if it mentions a keyword.

    Kind 30617 is addressable, so relays can hold different versions of one
    (author, ``d``) address. The newest wins (ties: lowest id, per NIP-01) and
    records every relay that served it. Keywords are checked on the winner
    only, so a newer version that dropped Marmot hides older ones.
    """
    pattern = keyword_pattern(keywords)
    newest: dict[tuple[str, str], dict] = {}
    relays: dict[str, set[str]] = {}
    for event in events:
        if event.get("kind") != 30617:
            continue
        relays.setdefault(event.get("id", ""), set()).add(event.get("_relay") or "")
        address = (event.get("pubkey", ""), next(iter(tag_values(event, "d")), ""))
        current = newest.get(address)
        if current is None or (-event.get("created_at", 0), event.get("id", "")) < (
            -current.get("created_at", 0), current.get("id", "")
        ):
            newest[address] = event
    selected = [
        {**event, "_source": NIP34_SOURCE, "_relay": ",".join(sorted(filter(None, relays[event.get("id", "")])))}
        for event in newest.values()
        if announcement_mentions(event, pattern)
    ]
    return sorted(selected, key=lambda event: event.get("id", ""))


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


def fetch_repository_announcements(settings: dict, since: int, failures: list[str]) -> list[dict]:
    """Fetch NIP-34 kind-30617 announcements that mention a configured keyword.

    Every announcement is kept until version selection, so a newer version
    without the keywords still supersedes an older one that had them.
    """
    events: list[dict] = []
    for relay in settings.get("relays", []):
        try:
            batch = run_nak(
                ["req", "-k", "30617", "--since", str(since), "--paginate", relay],
                timeout=settings.get("timeout_seconds", 45),
                keep=lambda event: event.get("kind") == 30617,
            )
        except RuntimeError as error:
            failures.append(f"NIP-34 fetch failed via {relay}: {error}")
            continue
        events.extend({**event, "_relay": relay} for event in batch)
    return select_announcements(events, settings.get("keywords", ["marmot"]))


def gitlab_json(url: str, token: str):
    request = urllib.request.Request(url, headers={"PRIVATE-TOKEN": token, "User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"GitLab API {url} -> HTTP {error.code}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"GitLab API {url} -> {error.reason}") from error


def gitlab_project_search(settings: dict, failures: list[str], skipped: list[str]) -> list[dict]:
    """Search public GitLab projects by name, path, description and topic.

    Runs only with ``GITLAB_TOKEN``. A token also sees private and internal
    projects, and this report is published on a public PR, so only public
    projects are requested or kept. Projects must mention a configured
    keyword as a whole word; they are reported as unverified leads, because
    only GitHub repositories are verified automatically.
    """
    if not settings.get("enabled"):
        return []
    fixture = fixture_file("gitlab-projects.json")
    responses = json.loads(fixture.read_text(encoding="utf-8")) if fixture else None
    token = os.environ.get("GITLAB_TOKEN", "").strip()
    if responses is None and not token:
        skipped.append(f"{GITLAB_SOURCE}: GITLAB_TOKEN not set")
        return []
    api = settings.get("api_url", "https://gitlab.com/api/v4").rstrip("/")
    pattern = keyword_pattern(settings.get("keywords", ["marmot"]))
    queries = [*(f"search={term}" for term in settings.get("searches", [])),
               *(f"topic={topic}" for topic in settings.get("topics", []))]
    # Archived and inactive projects cannot become leads, so they do not use
    # up the page cap.
    active_after = (NOW - dt.timedelta(days=ACTIVITY_WINDOW_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    projects: dict[str, dict] = {}
    for query in queries:
        field, _, value = query.partition("=")
        for page in range(1, settings.get("max_pages", 1) + 1):
            if responses is not None:
                batch = responses.get(query, []) if page == 1 else []
            else:
                try:
                    batch = gitlab_json(
                        f"{api}/projects?{field}={quote(value, safe='')}&visibility=public"
                        f"&archived=false&last_activity_after={active_after}"
                        f"&order_by=id&sort=asc&per_page=100&page={page}",
                        token,
                    )
                except RuntimeError as error:
                    failures.append(f"{GITLAB_SOURCE} failed for {query}: {error}")
                    break
            for project in batch:
                if project.get("visibility") != "public":
                    continue
                text = " ".join(str(part) for part in (
                    project.get("name"), project.get("path_with_namespace"),
                    project.get("description"), *(project.get("topics") or []),
                ) if part)
                if not project.get("web_url") or not pattern.search(text):
                    continue
                entry = projects.setdefault(project["web_url"], {**project, "_queries": []})
                entry["_queries"] = sorted({*entry["_queries"], query})
            if len(batch) < 100:
                break
        else:
            failures.append(f"{GITLAB_SOURCE} reached max_pages for {query}; later results were not read")
    return [projects[url] for url in sorted(projects)]


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

    # NIP-34 repository announcements from git relays.
    nip34 = config.get("nip34", {})
    if nip34.get("enabled"):
        nip34_fixture = fixture_file("nip34-events.jsonl")
        if nip34_fixture:
            announcements = [
                json.loads(line)
                for line in nip34_fixture.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            nostr_events.extend(select_announcements(announcements, nip34.get("keywords", ["marmot"])))
        else:
            nostr_events.extend(fetch_repository_announcements(nip34, since, failures))

    return org_repos, nostr_events, zapstore_events, failures


def catalog_repos() -> set[str]:
    text = CATALOG.read_text(encoding="utf-8")
    return {normalized for url in REPO_URL.findall(text) if (normalized := normalize_repo(url))}


def catalog_forge_entries() -> tuple[set[str], set[tuple[str, str]]]:
    """Return the catalog's non-GitHub links and its gitworkshop.dev repositories.

    gitworkshop.dev links name an ``npub`` and a repository identifier, which
    match a NIP-34 announcement's author (or maintainer) and ``d`` tag.
    """
    links: set[str] = set()
    nostr_repos: set[tuple[str, str]] = set()
    for link in LINK.findall(CATALOG.read_text(encoding="utf-8")):
        link = link.rstrip(".,;:")
        if not (normalized := normalize_forge_url(link)):
            continue
        links.add(normalized)
        parsed = urlparse(link)
        segments = [segment for segment in parsed.path.split("/") if segment]
        if parsed.netloc.lower() == "gitworkshop.dev" and len(segments) >= 2:
            pubkey = npub_to_hex(segments[0])
            identifier = segments[2] if len(segments) >= 3 and "." in segments[1] else segments[1]
            if pubkey:
                nostr_repos.add((pubkey, identifier))
    return links, nostr_repos


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
    branch = repo.get("default_branch")
    if not branch:
        return "default branch unavailable"
    try:
        commits = api_json(
            f"{GITHUB_API}/repos/{repo['full_name']}/commits?sha={quote(branch, safe='')}&per_page=1"
        )
        latest = commits[0]
        committed_at = latest["commit"]["committer"]["date"]
        committed = dt.datetime.fromisoformat(committed_at.replace("Z", "+00:00"))
        if committed.tzinfo is None or not re.fullmatch(r"[0-9a-f]{40}", latest["sha"]):
            return "invalid default-branch commit metadata"
    except RuntimeError as error:
        return f"default-branch commit lookup failed: {error}"
    except (KeyError, IndexError, TypeError, ValueError, AttributeError):
        return "default-branch commit unavailable or invalid"
    if committed > NOW:
        return "default-branch commit date is in the future"
    if committed < NOW - dt.timedelta(days=ACTIVITY_WINDOW_DAYS):
        return f"no default-branch commit in last {ACTIVITY_WINDOW_DAYS} days (committed_at={committed_at})"

    # Require an explicit Marmot mention in description or README.
    evidence = repo.get("description") or ""
    readme_status = http_head_status(
        f"https://raw.githubusercontent.com/{repo['full_name']}/{latest['sha']}/README.md"
    )
    if readme_status == 200:
        try:
            readme = fetch_url(
                f"https://raw.githubusercontent.com/{repo['full_name']}/{latest['sha']}/README.md"
            )[:200_000]
        except RuntimeError as error:
            return f"README lookup failed: {error}"
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
        "last_commit_at": committed_at,
        "commit_url": f"{repo['html_url']}/commit/{latest['sha']}",
        "evidence": evidence[:4000],
    }


def build_report(config, org_repos, nostr_events, zapstore_events, failures=None,
                 code_search_hits=(), gitlab_projects=()):
    failures = failures if failures is not None else []
    known = catalog_repos()
    known_links, known_nostr = catalog_forge_entries()
    seen = load_json(SEEN, {"event_ids": [], "repository_urls": []})
    seen_events = set(seen.get("event_ids", []))
    seen_repos = set(seen.get("repository_urls", []))

    retained: list[dict] = []
    rejected: list[dict] = []
    candidates: dict[str, dict] = {}
    leads: dict[str, dict] = {}
    # Rejection reasons by URL, so a repository named by several sources is
    # verified once.
    verdicts: dict[str, str] = {}

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
        verdict = verdicts.get(normalized) or verify_repo(normalized)
        if isinstance(verdict, str):
            verdicts[normalized] = verdict
            rejected.append({"url": normalized, "reason": verdict, "origin": origin})
            return
        candidates[normalized] = {**verdict, "provenance": [origin]}

    def add_lead(urls: list[str], name: str, description: str, web: list[str], origin: dict):
        """Record an unverified non-GitHub lead, or reject it if already seen."""
        if seen_repos.intersection(urls):
            rejected.append({"url": urls[0], "reason": "previously recorded in seen ledger", "origin": origin})
            return
        lead = leads.setdefault(urls[0], {
            "name": name, "description": description, "urls": [], "web": [], "provenance": [],
        })
        lead["urls"] = sorted({*lead["urls"], *urls})
        lead["web"] = sorted({*lead["web"], *web})
        lead["provenance"].append(origin)

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
            verdicts[normalized] = verdict
            rejected.append({"url": normalized, "reason": verdict,
                             "origin": {"source": "GitHub organization inventory", "detail": repo.get("full_name")}})
            continue
        candidates[normalized] = {**verdict, "provenance": [{
            "source": "GitHub organization inventory",
            "detail": repo.get("full_name"),
        }]}

    for hit in sorted(code_search_hits, key=lambda hit: (hit["url"], hit["query"], hit["evidence"])):
        consider(hit["url"], {"source": CODE_SEARCH_SOURCE, "detail": f"{hit['query']}: {hit['evidence']}"})

    announcements: list[tuple[dict, dict]] = []
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
        if event.get("_source") == "Zapstore signed app metadata":
            repos = extract_zapstore_repos(event)
        elif event.get("_source") == NIP34_SOURCE:
            repos, _clones = announcement_urls(event)
        else:
            repos = extract_repo_urls(event)
        retained.append({
            "id": event_id,
            "pubkey": event.get("pubkey"),
            "relay": event.get("_relay"),
            "source": event.get("_source"),
            "article_url": event.get("_article_url"),
            "repos": repos,
        })
        origin = {
            "source": event.get("_source"),
            "event": event_id,
            "relay": event.get("_relay"),
            "article_url": event.get("_article_url"),
        }
        if event.get("_source") == NIP34_SOURCE:
            origin["author"] = event.get("pubkey")
            announcements.append((event, origin))
        for repo_url in repos:
            consider(repo_url, dict(origin))

    # Non-GitHub clone URLs cannot be verified automatically. They become
    # leads unless the same announcement's GitHub URL already covers the
    # project (cataloged, proposed now, or proposed in an earlier week), or
    # the catalog links the repository or its gitworkshop.dev page.
    for event, origin in announcements:
        github, clones = announcement_urls(event)
        if not clones or any(url in known or url in candidates or url in seen_repos for url in github):
            continue
        identifier = next(iter(tag_values(event, "d")), "")
        pubkeys = {event.get("pubkey", ""), *tag_values(event, "maintainers")}
        web = sorted({url for value in tag_values(event, "web") if (url := normalize_forge_url(value))})
        if known_nostr.intersection((pubkey, identifier) for pubkey in pubkeys) or known_links.intersection([*clones, *web]):
            continue
        name = next(iter(tag_values(event, "name")), "") or identifier
        description = next(iter(tag_values(event, "description")), "")
        add_lead(clones, name, description, web, origin)

    window_start = NOW - dt.timedelta(days=ACTIVITY_WINDOW_DAYS)
    for project in sorted(gitlab_projects, key=lambda project: project.get("web_url", "")):
        url = normalize_forge_url(project.get("web_url", ""))
        if not url or url in known_links:
            continue
        origin = {"source": GITLAB_SOURCE, "detail": ", ".join(project.get("_queries", []))}
        if url in seen_repos:
            rejected.append({"url": url, "reason": "previously recorded in seen ledger", "origin": origin})
            continue
        if project.get("archived"):
            rejected.append({"url": url, "reason": "archived project", "origin": origin})
            continue
        # Any push updates last_activity_at, so an old value rules out recent
        # default-branch work. A recent value does not prove it.
        last_activity = project.get("last_activity_at")
        try:
            active = dt.datetime.fromisoformat(str(last_activity).replace("Z", "+00:00"))
        except ValueError:
            active = None
        if active is None or active.tzinfo is None:
            rejected.append({"url": url, "reason": "GitLab activity timestamp unavailable or invalid", "origin": origin})
            continue
        if active < window_start:
            rejected.append({
                "url": url,
                "reason": f"no GitLab project activity in last {ACTIVITY_WINDOW_DAYS} days (last_activity_at={last_activity})",
                "origin": origin,
            })
            continue
        add_lead([url], project.get("path_with_namespace") or url, project.get("description") or "", [], origin)

    return retained, rejected, candidates, leads


def render_origin(origin: dict) -> str:
    detail = origin.get("event") or origin.get("detail") or ""
    author = f" author={origin['author']}" if origin.get("author") else ""
    relay = origin.get("relay") or ""
    article = f" article={origin['article_url']}" if origin.get("article_url") else ""
    return f"  - {origin['source']} {detail}{author} {relay}{article}".rstrip()


def render_report(retained, rejected, candidates, leads, failures, days, skipped=()):
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
        f"- Unverified non-GitHub leads: {len(leads)}",
        f"- Source failures: {len(failures)}",
        "",
    ]
    if failures:
        lines += ["## Source failures", ""]
        for failure in sorted(failures):
            lines.append(f"- {failure}")
        lines.append("")
    if skipped:
        lines += ["## Skipped sources", ""]
        for item in sorted(skipped):
            lines.append(f"- {item}")
        lines.append("")
    if candidates:
        lines += ["## Verified candidates", ""]
        for url in sorted(candidates):
            candidate = candidates[url]
            lines.append(f"### {candidate['name']}")
            lines.append("")
            lines.append(f"- URL: {url}")
            lines.append(f"- Last default-branch commit: [{candidate['last_commit_at']}]({candidate['commit_url']})")
            lines.append(f"- Description: {candidate['description']}")
            lines.append("- Provenance:")
            for origin in sorted(candidate["provenance"], key=lambda o: json.dumps(o, sort_keys=True)):
                lines.append(render_origin(origin))
            lines.append("")
    if leads:
        lines += [
            "## Unverified non-GitHub leads",
            "",
            "Automated verification covers GitHub only. These leads passed a keyword filter, "
            "not the candidate gate: confirm source, default-branch activity and Marmot use by hand.",
            "",
        ]
        for key in sorted(leads):
            lead = leads[key]
            lines.append(f"### {lead['name']}")
            lines.append("")
            lines.append(f"- URLs: {', '.join(lead['urls'])}")
            if lead["web"]:
                lines.append(f"- Web: {', '.join(lead['web'])}")
            lines.append(f"- Description: {lead['description']}")
            lines.append("- Provenance:")
            for origin in sorted(lead["provenance"], key=lambda o: json.dumps(o, sort_keys=True)):
                lines.append(render_origin(origin))
            lines.append("")
    if not candidates and not leads:
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

    # Secondary search sources run only once the primary inventory succeeded.
    skipped: list[str] = []
    code_search_hits = github_code_search(config.get("github_code_search", {}), failures, skipped)
    gitlab_projects = gitlab_project_search(config.get("gitlab", {}), failures, skipped)

    retained, rejected, candidates, leads = build_report(
        config, org_repos, nostr_events, zapstore_events, failures, code_search_hits, gitlab_projects
    )
    report = render_report(retained, rejected, candidates, leads, failures, args.days, skipped)
    Path(args.output).write_text(report, encoding="utf-8")

    if args.write_seen:
        seen = load_json(SEEN, {"event_ids": [], "repository_urls": []})
        seen["event_ids"] = sorted({*seen.get("event_ids", []), *[event["id"] for event in retained]})
        seen["repository_urls"] = sorted({
            *seen.get("repository_urls", []), *candidates.keys(),
            *(url for lead in leads.values() for url in lead["urls"]),
        })
        SEEN.write_text(json.dumps(seen, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "candidates": len(candidates), "leads": len(leads),
        "retained": len(retained), "rejected": len(rejected),
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
