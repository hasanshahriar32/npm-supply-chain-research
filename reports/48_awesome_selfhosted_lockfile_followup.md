# Awesome-Selfhosted lockfile follow-up

The subsequent [Yarn Classic follow-up](49_yarn_and_consumer_evidence_support.md) adds evidence beyond the npm and pnpm results in this report.

The final five-account sensitivity resolves 74 of 155 projects. It confirms 51 shared hits and 23 shared negatives. Across all three version cutoff choices, turnover remains compatible with 0–52.3%, and net change ranges from −52.3 to +51.0 percentage points. YunoHost still supplies the five confirmed changes at this budget. [Final results](../research/consumer_holdout/runs/selfhosted-lockfile-followup/extension_results.json)

| Cumulative evidence | Resolved pairs | Turnover |
| --- | ---: | ---: |
| Original comparison | 29 | 0–81.3% |
| Corroborated empty roots | 42 | 0–72.9% |
| New readers and previously retained registry observations | 73 | 0–52.9% |
| Dated registry extension | 74 | 0–52.3% |

The follow-up takes the pinned root manifest and the single retained root lockfile when the other recorded lockfile names returned HTTP 404. It covers 27 npm and 26 pnpm files. Arborist and committed lockfile records corroborate npm paths. The pnpm comparison uses paths up to three mandatory production edges from the native offline listing and a separate lockfile reader. At least one location is corroborated in 37 projects. Registry joins use canonical public npm paths or matching SHA-512 values. The first follow-up links 1,928 locations to original Awesome-Selfhosted observations and 3,519 to previously retained YunoHost observations. It adds 28 common positives and three common negatives. [Path replay](../scripts/study_selfhosted_lockfile_followup.py) · [First-stage counts](../research/consumer_holdout/runs/selfhosted-lockfile-followup/results.json)

We froze 63 additional exact-version requests from six unresolved projects before acquisition. All returned usable maintainer lists on 21 November 2026. The projection retains observed dates, artifact digests and numeric membership for the frozen portfolios. The additional records establish one more shared negative. The extracted companion replays both stages with the retained outputs. [Acquisition queue](../research/consumer_holdout/runs/selfhosted-lockfile-followup/registry_queue.json) · [Offline replay](../scripts/study_selfhosted_registry_extension.py) · [Replication companion](../submission/ist/IST_Consumer_Replication.zip)

For the 777 canonical keys with records in both earlier captures, the two observations list the same accounts from the five-account portfolios. The observations disagree for 90 of the 777 keys once the account comparison includes the 100-account control. This gives direct support for pooling the overlap in the five-account comparison and shows why agreement should be checked separately for wider selections.

## Empirical readiness

The second frame now has 32 more resolved pairs than the previous manuscript. Its upper turnover bound falls by 20.6 percentage points. The follow-up addresses missing evidence within the existing frame while keeping the original comparison and the dated sensitivities visible. The six-budget comparison remains on the earlier, common evidence base. The two frames have different artifact support and 81 self-hosted pairs remain unresolved. No cross-catalog effect, directional improvement, or deployed dependency coverage can be established from these results.

The paper remains a reasonable Q1 submission on fixed-budget account selection and documented consumer root coverage. The strongest evidence is the held-out, paired YunoHost result under the frozen contrast and its cutoff checks. The wider self-hosted bounds define how far that conclusion can travel. [Current IST manuscript](../submission/ist/IST_Manuscript.pdf) · [ACM SIGSOFT repository-mining standard](https://github.com/acmsigsoft/EmpiricalStandards/blob/master/docs/standards/RepositoryMining.md)
