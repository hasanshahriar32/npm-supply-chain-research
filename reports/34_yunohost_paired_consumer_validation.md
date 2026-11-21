# YunoHost paired consumer validation

The primary comparison resolves different coverage outcomes for five of 215 applications under the supported root dependency and registry scope. Three have evidence only for the name portfolio and two only for the version portfolio. There are also 70 common positives and 37 common negatives. One other application has a documented name hit, with the version status unresolved. The confirmed differences establish at least 2.3% turnover in this frame. The compatible upper bound is 50.2%. The net change can range from −48.4 to +47.0 percentage points given the unresolved evidence.

| Paired results | Primary | Alternative 1 | Alternative 2 |
| --- | ---: | ---: | ---: |
| Documented under both | 70 | 67 | 71 |
| Documented name only | 4 | 7 | 3 |
| Documented version only | 2 | 1 | 2 |
| Documented under neither | 139 | 140 | 139 |
| Fully resolved pairs | 112 | 110 | 112 |
| Fully resolved differences | 5 | 5 | 4 |
| Turnover bounds | 2.3–50.2% | 2.3–51.2% | 1.9–49.8% |

A documented zero means the procedure has no confirmed witness for that portfolio. Three applications have fully resolved differences under every cutoff tie. The identical-portfolio control has zero gross and net change under all feasible assignments.

## Evidence acquisition and validation

The comparison preserves the frozen five-account portfolios and their two version cutoff ties. The pinned YunoHost frame excludes earlier repository keys and duplicate commits. Its root manifest requirement and the extractors' broader scope distinguish it from the first holdout, which resolves 29 of 155 pairs. The two sets of bounds describe separate catalog frames.

- All 15 requested, commit-pinned workspace manifests were retained and verified against their receipts.
- The exact-version queue contained 9,987 package/version pairs. Usable maintainer lists were observed for 9,968 requests. Nineteen responses lacked a usable maintainer list.
- Of 19,375 corroborated path witnesses, 13,250 joined through canonical npm registry tarball URLs and 5,744 through exact SHA-512 equality. Another 162 lacked a usable version observation and 219 lacked a corroborating artifact identity.
- Ninety projects have a registry-linked path. Complete root-scope path and registry checks exist for 72 projects. Shared positive witnesses also resolve some incomplete projects.
- Of the 103 unresolved primary pairs, 35 have a Yarn file and 23 are pnpm candidates. Sixteen lack a conventional root lockfile. The remaining 29 have other manager, path, or registry limitations.

The matched-input diagnostic uses the same 108 npm candidates with the earlier and expanded extractors. The earlier reader corroborates locations for 50 projects, the expanded reader for 67. The implementations share 8,158 locations. The expanded reader adds 5,463 locations across 19 projects, including three with workspaces, and leaves 316 previously corroborated locations unresolved across two projects. These are differences in extractor coverage and do not measure ground-truth path accuracy.

A post hoc check confirmed that at least one positive witness location for all five primary differences also appears in the earlier reader's corroborated output. The corresponding counts are five of five and four of four for the alternative ties. The expanded path and registry checks determine whether the opposing status is resolved.

The measurement covers committed mandatory production paths, using verified root-reachable npm workspaces and a three-edge pnpm scope. It records registry maintainer associations as observed on the collection date. The paths document reach under those evidence rules. Historical publishing authority, installed execution and intervention effects require separate observations.

## Replay and checks

The protocol, project-level results and matched-input diagnostic provide the design and aggregation records. Account and manifest receipts for exact replay remain in the ignored local evidence directory. [Protocol](../research/consumer_holdout/runs/yunohost-v2/protocol.json), [paired results](../research/consumer_holdout/runs/yunohost-v2/results.json), [extractor comparison](../research/consumer_holdout/runs/yunohost-v2/npm_extractor_comparison.json), [replay instructions](../research/consumer_holdout/README.md).

The offline verifier checked acquisition order, 10,002 receipt identities, the 215-project denominator, all four contrasts and the reported bounds. The VPS collection completed successfully, and the cleanup check found no collection process or temporary job directory.
