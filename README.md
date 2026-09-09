# Awesome Marmot 🦫

A curated catalog of apps, libraries, integrations, and developer tools built on or directly supporting the [Marmot Protocol](https://github.com/marmot-protocol/marmot)—MLS-based, end-to-end encrypted group messaging transported over Nostr.

![Catalog checks](https://img.shields.io/github/actions/workflow/status/marmot-protocol/awesome-marmot/ci.yml?label=catalog%20checks)

## Explore the ecosystem

| I want to… | Start here |
| --- | --- |
| Use a Marmot client | [Apps](#apps) |
| Connect an agent or automation | [Agent and automation integrations](#agent-and-automation-integrations) |
| Build with Marmot | [SDKs and libraries](#sdks-and-libraries) or [Examples](#examples) |
| Operate or inspect Marmot systems | [Infrastructure and developer tools](#infrastructure-and-developer-tools) |
| Research older implementations | [Archived and superseded projects](#archived-and-superseded-projects) |
| Add a project | [Contributing](#contributing) |

## How to read the labels

Protocol generation and repository activity are separate facts.

| Label | Meaning |
| --- | --- |
| **current-spec** | Primary-source evidence targets the adopted, post-MIP specification. This is not a conformance or security claim. |
| **legacy-spec** | The implementation targets the deprecated MIP-era protocol. |
| **transitional** | The project mixes current and legacy protocol surfaces or is actively migrating between them. |
| **unknown** | Public evidence is not enough to identify the implemented protocol generation. |
| **adjacent** | The project directly supports the ecosystem but does not implement Marmot wire behavior. |
| **active** | The canonical repository has had public activity within the last 12 months. |
| **inactive** | The repository remains writable but has not had public activity within the last 12 months. |
| **archived** | The canonical repository is read-only, explicitly obsolete, or superseded. |

Maintainer-supplied maturity labels such as **alpha** and **experimental** are shown separately. Activity is not evidence of protocol currency, interoperability, production readiness, or security. Evidence was last audited against primary sources on 2026-09-09.

## Protocol

- [marmot](https://github.com/marmot-protocol/marmot) — **current-spec, active** — Adopted specification organized by protocol surface, with historical migration mapping.

## Apps

### Messaging clients

- [White Noise for Android](https://github.com/marmot-protocol/whitenoise-android) — **current-spec, active** — Native Android White Noise client.
- [White Noise for iOS](https://github.com/marmot-protocol/whitenoise-ios) — **current-spec, active** — Native iOS White Noise client.
- [White Noise for macOS](https://github.com/marmot-protocol/whitenoise-mac) — **current-spec, active** — Native macOS White Noise client.
- [White Noise for Linux](https://github.com/marmot-protocol/whitenoise-linux) — **current-spec, active** — Rust/Slint desktop client; its repository points contributors to the canonical NIP-34 repository.
- [pika](https://github.com/justinmoon/pika) — **current-spec, active, alpha** — Cross-platform encrypted messenger with a Rust core and MDK.
- [Scramble](https://github.com/DavidGershony/Scramble) — **current-spec, active** — Desktop and Android client implemented with `marmot-cs`.
- [Marmota](https://github.com/dcadenas/marmota) — **legacy-spec, active, experimental** — Browser client pinned to a MIP-era `marmot-ts` revision.
- [amethyst](https://github.com/vitorpamplona/amethyst) — **legacy-spec, active** — Kotlin Multiplatform Nostr client whose Quartz layer implements the earlier monolithic group-data extension.
- [amy](https://github.com/vitorpamplona/amethyst/tree/main/cli) — **legacy-spec, active** — Amethyst CLI using the same Quartz Marmot implementation.

### Location, media, and device apps

- [Haven](https://github.com/mehmetefeumit/Haven-App) — **transitional, active** — Private Android/iOS location sharing with an MDK-based core that still carries legacy compatibility surfaces.
- [Mafrend](https://github.com/DestBro/mafrend-zapstore) — **unknown, active, alpha, closed-source** — Map-first social app whose public repository provides signed store metadata and releases describing Marmot private groups; source-level protocol generation cannot be verified publicly.
- [Whistle](https://github.com/sjmcnamara/whistle) — **unknown, active** — Cross-platform group location sharing and chat with public Marmot integration evidence but no conclusive generation marker.
- [Sonar](https://github.com/hedwig-corp/bitchat-to-sonar) — **current-spec, active** — Bluetooth/Nostr messenger and wallet with MDK-backed group DMs interoperable with White Noise.
- [FMDtr](https://gitlab.com/Kalle/fmdtr-android) — **transitional, active** — Android device finder and remote-control app with an MDK 0.8 bridge and documented Marmot migration work.
- [tubestr-v2](https://github.com/Tubestr/tubestr-v2) — **legacy-spec, active, scaffold** — Family-video prototype with an incomplete MDK bridge pinned to legacy 0.7-era components; it is not evidence of a completed Marmot app.

## Agent and automation integrations

The first-party connectors below live in MDK and delegate accounts, MLS state, Nostr transport, and durable sends to `wn-agent`.

- [Marmot for Hermes](https://github.com/marmot-protocol/mdk/tree/master/integrations/hermes/marmot) — **current-spec, active** — Hermes gateway plugin with rich chat, media, reactions, and preview support.
- [Marmot for OpenClaw](https://github.com/marmot-protocol/mdk/tree/master/integrations/openclaw/marmot) — **current-spec, active** — OpenClaw channel plugin.
- [wn-codex](https://github.com/marmot-protocol/mdk/tree/master/integrations/codex/marmot) — **current-spec, active** — Codex terminal harness connector.
- [wn-opencode](https://github.com/marmot-protocol/mdk/tree/master/integrations/opencode/marmot) — **current-spec, active** — OpenCode terminal harness connector.
- [wn-pi](https://github.com/marmot-protocol/mdk/tree/master/integrations/pi/marmot) — **current-spec, active** — Pi terminal harness connector.
- [agentnoise](https://github.com/nvk/agentnoise) — **adjacent, active** — Desktop bridge that uses White Noise as a control surface for local coding-agent sessions.
- [openclaw-marmot](https://github.com/tkhumush/openclaw-marmot) — **unknown, active** — Community OpenClaw channel plugin using an external Marmot daemon.
- [hermes-marmot](https://github.com/notmandatory/hermes-marmot) — **current-spec, active** — Community Hermes gateway plugin built with `mdk-python`.
- [botburrow](https://github.com/marmot-protocol/botburrow) — **unknown, active** — Bot-management infrastructure for Marmot groups.
- [burrow](https://github.com/CentauriAgent/burrow) — **unknown, active** — Marmot CLI for encrypted communication between people and agents.
- [marmot-cli](https://github.com/kai-familiar/marmot-cli) — **legacy-spec, active** — Rust CLI built on the earlier MDK generation.
- [dockerized-marmot-cli](https://github.com/rphilbrdigits/dockerized-marmot-cli) — **legacy-spec, active** — Container packaging for the legacy `marmot-cli`.
- [NostrBotKit](https://codeberg.org/Tuxor/NostrBotKit) — **unknown, active** — Self-hosted bot framework with a substantive Marmot message router.

## SDKs and libraries

- [mdk](https://github.com/marmot-protocol/mdk) — **current-spec, active** — Rust Marmot Development Kit and production implementation stack.
- [marmot-ts](https://github.com/marmot-protocol/marmot-ts) — **current-spec, active** — TypeScript implementation of the adopted protocol surfaces.
- [marmot-cs](https://github.com/DavidGershony/marmot-cs) — **current-spec, active** — C# Marmot implementation.
- [quartz](https://github.com/vitorpamplona/quartz) — **legacy-spec, active** — Kotlin Multiplatform Nostr library with a MIP-era Marmot implementation.
- [openmls-sled-storage](https://github.com/marmot-protocol/openmls-sled-storage) — **adjacent, inactive** — Sled backend for OpenMLS storage traits.
- [openmls-redb-storage](https://github.com/marmot-protocol/openmls-redb-storage) — **adjacent, inactive** — Redb backend for OpenMLS storage traits.
- [openmls-lmdb-storage](https://github.com/marmot-protocol/openmls-lmdb-storage) — **adjacent, inactive** — LMDB backend for OpenMLS storage traits.

## Infrastructure and developer tools

- [Facet](https://github.com/marmot-protocol/facet) — **adjacent, active** — Nostr-native comparison tracker whose first board covers White Noise feature parity.
- [goggles](https://github.com/marmot-protocol/goggles) — **adjacent, active** — Explorer for Marmot forensic audit traces.
- [marmot-server](https://github.com/nmadd57/marmot-server) — **current-spec, active** — Local Docker service exposing an MDK-backed REST API.
- [transponder](https://github.com/marmot-protocol/transponder) — **current-spec, active** — Notification server for the adopted Marmot push protocol.

## Examples

- [marmots-web-chat](https://github.com/marmot-protocol/marmots-web-chat) — **current-spec, active** — Browser chat example for `marmot-ts`.
- [mdk-python-example](https://github.com/marmot-protocol/mdk-python-example) — **current-spec, active** — Python binding example for the bindings maintained in MDK.
- [mdk-kotlin-example](https://github.com/marmot-protocol/mdk-kotlin-example) — **legacy-spec, active** — Kotlin example pinned to the obsolete standalone binding.

## Archived and superseded projects

These are substantive historical implementations, not current foundations.

- [wn-tui](https://github.com/marmot-protocol/wn-tui) — **legacy-spec, archived** — Deprecated terminal client superseded by the TUI in MDK.
- [whitenoise](https://github.com/marmot-protocol/whitenoise) — **legacy-spec, archived** — Superseded Flutter White Noise app.
- [whitenoise-rs](https://github.com/marmot-protocol/whitenoise-rs) — **legacy-spec, archived** — Former Rust core and CLI superseded by MDK and native clients.
- [mdk-kotlin](https://github.com/marmot-protocol/mdk-kotlin), [mdk-python](https://github.com/marmot-protocol/mdk-python), [mdk-ruby](https://github.com/marmot-protocol/mdk-ruby), and [mdk-swift](https://github.com/marmot-protocol/mdk-swift) — **legacy-spec, archived** — Obsolete standalone binding repositories superseded by bindings in MDK.
- [nostr-openmls](https://github.com/marmot-protocol/nostr-openmls) — **legacy-spec, archived** — Pre-MDK OpenMLS/Nostr library.
- [mls-ts](https://github.com/marmot-protocol/mls-ts) — **adjacent, archived** — Historical TypeScript MLS exploration, not a Marmot implementation.
- [dr.marmot](https://github.com/marmot-protocol/dr.marmot) — **adjacent, archived** — Diagnostic tool superseded by later Nostr diagnostics.

## Discovery and verification

The [weekly discovery workflow](.github/workflows/discover.yml) scans the Marmot Protocol organization, Zapstore's signed app metadata, Nostr Recap, and NostrMag's signed article-share events. NostrMag intake is anchored to event [`de399234…e19b`](https://njump.me/de399234b408ce0bf401c49004fb57342186c843917f94478dfaf54e7eeee19b), which points to its weekly Nostr roundup.

Roundups, store listings, newsletters, and search results are leads, not proof. The workflow retains event IDs, authors, relays, and URLs; deduplicates them against this catalog and prior intake; then requires a canonical repository, explicit Marmot evidence, and recent repository activity. It opens a review PR only when a new verified candidate exists and never edits this catalog automatically. See [the discovery runbook](docs/discovery.md) for the audit and failure model.

## Contributing

Pull requests are welcome. For each entry, include:

- its canonical public source repository, or for a closed-source app a verified public release/metadata repository that clearly identifies the private source boundary;
- primary-source evidence that it implements or directly supports Marmot, not merely MLS or encrypted Nostr DMs;
- separate protocol-generation and repository-activity labels;
- a one-line factual description, with maturity claims only when the maintainer supplies them.

Avoid duplicate platform wrappers, renamed repositories, empty scaffolds, and claims copied only from secondary sources. CI checks catalog structure, duplicate canonical URLs, required first-party connectors, and discovery regressions; maintainers verify time-sensitive evidence during review.
