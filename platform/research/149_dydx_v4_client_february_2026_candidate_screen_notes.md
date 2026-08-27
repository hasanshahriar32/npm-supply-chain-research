# Bounded dYdX v4 client February 2026 candidate screen

**Screen date:** 27 August 2026  
**Candidate package:** `@dydxprotocol/v4-client-js`  
**Candidate event family:** `dydx_v4_client_npm_pypi_maintainer_compromise_2026`  
**Screen status:** Eligible to request bounded official npm registry metadata only; no primary-ledger admission has been made by this note.

## Evidence observations before registry access

Socket reports a supply-chain attack affecting the npm package `@dydxprotocol/v4-client-js` and lists the exact npm versions `3.4.1`, `1.22.1`, `1.15.2`, and `1.0.31` as compromised.[1] The report characterizes maintainer compromise as an unconfirmed appearance rather than a settled attribution. It also distinguishes the 2026 package event from a September 2022 incident affecting dYdX-related infrastructure; this screen neither imports the 2022 incident nor asserts a relationship between the two.[1]

The Hacker News independently reports the same npm package and exactly the same four npm versions.[2] The governed candidate target is therefore the strict four-version intersection only. The PyPI release named by both reports is out of scope, as are all unlisted npm versions, other packages, actors, payload properties, installations, and downstream consequences.

| Source | Package | Exact npm versions stated | Use in this screen |
|---|---|---|---|
| Socket | `@dydxprotocol/v4-client-js` | `3.4.1`, `1.22.1`, `1.15.2`, `1.0.31` | Independent technical source; establishes candidate version set only. |
| The Hacker News | `@dydxprotocol/v4-client-js` | `3.4.1`, `1.22.1`, `1.15.2`, `1.0.31` | Independent reporting; confirms the finite exact-version intersection only. |

## Strict screening boundary

The next permitted step is a metadata-only request to the official npm registry for this single package. The assessment must determine the earliest timestamp among the four reported versions, subtract exactly one millisecond, select the latest retained version object strictly before that cutoff across all SemVer streams, and verify that the selected object is retained. A failed timestamp, predecessor, retained-object, or independent-family gate requires exclusion.

No package archive or payload will be downloaded, extracted, installed, or executed. This screen creates no ledger record, family, source snapshot, dependency declaration, graph edge, control, benign label, historical installation, reach or blast-radius value, authority value, score, rank, interval, calibration result, model, or predictive metric. Registry metadata, if used, will establish publication-time selection and retained-object availability only; it cannot establish historical installation, reach, current publisher state, causality, campaign completeness, or statistical independence.

## References

[1]: https://socket.dev/blog/malicious-dydx-packages-published-to-npm-and-pypi "Socket, Malicious dYdX Packages Published to npm and PyPI After Maintainer Compromise"
[2]: https://thehackernews.com/2026/02/compromised-dydx-npm-and-pypi-packages.html "The Hacker News, Compromised dYdX npm and PyPI Packages Deliver Wallet Stealers and RAT Malware"
