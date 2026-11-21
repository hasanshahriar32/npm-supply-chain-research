# Journal figure revision and YunoHost evidence intake

## Manuscript figures and layout

Figure 4 contrasts the collapsed package-name path with two disconnected exact-version paths. It keeps the original illustrative node identities and reverse-reach direction. The marked gap between the two intermediate versions identifies the exact point at which the name projection introduces apparent reach.

Figure 5 follows the analysis dependency. The observed graph yields reach sets, which supply parallel scoring and verification branches. Longer descriptions belong in the caption and methods. The new paired-evidence figure separates 23 common positives, six common negatives and 126 unresolved project pairs. It displays the conservative 0–81.3% range of compatible reassignment. The underlying results and alternate tie evaluations remain in the sealed results file.

The three illustrations are editable SVGs with vector PDF 1.5 assets and PNG previews. They are drawn at 248 pt and placed at the manuscript column width. The weights appendix table uses a compact one-column layout. The threshold section points to its existing table for detailed counts. The numerical inputs to those tables are retained.

Regenerate the new designs with `python scripts/render_journal_diagrams.py`. The [asset manifest](../manuscript_q1/results/journal_diagrams.json) binds the renderer, the holdout result, and output files by SHA-256. The previous diagram assets remain in `manuscript_q1/figures/editorial_inputs`.

## Second-frame intake

The medchain collector requested root manifests and conventional lockfile paths at all 215 previously screened commits. The local verifier matched every retained file to its receipt and every root manifest to the earlier screen's checksum. There were 454 HTTP 200 and 1,266 HTTP 404 file responses. A 404 at a root path says nothing about nested application files.

| Root intake classification | Projects |
| --- | ---: |
| npm file available | 108 |
| pnpm file available | 44 |
| Yarn file available | 35 |
| Bun file available | 6 |
| No root lockfile returned | 16 |
| Multiple manager families | 4 |
| Declared manager's file unavailable | 2 |

These categories use declared manager and root-file availability. They measure acquisition. Format support, workspace resolution, registry identity and final paired coverage require separate checks. The data include 152 projects with an npm or pnpm file candidate. The [intake ledger](../research/consumer_parser_development/yunohost_lockfile_intake.json) preserves every frame entry and its classification. Retained file bodies are kept in the local ignored evidence directory.

Both named and anonymous drafts compile to 17 pages. The revised figure pages and final appendix page were checked in rendered proofs, and the final build reported no overfull boxes, missing glyphs or undefined references. The VPS collection exited and its temporary process and directory checks returned no matches.

## Matching the illustrated architecture

The reference screenshot is the journal's `study_system.pdf`. The SVG master was drawn with [render_technical_architecture.py](../manuscript/scripts/render_technical_architecture.py) using [technical_icons.py](../manuscript/scripts/technical_icons.py). It places geometric SVG symbols, text and routed connectors independently. Librsvg exports the publication PDF. The existing [draw.io exporter](../manuscript/scripts/export_drawio.py) converts each label and route to a native object and keeps each icon separately movable.

Figures 4 and 5 now use those original isometric package, account, server, database and document symbols. Figure 4 uses arrow style as well as color to distinguish projected and exact reverse reach. Figure 5 routes the shared reach sets directly to both analysis branches. The 248-point SVGs use the same nominal width as before, with added vertical space for the illustrated labels and connectors.

- [Figure 4 SVG](../manuscript_q1/figures/graph_semantics.svg) and [draw.io](../manuscript_q1/figures/graph_semantics.drawio)
- [Figure 5 SVG](../manuscript_q1/figures/study_methodology.svg) and [draw.io](../manuscript_q1/figures/study_methodology.drawio)

Regenerate with `python scripts/render_journal_diagrams.py`. The renderer is the source of record. Draw.io edits can be used for separate design work. The publication PDFs and rendered manuscript pages were inspected. The draw.io files were verified as structured XML with separate icon, text and connector cells.
