# Research and manuscript validation — 20 October 2026

The current paper reports completed maintainer-prioritization experiments in our npm graph. The earlier artifact-consistency audit remains supporting quality control. The user-added Reports 01–02 are preserved; [Task 03](../../reports/03_q1_statistical_and_ablation_gap_analysis.md) qualifies their interpretation and records current statistical/operational evidence.

| Check | Actual result |
|---|---|
| Frozen scientific input/output and figure evidence | 65 hashes checked; no mismatches |
| Deterministic/random grids | 150 deterministic and 6,000 random budget rows; all C/H/P identities and exact-union additive dominance pass |
| Independent semantic validation | Hand-derived objective/version counterexamples, cycles, 60 random graphs and 675 independently traversed roots pass |
| In-study graph validation | 288 independently traversed roots; all 25,228 original stored reach counts reproduced |
| Identifier scope | 22,483 ordinary-shaped names plus 2,745 context identifiers; removing context nodes preserves every primary maintainer–workflow-repository set |
| Prospective records | Frozen before requests; 90 metadata captures, eight contextual 405s and two ordinary 404s; all 100 outcomes pending |
| Three full isolated reruns | Scientific result JSON byte-identical; 39.50-second mean, 0.98-second sample SD, 1,038.43-MiB maximum RSS on one host |
| Active bibliography | 13 cited primary references; 18 verified literature/source records |
| Anonymous PDF | 6 A4 pages, 177,502 bytes; all 27 fonts embedded, no Type 3 |
| Named PDF | 6 A4 pages, 178,870 bytes; all 28 fonts embedded, no Type 3 |
| Identity checks | Named author order, ECE/CSE departments and shared university present; supplied identities absent from anonymous PDF and author metadata |
| LaTeX diagnostics | No unresolved citations/references or overfull boxes; standard IEEEtran conference A4 10pt layout |

Reproducible checks are `python3 manuscript/scripts/verify_manuscript.py`, `python3 scripts/validate_research_study.py`, `python3 scripts/validate_observation_semantics.py`, `python3 manuscript/scripts/check_submission.py`, and `python3 manuscript/scripts/check_author_versions.py`. The three-run measurement command is `python3 scripts/profile_structural_study.py`.

Both PDFs were compiled with `bash manuscript/compile.sh --both`, Tectonic 0.17.0 and a writable temporary TeX cache. The relative-path `--both` invocation is verified from the repository root. GNU Make is unavailable on this host, so Make recipes were not executed; their constituent Python and shell commands were used directly. Fonts were inspected in the actual PDFs. The first-page author layout, experiment figures and final-page references were visually inspected. Underfull text warnings and fontconfig startup warnings remain benign; no missing glyph or font-embedding defect was observed.

The full working Overleaf ZIP contains both manuscript versions; the separate anonymous ZIP excludes named configurations, author records and working research notes. [package_validation.json](package_validation.json) records checksums, content checks and standalone anonymous-source compilation separately after packaging. That external report is intentionally excluded from the ZIPs to avoid circular archive checksums.

The observation-helper URL/response fixtures pass. The v2 collector was not used for fresh live GitHub workflow acquisition, and it does not repair historical flags automatically. Source archives and the original collector remain unchanged. Pending prospective surveillance ends on 18 January 2027; no trained forecast or real-world control effect is established.

Technical success does not certify human approval, authorship, similarity, venue eligibility or indirect anonymity. The acknowledgment now thanks the package maintainers, open-source community and public data resources used in the study. The supplied guideline's LLM disclosure requirement is unmet, and its restriction to non-intellectual assistance remains unresolved. These conditions are recorded separately from technical formatting checks; no AI-use, funding or author-approval declaration was added.

The editorial sentence directing the human authors to review interpretations, sources and disclosures was removed from the responsible-reporting paragraph. Both PDFs are checked for the neutral acknowledgment and absence of AI-use declarations and draft-review instructions. Research results and figures are unchanged.

## Research figure revision

Four code-generated figures are integrated into both PDFs: the implemented structural-measurement system, two objective budget curves, a source-set coverage partition, and graph-representation sensitivity. A fifth illustrative C/H/P mechanism is available as an optional figure outside the paper. All five are supplied as vector PDF, editable SVG and 300-dpi PNG, with a [gallery and source map](../figures/README.md).

The architecture now uses original infrastructure symbols and an explicit topology, rendered from Python-authored SVG through librsvg 2.63.3 to PDF 1.5. Its PDF contains no raster-image objects. The [draw.io export](../figures/study_system.drawio) contains 15 movable symbols, 52 editable labels and 19 native connector cells; five decorative paths remain separate, tightly cropped SVG objects. XML structure, unique cell identifiers, references, labels and geometry were checked. Interactive draw.io rendering was not exercised, so browser text placement may need minor adjustment. The SVG/PDF is the publication rendering source. The [design notes](../research/figure_design_notes.md) record the reference inspection and tool choice.

The renderers read the frozen structural results and identifier-scope census. Every plotted data row and partition is retained in `system_figure_data.json` or `analysis_figure_data.json`; `figure_manifest.json` binds inputs, all six generator modules and exports by SHA-256. Source verification checks all figure hashes and the exact partition totals. A repeat render produced byte-identical bytes for all 18 tracked exports and data records, including the draw.io file. Every generated PDF figure has embedded fonts and no Type 3 font; `figure_render_validation.json` records this check.

The system graph is explicitly schematic, its counts are empirical, maintainer links denote observed membership, and dependency traversal follows dependency to dependent. Source partition bars conserve 7,158 reachable repositories and exclude the 13 repositories without observed source identities. The optional six-endpoint example is illustrative and computed from its declared sets; it is not presented as a measured npm subgraph. No research result or source archive was changed by this visual revision.

The new system diagram and analysis pages were visually inspected at their intended print dimensions. An obsolete forced reference break was removed to retain the six-page limit with standard fonts and margins. Plot placement was adjusted to keep the budget chart near the results. Both named and anonymous PDFs pass the technical PDF checks; the separate disclosure requirement is unmet.
