# IEEE manuscript: Maintainer Prioritization in npm Supply Chains

The current paper is **Maintainer Prioritization in npm Supply Chains: Coverage, Exposure, and Graph Representation**. It reports our executed structural experiments, their observation assumptions and measured limitations. The earlier cross-export consistency audit remains supporting quality control; it is no longer the paper's central research contribution.

Read [main_authors.pdf](main_authors.pdf) for the named draft or [main.pdf](main.pdf) for anonymous review. Both use the same paper body and bibliography. The [full research report](research/2026-10-20_full_research_report.md) gives actual results, validation, literature positioning, acquired data and unfinished work.

## Scientific result and scope

We compare five deterministic maintainer-selection baselines and 200 seeded random orders at budgets 1, 5, 10, 25, 50 and 100. The objectives are distinct endpoint review coverage, exposure share under a stipulated uniform account-loss scenario, and exclusion of every observed source identity. Exact account unions and marginal-coverage greedy are established methods; the contribution is the measured objective tradeoff and its representation sensitivities.

At budget 100, greedy covers **5,538 of 7,171** workflow-associated repository keys (**77.23%**), while exact-union ranking covers **4,407** (**61.46%**). Their uniform-scenario exposure reductions are **11.48%** and **33.79%**, respectively. Only **800** of greedy's covered repositories satisfy all-source exclusion in the observed model; **4,738** remain reachable from an unselected identity. These are structural scenario results, not observed attacks prevented.

The graph contains **25,228 identifiers**, including **2,745 bundled-context strings** rather than independently registered package names. Removing those nodes preserves every maintainer/workflow-repository incidence set and C/H/P values for a fixed identity selection; it does not establish invariance of summed or maximum individual-package rankings. Preserving version continuity changes reach for **8,587 roots** and reduces identity/repository exposure pairs by **42.44%**. Neither representation reconstructs installed trees or a common historical cutoff. Workflow presence does not establish execution, credentials or publishing permission.

A frozen acquisition-feasibility wave selected 100 graph identifiers before requests: 90 ordinary-name metadata responses succeeded, two ordinary names returned 404 and eight bundled-context strings returned 405. All 100 outcomes remain pending, with 90-day follow-up ending **18 January 2027, 00:48:38.569362 Asia/Dhaka**. No GNN was trained and no forecast performance or deployed-control effect is claimed.

## Authors and manuscript versions

| Order | Author | Department |
|---|---|---|
| 1 | Shahriar Hasan | Department of ECE |
| 2 | Ashikul Islam | Department of CSE |

Both authors are affiliated with **Hajee Mohammad Danesh Science and Technology University**. Emails and corresponding-author designation have not been supplied. [submission_files/authors.json](submission_files/authors.json) and [author_details.md](submission_files/author_details.md) preserve the author record.

`main.tex` defaults to anonymous review. `main_authors.tex` enables [config/authors.tex](config/authors.tex). The named version supports author review and later camera-ready preparation; it does not imply acceptance or submission approval.

The full [Overleaf ZIP](../NPM_Supply_Chain_IEEE_Overleaf.zip) includes both entry points and author working material. The separate [anonymous source ZIP](../NPM_Supply_Chain_IEEE_Anonymous_Source.zip) omits author configuration, named PDF and research working notes. Use the anonymous PDF for the supplied initial-review guideline.

## Compile both versions

From the repository root:

```bash
bash manuscript/compile.sh                  # anonymous main.pdf
bash manuscript/compile.sh main_authors.tex # named main_authors.pdf
bash manuscript/compile.sh --both           # both PDFs
make -C manuscript both                    # both PDFs and PDF checks
make -C manuscript package                 # both source ZIPs
```

The script supports `latexmk`, Tectonic, or `pdflatex` plus `bibtex`; it copies each selected PDF from `build/` into this folder. Select an explicit Tectonic binary with `TECTONIC=/path/to/tectonic`. A standard TeX installation needs IEEEtran and the packages listed in [config/preamble.tex](config/preamble.tex). Committed figure PDFs allow ordinary compilation without Python plotting dependencies.

For Overleaf, upload the full ZIP as a new project and select `main.tex` or `main_authors.tex` as the main document. Both source ZIPs are self-contained for typesetting. Recomputing experiments additionally requires the repository's data archives; the large database is not duplicated in the writing ZIPs.

## Reproduce the executed research

```bash
python3 scripts/study_structural_interventions.py
python3 scripts/study_graph_validity.py
python3 scripts/validate_research_study.py
python3 scripts/validate_observation_semantics.py
make -C manuscript reproduce
```

The first four commands run from the repository root and use Python's standard library. The complete Make target runs the supporting archive audit, structural and validity experiments, independent semantic checks, figure rendering, source verification, both PDF builds and PDF checks. Figure rendering additionally needs [requirements-figures.txt](requirements-figures.txt): Matplotlib for charts, and the system tools librsvg `rsvg-convert` plus Noto Sans for the native SVG architecture.

The offline studies extract the original archive into a temporary directory and open SQLite read-only. They preserve source archives and the historical collector, execute no npm package code and make no network requests in their ordinary mode. Manifests bind source/code hashes, seeds, definitions and results. Optional source probes and prospective collection are separate network operations; `make reproduce` does not repeat or overwrite the frozen acquisition wave.

The future collector [collect_data_v2.py](../scripts/collect_data_v2.py) fixes lexical repository parsing and preserves unavailable/error/observed workflow states. Response fixtures and parser regression cases pass. No new live GitHub workflow collection was run, and corrected URLs do not automatically repair old flags.

## Folder structure and evidence

| Location | Purpose |
|---|---|
| [main.tex](main.tex), [main_authors.tex](main_authors.tex) | Anonymous and named IEEEtran entry points |
| [config/](config/) | Packages, title metadata and author block |
| [sections/](sections/), [bibliography/](bibliography/) | Shared paper body and references |
| [figures/](figures/), [tables/](tables/) | Vector figures and typeset tables |
| [results/structural_interventions/](results/structural_interventions/) | Six-budget curves, random trials, exact expectations and sensitivities |
| [results/graph_validity/](results/graph_validity/) | All-root graph checks, observation-unit census and source probes |
| [results/prospective_cohort/](results/prospective_cohort/) | Frozen selection, actual responses and pending outcomes |
| [research/](research/) | Full report, targeted literature review, novelty and claim/evidence records |
| [scripts/](scripts/) | Figure rendering, source/PDF validation and source packaging |
| [guideline/](guideline/), [submission_files/](submission_files/) | Supplied requirements, authorship and compliance records |

The [literature extension](research/2026-10-20_literature_extension.md) and [18-source verification record](research/2026-10-20_verified_sources.csv) establish the closest prior methods. The [research status](research/2026-10-20_research_status.json) distinguishes completed structural work from future forecasting. The [user-added audit reports](../reports/README.md) preserve their original inspected versions; their older extracted paper text is not substituted for the current source.

The GOAD example informed modular folder organization only. Scientific content, author details and results belong to our study. Earlier background documents in the root `research/` and `platform/research/` contain proposals and historical assessments; achieved status comes from the current report and executable outputs.

## Submission checks and outstanding author decisions

The paper uses the IEEE conference class, A4 paper, standard text size and two columns. The supplied [guide](guideline/guide.md) requires at most six pages including references, a PDF below 3 MB, embedded fonts without Type 3 and anonymous initial review. Current measured page counts, dimensions, sizes and fonts appear in [submission_compliance.json](results/submission_compliance.json) and [author_versions_validation.json](results/author_versions_validation.json).

```bash
make -C manuscript verify
make -C manuscript submission-check
python3 manuscript/scripts/check_author_versions.py
```

Technical checks do not certify originality, a similarity percentage, author approval or venue acceptance. [guideline_compliance.md](submission_files/guideline_compliance.md) records the remaining author-controlled requirements.

**LLM policy is unresolved:** the guide permits non-intellectual assistance, while assistance here included literature discovery, study design, code, analysis, drafting and editing. The acknowledgment discloses those roles. The authors must resolve this mismatch before submission; neither human approval nor compliance is assumed.

## Reproducible research figures

The paper includes a technical system topology and three measured analyses: budget tradeoffs, source-set partitions, and version-representation sensitivity. See the [figure gallery and source mapping](figures/README.md) for PDF/SVG/PNG previews, the [editable architecture in draw.io](figures/study_system.drawio), and the optional illustrative C/H/P mechanism.

Regenerate all figures and numeric tables with `python3 manuscript/scripts/render_research_figures.py` from the repository root, or `make -C manuscript figures`. [render_technical_architecture.py](scripts/render_technical_architecture.py) positions original [SVG infrastructure symbols](scripts/technical_icons.py), research entities, labeled connections and logical boundaries; librsvg converts the resulting SVG to vector PDF and PNG using Noto Sans. [export_drawio.py](scripts/export_drawio.py) supplies an editable diagram alongside the reproducible exports. The charts and optional objective illustration retain Matplotlib and saved research results. A game engine is unnecessary for these static publication figures.

Machine symbols describe logical collection, storage and analysis roles; they do not report measured hardware, deployed VPS instances, CI execution or publishing authority. The topology is illustrative, while its counts and result display are read from the executed experiments. [figure_design_notes.md](research/figure_design_notes.md) documents the design and reference inspection. [figure_manifest.json](results/figure_manifest.json) binds every current export to its input and renderer hashes; source verification checks those bindings and the repository partition counts. Figure generation makes no network requests.
