# Task 16: Acknowledgment edit and publication figure expansion

## 1. Completed request

Completed 2026-10-25T20:40:56.530398+06:00 (Asia/Dhaka). Removed the final acknowledgment sentence from the conference source shared by both versions and the corresponding named journal acknowledgment. The remaining LLM-use disclosure is retained. Expanded the conference from four to five figures, and the journal from four to eight. Rebuilt all four PDFs and all three ZIPs.

## 2. Research supporting the visual design

Reviewed primary methodological literature and visualization guidance rather than adding decorative illustrations:

- [ACM SIGSOFT general/data-science standards](https://www2.sigsoft.org/EmpiricalStandards/docs/standards) support explicit descriptions of acquisition, transformations, evaluation, and assumptions. Used this to separate the observation workflow from the analysis/validation workflow.
- [SIGSOFT Information Visualization supplement](https://www2.sigsoft.org/EmpiricalStandards/docs/supplements?supplement=InformationVisualization) recommends readable, preferably vector graphics, clear axes and annotations, proportionate encodings, and explicit logarithmic scales. Used native vectors, direct count labels, marker redundancy, and named units.
- [Zimmermann et al., USENIX Security 2019](https://www.usenix.org/system/files/sec19-zimmermann.pdf) provides the established dependency/maintainer-reach setting. Diagrams retain this distinction rather than depict a new trained detector.
- [Weeraddana et al., FSE 2024](https://rebels.cs.uwaterloo.ca/papers/fse2024_weeraddana.pdf) studies unused dependencies and CI waste. This reinforces the workflow-presence versus execution boundary in our diagrams.

The design decisions are our interpretation of those sources. All artwork is original code-generated vector geometry; no third-party figure was copied and no external raster image was added. This task is a focused presentation study, not a new exhaustive literature review or outcome experiment.

## 3. New and enhanced figures

| Figure | Change | Conference | Journal |
|---|---|---|---|
| study_system | Rebuilt as a compact observation workflow with sources, retained counts, typed relations, SCC/bitset computation, and the workflow-evidence boundary | Yes | Added |
| study_methodology | New six-stage analysis and correctness workflow: exact sets, comparison design, C/H/P, sensitivities, validation, and reporting limits | Added | Added |
| graph_semantics | New illustrative version-splicing explanation with incompatible intermediate versions and explicit reverse-reach direction | Supplement | Added |
| objective_tradeoff | Retains six-budget curves and exact random expectations; adds hybrid/direct-P markers at budget 100 and endpoint labels | Enhanced | Enhanced |
| coverage_partition | Labels all-source exclusion, covered residual exposure, and uncovered counts in every bar; states source-free exclusion | Enhanced | Added |
| representation_detail | Adds scenario H to pair mass and repository C, with version/name counts and units | Enhanced | Enhanced |

The journal retains its existing Pareto and heterogeneous-weight figures. All six shared visual sets are exported as PDF, editable SVG, and 300 dpi PNG. The conference uses five numbered figures; the version-splicing explanation is provided in the journal and supplementary assets to preserve the six-page limit.

## 4. Scientific provenance and reproducibility

`manuscript/scripts/render_publication_figures.py` implements the new visuals. The existing master figure generator now invokes it, avoiding a new external rendering dependency. `publication_figure_data.json` and `figure_manifest.json` bind assets to source/result/script hashes. Journal copies of all shared assets are checked against the same hashes.

The numerical experiment inputs and C/H/P, hybrid, residual/strict, and efficacy results are unchanged. The version-splicing topology is explicitly illustrative. Captions and in-text references were updated, and an existing journal label describing the version representation as ground truth was corrected to sensitivity representation. The older architecture drawio file remains historical; current editable layouts are the SVGs and native renderer.

## 5. Build and visual validation

| PDF | Pages | Figures | Bytes |
|---|---:|---:|---:|
| `manuscript/main.pdf` | 6 | 5 | 204,858 |
| `manuscript/main_authors.pdf` | 6 | 5 | 206,165 |
| `manuscript_q1/main_q1.pdf` | 17 | 8 | 386,151 |
| `manuscript_q1/main_q1_anonymous.pdf` | 17 | 8 | 385,959 |

Both conference versions remain exactly six A4 pages using standard IEEE formatting. The expanded journal is 17 pages. The journal abstract remains 188 words. All PDFs pass embedded-font, zero-Type-3, zero-overfull, zero-undefined-reference/citation, and zero-missing-glyph checks. Rendered conference and journal pages were visually inspected; workflow text and labels fit their boxes. Underfull boxes and font-shape fallback warnings remain.

Conference evidence verification checks 96 hashes, the 150 deterministic and 6,000 random result rows, and the five integrated figure inputs. Journal verification checks all eight figure inputs and shared-asset parity. The extracted anonymous package was compiled independently during validation. All three final archives pass CRC and exact workspace-member parity.

## 6. Saved deliverables

- Report: `reports/16_acknowledgment_and_publication_figure_expansion.md`, mirrored to `research_sessions/active_verification_track/16_acknowledgment_and_publication_figure_expansion.md`.
- Checksums and build/figure counts: `reports/16_publication_figure_artifact_manifest.json`.
- Updated PDFs: `manuscript/main.pdf`, `manuscript/main_authors.pdf`, `manuscript_q1/main_q1.pdf`, and `manuscript_q1/main_q1_anonymous.pdf`.
- Current figures and editable sources: `manuscript/figures/` and synchronized journal copies.
- Rebuilt archives: both conference source ZIPs and `NPM_Supply_Chain_Q1_Journal_Source.zip`.
- The reviewed conference lock and both verification reports are refreshed; the session ledger and report index are updated. Task 15 archives were retained under `research_sessions/active_verification_track/task16_before/`.

No submission or author approval is asserted. Existing author/venue-policy review remains separate from these completed presentation changes.
