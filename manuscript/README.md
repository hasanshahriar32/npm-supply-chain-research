# IEEE manuscript: Auditing the Blast Radius

This is a complete IEEE conference-style research draft for this repository. Its modular sections, configuration, figures, bibliography, and build entry point follow the organization of `/home/m4x1d/Desktop/GOAD/manuscript/`. The layout uses the actual `IEEEtran` conference class, A4 paper, standard 10-point text, and two columns; the GOAD example uses a one-column `article` class. No GOAD scientific content, author identities, or results were copied.

Open **[main_authors.pdf](main_authors.pdf)** for the paper with the supplied authors. **[main.pdf](main.pdf)** remains the anonymous initial-submission version required by the guideline. Edit **[main.tex](main.tex)** to change section order and **[config/metadata.tex](config/metadata.tex)** for the title and review/camera-ready author block. The PDF retains an anonymous author block and empty author metadata for initial double-blind review. Author-side notes are kept separate from the anonymous typesetting bundle.

## Authors and manuscript versions

| Order | Author | Department |
|---|---|---|
| 1 | Shahriar Hasan | Department of ECE |
| 2 | Ashikul Islam | Department of CSE |

Both authors are affiliated with **Hajee Mohammad Danesh Science and Technology University**. The sequence and department abbreviations follow the supplied details. No email addresses or corresponding-author designation were supplied. See [submission_files/author_details.md](submission_files/author_details.md) and [submission_files/authors.json](submission_files/authors.json).

`main_authors.tex` selects the named author block from `config/authors.tex`; `main.tex` defaults to anonymous review. Both share the same paper text, figures, and bibliography. The named draft is for author review and later camera-ready preparation, without implying acceptance or submission approval. The full Overleaf ZIP includes both versions; the anonymous ZIP excludes the named entry point, PDF, configuration, and author records.

## Applied submission guideline

The requirements in [guideline/guide.md](guideline/guide.md) and [guideline/template_link.txt](guideline/template_link.txt) are now applied to the paper. The revised PDF is **five A4 pages**, including all tables, figures, acknowledgment, and 15 references. Font inspection confirms all 18 fonts in the anonymous PDF are embedded and none is Type 3; the named PDF has 19 embedded fonts and no Type 3 fonts. Both are five pages and below 3 MB (approximately 108 KB anonymous, 109 KB named). The standard IEEE text size and margins have been retained.

The guide corresponds to the [ICEEICT 2027 initial-submission requirements](https://iceeict.mist.ac.bd/authors/paper-submission/). [submission_files/guideline_compliance.md](submission_files/guideline_compliance.md) maps each requirement to evidence or an outstanding author action. [results/submission_compliance.json](results/submission_compliance.json) records automated PDF checks.

**LLM policy remains unresolved.** The guide limits LLM assistance to non-intellectual purposes; this project used assistance for literature discovery, audit-code development, and drafting as well as editing. The acknowledgment states the actual roles. It does not assert that human review has already occurred or that the narrower policy has been met. Authors must resolve that mismatch before submission. No similarity score, authorship approval, originality declaration, or CMT status has been assumed.

## What the paper contributes

The paper reports a new, independently executed consistency audit of the two local compressed data artifacts. All seven SQLite metrics reproduce from the stored inputs, but the CSV and SQLite disagree on workflow reach for 17,809 of 25,228 packages. Their default-score top-253 queues share 65 packages under the stated name-order tie rule. Figures and sensitivity analysis show how the inconsistency changes review queues.

The draft also inventories the existing incident companion: 47 package-event records, 31 family identifiers, 45 retained source objects, and 258 declared dependency edges. These are counts of repository records, not independent re-adjudication of those incidents. No eligible comparison population exists in the companion. The paper therefore separates completed measurement results from a proposed temporal compromise benchmark. It does not invent trained HGAT results, accuracy, attacker ROI, or a completed three-queue evaluation.

The literature screen includes newer work such as [PatchRisk](https://arxiv.org/abs/2609.13719), [SupplyTGN](https://ssrn.com/abstract=7194447), [On Good Authority](https://arxiv.org/abs/2606.22593v2), and [CHRONO-RESOLUTION](https://arxiv.org/abs/2607.15315). The resulting novelty claim is deliberately limited to this empirical audit and its queue consequences. See [research/novelty_assessment.md](research/novelty_assessment.md).

## Folder structure

```text
manuscript/
  main.tex                         IEEEtran conference entry point
  main.pdf                         anonymous initial-submission PDF
  main_authors.tex                  named author draft entry point
  main_authors.pdf                  compiled draft with supplied authors
  config/                          package setup and author/title metadata
  sections/                        abstract, eight sections, LLM acknowledgment
  bibliography/references.bib       15 checked primary references
  tables/                          literature positioning table
  figures/                         vector PDF figures, PNG previews, TikZ diagram
  results/                         aggregate JSON/CSV and generated LaTeX values
  research/                        repository context, novelty, and claim evidence
  scripts/                         offline audit, figures, checks, ZIP packaging
  submission_files/                venue requirements and compliance notes
  guideline/                       supplied guide and IEEE template link
  compile.sh                       LaTeX build with compiler fallbacks
  Makefile                         convenient rebuild targets
  requirements-figures.txt          optional figure-rendering dependency
  build/                           ignored compiler intermediates
```

## Compile and use Overleaf

From this folder:

```bash
bash compile.sh                  # anonymous main.pdf
bash compile.sh main_authors.tex # named main_authors.pdf
```

The script supports `latexmk`, Tectonic, or `pdflatex` plus `bibtex`, and copies the selected entry point's PDF from `build/` into this folder. A standard TeX Live installation with IEEEtran, TikZ, booktabs, tabularx, hyperref, and xurl is sufficient. Tectonic fetches TeX resources on its first run and then caches them. An explicit binary can be selected with `TECTONIC=/path/to/tectonic bash compile.sh`.

For Overleaf, upload `../NPM_Supply_Chain_IEEE_Overleaf.zip` as a new project, select `main.tex` for anonymous review or `main_authors.tex` for the named draft, and compile with pdfLaTeX. This full working package includes local research context and is **not an anonymous review supplement**. `../NPM_Supply_Chain_IEEE_Anonymous_Source.zip` is a separate typesetting-only package that omits those working notes and provenance identifiers. The ZIP is self-contained for **typesetting**, including figures, numeric tables, bibliography, and this documentation. Recomputing the audit additionally requires the source repository and its data archives; the database is not duplicated in the ZIP.

## Reproduce the empirical work

Run from the repository checkout; the scripts resolve paths from their own locations:

```bash
python3 manuscript/scripts/audit_artifacts.py
python3 manuscript/scripts/verify_manuscript.py
```

The audit requires Python 3.11 or newer and uses only its standard library, extracts SQLite to a temporary directory, opens it read-only, and makes no network requests. It validates all 25,228 package traversals, compares fields using an explicit score-rounding tolerance, and emits aggregate results. No package payload is acquired or executed. Source files remain unchanged.

To rerender the two statistical figures, use a virtual environment with the version recorded in `requirements-figures.txt`, then run:

```bash
python3 manuscript/scripts/render_figures.py
```

The delivered figures were generated with Python 3.14.8 and Matplotlib 3.11.2. The delivered PDF was compiled using Tectonic 0.17.0. Figure PDFs are already committed to this writing package, so Python plotting dependencies are unnecessary for ordinary LaTeX compilation. `make reproduce` runs audit, rendering, verification, compilation, and PDF checks. `make authors-pdf` builds the named version; `make submission-check` checks the anonymous PDF. `make package` creates both source ZIPs.

## Evidence and editing rules

`results/artifact_audit.json` binds the analysis to full archive hashes and a repository revision. The audit date is 20 October 2026, not an asserted collection date. The platform's June snapshot date and SQLite's July metric calculation timestamp should not be treated as a single historical cutoff.

The root `research/` contains earlier plans; `platform/research/` contains an expanded, partly inconsistent research record. The paper does not silently reconcile those documents by choosing the largest count. It uses independently recomputed archive facts for audit claims and labels companion counts as an inventory. [research/claim_evidence.csv](research/claim_evidence.csv) maps claims to sources and limitations.

Before initial submission, retain anonymous paper metadata, review all scientific claims and indirect identifiers, resolve the LLM-policy mismatch, obtain the required similarity report, and confirm the author-controlled declarations. Keep the supplied names confined to the named draft until the review stage permits author identification. The extended pre-guideline methodology is preserved in [research/extended_benchmark_design.md](research/extended_benchmark_design.md). The current draft is an empirical measurement paper with a proposed follow-up benchmark, not a completed prediction study.

## Check the submission PDF

```bash
python3 manuscript/scripts/check_submission.py
```

Run from the repository root. The checker uses Poppler's `pdfinfo`, `pdffonts`, and `pdftotext` to verify the actual page count, every page's dimensions, byte size, font types and embedding, author metadata, and basic identity patterns. It also checks the LLM acknowledgment and compiled reference/overflow diagnostics. A technical pass does not certify similarity, authorship, venue eligibility, or complete anonymity.
