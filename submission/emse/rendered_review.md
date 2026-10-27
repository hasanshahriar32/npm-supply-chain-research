# Editorial Manager PDF review — 27 October 2026

Reviewed `EMSE-S-26-02038.pdf`. The rendering passes the checks below, but the data-release wording and portal metadata need correction before final submission.

## Corrections

| Location in merged PDF | Finding | Action |
| --- | --- | --- |
| Page 28, article page 26; also page 29 for code availability | Data/code availability still describe a planned release. The text says public access and an identifier are not yet available. | Publish and verify the versioned replication materials, insert the actual URL/version or DOI and any exclusions, rebuild the manuscript/title page, replace uploads and regenerate the submission PDF. |
| Page 1 | City is displayed as **Dianjpur**. | Correct the corresponding-author address/profile city in the portal to **Dinajpur**. |
| Page 1 | **Department of CSE** appears after Md. Ashikul Islam in the qualification position. | Move it to the affiliation's department field. Keep the author name as **Md. Ashikul Islam** and enter any actual qualification in the proper field. |
| Page 2 | Uploaded title page is the earlier one-page contact-only attachment. | Replace it with the current two-page `EMSE_Title_Page.pdf` after finalizing the data/code statements. The present names, emails, ORCIDs and address are correct. |

## Rendering checks

- The merged PDF has 32 pages: cover metadata, one uploaded title page, 29 article pages and a supplementary-PDF download page. No extra duplicate figure pages are appended.
- Article pages 1–29 correspond to merged PDF pages 3–31. Each page has exactly the same normalized extracted character inventory as the prepared `EMSE_Manuscript.pdf`, after removing the system's margin line numbers and top labels. Reading order differs for some rotated/vector content; this comparison does not claim byte-identical PDFs or prove character order.
- All 12 figure captions and nine table captions are present and consecutively numbered. All pages were inspected in contact sheets; the cover, landscape literature matrix, dense tables and declarations were inspected at larger scale. No visible clipped content was found. No text bounding boxes fall outside the page boundaries.
- No explicit LaTeX fatal-error, undefined-control-sequence or unresolved-citation/reference summary markers were found in the PDF text. The underlying EM compiler log is not included, so this is a check of the delivered PDF rather than a log audit.
- The cover abstract matches the canonical abstract after Unicode and whitespace normalization. The title, author order and six keywords agree with the prepared manuscript. The author-contact page has the correct emails and ORCIDs.
- Funding, competing interests, ethics/consent, data/code availability and the methods AI-use disclosure are included. The data/code statements are present but unfinished for the chosen public-release plan.
- No Type 3 fonts were observed. System-added Courier line-number fonts and the cover's Verdana font are unembedded; these are not a manuscript-text loss finding. The 1–65 margin numbering is added by Editorial Manager.
- The final page's reference-PDF download link is expected supplementary-material handling, not a compilation error. The blank cover Funding Information row does not alone establish that a no-funding response is missing; the manuscript expressly states no external funding.

`rendered_review.json` records the reviewed PDF hash, page-by-page comparisons, caption locations and findings. This is a rendering and submission-consistency review; it does not establish public data access, both authors' approval or editorial acceptance. The scientific numerical baseline was already checked in `manuscript_q1/results/q1_verification_report.json`; no research results were changed during this review.
