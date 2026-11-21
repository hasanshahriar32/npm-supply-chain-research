# Checking the remaining npm roots

We examined all 17 projects in the unresolved npm stratum after the Bun sensitivity. This is a post hoc check on the same 215-project frame. It distinguishes empty production declarations from incomplete artifact identity in a nonempty root. [Per-project observations](../research/consumer_holdout/runs/yunohost-npm-unresolved/results.json)

Three projects have corroborated empty production roots. In Y056 and Y106, the npm v3 root declaration records match the pinned manifests. In Y260, the npm v1 lockfile marks all 806 entries, including nested entries, as development-only. The exact locked versions for the development declarations satisfy their manifest ranges. All three pinned manifests lack regular, optional, peer, and bundled dependency declarations. Two other empty manifests have conflicting version labels in their lockfiles and remain unresolved. [npm lockfile reference](https://docs.npmjs.com/files/package-lock.json/)

Y300 and Y451 already had complete path extraction. Their corresponding lockfiles omit both a tarball URL and usable SHA-512 for 3 and 59 locations, respectively. A registry record for the same name and version leaves the locked artifact identity unresolved under the comparison's evidence rule. The check of direct npm v1 dependencies against retained exact-version observations yields no additional positive hits.

| Sensitivity stage | Resolved of 215 | Turnover bounds | Net change in percentage points |
| --- | ---: | ---: | ---: |
| After the Bun direct check | 161 | 2.3–27.4% | −25.1 to +23.7 |
| After checking unresolved npm roots | 164 | 2.3–26.0% | −23.7 to +22.3 |

The five confirmed differences persist, and either portfolio could reach more projects. The combined sensitivity leaves 51 primary pairs unresolved. The replication companion recomputes the combined bounds from the retained observations. Full source inspection uses the pinned capture and Node.js with npm SemVer. [Replication companion](../submission/emse/EMSE_Consumer_Replication.zip)
