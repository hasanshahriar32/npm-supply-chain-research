# Task 09: Extraction of Temporal Reconstruction, Release-Authority, and Incident Tables for the Q1 Journal

## 1. Execution Metadata

- **Task ID:** Task 09
- **Timestamp:** 2026-10-21 03:45:00 UTC+06:00
- **Working Directory:** `/home/ashik/Desktop/npm-supply-chain-research`
- **Execution Script:** `scripts/extract_q1_temporal_and_authority_tables.py`
- **Output Directory:** `manuscript/results/q1_journal/`
- **Generated Tables and Datasets:**
  - `q1_release_authority_audit.csv` & `q1_release_authority_table.tex`
  - `q1_temporal_reconstruction_summary.csv` & `q1_temporal_reconstruction_table.tex`
  - `q1_incident_case_study.csv` & `q1_incident_case_study_table.tex`
- **Conference Codebase Safety:** Zero modifications to conference manuscript files (`main.tex`, `main.pdf`, `sections/*.tex`) or root submission ZIP packages (`NPM_Supply_Chain_IEEE_Anonymous_Source.zip`, `NPM_Supply_Chain_IEEE_Overleaf.zip`). All conference verification tests remain 100% green.

---

## 2. Quantitative and Structural Findings

### 2.1 Pre-Event Release-Authority & Cryptographic Provenance Availability (Report 95 & 97)
Parsing `platform/research/95_release_authority_metadata_availability_audit.json` and `97_official_npm_provenance_attestation_access_assessment.json` across 45 verified pre-event source snapshots yields:
- **Predecessor Version Availability:** 44/45 (97.8%) versions have an immediate predecessor in the registry packument, enabling automated SemVer diffing.
- **Repository URL Comparison:** 42/45 (93.3%) versions have comparable git repository descriptors, enabling repository transfer/discontinuity detection.
- **gitHead Commit SHA Availability:** 34/45 (75.6%) snapshots record the exact git commit hash at publish time.
- **Distribution Integrity Hashes:** 45/45 (100.0%) tarballs contain cryptographic `dist.integrity` hashes (SHA-512 / SHA-1).
- **Embedded Maintainer Signatures:** 45/45 (100.0%) snapshots have embedded maintainer usernames in the registry metadata.
- **Official npm Sigstore Provenance:** 0/45 (0.0%) historical snapshots possess public cryptographic build provenance attestations, establishing that retrospective attestation auditing is not accessible via public metadata-only endpoints.

---

### 2.2 Bounded Recursive SemVer Cutoff Reconstruction (Report 74)
Parsing `platform/research/74_bounded_recursive_registry_semver_graph_manifest.json` demonstrates the feasibility of time-bounded dependency resolution:
- **Pre-Event Root Cutoffs:** 45 snapshots strictly time-indexed prior to active compromise ($t_{\text{cutoff}} < t_{\text{incident}}$).
- **Resolution Strategy:** Highest valid satisfying version under npm SemVer semantics without future leakage.
- **Traversal Bounds:** Max depth $\le 3$, node budget cap $N_{\max} = 250$ nodes per root.
- **Resolution Fidelity:** Only 1 out of 45 roots (2.2%, `@asyncapi/generator`) reached the node budget cap.
- **Graph Coverage:** 1,848 reconstructed SemVer edges across 1,272 distinct nodes, with only 7 unresolved edges across the entire ecosystem benchmark (99.89% resolution completeness).

---

### 2.3 Real-World Compromised Package Representation Distortion & Prioritization (Task 04)
The extracted case study across the 15 unique compromised packages (16 assessments) in our 25,228-package ecosystem graph demonstrates:
1. **Severe Blast-Radius Phantom Inflation:** Under package-name projection, `chalk` reaches 5,293 repos vs. 2,761 under version continuity (+91.7% phantom inflation), `ansi-styles` reaches 5,133 vs. 2,761 (+85.9%), `simple-swizzle` reaches 2,969 vs. 767 (+287.1%), and `debug` reaches 2,971 vs. 2,362 (+25.8%).
2. **Co-Maintenance Masking (`qix` Phishing Case Study):** Maintainer `qix` (author of `debug`, `simple-swizzle`, `backslash`) ranks #2,298 by portfolio size and is omitted beyond rank 100 under Greedy Coverage, yet ranks #8 under Exact Union (#5 under version continuity) and #4 under Pareto Hybrid ($\alpha=0.50$).
3. **Qualification:** All metrics reflect the observed June 2026 snapshot and serve as a structural representation case study rather than a time-aligned predictive forecast.

---

## 3. Code and Manuscript Diffs Performed

1. **Created Extraction Tool:** [`scripts/extract_q1_temporal_and_authority_tables.py`](file:///home/ashik/Desktop/npm-supply-chain-research/scripts/extract_q1_temporal_and_authority_tables.py).
2. **Generated Publication Assets in `manuscript/results/q1_journal/`:**
   - `q1_release_authority_audit.csv` & `q1_release_authority_table.tex`
   - `q1_temporal_reconstruction_summary.csv` & `q1_temporal_reconstruction_table.tex`
   - `q1_incident_case_study.csv` & `q1_incident_case_study_table.tex`
3. **Conference Codebase Immutable:** Zero lines modified in `manuscript/sections/*.tex`, `manuscript/main.pdf`, or root submission ZIPs.

---

## 4. Anomaly and Vulnerability Flags

1. **Retrospective Attestation Gaps:**
   - As documented in `97_official_npm_provenance_attestation_access_assessment.json`, version-specific Sigstore provenance bundles cannot be audited purely from historical npm metadata tarballs without downloading full payloads or accessing private registry endpoints. Journal text must explicitly cite this constraint.
2. **Snapshot Reach vs. Historical Impact:**
   - The 15 compromised package assessments measure structural reach on the June 2026 dependency graph; they illustrate representation sensitivity and co-maintenance overlap rather than pre-incident historical exposure.

---

## 5. Ledger Confirmation

Appended Task 09 record to [`research_sessions/SESSION_INDEX.md`](file:///home/ashik/Desktop/npm-supply-chain-research/research_sessions/SESSION_INDEX.md) and [`reports/README.md`](file:///home/ashik/Desktop/npm-supply-chain-research/reports/README.md):
```markdown
| Task 09 | 2026-10-21 03:45:00 UTC+06:00 | `research_sessions/active_verification_track/09_q1_temporal_and_authority_table_extraction.md` | Extracted release-authority (45 snapshots, 97.8% predecessor availability), SemVer reconstruction (1,848 edges, 99.89% resolution), and 16-incident case study tables for Q1 journal. | COMPLETED |
```

---

## 6. Handoff Payload for Principal Research Advisor

```text
========================================================================================
TASK 09 TEMPORAL & AUTHORITY EXTRACTION HANDOFF PAYLOAD
========================================================================================
1. EXTRACTED Q1 TABLES (manuscript/results/q1_journal/):
   - q1_release_authority_table.tex & q1_release_authority_audit.csv:
     * 45 pre-event source snapshots audited.
     * 44/45 predecessor versions available (97.8%).
     * 42/45 repository URLs available for diffing (93.3%).
     * 34/45 gitHead commits recorded (75.6%).
     * 45/45 dist.integrity hashes present (100.0%).
     * 0/45 public Sigstore/SLSA attestation bundles available via metadata.
   - q1_temporal_reconstruction_table.tex & q1_temporal_reconstruction_summary.csv:
     * 45 pre-event cutoffs evaluated.
     * 1,848 reconstructed SemVer edges across 1,272 nodes.
     * Only 1 root capped at N_max=250 (2.2%); 99.89% resolution completeness.
   - q1_incident_case_study_table.tex & q1_incident_case_study.csv:
     * 15 packages (16 assessments) in study graph.
     * Quantified phantom inflation: chalk (+91.7%), ansi-styles (+85.9%), simple-swizzle (+287.1%).
     * Maintainer qix captured at #8 (Union) and #4 (Pareto p=0.50) vs >100 (Greedy).
========================================================================================
```
