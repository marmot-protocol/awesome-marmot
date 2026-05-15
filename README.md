# Awesome Marmot

A curated list of apps, libraries, and tools built on the [Marmot Protocol](https://github.com/marmot-protocol/marmot) — MLS-based end-to-end encrypted group messaging over Nostr.

## Contents

- [Protocol](#protocol)
- [Applications](#applications)
- [SDKs & Libraries](#sdks--libraries)
- [Tools & Infrastructure](#tools--infrastructure)
- [Storage Adapters](#storage-adapters)
- [Demo Apps](#demo-apps)

---

## Protocol

- [marmot](https://github.com/marmot-protocol/marmot) — The Marmot Protocol specification. MLS + Nostr for efficient, decentralized, end-to-end encrypted group messaging.

## Applications

- [whitenoise](https://github.com/marmot-protocol/whitenoise) — White Noise Flutter app. Private, decentralized messenger built on Nostr and MLS. No phone. No email. No compromise.
- [whitenoise-cli](https://github.com/marmot-protocol/whitenoise-rs/tree/main/crates/whitenoise-cli) — Command-line interface for White Noise, part of the whitenoise-rs workspace.
- [wn-tui](https://github.com/marmot-protocol/wn-tui) — Terminal UI client for White Noise.
- [agentnoise](https://github.com/nvk/agentnoise) — Native desktop helper for using White Noise as the control surface for local Codex and Claude sessions. Rust-first, no Node/npm/bun in the trusted bridge path.
- [pika](https://github.com/sledtools/pika) — Marmot-based encrypted messaging app.
- [tubestr-v2](https://github.com/Tubestr/tubestr-v2) — Private family video sharing for parents and kids, built on Nostr and Marmot.
- [Vector](https://github.com/VectorPrivacy/Vector) — Peer-to-peer multiplayer game using Nostr for discovery, Marmot for encryption, and Iroh for QUIC transport.
- [Scramble](https://github.com/DavidGershony/Scramble) — Nostr-based encrypted messenger with MLS group encryption.
- [openclaw-marmot](https://github.com/tkhumush/openclaw-marmot) — OpenClaw channel plugin for Marmot Protocol. End-to-end encrypted Nostr messaging via MLS.

## SDKs & Libraries

- [mdk](https://github.com/marmot-protocol/mdk) — Marmot Development Kit. The core SDK for building Marmot-compatible apps.
- [whitenoise-rs](https://github.com/marmot-protocol/whitenoise-rs) — The Rust core library powering White Noise.
- [mdk-kotlin](https://github.com/marmot-protocol/mdk-kotlin) — Kotlin bindings for the MDK.
- [mdk-python](https://github.com/marmot-protocol/mdk-python) — Python bindings for the MDK.
- [mdk-ruby](https://github.com/marmot-protocol/mdk-ruby) — Ruby bindings for the MDK.
- [mdk-swift](https://github.com/marmot-protocol/mdk-swift) — Swift bindings for the MDK.
- [mdk-web](https://github.com/marmot-protocol/mdk-web) — Web/WASM bindings for the MDK.
- [marmot-ts](https://github.com/marmot-protocol/marmot-ts) — TypeScript implementation of the Marmot Protocol.
- [quartz](https://github.com/vitorpamplona/quartz) — Nostr library for Kotlin Multiplatform, used by Amethyst. Includes an embedded MDK implementation aligned with MIP-01 and MIP-05.
- [marmot-cs](https://github.com/DavidGershony/marmot-cs) — C# MDK implementation. Secure group messaging with MLS (RFC 9420) and Nostr.

## Tools & Infrastructure

- [transponder](https://github.com/marmot-protocol/transponder) — MIP-05 Marmot notifications server, implemented in Rust.
- [nostr-doctor](https://github.com/marmot-protocol/nostr-doctor) — Diagnoses issues with Nostr users and pubkeys.
- [botburrow](https://github.com/marmot-protocol/botburrow) — Bot infrastructure for Marmot.
- [propose](https://github.com/marmot-protocol/propose) — Test harness for MLS proposal and commit scenarios.
- [burrow](https://github.com/CentauriAgent/burrow) — Marmot Protocol CLI for encrypted messaging, targeting AI agents and humans.
- [marmot-cli](https://github.com/kai-familiar/marmot-cli) — Rust CLI for E2E encrypted messaging over Nostr via Marmot. Compatible with White Noise.
- [marmot-server](https://github.com/nmadd57/marmot-server) — Local Docker server with a REST API for the Marmot protocol.
- [dockerized-marmot-cli](https://github.com/rphilbrdigits/dockerized-marmot-cli) — Dockerized marmot-cli for on-demand E2E encrypted Nostr DMs.
- [burrow](https://github.com/CentauriAgent/burrow) — Marmot Protocol CLI for E2E encrypted messaging, built for AI agents and humans.
- [marmot-cli](https://github.com/kai-familiar/marmot-cli) — Rust CLI for E2E encrypted messaging over Nostr using Marmot. Compatible with White Noise.
- [marmot-server](https://github.com/nmadd57/marmot-server) — Local Docker server with a REST API for Marmot Protocol group messaging.
- [dockerized-marmot-cli](https://github.com/rphilbrdigits/dockerized-marmot-cli) — Dockerized marmot-cli for on-demand E2E encrypted Nostr DMs.

## Storage Adapters

- [openmls-sled-storage](https://github.com/marmot-protocol/openmls-sled-storage) — OpenMLS storage traits implemented with the Sled embedded database.
- [openmls-redb-storage](https://github.com/marmot-protocol/openmls-redb-storage) — OpenMLS storage traits implemented with Redb.
- [openmls-lmdb-storage](https://github.com/marmot-protocol/openmls-lmdb-storage) — OpenMLS storage traits implemented with LMDB.

## Demo Apps

- [marmots-web-chat](https://github.com/marmot-protocol/marmots-web-chat) — Web chat demo using marmoTS.
- [mdk-python-example](https://github.com/marmot-protocol/mdk-python-example) — Example usage of the MDK Python bindings.
- [mdk-kotlin-example](https://github.com/marmot-protocol/mdk-kotlin-example) — Example usage of the MDK Kotlin bindings.
- [mdk-ruby-example](https://github.com/marmot-protocol/mdk-ruby-example) — Example usage of the MDK Ruby bindings.

---

## Contributing

Pull requests welcome. Add your Marmot-compatible project by opening a PR — include the repo link and a one-line description.

Make sure the project:
- Is publicly accessible
- Uses the Marmot Protocol (or directly supports it)
- Is actively maintained or clearly labeled otherwise
