# IEEE manuscript: Auditing the Blast Radius

This is a complete IEEE conference-style research draft for this repository. Its modular sections, configuration, figures, bibliography, and build entry point follow the organization of `/home/m4x1d/Desktop/GOAD/manuscript/`. The layout uses the actual `IEEEtran` conference class and two columns; the GOAD example uses a one-column `article` class. No GOAD scientific content, author identities, or results were copied.

Open **[main.pdf](main.pdf)** to read the compiled paper. Edit **[main.tex](main.tex)** to change section order and **[config/metadata.tex](config/metadata.tex)** for the title and actual authors. Anonymous author text is intentional and does not assert that the repository or supplementary notes have been anonymized for submission.

## What the paper contributes

The paper reports a new, independently executed consistency audit of the two local compressed data artifacts. All seven SQLite metrics reproduce from the stored inputs, but the CSV and SQLite disagree on workflow reach for 17,809 of 25,228 packages. Their default-score top-253 queues share 65 packages under the stated name-order tie rule. Figures and sensitivity analysis show how the inconsistency changes review queues.

The draft also inventories the existing incident companion: 47 package-event records, 31 family identifiers, 45 retained source objects, and 258 declared dependency edges. These are counts of repository records, not independent re-adjudication of those incidents. No eligible comparison population exists in the companion. The paper therefore separates completed measurement results from a proposed temporal compromise benchmark. It does not invent trained HGAT results, accuracy, attacker ROI, or a completed three-queue evaluation.

The literature screen includes newer work such as [PatchRisk](https://arxiv.org/abs/2609.13719), [SupplyTGN](https://ssrn.com/abstract=7194447), [On Good Authority](https://arxiv.org/abs/2606.22593v2), and [CHRONO-RESOLUTION](https://arxiv.org/abs/2607.15315). The resulting novelty claim is deliberately limited to this empirical audit and its queue consequences. See [research/novelty_assessment.md](research/novelty_assessment.md).

## Folder structure

```text
manuscript/
  main.tex                         IEEEtran conference entry point
  main.pdf                         compiled paper
  config/                          package setup and author/title metadata
  sections/                        abstract and eight manuscript sections
  bibliography/references.bib       15 checked primary references
  tables/                          literature positioning table
  figures/                         vector PDF figures, PNG previews, TikZ diagram
  results/                         aggregate JSON/CSV and generated LaTeX values
  research/                        repository context, novelty, and claim evidence
  scripts/                         offline audit, figures, checks, ZIP packaging
  submission_files/                final author/venue preparation notes
  compile.sh                       LaTeX build with compiler fallbacks
  Makefile                         convenient rebuild targets
  requirements-figures.txt          optional figure-rendering dependency
  build/                           ignored compiler intermediates
```

## Compile and use Overleaf

From this folder:

```bash
bash compile.sh
```

The script supports `latexmk`, Tectonic, or `pdflatex` plus `bibtex`, and copies `build/main.pdf` to `main.pdf`. A standard TeX Live installation with IEEEtran, TikZ, booktabs, tabularx, hyperref, and xurl is sufficient. Tectonic fetches TeX resources on its first run and then caches them. An explicit binary can be selected with `TECTONIC=/path/to/tectonic bash compile.sh`.

For Overleaf, upload `../NPM_Supply_Chain_IEEE_Overleaf.zip` as a new project, select `main.tex`, and compile with pdfLaTeX. The ZIP is self-contained for **typesetting**, including figures, numeric tables, bibliography, and this documentation. Recomputing the audit additionally requires the source repository and its data archives; the database is not duplicated in the ZIP.

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

The delivered figures were generated with Python 3.14.8 and Matplotlib 3.11.2. The delivered PDF was compiled using Tectonic 0.17.0. Figure PDFs are already committed to this writing package, so Python plotting dependencies are unnecessary for ordinary LaTeX compilation. `make reproduce` runs audit, rendering, verification, and compilation; `make package` creates the Overleaf ZIP.

## Evidence and editing rules

`results/artifact_audit.json` binds the analysis to full archive hashes and a repository revision. The audit date is 20 October 2026, not an asserted collection date. The platform's June snapshot date and SQLite's July metric calculation timestamp should not be treated as a single historical cutoff.

The root `research/` contains earlier plans; `platform/research/` contains an expanded, partly inconsistent research record. The paper does not silently reconcile those documents by choosing the largest count. It uses independently recomputed archive facts for audit claims and labels companion counts as an inventory. [research/claim_evidence.csv](research/claim_evidence.csv) maps claims to sources and limitations.

Before submission, supply the actual author list, select a venue and page limit, review all scientific claims, resolve the incident-label target and historical data requirements, and follow the chosen venue's disclosure policy for writing tools. The current draft is an empirical measurement paper with a proposed follow-up benchmark, not a completed prediction study.
