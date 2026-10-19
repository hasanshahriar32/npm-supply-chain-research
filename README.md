# Maintainer Prioritization in npm Supply Chains

Our current paper is **Maintainer Prioritization in npm Supply Chains: Coverage, Exposure, and Graph Representation**. We study how a limited maintainer-review budget behaves under different defensive objectives and dependency representations.

The completed work is a reproducible structural experiment on our collected npm data. It compares review coverage, conditional exposure under an explicitly uniform account-loss scenario, and exclusion of every observed source identity. Longer-term compromise forecasting and graph learning remain research plans; no trained HGAT, credential-harvesting return, compromise probability or deployed-hardening effect is claimed.

Read the [authored paper](manuscript/main_authors.pdf), [anonymous review paper](manuscript/main.pdf), or [full research report](manuscript/research/2026-10-20_full_research_report.md). The [manuscript guide](manuscript/README.md) explains editing, builds and submission artifacts.

## Main completed findings

Our graph contains **25,228 packages**, **12,217 maintainer usernames**, **79,405 account/package relations**, and **88,113 distinct package-name dependency adjacencies**.

At a budget of 100 usernames:

| Selection objective/method | Distinct workflow-associated repositories covered | Uniform-scenario exposure reduction | Repositories satisfying all-source exclusion |
|---|---:|---:|---:|
| Greedy marginal coverage | 5,538 | 11.48% | 800 |
| Exact maintainer-union ranking | 4,407 | 33.79% | 534 |

There are 7,171 observed workflow-associated repository keys, of which 7,158 have at least one observed maintainer source. Greedy covers more distinct repositories; exact-union ranking removes more exposure under the stipulated uniform, mutually exclusive single-account-loss model. Coverage alone does not protect an endpoint against its other source accounts: **4,738 of greedy's covered repositories remain reachable through an unselected identity**.

Preserving version continuity reduces total identity/repository exposure pairs from 462,170 to 266,016 (**42.44%**), while greedy's coverage remains similar at this budget. All-root analysis finds **8,587 packages** whose projected reach changes when version identities are preserved. Repository deduplication, mapping exclusions, graph depth, identity grouping and tie order are evaluated separately.

These are measurements of the observed graph and conditional scenarios. Workflow association does not establish CI execution, accessible secrets or publishing permissions. The methods are established baselines; our contribution is the measured objective tradeoff and its representation/visibility sensitivities.

## Research status and new data collection

We implemented and executed six-budget comparisons, 200 seeded random orders, analytical random expectations, representation/visibility ablations and independent semantic checks. Outputs are in [structural_interventions/](manuscript/results/structural_interventions/) and [graph_validity/](manuscript/results/graph_validity/).

We also collected a new prospective feasibility wave: **100 uniformly sampled package names**, seed 20261020, with selection frozen before requests; **90 successful official npm metadata captures**, eight HTTP 405 and two HTTP 404 responses. No missing package was replaced.

The feature cutoff is **20 October 2026, 00:48:38.569362 Asia/Dhaka**; the 90-day follow-up ends **18 January 2027 at the same local time**. All 100 outcomes are pending. The [cohort manifest and status](manuscript/results/prospective_cohort/README.md) record the exact times, response hashes, sanitized features and limitations. This is completed acquisition groundwork, not forecast performance or a powered benchmark.

The [machine-readable status](manuscript/research/2026-10-20_research_status.json) and [groundwork assessment](manuscript/research/2026-10-20_groundwork_assessment.md) distinguish completed work from remaining outcome surveillance, historical authority reconstruction and real intervention validation.

## Reproduce the research

Run from the repository root:

```bash
python3 scripts/study_structural_interventions.py
python3 scripts/study_graph_validity.py
python3 scripts/validate_research_study.py
python3 scripts/validate_observation_semantics.py
```

These analyses use Python's standard library. They extract the original database archive into a temporary directory, open it read-only and execute no npm package code. Source archives and the historical collector are preserved unchanged. Manifests record inputs, methods, seeds and output checksums.

The complete manuscript reproduction target regenerates study outputs, runs semantic/source checks, renders figures and builds both PDFs:

```bash
make -C manuscript reproduce
```

Figure rendering additionally needs the dependency in [requirements-figures.txt](manuscript/requirements-figures.txt). A LaTeX engine with IEEEtran is required for PDF builds; committed figures let ordinary compilation proceed without rerendering.

To compile the two paper versions directly:

```bash
bash manuscript/compile.sh                  # anonymous main.pdf
bash manuscript/compile.sh main_authors.tex # named main_authors.pdf
make -C manuscript both                    # both PDFs
make -C manuscript package                 # both source ZIPs
```

Each direct compile-script invocation builds its selected entry point. Technical PDF results, including current page count, dimensions, size and fonts, are recorded in [submission_compliance.json](manuscript/results/submission_compliance.json) and [author_versions_validation.json](manuscript/results/author_versions_validation.json); regenerate them through the manuscript checks rather than relying on fixed counts in documentation.

## Project layout

| Location | Purpose |
|---|---|
| [manuscript/](manuscript/README.md) | IEEE LaTeX source, both PDFs, figures, bibliography and build tools |
| [scripts/study_structural_interventions.py](scripts/study_structural_interventions.py) | Exact portfolio/endpoint experiments, scenario objectives and sensitivities |
| [scripts/study_graph_validity.py](scripts/study_graph_validity.py) | All-root version-continuity, observation-unit and coverage diagnostics |
| [scripts/freeze_prospective_cohort.py](scripts/freeze_prospective_cohort.py) | Frozen prospective selection and sanitized current metadata acquisition |
| [scripts/research_observations.py](scripts/research_observations.py), [collect_data_v2.py](scripts/collect_data_v2.py) | Corrected lexical repository parsing and dated unavailable/error/observed workflow states for future collection |
| [data/](data/) | Immutable compressed study archives |
| [manuscript/research/](manuscript/research/) | Full report, verified literature, protocol, novelty assessment and claim/evidence records |
| [platform/](platform/README.md) | Existing research browsing/application code and earlier research artifacts |
| [research/](research/README.md), [docs/](docs/) | Earlier research plans and background; consult the current report for achieved status |

The v2 collector has local regression/response-fixture validation. No fresh GitHub workflow acquisition or live CI security test was performed. Corrected URLs do not repair old observations automatically. Future collection should use a fresh database; the original collector remains available to reproduce historical acquisition semantics.

The legacy `calculate_metrics.py` column names include `wormability`, `blast_radius` and `attacker_roi`. They are structural quantities, not measured propagation, infrastructure privilege or attacker return. An earlier cross-export consistency result remains supporting quality-control evidence, rather than the paper's main research contribution.

## Authors and submission versions

1. **Shahriar Hasan** — Department of ECE.
2. **Ashikul Islam** — Department of CSE.

Both are affiliated with **Hajee Mohammad Danesh Science and Technology University**. The order follows the supplied author record. Emails and a corresponding-author designation have not been supplied.

Use [main.pdf](manuscript/main.pdf) for the guideline's anonymous initial review. [main_authors.pdf](manuscript/main_authors.pdf) is the named working/camera-ready-preparation draft. The [full Overleaf ZIP](NPM_Supply_Chain_IEEE_Overleaf.zip) contains both entry points and author working material; the [anonymous source ZIP](NPM_Supply_Chain_IEEE_Anonymous_Source.zip) omits author records and research working notes.

**Submission-policy issue:** the supplied guideline limits LLM assistance to non-intellectual purposes, while this work used literature discovery, study design, code development, analysis, drafting and editing assistance. The disclosure states those roles. The authors must resolve this mismatch and review the work before submission; no policy compliance, similarity result, authorship approval or submission is asserted.
