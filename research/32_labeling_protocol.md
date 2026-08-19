# Historical Labeling Protocol

## Objective

Create a version-level, time-stamped label set for documented npm supply-chain compromises and malicious publications. The label set is for defensive research and must preserve uncertainty rather than force every advisory into a binary target.

## Evidence hierarchy

Use the strongest available evidence in this order:

1. Government or registry alert with affected package versions and event timing.
2. Maintainer or project post-mortem with affected versions and publication or removal timeline.
3. Independent technical analysis from a recognized security research organization with artifact evidence.
4. Peer-reviewed or archival incident dataset with package/version evidence.
5. OSV or GitHub Advisory entry with matching package/version data.
6. Secondary reporting or keyword-only evidence, used for discovery but not as sole confirmation.

## Label classes

| Class | Inclusion rule | Primary use |
|---|---|---|
| `confirmed_targeted_compromise` | Reliable source documents compromise of a maintainer, publisher, or package and identifies affected versions or package artifacts | Primary prediction label |
| `confirmed_malicious_publication` | Source confirms intentional malicious package publication but targeting mechanism is unclear | Secondary label |
| `dependency_confusion` | Source documents namespace or resolution confusion affecting a package or consumer | Separate incident family |
| `campaign_associated` | Package is part of a documented campaign but package-level causal involvement is not fully confirmed | Sensitivity analysis only |
| `ordinary_vulnerability` | Advisory describes a vulnerability without evidence of intentional compromise | Exclude from primary compromise label |
| `ambiguous` | Evidence conflicts or lacks package/version specificity | Unknown or low-confidence analysis |

## Required record

Every candidate incident record should include:

- canonical package name;
- exact affected version or version range;
- incident family;
- first malicious publication time, if known;
- first public detection or advisory time;
- removal or deprecation time, if known;
- evidence URLs and retrieval date;
- evidence summary in neutral language;
- label confidence;
- reviewer and review date;
- exclusion reason if not used in the primary benchmark.

## Review procedure

### Discovery

Use OSV, GitHub Advisory Database, npm advisories, registry notices, maintainer post-mortems, CISA alerts, and reputable incident analyses to identify candidates. Keyword matches such as “malicious,” “token,” or “compromise” are discovery filters only.

### Verification

For each candidate, confirm that the source identifies the package and the affected version or range. Confirm whether the event is intentional compromise, ordinary vulnerability, dependency confusion, typosquatting, or ambiguous. Record the earliest reliable event time, not merely the publication date of the report.

### Temporal labeling

The primary target for an observation date \(t\) and horizon \(h\) is positive if a high-confidence event begins in \((t, t+h]\). A package that is already publicly known to be compromised before \(t\) must not be a positive for a future prediction window unless the task explicitly models recurrence.

### Multi-package campaigns

For campaigns such as Shai-Hulud, preserve both the campaign-level record and package-level records. Do not assume that every package mentioned in a campaign report was equally involved. Store direct compromise, suspected involvement, and downstream exposure as separate fields.

### Negative candidates

A negative candidate is not “never malicious.” It is a package with no confirmed positive event in the selected observation and horizon window and sufficient observation coverage. Packages with poor data coverage should be marked unknown or excluded from a strict negative set.

## Current anchor incidents

The 2025 Shai-Hulud campaign is a high-impact multi-package incident documented by CISA, which reports more than 500 compromised packages and automated propagation through compromised developer credentials.[1] The 2026 Axios incident is a version-specific maintainer-compromise case: CISA and the Axios post-mortem identify `axios@1.14.1` and `axios@0.30.4`, the injected `plain-crypto-js@4.2.1`, and a short publication window.[2][3]

These anchors are useful, but they should not be the entire label set. A model that ranks two hand-picked case studies successfully has not demonstrated ecosystem-wide predictive validity.

## Label quality checks

Before model training:

- independently review a sample of positives and negatives;
- measure inter-reviewer agreement if more than one reviewer is available;
- publish a decision table for disputed cases;
- retain excluded candidates and reasons;
- calculate performance under high-confidence-only and inclusive labels;
- ensure no feature is derived from the incident source after the feature cutoff.

## References

[1]: https://www.cisa.gov/news-events/alerts/2025/09/23/widespread-supply-chain-compromise-impacting-npm-ecosystem "CISA Shai-Hulud alert"

[2]: https://www.cisa.gov/news-events/alerts/2026/04/20/supply-chain-compromise-impacts-axios-node-package-manager "CISA Axios alert"

[3]: https://github.com/axios/axios/issues/10636 "Axios maintainer post-mortem"

[4]: https://google.github.io/osv.dev/ "OSV documentation"
