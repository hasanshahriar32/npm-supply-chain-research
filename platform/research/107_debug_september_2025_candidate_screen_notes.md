# Debug September 2025 Candidate-Screen Notes

**Status:** Provisional candidate inventory only; not an admission decision.  
**Prepared by:** Manus AI  
**Screen date:** 26 August 2026

## Candidate and bounded initial evidence

The next compact candidate screen is scoped to `debug@4.4.2` in the September 2025 npm maintainer-account compromise. The Debug project’s incident issue, opened on 8 September 2025, states that the maintainer’s npm account was locked out after a phishing-driven 2FA-reset event, identifies `debug@4.4.2` among the affected releases, and records npm’s statement that impacted versions had been taken down. [1] Wiz and StepSecurity independently list `debug@4.4.2` among affected releases and describe the social-engineering or phishing compromise context. [2] [3]

| Screen field | Current bounded observation | Decision status |
|---|---|---|
| Candidate package/version | `debug@4.4.2` | Finite exact-version target is independently corroborated. [1] [2] [3] |
| Incident context | Maintainer reports phishing, npm-account lockout, and an npm-only compromise. [1] | Confirmed by independent technical reports for the bounded package-event screen. [2] [3] |
| Relatedness | The same maintainer issue lists multiple affected packages. [1] | The admitted row is one Qix-related family only; no campaign completeness or independence is inferred. |
| Registry cutoff and predecessor | Official registry metadata sets `debug@4.4.2` at `2025-09-08T13:12:39.973Z`; the strict cutoff selects retained `debug@4.4.1`. [4] | Exact source-object requirement is satisfied. |

This initial note records no package-source download, extraction, installation, execution, control, benign label, reach value, score, model, ranking, interval, calibration result, or predictive metric. The inaccessible NVD detail page was not treated as evidence. A separate governed assessment and atomic reconstruction determine the final ledger decision.

## References

[1] [Debug project, “Version 4.4.2 published to npm is compromised,” Issue #1005, 8 September 2025](https://github.com/debug-js/debug/issues/1005).

[2] [Wiz, “Widespread npm Supply Chain Attack: Breaking Down Impact & Scope Across Debug, Chalk, and Beyond,” 9 September 2025](https://www.wiz.io/blog/widespread-npm-supply-chain-attack-breaking-down-impact-scope-across-debug-chalk).

[3] [StepSecurity, “20+ Popular NPM Packages Compromised,” 8 September 2025](https://www.stepsecurity.io/blog/20-popular-npm-packages-compromised-chalk-debug-strip-ansi-color-convert-wrap-ansi).

[4] [npm registry metadata, `debug`](https://registry.npmjs.org/debug).
