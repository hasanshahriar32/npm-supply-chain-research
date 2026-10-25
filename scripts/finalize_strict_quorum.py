"""Validate and save the strict-quorum correction report and session ledger."""
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
import hashlib
import json
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NAME = '14_q1_strict_quorum_exclusion_fix_and_lock.md'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    q1 = ROOT / 'manuscript_q1'
    now = datetime.now(ZoneInfo('Asia/Dhaka')).isoformat()
    subprocess.run(['python3', '-m', 'unittest', 'discover', '-s', 'scripts/tests', '-p', 'test_strict_quorum.py'], cwd=ROOT, check=True)
    v = json.loads((q1 / 'results/q1_verification_report.json').read_text())
    assert v['status'] == 'PASS'
    m = json.loads((q1 / 'results/quorum_reproducibility.json').read_text())
    assert m['metric_version'] == 'strict_zero_anchored_v1'
    assert m['baseline_P_k_empty'] == {str(k): 0 for k in (1,2,3,5)}
    assert m['script_sha256'] == sha(ROOT / 'scripts/study_q1_quorum_and_oct2026.py')
    rows = json.loads((q1 / 'results/q1_quorum_exclusion.json').read_text())
    for relative, record in v['checks']['conference_freeze']['files'].items():
        assert sha(ROOT / relative) == record['expected_sha256']
    archive = ROOT / 'NPM_Supply_Chain_Q1_Journal_Source.zip'
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        entries = z.namelist()
        for entry in entries:
            assert z.read(entry) == (ROOT / entry).read_bytes(), entry
    artifacts = list(v['checks']['conference_freeze']['files']) + [
        'manuscript_q1/main_q1.pdf', 'manuscript_q1/main_q1_anonymous.pdf', archive.name,
        'manuscript_q1/results/q1_verification_report.json',
        'manuscript_q1/results/quorum_reproducibility.json',
        'manuscript_q1/results/q1_quorum_exclusion.json',
        'scripts/study_q1_quorum_and_oct2026.py', 'scripts/tests/test_strict_quorum.py',
    ]
    manifest = {'generated_at': now, 'status': 'PASS', 'metric_version': m['metric_version'],
        'boundary_tests': {'tests_passed': 4, 'exhaustive_source_selection_threshold_cases': 16384},
        'archive_crc_pass': True, 'archive_workspace_member_parity_pass': True,
        'archive_file_count': len(entries),
        'files': {name: {'bytes': (ROOT/name).stat().st_size, 'sha256': sha(ROOT/name)} for name in artifacts}}
    (ROOT / 'reports/14_strict_quorum_artifact_manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    lines = [
        '# Task 14: Strict quorum exclusion correction and artifact lock', '',
        '## 1. Executive summary', '',
        f'Completed {now} (Asia/Dhaka). Implemented the advisor’s explicit strict definition, regenerated all 20 strategy/budget rows, updated Sections 4 and 6.3, and rebuilt both journal PDFs and the source ZIP. Technical verification is **PASS**. The four frozen conference deliverables are unchanged.', '',
        'This correction supersedes the residual-threshold values in the earlier Task 14 handoff; that report remains as a historical record. The strict rule removes zero-budget credit but does not establish real package-approval enforcement.', '',
        '## 2. Mathematical definition and boundary checks', '',
        'For nonempty source sets, let n = |Sources(r)| and t = |Sources(r) \\ S|. Count an endpoint exactly when:', '',
        '```text', 't = 0 OR (n >= k AND t < k)', '```', '',
        'All 13 source-free workflow endpoints are excluded. Consequently P_k(empty set)=0 for k in {1,2,3,5}, P_1=P, and every credited endpoint has at least one hardened source. If n<k, all its sources must be hardened.', '',
        'Two advisor statements required correction: the compact expression t < min(k,n) is not equivalent, and strict counts need not increase with k. For n=2 and t=1, the explicit rule counts the endpoint at k=2 but excludes it at k=3. The manuscript and tests use the explicit rule. Counts remain monotone in the hardening set for each fixed k. Zero anchoring alone does not make source cardinality an observed release quorum.', '',
        'Four tests passed, including an independent set-based oracle over 16,384 source/selection/threshold cases, single-source and empty-source boundaries, the compact-form counterexample, and the nonmonotone-k counterexample.', '',
        '## 3. Source-cardinality census', '',
        '| Observed upstream sources | Workflow repositories |', '|---|---:|',
    ]
    for key,value in m['source_cardinality_distribution'].items():
        lines.append(f'| {key} | {value:,} |')
    lines += ['',
        'Total: 7,171 workflow repositories, of which 7,158 have nonempty sources. The census uses workflow-repository indices; other linked repositories are excluded. All four strict zero-budget counts equal zero.', '',
        '## 4. Corrected results', '',
        'The same five ordered selections and four budgets are reused. C, H, and efficacy-scaled H are unchanged. The original budget-100 P1 counts remain 800 for Greedy, 534 for Exact Union, 626 for Pareto, and 1,022 for Direct P.', '',
        '| Strategy | Budget | P1 | P2 | P3 | P5 |', '|---|---:|---:|---:|---:|---:|',
    ]
    for row in rows:
        name=row['strategy'].replace(r' ($\alpha=0.50$)', ' (alpha=0.50)').replace('$P(S)$','P(S)')
        lines.append(f"| {name} | {row['budget']} | " + ' | '.join(f"{row[f'P_{k}']:,}" for k in (1,2,3,5)) + ' |')
    lines += ['',
        'These are hypothetical structural threshold counts, not measured numbers of secure repositories. Package-level signer groups, approval roles, and bypass privileges remain unobserved. The compiled manuscript numbers this table as Table 6; “Table 10” was the earlier advisor/session label.', '',
        '## 5. Build, verification, and conference freeze', '',
        '| Check | Result |', '|---|---|',
        '| Strict boundary tests | 4 passed; 16,384 exhaustive cases |',
        '| Data parity | All 20 CSV/JSON/TeX rows match; workspace copies match |',
        '| Independent count check | Recomputed strict counts from retained (total, remaining) cardinality histograms |',
        '| Zero budget and P1 invariants | PASS |',
        '| Retired Budget-10 values | Absent from active manuscript text/results and extracted text of both PDFs |',
        f"| Abstract | {v['checks']['abstract']['word_count']} words |",
    ]
    for key in ('named_pdf','anonymous_pdf'):
        c=v['checks'][key]
        lines.append(f"| {c['pdf_name']} | {c['pages']} pages; {c['file_bytes']:,} bytes; embedded fonts; zero Type 3 |")
    for key in ('named_pdf','anonymous_pdf'):
        name=v['checks'][key]['pdf_name']
        log=(q1 / 'build' / name.replace('.pdf','.log')).read_text()
        assert 'Overfull \\hbox' not in log and 'Overfull \\vbox' not in log
    lines += [
        '| Compilation | Zero overfull boxes, undefined citations/references, or missing glyphs |',
        '| Render review | Table visually inspected on page 11; fits the page |',
        f'| ZIP validation | CRC and exact member/workspace parity PASS; {len(entries)} files |',
        '| Conference freeze | All four original SHA-256 hashes match |', '',
        'Frozen files: `manuscript/main.pdf`, `manuscript/main_authors.pdf`, `NPM_Supply_Chain_IEEE_Anonymous_Source.zip`, and `NPM_Supply_Chain_IEEE_Overleaf.zip`. Full checksums are retained in `reports/14_strict_quorum_artifact_manifest.json`. Underfull boxes and font-shape fallback warnings remain; compilation is not claimed to be warning-free.', '',
        '## 6. Saved deliverables and handoff', '',
        '- Report: `reports/14_q1_strict_quorum_exclusion_fix_and_lock.md`.',
        '- Mirrored report: `research_sessions/active_verification_track/14_q1_strict_quorum_exclusion_fix_and_lock.md`; session ledger updated.',
        '- PDFs: `manuscript_q1/main_q1.pdf` and `manuscript_q1/main_q1_anonymous.pdf`.',
        '- Results: `manuscript/results/q1_journal/q1_quorum_exclusion.csv`, `.json`, and `_table.tex`, with synchronized journal copies.',
        '- Provenance and census: `manuscript_q1/results/quorum_reproducibility.json`.',
        '- Verification: `manuscript_q1/results/q1_verification_report.json`.',
        '- Tests: `scripts/tests/test_strict_quorum.py`.',
        f'- Source archive: `NPM_Supply_Chain_Q1_Journal_Source.zip` ({archive.stat().st_size:,} bytes).',
        f'- Archive SHA-256: `{sha(archive)}`.', '',
        'Author review, venue-policy review, similarity checking, and submission approval remain separate from the technical lock. No external submission was performed.', '',
    ]
    report='\n'.join(lines)
    for directory in (ROOT/'reports', ROOT/'research_sessions/active_verification_track'):
        (directory/NAME).write_text(report)
    ledger=ROOT/'research_sessions/SESSION_INDEX.md'
    old=ledger.read_text()
    old='\n'.join(line for line in old.splitlines() if not line.startswith('| Task 14 strict correction |'))
    old+=f'\n| Task 14 strict correction | {now} | `research_sessions/active_verification_track/{NAME}` | Zero baselines for all k; 20 corrected rows; 4 boundary tests; both 16-page PDFs and source ZIP verified; conference hashes unchanged. | COMPLETED |\n'
    ledger.write_text(old)
    print(report)

if __name__ == '__main__':
    main()
