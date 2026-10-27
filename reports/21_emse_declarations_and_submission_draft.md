# EMSE declarations and submission draft — 27 October 2026

The journal working sources and PDFs now include the missing submission sections. A dedicated EMSE export uses the official Springer Nature class, author–year references, alphabetical bibliography, and a flat source archive. The confirmed author contacts, departments, institution and shared address appear in the named drafts and separate title page; the latter also includes both ORCIDs.

## Confirmed and pending facts

The user confirmed no external funding or competing interests for either author, and that neither the conference nor journal version has been published, accepted or submitted elsewhere. Funding and interest declarations use those confirmations. The title page records the unpublished status.

The user chose a public research-data release before submission. Public access is not yet established. The data/code statements describe this pending release rather than claiming an accessible deposit or inventing a DOI. They must be finalized once a versioned public deposit exists. The LaTeX archive is a typesetting package, not the research dataset.

The user asked the assistant to assign contributions. Actual roles cannot be established from author order, so the optional contribution statement is omitted. Both authors' approval has not been asserted. These pending items are recorded in `submission/emse/submission_status.json`.

## Changes

- Shared `manuscript_q1/sections/10_declarations.tex` supplies funding, competing interests, data availability, code availability and the study's ethics/consent scope to both journal working drafts and the EMSE export.
- Shared `sections/04a_ai_assistance.tex` documents substantive assistance in drafting, code revision, analysis checks and source verification within the methods, without asserting completed human approval.
- Journal keywords reduced to six; the 166-word abstract and measured results are retained.
- Named IEEE working source adds the supplied emails, corresponding-author designation, address and ORCIDs. Its anonymous counterpart shares the new sections without exposing author identities.
- `submission/emse/build_emse.py` derives the Springer version from the shared scientific sources, preserves all 12 active figure files, fits tables to the Springer text block and places the wide literature matrix on a landscape page. Official class/style files are unchanged; their download provenance and hashes are retained.
- The separate title-page attachment now includes declarations and acknowledgments on a second page. Questionnaire draft answers and upload instructions accompany the artifacts.

## Validation

| Artifact/check | Result |
| --- | --- |
| `manuscript_q1/main_q1.pdf` | PASS; 15 pages |
| `manuscript_q1/main_q1_anonymous.pdf` | PASS; 15 pages; author identities absent |
| `submission/emse/EMSE_Manuscript.pdf` | PASS; 29 pages, 12 figures |
| `submission/emse/EMSE_Title_Page.pdf` | PASS; 2 pages |
| Clean extraction and compilation of flat `EMSE_LaTeX_Source.zip` | PASS; 29 pages |
| Active numerical evidence and figure provenance | PASS; existing scientific verification suite |
| Conference artifact lock | PASS; all four frozen conference deliverables unchanged |

The PDF gates found embedded fonts, no Type 3 fonts, no undefined citations/references, and no horizontal overflow greater than 1pt. EMSE checks also found no oversized float or vertical overflow. Required declarations and methods assistance disclosure are present in the rendered PDFs. The title page, manuscript first page, landscape matrix and declarations were visually inspected. The IEEE small-cap heading and email text-extraction spacing are normalized when checking required content.

Machine-readable results are in `manuscript_q1/results/q1_verification_report.json`, `submission/emse/validation.json` and `21_emse_artifact_manifest.json`. The Q1 source archive is refreshed after the final source/documentation changes. Scientific datasets and figures are unchanged.

Preparation follows the [EMSE submission guidelines](https://link.springer.com/journal/10664/submission-guidelines), checked 27 October 2026. Successful technical checks do not certify author approval, data-deposit completion or editorial acceptance.
