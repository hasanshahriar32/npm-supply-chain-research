# Gap-Resolution Study Protocol

## Title

**A Multi-Queue, Time-Aware Benchmark for Defensive Prioritization in the npm Supply Chain**

## Research decision

The project will not claim that an HGAT predicts “attacker ROI” or that a single score forecasts both malicious payloads and control-plane compromise. The literature shows that dependency topology, npm weak-link metadata, package-content malware detection, public CI/CD configuration risk, release-authority discontinuities, and historical dependency resolution are active but distinct research areas. [1] [2] [3] [4] [5] [6]

> **Selected contribution.** The defensible contribution is a reproducible, time-aware benchmark that compares three distinct defensive review queues—**structural leverage**, **public CI/CD observability**, and **release-authority discontinuity**—against separately adjudicated package/version incident labels. It asks which queue is useful for which decision, how much each feature family adds beyond strong baselines, and where public observability fails.

This framing is worthy because it converts an overbroad predictive claim into an auditable decision problem while preserving the practical question: *which packages or releases should defenders review first under limited attention?* Its novelty is conditional on releasing the time-indexed join, clear target definitions, strict baselines, and overlap/ablation analyses—not on inventing another graph model.

## Candidate contribution assessment

| Candidate | Prior-work collision | Feasibility with public evidence | Publication value | Decision |
|---|---|---:|---:|---|
| “HGAT predicts attacker ROI” | Very high; claim combines unsupported causal and predictive assumptions | Low until many historical labels and snapshots exist | Low due to overclaim risk | Reject as headline |
| Dependency and maintainer centrality ranking | High; ecosystem concentration is well established [1] | High | Moderate if used as a baseline | Retain as baseline |
| Public CI/CD exposure score from workflow presence | Moderate; workflow security is well studied [4] [5] | Medium; only public configuration is visible | Moderate if semantically parsed and missingness-aware | Retain as one queue |
| Release-authority discontinuity score | High; recent work already defines a public control-plane queue [6] | Medium to high where predecessor records exist | Moderate as replication/extension | Reuse and compare; do not relabel as novel |
| Time-aware multi-queue benchmark with controlled labels and decision boundaries | Lower; required components exist separately, but their decision-oriented comparison is not established by the reviewed work | Medium; staged artifact construction is practical | High if released with provenance and negative results | **Select** |

## Research questions and falsifiable hypotheses

| ID | Question | Null / decision rule |
|---|---|---|
| RQ1 | Does structural leverage rank later, high-confidence compromised package versions above popularity, dependency-count, and weak-link baselines at fixed historical cutoffs? | If it does not improve rank metrics with uncertainty bounds, publish it as descriptive leverage rather than prediction. |
| RQ2 | Do parsed public CI/CD configuration features add discriminatory or operational value beyond structural features? | If only workflow presence drives results or missingness dominates, report public-CI/CD observability as insufficient. |
| RQ3 | How much do the structural, CI/CD, and release-authority queues overlap, and do they surface different review candidates? | If overlap is near-total, a unified but interpretable queue may be adequate; otherwise retain separate queues. |
| RQ4 | Are any apparent results robust to strict historical feature availability, incident-family grouping, and popularity controls? | If strict-fidelity performance collapses, do not use “pre-incident prediction” language. |
| RQ5 | Does a heterogeneous graph model add stable value beyond regularized tabular, gradient-boosted, and transparent weighted-score baselines? | Add graph learning only if it improves pre-registered rank/calibration metrics under matched temporal splits and computational cost is justified. |

## Unit of analysis and targets

The primary unit is a **package-version observation** at cutoff time \(t\), with a package-level rollup only where all included versions share the same feature cutoff. This avoids assigning a later malicious release to an earlier benign version.

Three targets must remain separate:

| Target | Positive definition | Main evidence | Use |
|---|---|---|---|
| `future_confirmed_compromise` | A high-confidence targeted compromise begins within horizon \((t,t+h]\) | Government, maintainer, or technically corroborated version-level record | Primary, rare-event ranking target |
| `future_malicious_publication` | A reviewed malicious package release begins within \((t,t+h]\), excluding ordinary vulnerabilities | Version-level incident datasets plus independent verification | Secondary sensitivity target |
| `review_surface` | A package/release satisfies a transparent structural, CI/CD, or authority rule at \(t\) | Historical ecosystem and repository evidence | Operational queue; not a compromise label |

## Population and sampling frame

The first analysis must describe the actual available population rather than assert ecosystem coverage. The current project snapshot contains **25,228 packages** and is a seed-and-expansion sample, not all npm packages. The released benchmark must therefore report:

1. snapshot identifier, collection period, and source checksums;
2. inclusion path or sampling stratum for each package;
3. package, version, maintainer, repository, and workflow missingness;
4. event coverage by date and incident family; and
5. all exclusions before seeing outcome metrics.

The staged design has two valid scopes. **Scope A** is a current descriptive cross-sectional study of structural leverage and observable workflow configuration. **Scope B** is a temporal benchmark limited to candidate packages for which every primary feature satisfies strict or reconstructed historical fidelity. Scope A must never borrow outcome language from Scope B.

## Feature families and availability ledger

Every feature record must have `source_system`, `observed_at`, `effective_at`, `cutoff_rule`, `historical_fidelity`, `leakage_risk`, `missingness_reason`, and an immutable source reference.

| Family | Examples | Fidelity requirement for primary temporal evaluation | Interpretation limit |
|---|---|---|---|
| Dependency structure | direct/transitive dependents, resolved dependency depth, version-aware reach | Exact or reconstructed resolution at/before cutoff; preferably CHRONO-RESOLUTION [5] | Reach is not exploitability |
| Maintainer structure | package count per publisher/maintainer, ownership transition, concentration | Historical registry ownership, not current account metadata | Public identities may be ambiguous or incomplete |
| Weak-link hygiene | install scripts, inactive ownership, account/domain indicators | Source state before cutoff | A weak link is not evidence of compromise [2] |
| Public CI/CD configuration | permissions, risky triggers, SHA pinning, third-party actions, OIDC, environment use, runner labels | Workflow commit valid at/before cutoff | YAML does not reveal actual secrets, cloud scope, or business impact [4] [7] |
| Release authority | publisher/repository/provenance/workflow deltas from predecessor | Predecessor-aware release record | A discontinuity is a review candidate, not a malicious label [6] |
| Popularity/confounders | dated downloads, age, release cadence, direct dependents | Dated source only | Must be controlled, not omitted |

## Queue definitions

The initial protocol uses interpretable queues, frozen before target scoring. Each queue reports its own score components, ranks, and missingness rather than collapsing them into “attacker ROI.”

### Queue S — structural leverage

Rank packages by a pre-specified combination of version-aware downstream reach and maintainer concentration. Compare the combination against its components separately. Use rank-normalized values only within the frozen population at each cutoff. Report results after stratifying or residualizing for direct dependents and dated popularity.

### Queue W — public workflow observability

Rank repositories only by transparent public configuration indicators. Candidate indicators are explicit write permissions, privileged triggers paired with checkout patterns, unpinned third-party actions, `id-token: write`, self-hosted runner labels, deployment/environment use, and workflow churn. This queue must include an `unobservable` state rather than treating no public workflow as a safe outcome. GitHub’s guidance and prior measurement motivate the indicators but do not validate them as compromise probabilities. [4] [7]

### Queue A — release authority

Use the predecessor-aware record from the release-authority literature where available: publisher, repository, workflow, provenance, signing, and publication-mediation changes. Report independently from S and W, including its overlap with later incident labels. Do not mutate it to maximize label overlap. [6]

## Label registry protocol

Each record must contain the canonical package name, exact version/range, event-start time, first public detection time, incident family, evidence URLs, retrieval date, confidence, reviewer decision, and exclusion reason. Labels use the following hierarchy:

1. government/registry alert with package/version evidence;
2. maintainer post-mortem or repository advisory;
3. independent technical evidence with artifact linkage;
4. peer-reviewed/archival incident corpus;
5. OSV or GitHub Advisory entry corroborated by another source.

The registry stores **confirmed**, **campaign-associated**, **ordinary vulnerability**, **ambiguous**, and **excluded** classes. Ambiguous and campaign-associated records are not primary positives. Candidate discovery may use OSV and modern malware benchmarks, but human adjudication sets primary labels. [3] [8] [9]

## Split design and leakage controls

Use rolling-origin splits with non-overlapping incident-family groups. The final period must remain untouched until all feature transformations, thresholds, and model choices are frozen.

| Stage | Data allowed | Prohibited leakage |
|---|---|---|
| Development | Earlier cutoffs and later outcomes in development windows | Final-period labels, current workflow state, post-event advisories |
| Validation | Next chronological period | Changing feature definitions after inspecting final test |
| Final test | One pre-registered latest cutoff | Hyperparameter, threshold, or queue redesign based on outcome |
| Sensitivity analysis | Inclusive labels and approximate-fidelity features | Replacing strict primary results with favorable approximate outcomes |

Dependency snapshots must respect package-manager semantics. A current graph cannot be substituted for a past resolution without an explicit `approximate` fidelity label. Package and campaign families must not straddle training and test splits when their shared artifacts create correlated leakage. [5] [10]

## Baseline and model ladder

| Tier | Model or score | Role |
|---|---|---|
| 0 | Random prevalence-aware ranking | Sanity baseline |
| 1 | Direct dependents, transitive reach, dated downloads, package age | Confounding baselines |
| 2 | Weak-link metadata score | Proactive npm-risk baseline [2] |
| 3 | Regularized logistic regression / discrete-time survival model | Interpretable multivariate baseline |
| 4 | Gradient-boosted trees with monotonic/interaction audit | Nonlinear tabular comparator |
| 5 | Homogeneous graph embedding/model | Tests graph structure independent of heterogeneity |
| 6 | Heterogeneous graph model | Optional; retained only if it offers stable incremental value |

All learning models use the same cutoff-valid feature information and grouped temporal splits. Attention weights are never treated as causal explanation. The graph model is omitted from the initial descriptive study if label count or historical coverage is insufficient.

## Evaluation and uncertainty

Primary measures are PR-AUC, Recall@K, Precision@K, normalized discounted cumulative gain, and enrichment over prevalence for fixed review budgets \(K\). Calibration metrics include Brier score, calibration intercept/slope, and reliability plots when probabilistic predictions are feasible. Report bootstrap confidence intervals clustered by incident family and package family; also report a permutation or label-shuffle sanity check.

For operational queues without a future-compromise outcome, evaluate: (a) component availability, (b) candidate volume, (c) queue overlap, (d) reviewer agreement on a preregistered sample, and (e) stability across adjacent cutoffs. Do not invent a success metric by assuming any review candidate is malicious.

## Minimum publication threshold

The work is publishable if it releases a provenance-complete benchmark and demonstrates either a useful, uncertainty-qualified incremental ranking result **or** a credible negative finding that public workflow and structural features do not support pre-incident prediction beyond confounders. It is not publishable as a forecasting claim if strict temporal fidelity is unavailable, if high-confidence labels are too sparse, or if metrics fail to beat transparent baselines.

## Immediate executable work packages

| Work package | Output | Completion test |
|---|---|---|
| WP1: Current snapshot audit | Descriptive leverage and workflow-proxy distribution report | Reproducible script and CSV summary from the committed metrics archive |
| WP2: Feature ledger | Machine-readable feature availability table | Every feature has time/fidelity/missingness fields |
| WP3: Seed incident registry | Version-level reviewed rows for authoritative anchors | Every inclusion has source URL, event time, confidence, and reviewer rationale |
| WP4: Queue overlap study | Structural, workflow, and authority queue join | No composite “ROI” label; overlap and missingness reported |
| WP5: Temporal pilot | One frozen-cutoff, grouped incident-family evaluation | Strict and approximate fidelity results reported separately |
| WP6: Model comparison | Baseline ladder with reproducible configuration | HGAT only runs after Tier 0–4 completion |

## References

[1]: https://www.usenix.org/conference/usenixsecurity19/presentation/zimmerman "Zimmermann et al., Small World with High Risks"
[2]: https://arxiv.org/abs/2112.10165 "Zahan et al., What are Weak Links in the npm Supply Chain?"
[3]: https://arxiv.org/abs/2005.09535 "Ohm et al., Backstabber’s Knife Collection"
[4]: https://www.usenix.org/conference/usenixsecurity22/presentation/koishybayev "Koishybayev et al., Characterizing the Security of GitHub CI Workflows"
[5]: https://arxiv.org/abs/2607.15315 "Rahman et al., CHRONO-RESOLUTION"
[6]: https://arxiv.org/abs/2606.22593 "Santos-Grueiro, On Good Authority"
[7]: https://docs.github.com/en/actions/reference/security/secure-use "GitHub, Secure use reference"
[8]: https://google.github.io/osv.dev/ "OSV documentation"
[9]: https://arxiv.org/html/2603.27549v1 "Guo et al., Understanding NPM Malicious Package Detection"
[10]: https://dl.acm.org/doi/abs/10.1145/3510003.3510142 "Liu et al., Demystifying Vulnerability Propagation"
