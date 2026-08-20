# Seed Incident Registry

## Purpose

This registry is a **high-confidence seed set** for a future temporal benchmark. It is intentionally small. A record is included only when it has an explicit package/version or campaign anchor, an evidence URL, an event-time field, a public-detection-time field, a confidence grade, and a reviewer rationale. It is not a complete list of npm incidents and must not be used as a training set without expansion and grouped temporal evaluation.

| Record | Class | Event date | Inclusion decision | Evidence |
|---|---|---|---|---|
| `axios@1.14.1` | Confirmed targeted compromise | 31 March 2026 | Primary-target eligible | CISA identifies this affected version and the injected malicious dependency. [1] |
| `axios@0.30.4` | Confirmed targeted compromise | 31 March 2026 | Primary-target eligible | CISA identifies this affected version and the injected malicious dependency. [1] |
| `plain-crypto-js@4.2.1` | Confirmed malicious publication | 31 March 2026 | Primary-target eligible, analyzed separately | The injected malicious dependency is not the same analytical object as the compromised Axios publisher target. [1] |
| Shai-Hulud campaign | Confirmed widespread compromise | 15 September 2025 | Campaign-only until version-specific corroboration | CISA and CERT/CC confirm the campaign and its automated propagation, but this row contains no named package/version. [2] [3] |

## Governance rule

The benchmark’s primary positive class accepts only version-specific, independently supportable records. Campaign-associated packages, ordinary vulnerabilities, source-only allegations, and rows whose time or affected version cannot be corroborated remain excluded or are reported in a sensitivity analysis. The full machine-readable provenance is in `52_seed_incident_registry.csv`.

## References

[1]: https://www.cisa.gov/news-events/alerts/2026/04/20/supply-chain-compromise-impacts-axios-node-package-manager "CISA, Supply Chain Compromise Impacts Axios Node Package Manager"
[2]: https://www.cisa.gov/news-events/alerts/2025/09/23/widespread-supply-chain-compromise-impacting-npm-ecosystem "CISA, Widespread Supply Chain Compromise Impacting npm Ecosystem"
[3]: https://kb.cert.org/vuls/id/534320 "CERT/CC, VU#534320"
