# Broader consumer dependency evidence

These experiments use the 40 previously inspected pilot repositories and synthetic fixtures. The sealed 155-project holdout has its own unchanged extractor and data. The new parser results measure development coverage.

## npm

The development extractor uses Arborist's offline virtual tree to interpret effective npm override ranges. For each traversed mandatory edge, it independently checks the nominal declaration against the committed lockfile, recomputes the nearest installation location, and checks the locked version against the effective range. A workspace importer needs a pinned manifest consistent with its locked identity and declarations. The extractor keeps the importer on every witness. An unresolved workspace or dependency edge remains visible in the output.

The importer cross-check recognizes literal workspace paths and single-segment wildcards. It does not assign a deployment importer. Both npm readers rely on package-manager metadata and use the same SemVer implementation. Tests with expected paths verify scoped overrides, workspace identity and stale declarations.

- [npm summary](npm_summary.json)
- [Detailed npm witness and request ledger](npm_projects.json.gz)

## pnpm

The reader supports v9 root-importer paths up to three mandatory edges. It parses exact snapshot references, retains peer suffixes, and corroborates each package/version in the path with the native pnpm lockfile listing. Presence in the boot document or another peer snapshot does not supply evidence for the project importer. Patched, linked and unsupported targets remain unresolved. A depth-limited result supplies positive evidence inside the supported horizon.

An omitted tarball URL cannot directly identify the public registry. The separate integrity check freezes all eligible package/version keys and compares full SHA-512 identifiers against their independently observed public npm `dist.integrity`. This establishes agreement between recorded content identifiers. No tarballs were retrieved and no account coverage was scored.

- [pnpm summary](pnpm_summary.json)
- [pnpm path ledger](pnpm_projects.json)
- [Registry integrity observations](pnpm_integrity_observations.json) and [summary](pnpm_integrity_summary.json)

## Replay

From the repository root:

```sh
python scripts/study_npm_parser_development.py
python scripts/study_pnpm_parser_development.py
python scripts/verify_pnpm_registry_integrity.py report
python -m unittest discover -s scripts/tests
node --test scripts/tests/test_consumer_lock_evidence.cjs scripts/tests/test_consumer_override_reference.cjs scripts/tests/test_consumer_parser_development.cjs
python scripts/verify_consumer_holdout.py research/consumer_holdout/runs/selfhosted-v1
```

The run used Node 24.22.0, npm 11.19.1, Arborist 9.9.1, SemVer 7.8.5, pnpm 12.14.0 and Ruby Psych 5.2.2. On a fresh checkout, replay the pinned root files using the original pilot collector, then use `scripts/study_npm_parser_development.py --fetch-workspaces` to retrieve the workspace manifests at the same commits. Archive the local `private/` directory to retain the original request records. Live registry collection can be repeated only as a new observation.

## Candidate second frame

The [YunoHost catalog preflight](yunohost_frame_preflight.json) records the captured catalog hash, application exclusions and overlap with earlier frames. It establishes candidate upstream GitHub keys. Root manifests and lockfiles answer later screening and evidence questions. [Official catalog documentation](https://doc.yunohost.org/en/dev/packaging/publish/) · [Upstream source field](https://doc.yunohost.org/en/dev/packaging/manifest/)

The second-frame [root manifest screen](yunohost_root_screen.json) ran on medchain using public Git HEAD and pinned raw manifest requests. The bounded [queue](yunohost_root_screen_queue.json) contains all 500 upstream keys remaining after the catalog and earlier frame exclusions. Replay of that screen against moving HEAD values is a new observation. Reconstruct the exact-commit deduplicated frame from the retained results:

```sh
python scripts/screen_yunohost_consumer_frame.py root-frame
```

The [eligible-root frame](yunohost_root_frame.json) records 215 pinned applications after excluding three earlier commit matches and one within-catalog duplicate. Dependency lockfile selection and outcome collection are later study phases.
