# Catalog refresh, 4 November 2026

## Whistle release follow-up, 4 November

Whistle **v2.0.1 is released**, superseding this morning's prerelease status below. The [public GitHub release](https://github.com/sjmcnamara/whistle/releases/tag/v2.0.1) includes Android and iOS artifacts and identifies this as the first public Marmot v2 build, using MarmotKit 0.14.0. Android v2.0.1 is also published on [Zapstore](https://zapstore.dev/apps/naddr1qqtx7un89enk2arhdp5hxarvv5h8w6rfwd6xcegprpmhxue69uhhyetvv9uju7npwpehgmmjv5hxgetkqgszedrn6ruhul9wpzjqsy9zs24w03jugz6q7zcse9cuwhl5qw6fx3srqsqqqlstgdfcxc) under `org.getwhistle.whistle`, version code 73, on the main channel for arm64-v8a.

The signed Zapstore app listing, release and linked asset metadata were verified. The declared APK URL, size and SHA-256 match GitHub's published asset metadata. Their event identities are retained in Whistle's `distribution_evidence` in the [audit snapshot](../data/catalog-audit.json). The [release source](https://github.com/sjmcnamara/whistle/tree/7daf1f9c2d94d76cacf43fd538298de8c5c01e47) pins MarmotKit 0.14.0 in both platform vendoring scripts. Its README still contains a prerelease label; published release records establish the later distribution status.

The publisher warns that **v1 groups cannot carry over or be recovered**. The identity is retained, and every group member must update. Offline chat delivery can be delayed or absent; the release notes report location sharing as unaffected. These are publisher statements, not independent runtime results. No APK installation, iOS App Store availability or cross-client interoperability was verified in this follow-up.

## Scope and inclusion

All 79 existing repository records were rechecked against their public default branches: 73 on GitHub and six on GitLab, Forgejo or canonical Git servers. Nineteen heads changed. Changed source was read against the previous pinned evidence; unchanged implementations retain their existing immutable evidence. Protocol generation, recent activity, maturity, source availability and released-build status remain separate.

Nine previously excluded v1 integrations now appear in the main catalog, bringing the snapshot to 88 repositories. A tracked-project cross-check also found dotnet-mls, bringing the final snapshot to 89. Verified older implementations belong in the v1 section. This corrects the inconsistent treatment of Sonar versus ZapBook and CodeDeck Next. Historical exclusion notes and the seen ledger remain available; the current snapshot supersedes their old inclusion decisions.

| Added v1 project | Implementation evidence |
| --- | --- |
| [codeswot/ZapBook](https://github.com/codeswot/ZapBook/tree/ddbd4814f0b16b1ea621df99c027314c969b1333) | Flutter social-reading app with encrypted reading circles and shared book files through marmot_dart 0.0.8. [Pinned implementation](https://github.com/codeswot/ZapBook/blob/ddbd4814f0b16b1ea621df99c027314c969b1333/pubspec.lock). |
| [JeroenOnNostr/codedeck-next-mobile](https://github.com/JeroenOnNostr/codedeck-next-mobile/tree/4b7f5977491ebf5a5babeea856af53c366535378) | Android remote control for coding sessions through paired laptop/VPS bridges; NIP-17 and legacy MDK messaging coexist. [Pinned implementation](https://github.com/JeroenOnNostr/codedeck-next-mobile/blob/4b7f5977491ebf5a5babeea856af53c366535378/apps/mobile/src-tauri/Cargo.toml). |
| [SovranBitcoin/Sovran](https://github.com/SovranBitcoin/Sovran/tree/7b32dbe390869ad0c660a8cd16eb52c6b5164dc4) | Cashu wallet with a White Noise chat integration and vendored marmot-ts 0.4.0. [Pinned implementation](https://github.com/SovranBitcoin/Sovran/blob/7b32dbe390869ad0c660a8cd16eb52c6b5164dc4/app/vendor/marmot-ts/package.json). |
| [covenant-gov/pacto-app](https://github.com/covenant-gov/pacto-app/tree/5c0e5e864a0499f6ba4b8bab4780215fdf25b5b2) | Community organizing app with legacy MDK group messaging beside NIP-17 DMs and governance/wallet integrations. [Pinned implementation](https://github.com/covenant-gov/pacto-app/blob/5c0e5e864a0499f6ba4b8bab4780215fdf25b5b2/src-tauri/Cargo.toml). |
| [covenant-gov/pacto-bot-api](https://github.com/covenant-gov/pacto-bot-api/tree/fdd630b1e5f1f13e30c3f3a12da462d40988a2fe) | Self-hosted Rust multi-bot daemon exposing JSON-RPC over local sockets or HTTP; pins MDK 0.8.0. [Pinned implementation](https://github.com/covenant-gov/pacto-bot-api/blob/fdd630b1e5f1f13e30c3f3a12da462d40988a2fe/Cargo.toml). |
| [sedecim-com/nostr](https://github.com/sedecim-com/nostr/tree/1efcb156decf19edcee25d4eeaee536272cc3e0a) | Early Nostr application/SDK stack with optional marmot-ts 0.5.1 groups. Managed mode is custodial; not for high-risk use without independent review. [Pinned implementation](https://github.com/sedecim-com/nostr/blob/1efcb156decf19edcee25d4eeaee536272cc3e0a/packages/marmot-adapter/package.json). |
| [paytaca/paytaca-app](https://github.com/paytaca/paytaca-app/tree/6be1bd3e91ae45c14ba419b0fb45c13db6bc35a7) | Source-available Bitcoin Cash wallet; custom ts-mls transport implements the legacy 0xf2ee Nostr group-data profile. Proprietary license. [Pinned implementation](https://github.com/paytaca/paytaca-app/blob/6be1bd3e91ae45c14ba419b0fb45c13db6bc35a7/src/services/mls/context.js). |
| [toddsmith456/nurunuru-android](https://github.com/toddsmith456/nurunuru-android/tree/4d871f4d4f0143dab7742ccc9d312701b9fcb9f1) | English Android fork of archived null--nostr. Timeline, Amber/passkey login and group chat; locked mdk-core 0.8.0. [Pinned implementation](https://github.com/toddsmith456/nurunuru-android/blob/4d871f4d4f0143dab7742ccc9d312701b9fcb9f1/rust-engine/Cargo.lock). |
| [Marc26z/nostr-grocery](https://github.com/Marc26z/nostr-grocery/tree/892dfb6d8865affb8a6dbcd0ca7bf442001af073) | Browser shared shopping lists and household pantry, with list chat through marmot-ts 0.5.1. [Pinned implementation](https://github.com/Marc26z/nostr-grocery/blob/892dfb6d8865affb8a6dbcd0ca7bf442001af073/package.json). |

ZapBook's lock resolves marmot_dart 0.0.8. The [published source archive](https://pub.dev/api/archives/marmot_dart-0.0.8.tar.gz) matched its locked SHA-256; the archive's Rust manifest pins mdk-core 0.8.0. CodeDeck Next pins MDK 0.8 and invokes it through its native messaging commands. It is distinct from codedeck-plus, which previously removed Marmot.

## Material updates

- Whistle: both platform vendoring scripts now pin MarmotKit 0.14.0, and the README calls app v2.0.1 a prerelease. The newest public GitHub release remains v1.11.2. Source migration does not establish a current v2 store build. [Source](https://github.com/sjmcnamara/whistle/tree/9e9c0e12f26b300701b4e46f33d21645f914b7ba).
- Marmish: v0.2.2 corrective prerelease is documented; the old unreleased-v0.2 description was stale. Keychain consent/recovery, a transport shutdown panic and full cross-platform qualification still have documented gaps. [Source](https://github.com/Epiphytic/marmish/tree/09232ec5596d6eb4a1d74b81764c0547926ca377).
- Wizard Messenger: the public Standard app recipe supersedes private-beta installation instructions. Its plaintext unified-inbox history and Telegram cloud-chat boundary remain explicit. [Source](https://github.com/humanitylabs-org/wizard-messenger/tree/7029085634a5db4264588f53ae396abb75572dc4).
- FMDtr: the current bridge pins the post-MIP MDK crate family at 3fb4b4759ac676b0c21c4c3527074866c9fa4c89, replacing the previous 0.10.4 pin. [Source](https://gitlab.com/Kalle/fmdtr-android/-/blob/45aef78b145eb95417f33d32fe6b62051312b8f3/rust/fmd-marmot-bridge/Cargo.toml).

Mafrend remains closed-source with unknown protocol generation. Its public store-metadata activity cannot establish implementation activity. Paytaca has inspectable source with a proprietary license; source availability is distinct from an open-source license. Alpha/experimental status and wallet-safety limitations remain explicit elsewhere in the catalog.

## Updated heads

| Repository | Checked head | Last commit |
| --- | --- | --- |
| [github.com/marmot-protocol/mdk](https://github.com/marmot-protocol/mdk/tree/c2f7d45c3c7d4bb23837b8fe205404a6c38e9394) | `c2f7d45c3c7d` | 2026-11-04 |
| [github.com/marmot-protocol/whitenoise-android](https://github.com/marmot-protocol/whitenoise-android/tree/56fabb16e9b0b4db9d0e52174238bc44359c48e9) | `56fabb16e9b0` | 2026-11-04 |
| [github.com/marmot-protocol/whitenoise-ios](https://github.com/marmot-protocol/whitenoise-ios/tree/4575ac5024fa2e90135c3898319bf8c02a2925e7) | `4575ac5024fa` | 2026-11-03 |
| [github.com/marmot-protocol/whitenoise-linux](https://github.com/marmot-protocol/whitenoise-linux/tree/05ecedcb03600b0e4b71004e0f2aad3c046e9716) | `05ecedcb0360` | 2026-11-04 |
| [github.com/marmot-protocol/whitenoise-mac](https://github.com/marmot-protocol/whitenoise-mac/tree/d7afafac7b874958233ece2748bdc45b2a343862) | `d7afafac7b87` | 2026-11-04 |
| [github.com/mehmetefeumit/Haven-App](https://github.com/mehmetefeumit/Haven-App/tree/c6b5428022509f338f822f623d54a9aa199510e3) | `c6b542802250` | 2026-11-04 |
| [github.com/sjmcnamara/whistle](https://github.com/sjmcnamara/whistle/tree/9e9c0e12f26b300701b4e46f33d21645f914b7ba) | `9e9c0e12f26b` | 2026-11-04 |
| [github.com/vitorpamplona/amethyst](https://github.com/vitorpamplona/amethyst/tree/34dbdc9d019a5d12357d3222b0809eb4b1ffad06) | `34dbdc9d019a` | 2026-11-04 |
| [github.com/vitorpamplona/quartz](https://github.com/vitorpamplona/quartz/tree/286842f57fa6e3af4d0e8cd241efada1dd867b61) | `286842f57fa6` | 2026-11-03 |
| [gitlab.com/Kalle/fmdtr-android](https://gitlab.com/Kalle/fmdtr-android/-/blob/45aef78b145eb95417f33d32fe6b62051312b8f3/rust/fmd-marmot-bridge/Cargo.toml) | `45aef78b145e` | 2026-11-04 |
| [github.com/chebizarro/nostrc](https://github.com/chebizarro/nostrc/tree/8aaae2f6a196eb748259f648d6baed327f9a3792) | `8aaae2f6a196` | 2026-11-04 |
| [github.com/cameri/nostream](https://github.com/cameri/nostream/tree/a409223f8bf27d5b4695205198bb11260787a2dd) | `a409223f8bf2` | 2026-11-04 |
| [git.coinos.io/coinosv3.git](https://git.coinos.io/coinosv3.git/tree/?id=08821882bc323c3411940f6150b4a731c1833c49) | `08821882bc32` | 2026-11-03 |
| [github.com/Noormohammadiazad/Textor](https://github.com/Noormohammadiazad/Textor/tree/4c0b1fd30f5c59ef8901cc21a098c9614493f050) | `4c0b1fd30f5c` | 2026-11-04 |
| [github.com/humanitylabs-org/wizard-messenger](https://github.com/humanitylabs-org/wizard-messenger/tree/7029085634a5db4264588f53ae396abb75572dc4) | `7029085634a5` | 2026-11-04 |
| [github.com/3DAGI/freedom-app](https://github.com/3DAGI/freedom-app/tree/e5381abf92d652f1916d7f411ac50a598054010b) | `e5381abf92d6` | 2026-11-03 |
| [github.com/Epiphytic/marmish](https://github.com/Epiphytic/marmish/tree/09232ec5596d6eb4a1d74b81764c0547926ca377) | `09232ec5596d` | 2026-11-04 |
| [github.com/Epiphytic/heterodyne-metaharness](https://github.com/Epiphytic/heterodyne-metaharness/tree/96fbe144718b0c4e39423b95cbaeec8f2e59a5b0) | `96fbe144718b` | 2026-11-03 |
| [gitworkshop.dev/npub1w4uswmv6lu9yel005l3qgheysmr7tk9uvwluddznju3nuxalevvs2d0jr5/relay.ngit.dev/nostr-agents](https://gitworkshop.dev/npub1w4uswmv6lu9yel005l3qgheysmr7tk9uvwluddznju3nuxalevvs2d0jr5/relay.ngit.dev/nostr-agents/tree/99ba2da71205ef346f57521ff6e8cce34422fd77) | `99ba2da71205` | 2026-11-04 |

## Discovery

The existing tracked-project registry and 3 November native intake were compared with the pinned catalog and seen ledger. `sledtools/pika` redirects to the listed `justinmoon/pika`; `DavidGershony/openChat` redirects to Scramble. These are aliases, not additions. The current `zerosats/mdk-pwa-reference` endpoint returned 404; source availability remains unverified, not abandoned. The Tether MDK mining worker is unrelated to Marmot.

[dotnet-mls](https://github.com/DavidGershony/dotnet-mls/tree/126e571024eda3c1250ebf6822bae1ba52e1531e) was added as adjacent supporting infrastructure. Its implementation provides MLS; [Scramble’s engine project](https://github.com/DavidGershony/Scramble/blob/25473e7396e25e1bda83a7824c785c9a660f03de/src/Scramble.Marmot.Engine/Scramble.Marmot.Engine.csproj) references its MLS and crypto projects. This does not establish a standalone Marmot client or general cross-client conformance.

The existing discovery script completed once after the classification edits, using a ten-day Nostr window and authenticated GitHub code search. It retained 131 source-event records (68 distinct event IDs), rejected 139 lead records, and produced three automated keyword/activity candidates plus one unverified native-source lead. Configured sources reported no failures. The automated GitLab search was skipped because its token was unavailable.

| Discovery result | Reviewed disposition |
| --- | --- |
| [awesome-nostr](https://github.com/aljazceru/awesome-nostr/tree/3e8a8cd135fa11cac76dcd6219044676ddc1aec7) | Another catalog, not a Marmot implementation. |
| [awesome-marmot](https://github.com/marmot-protocol/awesome-marmot/tree/5bf39cbdb82f8d2d3cd4f61fb770d56aa8243c22) | This catalog proposed itself because configured exclusions were ignored. |
| [whitenoise-web](https://github.com/marmot-protocol/whitenoise-web/tree/71c32f575159e8922223f856bf51f5f4b40333fe) | The White Noise website, not another messaging client. |
| [cordn-kmp](https://github.com/vitorpamplona/cordn-kmp/blob/b65932be962a675d658a5ec3206e09c9a0605114/README.md) | Describes its own coordinator/MCP-over-Nostr protocol. Sharing Quartz and mls-kmp with Amethyst does not establish Marmot implementation; not added. Native announcement aliases were retained. |

The exclusion list is now applied before verification across organization inventory and other discovery sources. The actual White Noise website URL was added to it. A regression test covers organization, signed-note, Zapstore and code-search inputs together, including URL normalization and retained provenance. There was no second live discovery run.

The reviewed event IDs and dispositions were incorporated into the existing seen ledger, preserving earlier entries. None of the four fresh automated results qualified as another implementation. The ten catalog additions in this refresh came from rechecking older exclusions and the existing tracked-project intake.

A separate bounded public GitLab query returned 39 matches, with FMDtr the relevant recent project; its source was already rechecked above. Codeberg's public search timed out, so that coverage remains incomplete. Web search and the existing native intake supplied cross-checks, not proof that every public forge or relay was searched.

## Verification boundaries

Activity means a default-branch commit within 90 days, including metadata-only commits; it is not a maintenance guarantee. No application was installed and no live cross-client, device, wallet-safety or security qualification was performed. Search indexes, relay retention, pagination caps and unavailable source endpoints limit discovery. Existing aliases, exclusions and uncertain results remain retained.
