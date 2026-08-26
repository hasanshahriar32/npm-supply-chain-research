# country-currency-map March 2025 candidate screen

**Screen date:** 26 August 2026  
**Status:** Bounded evidence screen; no ledger admission or source-object reconstruction has occurred.

Sonatype reported that `country-currency-map@2.1.8` was one of a finite set of cryptocurrency-related npm packages hijacked to exfiltrate environment data. Its report records `2.1.8` as the malicious version and dates the incident to 27 March 2025. [1] Independent contemporaneous BleepingComputer coverage identifies the same package, says its maintainer deprecated the malicious `2.1.8` release, and reports a recommendation to use `2.1.7`; this is corroboration of the one-version package event only, not a campaign census or a safety conclusion about the predecessor. [2]

The next bounded step is an official npm registry metadata-only response. It may establish the publication time of `2.1.8`, the strict one-millisecond cutoff, and whether the selected immediately pre-cutoff version object is retained. It cannot establish package installation history, downstream dependency reach, blast radius, current maintainer state, repository provenance, causal impact, controls, or predictive features.

## References

[1] [Sonatype, “Multiple Crypto Packages Hijacked, Turned Into Info-Stealers,” 27 March 2025](https://www.sonatype.com/blog/multiple-crypto-packages-hijacked-turned-into-info-stealers).

[2] [BleepingComputer, “Infostealer campaign compromises 10 npm packages, targets devs,” 27 March 2025](https://www.bleepingcomputer.com/news/security/infostealer-campaign-compromises-10-npm-packages-targets-devs/).
