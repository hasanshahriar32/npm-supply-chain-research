# EMSE submission draft

The journal manuscript now includes funding, competing interests, data availability, code availability, ethics/consent scope, and substantive AI assistance in the methods. The named manuscript and separate title page carry the supplied author contacts. The separate title page also records ORCIDs, acknowledgments and the confirmed unpublished status.

## Files for Editorial Manager

| File | Intended upload |
| --- | --- |
| `EMSE_Manuscript.pdf` | Local manuscript preview; use the TeX file as the primary Manuscript item when uploading full LaTeX source |
| `EMSE_LaTeX_Source.zip` | Upload and let Editorial Manager extract its flat contents; assign types as below |
| `EMSE_Reference_Copy.pdf` | Supplementary/reference PDF copy, with a different base filename from the primary TeX file |
| `EMSE_Title_Page.pdf` | Title Page containing ALL Author Contact Info. |
| `EMSE_Title_Page.tex` | Local editable source for the separate title page; keep out of the article's LaTeX upload |

For the full-source upload, select **Manuscript** and upload `EMSE_LaTeX_Source.zip`. Once it is extracted, put `EMSE_Manuscript.tex` first among the LaTeX files and classify it as **Manuscript**. Classify `references_q1.bib`, `EMSE_Manuscript.bbl`, `sn-basic.bst` and `sn-jnl.cls` as **LaTeX Supporting Files** (use the journal's equivalent label). Classify the 12 figure PDFs as **Figure**. Keep `EMSE_Title_Page.pdf` under **Title Page containing ALL Author Contact Info.** Upload `EMSE_Reference_Copy.pdf` as supplementary material for reference as instructed on the journal's screen. Remove the old manuscript PDF item when replacing it with the TeX source; do not also upload `EMSE_Manuscript.pdf` under the same basename. Confirm the per-file types after ZIP extraction, then proceed and inspect Editorial Manager's generated PDF before approving.

The reference copy is byte-identical to the current manuscript preview. The distinct filename avoids the TeX/PDF basename collision described in the [Editorial Manager LaTeX guide](https://www.ariessys.com/wp-content/uploads/EM_PM_LaTeX_Guide.pdf), pp. 2–8. The journal's on-screen **LaTeX Supporting Files** type takes precedence over the guide's generic **Manuscript** example for supporting files.

The EMSE export uses Springer Nature's official `sn-jnl` class, author–year citations and alphabetical references. The wide literature matrix occupies a landscape page. Scientific text, tables and figures derive from `manuscript_q1/`; the IEEE working drafts remain available there. Edit shared sections first and regenerate this export. Generated `source/` files are not the canonical research text.

## Items still pending before final submission

- Publish the versioned replication materials, verify unauthenticated access, and replace the pending data/code availability wording in `manuscript_q1/sections/10_declarations.tex` with the actual release URL, version or DOI, and any exclusions. The manuscript currently states that public access is not yet available. No deposit or DOI has been invented.
- Both authors must review the final manuscript and approve submission. No approval has been asserted.
- Individual author roles remain unconfirmed. The optional author-contribution statement is omitted rather than assigning invented roles. Add it once actual contributions are established.

The user confirmed no external funding or competing interests for either author, and that neither the conference nor journal version has been published, accepted or submitted elsewhere. `submission_status.json` records those facts separately from pending items. The conference-length draft must remain outside simultaneous review while this overlapping journal article is under consideration.

## Build and verification

From the repository root:

```sh
python3 submission/emse/build_emse.py
```

Requires Python, Tectonic, `pdfinfo`, `pdffonts` and `pdftotext`. The script expands shared LaTeX inputs, adapts formatting, compiles both attachments, packages the flat source ZIP, then compiles a clean extraction. `validation.json` records page counts, fonts, overflow/citation/glyph checks, required content and source hashes. Technical success does not assert a completed public deposit or author approval. The source ZIP is a typesetting package, not the research dataset.

The official template download and unchanged class/style hashes are recorded in `template/PROVENANCE.json`. Author order, departments, contacts and address follow `manuscript/submission_files/authors.json`. ORCID checksums pass; account ownership was not independently verified.

Preparation basis: [EMSE submission guidelines](https://link.springer.com/journal/10664/submission-guidelines), checked 27 October 2026. Questionnaire wording is in `questionnaire_answers.md`.
