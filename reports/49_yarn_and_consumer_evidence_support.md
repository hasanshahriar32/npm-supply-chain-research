# Yarn Classic and evidence support across consumer frames

The [subsequent root audit](50_ist_final_evidence_and_handoff.md) verifies two additional empty modern Yarn roots.

Applying the YunoHost Yarn Classic check to the Awesome-Selfhosted frame resolves 12 additional shared hits. This raises paired resolution from 74 to 86 of 155 and narrows turnover from 0–52.3% to 0–44.5%. All three version cutoff choices give the same result. Feasible net change is −44.5 to +43.2 percentage points. The five-account comparison still has zero confirmed changes in this frame. [Registry and comparison results](../research/consumer_holdout/runs/selfhosted-yarn-evidence/results.json)

Twenty-three unresolved projects had a pinned root manifest, a single Yarn lockfile, and HTTP 404 receipts for the other recorded root lockfile names. Six had readable traces and six partial traces. Nine used a newer format and two declared unsupported workspaces. Prior Yarn registry observations confirmed three shared hits. The frozen extension requested 1,828 exact versions, returning 1,728 usable maintainer lists. The 93 transport failures and seven records without usable lists leave gaps in metadata. All twelve projects with usable paths gained a confirmed shared hit, which fixes both binary outcomes in those projects. [Frozen protocol](../research/consumer_holdout/runs/selfhosted-yarn-evidence/protocol.json) · [Registry queue](../research/consumer_holdout/runs/selfhosted-yarn-evidence/registry_queue.json)

| Root evidence group | Awesome-Selfhosted resolved | YunoHost resolved |
| --- | ---: | ---: |
| npm | 48 / 57 | 94 / 108 |
| pnpm | 22 / 34 | 37 / 44 |
| Yarn | 12 / 23 | 23 / 35 |
| Bun | 0 / 4 | 1 / 6 |
| Multiple manager families | 0 / 1 | 0 / 4 |
| No usable lockfile at intake | 4 / 8 | 9 / 18 |
| No retained root manifest | 0 / 28 | 0 / 0 |
| **Total** | **86 / 155** | **164 / 215** |

Five confirmed coverage changes appear in the YunoHost npm group. Within the npm groups, turnover remains compatible with 0–15.8% in Awesome-Selfhosted and 4.6–17.6% in YunoHost. The groups come from retained files and, in YunoHost, the package manager selected at intake. Their overlap shows that even this comparison cannot resolve a direction of difference across catalogs. Twenty-eight of the 69 unresolved Awesome-Selfhosted pairs lack a retained root manifest. [Support ledger](../research/consumer_holdout/runs/selfhosted-yarn-evidence/support.json)

## IST recheck

The 2026 IST editorial emphasizes practical contribution, empirical validation and transparent reporting. The manuscript now gives a concrete decision at the five-account budget and shows how the toolchain and file support affect the conclusions. The companion reproduces both application frames and the conditional evidence counts. [IST editorial](https://www.sciencedirect.com/science/article/abs/pii/S0950584926001862) · [SIGSOFT repository-mining standard](https://github.com/acmsigsoft/EmpiricalStandards/blob/master/docs/standards/RepositoryMining.md)

Recent journal work distinguishes registry resolution, lockfile behavior and runtime use. This paper contributes evidence about which pinned applications change documented scope at an equal review budget. It supports a Q1 submission on that question. Inferences about catalog-wide superiority, runtime loading or effectiveness of a security intervention require different measurements. The revised related work includes the 2025 study of resolved dependencies and runtime accesses in 91 CommonJS packages. [TSE resolution study](https://doi.org/10.1109/TSE.2026.3717842) · [EMSE lockfile study](https://link.springer.com/article/10.1007/s10664-025-10789-w) · [JSS runtime study](https://www.sciencedirect.com/science/article/pii/S0164121225001773)
