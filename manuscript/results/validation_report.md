# Validation record after applying the supplied guideline

Completed on **20 October 2026**.

| Check | Result |
|---|---|
| Source binding | All 12 audit-input hashes match the workspace files. |
| Database recomputation | Recorded zero mismatches across seven metric fields for 25,228 packages; the formatting revision changes no audit inputs or results. |
| Numeric inputs and references | Generated quantities agree with the audit JSON; all 15 bibliography keys resolve. |
| LaTeX | Tectonic 0.17.0 compiled the revised IEEEtran conference paper. Standard 10-point text and IEEE margins retained. |
| Page count and size | Five pages; all A4. Figures, tables, acknowledgment, and references are included in that count. |
| File size | Approximately 108 KB, below 3 MB; exact bytes and PDF hash recorded in `submission_compliance.json`. |
| Fonts | All 18 fonts embedded; no Type 3 fonts. |
| PDF author metadata | Empty; visible author block reads Anonymous Authors. |
| Identity-pattern screen | No local home paths or email-address patterns found in PDF text. Manual indirect-identity review remains necessary. |
| Layout diagnostics | No unresolved citations/references or overfull boxes. |
| Visual inspection | Revised title/abstract, metric definitions, literature/result tables, both plots, disclosure, and references inspected. |
| Disclosure | Truthful LLM acknowledgment added; the non-intellectual-use restriction remains unresolved. |
| Source packages | Full author working ZIP and separate anonymous typesetting ZIP generated. |
| Independent rebuild | Anonymous source ZIP extracted outside the repository, compiled to five A4 pages, and produced PDF text identical to the workspace build. |
| ZIP checks | Both archives pass integrity checks; the anonymous bundle excludes working notes, audit metadata, local paths, and known local identity strings from its text inputs. |

The build emits some underfull-line messages and XeLaTeX startup font-family substitution messages. These do not indicate failed embedding or missing mathematical symbols; actual PDF fonts are checked separately.

Technical checks do not establish similarity, authorship, human approval, originality, or LLM-policy eligibility. `submission_compliance.json` therefore keeps `submission_ready` false even when technical checks pass. Incident sources have not been independently re-adjudicated and the predictive benchmark remains unevaluated.

## Author update

The user supplied Shahriar Hasan (Department of ECE), followed by Ashikul Islam (Department of CSE), both at Hajee Mohammad Danesh Science and Technology University. These details are stored in `submission_files/authors.json` and `config/authors.tex`.

`main_authors.pdf` renders the two names with department superscripts and a shared university line; its PDF author metadata contains both names in the supplied order. The named version is five A4 pages, 109,163 bytes, with 19 embedded fonts and no Type 3 fonts. Its first-page layout was inspected. `main.pdf` remains five A4 pages with anonymous authors and empty author metadata; the recorded names and institution are absent from its text. `author_versions_validation.json` records both versions' checksums and checks.

The full source package includes both entry points. The anonymous source package explicitly excludes the named author configuration, author record, entry point, PDF, and author-side working notes. No emails, corresponding author, contribution roles, or publication approvals were inferred.
