# Bounded got-fetch July 2025 Candidate Screen

## Scope

This screen considers only `got-fetch@5.1.11` and `5.1.12`. Checkmarx reports these two malware-bearing npm releases after a maintainer phishing compromise, and Snyk independently corroborates the affected interval and notes that only these two releases were affected.[1] [2] No package payload, tarball, archive, installation, or execution was accessed.

## Relatedness boundary

Checkmarx reports that the phishing campaign also affected other packages, including already governed `eslint-config-prettier`; this does not establish whether `got-fetch` belongs to an existing governed family. The screen therefore records relatedness as unresolved and does not create a ledger row, family, validation unit, control, or model output before a strict registry assessment.

## Next gate

Only official npm registry metadata may establish the earliest timestamp, one-millisecond cutoff, and retained predecessor. No current registry state can be interpreted as historical installation, reach, blast radius, benignness, or predictive evidence.

## References

[1]: https://checkmarx.com/zero-post/supply-chain-phishing-campaign-drops-more-malware-into-npm-got-fetch-5-1/ "Checkmarx got-fetch report"
[2]: https://security.snyk.io/vuln/SNYK-JS-GOTFETCH-10873306 "Snyk got-fetch advisory"
