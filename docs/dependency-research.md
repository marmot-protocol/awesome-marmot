# Marmot v2 discovery and dependencies

Current source and metadata: [4 November refresh](catalog-refresh-20261104.md) and [audit snapshot](../data/catalog-audit.json). Dated sections below retain their original evidence; later classifications supersede them.

Checked 2026-10-17. This pass follows application manifests, lockfiles and implementation code through the messaging engines. Protocol generation describes inspected source. Runtime interoperability, delivered binaries and security require separate qualification. Search coverage is bounded by public indexing.

## Additions

| Project | Dependency path and source limits |
| --- | --- |
| [Nostrautica](https://github.com/jooray/nostrautica/tree/b2205c348e5368c308b2ff2064361f104cd1053d) | PWA/coordinator workspace → vendored marmot-ts `0ab8336aea322dba8b4fa57697e9cdf686292a9b` → ts-mls `af6d1c599f2912fda5fbcac1b461fdd3013e37c7`. Android uses MarmotKit 0.12.0 with a committed checksum. Its [release source](https://github.com/marmot-protocol/mdk/blob/122bd90ffac60bb6311346e228d0f609a18521ee/crates/cgka-engine/src/account_identity_proof.rs) implements current 0x8009 identity proofs; APK bytes remain untested. Identity proof 0x8009 appears in actual engine code. Interoperability statements remain developer reports. |
| [Nostrbase](https://github.com/shroominic/nostrbase/tree/c3cd7609edc455d293f877c581041b0a20edef4f) | SDK → committed marmot-ts 0.6.0 tar → upstream `591eb25f6ba0b69cb6dc7b711fb75836da7ddbaa` plus two patches → bundled ts-mls `af6d1c599f2912fda5fbcac1b461fdd3013e37c7`. The tar checksum and identity-proof implementation were inspected. Fieldwork is an example app. |
| [cl-marmot](https://github.com/modus-lisp/cl-marmot/tree/4976cca038fe4ad495f165aaf790e8d7c450ac05) | Own MLS engine → natrium, secp256k1-fast, seal, cl-nostr and bordeaux-threads. Dependencies use unpinned ASDF/local checkouts. cl-nostr requires its marmot-rumors branch. Component codecs and 0x8009 proof establish v2 source; reported interop remains developer evidence. |
| [emissary](https://github.com/modus-lisp/emissary/tree/a77eb86bda280712f43c1c56f42e3bff23d5e3b4) | Optional cl-marmot transport → the independently inspected cl-marmot stack above. The integration invokes account, key-package and message APIs. Its dependency is unpinned, so this describes a compatible source path. Research software with shell-equivalent principal authority. |
| [quartz-marmot-kmp](https://github.com/kngako/quartz-marmot-kmp/tree/c3783a26b96c7fedbf47a504a8ecf817ffd0d6b9) | Own MLS/component implementation → Quartz 1.14.0 for Nostr events, plus Kotlin crypto HMAC/SHA2 0.0.4. Concrete app components establish v2. README reports JVM builds; Android/native builds and persistence/convergence have known gaps. Maven publication remains pending. |

Exact manifest, lock and implementation references appear in [the discovery evidence](../data/dependency-research-20261017.json). Each addition has an immutable source identity in [the catalog audit](../data/catalog-audit.json).

## Existing library families

| Family | Inspected dependency surface |
| --- | --- |
| MDK | [Workspace lock](https://github.com/marmot-protocol/mdk/blob/7692e26649193bd0bfba5f6a425a80b7c2e8f502/Cargo.lock) resolves OpenMLS 0.8.1 and RustCrypto provider from fork `59e7d3b27a7e95237879dd5478de1fd90eff7ada`, rust-nostr 0.45.5 fork `a9c7a6423d104c603de6ea8244265ea17f0f9d89`, and rusqlite 0.40.1. The catalog v2 workspace differs from registry MDK 0.8.0. |
| marmot-ts | [Package](https://github.com/marmot-protocol/marmot-ts/blob/591eb25f6ba0b69cb6dc7b711fb75836da7ddbaa/package.json) and [lock](https://github.com/marmot-protocol/marmot-ts/blob/591eb25f6ba0b69cb6dc7b711fb75836da7ddbaa/pnpm-lock.yaml) use a workspace ts-mls submodule at `af6d1c599f2912fda5fbcac1b461fdd3013e37c7`, bundled during publication. Direct runtime declarations include HPKE core 1.9.0, Noble crypto and Applesauce. Optional HPKE suites stay optional. |
| Quartz in Amethyst | [Build](https://github.com/vitorpamplona/amethyst/blob/3613bf05927c3523d9d0cee77cd71d2aa835dca4/quartz/build.gradle.kts) and [version catalog](https://github.com/vitorpamplona/amethyst/blob/3613bf05927c3523d9d0cee77cd71d2aa835dca4/gradle/libs.versions.toml) declare target-specific crypto providers, secp256k1 KMP JNI 0.24.0, Kotlin HMAC/SHA2 0.0.4 and SQLite drivers. The separate quartz-marmot-kmp implementation above has its own MLS code. |
| Scramble engine | [Engine references](https://github.com/DavidGershony/Scramble/blob/25473e7396e25e1bda83a7824c785c9a660f03de/src/Scramble.Marmot.Engine/Scramble.Marmot.Engine.csproj) use in-repository dotnet-mls and crypto projects. [Core](https://github.com/DavidGershony/Scramble/blob/25473e7396e25e1bda83a7824c785c9a660f03de/src/Scramble.Core/Scramble.Core.csproj) declares BouncyCastle 2.5.1, NBitcoin.Secp256k1 3.1.6 and Microsoft.Data.Sqlite 9.0.0. Standalone historical marmot-cs is a different engine. |
| libmarmot in nostrc | [Build](https://github.com/chebizarro/nostrc/blob/3e647abfabc266ad8b3f7443a46a26851f01e5c4/libmarmot/CMakeLists.txt) requires system OpenSSL, libsodium and libsecp256k1; SQLite is optional. System versions depend on the build environment. The adopted key-package producer is enabled by default at this source pin. |
| mdk-odin | The retained [source](https://gitworkshop.dev/cyberguy.fyi/relay.ngit.dev/mdk-odin/tree/42d93e288f17a870bb3e973ad18f0c2f0edd1085) identifies an independent Odin engine. Its prior account-proof/component audit remains dated 2026-10-08. A fresh dependency lock was unavailable in this pass; the MDK 0.12.0 migration target expresses a compatibility goal. |

[Manifest and lock inventory](../data/library-dependencies-20261017.json) retains declarations and resolved packages for the inspected families. These records retain their source dates. Protocol classification requires implementation evidence alongside dependency versions. The same OpenMLS package can carry different Marmot profiles.

## Candidates excluded from the v2 additions

| Candidate | Source-backed reason |
| --- | --- |
| [Sovran](https://github.com/SovranBitcoin/Sovran/tree/28adc886a288b667938ac12abd855ef7846acec3) | React Native Bitcoin wallet; dependency exists but current vendored engine is old dist MIP profile. Complete app integration tracing remains open. |
| [Sedecim](https://github.com/sedecim-com/nostr/tree/1efcb156decf19edcee25d4eeaee536272cc3e0a) | Real source UI and provider adapter, but MIP media v2 is NOT Marmot protocol v2; provider pins deprecated marmot-ts0.5.1, types include10051 legacy relay discovery. |
| [Hyperpipe](https://github.com/squip/hyperpipe/tree/859c3bb1f81c9e669fc513b93e792c83630ab88c) | Desktop/TUI modular chat application, inactive >90days; real MarmotService but old0.4.0 npm engine. |
| [marmot_dart](https://github.com/codeswot/marmot_dart/tree/ef6f0088cc96246d6d1daae106490e5025f49be1) | Registry MDK0.8.0 and default mip04 feature. Downloaded exact mdk-core0.8.0 source documents monolithic MIP-01 NostrGroupDataExtension; not adopted v2. Current Git source plus hosted package0.0.8 rust manifest/lock inspected. Dart FFI API over MDK, not independent protocol. |
| [ZapBook](https://github.com/codeswot/ZapBook/tree/ddbd4814f0b16b1ea621df99c027314c969b1333) | Flutter library/book app. pubspec marmot_dart^0.0.8 locks hosted0.0.8 SHA256ce868adef11eb6d96730cc15b503f3816eff7efc1c96b1b58a97b173353c98c8. Downloaded exact pub archive contains MDK0.8.0 registry source/lock and mip04, so no v2 upgrade inferred from latest Git source. |
| [chirp](https://github.com/pablof7z/chirp/tree/e8b11748e910149c7c73111471e15c3d02c4b777) | Marmot runtime explicitly installs nmp_marmot and optional feature. Cargo pins nmp-marmot to nostr-multi-platform bc6b42592d7fd61bc6767cac246a24a6b23bf8e3; exact upstream crates/nmp-marmot/Cargo.toml and Chirp lock resolve mdk-core0.8.0, OpenMLS0.8.1. Multi-platform Nostr app with actual group runtime, but MIP-era/v1, not v2. |
| [filestr](https://github.com/futpib/filestr/tree/1ad4632ce21fce24a886e6bd2b757339eb134632) | Friend-to-friend file sharing with actual MDK group hubs chat plane enabled by default daemon chat feature; registry mdk-core0.8.0 plus OpenMLS0.8.1 lock. MIP-era/v1. Android Flutter front-end is files-only/iroh-only: do not claim Android Marmot messaging. No interop verified. |

Additional searches found CodeDeck Next and Pacto Bot API pinned to registry MDK 0.8.0, Purser pinned to MDK 0.7.1, and cashu_mls_chat using MDK 0.5.1. These were excluded from v2 additions. Concord describes an alternative community protocol; Airhop uses Noise and Double Ratchet. Forensic VMDK libraries and audit mirrors are unrelated search matches.

## Reproduction

Inspect the pinned source links and resolve local overrides, workspaces, submodules and vendored archives before assigning a generation. Compare the actual application path with its locked engine. Distinguish optional adapters from default transports and developer interop claims from independently observed results. Archive checks inspected data; candidate install scripts stayed unexecuted.

The catalog checker validates record shape, matching labels and link structure. It does not certify remote code or runtime compatibility. Older catalog entries retain their original audit dates.
