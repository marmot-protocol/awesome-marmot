# Awesome Marmot 🦫

Find apps for private group chats, connect an agent, or build your own messenger with [Marmot](https://github.com/marmot-protocol/marmot): encrypted group messaging over Nostr.

## Start here

| What would you like to do? | Try this |
| --- | --- |
| Chat on your phone | White Noise for [Android](https://github.com/marmot-protocol/whitenoise-android) or [iOS](https://github.com/marmot-protocol/whitenoise-ios) |
| Chat on your computer | White Noise for [macOS](https://github.com/marmot-protocol/whitenoise-mac) or [Linux](https://github.com/marmot-protocol/whitenoise-linux) |
| Use a terminal or automate messages | [MDK CLI and TUI](https://github.com/marmot-protocol/mdk/tree/master/crates/cli): `wn` for commands and terminal chat, `wnd` for a background service |
| Connect an AI agent | [First-party connectors](#agents-and-automation) for Hermes, OpenClaw, Codex, Claude Code, OpenCode, and Pi |
| Build an app | [SDKs and libraries](#sdks-and-libraries) |
| Look up an older project | [No recent public commits](#no-recent-public-commits) or [archived projects](#archived-and-superseded) |

Follow each project's installation instructions; this list is not an app store or a security endorsement.

**Checked 2026-10-01.** Recently updated means a default-branch commit within **90 days** of that check—not a promise of maintenance. Version labels describe public source, not every shipped release. **Marmot v1 and v2 are not interchangeable**; check compatibility before joining the same group from different apps. [Label details](#what-the-labels-mean) and [verification evidence](docs/catalog-verification.md) are below.

## Marmot v2 — recently updated

### Apps

- [White Noise for Android](https://github.com/marmot-protocol/whitenoise-android) — **v2, active** — Native Android messaging app.
- [White Noise for iOS](https://github.com/marmot-protocol/whitenoise-ios) — **v2, active** — Native iPhone messaging app.
- [White Noise for macOS](https://github.com/marmot-protocol/whitenoise-mac) — **v2, active** — Native Mac messaging app.
- [White Noise for Linux](https://github.com/marmot-protocol/whitenoise-linux) — **v2, active** — Desktop app built with Odin and Clay, using MDK through its native interface.
- [MDK CLI and TUI](https://github.com/marmot-protocol/mdk/tree/master/crates/cli) — **v2, active** — Terminal chat and scriptable commands through `wn`, plus the `wnd` background daemon. Replaces the old standalone terminal client.
- [Scramble](https://github.com/DavidGershony/Scramble) — **v2, active** — Desktop and Android messenger whose current source implements the v2 application-component profile.
- [Amethyst](https://github.com/vitorpamplona/amethyst) — **v2, active** — Nostr client with a Marmot implementation in its bundled Quartz library; source now includes v2 identity-proof and media components.
- [amy](https://github.com/vitorpamplona/amethyst/tree/main/cli) — **v2, active** — Amethyst's terminal client, sharing its bundled Quartz implementation.

### Agents and automation

These connectors live in MDK and use its shared runtime for accounts, encrypted groups, and message delivery. Their activity label is for the repository as a whole, not a separate audit of each integration.

- [Marmot for Hermes](https://github.com/marmot-protocol/mdk/tree/master/integrations/hermes/marmot) — **v2, active** — Hermes messaging gateway integration.
- [Marmot for OpenClaw](https://github.com/marmot-protocol/mdk/tree/master/integrations/openclaw/marmot) — **v2, active** — OpenClaw channel integration.
- [wn-codex](https://github.com/marmot-protocol/mdk/tree/master/integrations/codex/marmot) — **v2, active** — Codex terminal connector.
- [wn-claude](https://github.com/marmot-protocol/mdk/tree/master/integrations/claude/marmot) — **v2, active** — Claude Code terminal connector.
- [wn-opencode](https://github.com/marmot-protocol/mdk/tree/master/integrations/opencode/marmot) — **v2, active** — OpenCode terminal connector.
- [wn-pi](https://github.com/marmot-protocol/mdk/tree/master/integrations/pi/marmot) — **v2, active** — Pi terminal connector.

### SDKs and libraries

- [MDK](https://github.com/marmot-protocol/mdk) — **v2, active** — Rust Marmot Development Kit: messaging runtime, storage, language bindings, and integrations.
- [marmot-ts](https://github.com/marmot-protocol/marmot-ts) — **v2, active, alpha** — TypeScript implementation. Its maintainer warns against production use.
- [Quartz in Amethyst](https://github.com/vitorpamplona/amethyst/tree/main/quartz) — **v2, active** — Kotlin Multiplatform library maintained inside Amethyst. This is different from the inactive standalone Quartz repository below.

### Specification and services

- [Marmot specification](https://github.com/marmot-protocol/marmot) — **v2, active** — Adopted protocol specification and migration guidance.
- [Transponder](https://github.com/marmot-protocol/transponder) — **v2, active** — Notification service targeting the adopted Marmot push protocol.

## Marmot v1 — recently updated

Recent development does not mean a project has migrated to v2.

- [Sonar](https://github.com/hedwig-corp/bitchat-to-sonar) — **v1, active** — Bluetooth/Nostr messenger and wallet. Its current core still pins MDK 0.8-era code and the old White Noise Rust stack.

## Migrating or version not yet verified

These projects have recent public commits, but should not be assumed compatible with the current v2 profile.

- [Haven](https://github.com/mehmetefeumit/Haven-App) — **transitional, active** — Private location sharing. Its source and migration notes show an early v2 MDK dependency with later wire-profile changes still pending.
- [marmots-web-chat](https://github.com/marmot-protocol/marmots-web-chat) — **transitional, active** — Browser chat example pinned to an early v2 TypeScript revision; that pin still documents the earlier identity-proof profile.
- [Whistle](https://github.com/sjmcnamara/whistle) — **unknown, active** — Group location sharing and chat; Marmot use is documented, but the implemented generation was not conclusively verified.
- [Mafrend](https://github.com/DestBro/mafrend-zapstore) — **unknown, active, alpha, closed-source** — Map-first social app. The public repository contains store metadata and releases, not its private implementation. “Active” describes that public metadata only.

## Supporting tools — recently updated

These support the ecosystem rather than implementing Marmot messaging.

- [Facet](https://github.com/marmot-protocol/facet) — **adjacent, active** — Nostr-native comparison boards, including White Noise feature parity.
- [Goggles](https://github.com/marmot-protocol/goggles) — **adjacent, active** — Explorer for forensic audit traces. Its documented v4 audit format is not a Marmot protocol version.

## No recent public commits

These repositories are not archived, but their default branches had no commits within the 90-day window. This is a lower-confidence starting point for new users—not proof that their maintainers have abandoned them. Dates are the last default-branch commits at the audit.

### Apps and prototypes

- [Pika](https://github.com/justinmoon/pika) — **v1, inactive, alpha** — Cross-platform messenger pinned to MDK 0.7-era code; the maintainer warns it is not ready for private or secure production use. Last commit: **2026-04-01**.
- [Marmota](https://github.com/dcadenas/marmota) — **v1, inactive, experimental** — Browser client pinned to a MIP-era TypeScript implementation. Last commit: **2026-03-09**.
- [tubestr-v2](https://github.com/Tubestr/tubestr-v2) — **unknown, inactive, scaffold** — Family-video prototype; a completed Marmot bridge was not verified. “v2” in the repository name is not protocol evidence. Last commit: **2026-05-24**.
- [FMDtr](https://gitlab.com/Kalle/fmdtr-android) — **v1, inactive** — Android device finder with an MDK 0.8 bridge. Last commit: **2026-06-19**.

### Agents, automation, and services

- [AgentNoise](https://github.com/nvk/agentnoise) — **adjacent, inactive** — Agent bridge whose documented setup still uses the superseded White Noise Rust daemon. Last commit: **2026-06-27**.
- [Community OpenClaw plugin](https://github.com/tkhumush/openclaw-marmot) — **unknown, inactive** — Separate community plugin using an external Marmot CLI; its exact protocol generation was not verified. Last commit: **2026-05-16**.
- [Community Hermes plugin](https://github.com/notmandatory/hermes-marmot) — **v1, inactive** — Older integration using the standalone Python MDK binding API; distinct from MDK's current first-party connector. Last commit: **2026-05-27**.
- [Botburrow](https://github.com/marmot-protocol/botburrow) — **v1, inactive** — Bot bridge built around the superseded White Noise Rust daemon. Last commit: **2026-04-14**.
- [Burrow](https://github.com/CentauriAgent/burrow) — **v1, inactive** — Agent-oriented CLI/app with a legacy MDK pin. Last commit: **2026-03-07**.
- [marmot-cli](https://github.com/kai-familiar/marmot-cli) — **v1, inactive** — Separate community CLI with an old MDK dependency. Prefer MDK's current CLI for new v2 work. Last commit: **2026-02-16**.
- [dockerized-marmot-cli](https://github.com/rphilbrdigits/dockerized-marmot-cli) — **v1, inactive** — Container wrapper around the older community CLI. Last commit: **2026-03-02**.
- [marmot-server](https://github.com/nmadd57/marmot-server) — **unknown, inactive** — Dockerized REST service using the TypeScript library; its resolved protocol generation was not verified. Last commit: **2026-04-05**.

### Libraries and old examples

- [marmot-cs](https://github.com/DavidGershony/marmot-cs) — **v1, inactive** — Standalone C# library with MIP-era documentation; do not confuse it with Scramble's newer in-repository implementation. Last commit: **2026-06-04**.
- [Standalone Quartz](https://github.com/vitorpamplona/quartz) — **unknown, inactive** — Older standalone repository, separate from the active library inside Amethyst. Last commit: **2025-09-23**.
- [openmls-sled-storage](https://github.com/marmot-protocol/openmls-sled-storage) — **adjacent, inactive** — Sled storage backend for OpenMLS. Last commit: **2025-05-30**.
- [openmls-redb-storage](https://github.com/marmot-protocol/openmls-redb-storage) — **adjacent, inactive** — Redb storage backend for OpenMLS. Last commit: **2025-01-21**.
- [openmls-lmdb-storage](https://github.com/marmot-protocol/openmls-lmdb-storage) — **adjacent, inactive** — LMDB storage backend for OpenMLS. Last commit: **2025-01-12**.
- [mdk-python-example](https://github.com/marmot-protocol/mdk-python-example) — **v1, inactive** — Example for the obsolete standalone Python binding API, not a current MDK quick start. Last commit: **2025-12-01**.
- [mdk-kotlin-example](https://github.com/marmot-protocol/mdk-kotlin-example) — **v1, inactive** — Example for the obsolete standalone Kotlin binding. Last commit: **2025-12-01**.

## Source unavailable at the last check

- [NostrBotKit](https://codeberg.org/mateos/NostrBotKit) — **unknown, unverified** — Previously listed bot toolkit. Its canonical page and API returned 404 during this audit; that alone does not prove abandonment or a protocol version.

## Archived and superseded

Kept for historical research, not recommended as foundations for new work. Archived repositories remain here even if they received a recent final commit.

- [wn-tui](https://github.com/marmot-protocol/wn-tui) — **v1, archived** — Explicitly deprecated by its maintainer and replaced by the TUI in MDK, although GitHub does not mark the repository read-only.
- [Flutter White Noise](https://github.com/marmot-protocol/whitenoise) — **v1, archived** — Superseded Flutter app.
- [whitenoise-rs](https://github.com/marmot-protocol/whitenoise-rs) — **v1, archived** — Former Rust core and CLI; replaced by MDK and native clients.
- [mdk-kotlin](https://github.com/marmot-protocol/mdk-kotlin) — **v1, archived** — Obsolete standalone Kotlin binding.
- [mdk-python](https://github.com/marmot-protocol/mdk-python) — **v1, archived** — Obsolete standalone Python binding.
- [mdk-ruby](https://github.com/marmot-protocol/mdk-ruby) — **v1, archived** — Obsolete standalone Ruby binding.
- [mdk-swift](https://github.com/marmot-protocol/mdk-swift) — **v1, archived** — Obsolete standalone Swift binding.
- [nostr-openmls](https://github.com/marmot-protocol/nostr-openmls) — **v1, archived** — Pre-MDK OpenMLS/Nostr implementation.
- [mls-ts](https://github.com/marmot-protocol/mls-ts) — **adjacent, archived** — Historical TypeScript MLS exploration.
- [dr.marmot](https://github.com/marmot-protocol/dr.marmot) — **adjacent, archived** — Superseded diagnostics tool.

## What the labels mean

Protocol version and activity are separate facts.

| Version label | Meaning |
| --- | --- |
| **v2** | Public source targets the adopted post-MIP protocol. Not a claim of complete conformance, compatible releases, or security. |
| **v1** | Public source targets the older MIP-era protocol or its implementation stack. |
| **transitional** | Migration or early v2 profile evidence does not establish current-profile compatibility. |
| **unknown** | Public evidence does not establish the implemented generation. |
| **adjacent** | Supporting tool rather than a Marmot wire-protocol implementation. |

| Activity label | Meaning at the dated check |
| --- | --- |
| **active** | A public default-branch commit within 90 days. |
| **inactive** | No public default-branch commit within 90 days; repository remains writable. |
| **archived** | GitHub marks it archived, or its maintainer explicitly deprecates it. |
| **unverified** | The canonical source could not be checked; do not infer inactivity. |

Stars, issues, releases, and pushes to other branches do not reset the activity clock. Shared repositories use repository-level activity; this does not prove each subproject is maintained. App versions, package versions, and audit-format versions are not Marmot versions. Maturity labels such as **alpha**, **experimental**, and **scaffold** are separate from protocol and activity labels.

## Discovery and verification

[Verification notes](docs/catalog-verification.md) explain this audit and link to pinned primary sources. The [machine-readable snapshot](data/catalog-audit.json) records the default branch, commit, date, and classification of every listed repository.

The [weekly discovery workflow](.github/workflows/discover.yml) checks the Marmot organization, Zapstore, Nostr Recap, and NostrMag. Secondary sources are leads, not proof: candidates require a public repository, explicit Marmot evidence, and a default-branch commit within 90 days. The job opens a review PR only for new candidates; it **never edits this catalog automatically**. See the [discovery runbook](docs/discovery.md).

## Contributing

Suggest a project or correction with a pull request. Include its canonical repository, a short plain-language description, primary-source evidence for its protocol label, and its latest default-branch commit. For a closed-source app, identify the public metadata/private source boundary.

Update [the audit snapshot](data/catalog-audit.json) with the evidence and check date; keep older projects visible in the appropriate section rather than silently dropping them. Treat a failed lookup as **unverified**, not as proof of inactivity.

Run the checks before submitting:

```sh
python3 scripts/check_catalog.py
python3 -m unittest discover -s tests -v
```

![Catalog checks](https://img.shields.io/github/actions/workflow/status/marmot-protocol/awesome-marmot/ci.yml?label=catalog%20checks)
