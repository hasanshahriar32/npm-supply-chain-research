# Executed validation workflow

The frozen protocol is `revision_validation_protocol.json`; its initial timestamp precedes new observation requests. The 120-endpoint probability sample, 100 replication roots and source archive are immutable inputs. The source-count strata have 1,716 / 1,473 / 1,959 / 2,010 endpoints, each sampled at n=30. No failed unit is replaced.

Completed work includes 38 full/component/cap/tie runs, 32 exact benchmark instances at three budgets, a fresh bounded dependency acquisition, pinned root workflow observations, an automated endpoint evidence audit, provisional transport diagnostics, and generated tables/figures. The original heuristic's 100-account order is reproduced before ablations.

## Reproduce existing observations

```sh
python3 scripts/verify_journal_revision.py
python3 scripts/study_validated_endpoints.py --label-source automated
python3 scripts/render_journal_validation.py
```

The first command in the full working repository checks raw retained source hashes. A released artifact uses `python3 scripts/reproduce_journal_validation.py --recompute-cohort`, which explicitly validates derived audit inputs rather than redistributing/re-annotating third-party source bodies. All source memberships are retained when candidates or endpoints are restricted.

The captured acquisition timestamps are in UTC. Root/dependency collection and pinned GitHub observations span different request windows; the fresh cohort is not an instantaneous snapshot. It inherits the original ordinary-name frame and has a different graph extent. Its effect-size difference is not attributed solely to temporal change.

## Future acquisition commands

Do not reuse this output directory to claim another independent collection. Freeze a new study version/output path first. The existing capture stages are resumable and do not overwrite captured observations:

```sh
python3 scripts/freeze_journal_validation.py
python3 scripts/collect_endpoint_validation.py registry
python3 scripts/collect_endpoint_validation.py commits
python3 scripts/collect_github_evidence_requests.py manuscript_q1/results/revision_validation/endpoint_audit/requests_commits.json
python3 scripts/collect_endpoint_validation.py directories
python3 scripts/collect_github_evidence_requests.py manuscript_q1/results/revision_validation/endpoint_audit/requests_directories.json
python3 scripts/collect_endpoint_validation.py files
python3 scripts/collect_github_evidence_requests.py manuscript_q1/results/revision_validation/endpoint_audit/requests_files.json
python3 scripts/collect_endpoint_validation.py summarize
```

The executed collection used the connected GitHub fetch tool for GitHub resources; the portable command is an alternative for future capture. Registry/dependency observations use public npm and deps.dev endpoints. Source code and package payloads are never executed by the collection process. The standalone helper can use an existing `gh` authentication or environment token without retaining credentials.

## Independent human review remains required

Each author independently fills their CSV under `../review_packets/`, using the rubric and pinned evidence links in `ENDPOINT_REVIEW_INSTRUCTIONS.md`. Do not copy automated suggestions or fill the other author's sheet. Allowed values are `supported`, `unsupported`, `unknown`; blank remains unreviewed. Add evidence notes for every completed row.

```sh
python3 scripts/study_validated_endpoints.py --label-source human
```

Until both sheets are complete, the command reports pending status and produces no human-reviewed metric table. Disagreements generate `adjudication.csv`; complete each adjudicated label and reason after comparing the independent initial records. The pipeline preserves the initial sheets and reports initial agreement separately. The paper cannot claim completed human review merely because files or tools exist.

After human review, regenerate the audit results, manuscript table/figure and claims using those actual results, record the authors' actual contributions, and obtain both authors' approval of the final version. Neither study execution nor this protocol establishes manuscript approval.
