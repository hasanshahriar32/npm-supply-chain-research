# Bounded Nx August 2025 Candidate Screen Notes

**Status:** Candidate evidence screen; no ledger decision.  
**Primary package scope:** `nx@21.5.0`, `20.9.0`, `20.10.0`, `21.6.0`, `20.11.0`, `21.7.0`, `21.8.0`, and `20.12.0`.

Nx’s postmortem and reviewed GitHub advisory identify a token-theft path that enabled malicious npm publications across several Nx packages; for the single `nx` package, both name the same finite eight-version release set. [1] [2] Independent Snyk and StepSecurity reporting independently retain the eight `nx` versions and publish-token compromise context. [3] [4] This screen treats only the `nx` package row as a compact target and does not assert campaign completeness, historical installations, downstream reach, package impact, or a control observation.

The next gate is bounded official npm registry metadata. It may establish only the earliest retained affected-version timestamp, the one-millisecond strict cutoff, and whether the selected immediate pre-cutoff version object is currently retained. It must not download, extract, install, execute, or interpret a package payload.

## References

[1] [Nx, “S1ngularity - What Happened, How We Responded, What We Learned,” 5 September 2025](https://nx.dev/blog/s1ngularity-postmortem).

[2] [GitHub Security Advisory, “Malicious versions of Nx and some supporting plugins were published,” GHSA-cxm3-wv7p-598c](https://github.com/nrwl/nx/security/advisories/GHSA-cxm3-wv7p-598c).

[3] [Snyk, “Weaponizing AI Coding Agents for Malware in the Nx Malicious Package Security Incident,” 27 August 2025](https://snyk.io/blog/weaponizing-ai-coding-agents-for-malware-in-the-nx-malicious-package/).

[4] [StepSecurity, “s1ngularity: Popular Nx Build System Package Compromised with Data-Stealing Malware,” 27 August 2025](https://www.stepsecurity.io/blog/supply-chain-security-alert-popular-nx-build-system-package-compromised-with-data-stealing-malware).
