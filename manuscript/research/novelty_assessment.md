# Novelty assessment and completed research status

Updated **20 October 2026**. This targeted primary-source review bounds the claims of our completed study. It is not a systematic review or a guarantee of publication novelty. Extended source verification appears in `2026-10-20_literature_extension.md` and `2026-10-20_verified_sources.csv`.

## Completed contribution

**We measure how the defensive objective changes fixed-budget maintainer prioritization in our observed npm graph.** Our completed experiments compare distinct downstream endpoint coverage, reduction of a stipulated sum of account-origin scenario exposures, and exclusion of every observed source account for an endpoint. They test package and repository units, version continuity, graph depth, repository mapping, candidate eligibility, workflow visibility, and identity grouping.

This is a structural empirical replication and extension. Maintainer unions, greedy maximum coverage, and hardening simulations are established methods. Our contribution is the measured separation of decision objectives and its sensitivity to representation and observation units. The artifact-consistency checks support data quality; they no longer define the paper's principal research contribution.

The observed dataset contains 25,228 package identifiers, 88,113 unique package adjacency pairs from 121,885 versioned rows, 12,217 maintainer usernames, and 79,405 package–maintainer relationships. Positive workflow observations cover 15,233 package names mapped to 7,171 normalized GitHub repository keys. These are lexical repository keys, not verified distinct workflows, machines, organizations, or release authorities.

The identifier population includes **2,745 context-encoded bundled dependency identifiers** containing `>`; none has a package-version metadata row in our archive. deps.dev documents these names as bundle-context coordinates that may differ from a global registry package, so we retain them as distinct observed nodes and do not collapse them onto their leaf names. They are included in the frozen sampling frame. Exactly eight of the prospective sample's 100 identifiers contain `>`; all eight requests returned HTTP 405. The other two unavailable requests returned HTTP 404 for ordinary names. Acquisition missingness is therefore associated with identifier representation, not a demonstrated random failure process. The 25,228-node population is not a count of distinct global npm registry coordinates. Counts were checked read-only against `packages.name`, `package_versions.package_name`, and the prospective capture records; interpretation follows the [deps.dev bundled-node documentation](https://docs.deps.dev/api/v3/#getdependencies).

## Main completed findings

At budget 100, or 0.819% of observed usernames:

| Selection method | Distinct positive-workflow repository keys covered | Share of 7,171 observed keys | Equal-scenario exposure reduction | All-source excluded keys |
|---|---:|---:|---:|---:|
| Portfolio count | 4,579 | 63.85% | 7.96% | 577 |
| Sum of package reach | 4,835 | 67.42% | 21.98% | 704 |
| Maximum package reach | 4,268 | 59.52% | 33.59% | 533 |
| Exact maintainer union reach | 4,407 | 61.46% | 33.79% | 534 |
| Marginal coverage greedy | 5,538 | 77.23% | 11.48% | 800 |
| Uniform random, mean over 200 orders | 1,680.605 | 23.44% | 0.804% | 12.78 |

Greedy covers 25.66% more distinct repository endpoints than exact-union ranking, while exact union removes a greater share of the equally weighted scenario exposure. This demonstrates objective mismatch, not universal superiority. Of greedy's 5,538 covered endpoints, 4,738 remain reachable through at least one unselected identity. Its 800 all-source exclusions are conditional structural statistics, not observed incidents prevented.

On the version-continuous graph, greedy covers 5,516 keys with 13.10% scenario reduction; exact union covers 4,479 with 40.59% reduction. Identity–repository incidence decreases from 462,170 to 266,016, or 42.44%. Aggregate coverage can therefore remain comparatively stable while the additive scenario quantity changes substantially. Neither representation reconstructs one installed tree or a common historical observation time.

Selecting greedy controls for all-package coverage reaches 5,308 workflow repository keys; selecting for workflow-package coverage reaches 5,315; selecting directly for repository coverage reaches 5,538. Excluding 60 positive version observations with inconsistent repository mappings leaves 7,147 positive keys; greedy covers 5,524 and satisfies all-source exclusion for 799. We exclude the conflicting observations rather than transfer their workflow flags without reacquisition.

These numerical findings are traceable through `claim_evidence.csv`. Full definitions, other budgets, random simulation ranges, checks, and limitations appear in `structural_interventions_notes.md` and `../results/structural_interventions/`.

## Theory and empirical extension

With a fixed uniform single-account loss scenario and ideal removal of selected origins, exposure reduction is additive across account footprints. Descending exact footprint size therefore optimizes that objective under equal costs. Uniform origins and perfect removal are scenario assumptions, not empirical compromise probabilities or measured control efficacy.

Distinct endpoint coverage is a monotone submodular union objective with the standard cardinality-budget greedy approximation guarantee. Complete exclusion instead requires every observed source account for an endpoint to be selected; coverage alone does not satisfy that condition. The guarantee does not extend to complete exclusion. See [Nemhauser, Wolsey, and Fisher (1978)](https://link.springer.com/article/10.1007/BF01588971). Our experiments measure these quantities and their sensitivity; they do not introduce a new optimizer or general theorem.

## Closest prior work and extension boundary

| Primary source | Established evidence or method | Boundary for our contribution |
|---|---|---|
| [Zimmermann et al., Small World with High Risks (2019)](https://www.usenix.org/system/files/sec19-zimmermann.pdf) | Definition 3.6 constructs maintainer union reach; Definition 3.8 selects greatest marginal coverage; Section 5.4 simulates influential-maintainer vetting. | Our unions and greedy selection replicate established methods. We compare separate coverage, additive-scenario, and all-source estimands, with representation and workflow-repository sensitivities. |
| [Wang, Defending the Core (2026), preprint](https://arxiv.org/html/2606.14036v1) | npm centrality-based package hardening, dependency pruning, and cascade simulations. | We remove hypothetical account-origin scenarios while retaining paths and other accounts. These intervention semantics differ from package-node blocking. |
| [Zahan et al., Weak Links (2022)](https://arxiv.org/abs/2112.10165v2) | Metadata weakness signals. | Footprint sizes do not establish account hygiene or compromise likelihood. |
| [Koishybayev et al. (2022)](https://www.usenix.org/conference/usenixsecurity22/presentation/koishybayev) and [ARGUS (2023)](https://www.usenix.org/conference/usenixsecurity23/presentation/muralee) | Configuration security properties and workflow injection analysis. | Directory observations define a target subset, without proving privileges, secrets, or exploitable execution. |
| [Liu et al., dependency trees (2022)](https://arxiv.org/abs/2201.03981v2) | npm resolution differs from package-level reachability. | Version continuity is a representation sensitivity, not validated installed-tree reconstruction. |
| [Tsakpinis and Pretschner, repository accessibility (2024; revised 2025)](https://arxiv.org/abs/2404.17403v2) | Repository availability varies with package importance. | Mapping and visibility assumptions remain explicit; lexical repository keys are deduplicated. |
| [On Good Authority, v2 (2026), preprint](https://arxiv.org/abs/2606.22593v2) | Predecessor-aware release-authority evidence. | Current maintainer associations do not reconstruct publisher, token, or workflow authority. |
| [npm-follower (2023)](https://arxiv.org/abs/2308.12545) and [CHRONO-RESOLUTION (2026)](https://arxiv.org/abs/2607.15315) | Archived releases and release-point dependency resources. | Historical data acquisition and resolution are established; our static study does not replace them. |
| [PatchRisk (September 2026)](https://arxiv.org/abs/2609.13719) | Future vulnerability-exposure prediction with temporal and package-disjoint evaluation. | Our completed results concern conditional structure, with no trained model or forecast metric. |

The strongest defensible extension is the **measured objective tradeoff and its representation/observation-unit sensitivity in our sample**. These distinctions do not establish that every individual component is unprecedented. Source experiments have not been independently reproduced, and preprint status is preserved.

## Prospective acquisition: completed freeze, future outcomes

We froze a uniform seeded feasibility sample of 100 package identifiers from the existing 25,228-identifier frame before metadata requests. Official npm metadata was captured for 90; ten unavailable observations were retained without replacement or benign labels, including the eight bundle-context identifiers described above. The feature cutoff is **20 October 2026 at 00:48:38 Asia/Dhaka**. The 90-day follow-up interval ends **18 January 2027 at 00:48:38 Asia/Dhaka**.

All 100 outcomes remain pending. Zero positive or negative labels have been assigned, zero models have been fitted, and no forecasting performance exists. This is completed data-acquisition feasibility work, not an externally preregistered or powered predictive benchmark. Surveillance sources, censoring rules, and the final analysis plan must be frozen before follow-up outcomes are examined. Archived structural features, if later joined, retain stale and incompletely timed provenance.

The feasibility cohort does not retroactively provide controls for the older incident companion. Future dated controls and adjudicated outcomes could support prediction; they are not present results.

## Permitted and unsupported claims

We can report the completed objective comparison, overlap quantities, sensitivity findings, validation checks, and acquisition status. Source/output hashes, read-only access, deterministic ties, and fixed random seeds support reproduction. Random simulation ranges describe baseline-selection variability on this graph, not confidence intervals for npm or future compromises.

We cannot claim a first package–maintainer security graph, a new coverage optimizer, calibrated attacker return, measured privilege, actual incidents prevented, inferred common credential control, a completed prospective prediction benchmark, a trained heterogeneous model, or ecosystem-wide representativeness. Missing observations remain distinct from verified absence.

Paper wording should describe **our dataset**, **our observed graph**, and **our experiments**. File and storage details belong in reproducibility documentation rather than framing the paper as an editor's review of a supplied repository.
