# Prospective cohort feasibility freeze

A uniform seeded sample of 100 package names was selected before metadata requests. Official npm metadata was captured for 90 packages. The other request outcomes are retained as missingness, without replacement or relabeling.

Feature cutoff: **2026-10-20T00:48:38.569362+06:00** (Asia/Dhaka). The 90-day interval ends **2027-01-18T00:48:38.569362+06:00**. All outcomes are pending. No model was fitted and no forecasting performance exists.

`selection_manifest.json` fixes the sampling frame, seed and selected names before requests. `capture_records.jsonl` contains status, capture times, response hashes and allowlisted metadata features. `cohort_status.json` fixes the exact collection cutoff and follow-up interval. Raw responses, emails, tarballs and install-script bodies are not retained.

This is a completed data-acquisition feasibility step. It is not a preregistered powered benchmark: final surveillance sources, censoring rules and analysis plan still require freezing before follow-up outcomes are examined. Absence from an advisory feed never certifies a package benign.
