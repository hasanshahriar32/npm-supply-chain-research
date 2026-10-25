# ICEEICT 2027 initial-submission compliance

Applied from the supplied `guideline/guide.md` and `guideline/template_link.txt`. The corresponding [official initial-submission page](https://iceeict.mist.ac.bd/authors/paper-submission/) was checked on 20 October 2026 and specifies the same technical requirements. The supplied IEEE template URL could not be fetched by the browser; the [IEEE Author Center](https://conferences.ieeeauthorcenter.ieee.org/write-your-paper/authoring-tools-and-templates/) confirms the conference-template route. The paper uses the installed IEEEtran conference class in A4 mode. The user-supplied authors are recorded in [author_details.md](author_details.md) and rendered in a separate `main_authors.pdf`; `main.pdf` retains the anonymous review format.

| Requirement | Applied change or verification | Status |
|---|---|---|
| IEEE double-column template | `IEEEtran` with `conference,a4paper,10pt`; standard layout retained | Implemented |
| PDF, at most 3 MB | Compiled `main.pdf`; exact bytes recorded in the JSON report | Pass |
| A4 on every page | Every page checked with `pdfinfo`, approximately 595.28 × 841.89 pt | Pass |
| At most six pages, including references | Page count including all 13 active references recorded in the PDF report | See generated report |
| All fonts embedded | Review and named-draft fonts checked using `pdffonts`; current counts recorded in the generated reports | Pass |
| No Type 3 fonts | No Type 3 font found | Pass |
| Double-blind review | Anonymous author block; empty PDF author metadata; recorded author names, institution, local paths and email patterns screened | Technical screen passes; manual indirect-identity review pending |
| LLM acknowledgment | Accurate LLM-use disclosure is present; it does not claim solely non-intellectual use or completed author approval | Disclosure present; policy mismatch remains |
| LLM use limited to non-intellectual purposes | The guide says models were employed “solely for non-intellectual purposes.” This draft used literature discovery, study design, code development, analysis, drafting, and editing assistance | **Unresolved policy mismatch** |
| Human review and approval of LLM output | Not asserted; actual authors must review sources, code, claims, and disclosure | Pending |
| Similarity below 30% | No external similarity-service report available | Not verified |
| Authorship, order, and submission approval | Cannot be established by formatting or PDF inspection | Author confirmation required |
| Originality and no simultaneous submission | No declaration made on the authors' behalf | Author confirmation required |
| Co-author CMT accounts | No accounts inspected or created | Author action required |
| Presentation/no-show requirements | Applies if accepted; no promise made on the authors' behalf | Author planning required |

The manuscript acknowledges LLM assistance with drafting, code revision, analysis checks, and source verification. The actual authors must review and finalize the disclosure. The supplied guideline restricts use to non-intellectual purposes, so disclosure presence does not resolve the policy mismatch. No paper has been submitted.

## Artifacts and checks

`results/submission_compliance.json` records the PDF checksum, page dimensions, size, fonts, technical checks, guideline hashes, and remaining author-controlled requirements. The disclosure check is reported separately under `venue_policy_checks`; a technical formatting pass does not make an unmet policy check pass. Regenerate it from the repository root:

```bash
python3 manuscript/scripts/check_submission.py
```

The full Overleaf ZIP is an author working package with research notes and provenance. The separate `NPM_Supply_Chain_IEEE_Anonymous_Source.zip` contains only anonymous typesetting inputs and `main.pdf`, omitting author records, `config/authors.tex`, `main_authors.tex`, `main_authors.pdf`, and contextual identifiers. This reduces obvious disclosures but does not replace human anonymity review. The stated initial upload is a PDF.

The follow-up outcome methodology is recorded in `research/extended_benchmark_design.md`. The paper reports completed structural experiments, C/H/P definitions, representation and observation sensitivities, literature positioning, operational measurements, and limitations. No font or margin compression was used to meet the page limit.
