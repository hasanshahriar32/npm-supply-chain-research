# Q1 submission reassessment, 21 November 2026

**Verdict.** The current evidence makes a credible submission to a Q1 empirical software engineering journal. Frame it as measurement of documented dependency coverage under different maintainer selections. I favor one focused editorial revision before sending it. An effectiveness claim about preventing compromises, or an ecosystem-wide estimate of turnover, would need additional evidence.

## Evidence against the original rejection

The earlier decision questioned empirical depth and the relevance of the data. The current draft tests the selection in real projects from two held-out application frames, with pinned root manifests, corroborated locked dependency paths, and exact-version registry observations. Its primary five-account YunoHost sensitivity now resolves 164 of 215 applications. The classification ledger contains 88 shared positives, 71 shared negatives, three name-only positives, and two version-only positives. The remaining 51 yield a finite-frame turnover interval of 2.3–26.0% and a net interval of −23.7 to +22.3 percentage points. Both directions remain possible. These are bounds from unresolved observations. [Current manuscript](../submission/emse/EMSE_Manuscript.pdf) · [November replication companion](../submission/emse/EMSE_Consumer_Replication.zip)

The five discordant cases provide the strongest evidence that representation can change which applications a fixed review budget reaches. The Awesome-Selfhosted frame corroborates paths to 23 shared projects with six shared negatives. Its 126 unresolved cases limit replication of the YunoHost contrast. The shipped archive results add a case of confirmed file inclusion and a case where available metadata leaves compiled module membership unresolved. Keep their one-release scopes explicit. [Five cases](../research/consumer_holdout/runs/yunohost-yarn-classic/confirmed_cases.md) · [Shipped module evidence](40_yunohost_shipped_module_evidence.md)

An additional retrospective check applied the original additive orders at a common set of budgets. It used the same YunoHost paths, locally retained account records from the initial and Yarn Classic runs, and the 34 corroborated empty roots. The reduced Bun receipt projection is limited to the original portfolios, so the following table leaves out the Bun shared positive from the published five-account comparison. Alternative cutoff ties were outside this reassessment.

| Account budget | Shared accounts | Resolved pairs | Confirmed name only | Confirmed version only | Turnover bounds |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 1 | 155 | 0 | 0 | 0.0% |
| 5 | 3 | 163 | 3 | 2 | 2.3–26.5% |
| 10 | 10 | 166 | 0 | 0 | 0.0% |
| 25 | 25 | 166 | 0 | 0 | 0.0% |
| 50 | 49 | 166 | 1 | 0 | 0.5–23.3% |
| 100 | 97 | 166 | 0 | 0 | 0.0–22.8% |

At 50, the confirmed name-only project is Y051, with 45 joined locations. The contrast can occur at more than one tested budget, and its evidence changes substantially with budget. The one-, ten-, and 25-account selections are identical across representations, which fixes turnover at zero even if some individual project outcomes remain unresolved. Keep the five-account result as the frozen confirmatory comparison and describe this budget check as exploratory.

## Comparison with published evidence

| Prior paper | What it validates | What this manuscript can claim |
| --- | --- | --- |
| Gamage et al., EMSE, 2026 | Design across seven package managers and interviews with 15 developers on lockfile practice. | The pinned consumer files establish a measurable consequence for portfolio coverage. Practitioner preferences and review costs remain open. |
| Bifolco et al., IST, 2025 | Accuracy of platform dependency records against project evidence in Java and Python, with a replication artifact. | The contribution goes from graph discrepancies to a paired decision outcome under a fixed budget, with uncertain cases kept in the denominator. |
| Wang et al., TSE, 2026 | Characterization across ten package managers and a scalable resolution framework. | The narrower representation comparison can show downstream consequences using project-owned lockfiles. Broad resolver evaluation would be a different contribution. |

[Gamage et al.](https://link.springer.com/article/10.1007/s10664-025-10789-w) · [Bifolco et al.](https://www.sciencedirect.com/science/article/pii/S0950584925001934) · [Wang et al.](https://www.computer.org/csdl/journal/ts/2026/11/11627712/2iwk9uDqra8)

The novelty is moderate and defensible. Concentration of npm maintainer reach has a direct historical precedent. Coordinated upstream prioritization also has recent precedent. The strongest distinction is the paired test of *which actual consumers change documented coverage* under alternative representations, with visible uncertainty about the unresolved cases. The current manuscript's recent-reference window leaves the closest historical comparison implicit. An explicit attribution would improve positioning if the authors allow a historical exception. [Zimmermann et al.](https://www.usenix.org/conference/usenixsecurity19/presentation/zimmerman) · [He et al.](https://www.microsoft.com/en-us/research/publication/pinning-is-futile-you-need-more-than-local-dependency-versioning-to-defend-against-supply-chain-attacks/)

## Submission decision

- **Research case.** Lead the 41-page Springer draft with one practitioner decision and the paired consumer result. Condense the sequence of sensitivity analyses to an evidence table and move parser-specific narrative to the supplement. Clarify which contrast was frozen before held-out collection and which checks were retrospective. The bounded claim can proceed with 51 unresolved cases.
- **Artifact.** The current source archive matches its exported TeX. I ran the main reproduction and final diagnostic from a clean extraction of the November archive. Reviewers can reproduce scoring from retained paths and observation projections. Full collection replay has additional inputs, and the public October artifact covers earlier work. All 28 repository unit tests passed.
- **Venue.** SCImago lists both Information and Software Technology and Empirical Software Engineering as Q1 in Software for 2025. This verifies SJR, with JCR assessed separately if the institution requires it. I would prioritize Information and Software Technology for the dependency-evidence angle. EMSE also fits the topic. Any new submission there should account for the previous decision and show what changed in the evidence. [IST ranking](https://www.scimagojr.com/journalsearch.php?q=18732&tip=sid) · [EMSE ranking](https://www.scimagojr.com/journalsearch.php?clean=0&q=18650&tip=sid) · [EMSE scope](https://link.springer.com/journal/10664/aims-and-scope)
- **Approval.** The current package records the two authors' contribution statement as a draft. Both authors' confirmation and approval of the exact submission remain open in the repository. [EMSE submission guidelines](https://link.springer.com/journal/10664/submission-guidelines)
