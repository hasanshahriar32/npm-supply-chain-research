# Temporal Incident-Label Adjudication Register

**Status:** High-confidence, package-event evidence register for the temporal pilot.  
**Prepared by:** Manus AI  
**Interpretation:** An incident record is an evidence anchor, not a negative label, a downstream-exposure estimate, or an independent model sample.

## Register purpose

This register expands the earlier seed labels into a compact, reviewable set of independently documented npm package-event records. It preserves the difference between a package whose publisher account was compromised, a maliciously published package, and an affected downstream dependency. Each row retains a primary evidence URL, an event-family identifier, the exact affected release(s) reported by that source, and an explicit target-eligibility decision.

The register began with sixteen package-event records in eleven incident families and is incrementally extended only through this bounded evidence process. The `unc3379_2021` records must be evaluated as one correlated campaign family, not three independent successful attacks. CISA documents the malicious `ua-parser-js` releases, while Mandiant identifies the affected `coa` and `rc` releases from the same 2021 Node.js campaign. [1] [2] npm's incident account documents `event-stream@3.3.6`, ESLint's postmortem provides the affected ESLint releases and timestamp, and CISA documents the Axios-related releases and injected package. [3] [4] [5] The 2026 `node-ipc` record is independently corroborated by a same-day SafeDep incident report and the OpenSSF OSV record `MAL-2026-3744`. [6] [7] The `@emcd-vue/auth` record is a distinct `oob.moika.tech` dependency-confusion campaign family with exact affected versions and earliest registry publication time corroborated by SafeDep and OpenSSF `MAL-2026-5163`. [8] [9] The bounded `wenk` record represents one distinct November 2025 Shai-Hulud second-wave family: the frozen Wiz IOC CSV and OpenSSF `MAL-2025-191155` agree on versions `1.0.9` and `1.0.10`, while the OpenSSF record retains independent Aikido, Wiz, and StepSecurity campaign references. [11] [12] [13] [14] The bounded `amapcn` record represents one distinct May 2026 Mini Shai-Hulud `atool` family: SafeDep and OpenSSF `MAL-2026-4127` agree on versions `0.2.2` and `0.3.2`, the latter preserving Amazon Inspector and Google Open Source Security origin provenance and a Socket campaign reference. [15] [16] [17] The bounded `is` record is a distinct July 2025 maintainer-compromise family: frozen OpenSSF `MAL-2025-6020`, a dated StepSecurity report, and the project maintainer’s v3.3.2 changelog agree that `is@3.3.1` and `5.0.0` contained malware from a hijacked account. [18] [19] [20] The bounded August 2026 `keyv` record is one Keyv/Cacheable campaign-family observation: frozen OpenSSF `MAL-2026-11524`, a frozen Wiz IOC list, and independent Snyk research agree on `keyv@6.0.0`; its earlier registry timestamp fixes the cutoff. Wiz describes its payload as Mini Shai-Hulud-descended, so the separate dated family is not asserted statistically independent from the May 2026 `atool` family. [21] [22] [23] [24] The two related 2022 `colors` and `faker` records are independently corroborated as intentional breaking publications by Snyk, Sonatype, and Russ Cox; they form one shared-maintainer family and one future validation unit, not two independent observations. [25] [26] [27]

> **Current amendment — 27 August 2026.** The active register now contains **30 package-event records in 24 incident families**. The March 2022 `node-ipc` protestware record is distinct from the May 2026 `node-ipc` compromise and forms its own family and future validation unit. The bounded March 2026 `react-native-country-select@0.3.91`, April 2026 `@bitwarden/cli`, May 2026 `@common-stack/generate-plugin`, `html-to-gutenberg`, March 2025 `country-currency-map`, October 2024 `@lottiefiles/lottie-player`, August 2025 `nx`, December 2024 `@solana/web3.js`, December 2023 Ledger Connect Kit, July 2025 `eslint-config-prettier`, and July 2026 Jscrambler records each remain separate units. The React Native sources document a same-day shared-publisher context with a separately named package but do not authorize an additional row, relationship to an existing governed family, or independence claim. The Bitwarden row has documented broader Checkmarx context but does not expand into further package records or establish a relationship to an existing governed family. The bounded September 2025 Debug and Chalk records remain in one shared `qix_npm_phishing_september_2025` family and one future validation unit. None establishes a campaign-complete census or turns any package row into an independent sample.

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
| `node-ipc-2022-03-07` | `node_ipc_march_2022_maintainer_protestware` | 2022-03-07 11:03:59.179 | `10.1.1`, `10.1.2` | GitHub reviewed advisory, independent technical report, and NVD | Included; strict registry cutoff selects retained `node-ipc@10.1.0`. Separate from the 2026 `node-ipc` family. [32] [33] [34] [35] |
| `emcd-vue-auth-2026-06-01` | `moika_dependency_confusion_2026` | 2026-06-01 07:04:12.358 | `6.4.8`, `6.4.9`, `6.4.5`, `7.0.0` | OpenSSF OSV and independent technical report | Included; earliest documented malicious publication is the strict cutoff. |
| `wenk-2025-11-24` | `shai_hulud_second_coming_2025` | 2025-11-24 10:06:12.376 | `1.0.9`, `1.0.10` | OpenSSF OSV and frozen independent technical IOC list | Included as one bounded second-wave family record; `wenk@1.0.9` is the strict cutoff. |
| `amapcn-2026-05-19` | `mini_shai_hulud_atool_2026` | 2026-05-19 01:56:40.925 | `0.2.2`, `0.3.2` | OpenSSF OSV and independent technical reports | Included as one bounded atool-family record; `amapcn@0.2.2` is the strict cutoff. |
| `is-2025-07-19` | `is_maintainer_compromise_2025` | 2025-07-19 11:40:30.778 | `3.3.1`, `5.0.0` | Frozen OpenSSF OSV, maintainer remediation, and independent technical report | Included as one bounded family record; `is@3.3.1` is the strict cutoff. |
| `keyv-2026-08-04` | `keyv_cacheable_august_2026` | 2026-08-04 09:35:00.763 | `6.0.0` | Frozen OpenSSF OSV, frozen Wiz IOC list, and independent technical report | Included as one bounded Keyv/Cacheable campaign-family record; `keyv@6.0.0` is the strict cutoff. Payload ancestry does not establish cross-campaign independence from the `atool` Mini Shai-Hulud family. |
| `colors-2022-01-08` | `colors_faker_protestware_2022` | 2022-01-08 04:24:16.448 | `1.4.44-liberty-2`, `1.4.1`, `1.4.2` | Independent technical and vendor reports | Included; earliest assessed official registry publication is the strict cutoff. Related to faker as one shared-maintainer family. |
| `faker-2022-01-05` | `colors_faker_protestware_2022` | 2022-01-05 01:38:36.409 | `6.6.6` | Independent technical and vendor reports | Included; official registry publication is the strict cutoff. Related to colors as one shared-maintainer family. |
| `debug-2025-09-08` | `qix_npm_phishing_september_2025` | 2025-09-08 13:12:39.973 | `4.4.2` | Maintainer and independent technical reports | Included; official registry publication is the strict cutoff and selects retained `debug@4.4.1`. One bounded family record only. [28] [29] [30] [31] |
| `solana-web3-js-2024-12-03` | `solana_web3_js_publish_access_compromise_2024` | 2024-12-03 15:10:07.122 | `@solana/web3.js@1.95.6`, `1.95.7` | Project advisory and independent technical report | Included; the all-stream registry time-map rule selects retained `2.1.0-canary-20241203100809`, with no same-branch substitution. One bounded family record only. |
| `chalk-2025-09-08` | `qix_npm_phishing_september_2025` | 2025-09-08 13:13:05.239 | `5.6.1` | Maintainer and independent technical reports | Included; official registry publication is the strict cutoff and selects retained `chalk@5.6.0`. Shares the Debug Qix family and validation unit; not an independent observation. |
| `ledger-connect-kit-2023-12-14` | `ledger_connect_kit_npm_account_compromise_2023` | 2023-12-14 08:49:04.310 | `@ledgerhq/connect-kit@1.1.5`, `1.1.6`, `1.1.7` | Primary and independent technical reports | Included; the earliest official affected-version publication defines the cutoff and selects retained `@ledgerhq/connect-kit@1.1.4`. One bounded family and validation unit only. |
| `jscrambler-2026-07-11` | `jscrambler_npm_token_compromise_2026` | 2026-07-11 15:12:40.410 | `jscrambler@8.14.0`, `8.16.0`, `8.17.0`, `8.18.0`, `8.20.0` | Primary and independent technical reports | Included; the earliest official affected-version publication defines the cutoff and selects retained `jscrambler@8.13.0`. One bounded family and validation unit only. |
| `lottie-player-2024-10-30` | `lottie_player_npm_account_takeover_2024` | 2024-10-30 20:12:15.375 | `@lottiefiles/lottie-player@2.0.5`, `2.0.6`, `2.0.7` | Primary and independent technical reports | Included; the earliest official affected-version publication defines the cutoff and selects retained `@lottiefiles/lottie-player@2.0.4`. One bounded family and validation unit only. [36] [37] [38] [39] |
| `nx-2025-08-26` | `nx_s1ngularity_publish_token_compromise_2025` | 2025-08-26 22:32:25.482 | `nx@21.5.0`, `20.9.0`, `20.10.0`, `21.6.0`, `20.11.0`, `21.7.0`, `21.8.0`, `20.12.0` | Primary, reviewed advisory, and independent technical reports | Included; the all-stream earliest affected-version cutoff selects retained `nx@21.5.0-canary.20250826-af44608`, with no same-branch substitution. One bounded family and validation unit only. [40] [41] [42] [43] [44] |
| `country-currency-map-2025-03-25` | `country_currency_map_crypto_package_hijack_2025` | 2025-03-25 09:03:00.518 | `2.1.8` | Primary and independent technical reports | Included; Sonatype and BleepingComputer independently identify the deprecated malicious `2.1.8` release. The strict cutoff selects retained `country-currency-map@2.1.7`. One bounded family and validation unit only. [45] [46] [47] |
| `html-to-gutenberg-2026-05-25` | `html_to_gutenberg_vscode_task_hijack_2026` | 2026-05-25 19:19:47.408 | `4.2.11`, `4.2.14` | Reviewed advisory and independent technical reports | Included; GitHub’s reviewed advisory identifies the exact pair and JFrog independently identifies the hijacked `4.2.11` release. The strict cutoff selects retained `html-to-gutenberg@4.2.10`. One bounded family and validation unit only; no relationship to another governed family is asserted. [48] [49] [50] [51] |
| `common-stack-generate-plugin-2026-05-21` | `common_stack_generate_plugin_polinrider_hijack_2026` | 2026-05-21 15:54:08.581 | `9.0.2-alpha.21`, `9.0.2-alpha.22` | Reviewed advisory and independent technical report | Included; Sonatype and GitHub’s reviewed malware advisory independently identify the strict two-version intersection. The strict cutoff selects retained `@common-stack/generate-plugin@9.0.2-alpha.18`. One bounded family and validation unit only; no relationship to another governed family is asserted. [52] [53] [54] |
| `bitwarden-cli-2026-04-22` | `bitwarden_cli_checkmarx_supply_chain_2026` | 2026-04-22 21:22:59.021 | `2026.4.0` | Primary and independent technical reports | Included; Bitwarden and StepSecurity identify the exact npm release, and the NVD-sourced public advisory corroborates it. The strict cutoff selects retained `@bitwarden/cli@2026.3.0`. One bounded separate family and validation unit only; documented Checkmarx context does not create more package rows or establish a relationship to another governed family. [58] [59] [60] [61] |
| `react-native-country-select-2026-03-16` | `react_native_shared_publisher_glassworm_march_2026` | 2026-03-16 10:54:18.512 | `0.3.91` | Independent technical reports | Included; StepSecurity and Aikido independently identify the strict `0.3.91` intersection. The strict cutoff selects retained `react-native-country-select@0.3.9`. Same-day shared-publisher context with a separately named package does not authorize another row, family relationship, campaign completeness, or independence claim. [62] [63] [64] |

## Adjudication constraints

Each recorded outcome uses the event anchor only to define a feature cutoff. The feature snapshot ends immediately before the anchor; no attributes from the malicious release, remediation, public alert, or later registry state may be included as features. This register does not assert that no other package was compromised, so it cannot by itself provide a benign or negative control population.

The 2026 Axios family includes two distinct package roles. `axios` is a publisher-compromise target, while `plain-crypto-js` is retained as the injected malicious dependency. Treating both as interchangeable targets would blur causal role and inflate inference. The same care applies to the 2021 records: the shared campaign identifier is retained so a future split or bootstrap can operate at the family level.

The bounded March 2026 `sbx-mask` screen is deliberately **not** a register row. Sonatype reports the malicious package in a suspected trusted-maintainer-account compromise, while GitHub’s reviewed advisory independently identifies the finite affected set `1.0.0`, `1.0.1`, and `1.0.2`. [55] [56] The official registry time map fixes the earliest at `2026-03-19T14:46:00.636Z`, but the resulting strict cutoff has no retained earlier version object: the current response holds only `0.0.1-security`. [57] This current-retention constraint neither disputes the incident nor supplies a substitute source, historical installation evidence, a control, or a non-event label.

The current reconstruction has **28 exact pre-event source snapshots** across **30 records**. `node-ipc@10.1.0` is the exact source object immediately before the March 2022 `node-ipc@10.1.1` cutoff and is distinct from the current 2026 `node-ipc@12.0.0` source object. `debug@4.4.1` is the strict source object immediately before the independently corroborated `debug@4.4.2` cutoff; `@solana/web3.js@2.1.0-canary-20241203100809` is the all-stream strict source object immediately before the earliest independently corroborated Solana cutoff and declares 18 runtime dependencies; `@lottiefiles/lottie-player@2.0.4` is the strict source object immediately before the October 2024 cutoff; `country-currency-map@2.1.7` is the strict source object immediately before the March 2025 cutoff; `@bitwarden/cli@2026.3.0` is the strict source object immediately before the April 2026 cutoff; `react-native-country-select@0.3.9` is the strict source object immediately before the March 2026 cutoff; `html-to-gutenberg@4.2.10` is the strict source object immediately before the May 2026 cutoff; `@common-stack/generate-plugin@9.0.2-alpha.18` is the strict source object immediately before the May 2026 cutoff; and the all-stream cutoff before `nx@21.5.0` selects `nx@21.5.0-canary.20250826-af44608`. The 153 direct declarations, 153 isolated cutoff-valid range approximations, and 974 depth-three registry-only sensitivity edges remain reconstruction artifacts—not installations, dependency reach, blast-radius values, or model features with causal or predictive interpretation.

## Relationship to the graph and calibration artifacts

Twenty-eight of the thirty records support an exact pre-event source-package metadata snapshot. The `plain-crypto-js` and `@emcd-vue/auth` records remain `not_available` in the current registry reconstruction, so they do not yield source-version dependency declarations. `node-ipc@10.1.0` is the exact March 2022 source object and declares four runtime dependencies; this does not alter the separate 2026 `node-ipc` record. The bounded `wenk` record selects `wenk@1.0.8` before its registry-derived cutoff and has no runtime dependency declarations; `amapcn@0.1.2` is the exact pre-cutoff source object for the Mini Shai-Hulud record and declares four runtime dependencies; `is@3.3.0` is the exact pre-cutoff source object for the July 2025 record and has no runtime dependency declarations; `keyv@6.0.0-rc.1` is the exact pre-cutoff source object for the August 2026 Keyv/Cacheable record and declares one runtime dependency; `@lottiefiles/lottie-player@2.0.4` is the exact pre-cutoff source object for the October 2024 record and declares 13 runtime dependencies; `country-currency-map@2.1.7` is the exact pre-cutoff source object for the March 2025 record and declares one runtime dependency; `@bitwarden/cli@2026.3.0` is the exact pre-cutoff source object for the April 2026 record and declares 27 runtime dependencies; `react-native-country-select@0.3.9` is the exact pre-cutoff source object for the March 2026 record and declares no runtime dependencies; `html-to-gutenberg@4.2.10` is the exact pre-cutoff source object for the May 2026 record and declares fourteen runtime dependencies; `@common-stack/generate-plugin@9.0.2-alpha.18` is the exact pre-cutoff source object for the May 2026 record and declares two runtime dependencies; `nx@21.5.0-canary.20250826-af44608` is the all-stream exact pre-cutoff source object for the August 2025 record and declares 35 runtime dependencies; and `colors@1.4.0` and `faker@5.5.3` are the exact pre-cutoff objects for the related 2022 records and each has no runtime dependency declarations. The associated direct-edge ledger and baseline gate are available in the temporal findings report; neither turns this evidence register into a predictive benchmark.

## Human-vetted positive-catalogue overlap

The current npm manifest from the human-vetted DataDog Malicious Software Packages Dataset was frozen at repository commit `6de6e895805a8415f4cc6093f870587a768c67cd` and compared with the sixteen primary records. [10] The overlap is intentionally limited to corroboration: the positive-only manifest has no row-level event time, evidence URL, campaign-family assignment, or negative labels, and its sample naming convention refers to discovery—not publication—dates.

| Primary record outcome | Count | Permitted interpretation |
|---|---:|---|
| Exact affected-version membership | 5 | The manifest lists the Axios, node-ipc, amapcn, `is`, and `keyv` affected version sets, corroborating positive package-version membership only. |
| Package present, versions unspecified | 2 | `plain-crypto-js` and `wenk` are present but have `null` manifest values; no version-specific assertion follows. |
| Package absent from current manifest | 9 | No conclusion; absence is not benign evidence and does not alter the primary record. |
| New primary labels, dates, families, or controls | 0 | The primary ledger remains authoritative. |

The complete overlap artifact (`80_datadog_positive_membership_overlap.json`) stores the source SHA-256 and commit identifier. It neither adds incident records nor changes any primary cutoff or target decision.

> **Current overlap amendment — 27 August 2026.** The positive-only manifest now compares 30 primary records: 13 have exact affected-version membership, 3 are package-present with unspecified versions, 1 is package-present without an exact version match (`node-ipc-2022-03-07`), and 13 are package-absent. Those outcomes remain corroboration or unknown only; absence and version mismatch are never benign labels or controls.

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

[18] [OpenSSF Malicious Packages, “MAL-2025-6020: Malicious code in is (npm),” frozen at commit `063a778`](https://github.com/ossf/malicious-packages/blob/063a778886548231828c8e476eecdb5c5c04fbcb/osv/malicious/npm/is/MAL-2025-6020.json).

[19] [StepSecurity, “Another npm Supply Chain Attack: The 'is' Package Compromise,” 22 July 2025](https://www.stepsecurity.io/blog/another-npm-supply-chain-attack-the-is-package-compromise).

[20] [enricomarino/is, “v3.3.2” remediation commit `0fe137a`](https://github.com/enricomarino/is/commit/0fe137a5946e4ecb0e649bd7dea48d5415a242fc).

[21] [OpenSSF Malicious Packages, “MAL-2026-11524: Malicious code in keyv (npm),” frozen at commit `88b1340754`](https://github.com/ossf/malicious-packages/blob/88b1340754c17c3d9ae43642c9b2de22b1bbfc10/osv/malicious/npm/keyv/MAL-2026-11524.json).

[22] [Wiz Research IOCs, frozen `keyv-packages.csv` at commit `22752e7`](https://github.com/wiz-sec-public/wiz-research-iocs/blob/22752e7cc55ece6a053e3277b60b914e0260e65d/reports/keyv-packages.csv).

[23] [Wiz Research, “keyv and cacheable npm Package Hijacked in Supply Chain Attack,” 4 August 2026](https://www.wiz.io/blog/keyv-and-cacheable-npm-supply-chain-attack).

[24] [Snyk, “Inside the keyv npm Compromise: preinstall Malware, Trusted Provenance, and IDE Hooks,” 4 August 2026](https://snyk.io/blog/inside-keyv-npm-compromise-preinstall-malware-trusted-provenance-ide-hooks/).

[25] [Snyk, “Open source maintainer pulls the plug on npm packages colors and faker, now what?”, 9 January 2022](https://snyk.io/blog/open-source-npm-packages-colors-faker/).

[26] [Sonatype, “npm Libraries ‘colors’ and ‘faker’ Sabotaged in Protest by Their Maintainer,” 10 January 2022](https://www.sonatype.com/blog/npm-libraries-colors-and-faker-sabotaged-in-protest-by-their-maintainer-what-to-do-now).

[27] [Russ Cox, “What NPM Should Do Today To Stop A New Colors Attack Tomorrow,” 10 January 2022](https://research.swtch.com/npm-colors).

[28] [Debug project, “Version 4.4.2 published to npm is compromised,” Issue #1005, 8 September 2025](https://github.com/debug-js/debug/issues/1005).

[29] [Wiz, “Widespread npm Supply Chain Attack: Breaking Down Impact & Scope Across Debug, Chalk, and Beyond,” 9 September 2025](https://www.wiz.io/blog/widespread-npm-supply-chain-attack-breaking-down-impact-scope-across-debug-chalk).

[30] [StepSecurity, “20+ Popular NPM Packages Compromised,” 8 September 2025](https://www.stepsecurity.io/blog/20-popular-npm-packages-compromised-chalk-debug-strip-ansi-color-convert-wrap-ansi).

[31] [npm registry metadata, `debug`](https://registry.npmjs.org/debug).

[32] [GitHub Advisory Database, “Embedded Malicious Code in node-ipc,” GHSA-97m3-w2cp-4xx6](https://github.com/advisories/GHSA-97m3-w2cp-4xx6).

[33] [Snyk, “Alert: peacenotwar module sabotages npm developers in the node-ipc package,” 16 March 2022](https://snyk.io/blog/peacenotwar-malicious-npm-node-ipc-package-vulnerability/).

[34] [NVD, “CVE-2022-23812 Detail”](https://nvd.nist.gov/vuln/detail/CVE-2022-23812).

[35] [npm registry metadata, `node-ipc`](https://registry.npmjs.org/node-ipc).

[36] [LottieFiles, “Resolution of Security Incident with @lottiefiles/lottie-player Package,” 2 November 2024](https://lottiefiles.com/blog/inside-lottiefiles/resolution-of-security-incident-with-lottiefiles-lottie-player-package).

[37] [Sonatype, “Lottie Player Compromised in Supply Chain Attack,” 31 October 2024](https://www.sonatype.com/blog/lottie-player-compromised-in-supply-chain-attack-all-you-need-to-know).

[38] [Snyk, “Lottie Player npm package compromised for crypto wallet theft,” 31 October 2024](https://snyk.io/blog/lottie-player-npm-package-compromised-crypto-wallet-theft/).

[39] [npm registry metadata, `@lottiefiles/lottie-player`](https://registry.npmjs.org/%40lottiefiles%2Flottie-player).

[40] [Nx, “S1ngularity - What Happened, How We Responded, What We Learned,” 5 September 2025](https://nx.dev/blog/s1ngularity-postmortem).

[41] [GitHub Security Advisory, “Malicious versions of Nx and some supporting plugins were published,” GHSA-cxm3-wv7p-598c](https://github.com/nrwl/nx/security/advisories/GHSA-cxm3-wv7p-598c).

[42] [Snyk, “Weaponizing AI Coding Agents for Malware in the Nx Malicious Package Security Incident,” 27 August 2025](https://snyk.io/blog/weaponizing-ai-coding-agents-for-malware-in-the-nx-malicious-package/).

[43] [StepSecurity, “s1ngularity: Popular Nx Build System Package Compromised with Data-Stealing Malware,” 27 August 2025](https://www.stepsecurity.io/blog/supply-chain-security-alert-popular-nx-build-system-package-compromised-with-data-stealing-malware).

[44] [npm registry metadata, `nx`](https://registry.npmjs.org/nx).

[45] [Sonatype, “Multiple Crypto Packages Hijacked, Turned Into Info-Stealers,” 27 March 2025](https://www.sonatype.com/blog/multiple-crypto-packages-hijacked-turned-into-info-stealers).

[46] [BleepingComputer, “Infostealer campaign compromises 10 npm packages, targets devs,” 27 March 2025](https://www.bleepingcomputer.com/news/security/infostealer-campaign-compromises-10-npm-packages-targets-devs/).

[47] [npm registry metadata, `country-currency-map`](https://registry.npmjs.org/country-currency-map).

[48] [GitHub Advisory Database, “Malware in html-to-gutenberg,” GHSA-2gqj-wrf5-35w8](https://github.com/advisories/GHSA-2gqj-wrf5-35w8).

[49] [JFrog Security Research, “Hijacked npm Packages Use Novel VSCode Autorun and Blockchain Dead Drops to Deploy a Credential/Crypto Stealer,” 24 June 2026](https://research.jfrog.com/post/hijacked-npm-vscode-tasks-blockchain/).

[50] [The Hacker News, “Hijacked npm and Go Packages Use VS Code Tasks to Deploy Python Infostealer,” 29 June 2026](https://thehackernews.com/2026/06/hijacked-npm-and-go-packages-use-vs.html).

[51] [npm registry metadata, `html-to-gutenberg`](https://registry.npmjs.org/html-to-gutenberg).

[52] [Sonatype, “Hijacked npm Package Attempts to Deliver PolinRider-Linked RAT,” 21 May 2026](https://www.sonatype.com/blog/hijacked-npm-package-attempts-to-deliver-polinrider-linked-rat).

[53] [GitHub Advisory Database, “Malware in @common-stack/generate-plugin,” GHSA-6p55-6hvr-3xmg](https://github.com/advisories/GHSA-6p55-6hvr-3xmg).

[54] [npm registry metadata, `@common-stack/generate-plugin`](https://registry.npmjs.org/%40common-stack%2Fgenerate-plugin).

[55] [Sonatype, “Sonatype Discovers Two Malicious npm Packages,” 19 March 2026](https://www.sonatype.com/blog/sonatype-discovers-two-malicious-npm-packages).

[56] [GitHub Advisory Database, “Malware in sbx-mask,” GHSA-r934-qgg3-v7fg](https://github.com/advisories/GHSA-r934-qgg3-v7fg).

[57] [npm registry metadata, `sbx-mask`](https://registry.npmjs.org/sbx-mask).

[58] [Bitwarden, “Bitwarden Statement on Checkmarx Supply Chain Incident,” 23 April 2026](https://community.bitwarden.com/t/bitwarden-statement-on-checkmarx-supply-chain-incident/96127).

[59] [StepSecurity, “Bitwarden CLI Hijacked on npm,” 23 April 2026](https://www.stepsecurity.io/blog/bitwarden-cli-hijacked-on-npm-bun-staged-credential-stealer-targets-developers-github-actions-and-ai-tools).

[60] [GitHub Advisory Database, CVE-2026-42994](https://github.com/advisories/GHSA-999x-2wm3-jfx8).

[61] [npm registry metadata, `@bitwarden/cli`](https://registry.npmjs.org/%40bitwarden%2Fcli).

[62] [StepSecurity, “Malicious npm Releases Found in Popular React Native Packages,” 16 March 2026](https://www.stepsecurity.io/blog/malicious-npm-releases-found-in-popular-react-native-packages---130k-monthly-downloads-compromised).

[63] [Aikido, “Glassworm Strikes Popular React Native Phone Number Packages,” 18 March 2026](https://www.aikido.dev/blog/glassworm-strikes-react-packages-phone-numbers).

[64] [npm registry metadata, `react-native-country-select`](https://registry.npmjs.org/react-native-country-select).
