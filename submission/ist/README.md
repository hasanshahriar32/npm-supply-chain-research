# Information and Software Technology submission package

The manuscript leads with the held-out fixed-budget comparison. The supporting PDF preserves the full evidence-stage table, parser and packaging details, and graph-objective sensitivity analyses.

| File | Contents |
| --- | --- |
| `IST_Manuscript.pdf` | Named manuscript with a structured abstract, funding and competing interests, data availability, contribution wording, and AI disclosure |
| `IST_LaTeX_Source.zip` | Editable manuscript and supplement, numbered bibliography style, figures, and the Elsevier class |
| `IST_Supplement.pdf` | Detailed consumer extraction methods, sensitivity results, and packaging diagnostics |
| `IST_Consumer_Replication.zip` | Offline verification of the five-account outcomes, additional evidence checks, and the exploratory six-budget comparison |
| `IST_Highlights.txt` | Four editable research highlights |
| `IST_Cover_Letter.txt` | Draft cover letter for the corresponding author |

The export uses the Elsevier LaTeX class, a structured abstract, and a separate supplement. The live IST author guide returned HTTP 403 during preparation. The submission package follows the verified general publisher guidance and the structured-abstract convention used by published IST articles. Journal-specific upload fields and review settings remain unverified. [IST author guide](https://www.sciencedirect.com/journal/information-and-software-technology/publish/guide-for-authors) · [Elsevier LaTeX instructions](https://www.elsevier.com/en-in/researcher/author/policies-and-guidelines/latex-instructions)

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

The builder compiles both LaTeX entries from a clean extraction of the ZIP. It checks the PDFs, key results and author names, records file hashes in `validation.json`, and runs `python submission/ist/check_readiness.py`. That check compares the archive with the current manuscript source and replays both application frames from a clean extraction. Template files come from the Elsevier package distributed by CTAN. [Template source](https://ctan.org/pkg/elsarticle)
