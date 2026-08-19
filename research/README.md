# Research Workspace

This directory contains the structured research record for the project **Predicting the Blast Radius: Forecasting High-ROI Attack Entry Points in Software Supply Chains**.

The project is being evaluated as a **defensive target-prioritization study**. It must not be interpreted as an exploit-development or credential-harvesting guide. The working objective is to determine whether time-stamped package, maintainer, dependency, and publicly observable CI/CD features can improve the prioritization of packages for defensive review.

## Evidence policy

Every substantive claim should be classified as one of the following:

| Evidence class | Meaning |
|---|---|
| Established | Directly supported by a primary paper, official documentation, or authoritative incident report |
| Repository-supported | Verified from the current code, data snapshot, or supplied project documents |
| Inferred | A reasoned interpretation that still needs empirical validation |
| Proposed | A research design choice or hypothesis for future testing |
| Unverified | A claim present in a draft but not yet supported by reproducible evidence |

The repository should not present draft claims about model performance, incident back-testing, or novelty as empirical findings until the corresponding data, code, and evaluation artifacts exist.

## Research questions

The current working question is:

> Given a time-stamped view of an open-source package ecosystem, can a package-level ranking model combining dependency reach, maintainer-sharing structure, and observable downstream CI/CD exposure identify historically compromised or strategically high-leverage packages more effectively than simpler graph, metadata, and ecosystem-security baselines without temporal leakage?

Subquestions concern the incremental value of maintainer and workflow features, the validity of the proposed Blast Radius and Wormability measures, the need for HGAT over interpretable baselines, and the generalizability of public-repository observations to real downstream infrastructure.

## Checkpoints

Research work is preserved in phase-based GitHub checkpoints:

1. Source inventory, claim audit, and research brief.
2. Literature matrix and related-work taxonomy.
3. Novelty, gap analysis, and worthiness assessment.
4. Refined hypotheses, methodology, leakage controls, ethics, and threats to validity.
5. Final report, decision memo, and implementation backlog.

Raw downloads, credentials, private tokens, unreviewed personal data, and unnecessary large generated files must not be committed.
