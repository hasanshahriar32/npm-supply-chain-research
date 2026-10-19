# Task 03: Statistical Rigor, Ablations, and Operational Evidence

## 1. Execution Metadata

- **Task:** 03, continued after inspecting commits `3303851`, `723db8d`, and `d0c34a3`.
- **Audit timestamp:** 20 October 2026, 05:15:38 Asia/Dhaka, for the independent aggregate checks below.
- **Working directory:** `/home/m4x1d/Documents/research/npm-supply-chain-research`.
- **Scope:** the current structural maintainer-prioritization study, its active LaTeX sources, and the statistical/operational extension questions in `manuscript/review/NPM Research Verification and Workflow.docx`.
- **Evidence:** `manuscript/results/structural_interventions/`, `manuscript/results/graph_validity/`, `manuscript/results/prospective_cohort/cohort_status.json`, `scripts/study_structural_interventions.py`, `scripts/collect_data.py`, active `manuscript/sections/*.tex`, `manuscript/bibliography/references.bib`, verified literature records, and Reports 00–02.
- **Boundary:** this is an artifact-grounded audit, not certification of journal acceptance, ranking, novelty, or venue compliance. Classifier-specific advice from the review document is applied only where it matches the actual research question. The supplied conference guideline requires at most **six A4 pages**, including references; generic 8–12-page advice in the review document does not override it.

Read-only inspection commands included:

```bash
git log -4 --oneline
git status --short
cat reports/README.md
cat manuscript/results/structural_interventions/run_config.json
cat manuscript/results/prospective_cohort/cohort_status.json
sed -n '428,491p' scripts/collect_data.py
sed -n '252,321p' scripts/study_structural_interventions.py
rg -n '^#|^##|^###' reports/01_workspace_extraction_and_manifest_audit.md reports/02_novelty_and_dataset_hygiene_verification.md
rg -n 'given|supplied|platform|repository context|new algorithm|first|novel|forecast|Q1|benign|protect' manuscript/sections manuscript/config/metadata.tex
```

Python inspection used the standard library (`csv`, `json`, `statistics`, `collections`, `hashlib`, `zipfile`, and `xml.etree.ElementTree`). It extracted `word/document.xml` from the DOCX; grouped `random_trials.csv` by `(endpoint, budget)`; recomputed sample means and sample standard deviations for all five persisted summary measurements; checked unique `(endpoint, seed, budget)` keys; checked nested `C`, selected-pair counts, and `P`; recalculated the budget-100 differences; compared every output checksum listed in `manifest.json`; and joined candidate assessment package names to the graph's package census. The checks and their exact numerical outputs are recorded below. No network requests, model fitting, or package execution were performed by this audit.

The following exact command was executed to reproduce the primary raw-summary and output-hash checks:

```bash
python3 - <<'PY'
import csv, hashlib, json, statistics
from collections import defaultdict
from pathlib import Path
p = Path('manuscript/results/structural_interventions')
read = lambda name: list(csv.DictReader((p / name).open()))
raw, summaries = read('random_trials.csv'), read('random_summary.csv')
groups = defaultdict(list)
for row in raw:
    groups[row['endpoint'], row['budget']].append(row)
metrics = ['covered_endpoints', 'coverage_fraction_observed',
           'scenario_exposure_reduction_fraction', 'fully_protected_endpoints',
           'selected_overlap_redundancy_fraction']
errors = []
for summary in summaries:
    group = groups[summary['endpoint'], summary['budget']]
    assert len(group) == 200
    for metric in metrics:
        values = [float(row[metric]) for row in group]
        errors += [abs(statistics.mean(values) - float(summary[metric + '_mean'])),
                   abs(statistics.stdev(values) - float(summary[metric + '_sd']))]
assert len({(r['endpoint'], r['seed'], r['budget']) for r in raw}) == len(raw)
manifest = json.loads((p / 'manifest.json').read_text())
mismatches = [name for name, digest in manifest['outputs_sha256'].items()
              if hashlib.sha256((p / name).read_bytes()).hexdigest() != digest]
print(json.dumps({'random_rows': len(raw), 'seeds': len({r['seed'] for r in raw}),
                  'summary_rows': len(summaries), 'max_mean_sd_error': max(errors),
                  'output_hash_mismatches': mismatches}, indent=2))
PY
```

## 2. Quantitative and Structural Findings

### 2.1 Persisted results and the unit of replication

| Artifact | Verified rows | Interpretation |
|---|---:|---|
| `deterministic_curves.csv` | 150 | Five methods × six budgets × five endpoint/visibility definitions |
| `random_trials.csv` | 6,000 | 200 orders × six budgets × five endpoint/visibility definitions |
| `random_summary.csv` | 30 | One random summary per endpoint definition and budget |
| `random_analytic_expectations.csv` | 30 | Exact finite-population random expectations |
| `ablations.csv` | 378 | Depth, endpoint-transfer, and candidate-eligibility sensitivities |
| `version_representation_curves.csv` | 270 | Within- and cross-representation selection/evaluation results |

All 6,000 random keys are unique, and there are exactly 200 seeds. These are **not 6,000 independent graph samples**. The same sampled identity order is reused across endpoint definitions and its prefixes form the nested budgets. The five definitions are all packages, positive-workflow packages, positive-workflow repositories, linked repositories, and workflow-check-attempted packages. The last two describe observation alternatives rather than a verified positive/negative workflow classification.

All recomputed random means and sample standard deviations matched the persisted values exactly at Python floating-point precision: maximum absolute discrepancy **0**. All checked deterministic and random nested curves were nondecreasing for `C`, selected identity–endpoint pairs, and `P`. Every output checksum in the existing intervention manifest matched; **zero mismatches** were found. These checks supplement the previously executed 288-root traversal check, all-25,228 stored-count comparison, and independent 60-small-graph/675-root semantic validation; they do not turn graph nodes into independent observations.

### 2.2 Appropriate effect sizes and uncertainty

The primary comparison uses 7,171 observed positive-workflow repositories and a budget of 100 observed maintainer usernames:

| Measurement | Coverage greedy | Exact-union ranking | Greedy minus exact union |
|---|---:|---:|---:|
| Distinct covered repositories, `C` | 5,538 | 4,407 | +1,131; +25.6637% relative to exact union |
| Conditional exposure reduction, `H` | 11.4850% | 33.7874% | −22.3024 percentage points |
| All-source exclusion, `P` | 800 | 534 | +266 |

The unrounded `H` difference is calculated from persisted fractions; displayed percentages above are rounded. The three measurements answer different questions. Greedy does not dominate exact-union ranking across objectives. Exact union's advantage for `H` follows analytically from the stipulated equal-weight, equal-cost additive objective. The empirical finding is the size of the resulting tradeoff and its representation sensitivity.

The current fixed graph yields exact deterministic measurements. A Wilcoxon test across its six nested budgets, a McNemar test on `C` versus `H`, or a Cliff's delta over overlapping package/version rows would not supply valid evidence of ecosystem generalization. No such p-values or confidence intervals were fabricated. Count differences, relative differences, and percentage-point differences are suitable descriptive effect sizes here. Generalization would require an explicit sampling or repeated-snapshot design with a justified dependence unit.

For the uniform-random baseline at budget 100:

| Measurement | 200-order mean | Between-order sample SD | Monte Carlo standard error of mean | Exact expectation |
|---|---:|---:|---:|---:|
| `C`, repositories | 1,680.605 | 530.6642 | 37.5236 | 1,716.7577 |
| `H`, percent | 0.804273% | 0.372718 percentage points | 0.026355 percentage points | 0.818532% |

Monte Carlo standard errors equal the sample SD divided by `sqrt(200)`, conditional on the fixed graph and the independent seeded orders at this one endpoint/budget. They describe numerical random-baseline estimation, not uncertainty in compromise probability or the npm population. The persisted central 95% random-selection range for `C` is **659.8–2,610.65**. That range is a distribution of random selections, not a confidence interval for a population mean. The simulated and analytic means need not be numerically identical. Since the exact random expectations are available, the manuscript can use them for smooth baseline curves while retaining simulations to describe order variability.

### 2.3 Completed ablations and the remaining boundaries

| Question | Completed evidence at budget 100 | Interpretation and remaining gap |
|---|---|---|
| Does graph depth affect selection? | Portfolio-only greedy selection gives `C=5,255`; one-hop selection gives `5,488`; full-reach selection gives `5,538`, all evaluated against full reach | A controlled selection sensitivity. It does not measure what fraction of real attacks travels multiple hops. |
| Does the endpoint unit affect selection? | All-package-selected greedy evaluated on workflow repositories gives `5,308`; workflow-package-selected gives `5,315`; direct repository selection gives `5,538` | Shared repositories change the objective. These are repository keys, not independent jobs or machines. |
| Does version continuity matter? | Identity–repository pairs fall `462,170 → 266,016` (42.44%). Version-selected greedy gives `C=5,516`, `H=13.10%`, `P=817` | Both graphs still join retained resolution contexts; neither is a historical installed tree. |
| Do specific mapping errors drive the result? | Excluding 60 inconsistent positive version observations removes 24 endpoint keys; greedy gives `C=5,524`, `P=799` over 7,147 keys | Conservative exclusion, not transfer of a historical workflow flag to a corrected URL. Remote associations remain unverified. |
| Do dominant portfolios determine coverage? | Excluding the largest 1/5/10 portfolios from candidates gives `C=5,522/5,149/5,076` | Original source scenarios remain in evaluation. No identity is classified as a bot or shared credential. |
| Is greedy sensitive to ties? | Reversed ties change `C=5,538 → 5,537` and `P=800 → 793` | A useful stability check within this graph, not proof of stability over future snapshots. |
| What if equal email hashes share a control? | Hypothetical grouping gives 12,147 groups; greedy still gives `C=5,538` | Hash equality is not validated credential sharing; scenario units and denominator change. |

No learned component is fitted in the current study, so neural layer-removal or feature-drop classifier ablations are inapplicable to its present claim. More informative extensions would measure account-specific costs/weights, repeated observation times, better release-authority evidence, and repository/installation validity. Those would require additional measured inputs; assuming them would not complete an experiment.

### 2.4 Temporal evidence and prediction status

There are **zero fitted prediction models**, **zero predicted probabilities**, **zero assigned positive outcomes**, and **zero assigned negative outcomes** in the prospective pilot. All **100 outcomes remain pending**. A pre-request seeded sample of 100 identifiers yielded 90 current metadata captures, eight HTTP 405 responses for bundled-context identifiers, and two HTTP 404 responses for ordinary names. There was no outcome-based replacement.

The recorded feature cutoff is **20 October 2026, 00:48:38 Asia/Dhaka** and the 90-day endpoint is **18 January 2027, 00:48:38 Asia/Dhaka**. The timestamps are metadata-acquisition cutoffs, not evidence that historical workflow/authority features were reconstructed at that time. Surveillance sources, reporting delays, censoring, and eligibility need to be fixed before outcomes are inspected. The 100-name pilot demonstrates acquisition feasibility and supplies no power claim or predictive performance.

Accordingly, classifier precision/recall/F1, McNemar tests on paired classification errors, calibration, temporal drift performance, and false-positive alerts per 10,000 publishes are **not currently estimable**. They are future outcome-study requirements if that claim is pursued, rather than missing numbers that can be filled from current reach measurements. Historical incident-name overlap does not solve this temporal problem.

### 2.5 Operational evidence

The intervention manifest records **48.29 seconds elapsed** for its original full run with 200 random orders, including the saved pipeline's I/O, graph construction, measurements, sensitivities, and serialization. This is a single local observation, not a replicated performance benchmark. The original manifest does not record peak resident memory, isolated stage timings, or per-selection latency. No network fetch cost, analyst time, control deployment effort, causal efficacy, or false-positive burden can be derived from it.

The current continuation also completed three isolated subprocess reruns using `python3 scripts/profile_structural_study.py`. I inspected that implementation and independently checked the resulting `manuscript/results/structural_interventions/performance_profile.json`: all recorded source hashes match current files, its reference scientific-result hash matches the frozen `results.json`, the mean and sample SD recompute exactly, and the Linux RSS conversion is correct. Each rerun writes into a temporary output directory and compares its `results.json` hash with the frozen result; none overwrites the scientific study.

| Full offline rerun | Wall time | Peak RSS |
|---|---:|---:|
| 1 | 38.6228 seconds | 1,037.9297 MiB |
| 2 | 39.3189 seconds | 1,038.1094 MiB |
| 3 | 40.5491 seconds | 1,038.4297 MiB |

Mean wall time is **39.4970 seconds**, sample SD **0.9754 seconds**, range **38.6228–40.5491 seconds**; maximum observed peak RSS is **1,038.43 MiB**. The host record specifies Python 3.14.8, x86_64 Linux, and eight logical CPUs. All three reruns produced byte-identical scientific `results.json` outputs, with SHA-256 `ed1d1ae3259635168497565e373881132f60c6effc747c74ff4a2c3e1c8836e7`.

These measurements include archive extraction, graph construction, all baselines, 200 random orders, sensitivities, and serialization. They use one host with warm and uncontrolled filesystem/OS caches. They are descriptive process measurements with **zero network requests and zero npm payload executions**; the measured process makes no LLM calls. They exclude API acquisition, development assistance, analyst review, and control deployment. Dividing the total by package count would be an amortized pipeline rate, not measured per-package inference latency. No cold-start, parallel-load, registry-wide scalability, or real-world triage-cost claim follows from three repeats.

### 2.6 Qualifications to earlier review reports

Reports 01 and 02 remain historical records of the files they inspected. Their prose does not override the current sources or established measurement definitions:

1. Report 01 extracted an older nested ZIP alongside then-active sources. A freshly rebuilt current PDF/source ZIP must be validated independently; an earlier archive title, bibliography count, or short results section is not evidence that those remain current.
2. In Report 02, `depth_0` is variously called direct dependents or one-step reach. It actually means **maintained portfolio endpoints only**; `depth_1` includes one reverse-adjacency step. Moreover, the corresponding selections are evaluated on full reach. Their `H` differences do not isolate the fraction of all exposure caused by multi-hop paths.
3. The column called “Residual Pairs” in Report 02's version table was populated from `removed_identity_endpoint_pairs`. Those are selected/removed pairs, not residual pairs. Normalized `H` also uses a different total pair denominator between representations; a change in `H` does not prove that real exploit paths are false.
4. The incident overlap consists of **16 matching assessment records but 15 unique package names**; `node-ipc` appears in two assessments. Neither count is an independent pre-incident test cohort. Present-day structural overlap can motivate case studies, but cannot validate a forecast with unaligned feature times.
5. The legacy collector checks whether the GraphQL object is present/truthy; it does not require a nonempty entries list. A workflow flag does not establish execution, permissions, or secret access. The current paper uses the appropriately narrower directory/association interpretation.
6. The sample is a high-impact-seeded expansion, not the complete npm ecosystem. A top-account pair share is a concentration statistic in this observed graph. It does not mean accounts control the corresponding fraction of real incidents, or count distinct graph paths: an identity–endpoint pair is deduplicated across paths.
7. Recent bibliography alone does not establish novelty, and an arbitrary number of 2024–2025 citations is not a readiness test. The closest verified work already contains maintainer-union reach and greedy coverage. The current contribution is the measured empirical extension across objectives and graph units.

## 3. Code and Manuscript Diffs Performed

This task adds this report and its session mirror, marks Task 03 complete in the report index, and records the local ledger entry. It does **not** modify Reports 00–02, rewrite their history, change experiment code, alter archived data, assign outcomes, or change the scientific manuscript. Source review findings were sent to the manuscript integration task. That task rebuilds the current PDFs and packages separately.

The independent audit read and recalculated existing aggregates in memory. It did not rerun collectors, fit models, download or execute package payloads, or create invented prediction logs. The separate three-run offline profile is new measured evidence from this continuation, rather than evidence retroactively attributed to the original run.

## 4. Anomaly and Vulnerability Flags

| Priority | Finding | Required handling |
|---|---|---|
| High for any forecasting claim | No completed follow-up outcomes or aligned historical test population | Keep forecast accuracy/probability claims absent; finalize prospective surveillance and wait for real outcomes. |
| High for scientific interpretation | Coverage, additive exposure reduction, and all-source exclusion have different objectives | Retain all three definitions, their denominators, and ideal-control assumptions. Do not label covered endpoints protected. |
| High for statistical interpretation | Nested budgets, shared random orders, graph overlap, repeated package/campaign records | Do not count these rows as independent ecosystem samples or manufacture significance tests from them. |
| Medium | Uniform identity costs/weights and perfect controls are unmeasured assumptions | Keep results conditional; measure costs/authority before making operational effectiveness claims. |
| Medium | No common field cutoff, extraction-root provenance, workflow commits, or verified execution context | Describe both graph representations as observed unions and report missingness. |
| Medium | Sparse prospective pilot and bundled-coordinate eligibility | Resolve registry eligibility and event-yield design before claiming a benchmark with adequate power. |
| Medium | No measured review/triage/control-deployment cost | Do not convert offline graph runtime into analyst savings, false-positive burden, or cooldown efficacy. |
| Reporting | Earlier reports contain the depth, pair-column, overlap-unit, and generalization errors above | Preserve reports with this explicit qualification; use current generated tables and active-source checks. |

The active manuscript covers construct, observation/external, internal/reproducibility, and interpretation/conclusion limits in substance. Future expansion should retain those distinctions; merely adding four heading labels or classifier statistics would not supply missing empirical evidence. The venue's LLM restriction remains a separate unresolved policy question already disclosed in the paper; this audit does not certify submission readiness.

## 5. Ledger Confirmation

Task 03 is saved at `reports/03_q1_statistical_and_ablation_gap_analysis.md` and mirrored to `research_sessions/active_verification_track/03_q1_statistical_and_ablation_gap_analysis.md`. The session index records the date, paths, and completed audit findings. `research_sessions/` is already ignored by the repository; the versioned report remains under `reports/`. No earlier session ledger was present in this checkout, so the new ledger identifies earlier tasks through their existing reports rather than fabricating prior local execution entries.

## 6. Handoff Payload for Principal Research Advisor

```text
Task 03 completed against current source and persisted raw aggregates.
Verified: 150 deterministic rows, 6,000 random budget rows, 200 seeds,
30 random summaries, 30 analytic expectations, 378 ablation rows,
270 representation rows. Mean/SD recomputation discrepancy = 0;
nested C/H/P checks pass; manifest output hash mismatches = 0.

At 100 identities, greedy vs exact union:
delta C = +1,131 (+25.6637%); delta H = -22.3024 percentage points;
delta P = +266. These are fixed-graph descriptive effects.
Random C mean 1,680.605; MCSE 37.5236; exact mean 1,716.7577.
Random H mean .804273%; MCSE .026355pp; exact mean .818532%.
The random central 95% selection range is not a population CI.

Completed sensitivities: endpoint/depth, version continuity,
mapping exclusion, dominant-portfolio eligibility, email grouping, ties.
Three full offline reruns: 38.62/39.32/40.55s; mean 39.50s;
max peak RSS 1,038.43 MiB. All three reproduce frozen results.json
exactly. One warm/uncontrolled-cache host; no API/analyst/LLM cost claim.
No trained model, prediction, classification metrics, or observed
prospective outcome exists. All 100 outcomes remain pending until
follow-up; horizon ends 18 January 2027, 00:48:38 Asia/Dhaka.

Do not import Report 02's depth labels, residual-pair column label,
16-record/15-unique-name confusion, or predictive-validity inference.
Current paper is a structural empirical replication/extension.
Journal acceptance and real-world control effectiveness are unproven.
```
