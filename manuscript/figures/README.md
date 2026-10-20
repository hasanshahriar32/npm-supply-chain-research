# Research figures

The current manuscript uses four code-generated vector figures. The architecture is a technical topology with original infrastructure and research-entity symbols, explicit relation types and labeled observation boundaries. Its population counts and result display come from frozen research outputs. The quantitative plots read the saved experiment rows directly. PDF is the typesetting format, SVG is editable vector source, and PNG is a 300-dpi preview. No image-generation service, stock illustration, external image asset or network request is used.

| Paper figure | Files | What it explains | Numerical source |
|---|---|---|---|
| 1. Implemented study system | [PDF](study_system.pdf) · [SVG](study_system.svg) · [PNG](study_system.png) · [draw.io](study_system.drawio) | Public observations, collection and evidence, typed graph, exact reach, budget selection and C/H/P evaluation | Population counts in the structural results and identifier-scope census; topology is explicitly illustrative |
| 2. Objective tradeoffs | [PDF](objective_tradeoff.pdf) · [SVG](objective_tradeoff.svg) · [PNG](objective_tradeoff.png) | Coverage and conditional exposure at six budgets, with five methods and the exact random expectation | `deterministic_curves` and `random_analytic_expectations` in the structural results |
| 3. Covered and remaining sources | [PDF](coverage_partition.pdf) · [SVG](coverage_partition.svg) · [PNG](coverage_partition.png) | All-source exclusion P, other covered repositories C−P, and repositories outside coverage | Budget-100 rows; bars conserve the 7,158 source-reachable repositories and exclude 13 without observed sources |
| 4. Representation sensitivity | [PDF](representation_detail.pdf) · [SVG](representation_detail.svg) · [PNG](representation_detail.png) | Total pair mass and reoptimized coverage under package projection and version continuity | Exact pair totals and within-representation budget-100 rows |
| Optional explanation | [PDF](objective_mechanism.pdf) · [SVG](objective_mechanism.svg) · [PNG](objective_mechanism.png) | A six-endpoint counterexample explaining why C, H and P differ | Computed from the declared illustrative exposure sets; this is not an observed npm subgraph |

Regenerate all five figure sets and the numeric paper tables from the repository root:

```bash
MPLCONFIGDIR=/tmp/npm-research-mpl python3 manuscript/scripts/render_research_figures.py
python3 manuscript/scripts/verify_manuscript.py
```

The focused renderers can also run independently:

```bash
python3 manuscript/scripts/render_system_figures.py
python3 manuscript/scripts/render_technical_architecture.py
python3 manuscript/scripts/export_drawio.py
python3 manuscript/scripts/render_analysis_figures.py
```

The architecture renderer [render_technical_architecture.py](../scripts/render_technical_architecture.py) writes native SVG using the original reusable paths in [technical_icons.py](../scripts/technical_icons.py). The symbols include a registry rack, API service, Git repository, database, collection workstation, maintainer, package, workflow, compute server and ranked list. [librsvg](https://gnome.pages.gitlab.gnome.org/librsvg/) converts that SVG to vector PDF and PNG through `rsvg-convert`; text uses Noto Sans. A game engine is unnecessary for this static technical drawing. The measured charts and optional illustrative objective figure continue to use Matplotlib.

[export_drawio.py](../scripts/export_drawio.py) creates [study_system.drawio](study_system.drawio), with individually movable glyphs, editable text and native connector cells. Open it in [diagrams.net](https://app.diagrams.net/) for manual layout changes. The Python-authored SVG remains the reproducible publication source: draw.io edits do not automatically update the renderer or numerical inputs. The [design notes](../research/figure_design_notes.md) explain the reference inspection, layout and scientific semantics.

For figure regeneration, install the Python dependencies from [requirements-figures.txt](../requirements-figures.txt) and make `rsvg-convert` and Noto Sans available on the system. The current architecture was exported with librsvg 2.63.3. Committed PDF figures require neither Python nor librsvg for ordinary LaTeX compilation.

The complete command also records [figure_manifest.json](../results/figure_manifest.json): source-result hashes, renderer hashes, export hashes, software versions and which figures appear in the paper. [system_figure_data.json](../results/system_figure_data.json) stores measured counts and the illustrative set definitions; [analysis_figure_data.json](../results/analysis_figure_data.json) stores the exact plotted rows and endpoint partitions. After running a focused renderer, rerun the complete command to refresh the combined manifest.

The distinction between diagram and measurement matters: machine glyphs denote logical service and analysis roles, rather than a measured inventory of physical hosts, PCs or VPS instances. Relation arrows describe structural exposure, observed maintainer links do not establish publishing authority, and workflow association does not establish execution. H assumes a fixed equal-account prior and perfect prevention of a selected source scenario. P counts all-source exclusion within that model; its gold segment is not a measured count of incidents prevented. The version graph remains an observed union, not an installed tree or historical ground truth.

Earlier `review_coverage`, `representation_sensitivity`, `artifact_comparison`, `weight_sensitivity` and `evidence_pipeline` assets are retained as historical analysis graphics; the current manuscript references the four figures above.

## System overview

![Implemented structural-measurement pipeline](study_system.png)

## Measured tradeoff

![Coverage and conditional exposure across budgets](objective_tradeoff.png)

## Covered repositories and remaining sources

![Repository source-set partition](coverage_partition.png)

## Representation effects

![Pair mass and coverage under both graph representations](representation_detail.png)
