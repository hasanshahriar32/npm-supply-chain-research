# Same-commit YunoHost importer comparison

The expanded audit finds one application where selecting the importer named by the recipe changes portfolio coverage at a fixed source commit. The Karakeep root has a single verified dependency with no mandatory children. It yields no hit under either portfolio. The named importers have corroborated paths that yield a hit under both portfolios for all three cutoff choices. This one case depends on a post hoc completeness check. The six other named candidates leave the size of the effect unresolved.

## Recipe sample

The sample excludes all 31 previously audited upstream keys. It includes the 39 remaining keys with an observed workspace marker and a seeded draw of 60 from the other 430 keys. The recipe sample was frozen before opening its pinned packaging files or matching portfolio accounts. Coverage and attrition proportions describe this workspace-enriched sample.

| Evidence in retained recipe files | Workspace markers | Other sampled keys | Total |
| --- | ---: | ---: | ---: |
| Explicit non-root importer used by build or service | 6 | 1 | 7 |
| JavaScript package command, named source path unverified | 15 | 11 | 26 |
| Release asset declared, no matched JavaScript command | 15 | 24 | 39 |
| Neither signal in the checked files | 3 | 24 | 27 |
| Total | 39 | 60 | 99 |

All 594 requests have a receipt. Of these, 394 returned files and 200 returned HTTP 404. The release-asset signal records a declaration. Deployment would require checking the selected asset and its provenance. Six of the seven named cases select a commit different from the earlier screened HEAD.

## Matched evidence

Four candidate archives passed the recipe checksum and matched the commit-pinned metadata files. Of those, one has packaging patches and another uses an unsupported Yarn workspace. Three other archives exceeded the retrieval limits. Two recipes have readable root and named contexts. Both views used the same 772 exact-version requests, yielding 771 usable maintainer lists.

| Application | Root joined paths | Named joined paths | Prespecified comparison |
| --- | ---: | ---: | --- |
| Reiverr | 83 | 0 | Root hit. Named result unresolved because 311 corroborated backend paths lack artifact identifiers. |
| Karakeep | 1 | 725 | Named hit. Root result unresolved under the nonempty pnpm guard. |

The post hoc check applied to every corroborated one-edge pnpm root. Karakeep was the sole candidate. Its pinned manifest, lock importer and exact-version registry declarations corroborate the single mandatory edge and no mandatory descendants. The artifact digest and maintainer list agree with the shared registry collection. The check establishes a root zero in the declared dependency scope. Turnover remains compatible with one to seven affected projects among the seven named candidates. The method provides neither a population-wide effect size nor evidence of runtime execution.

## Replay

The [sample](../research/consumer_holdout/runs/yunohost-importer-frame/sample.json), [recipe ledger](../research/consumer_holdout/runs/yunohost-importer-frame/recipes.json), [comparison results](../research/consumer_holdout/runs/yunohost-importer-frame/results.json), and [post hoc check](../research/consumer_holdout/runs/yunohost-importer-frame/single_edge_sensitivity.json) record the experiment. The earlier YunoHost benchmarks retain their original units and values. Exact replay uses the archived private recipe, source and registry receipts.
