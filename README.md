# Awesome Marmot 🦫

Apps, agents, and tools for private group messaging with [Marmot](https://github.com/marmot-protocol/marmot).

## Start here

| I want to… | Start with |
| --- | --- |
| Chat on my phone | White Noise for [Android](https://github.com/marmot-protocol/whitenoise-android) or [iOS](https://github.com/marmot-protocol/whitenoise-ios) |
| Chat on my computer | [Cross-platform desktop](https://github.com/marmot-protocol/whitenoise-linux) — Linux, Windows, macOS, OpenBSD — or [native macOS](https://github.com/marmot-protocol/whitenoise-mac) |
| Use a terminal | [MDK CLI/TUI](https://github.com/marmot-protocol/mdk/tree/master/crates/cli) |
| Connect an agent | [Hermes, OpenClaw, Codex, Claude Code, OpenCode, Pi](#agents-and-automation) |
| Build an app | [SDKs and libraries](#sdks-and-libraries) |

[Older projects](#no-recent-public-commits) · [Archived projects](#archived-and-superseded)

## Marmot v2 — recently updated

### Apps

- [White Noise for Android](https://github.com/marmot-protocol/whitenoise-android) — **v2, active** — Native Android messenger.
- [White Noise for iOS](https://github.com/marmot-protocol/whitenoise-ios) — **v2, active** — Native iPhone messenger.
- [White Noise for macOS](https://github.com/marmot-protocol/whitenoise-mac) — **v2, active** — Native Mac messenger.
- [White Noise for Linux](https://github.com/marmot-protocol/whitenoise-linux) — **v2, active** — Desktop messenger for Linux, Windows, macOS, and OpenBSD.
- [MDK CLI and TUI](https://github.com/marmot-protocol/mdk/tree/master/crates/cli) — **v2, active** — Terminal chat and automation with `wn` and the `wnd` daemon.
- [Scramble](https://github.com/DavidGershony/Scramble) — **v2, active** — Desktop and Android messenger with a v2 implementation.
- [Amethyst](https://github.com/vitorpamplona/amethyst) — **v2, active** — Nostr client with built-in Marmot messaging.
- [amy](https://github.com/vitorpamplona/amethyst/tree/main/cli) — **v2, active** — Amethyst's terminal client.

### Agents and automation

- [Marmot for Hermes](https://github.com/marmot-protocol/mdk/tree/master/integrations/hermes/marmot) — **v2, active** — Hermes messaging gateway.
- [Marmot for OpenClaw](https://github.com/marmot-protocol/mdk/tree/master/integrations/openclaw/marmot) — **v2, active** — OpenClaw channel integration.
- [wn-codex](https://github.com/marmot-protocol/mdk/tree/master/integrations/codex/marmot) — **v2, active** — Codex terminal connector.
- [wn-claude](https://github.com/marmot-protocol/mdk/tree/master/integrations/claude/marmot) — **v2, active** — Claude Code terminal connector.
- [wn-opencode](https://github.com/marmot-protocol/mdk/tree/master/integrations/opencode/marmot) — **v2, active** — OpenCode terminal connector.
- [wn-pi](https://github.com/marmot-protocol/mdk/tree/master/integrations/pi/marmot) — **v2, active** — Pi terminal connector.

### SDKs and libraries

- [MDK](https://github.com/marmot-protocol/mdk) — **v2, active** — Rust runtime, storage, language bindings, and integrations.
- [marmot-ts](https://github.com/marmot-protocol/marmot-ts) — **v2, active, alpha** — TypeScript SDK; not recommended for production.
- [Quartz in Amethyst](https://github.com/vitorpamplona/amethyst/tree/main/quartz) — **v2, active** — Kotlin Multiplatform library inside Amethyst.

### Specification and services

- [Marmot specification](https://github.com/marmot-protocol/marmot) — **v2, active** — Protocol specification and migration guide.
- [Transponder](https://github.com/marmot-protocol/transponder) — **v2, active** — Push notification service.

## Marmot v1 — recently updated

- [Sonar](https://github.com/hedwig-corp/bitchat-to-sonar) — **v1, active** — Bluetooth/Nostr messenger and wallet using the older MDK stack.

## Migrating or version not yet verified

- [Haven](https://github.com/mehmetefeumit/Haven-App) — **transitional, active** — Private location sharing; migrating between v2 profiles.
- [marmots-web-chat](https://github.com/marmot-protocol/marmots-web-chat) — **transitional, active** — Browser chat example pinned to an early v2 profile.
- [Whistle](https://github.com/sjmcnamara/whistle) — **unknown, active** — Group location sharing and chat; version unconfirmed.
- [Mafrend](https://github.com/DestBro/mafrend-zapstore) — **unknown, active, alpha, closed-source** — Map-first social app; public store metadata, private source.

## Supporting tools — recently updated

- [Facet](https://github.com/marmot-protocol/facet) — **adjacent, active** — Nostr-native feature comparison boards.
- [Goggles](https://github.com/marmot-protocol/goggles) — **adjacent, active** — Forensic audit trace explorer.

## No recent public commits

<details>
<summary>19 projects · last commit dates</summary>

### Apps and prototypes

- [Pika](https://github.com/justinmoon/pika) — **v1, inactive, alpha** — MDK 0.7-era messenger; not ready for secure production use · **2026-04-01**
- [Marmota](https://github.com/dcadenas/marmota) — **v1, inactive, experimental** — Browser messenger using the older TypeScript stack · **2026-03-09**
- [tubestr-v2](https://github.com/Tubestr/tubestr-v2) — **unknown, inactive, scaffold** — Family-video prototype with an incomplete Marmot bridge · **2026-05-24**
- [FMDtr](https://gitlab.com/Kalle/fmdtr-android) — **v1, inactive** — Android device finder with an MDK 0.8 bridge · **2026-06-19**

### Agents, automation, and services

- [AgentNoise](https://github.com/nvk/agentnoise) — **adjacent, inactive** — Agent bridge using the old White Noise Rust daemon · **2026-06-27**
- [Community OpenClaw plugin](https://github.com/tkhumush/openclaw-marmot) — **unknown, inactive** — Community plugin using an external CLI · **2026-05-16**
- [Community Hermes plugin](https://github.com/notmandatory/hermes-marmot) — **v1, inactive** — Older plugin using standalone Python bindings · **2026-05-27**
- [Botburrow](https://github.com/marmot-protocol/botburrow) — **v1, inactive** — Bot bridge using the old White Noise Rust daemon · **2026-04-14**
- [Burrow](https://github.com/CentauriAgent/burrow) — **v1, inactive** — Agent CLI/app with a legacy MDK pin · **2026-03-07**
- [marmot-cli](https://github.com/kai-familiar/marmot-cli) — **v1, inactive** — Community CLI with an older MDK dependency · **2026-02-16**
- [dockerized-marmot-cli](https://github.com/rphilbrdigits/dockerized-marmot-cli) — **v1, inactive** — Container wrapper for the older community CLI · **2026-03-02**
- [marmot-server](https://github.com/nmadd57/marmot-server) — **unknown, inactive** — TypeScript REST service; version unconfirmed · **2026-04-05**

### Libraries and old examples

- [marmot-cs](https://github.com/DavidGershony/marmot-cs) — **v1, inactive** — Standalone MIP-era C# library · **2026-06-04**
- [Standalone Quartz](https://github.com/vitorpamplona/quartz) — **unknown, inactive** — Older repository; current Quartz lives in Amethyst · **2025-09-23**
- [openmls-sled-storage](https://github.com/marmot-protocol/openmls-sled-storage) — **adjacent, inactive** — Sled storage for OpenMLS · **2025-05-30**
- [openmls-redb-storage](https://github.com/marmot-protocol/openmls-redb-storage) — **adjacent, inactive** — Redb storage for OpenMLS · **2025-01-21**
- [openmls-lmdb-storage](https://github.com/marmot-protocol/openmls-lmdb-storage) — **adjacent, inactive** — LMDB storage for OpenMLS · **2025-01-12**
- [mdk-python-example](https://github.com/marmot-protocol/mdk-python-example) — **v1, inactive** — Example for the obsolete Python bindings · **2025-12-01**
- [mdk-kotlin-example](https://github.com/marmot-protocol/mdk-kotlin-example) — **v1, inactive** — Example for the obsolete Kotlin bindings · **2025-12-01**


</details>

## Source unavailable at the last check

- [NostrBotKit](https://codeberg.org/Tuxor/NostrBotKit) — **unknown, unverified** — Bot toolkit; canonical source returned 404.

## Archived and superseded

<details>
<summary>10 historical projects</summary>

- [wn-tui](https://github.com/marmot-protocol/wn-tui) — **v1, archived** — Deprecated; replaced by MDK's TUI.
- [Flutter White Noise](https://github.com/marmot-protocol/whitenoise) — **v1, archived** — Former Flutter app, preserved at [flutter-final](https://github.com/marmot-protocol/whitenoise/tree/flutter-final).
- [whitenoise-rs](https://github.com/marmot-protocol/whitenoise-rs) — **v1, archived** — Former Rust core and CLI; replaced by MDK.
- [mdk-kotlin](https://github.com/marmot-protocol/mdk-kotlin) — **v1, archived** — Obsolete standalone Kotlin bindings.
- [mdk-python](https://github.com/marmot-protocol/mdk-python) — **v1, archived** — Obsolete standalone Python bindings.
- [mdk-ruby](https://github.com/marmot-protocol/mdk-ruby) — **v1, archived** — Obsolete standalone Ruby bindings.
- [mdk-swift](https://github.com/marmot-protocol/mdk-swift) — **v1, archived** — Obsolete standalone Swift bindings.
- [nostr-openmls](https://github.com/marmot-protocol/nostr-openmls) — **v1, archived** — Pre-MDK OpenMLS/Nostr implementation.
- [mls-ts](https://github.com/marmot-protocol/mls-ts) — **adjacent, archived** — Historical TypeScript MLS exploration.
- [dr.marmot](https://github.com/marmot-protocol/dr.marmot) — **adjacent, archived** — Superseded diagnostics tool.

</details>

## Contributing

Suggest a project or correction with its canonical source, version evidence, and latest commit. Update the [audit snapshot](data/catalog-audit.json) and run:

```sh
python3 scripts/check_catalog.py
python3 -m unittest discover -s tests -v
```

## What the labels mean

| Label | Meaning |
| --- | --- |
| **v2** | Adopted post-MIP protocol |
| **v1** | Older MIP-era protocol |
| **transitional** | Migrating or using an early v2 profile |
| **unknown** | Protocol version unconfirmed |
| **adjacent** | Supporting tool, not a messaging implementation |
| **active** | Default-branch commit within 90 days |
| **inactive** | No commit within 90 days; no known archive marker |
| **archived** | Archived or explicitly deprecated |
| **unverified** | Canonical source unavailable |

## Notes

**Checked 2026-10-01.** Activity is measured at that date, not a maintenance guarantee. Shared repositories use repository-level activity; Mafrend's public activity is store metadata only.

Versions describe source, not every shipped release or tested compatibility. **Marmot v1 and v2 are not interchangeable.** Package names, app versions, and audit formats are not protocol versions. Alpha and experimental labels describe maturity.

Follow each project's installation instructions. This catalog is not a security endorsement; unavailable sources are not assumed abandoned.

[Verification evidence](docs/catalog-verification.md) · [Audit snapshot](data/catalog-audit.json) · [Weekly discovery](docs/discovery.md)

![Catalog checks](https://img.shields.io/github/actions/workflow/status/marmot-protocol/awesome-marmot/ci.yml?label=catalog%20checks)
