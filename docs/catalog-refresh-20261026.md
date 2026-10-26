# Catalog refresh, 26 October 2026

The [current snapshot](../data/catalog-audit.json) contains 75 repositories. This refresh rechecked default branches, archive flags and commit dates for the previous 72 records and added three projects. Changed implementations were reviewed through pinned dependency manifests and relevant source files. The older [verification report](catalog-verification.md) remains a dated history; its original classifications do not override this refresh.

## Additions

| Project | Classification | Evidence and limits |
| --- | --- | --- |
| [Mantra](https://code.sigidli.com/mantra/mantra-kmp) | v1, active, alpha | Public Kotlin Multiplatform application for translation workgroups and threshold-signing approvals. Its app calls MIP-01 group creation and pins Quartz 1.14.0, whose source implements the older `0xf2ee` group-data extension and BasicCredential identity matching. The custom in-group private-message format requires an author-check carve-out in other clients. |
| [wn-notify](https://github.com/jooray/wn-notify) | v2, active | Small Python notification/file CLI using the `marmot.agent-control.v2` Unix-socket boundary of an existing local `wn-agent`. The label follows that transport; the wrapper has no independent MLS engine. |
| [RelayRider](https://github.com/davidjj999/relayrider) | adjacent, inactive | Browser relay evaluator with NIP-11 checks and publication/query probes. Its synthetic kind-30443 event has empty content. Acceptance tests relay handling, not cryptographic KeyPackage validity. Last default-branch commit: 11 July 2026. |

Mantra's canonical source is the public Sigidli repository, not its separate GitHub website repository. App version numbers and names are insufficient evidence of a protocol generation. The snapshot links each addition's immutable source and records the SHA-256 of Mantra's inspected Maven source archive.

## Corrections to existing entries

- **Whistle:** current iOS pre-release source uses Marmot v2 through MarmotKit 0.10.4. Android production remains on v1. The catalog now states that platform difference beside the app.
- **Quartz:** the standalone repository is now an active Nostr library with Marmot event types. It moved from historical projects to supporting tools. The Marmot and MLS engines remain separate libraries, `marmot-kmp` and `mls-kmp`.
- **Amethyst:** current manifests use externally published Quartz 2.3.0 and marmot-kmp 2.0.0; the snapshot no longer describes the implementation as bundled in the old in-tree Quartz module.
- **marmots-web-chat:** npm marmot-ts 0.7 and the current account-signer profile replace the old submodule and early proof implementation. Deleted evidence paths were replaced with the current manifest and lockfile.
- **codr:** current source supports Linux and macOS and pins MDK 0.14.0 with its connector patch. The entry includes editable progress and current media support.
- **Nostrautica:** Android tooling now pins MarmotKit 0.14.0. The snapshot links its current checksum file.
- **Wizard Messenger:** the alpha now documents a unified Matrix/Telegram inbox and AppStore installation. Its plaintext local history and Telegram encryption boundary remain explicit.
- **Facet:** its 24 July commit is outside the current 90-day window, so it moved to projects without recent commits. The old Python and Kotlin examples are now archived and moved accordingly.
- **ShyChat, mdk-odin and coinos v3:** current heads were read from their actual Git servers, with canonical browsing links retained. ShyChat now pins marmot-ts 0.8.0; mdk-odin still lists mixed-engine interoperability and independent review as release gates.

## Scope of verification

The snapshot separates current default-branch activity from historical release evidence. Groundhog's alpha5 source and desktop release references retain their original release commits. A refreshed source revision does not establish that a downloaded store build contains it.

These are public source and metadata checks. No installation, relay publication, message delivery or cross-client interoperability test was performed. A signed KeyPackage-shaped event can still be empty, expired or incompatible; catalog inclusion does not certify contactability or implementation security.

Run the offline catalog checker and unit suite after changing entries. They validate inventory retention, protocol/activity labels, immutable evidence links, section placement and the 90-day window without contacting the network.
