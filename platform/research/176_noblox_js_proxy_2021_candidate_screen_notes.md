# Bounded `noblox.js-proxy` / `noblox.js-proxies` October 2021 Candidate Screen

## Scope

This screen evaluates the distinct 2021 packages `noblox.js-proxy` and `noblox.js-proxies`, not the separately screened 2024 package `noblox.js-proxy-server`. Sonatype and BleepingComputer independently identify the two package names in an October 2021 Roblox-themed ransomware and password-stealing campaign.[1] [2]

## Evidence gate

Sonatype reports that `noblox.js-proxy@1.0.0` appeared normal and that malicious obfuscated content began at `1.0.1`.[1] The same report discusses `noblox.js-proxies` as a related package from the same actor, but the retrieved material does not provide a separately adjudicated finite affected-version set for that package. BleepingComputer independently corroborates both package names and the ransomware, trollware, and password-stealing behavior, but does not independently identify the exact affected release numbers.[2]

The strict intersection therefore remains insufficient for a two-package version-level record. The available evidence supports a contextual incident description, not a primary temporal label for exact versions.

## Official registry timing and retention

The official npm registry time maps show `noblox.js-proxy` versions `1.0.0`, `1.0.1`, `1.0.2`, `1.0.3`, and `1.0.5` sharing the timestamp `2021-10-19T12:31:54.735Z`.[3] They show `noblox.js-proxies` versions `1.0.0`, `1.0.2`, and `1.0.3` sharing the timestamp `2021-10-26T14:15:35.478Z`.[4] Under the one-millisecond rule, the candidate cutoffs are `2021-10-19T12:31:54.734Z` and `2021-10-26T14:15:35.477Z`, respectively. No retained version object exists before either cutoff in the official time map.

The registry result is a retention failure, not evidence that any version was safe, benign, unchanged, or installed. It also does not resolve the missing independent exact-version intersection.

## Decision

The 2021 Noblox candidate is **excluded from the primary temporal ledger** because the package-specific exact-version scope is not independently corroborated and no strict pre-event registry object is retained for either package. The record remains useful as contextual evidence for future brandjacking, typosquatting, and payload-capability analyses. It creates no ledger rows, family, validation unit, exact snapshot, graph artifact, control population, historical installation, reach estimate, score, ranking, model, interval, calibration result, or predictive metric.

The event is kept separate from the 2024 `noblox.js-proxy-server` candidate. Shared Roblox branding and related names do not by themselves establish one campaign family or a common actor.

## References

[1]: https://www.sonatype.com/blog/fake-npm-roblox-api-package-installs-ransomware-spooky-surprise "Sonatype: npm Ransomware Attack: Malicious Roblox API Package Discovered by Sonatype"
[2]: https://www.bleepingcomputer.com/news/security/malicious-npm-libraries-install-ransomware-password-stealer/ "BleepingComputer: Malicious NPM libraries install ransomware and password stealer"
[3]: https://registry.npmjs.org/noblox.js-proxy "npm registry metadata: noblox.js-proxy"
[4]: https://registry.npmjs.org/noblox.js-proxies "npm registry metadata: noblox.js-proxies"

**Retrieval date:** 2026-09-19

**Author:** Manus AI
