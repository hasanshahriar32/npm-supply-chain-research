# Executed research plan: maintainer exposure and defensive decisions

Study date: 20 October 2026. This is an internal analysis plan, not an externally preregistered study. The former paper centered on export consistency; that result is retained as a quality-control record and is no longer the intended scientific contribution.

## Aim and authorship voice

Develop the project's research into a completed empirical study using our npm dependency, maintainer, and public-repository observations. The manuscript should describe what **we collect, define, implement, evaluate, and find**. Internal storage choices, the research website, and earlier draft omissions belong in the working record rather than the paper's motivation.

The original long-term goal is to forecast consequential supply-chain compromise. A cross-sectional exposure study can provide necessary groundwork and decision results now; it cannot establish future compromise probabilities or attacker ROI. No future-prediction performance will be invented to fill that gap.

## Questions and estimands

1. How do maintainer portfolio size, summed package reach, and unique downstream reach differ as ranking signals?
2. How do rankings change when the objective is unique endpoint review coverage, reduction of exposure under a specified single-account scenario distribution, or complete protection from every modeled account source?
3. How sensitive are the results to counting packages versus distinct public workflow repositories, bounded versus transitive paths, and preservation of package versions?
4. Which historical evidence is currently usable for a future compromise study, and which acquisition and labeling steps still need execution?

For maintainer identity m, E_m is the union of its maintained packages and their downstream dependent endpoints in the stated graph. Three distinct quantities are evaluated for a selected account set S:

- Review coverage: the number of unique endpoints reached by at least one selected account.
- Fixed-scenario hardening reduction: the removed account–endpoint incidences divided by all modeled account–endpoint incidences, under an explicitly equal-account, single-source idealized scenario. This is a conditional structural simulation, not an empirical compromise rate.
- Complete source protection: endpoints whose every modeled source account belongs to S. This is an optimistic graph-based hardening model and omits unknown publication paths and control failures.

These objectives are not interchangeable. Established maintainer reach and greedy maximum coverage are credited to prior work, including Zimmermann et al. (2019). The contribution sought is an empirical extension of those methods to alternative defensive objectives, observable workflow repository targets, and representation sensitivity.

## Planned comparisons

Use identity budgets 1, 5, 10, 25, 50, and 100. Compare portfolio-size ranking, summed and maximum constituent-package reach, exact union reach, overlap-aware greedy endpoint coverage, and seeded random selection. Retain explicit deterministic tie rules. Report repeated random selections as Monte Carlo design variability, not confidence intervals for ecosystem representativeness.

Evaluate package endpoints, positively observed workflow-package endpoints, and deduplicated workflow-repository endpoints separately. Run zero-hop, one-hop, and transitive sensitivity where implemented. Inaccessible or missing workflows remain an observation limit; an unavailable observation must not become a confirmed secure endpoint.

## Integrity and release

Read source archives without modification. Record archive and code hashes, graph orientation, endpoint definitions, scenario assumptions, budgets, seeds, and validation checks. Release aggregate comparisons and reproducible scripts; avoid publishing account-name target lists. Preserve the six-page A4 IEEE format, supplied author records, anonymous review version, and truthful assistance disclosure.

Output a status report distinguishing completed experiments, measured results, unsupported claims, and the concrete requirements for further historical prediction work. A null or inconvenient result remains a result.
