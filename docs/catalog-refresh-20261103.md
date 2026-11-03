# Catalog refresh, 3 November 2026

This audit checks public source and default-branch metadata. It does not test installed applications, wallet safety or live cross-client interoperability.

## Scope

All 77 previously listed repositories were rechecked: 71 through authenticated GitHub repository and default-branch commit reads, FMDtr through GitLab, Mantra through its Forgejo API, and four repositories through their canonical Git servers. Twenty-eight default-branch heads changed. Existing immutable classification evidence was retained for unchanged heads; changed projects had their README and referenced implementation/manifests re-read. Two verified additions bring the snapshot to 79 repositories.

Activity remains a 90-day default-branch commit measure. It is separate from maturity, archive status and protocol generation. Counts in earlier reports are historical.

## Changes supported by source

### Whistle

Both platform sources now use MarmotKit 0.11.0. The README identifies the v2.0.0 migration as pre-release, and both vendoring scripts pin that version. GitHub releases still list v1.11.2 as the newest public release. Existing v1 groups do not carry over; account identity does.

Sources: [README.md](https://github.com/sjmcnamara/whistle/blob/a5ca6098edff1b958106d315c9049859f30b773b/README.md), [scripts/vendor_marmotkit.py](https://github.com/sjmcnamara/whistle/blob/a5ca6098edff1b958106d315c9049859f30b773b/scripts/vendor_marmotkit.py), [scripts/vendor_marmotkit_android.py](https://github.com/sjmcnamara/whistle/blob/a5ca6098edff1b958106d315c9049859f30b773b/scripts/vendor_marmotkit_android.py), [CHANGELOG.md](https://github.com/sjmcnamara/whistle/blob/a5ca6098edff1b958106d315c9049859f30b773b/CHANGELOG.md).

### Sessions Wallet

New v2 app entry. The desktop bridge and Android build helper pin post-MIP MDK 20ded88 (0.15.0-dev). The app registers the Tauri plugin; its group coordinator creates groups, invites members and sends wallet messages. The project calls itself an unaudited early mainnet alpha. Bridge availability is build-dependent.

Sources: [native/marmot-bridge/Cargo.toml](https://github.com/btcsessions/Sessions-Wallet/blob/641a061e59db6f79dabaeebcc0b99dd25683c900/native/marmot-bridge/Cargo.toml), [scripts/build-marmotkit.sh](https://github.com/btcsessions/Sessions-Wallet/blob/641a061e59db6f79dabaeebcc0b99dd25683c900/scripts/build-marmotkit.sh), [apps/wallet/src-tauri/src/lib.rs](https://github.com/btcsessions/Sessions-Wallet/blob/641a061e59db6f79dabaeebcc0b99dd25683c900/apps/wallet/src-tauri/src/lib.rs), [apps/wallet/src-tauri/src/group.rs](https://github.com/btcsessions/Sessions-Wallet/blob/641a061e59db6f79dabaeebcc0b99dd25683c900/apps/wallet/src-tauri/src/group.rs).

### Styx interoperability probes

New adjacent research entry, not a v2 client recommendation. Its Phase B verdict reports an isolated synthetic direct-MLS lifecycle against exact MDK pins. General Marmot conformance and product activation are explicitly excluded, and the probes were not rerun.

Sources: [README.md](https://github.com/styx-secure/styx/blob/20c1c98b647560c630d58ae308e1a5cbd94fa389/README.md), [docs/architecture/spikes/2026-08-17-marmot-openmls-phase-b-verdict.md](https://github.com/styx-secure/styx/blob/20c1c98b647560c630d58ae308e1a5cbd94fa389/docs/architecture/spikes/2026-08-17-marmot-openmls-phase-b-verdict.md), [styx-js/spikes/marmot-phase-b1/probe.mjs](https://github.com/styx-secure/styx/blob/20c1c98b647560c630d58ae308e1a5cbd94fa389/styx-js/spikes/marmot-phase-b1/probe.mjs).

### Other corrections

- Labradorite and agentd now use marmot-kmp 2.2.1 with Quartz 2.7.3 through the independent Kotlin engine; the former Rust MDK dependency has been removed. Kind-9 prompts/replies remain readable in White Noise. The [Android manifest](https://gitworkshop.dev/npub1w4uswmv6lu9yel005l3qgheysmr7tk9uvwluddznju3nuxalevvs2d0jr5/relay.ngit.dev/nostr-agents/tree/de9f65981a482c97c3cb4f43f6d94f997c2b3673/android/gradle/libs.versions.toml) and [host manifest](https://gitworkshop.dev/npub1w4uswmv6lu9yel005l3qgheysmr7tk9uvwluddznju3nuxalevvs2d0jr5/relay.ngit.dev/nostr-agents/tree/de9f65981a482c97c3cb4f43f6d94f997c2b3673/kotlin/agentd/build.gradle.kts) establish the new engine.
- Marmish now distinguishes its unreleased native Rust v0.2 development from legacy Python v0.1 releases; the catalog description preserves that distinction.
- Haven now pins MDK 0.10.4. The web-chat example uses marmot-ts 0.9.0; Nostrautica vendors 0.9.0 beside its Android MarmotKit runtime. Amethyst now pins Quartz 2.13.0 and marmot-kmp 2.2.1. These update source evidence without claiming every v2 profile interoperates.
- Coinos now documents browser/PWA and Android availability. ShyChat adds signed nsite distribution; its source remains an early client with localStorage key custody.
- The existing archived and inactive sections retain their evidence-backed classifications; the refreshed snapshot still distinguishes deprecation from low activity.

## Discovery and exclusions

Repository searches covered Marmot/Nostr, White Noise, MDK dependencies and marmot-ts, with focused code searches for engine manifests and agent-control consumers. General web searches included GitLab, Codeberg and GitWorkshop. GitHub search pages were bounded at 100 results; two broad queries reached that bound. Code search is default-branch-only, and the broad wn-agent query also exceeded one page. These searches do not establish exhaustive coverage of private projects, unindexed code or other forges. No new full NIP-34 relay census was run.

The Sessions Wallet native bridge surfaced through a manifest code search despite its README lacking a Marmot headline. Styx carries implemented, source-linked interoperability probes, which justify the adjacent research classification.

Rechecked leads were excluded for specific reasons:

- Airhop compares itself with White Noise; that comparison does not establish a Marmot implementation.
- Uniun uses its own OpenMLS/NIP-29 group transport. A Marmot label without verified v2 components is insufficient to classify it as an interoperable Marmot client.
- Acceso Nostr still pins marmot-ts 0.5.1; marmot_dart and NostrNet retain MIP-era implementations. They are not new v2 adopters.
- nosbot configures the already-listed wn-pi transport, so another wrapper entry would duplicate that integration.
- HeterodyneProtocol is a protocol proposal; it is distinct from the implemented admind integration already listed.
- llmref indexes documentation; a dependency snippet is not an implementation. hyperpipe is an older dependency consumer; current v2 adoption was not established.
- Generic Nostr projects, older prototypes, lists, forks, audit mirrors and abandoned demonstrations were kept out of the new current-project additions.

Codeberg web search was restricted by the search provider. Its missing search coverage is not proof that no projects exist there. Existing non-GitHub repositories were checked directly, not through cached search snippets.

## Refreshed inventory

The [audit snapshot](../data/catalog-audit.json) contains per-entry source, generation and feature evidence. This table records the reviewed default-branch identity and classification; it is not a release or compatibility matrix.

| Repository | Latest source commit date | Generation | Activity |
| --- | --- | --- | --- |
| [CentauriAgent/burrow](https://github.com/CentauriAgent/burrow/tree/ac883fa62106b61ed7731b0b4fb8c0cbf5589e52) | 2026-03-07 | v1 | inactive |
| [DavidGershony/Scramble](https://github.com/DavidGershony/Scramble/tree/25473e7396e25e1bda83a7824c785c9a660f03de) | 2026-10-01 | v2 | active |
| [DavidGershony/marmot-cs](https://github.com/DavidGershony/marmot-cs/tree/84b106feb239acfe2fdc811ef2f5ec8bce715e0d) | 2026-06-04 | v1 | inactive |
| [DestBro/mafrend-zapstore](https://github.com/DestBro/mafrend-zapstore/tree/0d99cf5e2d6737ffd8aeb6f63f39e8c194b1f8ef) | 2026-09-26 | unknown | active |
| [Tubestr/tubestr-v2](https://github.com/Tubestr/tubestr-v2/tree/8d53c162af4fde0c6735581a1e0d137ef003101e) | 2026-05-24 | v1 | inactive |
| [dcadenas/marmota](https://github.com/dcadenas/marmota/tree/37906ae7e165debe9fa49ccecfbb0317fa58e0ef) | 2026-03-09 | v1 | inactive |
| [hedwig-corp/bitchat-to-sonar](https://github.com/hedwig-corp/bitchat-to-sonar/tree/fdf091cbb645a1d1010bca207f7ad0c6b572cdd6) | 2026-11-01 | v1 | active |
| [justinmoon/pika](https://github.com/justinmoon/pika/tree/dd226e25633b04501b30652d682a2de49116c592) | 2026-04-01 | v1 | inactive |
| [kai-familiar/marmot-cli](https://github.com/kai-familiar/marmot-cli/tree/111e0705158eb583b904c676572d20bb4c473f64) | 2026-02-16 | v1 | inactive |
| [marmot-protocol/botburrow](https://github.com/marmot-protocol/botburrow/tree/e608ba5ff7c69e461867acfc08c6ac2ff3f5c926) | 2026-04-14 | v1 | inactive |
| [marmot-protocol/dr.marmot](https://github.com/marmot-protocol/dr.marmot/tree/4cb7ac2f05a0f9348fe20319f73e836ef5e25b1d) | 2026-03-04 | adjacent | archived |
| [marmot-protocol/facet](https://github.com/marmot-protocol/facet/tree/dbe992a01564cacb9686c306559d95e9cf402049) | 2026-07-24 | adjacent | inactive |
| [marmot-protocol/goggles](https://github.com/marmot-protocol/goggles/tree/767a98ffd64549800ae6b1ced361624f721f8992) | 2026-09-25 | adjacent | active |
| [marmot-protocol/marmot](https://github.com/marmot-protocol/marmot/tree/97efcaf8d7072edd010ee1663821a352952d77a7) | 2026-11-03 | v2 | active |
| [marmot-protocol/marmot-ts](https://github.com/marmot-protocol/marmot-ts/tree/a17913b93fb3c80f2084e8a1538e936bdb1c59df) | 2026-10-27 | v2 | active |
| [marmot-protocol/marmots-web-chat](https://github.com/marmot-protocol/marmots-web-chat/tree/8d7d18f7e485899968ccd36c209bb34a499aa325) | 2026-10-27 | v2 | active |
| [marmot-protocol/mdk](https://github.com/marmot-protocol/mdk/tree/51657365b7662395a7d4d6ed55980251544f41c0) | 2026-11-03 | v2 | active |
| [marmot-protocol/mdk-kotlin](https://github.com/marmot-protocol/mdk-kotlin/tree/5dd757dc83f2c68c37b99963a1347610cd3fada5) | 2026-08-05 | v1 | archived |
| [marmot-protocol/mdk-kotlin-example](https://github.com/marmot-protocol/mdk-kotlin-example/tree/94f432ef2b0d3319fd431477d56b7ecea40ef01e) | 2025-12-01 | v1 | archived |
| [marmot-protocol/mdk-python](https://github.com/marmot-protocol/mdk-python/tree/98f51545257979590d52cdfa2a6deb7916b8f54f) | 2026-08-05 | v1 | archived |
| [marmot-protocol/mdk-python-example](https://github.com/marmot-protocol/mdk-python-example/tree/80e86ae89171995fb98b0f0d905074b8b4180bc4) | 2025-12-01 | v1 | archived |
| [marmot-protocol/mdk-ruby](https://github.com/marmot-protocol/mdk-ruby/tree/96c5cf866019fa9efde2932e8554497492f01893) | 2026-08-05 | v1 | archived |
| [marmot-protocol/mdk-swift](https://github.com/marmot-protocol/mdk-swift/tree/d552830c55c5037f57db9759b47d73db0e152cdc) | 2026-08-05 | v1 | archived |
| [marmot-protocol/mls-ts](https://github.com/marmot-protocol/mls-ts/tree/294655433a17cfab9ea087967aa9f30378859c1d) | 2025-06-12 | adjacent | archived |
| [marmot-protocol/nostr-openmls](https://github.com/marmot-protocol/nostr-openmls/tree/b5c2c004c1bb8d13a5352c4d62f458e8c1a0946b) | 2025-05-30 | v1 | archived |
| [marmot-protocol/openmls-lmdb-storage](https://github.com/marmot-protocol/openmls-lmdb-storage/tree/b8070259705cdc48413a7ac6a24a3f8b316b82d8) | 2025-01-12 | adjacent | inactive |
| [marmot-protocol/openmls-redb-storage](https://github.com/marmot-protocol/openmls-redb-storage/tree/cd9b271be354c3020895a1d121e1946275830abe) | 2025-01-21 | adjacent | inactive |
| [marmot-protocol/openmls-sled-storage](https://github.com/marmot-protocol/openmls-sled-storage/tree/2228025fea9310dea99e3a9d8beeb479eb23399d) | 2025-05-30 | adjacent | inactive |
| [marmot-protocol/transponder](https://github.com/marmot-protocol/transponder/tree/7be9649a9913c8f554ac52f9e6a3dc73ba5b643c) | 2026-10-13 | v2 | active |
| [marmot-protocol/whitenoise](https://github.com/marmot-protocol/whitenoise/tree/07aa5a0a7d28dd0185c6e72e56834520ef27b66c) | 2026-09-18 | v1 | archived |
| [marmot-protocol/whitenoise-android](https://github.com/marmot-protocol/whitenoise-android/tree/efefaae7e0a663e7d98001159b366f4ed4c30d40) | 2026-11-03 | v2 | active |
| [marmot-protocol/whitenoise-ios](https://github.com/marmot-protocol/whitenoise-ios/tree/6607b9664f41c972834569c063e22669395bdb7a) | 2026-11-02 | v2 | active |
| [marmot-protocol/whitenoise-linux](https://github.com/marmot-protocol/whitenoise-linux/tree/b537340b48ac8e34b1845e7de18cf18c527f0aa1) | 2026-11-02 | v2 | active |
| [marmot-protocol/whitenoise-mac](https://github.com/marmot-protocol/whitenoise-mac/tree/e1f58dfa4eeefc0743291d984d29035a889315d0) | 2026-11-02 | v2 | active |
| [marmot-protocol/whitenoise-rs](https://github.com/marmot-protocol/whitenoise-rs/tree/95fa0b85c4b3bbee1a6fad3971849da1925df0d4) | 2026-08-05 | v1 | archived |
| [marmot-protocol/wn-tui](https://github.com/marmot-protocol/wn-tui/tree/5191bc92f5da0532ebc469e908f6b33ae760b6c9) | 2026-07-29 | v1 | archived |
| [mehmetefeumit/Haven-App](https://github.com/mehmetefeumit/Haven-App/tree/dc13935325c5306266df30f3ede2355a2809be3a) | 2026-11-03 | v2 | active |
| [nmadd57/marmot-server](https://github.com/nmadd57/marmot-server/tree/6878d89b564df3511de16650f80bdfc663344a04) | 2026-04-05 | v1 | inactive |
| [notmandatory/hermes-marmot](https://github.com/notmandatory/hermes-marmot/tree/c993e4732b600a0361624e9790a81c7e582f365b) | 2026-05-27 | v1 | inactive |
| [nvk/agentnoise](https://github.com/nvk/agentnoise/tree/41c9b3372c6fd366216e2894a2427db2190d41ab) | 2026-06-27 | adjacent | inactive |
| [rphilbrdigits/dockerized-marmot-cli](https://github.com/rphilbrdigits/dockerized-marmot-cli/tree/266d37013c40e66d0e90f6edd288a58e75b402f6) | 2026-03-02 | v1 | inactive |
| [sjmcnamara/whistle](https://github.com/sjmcnamara/whistle/tree/a5ca6098edff1b958106d315c9049859f30b773b) | 2026-10-29 | v2 | active |
| [tkhumush/openclaw-marmot](https://github.com/tkhumush/openclaw-marmot/tree/a8322b1ecbe2a6eed60b58cf096aba99e22561ea) | 2026-05-16 | v1 | inactive |
| [vitorpamplona/amethyst](https://github.com/vitorpamplona/amethyst/tree/b950f0d76234f6e28af3e2deaf283f8833790cc3) | 2026-11-03 | v2 | active |
| [vitorpamplona/quartz](https://github.com/vitorpamplona/quartz/tree/5ae28cbea1f972c72b0849c4597aca459257f543) | 2026-11-01 | adjacent | active |
| [https://gitlab.com/Kalle/fmdtr-android](https://gitlab.com/Kalle/fmdtr-android/-/blob/c177a13eaa6f5ac2e753be210bc5fe86c3293498/rust/fmd-marmot-bridge/Cargo.toml) | 2026-09-25 | v2 | active |
| [https://gitworkshop.dev/cyberguy.fyi/relay.ngit.dev/mdk-odin](https://gitworkshop.dev/cyberguy.fyi/relay.ngit.dev/mdk-odin/tree/f7ce90b98c81fa54f7398dd0f2fc9c267da36cd9) | 2026-10-21 | v2 | active |
| [LightningPiggy/lightning-piggy-mobile](https://github.com/LightningPiggy/lightning-piggy-mobile/tree/3f020caea15ad4322da57bbbe43148c9239ae8aa) | 2026-10-22 | v2 | active |
| [chebizarro/nostrc](https://github.com/chebizarro/nostrc/tree/71c0e3fcdabfd1d2c78c29111803ba9343d1de6b) | 2026-10-29 | v2 | active |
| [ShyChat](https://gitworkshop.dev/npub1mm5l2mfxvg2y7fl7sulfrznhxjqdqxkq72njafp567j6gej8elcsg6qlen/git.shychat.lol/shychat/tree/f4a91214fd1e087016fdcd99b8937b36d216046e) | 2026-10-27 | v2 | active |
| [modus-lisp/cl-marmot](https://github.com/modus-lisp/cl-marmot/tree/be2152dc935a0350e271a340531810ca40b39dd1) | 2026-10-23 | v2 | active |
| [modus-lisp/emissary](https://github.com/modus-lisp/emissary/tree/2a1be7555b07a168836e3979a68a16251717aa9c) | 2026-10-23 | v2 | active |
| [kngako/quartz-marmot-kmp](https://github.com/kngako/quartz-marmot-kmp/tree/c3783a26b96c7fedbf47a504a8ecf817ffd0d6b9) | 2026-09-08 | v2 | active |
| [jooray/nostrautica](https://github.com/jooray/nostrautica/tree/5af109f702b8da6c07b546ed21fa41edbb2ac93d) | 2026-10-31 | v2 | active |
| [shroominic/nostrbase](https://github.com/shroominic/nostrbase/tree/c3cd7609edc455d293f877c581041b0a20edef4f) | 2026-10-06 | v2 | active |
| [cameri/nostream](https://github.com/cameri/nostream/tree/bc6d2bbbc4218a389a5be9d35c266b48bff0efef) | 2026-11-02 | adjacent | active |
| [tidley/codr](https://github.com/tidley/codr/tree/f8fe9da5b739042c335708ec65775581ee836b8d) | 2026-10-31 | v2 | active |
| [tsgx1990/moyu](https://github.com/tsgx1990/moyu/tree/88a20d247510d1cc46ca955564aa395d26ae8e89) | 2026-09-30 | v2 | active |
| [januszgrze/chascuro](https://github.com/januszgrze/chascuro/tree/e892802d7dc9ad40a588288ef1161426c5bb6bc6) | 2026-08-31 | v2 | active |
| [https://git.coinos.io/coinosv3.git](https://git.coinos.io/coinosv3.git/tree/?id=c566edbe50a8921311127efac65836bd6ff9c6d3) | 2026-11-02 | v2 | active |
| [Noormohammadiazad/Textor](https://github.com/Noormohammadiazad/Textor/tree/2b9e6fdd3a453a7f3dba8b2ca6de19a2d56f9baa) | 2026-11-03 | v2 | active |
| [humanitylabs-org/wizard-messenger](https://github.com/humanitylabs-org/wizard-messenger/tree/65c7666604155ad4b7a59b9a48fd48f8dae1b551) | 2026-11-03 | v2 | active |
| [3DAGI/freedom-app](https://github.com/3DAGI/freedom-app/tree/ba0b705e955e45a690051f75bcfabe8987fee856) | 2026-11-03 | v2 | active |
| [Epiphytic/deaddrop](https://github.com/Epiphytic/deaddrop/tree/b38b2841b081952dc7728da391fe0e26fc7c6181) | 2026-09-03 | v2 | active |
| [marmot-protocol/frigate-marmot](https://github.com/marmot-protocol/frigate-marmot/tree/67ff0d58994e8859debb7493454b883ff1b0775a) | 2026-10-13 | v2 | active |
| [Epiphytic/marmish](https://github.com/Epiphytic/marmish/tree/540e39cf08aec38bec75d1cbdd36f162d0219f82) | 2026-11-03 | v2 | active |
| [Epiphytic/heterodyne-metaharness](https://github.com/Epiphytic/heterodyne-metaharness/tree/dcb6df07ae2125f4a3c449eb909639a0c80430fb) | 2026-11-01 | v2 | active |
| [hzrd149/marmots-tunnels](https://github.com/hzrd149/marmots-tunnels/tree/5a77ad022505a262ed8265f60e60d86278319693) | 2026-09-12 | adjacent | active |
| [marmot-protocol/nostr-doctor](https://github.com/marmot-protocol/nostr-doctor/tree/b43fd966ef256fd277118a59dfc064be468677a8) | 2026-09-06 | adjacent | active |
| [FelineStateMachine/bindws](https://github.com/FelineStateMachine/bindws/tree/5d3126716ae5b6bf01d46cdf14fceb05244445e0) | 2026-09-05 | adjacent | active |
| [vitorpamplona/marmot-kmp](https://github.com/vitorpamplona/marmot-kmp/tree/e47856e255a705dd62e1f3e2cb341fcd87fca8a1) | 2026-10-31 | v2 | active |
| [vitorpamplona/mls-kmp](https://github.com/vitorpamplona/mls-kmp/tree/970276298605da953c14489b8feea5b1ab2e2603) | 2026-10-31 | adjacent | active |
| [https://code.sigidli.com/mantra/mantra-kmp](https://code.sigidli.com/mantra/mantra-kmp/src/commit/99f48d176974cf064a292fa6dae7ae18712dda4c) | 2026-10-03 | v1 | active |
| [jooray/wn-notify](https://github.com/jooray/wn-notify/tree/ba21270edace90c0d6dde7fde7c3b1e3fb5c6201) | 2026-10-25 | v2 | active |
| [davidjj999/relayrider](https://github.com/davidjj999/relayrider/tree/5651cf0a76b3e15dc3cdba9bbb3f84aa05f833af) | 2026-07-11 | adjacent | inactive |
| [Labradorite / agentd](https://gitworkshop.dev/npub1w4uswmv6lu9yel005l3qgheysmr7tk9uvwluddznju3nuxalevvs2d0jr5/relay.ngit.dev/nostr-agents/tree/de9f65981a482c97c3cb4f43f6d94f997c2b3673) | 2026-11-03 | v2 | active |
| [jooray/third-ear](https://github.com/jooray/third-ear/tree/e4f7e4358ea63a60dd13bb8e69428f9f6514ff37) | 2026-11-03 | v2 | active |
| [btcsessions/Sessions-Wallet](https://github.com/btcsessions/Sessions-Wallet/tree/641a061e59db6f79dabaeebcc0b99dd25683c900) | 2026-10-30 | v2 | active |
| [styx-secure/styx](https://github.com/styx-secure/styx/tree/20c1c98b647560c630d58ae308e1a5cbd94fa389) | 2026-11-02 | adjacent | active |
