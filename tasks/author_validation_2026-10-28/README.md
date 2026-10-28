# Author validation task

Start with **Author_Validation_Guide.pdf**. It explains the complete workflow for Shahriar Hasan and Md. Ashikul Islam.

1. Open `Evidence_Index.html` in your browser.
2. Each author independently completes their own file in `reviews/` for the same 120 endpoints.
3. Preserve both initial files before comparing labels or resolving disagreements.
4. Return the completed files and actual contribution descriptions for analysis and manuscript integration.
5. Read and approve the exact final manuscript yourselves.

The sheets are intentionally unfilled. This folder records a task, not completed reviews. The endpoint audit is optional additional research; actual author approval is required for submission. The corrected manuscript already describes the absence of manual validation.

`Evidence_Packet.md` provides the detailed original source links. `templates/` contains unfilled contribution, session-log and approval forms. `validate_reviews.py` checks only local sheet structure/completeness and does not alter records or calculate agreement. The analysis program reads the canonical repository sheets, so these task copies must be handed back or explicitly integrated before analysis.

Rebuild the PDF with `python3 build_guide.py` (requires Tectonic). This folder and its ZIP can be shared between the two authors; keep the initial label files separate during review. The task includes frozen request records and readable source-text copies under `evidence/`, linked from the HTML index. Extract the complete ZIP to use them offline. Public pinned and live API links need internet access. No automated label summaries are included.
