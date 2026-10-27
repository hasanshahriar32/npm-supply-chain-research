# Repository review and figure assessment

Review date: 27 October 2026 (Asia/Dhaka). Scope: both current manuscript tracks, retained measurements and their generators, verification coverage, figures/captions, research protocols, and relevant platform integration. This is an evidence review, not a new literature survey, live service audit, or certification of every repository file. Manuscript content and publication archives were not changed during this review.

## Assessment

The core structural comparison is useful, and the retained baseline experiment has substantial reproducibility and independent-validation support. The journal draft nevertheless contains material numerical and interpretation errors that survive its current verifier. The conference is better qualified but also contains an endpoint mismatch in its named-maintainer example. These issues should be resolved before adding publication figures or describing either paper as ready for submission.

Re-running the existing conference and journal verifiers passes. That result does not contradict the findings below: the verifiers do not check all active numerical tables, endpoint provenance, or evidential interpretations. A passing build and matching hashes cannot validate a mislabeled measurement.

## Priority findings

### 1. Critical: active journal budget table disagrees with retained results

Location: `manuscript_q1/sections/05_empirical_results_rq1_to_rq3.tex`, inline table beginning at line 15.

Compared five deterministic methods × six budgets × C/H/P against `manuscript/results/structural_interventions/results.json`: **69 of 90 cells disagree**, using a 0.00501 tolerance for two-decimal percentages. Mismatches by budget: 1: 15, 5: 15, 10: 13, 25: 13, 50: 13; budget 100's deterministic cells agree at the printed precision. Random-column entries have additional discrepancies and are outside that 90-cell count.

For example, the inline table gives budget-one greedy coverage as 23.65% and P as 164; retained results give 2,543/7,171 = **35.46%** and **P=269**. At budget 100 the random H sample mean is **0.80%**, not the inline table's 0.82%; its P MCSE is approximately **1.42**, not 1.1.

A generated corrected table already exists at `manuscript_q1/tables/q1_multi_budget_table.tex`, produced by `scripts/reconcile_full_manuscript.py`, but it is not the active table. Replace the duplicated inline table with that input and verify every rendered cell against the underlying results, including random means and MCSEs.

### 2. Critical: named-maintainer case study mixes endpoint universes in both papers

Locations: `manuscript/sections/05_results.tex` and journal Section 5/Table 4; generators `scripts/extract_q1_temporal_and_authority_tables.py` and `scripts/reconcile_full_manuscript.py`.

Recomputed account reach from the read-only SQLite archive using the maintained portfolios, SCC closure engine, and the two separate endpoint maps:

| Measurement | Workflow-associated repositories | All linked repositories |
|---|---:|---:|
| qix reach | 1,942 | 2,971 |
| qix exact-union rank | 7 | 8 |
| sindresorhus reach | 2,543 | 4,113 |
| tootallnate reach | 2,113 | 3,238 |
| qix endpoints outside sindresorhus reach | 366 | 444 |
| qix endpoints overlapping sindresorhus OR tootallnate | 1,936 | 2,953 |

qix is beyond the first 100 greedy selections in both universes. The qualitative masking example survives, but the reported workflow counts and some ranks are mislabeled. Both case-study generators construct account sets with `repo_nodes` (all linked repositories), while the primary workflow experiment uses `wf_repo_nodes`. Individual-package reach columns use workflow endpoints, producing a mixed-universe table.

The earlier conference revision preserved the 2,971/rank-eight claim. That was an incomplete check and needs correction. Recompute version counts and all incident account rankings under the chosen endpoint definition before updating either manuscript. Do not simply change one number while retaining linked-repository ranks elsewhere.

### 3. Critical: absence of attestation acquisition is reported as absence of attestations

Locations: journal Section 7, conclusion, and `tables/q1_release_authority_table.tex`; generator `scripts/extract_q1_temporal_and_authority_tables.py`.

`platform/research/97_official_npm_provenance_attestation_access_assessment.json` explicitly records **zero requests, zero retrieved bundles, zero verification runs, and zero classified attestation states**. Its decision is `metadata_only_version_specific_attestation_access_not_established`, and it explicitly prohibits inferring that pre-event versions lack attestations. The paper's claim that 0/45 possessed provenance is unsupported. Report **not assessed / acquisition unavailable**, with a reason and denominator of assessed versions.

Likewise, the generator labels `selectedEmbeddedMaintainersPresent` as “Embedded Maintainer Signatures.” A maintainer array is metadata, not a cryptographic signature. The paper's assertion of registry PGP signatures on 100% of tarballs does not follow from this field. The availability audit also records zero classified deltas and zero authority scores, so availability cannot be presented as validated release-authority continuity or control effectiveness.

### 4. High: temporal accuracy and completeness claims exceed the retained reconstruction

Locations: journal Section 7 and temporal table; the extractor hardcodes the 99.89% figure.

The retained edge CSV has **1,848 rows: 1,841 resolved and seven `target_registry_unavailable`**. This is **99.62% resolution among retained rows**, not 99.89%, and does not measure completeness of a historical installation. Registry unavailability alone does not prove the targets were private scopes.

The manifest's 1,272 nodes are summed across roots, not a global count of unique nodes. Its 45 records contain **44 distinct (recordId, rootNode, cutoffUtc) tuples**, with `node-ipc-2026-05-14` repeated. Clarify the unit and campaign/event grouping before revising denominators.

The manifest explicitly prohibits treating this depth-three, 250-node, runtime-dependency-only approximation as a full transitive graph or using it for global downstream reach. The paper nevertheless says it captures the “true” tree and attributes downstream changes to post-incident removals. Those interpretations need removal or a separately implemented experiment.

### 5. High: reported cycle and source-multiplicity statistics are wrong

Locations: journal Sections 3, 5, 8, and conclusion.

Retained graph-validity results give:

| Quantity | Package projection | Exact-version union |
|---|---:|---:|
| Nontrivial SCCs | 82 | 68 |
| Nodes in those SCCs | 403 | 304 |
| Largest SCC | 61 | 61 |

The manuscript instead describes 82 nodes in 68 components and a largest cycle of four. It also claims mean downstream source count 3.12 and maximum 182. Retained source-cardinality histograms imply **462,170/7,158 = 64.57 sources per source-reachable repository**, with **maximum 1,502** (64.45 if all 7,171 repositories form the denominator).

Correct SCC condensation preserves reach exactly; an alleged <0.15% reach/selection change requires a clearly different graph operation or an implementation discrepancy. No supporting artifact for that alleged comparison was located in the reviewed study outputs.

### 6. High: unsupported ablation percentages and causal explanations

Journal Section 7 reports 31.8% changed historical downstream counts, depth increases of 14.2% and 1.8%, and a 250-to-500 node-cap test. The reviewed outputs and scripts do not establish these experiments. The existing baseline ablations instead include portfolio-only, one-hop and full-reach comparisons. Either identify exact executable provenance for the journal claims or remove them; new measurements require new experiments.

### 7. High: observation scope and control effects are overstated

Journal wording includes “25,228 unique npm package names,” “publisher accounts,” “verified, active” workflows, “fully defended,” “impervious,” “immunization,” and “fully measured population.” These go beyond what was collected:

- The graph includes 2,745 bundled-context identifiers, which are not separate registry package observations.
- Registry maintainer membership does not establish historical publication authority or peer review.
- The workflow signal is directory presence at HEAD, without workflow execution, lockfile inspection, permissions, or secret-access measurements.
- P is complete exclusion of observed source identities under a specified ideal control; it cannot certify deployed protection.
- Neither merged version representation nor cutoff approximation is an installed-tree ground truth.

The journal limitations also claim manifest/lockfile acquisition and highest-SemVer resolution for the main version graph, which conflates the original deps.dev version-edge union with the separate temporal companion. Use the conference's qualified definitions consistently across both tracks.

### 8. High: novelty, Pareto and operational claims need narrowing

Seven greedy scalarization settings establish an observed tradeoff curve, not a certified global Pareto frontier or a universally optimal alpha. The alpha-0.5 result retains 90.65% of the greedy coverage baseline and 92.31% of exact-union H, but no stakeholder utility or knee-selection criterion was estimated. The dedicated P rule is a heuristic without a global optimum guarantee. Replace “breakthrough,” “proving polarization,” “sweet spot,” and operational prescriptions with measured, qualified claims.

The paper says coverage optimization undermines P, although greedy P=800 exceeds exact-union P=534. Its own results require a more careful statement about different objectives. Current conclusions prescribe specific cohorts and controls without a deployed-control evaluation.

The description “inflates by 42.44%” also uses the wrong reference denominator: 42.44% is the decrease from 462,170 to 266,016; the projected total is 73.74% higher relative to the version total. Neither establishes actual exploit-path inflation.

### 9. Medium: figure captions and layout disagree with the actual plots

- Journal Section 5's budget-plot caption describes three panels C/H/P. `objective_tradeoff` has only two panels, C/H.
- Journal Section 6's weighting caption names log-portfolio weights; the rendered bars show uniform, account-sole, and package-sole measures.
- The weighting figure's strategy labels collide, its legend covers tall bars, and the P-curve annotation overlaps the plotted line. Split or redesign this figure before adding more.
- The version caption attributes removed paths to “spurious cyclic paths”; version splicing and cycle condensation are different operations.
- Existing Pareto labels need the same evidential qualification as the text.

### 10. Medium: verification passes leave scientific gaps

The journal verifier checks selected table-four strings, a small number of scalar invariants, threshold tables, figure bindings, and PDF properties. It does not verify the active budget table, temporal percentages, SCC census, attestation semantics, or caption panel content. Some expected incident values are hardcoded and reproduce the same endpoint mistake. Its description claims SQLite/table verification more broadly than the code actually performs.

Add full data-driven checks on active LaTeX inputs and denominators. Keep scientific claim validation distinct from PDF layout, archive parity, and hash checks. The existing corrected but unused budget table demonstrates why checking a generated artifact alone is insufficient.

### 11. Medium: smaller cross-track and repository consistency issues

- Conference H difference is -22.30 pp when calculated from full precision (33.78735097 minus 11.48495142). The journal uses 22.31 from subtracting rounded values. Derive once and specify the convention.
- The journal conclusion calls the prospective protocol “pre-registered,” while the conference explicitly states it was an internal exploratory plan without external preregistration.
- The platform ingestion source remains `ashik-hstu/npm-supply-chain-research` in `platform/server/researchIngestion.ts:4` and its README, despite the Git remote now using `hasanshahriar32`. Update the configured source and relevant tests/docs before relying on ingestion from the new owner. This was a static finding; no live ingestion was attempted.
- Historical research plans and completion reports contain superseded claims. Retain their historical provenance while pointing readers to a current achieved-status record; do not silently rewrite audit history.

## Figure recommendation

The conference currently has **five figures in six pages**; the journal has **eight in 17 pages**. Figure count alone is not the main limitation. Add views that expose the evidence behind overlap and sensitivity, after correcting the underlying definitions.

| Priority | Proposed figure | Reader question and evidence | Suggested placement |
|---|---|---|---|
| 1 | Source multiplicity and residual-source distribution, two panels | How many upstream identities reach a repository, and how many remain after selection? Derive from source-cardinality/remaining-cardinality histograms, with zero-source endpoints separated. Use an ECDF or log-binned distribution and residual curves. | Journal main text; possible conference replacement for the generic methodology diagram |
| 2 | Representation sensitivity matrix, C/H/P panels | What happens when selection and evaluation use different representations? Use `version_representation_curves.csv`; distinguish within-representation results from transported selections and normalize each H denominator explicitly. | Journal main text |
| 3 | Observation and sampling-frame diagram | Which identifiers are valid units, which have metadata/workflow observations, and what is excluded? Combine identifier census, missingness, and the prospective 100/92/90 selection path. Keep overlapping states in separate panels rather than a falsely additive funnel. | Journal main text or supplement |
| 4 | Robustness effect plot | Which changes matter most: endpoint units, depth, URL exclusions, tie order, portfolio exclusions, and identity grouping? Use saved ablation CSVs with explicit fixed or changing evaluation denominators. Do not invent confidence bars for deterministic values. | Journal supplement or main text if space permits |
| 5 | Incident representation comparison | How much do package reach and account ranks move? Use a dumbbell/slope plot after correcting endpoint universes; show current-snapshot associations and avoid implying pre-event prediction. | Journal supplement |

For the journal, add the first **two or three** evidence figures and repair the existing weighting figure. Consider splitting P curves and heterogeneous measures into separate figures for readability. For the conference, preserve the six-page limit and prefer replacing or combining an explanatory diagram with one compact empirical figure. Retain the user-preferred architecture. Avoid an unreadable drawing of the entire 25,228-node graph, repetitive plots of the same budget-100 comparison, or prospective performance plots before outcome labels exist.

All publication plots should have explicit endpoint universes, denominators, representation and selection/evaluation rules, readable labels at column width, consistent method colors, vector exports, and data-derived captions. Reuse the repository's native plotting workflow; raster illustration generation would not improve these scientific results.

## Recommended order of work

1. Correct endpoint maps and the active numerical tables; fix generators before regenerating derived artifacts.
2. Reconcile authority, temporal and graph claims with retained evidence; remove unsupported results and qualify operational language.
3. Expand scientific verification to cover active sources, units, denominators and derived captions.
4. Add the two highest-value empirical figures and repair the existing visual defects.
5. Rebuild PDFs and source archives, then refresh locks and the achieved-status handoff.

Detailed cell discrepancies and independently recomputed endpoint measurements are saved in `reports/19_repository_review_evidence.json`. No new empirical accuracy, control-effect, or detector-score result is claimed by this review.
