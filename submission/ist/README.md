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

Both authors' confirmation of the contribution text and their approval of this version remain open. The draft credits Shahriar Hasan with leading the held-out studies, analysis, and manuscript preparation. Md. Ashikul Islam is credited for visualization, reconciliation of incident-associated results, and manuscript editing.

## Rebuild

```sh
python scripts/replay_yunohost_budgets.py
python scripts/package_yunohost_consumer_replay.py
python submission/ist/build_ist.py
```

The builder compiles both LaTeX entries from a clean extraction of the ZIP. It checks the PDFs, key results and author names, and records file hashes in `validation.json`. Template files come from the Elsevier package distributed by CTAN. [Template source](https://ctan.org/pkg/elsarticle)
