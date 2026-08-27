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

## Temporal implementation amendment — 24 August 2026

The expanded reconstruction stage contains sixteen adjudicated package-event records in eleven incident families; fourteen strict pre-event package-version objects were reconstructed from official npm registry version-time maps. The independently corroborated `node-ipc` family adds three affected releases and selects `node-ipc@12.0.0` immediately before the earliest malicious publication cutoff. [12] [13] The independently corroborated `@emcd-vue/auth` dependency-confusion family is retained as label-only because the current registry response lacks a usable pre-cutoff version object. [15] [16] A frozen Wiz IOC CSV and OpenSSF `MAL-2025-191155` independently agree on `wenk@1.0.9` and `wenk@1.0.10` in the November 2025 Shai-Hulud second wave; the official registry timestamp of `wenk@1.0.9` defines the strict cutoff and selects `wenk@1.0.8` as an exact pre-event source object. [20] [21] SafeDep and OpenSSF `MAL-2026-4127` agree on Mini Shai-Hulud `atool` package `amapcn@0.2.2` and `0.3.2`; the official registry timestamp of `amapcn@0.2.2` defines the cutoff and selects `amapcn@0.1.2` as the exact pre-event source object. [22] [23] Frozen OpenSSF `MAL-2025-6020`, a dated StepSecurity report, and the `is` maintainer’s remediation changelog agree on `is@3.3.1` and `5.0.0`; the earliest official registry timestamp selects `is@3.3.0` as the exact pre-event source object. [25] [26] [27] Frozen OpenSSF `MAL-2026-11524`, frozen Wiz `keyv-packages.csv`, and independent Snyk research agree on `keyv@6.0.0`; the official registry timestamp selects `keyv@6.0.0-rc.1` as its exact pre-event source object. [28] [29] [30] [31] Snyk and Sonatype independently document related intentional breaking publications for `colors` and `faker`, while Russ Cox independently records intentional sabotage of both packages. [56] [57] [58] Official registry times select `colors@1.4.0` and `faker@5.5.3` as their strict pre-event objects. [59] [60] The two package-event records form one shared-maintainer family and one future validation unit. Wiz describes the Keyv payload as Mini Shai-Hulud-descended, so the dated `keyv_cacheable_august_2026` family remains separate for campaign grouping but is not asserted statistically independent of `mini_shai_hulud_atool_2026`. The companion artifact records 29 exact source-version direct dependency declarations. A separate bounded pass selected a highest satisfying target version for each of the 29 ranges using only target versions whose registry timestamp is at or before the relevant cutoff. These target values are labeled **`registry_reconstructed_cutoff_semver_approximation`** and must not be interpreted as package-lock entries, historical npm installation results, or transitive graph edges.

The bounded registry-only sensitivity graph contains 64 depth-limited edges across nine roots with runtime dependencies. It remains a range-selected sensitivity artifact rather than a lockfile, historical installation tree, dependency-reach measure, or blast-radius estimate. The sixteen records span eleven campaign families but do not become independent samples through campaign naming; fourteen exact snapshots span ten exact-snapshot families, and the inference gate remains blocked by the missing cutoff-valid adjudicated control population, two label-only events without exact feature objects, and no historical resolver-backed traversal. Consequently, it reports no ranking, PR-AUC, Recall@K, calibration, logistic-regression, blast-radius, or attack-return metric.

`94_campaign_relatedness_and_grouped_inference_protocol.json` now records the relatedness registry that any future eligible evaluation must use. It maps all sixteen event records to eleven campaign families, preserves shared-family partitioning, and creates ten validation units by grouping `mini_shai_hulud_atool_2026` with `keyv_cacheable_august_2026` only for validation and resampling while retaining colors/faker as one shared-maintainer family. The grouping reflects documented payload lineage or shared-maintainer incident context, not proof of common actor, complete campaign membership, or causal transmission beyond the source descriptions. Any future temporal split must assign each validation unit as a whole to development, validation, or final test; any eligible uncertainty procedure must resample those units rather than package-event rows. GroupKFold, GroupShuffleSplit, and scikit-learn’s group/time-aware validation guidance inform this implementation pattern only. [32] [33] [34] No split, resampling replicate, model fit, interval, ranking, or metric has been generated while the primary control-frame gate remains blocked.

`95_release_authority_metadata_availability_audit.json` records a separate availability gate for the release-authority queue. Among the fourteen exact source objects, an immediate earlier retained registry version object exists for all fourteen; paired repository-descriptor availability exists for thirteen and paired `gitHead` availability for eleven. These counts establish neither field values nor release-authority deltas. The audit excludes root-document state, current dist-tags, current maintainers, current repositories and workflows, downloads, dependency graphs, metadata-value emission, equality tests, and delta classification. It records no publisher transition, repository transfer, provenance change, score, outcome effect, rank, model, or metric. A future authority feature requires a separate pre-registered semantics and fidelity decision after the control-frame gate opens.

`96_release_authority_delta_semantics_protocol.json` supplies that future-only decision contract without applying it. It defines six candidate delta families—repository link, source revision, release-manifest publication intent, verifiable provenance attestation, release mediation/publisher authority, and release-bound workflow authority—and requires field-specific raw evidence, immutable provenance references, canonicalization, time-validity, and missingness rules. The protocol adopts `not_eligible_missing_or_ambiguous_evidence` and `not_applicable_to_release_regime` rather than an unchanged fallback. It retains Santos-Grueiro’s predecessor-aware comparison as a review-surface design reference, not an outcome target; it also retains npm’s documented qualification that provenance does not guarantee no malicious code. [35] [36] [37] No raw values, comparisons, classified deltas, scores, controls, effects, ranks, models, intervals, or metrics have been produced.

`97_official_npm_provenance_attestation_access_assessment.json` constrains the attestation branch further. The strict ledger provides fourteen exact pre-event source objects, but the official documentation reviewed establishes `npm audit signatures` for downloaded dependency sets rather than a documented, unauthenticated metadata-only retrieval path for an arbitrary historical version. The public Registry API reference reviewed during the screen does not supply such an attestation-bundle endpoint. The protocol therefore made zero endpoint requests, guesses, downloads, installations, verification runs, retrieved bundles, or attestation-state classifications. This is an access-contract result, not evidence that an attestation is absent; current provenance indicators and transparency-log queries remain excluded as historical evidence. [38] [39] [40] No controls, authority scores, models, rankings, or metrics were created.

`98_full_ledger_source_object_retention_census.json` extends the strict reconstruction boundary to every one of the sixteen package-event records. It records checksum-bound current registry response retention, not release-time package state. Fourteen records retain a selected pre-cutoff source version object and remain eligible for the existing strict reconstruction; `plain-crypto-js` has a time-map selection whose selected object fails strict retention, and `@emcd-vue/auth` has no retained pre-cutoff selection. Both remain label-only. The census emits identifiers, timestamps, retention states, and response provenance only. It emits zero package, maintainer, publisher, repository, workflow, provenance, or attestation values; derives zero features; and creates zero controls, scores, models, rankings, or metrics. Current retention differences never imply safe, benign, unchanged, no-known-event, or cross-campaign independence.

`99_release_authority_raw_evidence_capture_contract.json` is the next, deliberately non-executed layer beneath the delta ontology. It specifies the minimum future capture manifest, byte-integrity and chain-of-custody entries, source-time decision vocabulary, opaque canonicalization ledger, activation gate, abort conditions, and one narrow field-collection schema for each of the six delta types. Raw evidence must reside outside the public repository in an access-controlled immutable store; public-safe records may hold protocol identifiers, byte digests, lengths, reason codes, and non-reversible opaque references, but never raw repository links, revision strings, publisher identifiers, workflow text, certificates, credentials, provenance statements, canonicalized values, outcomes, or scores. Canonicalization must be offline, versioned, deterministic under its declared parameter digest, and committed under an access-controlled key. No source was contacted, no raw evidence was retrieved or stored, no canonicalization or time-validity decision was run, and no comparison, control, score, model, ranking, interval, calibration, or metric was created. The contract cannot activate until the separate primary control-frame gate, historical pair-retention requirements, access controls, and outcome separation are satisfied.

`100_future_outcome_manifest_sealing_protocol.json` defines the still-separate future outcome layer. It requires a pre-sealed target and horizon interval, scoped source inventory, version-specific candidate dockets, independent double adjudication and reconciliation, source-specific full-horizon coverage records, retraction-preserving immutable revisions, public-safe checksum/Merkle sealing, and outcome/feature blinding. A target decision is limited to a documented exact npm package version, event-time support, target fit, and frozen corroboration threshold. A non-event is only eligible after complete, documented coverage of the full horizon and registered exclusions; missing source membership, advisory absence, registry survival, no-known-event language, package deletion, and current state remain unknown. No source was contacted, no outcome row, positive, non-event, control, coverage record, manifest seal, feature join, split, score, model, rank, interval, calibration result, or metric was created. The protocol now inherits ten future validation units and requires that the documented Mini Shai-Hulud `atool` / Keyv/Cacheable related-family cluster never straddle an eligible partition; colors/faker remain one separate shared-maintainer unit. The existing sixteen strict incident records remain independently adjudicated positive evidence only, not a closed-world outcome population.

`101_future_public_safe_aggregate_release_policy.json` supplies the outcome protocol’s previously required public-safe release policy without releasing protected evidence. It defines P0 protocol metadata, P1 sealed integrity metadata, P2 screened descriptive aggregates, and P3 aggregate benchmark results. P0 alone is described by the present policy; P1 and P2 require independently sealed population/outcome/authority quality controls, source-term permissions, a separately sealed aggregate plan, independent disclosure review, small-cell and minimum-validation-unit controls, complementary suppression, differencing and external-linkage review, relatedness protection, temporal reconstruction-risk review, immutable revision lineage, and revocation handling. P3 is explicitly disabled pending a future amendment and an independently eligible benchmark. Raw source objects, protected package/version identities, outcome/control/unknown rows, authority values and commitments, reviewer material, feature rows, split membership, scores, ranks, intervals, and model metrics remain restricted. No source was inspected; no plan, release, cell, summary count, outcome, control, score, rank, model, interval, or metric was created. The existing 16 positives, 11 families, and 10 future validation units are themselves non-releasable as P2 aggregates unless an independent future disclosure review establishes a valid broader eligible frame.

`102_future_aggregate_plan_parameter_sealing_contract.json` specifies the otherwise unfilled sealed-parameter requirement for a future P2 aggregate plan. It requires secure-only custody of a complete parameter set, pre-inspection attestations, distinct parameter/disclosure/implementation/audit roles, access controls, key custody, append-only records, a non-reversible public-safe keyed commitment, independent verification, and strict amendment/revocation rules. The parameter authority receives only frozen protocol schemas and source-term constraints; it must never see protected evidence, candidate identities, rows, labels, controls, coverage decisions, aggregate previews, prevalence, scores, ranks, splits, model artifacts, intervals, calibration, or metrics before sealing. A post-access conflict aborts the release and requires a new protocol instance rather than parameter tuning. The current artifact sets zero thresholds, strata, rounding rules, suppression settings, aggregation measures, secure records, commitments, attestations, verification decisions, plans, cells, releases, outcomes, controls, scores, models, rankings, intervals, or metrics. Its commitment and verification status are governance metadata only and neither authorize release nor establish safe disclosure, coverage, a control frame, or model eligibility.

`103_crossenv_typosquatting_candidate_assessment.json` exercises the primary-ledger gate on an independently corroborated historic candidate without relaxing it. npm’s archived notice, a contemporaneous technical account, and a Snyk advisory identify the `crossenv` typosquatting incident and `crossenv@6.1.1`; the official registry time map fixes that release at `2017-07-19T06:49:52.698Z` and selects `6.0.7` immediately before the strict cutoff. [48] [49] [50] [51] The current bounded metadata response does not retain the selected `6.0.7` version object, however, so it cannot produce the exact source snapshot required by the ledger. The candidate remains excluded: it creates zero ledger rows, families, snapshots, declarations, resolver approximations, graph edges, validation units, controls, labels, historical installations, reach measures, scores, models, rankings, intervals, or metrics. This exclusion does not dispute the incident or infer a negative outcome from registry retention.

`104_flatmap_stream_candidate_assessment.json` applies the same gate to the package-level payload component of the established 2018 event-stream incident. npm identifies `flatmap-stream@0.1.1` as malicious and associated with `event-stream@3.3.6`; Snyk independently identifies the injected `0.1.1` release; and Microsoft independently blocks `0.1.0`, `0.1.1`, and `0.1.2`. [52] [53] [54] Current bounded registry metadata retains no official `0.1.1` timestamp, no `0.1.x` time-map history, and no historically relevant `0.1.x` source object—only an unrelated later `0.0.1-security` holder object. [55] No official exact cutoff or strict pre-event snapshot can therefore be reproduced, so the candidate is excluded rather than admitted. It adds zero ledger rows, families, validation units, snapshots, declarations, resolver approximations, graph edges, controls, labels, historical installations, reach measures, scores, models, rankings, intervals, or metrics. If future evidence ever makes the package eligible, it must remain within the existing `event_stream_2018` family; relatedness is not proof of independence, a new validation unit, campaign completeness, or causality.

`105_colors_faker_protestware_candidate_assessment.json` adds two strictly eligible related records without loosening the target or control boundaries. Snyk, Sonatype, and Russ Cox independently document the colors/faker incident context; official registry metadata provides exact cutoffs and selects `colors@1.4.0` and `faker@5.5.3` as retained pre-event objects. [56] [57] [58] [59] [60] The two records form the one `colors_faker_protestware_2022` family and one validation unit. They add no controls, historical installations, reach measures, authority observations, scores, models, rankings, intervals, or metrics.

### Debug update — 26 August 2026

`108_debug_september_2025_candidate_assessment.json` admits one bounded `debug@4.4.2` record under the separate `qix_npm_phishing_september_2025` family. The Debug maintainer issue and independent Wiz and StepSecurity reports agree on the exact affected release and phishing-driven npm-account-compromise context; the official registry timestamp fixes the strict cutoff at `2025-09-08T13:12:39.972Z` and selects retained `debug@4.4.1` as the exact source object. [65] [66] [67] [68] The current governed cohort is **17 records, 12 families, 15 exact snapshots, 30 direct declarations, 30 isolated cutoff-valid range approximations, 65 bounded registry-only sensitivity edges, and 11 future validation units**. The candidate adds one record, family, validation unit, snapshot, declaration, range approximation, and bounded edge, while preserving zero controls, benign labels, historical installations, reach measures, authority observations, scores, models, rankings, intervals, calibration results, and predictive metrics. It does not establish campaign completeness, common actor identity beyond documented context, or statistical independence from unadjudicated package rows.

`106_peacenotwar_protestware_candidate_assessment.json` applies the same frozen gate to the historic `peacenotwar` protestware candidate. Snyk’s incident report and dedicated advisory document the March 2022 publication context and mark all versions affected, while the CNCF catalogue independently records the malicious-maintainer context. [61] [62] [63] No inspected independent source identifies a finite exact `peacenotwar` release set; the current bounded official registry response begins at `9.1.1` on `2022-03-08T16:38:45.767Z`, leaving no version object strictly earlier than the cutoff. [64] The candidate is therefore excluded without altering the 16-record ledger, 11-family grouping, 10 validation units, or any governed reconstruction artifact. It creates zero snapshots, declarations, graph edges, controls, benign labels, historical installations, reach measures, scores, models, rankings, intervals, or metrics. The exclusion does not deny the incident, convert an all-version advisory into a finite target, or infer a benign or negative outcome from unavailable pre-event registry state.

The project assessed Open Source Insights' deps.dev BigQuery dataset as a possible provider-backed control-population source. Its documented full-snapshot, package-version, upstream-publication, and advisory fields could support a future frozen population design, but the advisory relation is vulnerability-oriented rather than a closed-world record of malicious publications or publisher compromises. [17] The provider requires a Google Cloud account and BigQuery API; the current no-credential metadata probe returned HTTP 401 and retrieved no rows. A versioned malicious/benign source-code dataset was also excluded because its public metadata does not establish package-version identity, collection cutoff, coverage, or outcome horizon. [18] [19] The protocol therefore retains its no-control decision: no package is classified as benign from absence in an advisory or catalogue.

The public CHRONO-RESOLUTION archive was selectively inspected through bounded HTTP byte ranges. Its validated relation schema includes package and dependency versions plus interval start/end, but its only relations payload is a 10.23 GB compressed, 138.73 GB uncompressed monolithic SQL member. A one-pass, memory-bounded attempt to stream that member timed out after 1,500 seconds with 7.6569% of the compressed stream received; no candidate rows were retained. A future transitive stage requires either an approved bulk-compute environment or an upstream filtered export, together with a pre-registered cutoff join and control design. [5]

The evaluated npm-follower resource is a relevant future source for version retention and population coverage, but its public project page describes a 20+ TB replica. The present worktree has neither an official query interface nor a frozen filtered export for it. Accordingly, this study does not convert registry rows with no known incident into benign controls. A temporal ranking or calibration stage remains conditional on a frozen incident-coverage source and a documented at-risk population frame. [11]

The current DataDog npm manifest was also frozen as a human-vetted, positive-only catalogue. It corroborates exact package-version membership for the Axios, node-ipc, amapcn, `is`, and `keyv` records and package presence without version detail for `plain-crypto-js` and `wenk`; its absence entries produce no conclusion. Because it has no row-level event time, campaign assignment, evidence URLs, or negative labels, it neither alters the primary ledger nor supplies a temporal control population. [14]

The npm-specific Original Sin of npm study is also excluded from the temporal-control population. It reports a 5 September 2023 npm-follower snapshot, random sampling, later live-registry availability/stub filtering, default-or-latest dependency construction, and OSV/NVD vulnerability records for a custom analysis database. [24] That supports methodology context for vulnerability timing and right-censoring only: the target is disclosed vulnerability propagation rather than malicious-publication or maintainer-compromise coverage, the final sample is not a frozen cutoff-valid at-risk denominator, no row-level custom-database release or query endpoint is named, and no future non-event horizon is declared. It creates zero controls, labels, model fits, or metrics.

`90_authorized_npm_control_frame_access_specification.json` supplies a non-executed reproducibility contract for the provider path already assessed as inaccessible and target-mismatched. The contract begins with a user-controlled BigQuery environment and one frozen `Snapshots.Time` value, selects npm `PackageVersions` rows only at the matching `SnapshotAt` and at or before the specified `UpstreamPublishedAt` cutoff, and records the exact query, parameters, deterministic export, job metadata, row count, and checksums. [17] It then requires an independent frozen positive-coverage manifest for malicious publication or maintainer compromise over a pre-registered horizon. Provider advisories remain vulnerability provenance only; advisory absence, a `Latest` view, current package state, or source omission cannot yield a non-event label. This is a future-access specification, not a query result: it creates zero rows, controls, labels, model fits, or metrics.

### Current strict-cohort amendment — 26 August 2026

The protocol now governs **23 positive package-event records in 17 incident families**, with **21 exact retained pre-event snapshots**, **69 direct declarations**, **69 isolated cutoff-valid SemVer approximations**, **322 bounded depth-three registry-only sensitivity edges**, and **16 future validation units**. The added `node-ipc-2022-03-07` record is a separate March 2022 maintainer-protestware event, not an extension of `node_ipc_2026`: GitHub’s reviewed advisory and Snyk’s contemporaneous report identify `10.1.1` and `10.1.2`, while official registry metadata fixes the earliest publication at `2022-03-07T11:03:59.179Z` and selects retained `10.1.0` before the one-millisecond cutoff.[61] [69] [70] [71]

This amendment preserves the existing negative/control, outcome-sealing, provenance-access, relatedness, and disclosure gates. No control, benign label, installation history, resolved lock, reach value, authority value, score, rank, interval, calibration result, model, or predictive metric is created.

### Bounded Noblox 2021 package-name screen — 26 August 2026

Sonatype and BleepingComputer independently identify `noblox.js-proxy` and `noblox.js-proxies` as the 2021 Roblox-targeting malicious npm package names. The retrieved reports do not state an exact affected release or finite affected-version set, however.[72] [73] A bounded official registry metadata response for `noblox.js-proxy` retains package-history timestamps and only a `0.0.1-security` version object, but registry state cannot convert package-name corroboration into a version-specific outcome target.[74]

The candidate is therefore excluded before cutoff selection and source-object reconstruction. It adds **zero** primary records, families, validation units, snapshots, direct declarations, SemVer approximations, graph edges, controls, benign labels, historical installations, reach values, authority values, scores, models, rankings, intervals, calibration results, or predictive metrics. The exclusion neither disputes the reports nor treats registry retention as evidence of benignness, safety, unchanged state, or no known event.

### Lottie Player October 2024 admission — 26 August 2026

The strict ledger now admits `@lottiefiles/lottie-player@2.0.5`, `2.0.6`, and `2.0.7` as one distinct October 2024 account-takeover family. LottieFiles’ incident resolution and independent Sonatype and Snyk reports identify the finite release set and unauthorized publishing context.[75] [76] [77] The earliest official registry publication is `2.0.5` at `2024-10-30T20:12:15.375Z`; the exact one-millisecond cutoff selects retained `2.0.4` as the strict pre-event source object.[78]

The protocol now governs **24 positive package-event records in 18 incident families**, with **22 exact retained pre-event snapshots**, **74 direct declarations**, **74 isolated cutoff-valid SemVer approximations**, **335 bounded depth-three registry-only sensitivity edges**, and **17 future validation units**. The Lottie Player row adds one family and one unit. It adds no control, benign label, installation history, resolved lock, reach value, authority value, score, rank, interval, calibration result, model, or predictive metric. The no-control/no-model gate remains blocked.

### Nx S1ngularity August 2025 admission — 26 August 2026

The strict ledger now admits `nx@21.5.0`, `20.9.0`, `20.10.0`, `21.6.0`, `20.11.0`, `21.7.0`, `21.8.0`, and `20.12.0` as one distinct August 2025 publish-token-compromise family. The Nx postmortem and reviewed GitHub advisory identify the finite release set and token-theft publication path; Snyk and StepSecurity independently retain the same `nx` versions.[79] [80] [81] [82] The earliest official registry publication is `21.5.0` at `2025-08-26T22:32:25.482Z`; the exact one-millisecond cutoff selects retained `21.5.0-canary.20250826-af44608` under the all-stream rule, with no same-branch substitution.[83]

The protocol now governs **25 positive package-event records in 19 incident families**, with **23 exact retained pre-event snapshots**, **109 direct declarations**, **109 isolated cutoff-valid SemVer approximations**, **458 bounded depth-three registry-only sensitivity edges**, and **18 future validation units**. The Nx row adds one family and one unit. It adds no control, benign label, installation history, resolved lock, reach value, authority value, score, rank, interval, calibration result, model, or predictive metric. The no-control/no-model gate remains blocked.

### country-currency-map March 2025 admission — 26 August 2026

The strict ledger now admits `country-currency-map@2.1.8` as one distinct March 2025 package-hijack family. Sonatype identifies `2.1.8` as the hijacked malicious release, and BleepingComputer independently names that deprecated release; the official npm registry timestamps it at `2025-03-25T09:03:00.518Z`.[84] [85] [86] The exact one-millisecond cutoff selects retained `country-currency-map@2.1.7` as the strict pre-event source object.

The protocol now governs **26 positive package-event records in 20 incident families**, with **24 exact retained pre-event snapshots**, **110 direct declarations**, **110 isolated cutoff-valid SemVer approximations**, **459 bounded depth-three registry-only sensitivity edges**, and **19 future validation units**. The country-currency-map row adds one family and one unit. It adds no control, benign label, installation history, resolved lock, reach value, authority value, score, rank, interval, calibration result, model, or predictive metric. The no-control/no-model gate remains blocked.

### html-to-gutenberg May 2026 admission — 26 August 2026

The strict ledger now admits `html-to-gutenberg@4.2.11` and `4.2.14` as one distinct May 2026 hijacked-publication family. GitHub’s reviewed malware advisory identifies the finite version set, and JFrog independently identifies the hijacked `4.2.11` release and May 2026 upload timing; The Hacker News independently corroborates the package-level hijack and upload date.[87] [88] [89] The earliest official registry publication is `4.2.11` at `2026-05-25T19:19:47.408Z`; the exact one-millisecond cutoff selects retained `html-to-gutenberg@4.2.10` as the strict pre-event source object.[90]

The protocol now governs **27 positive package-event records in 21 incident families**, with **25 exact retained pre-event snapshots**, **124 direct declarations**, **124 isolated cutoff-valid SemVer approximations**, **721 bounded depth-three registry-only sensitivity edges**, and **20 future validation units**. The html-to-gutenberg row adds one separate family and one unit; no relationship to another governed family is asserted. It adds no control, benign label, installation history, resolved lock, reach value, authority value, score, rank, interval, calibration result, model, or predictive metric. The no-control/no-model gate remains blocked.

### common-stack generate-plugin May 2026 admission — 27 August 2026

The strict ledger now admits `@common-stack/generate-plugin@9.0.2-alpha.21` and `9.0.2-alpha.22` as one distinct May 2026 hijacked-publication family. Sonatype identifies those two releases as malicious, and GitHub’s reviewed malware advisory independently includes the same two releases in its package-specific affected-version list.[91] [92] The governed target is the strict two-version intersection only; no later advisory-only versions are inferred into the primary row. The earliest official registry publication is `9.0.2-alpha.21` at `2026-05-21T15:54:08.581Z`; the exact one-millisecond cutoff selects retained `9.0.2-alpha.18` as the strict pre-event source object.[93]

The protocol now governs **28 positive package-event records in 22 incident families**, with **26 exact retained pre-event snapshots**, **126 direct declarations**, **126 isolated cutoff-valid SemVer approximations**, **760 bounded depth-three registry-only sensitivity edges**, and **21 future validation units**. The common-stack generate-plugin row adds one separate family and one unit; no relationship to another governed family is asserted. It adds no control, benign label, installation history, resolved lock, reach value, authority value, score, rank, interval, calibration result, model, or predictive metric. The no-control/no-model gate remains blocked.

### sbx-mask March 2026 source-object exclusion — 27 August 2026

The bounded `sbx-mask` screen has independently documented finite affected versions but fails the retained-source-object gate. Sonatype reports `sbx-mask` as a malicious package in a suspected trusted-maintainer-account compromise, while GitHub’s reviewed malware advisory independently identifies exactly `1.0.0`, `1.0.1`, and `1.0.2`.[94] [95] Official npm registry metadata timestamps the earliest affected version, `1.0.0`, at `2026-03-19T14:46:00.636Z`; strict subtraction yields `2026-03-19T14:46:00.635Z`. The response retains only `0.0.1-security`, which is later than the cutoff, so no strict pre-event version can be selected and no pre-event version object is retained.[96]

The resulting `138_sbx_mask_march_2026_candidate_assessment.json` is an exclusion, not a ledger addition. The governed cohort therefore remains **28 positive package-event records in 22 incident families, 26 exact retained snapshots, 126 direct declarations and isolated approximations, 760 bounded registry-only sensitivity edges, and 21 future validation units**. It creates zero snapshots, declarations, graph edges, controls, benign labels, historical installations, dependency reach or blast-radius values, authority values, scores, models, rankings, intervals, calibration results, or predictive metrics. Current registry retention is an eligibility constraint only: it does not dispute the incident, make an unretained release benign, or establish current publisher state, causal effects, or a non-event outcome.

### Bitwarden CLI April 2026 admission — 27 August 2026

The strict ledger now admits `@bitwarden/cli@2026.4.0` as one bounded April 2026 npm distribution-path compromise record. Bitwarden’s incident statement identifies the malicious distribution of that exact npm release during a limited 22 April window, while StepSecurity independently identifies the same package and version as compromised; the NVD-sourced public CVE record corroborates the same release.[97] [98] [99] The official npm registry time map lists `2026.4.0` at `2026-04-22T21:22:59.021Z`; the exact one-millisecond cutoff selects retained `@bitwarden/cli@2026.3.0` as the strict pre-event source object.[100]

The protocol now governs **29 positive package-event records in 23 incident families**, with **27 exact retained pre-event snapshots**, **153 direct declarations**, **153 isolated cutoff-valid SemVer approximations**, **974 bounded depth-three registry-only sensitivity edges**, and **22 future validation units**. The Bitwarden CLI row adds one bounded separate family and one unit. The documented broader Checkmarx context neither authorizes an additional package row nor establishes a relationship to an existing governed family or statistical independence. The row adds no control, benign label, installation history, resolved lock, reach value, authority value, score, rank, interval, calibration result, model, or predictive metric. The no-control/no-model gate remains blocked.

### React Native country-select March 2026 admission — 27 August 2026

The strict ledger now admits `react-native-country-select@0.3.91` as one bounded March 2026 malicious-publication family. StepSecurity and Aikido independently identify the same exact release; the governed target is their single-version intersection only, so later versions reported by StepSecurity are not inferred into the row.[101] [102] The official npm registry time map lists `0.3.91` at `2026-03-16T10:54:18.512Z`; the exact one-millisecond cutoff selects retained `react-native-country-select@0.3.9` as the strict pre-event source object.[103]

The protocol now governs **30 positive package-event records in 24 incident families**, with **28 exact retained pre-event snapshots**, **153 direct declarations**, **153 isolated cutoff-valid SemVer approximations**, **974 bounded depth-three registry-only sensitivity edges**, and **23 future validation units**. This row adds one bounded family and one unit. The sources document a same-day shared-publisher context with a separately named package, but that does not authorize another package row, campaign-complete census, assignment to an existing governed family, or statistical-independence claim. The row adds no control, benign label, installation history, resolved lock, reach value, authority value, score, rank, interval, calibration result, model, or predictive metric. The no-control/no-model gate remains blocked.

### rand-user-agent April–May 2025 unauthorized-publication admission — 27 August 2026

The strict ledger now admits `rand-user-agent@2.0.83`, `@2.0.84`, and `@1.0.110` as one bounded unauthorized-publication family. Aikido and BleepingComputer independently identify exactly these three releases; BleepingComputer also records direct developer confirmation of the three unauthorized npm publications.[104] [105] The bounded official npm registry time map lists earliest affected `2.0.83` at `2025-04-26T15:25:00.992Z`; the exact one-millisecond cutoff selects retained `rand-user-agent@2.0.82` as the strict pre-event source object.[106]

The protocol now governs **31 positive package-event records in 25 incident families**, with **29 exact retained pre-event snapshots**, **153 direct declarations**, **153 isolated cutoff-valid SemVer approximations**, **974 bounded depth-three registry-only sensitivity edges**, and **24 future validation units**. This row adds one bounded family, one exact source snapshot, and one unit, but no direct declarations, range approximations, or sensitivity edges. The documented unauthorized-publication context does not authorize expansion into other packages, an existing governed family, campaign completeness, or statistical independence. The row adds no control, benign label, installation history, resolved lock, reach value, authority value, score, rank, interval, calibration result, model, or predictive metric. The no-control/no-model gate remains blocked.

### Joyfill July 2026 relatedness exclusion — 27 August 2026

The bounded `@joyfill/components` screen identified one strict source intersection, `4.0.0-rc24-2773-beta.4`: StepSecurity reports three malicious `2773` beta versions, while Socket independently names that exact version.[107] [108] Socket explicitly links the package to the ongoing PolinRider supply-chain attack, which is already represented by the governed `common_stack_generate_plugin_polinrider_hijack_2026` family.[108] The screen therefore excludes it as a **new independent family** before registry access. It does not decide a later existing-family addition, because the present task is limited to genuinely separate candidates and does not authorize related-family expansion by inference.

The governed cohort remains **31 positive package-event records in 25 incident families**, with **29 exact retained pre-event snapshots**, **153 direct declarations**, **153 isolated cutoff-valid SemVer approximations**, **974 bounded depth-three registry-only sensitivity edges**, and **24 future validation units**. No official registry request, cutoff, or pre-event source object was selected. This exclusion adds no record, family, unit, snapshot, declaration, range approximation, graph edge, control, benign label, installation history, reach value, authority value, score, rank, interval, calibration result, model, or predictive metric. It does not dispute the reported version or establish campaign completeness, current publisher state, downstream exposure, causality, or statistical independence.

### AsyncAPI generator July 2026 admission — 27 August 2026

The strict ledger now admits `@asyncapi/generator@3.3.1` as one bounded GitHub Actions release-pipeline-compromise family. Aikido and Microsoft Security independently identify the exact affected release; the governed target is their single-version intersection only.[109] [110] The official npm registry time map lists `3.3.1` at `2026-07-14T07:10:48.853Z`; the exact one-millisecond cutoff selects retained `@asyncapi/generator@3.3.0` as the strict pre-event source object.[111]

The protocol now governs **32 positive package-event records in 26 incident families**, with **30 exact retained pre-event snapshots**, **179 direct declarations**, **179 isolated cutoff-valid SemVer approximations**, **1,408 bounded depth-three registry-only sensitivity edges**, and **25 future validation units**. This row adds one bounded family, one exact source snapshot, 26 direct declarations, 26 isolated approximations, 434 bounded sensitivity edges, and one unit. Other AsyncAPI packages named in the reports are not added. Reported tooling overlap and unresolved attribution do not establish a relationship to any governed family, campaign completeness, causal attribution, or statistical independence. The row adds no control, benign label, installation history, resolved lock, reach value, authority value, score, rank, interval, calibration result, model, or predictive metric. The no-control/no-model gate remains blocked.

### dYdX v4 client January–February 2026 admission — 27 August 2026

The strict ledger now admits `@dydxprotocol/v4-client-js@3.4.1`, `@1.22.1`, `@1.15.2`, and `@1.0.31` as one bounded npm/PyPI-context malicious-publication family. Socket and The Hacker News independently identify the exact npm version set; the PyPI release is outside the governed target.[112] [113] The official npm registry time map lists earliest affected `1.0.31` at `2026-01-27T13:22:18.888Z`; the exact one-millisecond cutoff selects retained `@dydxprotocol/v4-client-js@3.4.0` as the strict pre-event source object.[114]

The protocol now governs **33 positive package-event records in 27 incident families**, with **31 exact retained pre-event snapshots**, **200 direct declarations**, **200 isolated cutoff-valid SemVer approximations**, **1,553 bounded depth-three registry-only sensitivity edges**, and **26 future validation units**. This row adds one bounded family, one exact source snapshot, 21 direct declarations, 21 isolated approximations, 145 bounded sensitivity edges, and one unit. The reports characterize maintainer-compromise attribution as unconfirmed. Neither that context, its cross-ecosystem scope, nor the reference to a prior dYdX-related incident establishes a relationship to a governed family, campaign completeness, causal attribution, or statistical independence. The row adds no control, benign label, installation history, resolved lock, reach value, authority value, score, rank, interval, calibration result, model, or predictive metric. The no-control/no-model gate remains blocked.

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
[11]: https://donaldpinckney.com/publication/npm-follower/ "npm-follower project page"
[12]: https://github.com/ossf/malicious-packages/blob/main/osv/malicious/npm/node-ipc/MAL-2026-3744.json "OpenSSF MAL-2026-3744 node-ipc report"
[13]: https://safedep.io/malicious-node-ipc-npm-compromise/ "SafeDep node-ipc compromise report"
[14]: https://github.com/DataDog/malicious-software-packages-dataset "DataDog Malicious Software Packages Dataset"
[15]: https://safedep.io/oob-moika-tech-dependency-confusion-campaign/ "SafeDep oob.moika.tech dependency-confusion campaign"
[16]: https://github.com/ossf/malicious-packages/blob/main/osv/malicious/npm/%40emcd-vue/auth/MAL-2026-5163.json "OpenSSF MAL-2026-5163 @emcd-vue/auth report"
[17]: https://docs.deps.dev/bigquery/v1/ "Open Source Insights deps.dev BigQuery dataset"
[18]: https://doi.org/10.6084/m9.figshare.31451728 "Figshare Malicious NPM Package Detection Dataset"
[19]: https://doi.org/10.17632/6tc8wrp62g.1 "Mendeley Malicious NPM Package Detection Dataset"
[20]: https://github.com/ossf/malicious-packages/blob/c04e75e38121768f82fef0495de77b68b7054d7c/osv/malicious/npm/wenk/MAL-2025-191155.json "OpenSSF MAL-2025-191155 wenk report"
[21]: https://github.com/wiz-sec-public/wiz-research-iocs/blob/22752e7cc55ece6a053e3277b60b914e0260e65d/reports/shai-hulud-2-packages.csv "Wiz frozen Shai-Hulud second-wave IOC CSV"
[22]: https://safedep.io/mini-shai-hulud-strikes-again-314-npm-packages-compromised/ "SafeDep Mini Shai-Hulud atool incident report"
[23]: https://github.com/ossf/malicious-packages/blob/c04e75e38121768f82fef0495de77b68b7054d7c/osv/malicious/npm/amapcn/MAL-2026-4127.json "OpenSSF MAL-2026-4127 amapcn report"
[24]: https://arxiv.org/html/2604.17668v1 "Robinson et al., Original Sin of npm"
[25]: https://github.com/ossf/malicious-packages/blob/063a778886548231828c8e476eecdb5c5c04fbcb/osv/malicious/npm/is/MAL-2025-6020.json "OpenSSF MAL-2025-6020 is report"
[26]: https://www.stepsecurity.io/blog/another-npm-supply-chain-attack-the-is-package-compromise "StepSecurity is compromise report"
[27]: https://github.com/enricomarino/is/commit/0fe137a5946e4ecb0e649bd7dea48d5415a242fc "is v3.3.2 maintainer remediation commit"
[28]: https://github.com/ossf/malicious-packages/blob/88b1340754c17c3d9ae43642c9b2de22b1bbfc10/osv/malicious/npm/keyv/MAL-2026-11524.json "OpenSSF MAL-2026-11524 keyv report"
[29]: https://github.com/wiz-sec-public/wiz-research-iocs/blob/22752e7cc55ece6a053e3277b60b914e0260e65d/reports/keyv-packages.csv "Wiz frozen keyv IOC CSV"
[30]: https://www.wiz.io/blog/keyv-and-cacheable-npm-supply-chain-attack "Wiz keyv and cacheable incident report"
[31]: https://snyk.io/blog/inside-keyv-npm-compromise-preinstall-malware-trusted-provenance-ide-hooks/ "Snyk keyv compromise report"
[32]: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html "scikit-learn GroupKFold documentation"
[33]: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupShuffleSplit.html "scikit-learn GroupShuffleSplit documentation"
[34]: https://scikit-learn.org/stable/modules/cross_validation.html "scikit-learn cross-validation user guide"
[35]: https://arxiv.org/abs/2606.22593 "Santos-Grueiro, On Good Authority"
[36]: https://docs.npmjs.com/generating-provenance-statements "npm provenance documentation"
[37]: https://blog.deps.dev/npm-provenance/ "Open Source Insights npm provenance overview"
[38]: https://docs.npmjs.com/generating-provenance-statements "npm provenance documentation"
[39]: https://api-docs.npmjs.com/ "npm Registry API"
[40]: https://github.blog/security/supply-chain-security/introducing-npm-package-provenance/ "GitHub npm provenance announcement"
[48]: https://blog.npmjs.org/post/163723642530/crossenv-malware-on-the-npm-registry "npm crossenv malware notice"
[49]: https://iamakulov.com/notes/npm-malicious-packages/ "Ivan Akulov malicious npm packages account"
[50]: https://security.snyk.io/vuln/npm:crossenv:20170802 "Snyk crossenv malicious package advisory"
[51]: https://registry.npmjs.org/crossenv "npm registry crossenv metadata"
[52]: https://blog.npmjs.org/post/180565383195/details-about-the-event-stream-incident "npm event-stream incident notice"
[53]: https://snyk.io/blog/a-post-mortem-of-the-malicious-event-stream-backdoor/ "Snyk event-stream post-mortem"
[54]: https://devblogs.microsoft.com/devops/blocking-malicious-versions-of-event-stream-and-flatmap-stream-packages/ "Microsoft flatmap-stream block notice"
[55]: https://registry.npmjs.org/flatmap-stream "npm registry flatmap-stream metadata"
[56]: https://snyk.io/blog/open-source-npm-packages-colors-faker/ "Snyk colors and faker incident report"
[57]: https://www.sonatype.com/blog/npm-libraries-colors-and-faker-sabotaged-in-protest-by-their-maintainer-what-to-do-now "Sonatype colors and faker incident report"
[58]: https://research.swtch.com/npm-colors "Russ Cox colors and faker incident analysis"
[59]: https://registry.npmjs.org/colors "npm registry colors metadata"
[60]: https://registry.npmjs.org/faker "npm registry faker metadata"
[61]: https://snyk.io/blog/peacenotwar-malicious-npm-node-ipc-package-vulnerability/ "Snyk peacenotwar incident report"
[62]: https://security.snyk.io/vuln/SNYK-JS-PEACENOTWAR-2426724 "Snyk peacenotwar advisory"
[63]: https://tag-security.cncf.io/community/catalog/compromises/2022/node-ipc-peacenotwar/ "CNCF TAG Security node-ipc peacenotwar compromise catalogue"
[64]: https://registry.npmjs.org/peacenotwar "npm registry peacenotwar metadata"
[65]: https://github.com/debug-js/debug/issues/1005 "Debug maintainer incident issue"
[66]: https://www.wiz.io/blog/widespread-npm-supply-chain-attack-breaking-down-impact-scope-across-debug-chalk "Wiz Debug September 2025 incident report"
[67]: https://www.stepsecurity.io/blog/20-popular-npm-packages-compromised-chalk-debug-strip-ansi-color-convert-wrap-ansi "StepSecurity Debug September 2025 incident report"
[68]: https://registry.npmjs.org/debug "npm registry debug metadata"

[69]: https://github.com/advisories/GHSA-97m3-w2cp-4xx6 "GitHub Advisory Database: Embedded Malicious Code in node-ipc"
[70]: https://nvd.nist.gov/vuln/detail/CVE-2022-23812 "NVD: CVE-2022-23812"
[71]: https://registry.npmjs.org/node-ipc "npm registry node-ipc metadata"
[72]: https://www.sonatype.com/blog/fake-npm-roblox-api-package-installs-ransomware-spooky-surprise "Sonatype Noblox package report"
[73]: https://www.bleepingcomputer.com/news/security/malicious-npm-libraries-install-ransomware-password-stealer/ "BleepingComputer Noblox package report"
[74]: https://registry.npmjs.org/noblox.js-proxy "npm registry noblox.js-proxy metadata"
[75]: https://lottiefiles.com/blog/inside-lottiefiles/resolution-of-security-incident-with-lottiefiles-lottie-player-package "LottieFiles Lottie Player incident resolution"
[76]: https://www.sonatype.com/blog/lottie-player-compromised-in-supply-chain-attack-all-you-need-to-know "Sonatype Lottie Player incident report"
[77]: https://snyk.io/blog/lottie-player-npm-package-compromised-crypto-wallet-theft/ "Snyk Lottie Player incident report"
[78]: https://registry.npmjs.org/%40lottiefiles%2Flottie-player "npm registry Lottie Player metadata"
[79]: https://nx.dev/blog/s1ngularity-postmortem "Nx S1ngularity postmortem"
[80]: https://github.com/nrwl/nx/security/advisories/GHSA-cxm3-wv7p-598c "GitHub Security Advisory GHSA-cxm3-wv7p-598c"
[81]: https://snyk.io/blog/weaponizing-ai-coding-agents-for-malware-in-the-nx-malicious-package/ "Snyk Nx incident report"
[82]: https://www.stepsecurity.io/blog/supply-chain-security-alert-popular-nx-build-system-package-compromised-with-data-stealing-malware "StepSecurity Nx incident report"
[83]: https://registry.npmjs.org/nx "npm registry nx metadata"
[84]: https://www.sonatype.com/blog/multiple-crypto-packages-hijacked-turned-into-info-stealers "Sonatype country-currency-map hijack report"
[85]: https://www.bleepingcomputer.com/news/security/infostealer-campaign-compromises-10-npm-packages-targets-devs/ "BleepingComputer country-currency-map incident report"
[86]: https://registry.npmjs.org/country-currency-map "npm registry country-currency-map metadata"
[87]: https://github.com/advisories/GHSA-2gqj-wrf5-35w8 "GitHub Advisory Database html-to-gutenberg malware advisory"
[88]: https://research.jfrog.com/post/hijacked-npm-vscode-tasks-blockchain/ "JFrog html-to-gutenberg hijack report"
[89]: https://thehackernews.com/2026/06/hijacked-npm-and-go-packages-use-vs.html "The Hacker News html-to-gutenberg incident report"
[90]: https://registry.npmjs.org/html-to-gutenberg "npm registry html-to-gutenberg metadata"
[91]: https://www.sonatype.com/blog/hijacked-npm-package-attempts-to-deliver-polinrider-linked-rat "Sonatype common-stack generate-plugin hijack report"
[92]: https://github.com/advisories/GHSA-6p55-6hvr-3xmg "GitHub Advisory Database common-stack generate-plugin malware advisory"
[93]: https://registry.npmjs.org/%40common-stack%2Fgenerate-plugin "npm registry common-stack generate-plugin metadata"
[94]: https://www.sonatype.com/blog/sonatype-discovers-two-malicious-npm-packages "Sonatype sbx-mask incident report"
[95]: https://github.com/advisories/GHSA-r934-qgg3-v7fg "GitHub Advisory Database sbx-mask malware advisory"
[96]: https://registry.npmjs.org/sbx-mask "npm registry sbx-mask metadata"
[97]: https://community.bitwarden.com/t/bitwarden-statement-on-checkmarx-supply-chain-incident/96127 "Bitwarden Statement on Checkmarx Supply Chain Incident"
[98]: https://www.stepsecurity.io/blog/bitwarden-cli-hijacked-on-npm-bun-staged-credential-stealer-targets-developers-github-actions-and-ai-tools "StepSecurity Bitwarden CLI incident report"
[99]: https://github.com/advisories/GHSA-999x-2wm3-jfx8 "GitHub Advisory Database CVE-2026-42994"
[100]: https://registry.npmjs.org/%40bitwarden%2Fcli "npm registry Bitwarden CLI metadata"
[101]: https://www.stepsecurity.io/blog/malicious-npm-releases-found-in-popular-react-native-packages---130k-monthly-downloads-compromised "StepSecurity React Native malicious-release incident report"
[102]: https://www.aikido.dev/blog/glassworm-strikes-react-packages-phone-numbers "Aikido React Native package incident report"
[103]: https://registry.npmjs.org/react-native-country-select "npm registry react-native-country-select metadata"
[104]: https://www.aikido.dev/blog/catching-a-rat-remote-access-trojian-rand-user-agent-supply-chain-compromise "Aikido rand-user-agent incident report"
[105]: https://www.bleepingcomputer.com/news/security/supply-chain-attack-hits-npm-package-with-45-000-weekly-downloads/ "BleepingComputer rand-user-agent incident report"
[106]: https://registry.npmjs.org/rand-user-agent "npm registry rand-user-agent metadata"
[107]: https://www.stepsecurity.io/blog/joyfill-npm-supply-chain-compromise "StepSecurity Joyfill compromised npm packages report"
[108]: https://socket.dev/blog/joyfill-npm-beta-releases-compromised "Socket Joyfill PolinRider-related incident report"
[109]: https://www.aikido.dev/blog/asyncapi-npm-packages-backdoored-via-github-actions "Aikido AsyncAPI npm packages backdoored via GitHub Actions"
[110]: https://www.microsoft.com/en-us/security/blog/2026/07/15/unpacking-asyncapi-npm-supply-chain-compromise-import-time-payload-delivery/ "Microsoft Security AsyncAPI npm supply chain compromise analysis"
[111]: https://registry.npmjs.org/%40asyncapi%2Fgenerator "npm registry AsyncAPI generator metadata"
[112]: https://socket.dev/blog/malicious-dydx-packages-published-to-npm-and-pypi "Socket dYdX npm and PyPI package compromise report"
[113]: https://thehackernews.com/2026/02/compromised-dydx-npm-and-pypi-packages.html "The Hacker News dYdX npm and PyPI package compromise report"
[114]: https://registry.npmjs.org/%40dydxprotocol%2Fv4-client-js "npm registry dYdX v4 client metadata"

## Bounded dYdX Solo September 2022 admission — 27 August 2026

GitHub’s reviewed advisory and BleepingComputer independently identify `@dydxprotocol/solo@0.41.1` and `0.41.2`; bounded npm registry metadata fixes the earliest publication at `2022-09-23T10:39:42.987Z` and selects retained `0.41.0` one millisecond before cutoff.[115] [116] [117] The active cohort is 34 records, 28 families, 32 snapshots, 211 direct declarations and approximations, 1,643 bounded sensitivity edges, and 27 validation units. Companion packages, relatedness, independence, controls, installations, reach, scores, models, calibration, ranking, intervals, and predictive metrics are not inferred.

[115]: https://github.com/advisories/GHSA-xjr5-5w2w-3233 "GitHub Advisory Database, Malware in @dydxprotocol/solo"
[116]: https://www.bleepingcomputer.com/news/security/npm-packages-used-by-crypto-exchanges-compromised/ "BleepingComputer dYdX npm report"
[117]: https://registry.npmjs.org/%40dydxprotocol%2Fsolo "npm registry @dydxprotocol/solo metadata"

## Bounded TanStack History May 2026 family-member admission — 27 August 2026

TanStack and StepSecurity independently identify `@tanstack/history@1.161.9` and `1.161.12`; official npm registry metadata fixes the earliest publication at `2026-05-11T19:20:39.565Z`, and the one-millisecond cutoff selects retained `1.161.6`.[118] [119] [120] StepSecurity expressly frames this as TeamPCP Mini Shai-Hulud. Accordingly, the row is admitted to the existing `mini_shai_hulud_atool_2026` family, rather than as a new family or validation unit. The active cohort is 35 records, 28 families, 33 snapshots, 211 direct declarations and approximations, 1,643 bounded sensitivity edges, and 27 validation units. Campaign completeness, actor linkage beyond the sources, independence, controls, installations, reach, scores, models, calibration, ranking, intervals, and predictive metrics are not inferred.

[118]: https://tanstack.com/blog/npm-supply-chain-compromise-postmortem "TanStack npm supply-chain compromise postmortem"
[119]: https://www.stepsecurity.io/blog/mini-shai-hulud-is-back-a-self-spreading-supply-chain-attack-hits-the-npm-ecosystem "StepSecurity TeamPCP Mini Shai-Hulud report"
[120]: https://registry.npmjs.org/%40tanstack%2Fhistory "npm registry @tanstack/history metadata"

## Bounded @ctrl/tinycolor September 2025 exact-version exclusion — 27 August 2026

StepSecurity’s public report names `@ctrl/tinycolor` in the September 2025 Shai-Hulud event, while CISA independently records the event context; neither reviewed source supplies an independently corroborated finite exact package-version set.[121] [122] The candidate is excluded before a registry request because package-level reporting cannot establish a target version, cutoff, or retained source object. The shared campaign name alone does not establish a ledger-family assignment, actor linkage, completeness, or statistical independence. The active cohort remains 35 records, 28 families, 33 snapshots, 211 direct declarations and approximations, 1,643 bounded sensitivity edges, and 27 validation units; no controls, installs, reach, scores, models, rankings, intervals, calibration, or predictive metrics are created.

[121]: https://www.stepsecurity.io/blog/ctrl-tinycolor-and-40-npm-packages-compromised "StepSecurity September 2025 Shai-Hulud report"
[122]: https://www.cisa.gov/news-events/alerts/2025/09/23/widespread-supply-chain-compromise-impacting-npm-ecosystem "CISA September 2025 widespread npm compromise alert"

## Bounded ansi-styles September 2025 family-member admission — 27 August 2026

StepSecurity and Wiz independently identify `ansi-styles@6.2.2` in the September 2025 malicious-publish event; registry metadata fixes its publication at `2025-09-08T13:12:10.343Z` and selects retained `6.2.1` one millisecond before cutoff.[123] [124] [125] The row joins the already governed Qix family without a new family or validation unit. The active cohort is 36 records, 28 families, 34 snapshots, 211 declarations, 1,643 sensitivity edges, and 27 units; no controls or predictive outputs are created.

[123]: https://www.stepsecurity.io/blog/20-popular-npm-packages-compromised-chalk-debug-strip-ansi-color-convert-wrap-ansi "StepSecurity September 2025 affected-version report"
[124]: https://www.wiz.io/blog/widespread-npm-supply-chain-attack-breaking-down-impact-scope-across-debug-chalk "Wiz September 2025 affected-version report"
[125]: https://registry.npmjs.org/ansi-styles "npm registry ansi-styles metadata"

## Bounded backslash September 2025 family-member admission

StepSecurity and Wiz independently identify `backslash@0.2.1`; registry metadata selects retained `0.2.0` one millisecond before its `2025-09-08T13:20:31.923Z` publication.[126] [127] [128] The row joins the existing Qix family without a new family or validation unit; the cohort is 37 records, 28 families, 35 snapshots, 211 declarations, 1,643 edges, and 27 units. No controls or predictive outputs are created.

[126]: https://www.stepsecurity.io/blog/20-popular-npm-packages-compromised-chalk-debug-strip-ansi-color-convert-wrap-ansi "StepSecurity report"
[127]: https://www.wiz.io/blog/widespread-npm-supply-chain-attack-breaking-down-impact-scope-across-debug-chalk "Wiz report"
[128]: https://registry.npmjs.org/backslash "npm registry metadata"

## Bounded simple-swizzle September 2025 family-member admission

StepSecurity and Wiz independently identify `simple-swizzle@0.2.3`; registry metadata selects retained `0.2.2` one millisecond before its `2025-09-08T13:19:05.292Z` publication.[129] [130] [131] The row joins the Qix family without a new family or validation unit. The cohort is 38 records, 28 families, 36 snapshots, 212 declarations, 1,644 edges, and 27 units; no controls or predictive outputs are created.

[129]: https://www.stepsecurity.io/blog/20-popular-npm-packages-compromised-chalk-debug-strip-ansi-color-convert-wrap-ansi "StepSecurity report"
[130]: https://www.wiz.io/blog/widespread-npm-supply-chain-attack-breaking-down-impact-scope-across-debug-chalk "Wiz report"
[131]: https://registry.npmjs.org/simple-swizzle "npm registry metadata"

### OpenSearch JavaScript client admission — 27 August 2026

`162_opensearch_client_may_2026_candidate_assessment.json` admits one package-event record in one distinct `opensearch_npm_development_package_compromise_2026` family. OpenSearch and GitHub’s reviewed advisory independently name exactly `@opensearch-project/opensearch@3.5.3`, `3.6.2`, `3.7.0`, and `3.8.0`; official registry metadata fixes the earliest affected release, `3.6.2`, at `2026-05-12T00:29:34.210Z`. [132] [133] [134] The strict cutoff is therefore `2026-05-12T00:29:34.209Z`, and the all-stream retained object is `3.6.0`. The admission adds one record, family, exact snapshot, and future validation unit only. The governed totals are **39 records, 29 families, 37 exact snapshots, 218 direct declarations and isolated cutoff-valid SemVer approximations, 1,651 bounded registry-only sensitivity edges, and 28 future validation units**. It establishes no broader campaign, other OpenSearch package, control, benign label, historical installation, reach, blast-radius value, score, rank, model, interval, calibration result, or predictive metric.

[132]: https://forum.opensearch.org/t/urgent-security-notice-regarding-malicious-npm-packages/34807 "OpenSearch security notice"
[133]: https://github.com/advisories/GHSA-2qw9-7rhx-g3c9 "GitHub reviewed advisory"
[134]: https://registry.npmjs.org/@opensearch-project%2fopensearch "npm registry metadata"

### Red Hat Cloud Services Chrome admission — 27 August 2026

`163_redhat_cloud_services_chrome_june_2026_candidate_assessment.json` admits `@redhat-cloud-services/chrome@2.3.1` and `2.3.2` as one bounded row. StepSecurity and Aikido independently identify the exact pair; official registry metadata timestamps `2.3.1` at `2026-06-01T10:54:42.121Z`, fixes the cutoff at `2026-06-01T10:54:42.120Z`, and retains `2.3.0` as the all-stream source object. [135] [136] [137] Red Hat describes Miasma as Mini Shai-Hulud, so the row joins the existing `mini_shai_hulud_atool_2026` family and creates no new family or validation unit; this documents neither actor identity, campaign completeness, nor statistical independence. The governed totals are **40 records, 29 families, 38 exact snapshots, 219 direct declarations and isolated cutoff-valid SemVer approximations, 1,652 bounded registry-only sensitivity edges, and 28 future validation units**. No control, benign label, historical installation, reach, blast-radius, score, rank, model, interval, calibration result, or predictive metric is created.

[135]: https://www.stepsecurity.io/blog/multiple-redhat-cloud-services-npm-packages-compromised "StepSecurity report"
[136]: https://www.aikido.dev/blog/red-hat-npm-packages-compromised-credential-stealing-worm "Aikido report"
[137]: https://registry.npmjs.org/%40redhat-cloud-services%2Fchrome "npm registry metadata"
