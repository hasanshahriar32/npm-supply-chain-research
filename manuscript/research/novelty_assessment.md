# Novelty assessment and research direction

Screen updated **20 October 2026**. This is a targeted primary-source review, not an exhaustive systematic literature review or a guarantee of publication novelty.

## Defensible current contribution

**An empirical consistency audit of co-located npm research artifacts, showing that matching package populations and dependency metrics can conceal workflow-derived disagreement that substantially changes fixed-budget review queues.** The provided offline implementation, aggregate outputs, boundary-tie calculation, weight sensitivity, and source hashes make this result inspectable.

This work newly executes the full archive comparison. It does not merely reformat the earlier report: the earlier CSV-only analysis did not establish agreement with the database's stored metrics, and the supplied database reproduces a different workflow result. The revised paper localizes this inconsistency and avoids assigning an undocumented cause.

## Closest prior work and implications

| Primary source | Relevance to the novelty boundary |
|---|---|
| [Zimmermann et al., Small World with High Risks (2019)](https://www.usenix.org/conference/usenixsecurity19/presentation/zimmerman) | Dependency and maintainer concentration are established premises. |
| [Zahan et al., Weak Links (2022)](https://arxiv.org/abs/2112.10165v2) | Proactive metadata concerns already have an empirical research base. |
| [Koishybayev et al., CI workflow security (2022)](https://www.usenix.org/conference/usenixsecurity22/presentation/koishybayev) and [ARGUS (2023)](https://www.usenix.org/conference/usenixsecurity23/presentation/muralee) | Public workflow security analysis goes substantially beyond directory presence. |
| [On Good Authority, v2 (2026)](https://arxiv.org/abs/2606.22593v2) | Release-path discontinuity already defines a distinct review surface. |
| [CHRONO-RESOLUTION (2026)](https://arxiv.org/abs/2607.15315) and [npm-follower (2023)](https://arxiv.org/abs/2308.12545) | Historical dependency and release data resources already exist. |
| [SupplyTGN (2026)](https://ssrn.com/abstract=7194447) | Cutoff-safe temporal package-risk evaluation is already studied in a PyPI/OSV setting. |
| [PatchRisk (September 2026)](https://arxiv.org/abs/2609.13719) | Particularly close new work: future vulnerability exposure forecasting for npm/PyPI. Added because it postdates the workspace's August novelty notes. |
| [Guo et al., malicious-package detector study, v2 (2026)](https://arxiv.org/abs/2603.27549v2) | Released-content classification must remain distinct from future publisher-compromise ranking. The current title differs from v1 in older repository notes. |

## Claims to avoid

- First dependency/maintainer graph for supply-chain security.
- First leakage-aware temporal npm benchmark.
- First public-workflow or release-authority security score.
- A trained heterogeneous graph model or improved forecasting accuracy.
- Calibrated attacker ROI, optimized attacker behavior, or measured private-system privilege.
- A completed comparison of structural, workflow, and authority queues; the current measured comparison is between artifacts and their structural scores.

## Conditional next contribution

A future study could test whether dated maintainer, workflow, and authority evidence improves **documented publisher-compromise review** beyond dated metadata and dependency baselines. It must first provide an independently defined at-risk population, horizon-specific no-known-event controls, campaign-aware splits, source-time evidence, and released predictions. This would be differentiated by its outcome and evidence linkage, not by the mere use of a GNN.

Suggested falsifiable questions:

1. Does historically available workflow configuration add review yield after dependency and release-activity baselines?
2. Does authority discontinuity identify a complementary queue, and how much does that queue overlap adjudicated compromise events at fixed budgets?
3. Do relation-aware models outperform regularized tabular models under matched historical coverage and campaign-disjoint evaluation?
4. How much apparent gain disappears when missingness-only features, package identity, post-event metadata, and correlated campaign records are controlled?

These are proposed research directions. The current manuscript cannot answer them with the available positive-only companion.

## Search record

The review searched for npm supply-chain graph prioritization, temporal leakage and package forecasting, release authority, historical dependency reconstruction, and the named close studies. Representative queries included:

```text
npm supply chain security temporal graph prioritization maintainer blast radius SupplyTGN
"CHRONO-RESOLUTION" dependency
npm "release authority" discontinuity security
npm supply chain prediction graph temporal leakage benchmark
npm compromise forecasting prioritization graph "2026" temporal benchmark maintainer
```

Primary paper landing pages, versioned arXiv pages, USENIX bibliographic entries, and official npm/deps.dev/GitHub documentation were inspected. Search results and indexed SSRN abstract metadata supplied the SupplyTGN landing text because direct SSRN access failed. The work is cited as a preprint; its experiments were not reproduced. Search absence is not used to claim that no similar artifact audit exists.
