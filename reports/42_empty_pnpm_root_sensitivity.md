# Sensitivity to empty pnpm roots

After the Yarn Classic follow-up, 86 of the 215 project classifications remained unresolved in the primary comparison. Twenty-three of these projects had pnpm lockfile evidence. We used the earlier extraction results to identify all 16 unresolved projects with a successful pnpm comparison and zero witnesses. We fixed the candidate list and the rule for evaluating empty roots before inspecting those source files for this follow-up. This is a post hoc sensitivity analysis. [Diagnostic protocol](../research/consumer_holdout/runs/yunohost-empty-pnpm-roots/protocol.json)

The root manifest and the v9 lockfile's root importer both had zero regular dependency declarations for all 16 projects. Thirteen manifests declared development dependencies. Three declared neither regular nor development dependencies. None declared optional dependencies. A regular production path cannot start from an empty regular dependency declaration at the root. The 16 pairs can therefore be treated as common negatives within that scope. The files and their recorded digests identify what was checked. [Source evidence and results](../research/consumer_holdout/runs/yunohost-empty-pnpm-roots/results.json)

| Comparison | Resolved of 215 | Turnover bounds | Net change in percentage points |
| --- | ---: | ---: | ---: |
| After Yarn Classic | 129 | 2.3–42.3% | −40.0 to +38.6 |
| Empty pnpm root sensitivity | 145 | 2.3–34.9% | −32.6 to +31.2 |

All five confirmed differences remain. A net gain for either portfolio remains compatible with the evidence. The same 16 common negatives narrow both alternative cutoff comparisons. The identical-portfolio control retains zero turnover and zero net change.

Among the remaining 70 unresolved primary pairs, 18 had no returned root lockfile or an unavailable declared lockfile, 18 had Yarn evidence, 17 had npm evidence, seven had pnpm evidence, six had Bun evidence and four had observations from multiple manager families. This inventory describes the retained evidence under the frozen rules. It gives the unresolved denominator even when an observed package manager or lockfile leaves a path inconclusive.

The standalone companion rebuilds the sensitivity from the recorded source checks and reproduces the displayed table. Full verification of declaration counts uses the pinned capture. The result is scoped to declared mandatory production dependencies at the root. [Replay commands](../research/consumer_holdout/README.md)
