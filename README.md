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

- [White Noise for Android](https://github.com/marmot-protocol/whitenoise-android) — **v2, active** — Native Android chat with voice dictation, read-aloud playback, and Amber signer support.
- [White Noise for iOS](https://github.com/marmot-protocol/whitenoise-ios) — **v2, active** — Native iPhone chat with multiple identities, QR profile sharing, and notifications rendered privately on-device.
- [White Noise for macOS](https://github.com/marmot-protocol/whitenoise-mac) — **v2, active** — Early native SwiftUI client with a single-window workspace; Apple Silicon and macOS 15.6+ only.
- [White Noise for Linux](https://github.com/marmot-protocol/whitenoise-linux) — **v2, active** — Desktop chat for Linux, Windows, macOS, and OpenBSD, with chat export, PDF/3D attachment previews, and a password-encrypted vault.
- [MDK CLI and TUI](https://github.com/marmot-protocol/mdk/tree/master/crates/cli) — **v2, active** — Keyboard-driven terminal chat with `wn`; JSON commands and the `wnd` background daemon also suit scripts and agents.
- [Scramble](https://github.com/DavidGershony/Scramble) — **v2, active** — Desktop and Android chat with voice messages, encrypted file sharing, Amber login, and switchable themes.
- [Amethyst](https://github.com/vitorpamplona/amethyst) — **v2, active** — Android and desktop Nostr client combining social feeds, Lightning tips, and Marmot groups in one app.
- [amy](https://github.com/vitorpamplona/amethyst/tree/main/cli) — **v2, active** — Amethyst from the terminal: post public notes, send private DMs, and manage Marmot groups with scriptable JSON output.
- [Haven](https://github.com/mehmetefeumit/Haven-App) — **v2, active, beta** — Android/iOS location sharing in private circles, with your choice of relays and no phone-number signup.
- [marmots-web-chat](https://github.com/marmot-protocol/marmots-web-chat) — **v2, active** — React browser-chat example for developers; local-key login and an early v2 profile, not a polished consumer app.

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

- [Sonar](https://github.com/hedwig-corp/bitchat-to-sonar) — **v1, active** — Phone messaging over offline Bluetooth mesh or online Nostr, plus a Lightning wallet and nearby payments; desktop features differ.
- [Whistle](https://github.com/sjmcnamara/whistle) — **v1, active** — iOS/Android group maps and chat with pausable live location, tap-to-join invites, and low-battery alerts for your circle.

## Closed-source apps

- [Mafrend](https://github.com/DestBro/mafrend-zapstore) — **unknown, active, alpha, closed-source** — Map-first chat with shared places, rich place cards, and time-limited location messages rather than continuous tracking. [Founder contact](https://t.me/destme7).

## Supporting tools — recently updated

- [Facet](https://github.com/marmot-protocol/facet) — **adjacent, active** — Nostr-native feature comparison boards.
- [Goggles](https://github.com/marmot-protocol/goggles) — **adjacent, active** — Forensic audit trace explorer.

## No recent public commits

<details>
<summary>19 projects · last commit dates</summary>

### Apps and prototypes

- [Pika](https://github.com/justinmoon/pika) — **v1, inactive, alpha** — Cross-platform prototype with voice calls and mobile polls; not for sensitive or production use · **2026-04-01**
- [Marmota](https://github.com/dcadenas/marmota) — **v1, inactive, experimental** — Browser group chat with locally stored history, using the older TypeScript stack · **2026-03-09**
- [tubestr-v2](https://github.com/Tubestr/tubestr-v2) — **v1, inactive, scaffold** — Family-video prototype with parent-managed child profiles; encrypted sharing and sync are unfinished · **2026-05-24**
- [FMDtr](https://gitlab.com/Kalle/fmdtr-android) — **v1, inactive** — Find, ring, or remotely wipe an Android device via Marmot, SMS, or a web interface · **2026-06-19**

### Agents, automation, and services

- [AgentNoise](https://github.com/nvk/agentnoise) — **adjacent, inactive** — Agent bridge using the old White Noise Rust daemon · **2026-06-27**
- [Community OpenClaw plugin](https://github.com/tkhumush/openclaw-marmot) — **v1, inactive** — Community plugin for the older Marmot CLI · **2026-05-16**
- [Community Hermes plugin](https://github.com/notmandatory/hermes-marmot) — **v1, inactive** — Older plugin using standalone Python bindings · **2026-05-27**
- [Botburrow](https://github.com/marmot-protocol/botburrow) — **v1, inactive** — Bot bridge using the old White Noise Rust daemon · **2026-04-14**
- [Burrow](https://github.com/CentauriAgent/burrow) — **v1, inactive** — Agent CLI/app with a legacy MDK pin · **2026-03-07**
- [marmot-cli](https://github.com/kai-familiar/marmot-cli) — **v1, inactive** — Community CLI with an older MDK dependency · **2026-02-16**
- [dockerized-marmot-cli](https://github.com/rphilbrdigits/dockerized-marmot-cli) — **v1, inactive** — Container wrapper for the older community CLI · **2026-03-02**
- [marmot-server](https://github.com/nmadd57/marmot-server) — **v1, inactive** — REST service using MIP-era marmot-ts 0.4.0 · **2026-04-05**

### Libraries and old examples

- [marmot-cs](https://github.com/DavidGershony/marmot-cs) — **v1, inactive** — Standalone MIP-era C# library · **2026-06-04**
- [Standalone Quartz](https://github.com/vitorpamplona/quartz) — **adjacent, inactive** — Empty repository; current Quartz lives in Amethyst · **2025-09-23**
- [openmls-sled-storage](https://github.com/marmot-protocol/openmls-sled-storage) — **adjacent, inactive** — Sled storage for OpenMLS · **2025-05-30**
- [openmls-redb-storage](https://github.com/marmot-protocol/openmls-redb-storage) — **adjacent, inactive** — Redb storage for OpenMLS · **2025-01-21**
- [openmls-lmdb-storage](https://github.com/marmot-protocol/openmls-lmdb-storage) — **adjacent, inactive** — LMDB storage for OpenMLS · **2025-01-12**
- [mdk-python-example](https://github.com/marmot-protocol/mdk-python-example) — **v1, inactive** — Example for the obsolete Python bindings · **2025-12-01**
- [mdk-kotlin-example](https://github.com/marmot-protocol/mdk-kotlin-example) — **v1, inactive** — Example for the obsolete Kotlin bindings · **2025-12-01**


</details>

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
| **unknown** | Protocol version unconfirmed |
| **adjacent** | Supporting tool, not a messaging implementation |
| **active** | Default-branch commit within 90 days |
| **inactive** | No commit within 90 days; no known archive marker |
| **archived** | Archived or explicitly deprecated |

## Notes

**Checked 2026-10-01.** Activity is measured at that date, not a maintenance guarantee. Shared repositories use repository-level activity; Mafrend's public activity is store metadata only.

Versions describe source, not every shipped release or tested compatibility. **Marmot v1 and v2 are not interchangeable.** Package names, app versions, and audit formats are not protocol versions. Alpha and experimental labels describe maturity.

Follow each project's installation instructions. Features describe checked source or, for closed-source Mafrend, its publisher's description—not new hands-on tests. This catalog is not a security endorsement.

[Verification evidence](docs/catalog-verification.md) · [Audit snapshot](data/catalog-audit.json) · [Weekly discovery](docs/discovery.md)

![Catalog checks](https://img.shields.io/github/actions/workflow/status/marmot-protocol/awesome-marmot/ci.yml?label=catalog%20checks)
