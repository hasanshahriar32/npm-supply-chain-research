# Noblox-related npm candidate discovery notes

**Screen date:** 26 August 2026  
**Status:** Discovery only; not an incident admission or a primary-ledger change.

Socket’s 6 February 2024 report identifies `noblox.js-proxy-server@4.15.4` as a malicious impersonation package. The independently reviewed GitHub advisory found during the same bounded screen instead concerns the distinct package `noblox.js-proxy-agent` and is all-version scoped (`>= 0`), so it cannot corroborate the exact `noblox.js-proxy-server@4.15.4` target.

For the 2021 ransomware reports, Sonatype and BleepingComputer independently identify the package names `noblox.js-proxy` and `noblox.js-proxies`. The material retrieved from both sources does **not** supply a finite exact affected release list. That preserves a second strict-screen blocker: the corroborated package names are not a version-specific temporal target.

The retrieved historic Sonatype ransomware-report URL returned a current page-not-found response. It is therefore not usable as corroboration from the material actually reviewed. No official npm registry metadata has yet been used for either package, and this note creates zero affected-version targets, event cutoffs, source snapshots, ledger rows, incident families, validation units, controls, labels, installations, reach values, scores, models, rankings, intervals, calibration results, or predictive metrics.

## References

[1] [Socket, “Malicious npm Package Masquerades as Noblox.js, Targeting Roblox Users,” 6 February 2024](https://socket.dev/blog/malicious-npm-package-masquerades-as-noblox-js).

[2] [GitHub Advisory Database, “Malware in noblox.js-proxy-agent,” GHSA-475f-hjh6-233f](https://github.com/advisories/GHSA-475f-hjh6-233f).

[3] [Sonatype, “npm Ransomware Attack: Malicious Roblox API Package Discovered by Sonatype,” 27 October 2021](https://www.sonatype.com/blog/fake-npm-roblox-api-package-installs-ransomware-spooky-surprise).

[4] [BleepingComputer, “Malicious NPM libraries install ransomware, password stealer,” 27 October 2021](https://www.bleepingcomputer.com/news/security/malicious-npm-libraries-install-ransomware-password-stealer/).
