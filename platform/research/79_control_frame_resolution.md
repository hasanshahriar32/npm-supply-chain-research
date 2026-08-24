# Control-Frame Resolution: Explicit Release Labels Do Not Yet Create a Primary Temporal Benchmark

**Status:** Completed evidence-gate review; **primary future-compromise control frame remains blocked.**  
**Scope:** The public Amalfi ICSE 2022 `basic-corpus.csv`, frozen at commit `9d15930a52dd1949615005dce240bb628cec7860`, and registry-provenance checks.  
**Prepared by:** Manus AI  
**Artifact date:** 24 August 2026

## Decision

The Amalfi artifact supplies a useful, compact source of **explicit package-version release labels**, not a valid control population for the pre-registered future-compromise benchmark. The corpus has 1,790 labelled rows—643 `malicious` and 1,147 `benign`—each with an exact package version and content hash. Its public documentation states that the basic corpus is manually labelled, whereas its daily-release files contain unreviewed `not triaged` rows. [1]

That distinction matters. The 1,147 benign rows are not inferred from the absence of a known incident, but neither are they a population-level “no future compromise” sample. The basic corpus is a detection dataset centred on known malicious-package families; it does not expose an individual review time, future-outcome horizon, or probability-sampled at-risk npm population. It must remain separate from the independently adjudicated compromise ledger.

## Frozen provenance and registry availability

| Measure | Result | Interpretation |
|---|---:|---|
| Frozen artifact commit | `9d15930…7860` | Committed 25 January 2022; source identity is preserved. |
| Corpus SHA-256 | `f0b911…18e7` | Raw CSV checksum recorded in the diagnostics. |
| Explicit labelled release rows | 1,790 | 643 malicious; 1,147 benign. |
| Distinct package names | 444 | Version rows within a package are correlated and cannot be treated as independent attacks. |
| Retained registry version objects | 1,102 | Version-level registry metadata is presently available. |
| Retained malicious / benign rows | 9 / 1,093 | Severe label-associated retention imbalance; not suitable for release-classification fitting. |
| Missing or unretained malicious / benign rows | 634 / 54 | Must not be imputed; availability is demonstrably outcome-related. |

The label-specific provenance ledger records the original content hash, artifact commit, present registry availability, version publication time where retained, and a registry-response checksum. It assigns every row the scope `retrospective_release_classification_sensitivity_only` and marks it **excluded** from the primary temporal benchmark.

## Evidence-gate result

| Requested use | Decision | Reason |
|---|---|---|
| Explicit benign release labels | Available for a separate retrospective corpus | The source directly assigns version-level labels. [1] |
| Primary future-compromise controls | **Blocked** | No row-level event/review horizon and no at-risk population definition. |
| Incident-family temporal ranking or calibration | **Blocked** | Corpus construction and target differ from the primary compromise target. |
| Package-grouped release-classification sensitivity | Blocked in the current registry reconstruction | Only 9 malicious rows are retained versus 1,093 benign rows; any fitted result would be dominated by outcome-linked deletion/retention. |
| Imputation of unretained versions | Prohibited | 688 unavailable version objects create non-random availability risk. |

> **Primary conclusion.** Explicit benign labels improve the evidence available for a separate release-classification sensitivity corpus, but they do not turn arbitrary registry rows into benign controls and do not satisfy the project’s pre-registered future-compromise control requirement.

## Required next data contract

The primary benchmark can proceed only when a source provides all three components together: an immutable incident-coverage snapshot, a documented outcome horizon, and a population or explicitly sampled at-risk frame at each cutoff. That source must support grouping by incident family and preserve exposure/feature availability before the outcome window. Until then, the program retains the no-fit result for ranking, PR-AUC, Recall@K, calibration, logistic regression, and uncertainty estimates.

## Reproducibility artifacts

The frozen input is `76_amalfi_basic_corpus.csv`; its source commit is stored in `76_amalfi_artifact_commit.json`. `build-amalfi-release-sensitivity-ledger.mjs` emits `77_amalfi_release_sensitivity_ledger.csv` and `77_amalfi_release_sensitivity_diagnostics.json`. `analyze-amalfi-release-sensitivity.mjs` emits `78_amalfi_release_sensitivity_gate.json`. These artifacts are independent of the incident-family temporal ledger.

## References

[1] [A. Sejfia and M. Schäfer, “Practical Automated Detection of Malicious npm Packages,” ICSE 2022 artifact repository](https://github.com/githubnext/amalfi-artifact).
