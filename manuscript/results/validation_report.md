# Validation record

Completed on **20 October 2026**.

| Check | Result |
|---|---|
| Source binding | All 12 recorded input hashes match the workspace files. |
| Database recomputation | Zero mismatches across seven metric fields for all 25,228 packages. |
| Cross-artifact comparison | Full package population compared; six-decimal score serialization accounted for separately. |
| Generated quantities | Numeric macros agree with the aggregate JSON. |
| Temporal timestamp check | Zero retained rows have a recorded source publication time after their cutoff. This is a ledger check, not source authentication. |
| References | All 15 citation keys resolve; BibTeX completed successfully. |
| LaTeX | Tectonic 0.17.0 compiled an eight-page IEEEtran conference PDF. No unresolved citations/references or overfull boxes remain. |
| Visual inspection | Title/abstract, literature table, equations, result tables, pipeline, both statistical figures, and reference-page layout inspected. |
| Standalone package | Overleaf ZIP extracted outside the repository and compiled successfully with Tectonic. Extracted PDF text matches the repository build. |
| ZIP integrity | Archive integrity check passed; source, bibliography, numeric inputs, figures, and compiled PDF are included. |
| Existing work | Original source data and research records retained unchanged. |

The XeLaTeX build emits startup font-family substitution messages and some underfull-line messages. The rendered text and mathematical symbols were inspected; these messages do not indicate missing references or a failed build. The standard IEEE layout and margins have not been compressed to force a page count.

The audit and consistency checks are reproducible. The incident sources have not been independently re-adjudicated here, and the proposed predictive benchmark remains unevaluated.
