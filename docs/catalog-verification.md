# Catalog verification — 2026-10-01

This is a dated public-source audit, not a live health monitor or an interoperability test.

## Scope and method

All previously listed projects remain discoverable. The audit checked **45 distinct GitHub repositories**, the GitLab FMDtr repository, and the Codeberg NostrBotKit endpoint. MDK's CLI and Claude Code integration, and Quartz inside Amethyst, are additional entries in existing repositories.

For each available GitHub repository, authenticated primary API reads supplied its canonical URL, archive flag, default branch, exact head commit, and committer timestamp. README files, dependency manifests, migration notes, or implementation files were then inspected at that commit to classify protocol generation. The [snapshot](../data/catalog-audit.json) retains all 47 repository records and pinned public source links. GitLab supplied FMDtr's default branch and latest commit; its bridge manifest was read at that commit. Codeberg's canonical page and repository API both returned 404.

The activity window is **90 days**, measured backwards from the snapshot timestamp. There are **17 recently updated repositories**, **19 without recent public commits**, **10 archived or explicitly deprecated**, and **1 unavailable**. Counts are repositories, not individual catalog entries. MDK and Amethyst contain several entries.

No audit logs, credentials, private implementation details, or installation data were used or published. Broad discovery used a local mirror first; final classifications used direct forge reads. The snapshot fixes the evidence in time so CI is repeatable without a network connection.

## Important corrections and evidence

- **MDK terminal tools:** [CLI README](https://github.com/marmot-protocol/mdk/blob/a21a7b1d27afb863b3fd590058c66e6a22649391/crates/cli/README.md) documents `wn` commands/TUI and `wnd`, the background daemon. [Old terminal client README](https://github.com/marmot-protocol/wn-tui/blob/5191bc92f5da0532ebc469e908f6b33ae760b6c9/README.md) explicitly deprecates that standalone project, even though its GitHub archive flag is false.
- **First-party connectors:** the [MDK integration directory](https://github.com/marmot-protocol/mdk/tree/a21a7b1d27afb863b3fd590058c66e6a22649391/integrations) contains Hermes, OpenClaw, Codex, Claude Code, OpenCode, and Pi. These share MDK's runtime; activity is measured at repository level.
- **Amethyst and amy are no longer classified as v1:** [component definitions](https://github.com/vitorpamplona/amethyst/blob/3613bf05927c3523d9d0cee77cd71d2aa835dca4/quartz/src/commonMain/kotlin/com/vitorpamplona/quartz/marmot/appComponents/AppComponentIds.kt) replace the earlier monolithic group-data extension and define v2 identity-proof/media components. The active library is [inside Amethyst](https://github.com/vitorpamplona/amethyst/tree/3613bf05927c3523d9d0cee77cd71d2aa835dca4/quartz), not the old standalone repository.
- **Scramble differs from standalone marmot-cs:** [current profile](https://github.com/DavidGershony/Scramble/blob/7f1f4aaf395724f8e310af19e86e8d85ff294ceb/src/Scramble.Marmot.AppComponents/CurrentProfile.cs) specifies the new component dictionary and identity-proof component. Standalone [marmot-cs documentation](https://github.com/DavidGershony/marmot-cs/blob/84b106feb239acfe2fdc811ef2f5ec8bce715e0d/README.md) is still MIP-era and its last default-branch commit is June 4.
- **Sonar is active but v1:** [core dependency pins](https://github.com/hedwig-corp/bitchat-to-sonar/blob/7bcc1b48e50e94283d0d380fc0e69b1dbb2be146/core/Cargo.toml) point to MDK revision `e8cd584` from the 0.8-era stack and the superseded White Noise Rust core. Source activity does not establish migration.
- **Pika is not a current v2 recommendation:** [dependency manifest](https://github.com/justinmoon/pika/blob/dd226e25633b04501b30652d682a2de49116c592/Cargo.toml) pins MDK revision `ca0663ee` from the 0.7-era stack. Its [README](https://github.com/justinmoon/pika/blob/dd226e25633b04501b30652d682a2de49116c592/README.md) warns against private/secure production use. Last default-branch commit: April 1.
- **Haven remains transitional:** [core manifest](https://github.com/mehmetefeumit/Haven-App/blob/a7a8ab2036b39a6dd7d83375e9a80bdad4281823/haven-core/Cargo.toml) and [protocol migration notes](https://github.com/mehmetefeumit/Haven-App/blob/a7a8ab2036b39a6dd7d83375e9a80bdad4281823/MARMOT_PROTOCOL_KNOWLEDGE.md) distinguish its early v2 dependency from later pending wire-profile migration. Calling it current-profile compatible would overstate the evidence.
- **The web example is an early v2 pin:** its [TypeScript submodule](https://github.com/marmot-protocol/marmot-ts/tree/714fe294504a516def392d10f2e3e18ed41977eb) documents the earlier identity-proof profile, unlike [current marmot-ts](https://github.com/marmot-protocol/marmot-ts/blob/591eb25f6ba0b69cb6dc7b711fb75836da7ddbaa/README.md). A recently updated wrapper does not update the pinned engine automatically.
- **Linux implementation corrected:** [Linux README](https://github.com/marmot-protocol/whitenoise-linux/blob/7fc366b8708bcf2193dcb786b03bf1d206cdc2bc/README.md) and [dependency pin](https://github.com/marmot-protocol/whitenoise-linux/blob/7fc366b8708bcf2193dcb786b03bf1d206cdc2bc/DEPS_PIN) describe Odin/Clay and its MDK-based native interface; the former Rust/Slint description was stale.
- **FMDtr remains on an older bridge:** its [pinned manifest](https://gitlab.com/Kalle/fmdtr-android/-/blob/4ac62356c4237a6beb77f41a9997d9686003c3e0/rust/fmd-marmot-bridge/Cargo.toml) uses MDK 0.8.0. Last default-branch commit: June 19.
- **Botburrow and AgentNoise are not recently updated:** their [Botburrow](https://github.com/marmot-protocol/botburrow/blob/e608ba5ff7c69e461867acfc08c6ac2ff3f5c926/README.md) and [AgentNoise](https://github.com/nvk/agentnoise/blob/41c9b3372c6fd366216e2894a2427db2190d41ab/README.md) setup instructions still reference the old White Noise Rust daemon. Their last default-branch commits were April 14 and June 27 respectively.
- **Unknown is intentional:** the incomplete Tubestr scaffold, Whistle's unresolved generation, the public-only Mafrend store metadata, the standalone Quartz repository, and unverified dependency resolution in community wrappers are not assigned a protocol generation from names or marketing claims. Supporting tools and audit-format versions are not wire-protocol generations.
- **NostrBotKit is unverified, not abandoned:** the [canonical source](https://codeberg.org/mateos/NostrBotKit) and [repository endpoint](https://codeberg.org/api/v1/repos/mateos/NostrBotKit) could not be verified. A 404 can reflect several conditions; the historical listing is retained without invented commit dates.

## Limits

A recent commit can be a documentation update. An inactive repository may still be supported privately. Archive status overrides the 90-day window; explicit deprecation requires pinned maintainer evidence. Monorepo activity does not prove activity in each subdirectory, and a store metadata repository does not expose private development.

Protocol classifications refer to inspected source—not an APK, a store release, every supported mode, complete specification conformance, or tested cross-client group compatibility. Early v2 implementations may be incompatible with the current component profile. App/package version numbers do not establish Marmot v1/v2.

## Refresh procedure

1. Read canonical metadata and the latest **default-branch commit**, not `pushed_at`.
2. Inspect primary generation evidence at that same revision. Use **unknown** if it cannot be established; use **unverified** for an unavailable source.
3. Update all affected snapshot records, the README check date, entry labels/dates, and this dated note together. Recompute activity for the entire inventory against the new check timestamp.
4. Preserve older entries in the appropriate section; do not silently drop them.
5. Run `python3 scripts/check_catalog.py` and `python3 -m unittest discover -s tests -v`. CI verifies coverage, labels, section placement, the activity window, immutable source references, local README links, and discovery regressions.

The [weekly discovery workflow](discovery.md) creates reviewed leads. It does not continually refresh this snapshot or automatically certify existing entries.
