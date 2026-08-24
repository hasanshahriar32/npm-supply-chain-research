# Package-Level Temporal Companion Protocol

## Why a companion protocol is necessary

The exact-version pilot produced a pre-registered boundary result: affected Axios releases were published at or after the event cutoff, while their registry version objects are no longer available. A version cannot be scored before it exists. The correct next unit is therefore a **package observation immediately before a documented incident**, with the later affected version retained only as outcome evidence.

This companion protocol does not replace the package-version target in the main study. It provides a strictly weaker but valid feasibility test: whether reproducible package-level snapshots and dated package-event labels can be joined without using post-event metadata.

## Observation construction

For each incident package, define `feature_cutoff = event_start_utc - 1 millisecond`. Select the latest registry version whose publication timestamp is at or before that cutoff. Extract only that version object’s direct dependency map, lifecycle-script fields, integrity flag, publication timestamp, and count of package versions released by the cutoff. Preserve the event’s affected versions as label evidence but never as features.

| Field | Interpretation | Leakage rule |
|---|---|---|
| `pre_event_latest_version` | Last registry-visible version before event | Must have `time[version] <= cutoff` |
| `direct_dependency_count` | Direct declaration count for selected version | No current transitive resolution |
| `has_install_script` | Lifecycle-script indicator in selected version | No package payload download or execution |
| `package_age_days` | Time from first registry publication to cutoff | Registry timestamp only |
| `prior_version_count` | Published versions at/before cutoff | Version-time map only |
| `incident_family` | Group for split and uncertainty logic | Never split related rows across train/test |

## Label ledger policy

The ledger includes the 2021 `ua-parser-js`, `coa`, and `rc` compromise versions identified by Mandiant; CISA independently confirms the three `ua-parser-js` versions. [1] [2] It includes the 2026 CISA Axios and injected `plain-crypto-js` evidence separately. [3] The 2021 records form one `unc3379_2021` family; Axios and `plain-crypto-js` form one `axios_2026` family. Thus the ledger contains several package observations but only **two independent incident families**.

The controls are a pre-specified, real-package sentinel set with `no_known_event_in_selected_sources`, not a benign ground truth. They support feature-availability diagnostics only. They must not be used to estimate a false-positive rate or report discrimination metrics.

## Baseline and calibration gate

The script produces transparent features and a protocol gate. It must not fit a logistic model, rank model, calibration curve, PR-AUC, or confidence interval unless at least ten strict future positives from at least five independent incident families and a defensible negative/control design are available. Until then it reports only descriptive coverage and the fact that calibration inference is blocked.

## References

[1]: https://cloud.google.com/blog/topics/threat-intelligence/supply-chain-node-js/ "Mandiant: No Unaccompanied Miners"
[2]: https://www.cisa.gov/news-events/alerts/2021/10/22/malware-discovered-popular-npm-package-ua-parser-js "CISA: Malware Discovered in Popular NPM Package, ua-parser-js"
[3]: https://www.cisa.gov/news-events/alerts/2026/04/20/supply-chain-compromise-impacts-axios-node-package-manager "CISA: Supply Chain Compromise Impacts Axios Node Package Manager"
