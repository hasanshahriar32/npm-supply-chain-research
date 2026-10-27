# Maintainer Prioritization in npm Supply Chains

The [28 October journal validation revision](reports/23_journal_validation_implementation.md) adds a frozen 120-endpoint evidence audit, heuristic ablations and exact benchmarks, and a fresh 100-root acquisition. The [versioned research artifact](https://github.com/hasanshahriar32/npm-supply-chain-research/releases/tag/research-validation-2026-10-28) is public and was reproduced from a clean extraction. The journal now has four focused research questions, with exploratory material in appendices. Independent human endpoint annotations and final author approval remain pending; automated evidence is explicitly provisional.

Our current paper is **Maintainer Prioritization in npm Supply Chains: Coverage, Exposure, and Graph Representation**. We study how a limited maintainer-review budget behaves under different defensive objectives and dependency representations.

The completed work is a reproducible structural experiment on our collected npm data. It compares review coverage, conditional exposure under an explicitly uniform account-loss scenario, and exclusion of every observed source identity. Longer-term compromise forecasting and graph learning remain research plans; no trained HGAT, credential-harvesting return, compromise probability or deployed-hardening effect is claimed.

Read the [authored paper](manuscript/main_authors.pdf), [anonymous review paper](manuscript/main.pdf), or [full research report](manuscript/research/2026-10-20_full_research_report.md). The [manuscript guide](manuscript/README.md) explains editing, builds and submission artifacts. The [figure gallery](manuscript/figures/README.md) shows the code-generated system diagram and measured analyses, with editable SVG and vector PDF exports.

The [27 October reconciliation](reports/20_evidence_reconciliation_and_figures.md) corrects journal tables, workflow endpoint case-study values, temporal and provenance interpretations, and verification gaps. The conference retains six pages and five figures; the revised journal has fifteen pages and twelve figures. New journal evidence views cover source multiplicity, selection/evaluation representation, and observation units. Use this reconciliation for the corrected achieved status.

## Main completed findings

For the current journal submission, use the [EMSE manuscript](submission/emse/EMSE_Manuscript.pdf), [title page](submission/emse/EMSE_Title_Page.pdf), and [flat LaTeX source archive](submission/emse/EMSE_LaTeX_Source.zip). The revised export contains 13 active figures and the new validation results. The [EMSE guide](submission/emse/README.md) and [Report 23](reports/23_journal_validation_implementation.md) record the current outputs and remaining human-review items. Earlier page/figure counts below describe the preceding baseline revision.

Our graph contains **25,228 identifiers**, **12,217 maintainer usernames**, **79,405 account/package relations**, and **88,113 distinct projected dependency adjacencies**. The identifiers include **2,745 bundled-context strings containing `>`** and **22,483 ordinary-shaped names**. Bundled-context strings have no matching registry metadata or maintainer membership in the archive; they must not be counted as independently registered npm packages. We retain the original graph for a reproducible representation study. Removing all context nodes leaves every maintainer/workflow-repository incidence set unchanged, so repository-level C/H/P values for any fixed identity selection are unchanged; all-package endpoints have a different scope. This does not establish that summed or maximum individual-package scores retain their rankings.

At a budget of 100 usernames:

| Selection objective/method | Distinct workflow-associated repositories covered | Uniform-scenario exposure reduction | Repositories satisfying all-source exclusion |
|---|---:|---:|---:|
| Greedy marginal coverage | 5,538 | 11.48% | 800 |
| Exact maintainer-union ranking | 4,407 | 33.79% | 534 |

There are 7,171 observed workflow-associated repository keys, of which 7,158 have at least one observed maintainer source. Greedy covers more distinct repositories; exact-union ranking removes more exposure under the stipulated uniform, mutually exclusive single-account-loss model. Coverage alone does not protect an endpoint against its other source accounts: **4,738 of greedy's covered repositories remain reachable through an unselected identity**.

Preserving version continuity reduces total identity/repository exposure pairs from 462,170 to 266,016 (**42.44%**), while greedy's coverage remains similar at this budget. All-root analysis finds **8,587 identifier roots** whose projected reach changes when version identities are preserved. Repository deduplication, mapping exclusions, graph depth, identity grouping and tie order are evaluated separately.

These are measurements of the observed graph and conditional scenarios. Workflow association does not establish CI execution, accessible secrets or publishing permissions. The methods are established baselines; our contribution is the measured objective tradeoff and its representation/visibility sensitivities.

## Research status and new data collection

We implemented and executed six-budget comparisons, 200 seeded random orders, analytical random expectations, representation/visibility ablations and independent semantic checks. Outputs are in [structural_interventions/](manuscript/results/structural_interventions/) and [graph_validity/](manuscript/results/graph_validity/).

We also collected a new prospective feasibility wave: **100 uniformly sampled graph identifiers**, seed 20261020, with selection frozen before requests. The selection contains 92 ordinary-shaped names and eight bundled-context strings. The ordinary names produced **90 successful official npm metadata captures** and two HTTP 404 responses; all eight context strings produced HTTP 405. These are sampling-frame defects, not eight confirmed unavailable registry packages. No selected identifier was replaced.

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
bash manuscript/compile.sh --both           # both PDFs
make -C manuscript both                    # both PDFs
make -C manuscript package                 # both source ZIPs
```

The default compile-script invocation builds the anonymous entry point; `--both` builds both. Technical PDF results, including current page count, dimensions, size and fonts, are recorded in [submission_compliance.json](manuscript/results/submission_compliance.json) and [author_versions_validation.json](manuscript/results/author_versions_validation.json); regenerate them through the manuscript checks rather than relying on fixed counts in documentation.

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
| [reports/](reports/README.md) | User-added sequential audits, retaining the evidence and manuscript version inspected at each review |

The v2 collector has local regression/response-fixture validation. No fresh GitHub workflow acquisition or live CI security test was performed. Corrected URLs do not repair old observations automatically. Future collection should use a fresh database; the original collector remains available to reproduce historical acquisition semantics.

The legacy `calculate_metrics.py` column names include `wormability`, `blast_radius` and `attacker_roi`. They are structural quantities, not measured propagation, infrastructure privilege or attacker return. An earlier cross-export consistency result remains supporting quality-control evidence, rather than the paper's main research contribution.

## Authors and submission versions

1. **Shahriar Hasan** — Department of ECE.
2. **Md. Ashikul Islam** — Department of CSE.

Both are affiliated with **Hajee Mohammad Danesh Science and Technology University**. The order follows the supplied author record. Author emails, ORCIDs and the shared Dinajpur address are recorded in `manuscript/submission_files/authors.json`; Shahriar Hasan is first and corresponding author. A separate EMSE title page is available in `submission/emse/`.

Use [main.pdf](manuscript/main.pdf) for the guideline's anonymous initial review. [main_authors.pdf](manuscript/main_authors.pdf) is the named working/camera-ready-preparation draft. The [full Overleaf ZIP](NPM_Supply_Chain_IEEE_Overleaf.zip) contains both entry points and author working material; the [anonymous source ZIP](NPM_Supply_Chain_IEEE_Anonymous_Source.zip) omits author records and research working notes.

The acknowledgment thanks the package maintainers, open-source community and public data resources used in the study. The supplied guideline's LLM disclosure requirement and restriction to non-intellectual assistance remain unresolved in the [author-side compliance record](manuscript/submission_files/guideline_compliance.md). No policy compliance, similarity result, authorship approval or submission is asserted.
