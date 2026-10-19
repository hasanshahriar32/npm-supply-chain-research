# Author details for the named manuscript

The user supplied the following authors in this order:

| Order | Author | Department | Institution |
|---|---|---|---|
| 1 | Shahriar Hasan | Department of ECE | Hajee Mohammad Danesh Science and Technology University |
| 2 | Ashikul Islam | Department of CSE | Hajee Mohammad Danesh Science and Technology University |

The institution spelling has been normalized to “Science and Technology.” Department abbreviations are retained as provided. Email addresses, a corresponding-author designation, contribution roles, and publication approval were not supplied or invented. The supplied order is recorded; this does not assert approval by both individuals.

`authors.json` holds the structured author record. `config/authors.tex` contains the IEEE author block and PDF author metadata for the named draft. Superscripts map Shahriar Hasan to ECE and Ashikul Islam to CSE; the shared university appears below both names in `main_authors.pdf`.

## Which version to use

- **Named author draft:** `main_authors.tex` → `main_authors.pdf`. For author review and later camera-ready preparation; this is not an assertion of acceptance or submission readiness.
- **Anonymous initial submission:** `main.tex` → `main.pdf`. The supplied guideline requires exclusion of authors and affiliations during double-blind review.

Build both from `manuscript/`:

```bash
bash compile.sh main_authors.tex
bash compile.sh
```

The full Overleaf package includes both entry points and this author record. The anonymous typesetting package excludes this document, `authors.json`, `config/authors.tex`, and the named entry point/PDF. Its remaining text inputs are screened for the recorded names and institution; the review PDF is checked separately for those identifiers.
