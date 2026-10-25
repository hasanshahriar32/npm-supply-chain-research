# Publication figures and editable sources

Current figures are original native-vector drawings and measured plots. PDF is embedded in LaTeX, SVG is editable, and PNG is a 300 dpi preview.

| Conference figure | Stem | Contents |
|---|---|---|
| 1 | study_system | Public observations, retained counts, typed graph and exact closure engine |
| 2 | study_methodology | Six analysis, sensitivity, correctness and reporting stages |
| 3 | objective_tradeoff | Six-budget C/H curves, analytic random expectations and budget-100 hybrid/direct-P markers |
| 4 | coverage_partition | Complete-source exclusion, covered residual sources and uncovered counts |
| 5 | representation_detail | Name/version pair mass, C and H |

The journal also embeds graph_semantics, an explicitly illustrative version-splicing example. objective_mechanism remains a supplementary set example. There are eight exported figure sets in total, including the supplementary compact observation workflow, with seven shared visual sets produced by `scripts/render_publication_figures.py`.

Regenerate from the repository root:

```sh
python3 manuscript/scripts/render_research_figures.py
python3 manuscript/scripts/verify_manuscript.py
```

Source and output hashes are in `results/figure_manifest.json`, `results/publication_figure_data.json`, `results/analysis_figure_data.json` and `results/system_figure_data.json`. The original icon-based study_system architecture has been restored, together with its matching SVG and draw.io sources. The compact replacement is retained separately as observation_workflow and is not used in the paper. original_architecture/ preserves the approved original assets. No external raster imagery is used.
