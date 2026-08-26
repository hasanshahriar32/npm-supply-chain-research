# Bounded Jscrambler July 2026 Candidate Screen Notes

**Status:** Candidate evidence screen; no ledger decision.  
**Primary package scope:** `jscrambler@8.14.0`, `8.16.0`, `8.17.0`, `8.18.0`, and `8.20.0`.

Jscrambler’s 11 July 2026 security advisory identifies an unauthorized malicious publication affecting those five `jscrambler` versions. [1] StepSecurity independently reports `jscrambler@8.14.0` as carrying the malicious preinstall hook, and Socket independently reports the broader package compromise. [2] [3]

No package payload was downloaded, extracted, installed, or executed. No ledger row, family, validation unit, snapshot, declaration, graph edge, control, benign label, historical installation, reach value, score, model, ranking, interval, calibration output, or predictive metric has been created. The next gate is bounded official npm registry metadata: determine the earliest affected publication timestamp and a retained version object strictly before it.

## References

[1] [Jscrambler, “Unauthorized Publication of a Malicious npm Package Affecting CI,” 11 July 2026](https://jscrambler.com/blog/security-advisory-malicious-npm-package/).

[2] [StepSecurity, “jscrambler npm package publishes malicious preinstall binary,” 11 July 2026](https://www.stepsecurity.io/blog/jscrambler-npm-package-publishes-malicious-preinstall-binary).

[3] [Socket, “Jscrambler npm Package Compromised in Supply Chain Attack,” 11 July 2026](https://socket.dev/blog/jscrambler-supply-chain-attack).
