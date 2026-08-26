# Bounded `eslint-config-prettier` July 2025 Candidate Screen Notes

**Status:** Candidate-selection notes only; no ledger decision.  
**Scope:** `eslint-config-prettier@8.10.1`, `9.1.1`, `10.1.6`, and `10.1.7` only.

GitHub’s reviewed advisory for CVE-2025-54313 identifies those four versions as containing embedded malicious code in a supply-chain compromise. [1] The upstream project issue records the anomalous publications and missing corresponding repository changes. [2]

No package payload was downloaded, extracted, installed, or executed. No ledger record, family, validation unit, snapshot, dependency edge, control, benign label, historical installation, reach value, score, model, ranking, interval, calibration output, or predictive metric has been created. The next gate is bounded official npm registry metadata: the earliest affected-version timestamp, then a retained strictly earlier source object.

## References

[1] [GitHub Advisory Database, “CVE-2025-54313,” reviewed 21 July 2025](https://github.com/advisories/GHSA-f29h-pxvx-f335).

[2] [Prettier, “four new versions published with no code changes to repo,” issue #339, 18 July 2025](https://github.com/prettier/eslint-config-prettier/issues/339).
