# Weekly discovery runbook

The weekly job is a conservative intake queue, not an auto-publisher.

## Sources and trust boundaries

1. GitHub organization inventory is a primary source for Marmot-owned repositories.
2. Zapstore kind `32267` events are signed app metadata. They can establish who published a listing, but not that its claims are correct.
3. Nostr Recap and NostrMag are secondary discovery sources. Every retained item includes its event ID, author, relay, and outbound URLs. NostrMag's canonical seed is event `de399234b408ce0bf401c49004fb57342186c843917f94478dfaf54e7eeee19b`, authored by `fe5915…403b`; it is fetched from `wss://nostr.mom`, its linked article body is fetched from the `r` tag URL, and repository leads are extracted from that body.
4. The Compass project registry and archives are useful cross-checks during human review. They are not available inside public CI and never replace a project's own repository evidence.
5. GitHub code search is a secondary source for projects that depend on Marmot through Git rather than a registry (crates.io stops at mdk-core 0.8.0). Configured queries look outside the marmot-protocol organization for `marmot-protocol/mdk` manifests naming `cgka-engine`, `marmot-app` or `transport-nostr-peeler`, and for `@internet-privacy/marmot-ts`, `wn-agent` and `marmot.agent-control.v2`. Requests are spaced under the 10-per-minute code-search limit; a 403 or 429 stops the source for that run. Hits pass the candidate gate below, and provenance cites the matching file at its commit. Code search needs `GITHUB_TOKEN` and covers default branches only.
6. NIP-34 kind `30617` repository announcements are read from the git relays in `config/discovery-sources.json` over the rolling window. Each signature is checked with `nak verify`, and only the newest version of each author and `d` address is kept. An announcement is retained when its `d`, name, description or `t` tags mention Marmot, White Noise, MDK or MLS as a whole word. GitHub URLs in its `clone`, `web` or `source` tags pass the candidate gate. Other clone URLs become unverified leads with the signed event ID and author, unless the GitHub URL produced a candidate or the catalog already links the repository (directly, or through a gitworkshop.dev page naming the author or a maintainer). Run once with a longer `--days` window to backfill.
7. GitLab.com project search by name, path, description and topic runs only when `GITLAB_TOKEN` is set; without it, the report lists the source as skipped. Projects must mention Marmot as a whole word. Archived projects, and projects with no GitLab activity at all in the 90-day window, are rejected. The rest are unverified leads: `last_activity_at` cannot show default-branch work.

Each of sources 5–7 has an `enabled` switch in `config/discovery-sources.json`. Unverified leads appear in their own report section and never pass as verified candidates.

Automated repository verification currently supports GitHub only. GitLab, Codeberg, NIP-34, and other forges remain eligible for the catalog, but their leads are unverified and need manual verification in review. [Manual cross-forge sweeps](#manual-cross-forge-sweeps) describes how to run one.

## Candidate gate

A repository is proposed only when all of these hold:

- its normalized canonical URL is absent from `README.md` and `data/discovery-seen.json`;
- GitHub says it is public and not archived;
- its description or README explicitly mentions Marmot (generic MLS/Nostr support is insufficient);
- its latest default-branch commit is within the 90-day activity window, with a valid, timezone-aware committer timestamp that is not in the future.

Verification reads the commit for the API-reported default branch, not repository `pushed_at`. A push to an unrelated branch, tag, or release does not establish recent default-branch work. Reports retain the immutable commit link, and README evidence is fetched at that same commit. Unavailable or malformed commit metadata is a rejected, unverified lead—not proof of abandonment.

Redirects and renamed repositories are normalized through GitHub's API before deduplication. A roundup mention without a repository URL stays in the audit report but cannot become a candidate.

## Idempotence and failures

`scripts/discover.py` sorts and normalizes all inputs. Re-running it with the same source events produces byte-identical output. The workflow exits without a branch, commit, or PR when there are no verified candidates and no unverified leads. A source outage is recorded; loss of every primary source is a hard failure. Invalid Nostr signatures are rejected by `nak verify`.

When candidates or leads exist, the action records their URLs in the seen ledger and writes `discovery-report.md` on a deterministic weekly branch, then opens (or updates) one PR for human review. It never changes `README.md`. A maintainer verifies the evidence, edits the catalog, and merges through normal branch protection.

## Local run

Requirements: Python 3.11+, `nak` 0.20.2, and a GitHub token for higher API limits and code search. Set `GITLAB_TOKEN` to include GitLab project search. The `DISCOVERY_FIXTURE_DIR` described below may also hold `nip34-events.jsonl`, `github-code-search.json` (responses keyed by query) and `gitlab-projects.json` (keyed by `search=` or `topic=` term); see `tests/fixtures`.

```sh
python3 scripts/discover.py --days 10 --output discovery-report.md
```

Set `DISCOVERY_FIXTURE_DIR` to a directory containing `github-org.json`, `nostr-events.jsonl`, and `zapstore-events.jsonl` to fixture the source inventory. Candidate metadata and commit verification still use GitHub unless mocked in the tests; this is not a fully offline end-to-end mode.

## Manual cross-forge sweeps

The weekly job automates this sweep's manifest code search, NIP-34 announcements and GitLab project search (sources 5–7 above). Repository search, dependency graphs, Codeberg and registries stay manual, and code search is incomplete. Most community projects reach the catalog through occasional manual sweeps. The [2026-10-23 sweep](catalog-verification.md#discovery-sweep-additions-and-corrections-2026-10-23) added 11 projects and corrected 2 entries. These sources found them:

| Source | What worked | Limits |
| --- | --- | --- |
| GitHub | Repository search (best match and recently updated) for Marmot, White Noise, MDK and NIP-EE terms. Code search for manifests naming `marmot-protocol/mdk`, `cgka-engine`, `marmot-app`, `@internet-privacy/marmot-ts`, `wn-agent` or `marmot.agent-control.v2`. The "Used by" dependency graph of marmot-ts, mdk-core and ts-mls. | Code search indexes default branches only and is visibly incomplete: several v2 projects missed every manifest query. Broad queries cap at about 300 results. Some dependents are private. |
| GitLab.com | Unauthenticated project search by name and description. Topic search. Listing the projects of known Nostr developers' namespaces; one find surfaced only this way. | Code (`blobs`) search, global project search and web search need a token. Unauthenticated responses omit `archived`. |
| Codeberg | Forgejo repository search with `includeDesc=true`; without it, only names match. | No code search. |
| NIP-34 | Kind 30617 repository announcements paged from git relays (relay.ngit.dev, index.ngit.dev, git.shakespeare.diy, gitnostr.com, relay.gittr.space) and general relays, filtered by name, description and tags. Then shallow clones of announced repositories to read manifests. Check each announcement with `nak verify`, and compare kind 30618 state with `git ls-remote`. | Many announcements have no HTTPS clone URL (htree://, ssh). relay.damus.io and relay.nostr.band did not page reliably. |
| Registries | Reverse dependencies on crates.io; npm, pub.dev, NuGet, Hex and pkg.go.dev search. | crates.io stops at mdk-core 0.8.0, because MDK 0.9+ is published only through Git. Registry dependents are therefore all v1, and v2 users are invisible there. npm misses aliased installs. |

Treat a lead as a candidate only after reading its default-branch head. Check that the code really uses Marmot: README mentions and kind-number labels alone do not qualify. Two projects found in the 2026-10-23 sweep had already dropped Marmot. Classify the generation from pinned engine or component evidence, as described in the [refresh procedure](catalog-verification.md#refresh-procedure).

Record reviewed GitHub leads that are not added in `data/discovery-seen.json`, so the weekly job does not re-propose them. The ledger suppresses proposals, so a recorded v1 project that later upgrades needs a manual recheck. Record GitLab project URLs and NIP-34 clone URLs there too, without a trailing `.git`; the weekly job checks its unverified leads against them. List them in the dated verification note as well.
