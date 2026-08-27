# Preliminary bounded `rand-user-agent` May 2025 candidate screen

**Screen status:** The finite affected-version target is independently corroborated. No primary-ledger admission, exclusion, registry request, source-object selection, package download, archive inspection, installation, payload extraction, or execution has occurred.

## Bounded lead

Aikido reports that its analysis detected `rand-user-agent@1.0.110` on 5 May 2025 and lists `2.0.83`, `2.0.84`, and `1.0.110` as malicious-version indicators. It characterizes the case as a supply-chain attack against a legitimate package.[1]

BleepingComputer independently reports that `2.0.83`, `2.0.84`, and `1.0.110` were malicious unauthorized releases after the last legitimate `2.0.82` release. It reports direct contact with the package developer, who confirmed three unauthorized versions published on 5 May 2025; this source is retained as independent incident corroboration, not an outcome, reach, or installation source.[2]

The strict affected-version target for this screen is the three-version intersection: `2.0.83`, `2.0.84`, and `1.0.110`. No other version, package, incident, relationship, common-actor attribution, or campaign member is in scope.

## Scope and prohibition boundary

The next permitted action is a metadata-only official npm registry request for `rand-user-agent` to fix the earliest affected release time and test strict pre-event source-object retention. This screen cannot support claims about historical installs, dependency reach, blast radius, current maintainer state, controls, benignness, causal effects, scores, models, rankings, intervals, calibration, or predictive metrics.

## References

[1]: https://www.aikido.dev/blog/catching-a-rat-remote-access-trojian-rand-user-agent-supply-chain-compromise "Aikido, RATatouille: A Malicious Recipe Hidden in rand-user-agent"
[2]: https://www.bleepingcomputer.com/news/security/supply-chain-attack-hits-npm-package-with-45-000-weekly-downloads/ "BleepingComputer, Supply chain attack hits npm package with 45,000 weekly downloads"
