# Bounded `@bitwarden/cli` April 2026 candidate screen

**Status:** Continuing evidence screen; **not** a ledger admission.  
**Date:** 27 August 2026.  
**Scope:** One package-event candidate, `@bitwarden/cli@2026.4.0`; no other Checkmarx-related package or event is added, grouped, or inferred.

## Bounded source observations

Bitwarden’s public incident statement says that a malicious package was briefly distributed through the npm delivery path for `@bitwarden/cli@2026.4.0` between 5:57 PM and 7:30 PM ET on 22 April 2026. It identifies a broader Checkmarx supply-chain incident but specifies that the incident affected npm distribution rather than the integrity of the legitimate Bitwarden CLI codebase. [1]

StepSecurity’s independently reviewed technical account identifies the same `@bitwarden/cli@2026.4.0` release as compromised on npm. [2] GitHub’s public advisory for CVE-2026-42994, sourced from the National Vulnerability Database, independently states that Bitwarden CLI `2026.4.0` obtained from npm during the stated April 22 window had embedded malicious code and describes it as related to the Checkmarx incident. [3]

| Candidate question | Current bounded finding | Permitted interpretation |
|---|---|---|
| Package event | Bitwarden records a malicious npm distribution path for `@bitwarden/cli@2026.4.0`; StepSecurity separately identifies the same release as compromised. | Supports continued one-package screening only. |
| Exact version set | All retrieved sources converge on `2026.4.0` only. | A single finite candidate target exists; no additional versions may be inferred. |
| Campaign context | Sources call the incident related to a broader Checkmarx event. | No campaign census, multi-package expansion, relationship to a governed family, or statistical-independence claim is made. |
| Pre-event source object | Not yet inspected. | No cutoff, predecessor, ledger row, snapshot, declaration, or graph edge exists. |

## Interpretation boundary

This source screen creates **zero** controls, benign labels, historical installation records, dependency reach or blast-radius claims, ranks, authority values, scores, calibration results, intervals, models, or predictive metrics. It does not download, extract, install, or execute package material. The next step, if any, is a metadata-only official npm registry time-map and retained-predecessor assessment. Registry metadata can establish strict cutoff selection and current object retention only; it cannot establish historical installation, downstream reach, current publisher state, causality, or a non-event label.

## References

[1] [Bitwarden, “Bitwarden Statement on Checkmarx Supply Chain Incident,” 23 April 2026](https://community.bitwarden.com/t/bitwarden-statement-on-checkmarx-supply-chain-incident/96127).

[2] [StepSecurity, “Bitwarden CLI Hijacked on npm,” 23 April 2026](https://www.stepsecurity.io/blog/bitwarden-cli-hijacked-on-npm-bun-staged-credential-stealer-targets-developers-github-actions-and-ai-tools).

[3] [GitHub Advisory Database, CVE-2026-42994](https://github.com/advisories/GHSA-999x-2wm3-jfx8).
