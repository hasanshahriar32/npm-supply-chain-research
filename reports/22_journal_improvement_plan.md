# Journal improvement plan — 27 October 2026

Status: proposed work, not executed experiments. Target: strengthen the corrected journal manuscript for Empirical Software Engineering (EMSE). This plan does not change the manuscript, collect new observations, publish artifacts, or submit anything.

The priority is stronger empirical validation and a sharper contribution. The existing numerical reconciliation, twelve figures, source package, and PDF checks provide a useful foundation. Additional cosmetic editing has less value than establishing whether the observation proxies and selection conclusions withstand independent scrutiny.

EMSE welcomes original and replicated empirical studies and emphasizes practical relevance and reproducibility; a new algorithm is not a prerequisite. This plan is our research recommendation, not an additional list of journal requirements. See the [journal scope](https://link.springer.com/journal/10664/aims-and-scope) and [submission instructions](https://link.springer.com/journal/10664/submission-guidelines), checked 27 October 2026.

**Recommended scope and order**

| Priority | Work package | Main question it answers | Completion evidence |
| --- | --- | --- | --- |
| P0 | Freeze the revised protocol and contribution claims | What is new, what is being tested, and what would change our conclusion? | Dated protocol, claim-to-evidence matrix, immutable baseline hashes |
| P1 | Audit repository mappings and workflow evidence | How credible is the workflow-associated endpoint definition? | Frozen probability sample, dated evidence, human-reviewed labels, uncertainty and unknown-state accounting |
| P1 | Re-evaluate selections on audited endpoints | Do the original comparisons survive stricter endpoint definitions? | Paired C/H/P results with explicit denominators and missingness bounds |
| P1 | Benchmark and ablate the exclusion heuristic | Is its improvement robust to its arbitrary implementation choices? | Component ablations, tie sensitivity, candidate-restricted exact benchmarks |
| P1 | Restructure the manuscript around completed evidence | What should a reader learn beyond existing reach/vetting work? | Revised research questions, focused results and discussion, exploratory material moved to supplement |
| P2 | Independently reacquire a second graph snapshot or cohort | Are the main patterns specific to the retained acquisition? | New immutable acquisition, provenance, comparable and full-population analyses |
| P1 | Release reproducible artifacts and finish submission checks | Can an outsider reproduce the reported comparisons? | Clean-environment reproduction, public versioned release, synchronized submission files |

Minimum meaningful revision: finish P0 and the P1 work packages. Preferred stronger EMSE revision: also complete P2. If access or time makes P2 infeasible, state the remaining single-acquisition limitation and narrow the conclusions; repeated analysis of the same archive is not independent replication. Neither route guarantees acceptance.

**1. Freeze the protocol and clarify the contribution**

Create `manuscript_q1/protocols/revision_validation_protocol.md` and `manuscript_q1/protocols/revision_claim_matrix.csv` before new sampling or inspection. Record the protocol date, revision version, source/code hashes, endpoint definitions, candidate populations, strata, sample sizes, seeds, labeling rules, planned comparisons, and deviations. Describe it as a prospective protocol for the new validation work, not retrospective preregistration of completed analyses.

Use the following contribution structure as a proposal:

1. A measured account of the tradeoff between coverage C, additive scenario exposure H, and all-source exclusion P at equal budgets.
2. Evidence about how much representation and endpoint observation choices change selection and evaluation.
3. An evaluated exclusion-oriented heuristic, with transparent limitations and an artifact that permits independent replication.

Treat standard submodularity results, additive ranking optimality, and scalarization as theoretical foundations. Exact union winning its own additive objective is expected; the empirical findings of interest are the size and consequences of the accompanying tradeoffs. Do not advertise a novel coverage algorithm or a universally optimal alpha.

Update the closest-work comparison using primary papers, starting with Zimmermann et al. (2019), Zahan et al. (2022), and directly relevant dependency-resolution and CI studies already cited. For each closest paper, record population, observation dates, endpoints, maintainer semantics, objective, baselines, version treatment, validation, and the specific additional finding our study tests. Verify every new novelty statement against those papers; do not assume that changing the dataset year establishes novelty. A publication/preprint label and each cited incident claim also need accurate primary-source support.

Completion: every proposed headline claim has an existing result or a named planned experiment; assumptions and future-work statements are marked as such. There is no acceptance criterion requiring favorable results.

**2. Audit the endpoint observation proxies — highest priority**

Existing entry points: `scripts/research_observations.py`, `scripts/collect_data_v2.py`, `scripts/study_graph_validity.py`, and the workflow-repository endpoint map in `scripts/study_structural_interventions.py`.

Important implementation gap: `collect_data_v2.py` logs dated directory observations and response hashes. It still queries HEAD for a directory listing. It does not retain workflow YAML, immutable commit IDs, lockfiles, or the evidence necessary to establish installation. Implement a separate audit collector rather than treating the existing collector as having those capabilities.

Proposed sampling design:

- Unit: a unique normalized repository endpoint, preserving its full list of associated package/version observations and any monorepo package paths.
- Primary audit frame: the 7,158 original workflow endpoints with observed source identities. Freeze the frame before requests.
- Initial target: 120 endpoints, sampled randomly without replacement within four original source-count strata: 1, 2–5, 6–50, and greater than 50 sources; target 30 per stratum. Check stratum sizes first. Census any smaller stratum and freeze a documented redistribution rule before drawing the sample.
- This is a feasible diagnostic target, not a statistical power guarantee. For context, a simple random sample of 120 has an approximate worst-case 95% margin near nine percentage points for a proportion; the actual stratified design and nonresponse determine the reported precision.
- Record each stratum size and inclusion probability. For an overall estimate over this frame, weight stratum estimates by their population shares. The equally allocated pooled sample percentage is not the population estimate.
- Audit the 13 source-free endpoints separately if feasible. Optionally inspect up to 20 known mapping disagreements as a diagnostic case series. These purposive cases must not be pooled into the probability-sample estimate unless their inclusion probabilities and overlap are correctly handled.
- Preserve selected failures and inaccessible repositories. Do not replace them with easy-to-fetch successes. Record response status, retry policy and final unknown states.

For each sampled endpoint, retain the original observation, retrieval time in UTC, requested and resolved URL, immutable commit SHA, package/version mapping evidence, relevant package path, workflow paths and hashes, lockfile path/type/hash, and evidence excerpts or redistributable source files. A single verified package mapping does not validate every package assigned to a monorepo; retain mapping-level labels and define how they yield an endpoint label.

Resolve a commit once and fetch all relevant files at that commit. Current audits support a current-time validation statement. They cannot certify that an undated historical HEAD observation was correct. Historical checks require an identifiable historical commit/version and explicit evidence; unavailable historical evidence remains unknown.

Use separate labels rather than a single broad "verified CI" flag:

| Label | What it establishes | What it does not establish |
| --- | --- | --- |
| `repository_mapping_supported` | Package/version evidence supports the repository and relevant package path | Historical publication authority |
| `workflow_file_present` | A workflow file exists at the recorded commit | That the workflow ran |
| `install_directive_observed` | A workflow or resolved reusable action contains an npm/yarn/pnpm installation directive, with working directory and conditions recorded | Successful installation or execution on every run |
| `lockfile_present` | A relevant lockfile is available at that commit | That every job used it |
| `dependency_version_supported` | The manifest/lockfile supports a particular dependency/version relationship | Actual vulnerable-code execution or secret access |
| `unknown_or_unresolved` | Evidence cannot settle the label | A negative or safe outcome |

Account for reusable workflows, composite actions, monorepos, conditional jobs, generated dependencies and unavailable referenced actions. Use the actual evidence level in the manuscript. Read public metadata and source files; no package installation or payload execution is needed for this audit.

Two human reviewers should independently label the probability sample if available, blinded to algorithm selections and incident associations as far as practical. Save initial labels, disagreements and their resolution. Report raw agreement, a confusion table and, where informative, a chance-adjusted agreement measure. If only one reviewer is available, report a single-reviewer audit; automated or AI checks are not a second independent human annotation. Record actual contributions after the work occurs.

Proposed outputs:

- `manuscript_q1/protocols/endpoint_audit_sample.csv`
- `scripts/collect_endpoint_validation.py`
- `manuscript_q1/results/endpoint_validation/evidence_manifest.json`
- `manuscript_q1/results/endpoint_validation/labels_initial.csv`
- `manuscript_q1/results/endpoint_validation/labels_adjudicated.csv`
- `manuscript_q1/results/endpoint_validation/summary.json`

Completion: every selected endpoint has a terminal evidence state, provenance and reviewed labels; unknown observations remain in the denominator accounting. Report stratified estimates with design-appropriate intervals, together with conservative bounds treating unresolved cases as supported versus unsupported. No arbitrary 90% pass rate is required. Poor mapping support would require repairing the endpoint definition or reducing claims.

**3. Re-evaluate the conclusions using the audit**

Implement `scripts/study_validated_endpoints.py` using the retained graph engines. Keep all maintainer identities and original source memberships; restrict the evaluation endpoint masks according to the audited labels. Do not create apparent all-source exclusion by deleting unverified source accounts.

Predefine nested or explicitly overlapping endpoint definitions, such as mapping-supported repositories; mapping-supported repositories with workflow files; and mapping-supported repositories with static installation evidence for the relevant package path. Record why an endpoint qualifies. Lockfile availability can supply a further diagnostic, but a sample of lockfiles cannot validate every transitive path in the retained graph.

Primary analysis: evaluate the original frozen maintainer selections on each audited endpoint definition at budgets 1, 5, 10, 25, 50 and 100. This tests transport of the original conclusions. Reoptimizing rankings on the audit subset is a separate exploratory analysis and must be labeled accordingly.

Report C counts and shares, P counts and shares over nonempty-source endpoints, and H using the total account–endpoint pair mass of the same evaluation universe. All compared methods in a row must share denominators. Include sample sizes, eligible counts, unresolved cases and the source-count distribution. Do not compare an H percentage from one endpoint universe directly with another as though the denominator were unchanged.

Distinguish conditional audited-subset results from estimates for the full 7,158-endpoint frame. If estimating full-frame quantities, use recorded inclusion probabilities: weighted endpoint totals for C/P and an explicitly described weighted numerator/denominator ratio for H, with design-aware uncertainty. Missing validation labels need sensitivity bounds, not automatic exclusion. For a ratio such as H, treating all unresolved endpoints as included versus excluded supplies two scenarios, not necessarily its mathematical bounds; compute valid bounds over the allowed assignments or explicitly label the results as scenario sensitivity. No estimate from this audit establishes npm-wide representativeness.

Show paired method differences within the same dataset/endpoint universe. Keep Monte Carlo uncertainty from randomized ranking separate from uncertainty due to sampling. Nested budgets are correlated evaluations, not independent observations; 200 random orders are not 200 independently collected ecosystems.

Completion: publish all planned comparisons, including reversals or inconclusive results. If the coverage/exposure tradeoff persists, quantify its size and limits. If it weakens, revise the headline claim to specify the conditions under which it holds. Avoid selecting only favorable strata, budgets or endpoint definitions.

**4. Evaluate the exclusion heuristic more rigorously**

Relevant code is currently duplicated in `scripts/study_q1_pareto_and_weights.py` and `scripts/study_q1_quorum_and_oct2026.py`. For new experiments, extract a shared, parameterized selection routine with an explicit equivalence check against the retained baseline before adding variants. Preserve the baseline artifacts and record any discovered discrepancy rather than silently regenerating historical evidence.

Predefine these component ablations:

- Full existing lexicographic rule: immediate completions, reciprocal remaining-source score, coverage tie-break and deterministic identity tie-break.
- Immediate-completion-only variant, with a fully specified fallback when all completion gains are zero.
- Remove the reciprocal-score component while retaining the remaining tie rules.
- Remove the coverage tie-break.
- Candidate remaining-source cap sensitivity: 1, 5, 10, 20 and no cap, with the same fallback rule. Cap 10 is the current setting, not a fitted optimum.
- Randomized tie-breaking for eligible tied candidates, using a fixed list of 30 seeds. Report selection variability descriptively.

Compare against the existing portfolio, summed/max reach, exact-union, greedy-coverage and random baselines. Report C/H/P and runtime/memory under the same budgets. Use supported observations; do not introduce expensive new centrality baselines merely to increase the method count.

Add exact benchmarks on tractable instances, for example 20 candidate accounts and budgets 1, 3 and 5, where exhaustive enumeration is feasible. Include documented synthetic overlap patterns and candidate-restricted empirical cases drawn by a frozen rule. Preserve complete endpoint source sets: accounts outside the candidate pool remain unselected and prevent P completion when applicable. Never intersect source sets with the candidate pool to make exclusion artificially easy. Include zero-optimum cases and report absolute gaps when ratios are undefined.

The resulting optimum is conditional on the stated candidate pool and instance. It supplies no full-graph optimality certificate. Record exact objective values, heuristic gaps, eligible candidates, source-set construction, seeds and instance provenance. Do not extrapolate small-instance approximation ratios into a new theorem.

Proposed outputs: `scripts/study_exclusion_heuristic_validation.py`, `manuscript_q1/results/heuristic_validation/ablations.csv`, `exact_instances.json`, `exact_comparison.csv` and `manifest.json`.

Completion: explain which components matter and how often the heuristic falls short on the benchmark instances. If simple variants perform similarly, simplify the method and reduce algorithmic novelty claims. An honest negative result still improves the paper.

**5. Optional stronger evidence: independently reacquire a second snapshot or cohort**

Choose and freeze one design before collection:

- Practical first choice: reacquire the baseline seed population in a new dated observation window, preserving failures and removals. This is a temporal repeat with new observations, not an independent random sample of npm.
- Stronger external-validity alternative: define an accessible broader sampling frame, randomly select seeds with recorded probabilities, then independently collect their dependency and repository observations. A new seed frame still needs a precise target population; it does not automatically make dependency-expanded nodes a registry-wide random sample.

Use a fresh database and immutable release directory. Capture start/end acquisition times and per-observation timestamps, explicit version IDs, API outcomes, source identity states and the stricter repository observations. The corrected collector is a starting point, not a complete replication protocol. Acquire dependencies and maintainer memberships again where these are part of the claim; refetching only workflow flags does not create a second graph snapshot.

Refactor new-study runners to take the input archive and output directory as arguments and derive population totals. The current Q1 scripts contain `N_WF_TOTAL = 7171` and baseline-specific assumptions; reusing them unchanged on a new population would be wrong. Do not overwrite `data/npm_ecosystem.db.zip` or the baseline result directory.

Evaluate both complete observed populations and a clearly defined common population. Report acquisition/missingness differences, C/H/P curves, paired method contrasts, source-count distributions, pair mass, and top-k set overlap. A stable-population comparison can restrict eligible maintainer accounts and endpoints to their intersection while retaining full observed source sets; sources outside the eligible account set remain unselected. Report how entry/exit and new source memberships affect P rather than silently discarding them. Evaluate name and exact-version representations within each snapshot and retain explicit denominators.

Two collection windows support a descriptive stability check, not a population confidence interval across time. A disjoint seed sample, a new timestamp and a different ecosystem test different generalization questions; describe the design actually executed.

Completion: a provenance-complete independent acquisition and honest reporting of stability or instability. If collection cannot be completed under a fixed, documented request budget, report the achieved cohort and narrow the study; do not reuse the original graph and call it replication.

**6. Restructure the manuscript after results are known**

Proposed revised research questions:

1. At equal account budgets, how large are the observed tradeoffs among coverage, additive exposure and all-source exclusion?
2. How do graph representation and validated endpoint definitions change those conclusions?
3. How robust and effective is the exclusion-oriented heuristic relative to simpler variants and tractable exact benchmarks?
4. If an independent acquisition is completed: which findings persist across the specified snapshots or cohorts?

If package 5 is not completed, use three core questions. Do not present an unexecuted replication as RQ4 results.

| Existing source | Planned revision |
| --- | --- |
| `sections/00_abstract.tex` | State the revised study design and strongest measured findings; include audit/replication results only after completion; keep within 150–250 words. |
| `sections/01_introduction.tex` | Lead with the objective/measurement problem and precise new evidence; shorten the incident catalog; replace five diffuse questions with the completed questions above. |
| `sections/02_related_work.tex` | Make the closest-work comparison specific and evidence-backed; shorten broad surveys; distinguish empirical extension from new optimization theory. |
| `sections/03_data_and_graph_construction.tex` | Add observation dates, audit sampling and labeling, response accounting, and any independent acquisition. Preserve the distinction between identifiers, packages and repository endpoints. |
| `sections/04_objectives_and_optimization_framework.tex` | Keep C/H/P assumptions explicit, shorten standard derivations, specify heuristic parameters and planned comparisons. Add an algorithm box only if it improves reproducibility. |
| `sections/04a_ai_assistance.tex` | Retain an accurate disclosure and update it if the actual workflow changes. |
| `sections/05_empirical_results_rq1_to_rq3.tex` | Center measured tradeoffs, representation effects and validated-endpoint results. Rename "Real-World Compromise Case Study" to reflect cross-sectional incident-associated illustrations. Correct residual references to 25,228 "packages" and the main observed version graph as a "SemVer dependency graph." |
| `sections/06_pareto_and_heterogeneous_results_rq4.tex` | Add heuristic validation. Keep scalarization/weights only where they reveal a consequential choice; move arbitrary threshold variants and the uniform efficacy multiplier to supplementary material unless independently justified. |
| `sections/07_temporal_authority_and_prospective_design_rq5.tex` | Move the incomplete prospective protocol and detailed metadata-feasibility tables to a supplement or a short limitations/future-work passage. Pending outcomes do not become a completed validation experiment. Preserve the original prospective record unchanged. |
| New focused Discussion section | Explain what a practitioner can infer under each objective, when conclusions change, and what measurements would be needed for operational recommendations. Avoid claims that the measured rankings prevent real attacks. |
| `sections/08_threats_to_validity_and_ethics.tex` | Replace limitations actually addressed with measured audit results, while retaining residual sampling, timing, identity, missingness and execution limits. |
| `sections/09_conclusion.tex` | Answer the completed questions and scope each result to its supporting evidence. |
| `sections/10_declarations.tex` | Insert actual release access details after publication; retain confirmed funding/interests and actual authorship information. |

Figures should support the new evidence. Add an audit outcome/missingness figure and a paired robustness-effect figure; add a heuristic-gap panel if it communicates more than a compact table. Move redundant diagrams and exploratory sensitivity plots to the supplement as needed. There is no target figure count or page count. Preserve the preferred architecture figure if it remains useful. Use vector, data-generated plots and show denominators. Confidence bars belong only to a stated inferential design, not deterministic fixed-graph curves.

Completion: the abstract, introduction, results and conclusion tell the same story. Every core research question has completed evidence. Existing results that are moved remain available in the supplement and artifact with their original provenance.

**7. Reproduction, release and final acceptance criteria for this revision**

Create a versioned research release containing the retained observations needed for offline reproduction, audit frame and labels, permitted evidence files or reproducible acquisition references, scripts, environment specification, seeds, definitions, generated tables/figures, and a manifest. Document any redistribution restrictions or exclusions and their consequences. Keep credentials and unrelated personal files out of the release. Publishing the whole working repository is not required to make the research artifact useful.

An independent clean-environment run should reproduce the main tables from released inputs without live API calls. Verify the public release while logged out; cite its actual version/URL or persistent identifier. A DOI is useful if the chosen archive provides one, but never insert an anticipated identifier as though it resolves.

Extend the existing scientific checks for sample-frame uniqueness, recorded inclusion probabilities, no replacement of failed observations, evidence-to-label links, label counts/unknown states, endpoint masks, full source-set preservation, denominator consistency and complete scenario exports. Use small exact instances to test the new heuristic runner. Check newly generated active tables against machine-readable outputs and ensure inconvenient outcomes are not dropped.

Relevant existing verification/build entry points:

```sh
python3 scripts/verify_reconciled_papers.py
python3 -m unittest discover -s scripts/tests -p 'test_*.py'
bash manuscript_q1/compile_q1.sh
bash manuscript_q1/compile_q1.sh main_q1_anonymous.tex
python3 manuscript_q1/scripts/verify_manuscript_q1.py
python3 manuscript_q1/scripts/package_q1.py
python3 submission/emse/build_emse.py
```

Adapt figure-count and active-input assertions when the approved paper structure changes: the current journal verifier and EMSE builder expect twelve figures. Validate the active input tree and a reviewed manifest instead of retaining a stale count or scanning inactive source files. Update provenance records only after the new outputs pass their data-driven checks. Conference artifacts stay bound to the existing lock unless a separate conference revision is requested.

The revision is complete when the protocol, audit, robustness/heuristic results, focused paper, and reproducible public artifact are present and mutually consistent. A positive finding is not required. Actual author contributions and both authors' final approval must be established by the authors. Finally correct the portal city/qualification fields, upload the synchronized title page/source/reference PDF, and inspect the regenerated Editorial Manager PDF.

If the paper is still a portal draft, revise it before approval. If it has already been formally submitted, use the journal's revision/editorial process for changes; do not create a second overlapping submission. No editor communication is authorized by this plan.

**Decision points and scope control**

- After protocol review: freeze the research questions, estimands and audit design before examining new labels.
- After endpoint audit: decide whether to retain, repair or narrow the workflow-endpoint interpretation, based on evidence rather than a desired pass threshold.
- After heuristic validation: keep a methodological contribution only to the extent the results support it; otherwise emphasize the empirical comparison and simplify the method.
- After the independent-acquisition feasibility check: execute the frozen replication design or explicitly retain a single-acquisition scope.
- After the evidence is complete: revise text and figures once, reproduce from released inputs, and stop adding experiments without a specific unresolved question.

Do not add a GNN/ML prediction model, more incident anecdotes, a sweeping cross-ecosystem study, extra significance tests on dependent budget rows, or additional decorative figures to manufacture novelty. A forecasting study would need its own adequate outcome data, controls, leakage prevention and evaluation design. The existing 100 pending outcomes do not establish that foundation, and waiting for their horizon alone does not guarantee enough events for a useful model.

The immediate next action is package 1: freeze the revised contribution and validation protocol. Then implement the endpoint audit while preparing the offline heuristic benchmarks. Data collection and empirical changes remain future work until separately carried out.
