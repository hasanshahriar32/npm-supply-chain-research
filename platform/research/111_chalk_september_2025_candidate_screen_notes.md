# Bounded `chalk` September 2025 Candidate Screen Notes

**Status:** Candidate-selection notes only; no ledger decision.  
**Date:** 26 August 2026.  
**Scope:** Bounded screen for `chalk@5.6.1` only.

## Evidence preserved before registry screening

The Chalk maintainer issue identifies `chalk@5.6.1` among the vulnerable versions and reports that the compromised account was removed. [1] StepSecurity independently lists `chalk@5.6.1` in its confirmed-compromised package list and describes the September 2025 phishing compromise of the Qix maintainer account. [2]

| Screening requirement | Current bounded evidence | Decision at this note stage |
|---|---|---|
| Finite affected version target | Both sources identify `chalk@5.6.1`. [1] [2] | Provisionally satisfied. |
| Independent compromise-context corroboration | The maintainer issue records the compromised-account response; StepSecurity independently reports the phishing context. [1] [2] | Provisionally satisfied. |
| Relatedness | The candidate is explicitly linked to the already-admitted September 2025 Qix event through the maintainer issue and StepSecurity campaign description. | It must remain in the existing `qix_npm_phishing_september_2025` family and cannot create a new independent validation unit. |
| Official registry cutoff and retained predecessor | Not yet assessed. | Requires bounded official registry metadata, a documented event-time rule, and a retained source object strictly before the cutoff. |

No package payload was downloaded, extracted, installed, or executed. This note creates zero ledger records, families, validation units, snapshots, dependency declarations, graph edges, controls, benign labels, historical installations, reach or blast-radius values, scores, models, rankings, intervals, calibration results, or predictive metrics.

## References

[1] [Chalk, “Version 5.6.1 published to npm is compromised (RESOLVED),” issue #656, 8 September 2025](https://github.com/chalk/chalk/issues/656).

[2] [StepSecurity, “20+ Popular NPM Packages Compromised (Chalk, Debug, Strip-ANSI, Color-Convert, Wrap-ANSI…),” 8 September 2025](https://www.stepsecurity.io/blog/20-popular-npm-packages-compromised-chalk-debug-strip-ansi-color-convert-wrap-ansi).
