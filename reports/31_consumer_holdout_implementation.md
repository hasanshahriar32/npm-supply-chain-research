# Held-out application comparison

The November 21 Bangladesh-time run applies the design in [Report 30](30_post_pilot_research_design/research_design.pdf). The primary comparison uses the frozen five-account additive portfolios and repeats the same scoring for both tied version alternatives. The identical greedy selection supplies a control.

- **Frame.** The 199-entry pinned catalog loses 40 feasibility-pilot entries and four additional earlier endpoint keys, leaving 155 repositories. Collection pins the observed public default HEAD in a 24-hour window. One HEAD remained unresolved. The other 154 SHA values are distinct. Canonical repository identity across all forks was outside the lexical frame definition.
- **Path evidence.** Thirty projects supported a comparison, 25 yielded a corroborated path, and the two implementations agreed on 6,388 package locations within these cases. Eighteen inputs passed Arborist while the custom parser declined them. Shared lockfiles and SemVer limit what agreement can establish.
- **Independent registry reference.** All 3,299 distinct public package/version keys from the valid joint paths entered the registry request queue. This stage collects evidence for those keys before reaching the portfolio-matching step. It uses the registry maintainer list as observed during acquisition. It does not reconstruct publish authority.
- **Interpretation.** Documented cells and bounds use the entire frozen frame. The bounds concern coverage under the defined mandatory production dependency scope. The chosen five-slot case was identified from training evidence after the earlier pilot.

## Outcomes

The registry stage completed within the frozen window after an interruption and resumption about seven hours later. It recorded usable maintainer lists for **3,287 of 3,299** distinct versions. The other 12 remain in the request ledger as unknown. Registry acquisition times and project HEAD observation times are retained independently.

| Comparison | Documented both | Name only | Version only | Neither documented | Fully resolved pairs | Gross reassignment bounds | Net coverage bounds |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Primary, five slots | 23 | 0 | 0 | 132 | 29 | 0–81.3% | −81.3 to +81.3 points |
| Alternate 1, five slots | 23 | 0 | 0 | 132 | 29 | 0–81.3% | −81.3 to +81.3 points |
| Alternate 2, five slots | 23 | 0 | 0 | 132 | 29 | 0–81.3% | −81.3 to +81.3 points |
| Identical greedy control | 24 | 0 | 0 | 131 | 29 | 0 | 0 |

All 23 common hits had a path to an account present in both portfolios. In the primary result, 23 confirmed common positives and six confirmed common negatives coexist with 126 unresolved pairs. The unresolved cases drive the wide bounds. Reporting zero documented change as evidence for practical equivalence would overstate the experiment. [Paired outcomes](../research/consumer_holdout/runs/selfhosted-v1/results.json)

## What limits the next comparison

The project-side stages excluded 27 other declared package managers, 24 workspaces, 27 absent root manifests and 24 cases without a root npm lockfile. These mutually exclusive intake counts show that expanding the registry collection alone would leave most of the coverage uncertainty in place. Fifteen of 18 Arborist-only cases had overrides and three had importer identity disagreement. One additional override case encountered an external or ambiguous path.

A new offline regression fixture checks both an ancestor-scoped override and nominally identical sibling ranges. Arborist 9.9.1 resolves the target under the applicable override while retaining the sibling's original range. The fixture distinguishes a valid locked override from a genuine mismatch. Before opening the next comparison frame, the independent implementation needs tests for that same distinction, applicable workspace importers and the manager formats chosen on development inputs.

## Verification and deliverables

The [study directory](../research/consumer_holdout/README.md) documents how to replay the result from the local sealed source archive. The separate verifier recomputes the paired counts and bounds and checks the acquisition chronology. The [revised section](../manuscript_q1/sections/07aa_consumer_holdout.tex) and its generated table are part of both journal working drafts. The report contains evidence from automated tools and does not attribute judgments to human reviewers.
