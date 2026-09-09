# Awesome Marmot

A curated catalog of software that implements or directly supports the [Marmot Protocol](https://github.com/marmot-protocol/marmot): MLS-based, end-to-end encrypted group messaging transported over Nostr.

> **Project status:** **active** means its canonical repository has had public activity within the last 12 months. **inactive** means the repository is writable but has not. **beta/experimental** is the maintainer's own maturity signal. **archived** means the canonical repository is read-only or superseded. Activity is not a security endorsement; review each project's threat model and release notes before relying on it.

## Contents

- [Apps](#apps)
- [Agent and automation integrations](#agent-and-automation-integrations)
- [SDKs and libraries](#sdks-and-libraries)
- [Infrastructure and developer tools](#infrastructure-and-developer-tools)
- [Examples](#examples)
- [Archived and superseded projects](#archived-and-superseded-projects)
- [Discovery and verification](#discovery-and-verification)
- [Contributing](#contributing)

## Protocol

- [marmot](https://github.com/marmot-protocol/marmot) — **active** — Specification, Marmot Improvement Proposals (MIPs), and interoperability material.

## Apps

### Messaging clients

- [White Noise for Android](https://github.com/marmot-protocol/whitenoise-android) — **active** — Native Android White Noise client.
- [White Noise for iOS](https://github.com/marmot-protocol/whitenoise-ios) — **active** — Native iOS White Noise client.
- [White Noise for macOS](https://github.com/marmot-protocol/whitenoise-mac) — **active** — Native macOS White Noise client.
- [White Noise for Linux](https://github.com/marmot-protocol/whitenoise-linux) — **active** — Rust/Slint desktop client; its repository points contributors to the canonical NIP-34 repository.
- [wn-tui](https://github.com/marmot-protocol/wn-tui) — **active** — Terminal White Noise client.
- [pika](https://github.com/justinmoon/pika) — **active, alpha** — Cross-platform encrypted messenger with a Rust core and MDK.
- [Scramble](https://github.com/DavidGershony/Scramble) — **active** — Desktop and Android Marmot client implemented with `marmot-cs`.
- [Marmota](https://github.com/dcadenas/marmota) — **active, experimental** — Browser client built with `marmot-ts` and local IndexedDB storage.
- [amethyst](https://github.com/vitorpamplona/amethyst) — **active** — Kotlin Multiplatform Nostr client whose Quartz layer includes an embedded MDK implementation.
- [amy](https://github.com/vitorpamplona/amethyst/tree/main/cli) — **active** — Amethyst's CLI for Marmot/MLS group operations.

### Location, media, and device apps

- [Haven](https://github.com/mehmetefeumit/Haven-App) — **active** — Private Android/iOS location sharing over Marmot, without a central account service.
- [Mafrend](https://github.com/DestBro/mafrend-zapstore) — **active, alpha, closed-source** — Map-first Nostr social app with Marmot-based private groups, invitations, group maps, and encrypted group media; the linked public repository hosts Zapstore metadata and APK releases rather than the private app source.
- [Whistle](https://github.com/sjmcnamara/whistle) — **active** — Cross-platform group location sharing and chat over Nostr, MLS, and Marmot.
- [Sonar](https://github.com/hedwig-corp/bitchat-to-sonar) — **active** — Bluetooth/Nostr messenger and wallet with Marmot group DMs interoperable with White Noise.
- [FMDtr](https://gitlab.com/Kalle/fmdtr-android) — **active** — Android device finder and remote-control app with Marmot, SMS, messenger, and server transports.
- [tubestr-v2](https://github.com/Tubestr/tubestr-v2) — **active** — Private family video sharing built on Nostr and Marmot.

## Agent and automation integrations

- [agentnoise](https://github.com/nvk/agentnoise) — **active** — Desktop bridge that uses White Noise as a control surface for local coding-agent sessions.
- [openclaw-marmot](https://github.com/tkhumush/openclaw-marmot) — **active** — OpenClaw channel plugin for MLS-encrypted Marmot messaging.
- [hermes-marmot](https://github.com/notmandatory/hermes-marmot) — **active** — Hermes Agent gateway plugin built with `mdk-python`.
- [botburrow](https://github.com/marmot-protocol/botburrow) — **active** — Bot infrastructure for Marmot groups.
- [burrow](https://github.com/CentauriAgent/burrow) — **active** — Marmot CLI for encrypted communication between people and agents.
- [marmot-cli](https://github.com/kai-familiar/marmot-cli) — **active** — Rust CLI interoperable with White Noise.
- [dockerized-marmot-cli](https://github.com/rphilbrdigits/dockerized-marmot-cli) — **active** — Containerized packaging for on-demand Marmot CLI use.
- [NostrBotKit](https://codeberg.org/Tuxor/NostrBotKit) — **active** — Self-hosted bot framework with Marmot group support.

## SDKs and libraries

- [mdk](https://github.com/marmot-protocol/mdk) — **active** — Reference Rust Marmot Development Kit and current core stack.
- [marmot-ts](https://github.com/marmot-protocol/marmot-ts) — **active** — TypeScript implementation of Marmot.
- [marmot-cs](https://github.com/DavidGershony/marmot-cs) — **active** — C# Marmot/MDK implementation.
- [mdk-web](https://github.com/marmot-protocol/mdk-web) — **active** — Web/WASM bindings for MDK.
- [quartz](https://github.com/vitorpamplona/quartz) — **active** — Kotlin Multiplatform Nostr library with an embedded MDK implementation.
- [openmls-sled-storage](https://github.com/marmot-protocol/openmls-sled-storage) — **inactive** — OpenMLS storage traits backed by Sled; no public repository activity in the last 12 months.
- [openmls-redb-storage](https://github.com/marmot-protocol/openmls-redb-storage) — **inactive** — OpenMLS storage traits backed by Redb; no public repository activity in the last 12 months.
- [openmls-lmdb-storage](https://github.com/marmot-protocol/openmls-lmdb-storage) — **inactive** — OpenMLS storage traits backed by LMDB; no public repository activity in the last 12 months.

## Infrastructure and developer tools

- [transponder](https://github.com/marmot-protocol/transponder) — **active** — MIP-05 notification server.
- [goggles](https://github.com/marmot-protocol/goggles) — **active** — Explorer for `marmot-forensics-audit/v1` JSONL traces.
- [nostr-doctor](https://github.com/marmot-protocol/nostr-doctor) — **active** — Nostr user and pubkey diagnostics.
- [propose](https://github.com/marmot-protocol/propose) — **active** — MLS proposal/commit scenario test harness.
- [marmot-server](https://github.com/nmadd57/marmot-server) — **active** — Local Docker service exposing a REST API for Marmot.

## Examples

- [marmots-web-chat](https://github.com/marmot-protocol/marmots-web-chat) — **active** — Browser chat reference implementation for `marmot-ts`.
- [mdk-python-example](https://github.com/marmot-protocol/mdk-python-example) — **active** — Python binding example.
- [mdk-kotlin-example](https://github.com/marmot-protocol/mdk-kotlin-example) — **active** — Kotlin binding example.
- [mdk-ruby-example](https://github.com/marmot-protocol/mdk-ruby-example) — **active** — Ruby binding example.

## Archived and superseded projects

These remain useful for history and migration research, but should not be presented as current foundations.

- [whitenoise](https://github.com/marmot-protocol/whitenoise) — **archived** — Superseded Flutter White Noise app.
- [whitenoise-rs](https://github.com/marmot-protocol/whitenoise-rs) — **archived** — Former White Noise Rust core and CLI; current development moved to MDK and native clients.
- [mdk-kotlin](https://github.com/marmot-protocol/mdk-kotlin), [mdk-python](https://github.com/marmot-protocol/mdk-python), [mdk-ruby](https://github.com/marmot-protocol/mdk-ruby), and [mdk-swift](https://github.com/marmot-protocol/mdk-swift) — **archived** — Historical standalone binding repositories.
- [nostr-openmls](https://github.com/marmot-protocol/nostr-openmls) — **archived** — Pre-MDK OpenMLS/Nostr library.
- [mls-ts](https://github.com/marmot-protocol/mls-ts) — **archived** — Historical TypeScript MLS exploration.
- [dr.marmot](https://github.com/marmot-protocol/dr.marmot) — **archived** — Superseded by `nostr-doctor`.

## Discovery and verification

The [weekly discovery workflow](.github/workflows/discover.yml) scans the Marmot Protocol organization, Zapstore's signed app metadata, Nostr Recap, and NostrMag's signed article-share events. NostrMag intake is anchored to event [`de399234…e19b`](https://njump.me/de399234b408ce0bf401c49004fb57342186c843917f94478dfaf54e7eeee19b), which points to its weekly Nostr roundup.

Roundups, store listings, Compass, and search results are **leads, not proof**. The workflow retains event IDs, authors, relays, and URLs; deduplicates them against this catalog and prior intake; then requires a canonical repository, explicit Marmot evidence, and recent repository activity. It opens a review PR only when a new verified candidate exists and never edits this catalog automatically. See [the discovery runbook](docs/discovery.md) for the audit and failure model.

## Contributing

Pull requests are welcome. For each entry, include:

- its canonical public source repository, or for a closed-source app a verified public release/metadata repository that clearly identifies the private source boundary;
- primary-source evidence that it implements or directly supports Marmot, not merely MLS or encrypted Nostr DMs;
- a one-line, factual description and honest maturity/status label;
- evidence of maintenance, or an explicit archived/unmaintained label.

Avoid duplicate platform wrappers, renamed repositories, and claims copied only from a roundup. CI checks catalog structure, duplicate canonical URLs, and discovery regression tests; maintainers verify time-sensitive link and status evidence during review.
