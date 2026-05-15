# Awesome Marmot [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

A curated list of apps, libraries, and tools built on the [Marmot Protocol](https://github.com/marmot-protocol/marmot) — MLS-based end-to-end encrypted group messaging over Nostr.

## Contents

- [Protocol](#protocol)
- [Applications](#applications)
- [SDKs & Libraries](#sdks--libraries)
- [Tools & Infrastructure](#tools--infrastructure)
- [Storage Adapters](#storage-adapters)
- [Reference Implementations](#reference-implementations)

---

## Protocol

- [marmot](https://github.com/marmot-protocol/marmot) — The Marmot Protocol specification. MLS + Nostr for efficient, decentralized, end-to-end encrypted group messaging.
- [marmot-web](https://github.com/marmot-protocol/marmot-web) — The Marmot Protocol website.

## Applications

- [whitenoise](https://github.com/marmot-protocol/whitenoise) — White Noise Flutter app. Private, decentralized messenger built on Nostr and MLS. No phone. No email. No compromise.
- [whitenoise-rs](https://github.com/marmot-protocol/whitenoise-rs) — The Rust core library powering White Noise.
- [whitenoise-web](https://github.com/marmot-protocol/whitenoise-web) — White Noise marketing website.
- [whitenoise-podcast](https://github.com/marmot-protocol/whitenoise-podcast) — White Noise Podcast content and episodes.
- [wn-tui](https://github.com/marmot-protocol/wn-tui) — Terminal UI client for White Noise.

## SDKs & Libraries

- [mdk](https://github.com/marmot-protocol/mdk) — Marmot Development Kit. The core SDK for building Marmot-compatible apps.
- [mdk-kotlin](https://github.com/marmot-protocol/mdk-kotlin) — Kotlin bindings for the MDK.
- [mdk-python](https://github.com/marmot-protocol/mdk-python) — Python bindings for the MDK.
- [mdk-ruby](https://github.com/marmot-protocol/mdk-ruby) — Ruby bindings for the MDK.
- [mdk-swift](https://github.com/marmot-protocol/mdk-swift) — Swift bindings for the MDK.
- [mdk-web](https://github.com/marmot-protocol/mdk-web) — Web/WASM bindings for the MDK.
- [marmot-ts](https://github.com/marmot-protocol/marmot-ts) — TypeScript implementation of the Marmot Protocol.

## Tools & Infrastructure

- [transponder](https://github.com/marmot-protocol/transponder) — MIP-05 Marmot notifications server, implemented in Rust.
- [nostr-doctor](https://github.com/marmot-protocol/nostr-doctor) — Diagnoses issues with Nostr users and pubkeys.
- [botburrow](https://github.com/marmot-protocol/botburrow) — Bot infrastructure for Marmot.
- [proton-beam](https://github.com/marmot-protocol/proton-beam) — Nostr events to Protobuf conversion.
- [propose](https://github.com/marmot-protocol/propose) — Test harness for MLS proposal and commit scenarios.

## Storage Adapters

- [openmls-sled-storage](https://github.com/marmot-protocol/openmls-sled-storage) — OpenMLS storage traits implemented with the Sled embedded database.
- [openmls-redb-storage](https://github.com/marmot-protocol/openmls-redb-storage) — OpenMLS storage traits implemented with Redb.
- [openmls-lmdb-storage](https://github.com/marmot-protocol/openmls-lmdb-storage) — OpenMLS storage traits implemented with LMDB.

## Reference Implementations

- [marmots-web-chat](https://github.com/marmot-protocol/marmots-web-chat) — Reference web chat implementation using marmoTS.
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
