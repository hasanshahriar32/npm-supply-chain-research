# Temporal Incident-Label Adjudication Register

**Status:** High-confidence, package-event evidence register for the temporal pilot.  
**Prepared by:** Manus AI  
**Interpretation:** An incident record is an evidence anchor, not a negative label, a downstream-exposure estimate, or an independent model sample.

## Register purpose

This register expands the earlier seed labels into a compact, reviewable set of independently documented npm package-event records. It preserves the difference between a package whose publisher account was compromised, a maliciously published package, and an affected downstream dependency. Each row retains a primary evidence URL, an event-family identifier, the exact affected release(s) reported by that source, and an explicit target-eligibility decision.

The register includes eight package-event records in four independent incident families. The `unc3379_2021` records must be evaluated as one correlated campaign family, not three independent successful attacks. CISA documents the malicious `ua-parser-js` releases, while Mandiant identifies the affected `coa` and `rc` releases from the same 2021 Node.js campaign. [1] [2] npm's incident account documents `event-stream@3.3.6`, ESLint's postmortem provides the affected ESLint releases and timestamp, and CISA documents the Axios-related releases and injected package. [3] [4] [5]

| Record | Incident family | Event anchor (UTC) | Affected release(s) | Evidence tier | Target decision |
|---|---|---|---|---|---|
| `ua-parser-js-2021-10-22` | `unc3379_2021` | 2021-10-22 12:15 | `0.7.29`, `0.8.0`, `1.0.0` | Government and technical | Included; confirmed targeted compromise. |
| `coa-2021-11-04` | `unc3379_2021` | 2021-11-04 00:00 | `2.0.3`, `2.0.4`, `2.1.1`, `2.1.3`, `3.1.3` | Independent technical | Included; confirmed targeted compromise. |
| `rc-2021-11-04` | `unc3379_2021` | 2021-11-04 00:00 | `1.2.9`, `1.3.9`, `2.3.9` | Independent technical | Included; confirmed targeted compromise. |
| `axios-2026-03-31` | `axios_2026` | 2026-03-31 00:00 | `1.14.1`, `0.30.4` | Government | Included; compromised publisher target. |
| `plain-crypto-js-2026-03-31` | `axios_2026` | 2026-03-31 00:00 | `4.2.1` | Government | Included separately; malicious publication, not the Axios publisher target. |
| `event-stream-2018-11-26` | `event_stream_2018` | 2018-11-26 00:00 | `3.3.6` | npm incident report | Included; confirmed targeted compromise. |
| `eslint-scope-2018-07-12` | `eslint_2018` | 2018-07-12 10:40 | `3.7.2` | Maintainer postmortem | Included; confirmed targeted compromise. |
| `eslint-config-eslint-2018-07-12` | `eslint_2018` | 2018-07-12 09:49 | `5.0.2` | Maintainer postmortem | Included; confirmed targeted compromise. |

## Adjudication constraints

Each recorded outcome uses the event anchor only to define a feature cutoff. The feature snapshot ends immediately before the anchor; no attributes from the malicious release, remediation, public alert, or later registry state may be included as features. This register does not assert that no other package was compromised, so it cannot by itself provide a benign or negative control population.

The 2026 Axios family includes two distinct package roles. `axios` is a publisher-compromise target, while `plain-crypto-js` is retained as the injected malicious dependency. Treating both as interchangeable targets would blur causal role and inflate inference. The same care applies to the 2021 records: the shared campaign identifier is retained so a future split or bootstrap can operate at the family level.

## Relationship to the graph and calibration artifacts

Seven of the eight records support an exact pre-event source-package metadata snapshot. The `plain-crypto-js` record remains `not_available` in the current registry reconstruction, so it does not yield a source-version dependency declaration. The associated direct-edge ledger and baseline gate are available in the temporal findings report; neither turns this evidence register into a predictive benchmark.

## References

[1] [CISA, “Malware Discovered in Popular npm Package ua-parser-js,” 22 October 2021](https://www.cisa.gov/news-events/alerts/2021/10/22/malware-discovered-popular-npm-package-ua-parser-js).

[2] [Mandiant, “Supply Chain Compromise Affects Node.js Package Manager,” 2021](https://cloud.google.com/blog/topics/threat-intelligence/supply-chain-node-js/).

[3] [npm, “Details about the event-stream incident,” 2018](https://blog.npmjs.org/post/180565383195/details-about-the-event-stream-incident).

[4] [ESLint, “Postmortem for Malicious Package Publishes,” 2018](https://eslint.org/blog/2018/07/postmortem-for-malicious-package-publishes/).

[5] [CISA, “Supply Chain Compromise Impacts Axios Node Package Manager,” 20 April 2026](https://www.cisa.gov/news-events/alerts/2026/04/20/supply-chain-compromise-impacts-axios-node-package-manager).
