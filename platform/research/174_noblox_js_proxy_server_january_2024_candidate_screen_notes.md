# Bounded `noblox.js-proxy-server` January 2024 Candidate Screen

## Scope

This screen evaluates only the impersonation package `noblox.js-proxy-server`, with Socket identifying version `4.15.4` as malicious in a report dated 6 February 2024.[1] The screen uses public reporting and official npm registry metadata only. It does not download, install, execute, or inspect package payloads.

## Corroboration result

Socket provides a finite exact package-version claim for `noblox.js-proxy-server@4.15.4` and describes brandjacking, combosquatting, starjacking, data collection, and follow-on execution behavior.[1] The independent Checkmarx report confirms a broader year-long campaign of malicious packages mimicking `noblox.js`, including named packages such as `noblox.js-async`, `noblox.js-threads`, `noblox.js-thread`, and `noblox.js-api`.[2] It does **not** independently identify `noblox.js-proxy-server@4.15.4` as an affected exact release.

The 2021 Sonatype and BleepingComputer reports concern distinct packages named `noblox.js-proxy` and `noblox.js-proxies`, not `noblox.js-proxy-server`.[3] [4] Sonatype records that the 2021 packages began with version `1.0.0` and became malicious at `1.0.1`, but that evidence cannot be transferred to the 2024 package name.[3]

The GitHub-reviewed advisory located during the earlier discovery screen concerns `noblox.js-proxy-agent` and is scoped to all versions. It cannot corroborate the exact `noblox.js-proxy-server@4.15.4` claim.[5]

## Official registry timing

The official npm registry time map records the following publication sequence for `noblox.js-proxy-server`: `4.15.0` at `2024-01-16T22:10:38.724Z`, `4.15.1` at `2024-01-16T23:04:07.999Z`, `4.15.2` at `2024-01-16T23:07:00.974Z`, `4.15.3` at `2024-01-16T23:53:58.655Z`, and `4.15.4` at `2024-01-17T03:39:58.207Z`.[6] The strict one-millisecond cutoff for the Socket-reported version is therefore `2024-01-17T03:39:58.206Z`, and `4.15.3` is a retained earlier registry version object.

This timing result does not cure the corroboration failure. Registry metadata establishes publication ordering and retained-object availability; it does not independently establish that the exact version was malicious.

## Decision

The candidate is **excluded from the primary temporal ledger** because the exact affected-version set is not independently corroborated. The screen retains the Socket claim as a contextual candidate, preserves the official timestamp and predecessor evidence, and creates no ledger row, family, validation unit, graph artifact, control population, historical installation, reach estimate, score, ranking, model, interval, calibration result, or predictive metric.

The 2021 `noblox.js-proxy` and `noblox.js-proxies` event remains a separate candidate family and is not imported into this record. The 2024 Roblox impersonation campaign remains useful for future campaign-level or brandjacking research, but campaign breadth is not a substitute for exact version-level corroboration.

## References

[1]: https://socket.dev/blog/malicious-npm-package-masquerades-as-noblox-js "Socket: Malicious npm package masquerades as Noblox.js"
[2]: https://checkmarx.com/blog/year-long-campaign-of-malicious-npm-packages-targeting-roblox-users/ "Checkmarx: Year-long campaign of malicious npm packages targeting Roblox users"
[3]: https://www.sonatype.com/blog/fake-npm-roblox-api-package-installs-ransomware-spooky-surprise "Sonatype: npm ransomware attack involving malicious Roblox API packages"
[4]: https://www.bleepingcomputer.com/news/security/malicious-npm-libraries-install-ransomware-password-stealer/ "BleepingComputer: Malicious NPM libraries install ransomware and password stealer"
[5]: https://github.com/advisories/GHSA-475f-hjh6-233f "GitHub Advisory Database: Malware in noblox.js-proxy-agent"
[6]: https://registry.npmjs.org/noblox.js-proxy-server "npm registry metadata: noblox.js-proxy-server"

**Retrieval date:** 2026-09-19

**Author:** Manus AI
