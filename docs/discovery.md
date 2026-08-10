# Weekly discovery runbook

The weekly job is a conservative intake queue, not an auto-publisher.

## Sources and trust boundaries

1. GitHub organization inventory is a primary source for Marmot-owned repositories.
2. Zapstore kind `32267` events are signed app metadata. They can establish who published a listing, but not that its claims are correct.
3. Nostr Recap and NostrMag are secondary discovery sources. Every retained item includes its event ID, author, relay, and outbound URLs. NostrMag's canonical seed is event `de399234b408ce0bf401c49004fb57342186c843917f94478dfaf54e7eeee19b`, authored by `fe5915…403b`; it is fetched from `wss://nostr.mom`, its linked article body is fetched from the `r` tag URL, and repository leads are extracted from that body.
4. The Compass project registry and archives are useful cross-checks during human review. They are not available inside public CI and never replace a project's own repository evidence.

Automated repository verification currently supports GitHub only. GitLab, Codeberg, NIP-34, and other forges remain eligible for the catalog, but require manual discovery and verification in review.

## Candidate gate

A repository is proposed only when all of these hold:

- its normalized canonical URL is absent from `README.md` and `data/discovery-seen.json`;
- GitHub says it is public and not archived;
- its description or README explicitly mentions Marmot (generic MLS/Nostr support is insufficient);
- its default branch has activity within the configured 365-day window.

Redirects and renamed repositories are normalized through GitHub's API before deduplication. A roundup mention without a repository URL stays in the audit report but cannot become a candidate.

## Idempotence and failures

`scripts/discover.py` sorts and normalizes all inputs. Re-running it with the same source events produces byte-identical output. The workflow exits without a branch, commit, or PR when the verified candidate list is empty. A source outage is recorded; loss of every primary source is a hard failure. Invalid Nostr signatures are rejected by `nak verify`.

When candidates exist, the action updates the seen ledger and writes `discovery-report.md` on a deterministic weekly branch, then opens (or updates) one PR for human review. It never changes `README.md`. A maintainer verifies the evidence, edits the catalog, and merges through normal branch protection.

## Local run

Requirements: Python 3.11+, `nak` 0.20.2, and a GitHub token for higher API limits.

```sh
python3 scripts/discover.py --days 10 --output discovery-report.md
```

Set `DISCOVERY_FIXTURE_DIR` to a directory containing `github-org.json`, `nostr-events.jsonl`, and `zapstore-events.jsonl` to run without the network.
