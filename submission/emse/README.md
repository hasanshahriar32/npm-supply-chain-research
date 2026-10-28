# EMSE submission draft

The journal validation revision includes heuristic component/exact benchmarks, a fresh bounded cohort and automated endpoint evidence. It has four focused research questions and 13 active figures; extended sensitivities and historical reconstruction/acquisition feasibility are appendices. Required declarations and methods assistance disclosure are included. The named manuscript/title page provide the verified public artifact link and author contacts; the anonymous working PDF omits the author-identifying release URL.

## Files for Editorial Manager

| File | Intended upload |
| --- | --- |
| `EMSE_Manuscript.pdf` | Local manuscript preview; use the TeX file as the primary Manuscript item when uploading full LaTeX source |
| `EMSE_LaTeX_Source.zip` | Upload the regenerated flat contents, with 13 active figure PDFs named `Fig1.pdf` through `Fig13.pdf`; assign types as below |
| `EMSE_Reference_Copy.pdf` | Supplementary/reference PDF copy, with a different base filename from the primary TeX file |
| `EMSE_Title_Page.pdf` | Title Page containing ALL Author Contact Info. |
| `EMSE_Title_Page.tex` | Local editable source for the separate title page; keep out of the article's LaTeX upload |

For the full-source upload, select **Manuscript** and upload `EMSE_LaTeX_Source.zip`. Once it is extracted, put `EMSE_Manuscript.tex` first among the LaTeX files and classify it as **Manuscript**. Classify `references_q1.bib`, `EMSE_Manuscript.bbl`, `sn-basic.bst` and `sn-jnl.cls` as **LaTeX Supporting Files** (use the journal's equivalent label). Classify the 13 figure PDFs as **Figure**. Keep `EMSE_Title_Page.pdf` under **Title Page containing ALL Author Contact Info.** Upload `EMSE_Reference_Copy.pdf` as supplementary material for reference as instructed on the journal's screen. Replace the previous attachment set so unused old figures and stale sources are not retained. Update the form abstract to match this revised manuscript. Confirm the per-file types after ZIP extraction, then proceed and inspect Editorial Manager's generated PDF before approving.

The reference copy is byte-identical to the current manuscript preview. The distinct filename avoids the TeX/PDF basename collision described in the [Editorial Manager LaTeX guide](https://www.ariessys.com/wp-content/uploads/EM_PM_LaTeX_Guide.pdf), pp. 2–8. The journal's on-screen **LaTeX Supporting Files** type takes precedence over the guide's generic **Manuscript** example for supporting files.

The EMSE export uses Springer Nature's official `sn-jnl` class, author–year citations and alphabetical references. The wide literature matrix occupies a landscape page. Scientific text, tables and figures derive from `manuscript_q1/`; the IEEE working drafts remain available there. Edit shared sections first and regenerate this export. Generated `source/` files are not the canonical research text.

## Author attestations and optional validation

The manuscript reports an automated evidence audit and explicitly states that its indicators were not manually validated. Independent author annotation is optional additional research, not an EMSE submission requirement; no completed human audit or agreement statistics are claimed. Existing review sheets remain research working materials outside the flat submission package.

Both authors must approve the actual submission and its author list. The assistant cannot provide either author's approval. Individual roles have not been confirmed, so the recommended contribution statement is omitted rather than invented. These author confirmations belong in the submission process, not as task notes in the manuscript.

The [research prerelease](https://github.com/hasanshahriar32/npm-supply-chain-research/releases/tag/research-validation-2026-10-28) is public. Its companion includes code, new observations and derived audit data; a helper downloads the original database from a fixed commit and verifies its checksum. Clean offline reproduction passed. Raw third-party workflow/manifest bodies are referenced by pinned URLs/hashes rather than redistributed in that asset. The public download was verified without authentication; receipt and checksum are in `../research_artifact/package_manifest.json`.

The user confirmed no external funding or competing interests for either author, and that neither the conference nor journal version had been published, accepted or submitted elsewhere. `submission_status.json` records those confirmations separately from pending items. The conference-length draft must remain outside simultaneous review while this overlapping journal article is under consideration. If this submission has already been formally submitted, changes need the journal's revision/editorial route; the local rebuild does not update Editorial Manager automatically.

## Build and verification

From the repository root:

```sh
python3 submission/emse/build_emse.py
```

Requires Python, Tectonic, `pdfinfo`, `pdffonts` and `pdftotext`. The script expands shared LaTeX inputs and appendices, adapts formatting, compiles both attachments, packages the flat source ZIP, then compiles a clean extraction. `validation.json` records page counts, fonts, overflow/citation/glyph checks, required content, public-release status and source hashes. Technical success does not assert completed human annotation or author approval. The source ZIP is a typesetting package, not the research dataset. Run `python3 submission/emse/check_guidelines.py` for caption/citation-order, internal-note, archive and metadata checks. Journal figure presentation is prepared by `python3 scripts/prepare_emse_figures.py`; its original inputs are frozen under `manuscript_q1/figures/editorial_inputs/` and must be deliberately refreshed when underlying measurements change.

The official template download and unchanged class/style hashes are recorded in `template/PROVENANCE.json`. Author order, departments, contacts and address follow `manuscript/submission_files/authors.json`. ORCID checksums pass; account ownership was not independently verified.

Preparation basis: [EMSE submission guidelines](https://link.springer.com/journal/10664/submission-guidelines), checked 28 October 2026. Questionnaire wording is in `questionnaire_answers.md`.

The 28 October guideline correction removes internal task-status language, retains the absence of manual validation as a methodological limitation, shortens the factual Methods AI disclosure, corrects bibliographic names/venues, adds missing figure/table citations, and numbers figure upload filenames. The title-page publication-status assertion is removed. See `guideline_review/compliance_review.md` for the scope and author-controlled items.
