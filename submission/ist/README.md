# Information and Software Technology submission package

Open `IST_Submission_Package.zip` locally. Use the individual files for Editorial Manager. Both manuscript PDFs use the same results and structured abstract. The anonymous copy is available if the portal requests it.

| File | Contents |
| --- | --- |
| `IST_Manuscript.pdf` | Named manuscript with a structured abstract, funding and competing interests, data availability, contribution wording, and AI disclosure |
| `IST_LaTeX_Source.zip` | Editable named manuscript with a single LaTeX entry point, bibliography, figures and Elsevier class |
| `IST_Anonymous_Manuscript.pdf` | Reviewer copy for a double-anonymized workflow |
| `IST_Anonymous_LaTeX_Source.zip` | Editable anonymous manuscript for a portal that requests source |
| `IST_Title_Page.pdf` | Author names, contact details, ORCIDs and contributions for the editorial office |
| `IST_Supplement.pdf` | Detailed consumer extraction methods, sensitivity results, and packaging diagnostics |
| `IST_Supplement_Source.zip` | Editable supplement with its own LaTeX entry point |
| `IST_Consumer_Replication.zip` | Offline verification of the five-account outcomes, additional evidence checks, and the exploratory six-budget comparison |
| `IST_Highlights.txt` | Four editable research highlights |
| `IST_Cover_Letter.txt` | Draft cover letter for the corresponding author |
| `IST_Form_Metadata.txt` | Copy-ready title, structured abstract, keywords, author details and data information |

The live IST author guide returned HTTP 403 during preparation. The package follows the publisher's general instructions and the structured-abstract convention of published IST articles. Choose one manuscript version according to the live portal. Use the matching source ZIP where source is requested. For an anonymous workflow, choose the designated title-page field for the editor-only PDF and check that the cover letter and author-only metadata remain outside the review PDF. [IST author guide](https://www.sciencedirect.com/journal/information-and-software-technology/publish/guide-for-authors) · [Elsevier file preparation](https://www.elsevier.support/publishing/answer/how-do-i-prepare-my-files-for-submission-in-editorial-manager)

## Before submitting

1. Shahriar Hasan and Md. Ashikul Islam should review the final PDF, confirm their contribution wording, and agree to submit this version. The draft assigns Hasan the lead on the consumer studies, analysis and manuscript preparation. It credits Islam for visualization, reconciliation of incident-associated results and manuscript editing. [Elsevier authorship policy](https://www.elsevier.com/about/policies-and-standards/publishing-ethics#authorship-of-the-paper)
2. Make `IST_Consumer_Replication.zip` available to reviewers. It contains the current consumer evidence. The public October release contains the earlier graph validation and original-data link. If the portal requests a repository identifier for the current consumer evidence, deposit the ZIP as a versioned record and use that record in the data statement. Use the ZIP hash in `validation.json` to check the downloaded copy. [October release](https://github.com/hasanshahriar32/npm-supply-chain-research/releases/tag/research-validation-2026-10-28) · [Elsevier research data guidance](https://www.elsevier.com/researcher/author/tools-and-resources/research-data)
3. Confirm the live journal's article type, review settings and attachment fields in Editorial Manager. Open the generated review PDF and check the title, abstract, authors, supplement and reviewer access to the archive before approval. [Elsevier upload instructions](https://www.elsevier.support/publishing/answer/how-do-i-prepare-my-files-for-submission-in-editorial-manager)

## Rebuild

```sh
python scripts/replay_yunohost_budgets.py
python scripts/package_yunohost_consumer_replay.py
python submission/ist/build_ist.py
```

The builder compiles the named manuscript, anonymous manuscript and supplement from separate clean source ZIPs. It builds the title page from the author record, checks the rendered PDFs and exports the submission bundle. The readiness check compares the source archives with the manuscript, checks direct author identifiers in anonymous files and replays both application frames. `validation.json` records the hashes of the individual submission files. [Template source](https://ctan.org/pkg/elsarticle)
