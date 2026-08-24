# Temporal Incident-Label Adjudication Register

**Status:** High-confidence, package-event evidence register for the temporal pilot.  
**Prepared by:** Manus AI  
**Interpretation:** An incident record is an evidence anchor, not a negative label, a downstream-exposure estimate, or an independent model sample.

## Register purpose

This register expands the earlier seed labels into a compact, reviewable set of independently documented npm package-event records. It preserves the difference between a package whose publisher account was compromised, a maliciously published package, and an affected downstream dependency. Each row retains a primary evidence URL, an event-family identifier, the exact affected release(s) reported by that source, and an explicit target-eligibility decision.

The register includes twelve package-event records in eight independent incident families. The `unc3379_2021` records must be evaluated as one correlated campaign family, not three independent successful attacks. CISA documents the malicious `ua-parser-js` releases, while Mandiant identifies the affected `coa` and `rc` releases from the same 2021 Node.js campaign. [1] [2] npm's incident account documents `event-stream@3.3.6`, ESLint's postmortem provides the affected ESLint releases and timestamp, and CISA documents the Axios-related releases and injected package. [3] [4] [5] The 2026 `node-ipc` record is independently corroborated by a same-day SafeDep incident report and the OpenSSF OSV record `MAL-2026-3744`. [6] [7] The `@emcd-vue/auth` record is a distinct `oob.moika.tech` dependency-confusion campaign family with exact affected versions and earliest registry publication time corroborated by SafeDep and OpenSSF `MAL-2026-5163`. [8] [9] The bounded `wenk` record represents one distinct November 2025 Shai-Hulud second-wave family: the frozen Wiz IOC CSV and OpenSSF `MAL-2025-191155` agree on versions `1.0.9` and `1.0.10`, while the OpenSSF record retains independent Aikido, Wiz, and StepSecurity campaign references. [11] [12] [13] [14] The bounded `amapcn` record represents one distinct May 2026 Mini Shai-Hulud `atool` family: SafeDep and OpenSSF `MAL-2026-4127` agree on versions `0.2.2` and `0.3.2`, the latter preserving Amazon Inspector and Google Open Source Security origin provenance and a Socket campaign reference. [15] [16] [17]

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
| `node-ipc-2026-05-14` | `node_ipc_2026` | 2026-05-14 14:25:30.311 | `9.1.6`, `9.2.3`, `12.0.1` | OpenSSF OSV and independent technical report | Included; earliest malicious publication is the strict cutoff. |
| `emcd-vue-auth-2026-06-01` | `moika_dependency_confusion_2026` | 2026-06-01 07:04:12.358 | `6.4.8`, `6.4.9`, `6.4.5`, `7.0.0` | OpenSSF OSV and independent technical report | Included; earliest documented malicious publication is the strict cutoff. |
| `wenk-2025-11-24` | `shai_hulud_second_coming_2025` | 2025-11-24 10:06:12.376 | `1.0.9`, `1.0.10` | OpenSSF OSV and frozen independent technical IOC list | Included as one bounded second-wave family record; `wenk@1.0.9` is the strict cutoff. |
| `amapcn-2026-05-19` | `mini_shai_hulud_atool_2026` | 2026-05-19 01:56:40.925 | `0.2.2`, `0.3.2` | OpenSSF OSV and independent technical reports | Included as one bounded atool-family record; `amapcn@0.2.2` is the strict cutoff. |

## Adjudication constraints

Each recorded outcome uses the event anchor only to define a feature cutoff. The feature snapshot ends immediately before the anchor; no attributes from the malicious release, remediation, public alert, or later registry state may be included as features. This register does not assert that no other package was compromised, so it cannot by itself provide a benign or negative control population.

The 2026 Axios family includes two distinct package roles. `axios` is a publisher-compromise target, while `plain-crypto-js` is retained as the injected malicious dependency. Treating both as interchangeable targets would blur causal role and inflate inference. The same care applies to the 2021 records: the shared campaign identifier is retained so a future split or bootstrap can operate at the family level.

## Relationship to the graph and calibration artifacts

Ten of the twelve records support an exact pre-event source-package metadata snapshot. The `plain-crypto-js` and `@emcd-vue/auth` records remain `not_available` in the current registry reconstruction, so they do not yield source-version dependency declarations. The bounded `wenk` record selects `wenk@1.0.8` before its registry-derived cutoff and has no runtime dependency declarations; `amapcn@0.1.2` is the exact pre-cutoff source object for the Mini Shai-Hulud record and declares four runtime dependencies. The associated direct-edge ledger and baseline gate are available in the temporal findings report; neither turns this evidence register into a predictive benchmark.

## Human-vetted positive-catalogue overlap

The current npm manifest from the human-vetted DataDog Malicious Software Packages Dataset was frozen at repository commit `6de6e895805a8415f4cc6093f870587a768c67cd` and compared with the twelve primary records. [10] The overlap is intentionally limited to corroboration: the positive-only manifest has no row-level event time, evidence URL, campaign-family assignment, or negative labels, and its sample naming convention refers to discovery—not publication—dates.

| Primary record outcome | Count | Permitted interpretation |
|---|---:|---|
| Exact affected-version membership | 3 | The manifest lists the Axios, node-ipc, and amapcn affected version sets, corroborating positive package-version membership only. |
| Package present, versions unspecified | 2 | `plain-crypto-js` and `wenk` are present but have `null` manifest values; no version-specific assertion follows. |
| Package absent from current manifest | 7 | No conclusion; absence is not benign evidence and does not alter the primary record. |
| New primary labels, dates, families, or controls | 0 | The primary ledger remains authoritative. |

The complete overlap artifact (`80_datadog_positive_membership_overlap.json`) stores the source SHA-256 and commit identifier. It neither adds incident records nor changes any primary cutoff or target decision.

## References

[1] [CISA, “Malware Discovered in Popular npm Package ua-parser-js,” 22 October 2021](https://www.cisa.gov/news-events/alerts/2021/10/22/malware-discovered-popular-npm-package-ua-parser-js).

[2] [Mandiant, “Supply Chain Compromise Affects Node.js Package Manager,” 2021](https://cloud.google.com/blog/topics/threat-intelligence/supply-chain-node-js/).

[3] [npm, “Details about the event-stream incident,” 2018](https://blog.npmjs.org/post/180565383195/details-about-the-event-stream-incident).

[4] [ESLint, “Postmortem for Malicious Package Publishes,” 2018](https://eslint.org/blog/2018/07/postmortem-for-malicious-package-publishes/).

[5] [CISA, “Supply Chain Compromise Impacts Axios Node Package Manager,” 20 April 2026](https://www.cisa.gov/news-events/alerts/2026/04/20/supply-chain-compromise-impacts-axios-node-package-manager).

[6] [SafeDep, “Compromised node-ipc on npm: Credential Stealer via DNS Exfiltration,” 14 May 2026](https://safedep.io/malicious-node-ipc-npm-compromise/).

[7] [OpenSSF Malicious Packages, “MAL-2026-3744: Malicious code in node-ipc (npm)”](https://github.com/ossf/malicious-packages/blob/main/osv/malicious/npm/node-ipc/MAL-2026-3744.json).

[8] [SafeDep, “183 npm Packages Target Cloud and Finance via oob.moika.tech,” 28 May 2026](https://safedep.io/oob-moika-tech-dependency-confusion-campaign/).

[9] [OpenSSF Malicious Packages, “MAL-2026-5163: Malicious code in @emcd-vue/auth (npm)”](https://github.com/ossf/malicious-packages/blob/main/osv/malicious/npm/%40emcd-vue/auth/MAL-2026-5163.json).

[10] [DataDog, “Malicious Software Packages Dataset”](https://github.com/DataDog/malicious-software-packages-dataset).

[11] [OpenSSF Malicious Packages, “MAL-2025-191155: Malicious code in wenk (npm)”](https://github.com/ossf/malicious-packages/blob/c04e75e38121768f82fef0495de77b68b7054d7c/osv/malicious/npm/wenk/MAL-2025-191155.json).

[12] [Wiz Research IOCs, frozen `shai-hulud-2-packages.csv` at commit `22752e7`](https://github.com/wiz-sec-public/wiz-research-iocs/blob/22752e7cc55ece6a053e3277b60b914e0260e65d/reports/shai-hulud-2-packages.csv).

[13] [Aikido Security, “Shai Hulud Launches Second Supply-Chain Attack,” 24 November 2025](https://www.aikido.dev/blog/shai-hulud-strikes-again-hitting-zapier-ensdomains).

[14] [StepSecurity, “Sha1-Hulud: The Second Coming,” 23 November 2025](https://www.stepsecurity.io/blog/sha1-hulud-the-second-coming-zapier-ens-domains-and-other-prominent-npm-packages-compromised).

[15] [SafeDep, “Mini Shai-Hulud Strikes Again: 317 npm Packages Compromised,” 19 May 2026](https://safedep.io/mini-shai-hulud-strikes-again-314-npm-packages-compromised/).

[16] [OpenSSF Malicious Packages, “MAL-2026-4127: Malicious code in amapcn (npm)”](https://github.com/ossf/malicious-packages/blob/c04e75e38121768f82fef0495de77b68b7054d7c/osv/malicious/npm/amapcn/MAL-2026-4127.json).

[17] [Socket Research, “Mini Shai-Hulud Hits @antv Ecosystem, 639 Compromised npm Package Versions,” 19 May 2026](https://socket.dev/blog/antv-packages-compromised).
