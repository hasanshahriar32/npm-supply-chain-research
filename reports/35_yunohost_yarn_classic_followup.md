# Yarn Classic follow-up

The additional lockfile coverage resolves 17 more primary pairs as shared hits. The count rises from 112 to 129 of 215, and 86 pairs remain unresolved. The five confirmed differences still support a positive lower bound on turnover. The upper bound drops from 50.2% to 42.3%. Net coverage can still move in either direction, with bounds from −40.0 to +38.6 percentage points.

| Comparison | Initial resolved | Follow-up resolved | Follow-up turnover | Follow-up net change (pp) |
| --- | ---: | ---: | ---: | ---: |
| Primary | 112 | 129 | 2.3–42.3% | −40.0 to +38.6 |
| Alternative 1 | 110 | 127 | 2.3–43.3% | −41.9 to +37.7 |
| Alternative 2 | 112 | 129 | 1.9–41.9% | −39.5 to +39.1 |

The result uses the same finite frame and all three frozen contrasts. The identical-portfolio control retains zero turnover and zero net change. Only rows for the 35 Yarn candidates can change. The registry measurements for Yarn were collected separately after the initial analysis, so the combined results measure sensitivity to the added evidence.

## Coverage and checks

- Fourteen of the 35 candidates use newer Yarn formats. One Classic project has workspaces. The two readers agree on the other 20 Classic lockfiles. Seven have readable graphs without a reported path exclusion and 13 are partial. [Yarn Classic lockfile documentation](https://classic.yarnpkg.com/en/docs/yarn-lock).
- The frozen queue contains 3,557 exact versions, of which 3,555 have usable maintainer lists. Nineteen applications yield verified registry-linked paths, with 4,831 distinct package/version observations summed over projects. Two applications have a documented hit on one side and an unresolved opposing status.
- The reader checks locked versions against the declared ranges and excludes edges affected by selective resolutions. The registry join requires canonical package identity and exact SHA-512 agreement for Yarn mirror artifacts. Before continuing through a transitive edge, the analyzer checks its declaration against the parent package's exact-version registry record. Yarn contributes positive evidence only.
- The scoring replay reproduces every earlier paired result before applying the additional evidence. For every project and comparison, the new feasible set is a subset of the old set. Original npm and pnpm rows remain identical.

The [frozen follow-up](../research/consumer_holdout/runs/yunohost-yarn-classic/protocol.json) and [paired results](../research/consumer_holdout/runs/yunohost-yarn-classic/results.json) record the evidence and calculations. The VPS collector exited and its working directory was removed.
