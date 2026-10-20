# Full research report — 20 October 2026

**Paper:** Maintainer Prioritization in npm Supply Chains: Coverage, Exposure, and Graph Representation.

**Authors:** Shahriar Hasan, Department of ECE; Ashikul Islam, Department of CSE. Both are affiliated with Hajee Mohammad Danesh Science and Technology University, in that order.

We completed a structural measurement study, verified its nearest prior methods, executed graph and observation-unit sensitivity analyses, corrected future acquisition semantics, and collected a frozen prospective feasibility wave. The paper now reports our research directly. The completed evidence supports maintainer-prioritization tradeoffs under explicit graph and scenario assumptions; compromise prediction and real deployed-control effectiveness have not been evaluated.

## Recent changes reviewed and preserved

Before continuing, we reviewed the clean working tree and recent commits: `3303851` adds the Task 02 deep audit, `723db8d` adds research-verification reports and review workflow, and `d0c34a3` contains study/observation regression validation. The user-added [reports](../../reports/README.md) and session records remain intact.

Those reports describe the source or packaged manuscript version inspected at their recorded review time. Earlier extracted text about an artifact-consistency paper is historical evidence, not the title or contribution of the current paper. The new review findings are incorporated where supported by executable outputs. In particular, version-representation differences do not identify causal risk, depth zero means portfolio endpoints alone, and incidental overlap with an incident ledger does not validate a predictor. This report does not certify a publication tier or supply classifier metrics for a study that has no fitted classifier.

## Questions, data and observation units

Our completed questions are:

1. How does selecting maintainer identities for distinct review coverage differ from selecting them for exposure share under a fixed account-loss scenario?
2. How many covered repositories remain reachable through unselected identities?
3. How sensitive are those measurements to graph representation, workflow endpoint units, mapping evidence, depth, candidate eligibility, tie order and identity grouping?

The source archive contains **25,228 graph identifiers**, **12,217 maintainer usernames**, **79,405 identity/identifier relations**, **121,885 version-edge rows**, and **88,113 distinct projected adjacencies**. These data arise from a high-impact-seeded expansion and merged resolved graphs. They are not a random npm sample, an installation tree or a snapshot with one known acquisition cutoff.

A new scope check distinguishes **22,483 ordinary-shaped names** from **2,745 bundled-context strings containing `>`**. The context strings have **zero matching metadata rows and zero maintainer memberships** in this archive. Thus “25,228 npm packages” overstates the registry population. We retain the original identifiers in representation experiments and state their unit explicitly. Ordinary name shape alone does not independently validate current registry existence. The executable census is [check_identifier_scope.py](../../scripts/check_identifier_scope.py), with evidence in [identifier_scope.json](../results/graph_validity/identifier_scope.json). Removing all context nodes leaves **every maintainer/workflow-repository incidence set unchanged**, preserving all 462,170 primary identity/repository pairs and the `C/H/P` values for every fixed selection. Workflow-package incidence loses 28 identity/endpoint pairs, so that broader package-level result is not invariant. Context removal is a sensitivity, not a repaired dependency model or justification for aliasing strings to their leaf names.

Positive workflow observations cover **15,233 ordinary package names** and **7,171 distinct normalized repository keys**. Only **7,158** of those keys are reachable from an observed maintainer source. The primary table uses all 7,171 observed keys as its coverage denominator. A positive directory flag indicates association with an observed workflow directory; it does not establish actual execution, secrets, permission scope, trusted publishing or exploitable code.

## Literature verification and contribution

The [targeted literature extension](2026-10-20_literature_extension.md) records a review of **18 primary sources**, with URLs, dates, publication/preprint status and verification scope in [verified_sources.csv](2026-10-20_verified_sources.csv). This was a targeted search, not a systematic review or proof that no closer work exists.

The decisive novelty correction comes from [Zimmermann et al., USENIX Security 2019](https://www.usenix.org/system/files/sec19-zimmermann.pdf): maintainer footprint unions, marginal-coverage greedy and influential-maintainer vetting already appear there. [Wang's 2026 preprint](https://arxiv.org/abs/2606.14036) also studies centrality-based package protection with a different node-hardening model. We therefore make **no new optimization-algorithm claim**. The standard maximum-coverage approximation result remains prior theory, not an experimental discovery. [He et al., FSE 2025](https://arxiv.org/abs/2502.06662), on dependency-versioning defenses, further bounds claims that local version choices identify actual supply-chain protection.

The contribution is an empirical replication and extension: we separately measure coverage, fixed-scenario exposure share and all-source exclusion, then test how their tradeoff changes with workflow/repository units and version/context assumptions. Work on npm resolution, workflow security, archival collection, repository availability, release authority and temporal prediction bounds what these structural observations can support. None of those papers' experimental results has been independently reproduced here.

## Executed methods and estimands

For username `m`, let `E_m` be the distinct endpoints reached by reverse dependency traversal from its observed portfolio. Maintained seed endpoints are included. All graph unions are exact; SCC condensation and integer bitsets handle cycles. We compare:

- **Portfolio size:** rank by the number of associated packages.
- **Summed package reach:** sum each portfolio package's endpoint reach, allowing within-portfolio overlap.
- **Maximum package reach:** use the largest individual package footprint.
- **Exact maintainer union:** rank by `|E_m|`.
- **Greedy coverage:** repeatedly select the largest marginal addition to covered endpoints.
- **Uniform random:** 200 seeded orders without replacement, reusing each order across endpoint definitions.

Budgets are **1, 5, 10, 25, 50 and 100** identities. Deterministic ties follow ascending username order internally; names and individual selections are not released by the intervention outputs. The saved run plan is an exploratory local plan, not external preregistration.

The measured quantities are deliberately separate:

| Quantity | Definition | Interpretation |
|---|---|---|
| `C(S)` | Number of endpoints in the union of selected `E_m` | Structural breadth represented by selected review scenarios |
| `H(S)` | `sum_selected |E_m| / sum_all |E_m|` | Exposure share removed under uniform, mutually exclusive account-loss scenarios and ideal source hardening |
| `P(S)` | Number of endpoints whose nonempty set of observed source identities is entirely selected | All-source exclusion within the observed model |

`H` uses a fixed prior over all observed usernames: a selected origin's scenario is blocked and other origins retain their weight. It does not estimate compromise probability or model an attacker adapting to the controls. Exact-union ranking is optimal for this additive equal-cost objective by construction. Greedy approximately optimizes a different, established coverage objective. No method is claimed to optimize `P` globally. Targets with zero observed source identities are excluded from `P`.

The distinction is independently tested with a hand-derived counterexample: account footprints of sizes 4, 3 and 2 can make coverage greedy cover six endpoints while exact-union ranking covers four but removes seven rather than six identity/endpoint scenario pairs. This is an explanatory example, not an npm observation.

## Main measured results

At **100 identities**, or **0.819%** of observed usernames, the completed workflow-repository comparison is:

| Method | Covered repositories `C` | Coverage of 7,171 keys | Scenario exposure share `H` | All-source excluded repositories `P` |
|---|---:|---:|---:|---:|
| Portfolio size | 4,579 | 63.85% | 7.96% | 577 |
| Summed package reach | 4,835 | 67.42% | 21.98% | 704 |
| Maximum package reach | 4,268 | 59.52% | 33.59% | 533 |
| Exact maintainer union | 4,407 | 61.46% | 33.79% | 534 |
| Greedy coverage | 5,538 | 77.23% | 11.48% | 800 |
| Uniform random, 200-order mean | 1,680.605 | 23.44% | 0.804% | 12.78 |

Greedy covers **1,131 more keys**, a **25.66% relative increase**, than exact-union ranking at this budget. Exact-union ranking removes a larger share of the stipulated scenario exposure. These outcomes answer different allocation questions; one method cannot be declared universally superior by selecting its own objective as the only criterion.

Of greedy's **5,538 covered repositories**, **4,738 remain reachable through an unselected identity**. Only **800** satisfy the all-source exclusion condition; **6,358** of the 7,158 source-reachable repositories remain reachable from some unselected identity. None of these numbers is an observed count of prevented attacks.

At budget **25**, greedy covers **4,854** repositories, versus **4,284** for exact-union ranking and **4,067** for portfolio size. Their scenario exposure shares are **6.08%**, **9.86%** and **4.38%**. At budget 100, overlap redundancy is **89.57%** for greedy and **97.18%** for exact-union ranking, using `1 - C/sum_selected|E_m|`. Overlap has different implications for broad review and removal of several origin scenarios.

Random coverage at budget 100 has a central 95% empirical range of **659.8–2,610.65**. This is variation across seeded random selections on a fixed graph, not an ecosystem confidence interval. [Analytical expectations](../results/structural_interventions/random_analytic_expectations.csv) additionally use exact finite-population hypergeometric probabilities; simulation means need not equal those expectations exactly.

## Representation, measurement and eligibility sensitivity

| Experiment at budget 100 unless stated | Actual result | Supported conclusion |
|---|---|---|
| Exact version continuity | Identity/repository pairs fall from 462,170 to 266,016, a 42.44% difference; 2,582 identities' repository unions change | Exposure-pair mass depends substantially on retained version paths |
| Greedy selected and evaluated on version graph | `C=5,516`, `H=13.10%`, `P=817` | Aggregate coverage remains similar at this budget |
| Exact union on version graph | `C=4,479`, `H=40.59%`, `P=527` | Its objective tradeoff persists in this alternative representation |
| Package-selected greedy evaluated on version graph | `C=5,491` | Cross-representation transfer remains high at this aggregate budget |
| Depth-zero selection, evaluated on full reach | `C=5,255` | Portfolio endpoints alone are informative; depth zero has no dependency hop |
| One-hop selection, evaluated on full reach | `C=5,488`, versus full-reach selection's 5,538 | Greater depth adds coverage under this fixed evaluation |
| Select for all-package or workflow-package coverage, evaluate repository keys | `C=5,308` or `5,315`, versus direct repository selection's 5,538 | Endpoint choice changes the queue and observed coverage |
| Remove all 2,745 context nodes | Every maintainer/workflow-repository incidence set is identical; all 462,170 primary pairs retained | C/H/P are invariant for fixed selections; summed/maximum package-score ranking invariance is not established |
| Exclude 60 positive version rows with inconsistent repository targets | 24 keys removed; 7,147 retained; greedy `C=5,524`, `P=799` | Main aggregate finding survives conservative exclusion without reassigning flags |
| Exclude largest 1, 5 or 10 portfolios from selectable controls | Greedy `C=5,522`, `5,149`, `5,076` | Eligibility of dominant portfolios affects breadth; this does not classify them as bots or people |
| Hypothetical grouping by identical email hash | 12,147 groups; 67 groups contain several usernames; greedy `C=5,538`, `P=800` at 100 groups | A limited sensitivity, not validated shared credential control |
| Reverse tie order | Greedy `C=5,537`, `P=793`; `H` changes by 0.457 percentage points | Some selection-level dependence exists despite stable aggregate coverage |

The 42.44% pair difference compares denominators from two structural representations. It is **not** the fraction of real attack paths that are impossible, a causal multihop-risk reduction or an intervention effect. `H` percentages from different graph denominators are within-representation shares and cannot by themselves quantify prevented real exposure.

The separate all-root experiment finds additional projected reach for **8,587 roots**, **1,273,291 extra ordered root/reached-identifier pairs**, and a **155/253** overlap between projected and version-continuous raw-reach queues. The maximum root difference is **4,127**; checked path examples document version splicing. Both graphs still merge resolution contexts; exact version continuity alone is not joint installation feasibility or historical reconstruction.

Positive workflow packages deduplicate from **15,233 to 7,171** repository keys. Across linked observations, **1,087** repository keys serve multiple packages. Repository normalization is lexical; redirects, transfers and immutable remote identity have not been validated.

## Groundwork and data quality findings

The original parser truncates dotted repository names. A raw-key comparison finds **658 mismatched package targets**, including **60 positive version rows**; `.git` normalization gives **657**, explaining the one-record difference between the two studies. Correcting a URL does not transfer a flag to another repository. The conservative sensitivity above excludes affected positives and leaves the archive unchanged.

**3,772 graph identifiers** have only missing/NULL workflow evidence, including 2,959 without metadata. Another **6,223** have only zero flags; the old collector uses zero for both missing directories and unavailable repositories. These are observation limitations, not confirmed safety or confirmed workflow absence.

Only **14,248/32,240** dependency target-version nodes have matching metadata, and both endpoint versions have metadata in **51,427/121,885** edge rows. The collector's DIRECT/INDIRECT value describes the target node relative to the query root. Filtering to DIRECT would discard genuine adjacency and change reach for **12,993 roots**. Dependency-extraction root provenance, acquisition timestamps and resolver-error records were not retained, so we do not infer them from table names or later metric timestamps.

The earlier cross-export audit reproduces all seven database metrics but finds **17,809** workflow-reach/score disagreements with the separate CSV export. That remains quality-control evidence. Current experiments use the explicitly hashed SQLite source rather than silently mixing exports.

The incident companion contains 47 package-event rows, 31 family identifiers, 45 source-version reconstruction records and 258 declared runtime edges. Derived features and response hashes are not complete retained raw metadata or historical authority. Other user-reviewed incident ledgers contain additional assessment records with different inclusion units. Their incidental graph overlap does not provide time-aligned held-out predictions or validate this structural study as a forecast.

## Acquisition actually performed

Bounded official-source probes attempted six endpoints and obtained five HTTP 200 responses: current npm version/time metadata, a minimal version-specific deps.dev graph, an OSV version-specific malicious-package report, Zenodo release metadata and the OpenSSF source description. The historical population portal failed DNS even after a network retry. The large historical relation archive was not ingested. The [source-access records](../results/graph_validity/source_access/access_attempts.json) preserve statuses and hashes. Successful access demonstrates feasibility, not comprehensive outcome ascertainment.

The frozen new wave selected **100 graph identifiers**, seed **20261020**, before any metadata request. It contains **92 ordinary-shaped names** and **eight bundled-context strings**. Official npm `/latest` returned **90 successful metadata responses**, **two ordinary-name 404 responses**, and **eight context-string 405 responses**. No identifier was replaced. This reveals a sampling-frame defect, so the wave must not be described as 100 validated registry packages or used to estimate registry unavailability.

Allowlisted captures preserve timestamps, hashes, version IDs, public maintainer usernames, a separate recorded version-publisher field, repository keys and dependency counts. Emails, raw response bodies, install-script bodies and tarballs are omitted. Selection/capture integrity and pending labels are checked in the [frozen cohort records](../results/prospective_cohort/README.md).

The common feature cutoff is **20 October 2026, 00:48:38.569362 Asia/Dhaka**. The 90-day interval ends **18 January 2027, 00:48:38.569362 Asia/Dhaka**. **All 100 outcomes are NULL/pending.** This is acquisition-feasibility groundwork, not a powered or fully preregistered benchmark. Future package-level waves should validate their registry sampling units and freeze separate selections; the existing wave remains unchanged.

The v2 collector and repository-observation helpers are implemented and pass local parser and response-fixture checks. They preserve unavailable/error/directory-observed states and dots in repository names. **No new live GitHub workflow collection was run.** They do not retrospectively repair old flags or provide missing historical workflow commits.

## Validation and reproduction

The intervention implementation independently checks **288 BFS roots**, including large closures, and reproduces every stored reach count. All-root validity checks cover **25,228 original identifiers**, with version-continuous reached sets contained in projected sets. Source-incidence duality, repository deduplication, nested-budget monotonicity, union bounds, cycle handling and `P<=C` checks pass.

The separate [independent validation](../results/structural_interventions/independent_validation.json) uses a hand-derived coverage/exposure counterexample, a version-splicing example, cycles and isolated nodes, then **60 seeded random graphs and 675 BFS-checked roots**. Lazy greedy matches naive marginal selection, and source/protection calculations match direct set evaluation. Observation fixtures cover dotted repository names, transport forms, false-host rejection and unavailable/error/positive workflow states.

The [resource profile](../results/structural_interventions/performance_profile.json) executes the complete offline structural study in three isolated runs on one host. Wall times are **38.62, 39.32 and 40.55 seconds** (mean **39.50 seconds**, sample SD **0.98 seconds**); maximum process RSS is **1,038.43 MiB**. Each run reproduces the frozen scientific-results hash. The measured process makes **zero network requests**, executes **zero npm payloads** and calls **no LLM**; development-assistance costs are outside this measurement. These are descriptive full-process costs with uncontrolled warm caches, not cold-start benchmarks, per-package inference latency, collection cost or deployed triage cost.

From the repository root:

```bash
python3 scripts/study_structural_interventions.py
python3 scripts/study_graph_validity.py
python3 scripts/check_identifier_scope.py
python3 scripts/validate_research_study.py
python3 scripts/validate_observation_semantics.py
make -C manuscript reproduce
```

Ordinary study reproduction is offline, uses read-only temporary SQLite extraction and executes no npm package code. Statistical plots need the recorded Matplotlib dependency; the architecture uses Python-authored SVG, original technical glyphs, librsvg's `rsvg-convert`, and Noto Sans. PDF compilation needs a supported TeX engine. The Make target regenerates experiments/checks/figures and both manuscript versions, without overwriting the prospective selection or repeating source probes. Source and output hashes, code identifiers, seeds and interpretation appear in each manifest. An execution-time Git revision identifies that run's provenance; a later documentation commit is not itself a data-source change.

Use `bash manuscript/compile.sh --both` or `make -C manuscript both` for both PDFs. Current page/font/size and author-anonymity checks are recorded in [submission_compliance.json](../results/submission_compliance.json) and [author_versions_validation.json](../results/author_versions_validation.json), rather than fixed values copied into this report. The full Overleaf ZIP includes named working material; the anonymous source ZIP contains typesetting inputs with author records omitted.

## Work that remains

| Work | Actual status and next evidence |
|---|---|
| Completed structural comparison | Executed; source-bound curves and sensitivities available |
| Offline operational cost | Three isolated full-study runs; matching result hashes, 39.50-second mean and 1,038.43-MiB maximum RSS on this host |
| New capture feasibility | Executed; 90 metadata responses, measured frame defect, 100 pending outcomes |
| Registry-level next wave | Validate units, freeze a separate frame and selection; do not replace failed original selections |
| Prospective surveillance | Freeze sources, eligible incident roles, reporting delay, censoring and analysis before reviewing future outcomes |
| Outcome follow-up | Pending through 18 January 2027; no unattended surveillance task has been activated |
| Powered forecast evaluation | Not executed; assess independent event yield and precision before choosing models |
| Historical compromise forecasting | Requires time-aligned pre-event features, an at-risk frame and adjudicated documented-event coverage |
| Learned graph model | No HGAT/GNN trained or evaluated; compare transparent baselines first if valid events become available |
| Real hardening | Requires measured implemented controls and outcomes before causal or prevention claims |

A documented-event-versus-unlabeled design need not prove that every unreported package is benign. It does require a defined population, time interval, source coverage, reporting assumptions and explicit unknown/censored states. A small or zero event yield is a result to report, not a reason to change targets or relabel ordinary vulnerabilities as publisher compromise. [extended_benchmark_design.md](extended_benchmark_design.md) records the follow-up design and [research_status.json](2026-10-20_research_status.json) records the current machine-readable state.

**Submission-policy status:** assistance included literature discovery, design, code, analysis, drafting and editing. The supplied guideline restricts LLM use to non-intellectual purposes, so the acknowledgment discloses the actual roles and the mismatch remains unresolved. No similarity result, human authorship approval, policy compliance or submission is asserted.


## Code-generated figures

The current paper contains four figures explaining the implemented system, objective budget tradeoffs, covered repositories with remaining sources, and representation sensitivity. Their PDF/SVG/PNG exports and an optional illustrative C/H/P mechanism are documented in the [figure gallery](../figures/README.md). All measured marks and annotations come from the saved study outputs; the representative system graph and optional set example are explicitly schematic. `render_research_figures.py` regenerates all assets, while `figure_manifest.json` records input, code and export hashes. The figure revision changes presentation rather than the scientific results.
