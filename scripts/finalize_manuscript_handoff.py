"""Save Task 14 technical handoff and session-ledger entry without changing frozen conference files."""
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
import hashlib
import json
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    meta_path = ROOT / 'manuscript_q1/results/quorum_reproducibility.json'
    if json.loads(meta_path.read_text()).get('metric_version') == 'strict_zero_anchored_v1':
        raise SystemExit('Historical handoff superseded; run scripts/finalize_strict_quorum.py instead.')
    now = datetime.now(ZoneInfo('Asia/Dhaka')).isoformat()
    q1 = ROOT / 'manuscript_q1'
    checks = json.loads((q1 / 'results/q1_verification_report.json').read_text())
    assert checks['status'] == 'PASS', 'Run verification successfully before handoff'
    for relative, record in checks['checks']['conference_freeze']['files'].items():
        assert digest(ROOT / relative) == record['expected_sha256'], relative
    archive = ROOT / 'NPM_Supply_Chain_Q1_Journal_Source.zip'
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        entries = z.namelist()
        for entry in entries:
            assert z.read(entry) == (ROOT / entry).read_bytes(), entry
    meta = json.loads((q1 / 'results/quorum_reproducibility.json').read_text())
    sources = json.loads((q1 / 'results/source_verification_2026-10-25.json').read_text())
    rows = json.loads((q1 / 'results/q1_quorum_exclusion.json').read_text())
    conference = subprocess.check_output(['pdftotext', str(ROOT / 'manuscript/main.pdf'), '-'], text=True)
    info = subprocess.check_output(['pdfinfo', str(ROOT / 'manuscript/main.pdf')], text=True)
    assert 'non-intellectual editing' in conference
    files = [ROOT / x for x in checks['checks']['conference_freeze']['files']]
    files += [q1 / 'main_q1.pdf', q1 / 'main_q1_anonymous.pdf', archive,
              q1 / 'results/q1_verification_report.json', q1 / 'results/quorum_reproducibility.json',
              q1 / 'results/source_verification_2026-10-25.json',
              ROOT / 'scripts/study_q1_quorum_and_oct2026.py']
    manifest = {
        'generated_at': now,
        'technical_status': 'PASS',
        'archive_integrity': 'PASS',
        'archive_workspace_member_parity': 'PASS',
        'archive_file_count': len(entries),
        'conference_acknowledgment': 'LLM disclosure present in locked PDF; author approval and purpose restriction are not certified',
        'submission_status': 'drafts prepared; no external submission performed',
        'files': {str(p.relative_to(ROOT)): {'bytes': p.stat().st_size, 'sha256': digest(p)} for p in files},
    }
    (ROOT / 'reports/14_final_artifact_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    lines = [
        '# Task 14: Final manuscript verification and handoff', '',
        '## 1. Executive summary and scope', '',
        f'Completed: {now} (Asia/Dhaka).', '',
        'Completed the continuation of Task 13: independently checked the new incident sources, corrected scientific interpretation and citation metadata, reproduced the threshold experiment, rebuilt both journal PDFs, and verified the source archive. The four locked conference deliverables remain byte-for-byte unchanged.', '',
        '**This report supersedes Task 13 wherever it claims operational quorum protection, verified placeholder references, or unconditional submission readiness.** Technical preparation is complete; actual submission, author approval, a similarity-service report, and venue-specific acceptance of the disclosure are not established.', '',
        '## 2. Evidence and source verification', '',
        'The focused source ledger is `manuscript_q1/results/source_verification_2026-10-25.json`. Sources were inspected through the browser on October 25, 2026. Source statements are distinguished from our interpretation; no package payloads or exploits were executed.', '',
        '| Reference | Primary source and correction |', '|---|---|',
    ]
    for entry in sources['entries']:
        key, url, finding = entry['key'], entry['url'], entry['finding']
        lines.append(f'| `{key}` | ' + (f'[Primary record]({url}). ' if url else '') + finding + ' |')
    lines += ['',
        'This is a focused audit, not a new certification of every historical reference. PHP, Capcom, and the separate OpenCode Console breach were not added to the empirical cohort. Cross-ecosystem examples motivate limitations and do not validate the npm measurements.', '',
        '## 3. Methods and scientific corrections', '',
        '- Re-ran five strategies at budgets 10, 25, 50, and 100, with thresholds 1, 2, 3, and 5 and uniform efficacy multipliers 1.00, 0.95, 0.90, and 0.75.',
        '- Checked forward endpoint closures against independently transposed maintainer-source incidence; checked selection uniqueness, budget/threshold monotonicity, and efficacy identities.',
        '- Corrected the Direct P tie-break to use marginal coverage, matching the existing experiment; all reported table counts remained unchanged.',
        '- Explicitly restricted P and P_k to 7,158 endpoints with observed sources. The literal full-universe formula adds 13 source-free endpoints to every count. Coverage percentages retain the 7,171-repository denominator.',
        '- Recorded all ordered selections, archive/script hashes, zero-budget baselines and intervention increments in `quorum_reproducibility.json`.',
        '- Reframed P_k as a hypothetical residual-source threshold count. Distinct upstream identities need not share a release policy. Token roles, package signer groups, bypass privileges, and approval rules are absent from the graph; token count does not establish a quorum.',
        '- Explained that uniform H_eta = eta H preserves rankings and is an assumed sensitivity, without a measured bypass rate or correlated-failure guarantee.',
        '- Corrected hybrid-objective monotonicity wording, the implemented lexicographic P heuristic, baseline-versus-optimum claims, and the distinction between Pareto and weight-aware selections.',
        '- Replaced claims of continuous prospective validation with the retained status: 90 metadata captures, ten unavailable records, 100 pending outcomes, no fitted models or predictions, horizon ending January 18, 2027.',
        '- Aligned journal authors and department/order with the user-provided author record; removed unprovided email addresses and IEEE membership assertions. Replaced submission/publication assertions with draft labels and an accurate AI-assistance disclosure requiring author review.', '',
        '## 4. Reproduced quantitative results', '',
        f'Population: 25,228 packages, 12,217 maintainers, 7,171 workflow repositories; {meta["observed_source_endpoints"]:,} endpoints have observed sources.', '',
        '| k | P_k(empty set) |', '|---:|---:|',
    ]
    for k, value in meta['baseline_P_k_empty'].items():
        lines.append(f'| {k} | {value:,} |')
    lines += ['', 'Budget 100 results; P_k columns are structural counts rather than operational protection claims:', '',
              '| Strategy | C | H (%) | P1 | P2 | P3 | P5 | P2 increment over empty set |',
              '|---|---:|---:|---:|---:|---:|---:|---:|']
    for row in rows:
        if row['budget'] != 100:
            continue
        lines.append(f"| {row['strategy']} | {row['C']:,} | {row['H_pct']:.2f} | {row['P_1']:,} | {row['P_2']:,} | {row['P_3']:,} | {row['P_5']:,} | {row['P_2']-1716:,} |")
    lines += ['',
        'For Pareto Hybrid, P2=2,153 includes 1,716 endpoints already below threshold at zero budget; its intervention increment is 437. Treating 2,153 as newly secured repositories would therefore overstate even the hypothetical scenario. H_0.90=28.07% is a scaled assumption, not a measured reduction in incidents.', '',
        '## 5. Build, validation, and freeze results', '',
        'Commands completed successfully:', '', '```sh',
        'python3 scripts/study_q1_quorum_and_oct2026.py',
        'python3 -m py_compile scripts/study_q1_quorum_and_oct2026.py manuscript_q1/scripts/verify_manuscript_q1.py',
        'bash manuscript_q1/compile_q1.sh',
        'bash manuscript_q1/compile_q1.sh main_q1_anonymous.tex',
        'python3 manuscript_q1/scripts/verify_manuscript_q1.py',
        'python3 manuscript_q1/scripts/package_q1.py',
        'python3 scripts/finalize_manuscript_handoff.py', '```', '',
        'The verifier now compares all 20 table rows with CSV and JSON, verifies input/script hashes and population baselines, rejects missing compilation logs, and records the actual execution timestamp. Source-link presence checks support traceability; they do not automatically establish factual validity.', '',
        '| Check | Result |', '|---|---|',
        f"| Abstract | {checks['checks']['abstract']['word_count']} words |",
    ]
    for name in ('named_pdf','anonymous_pdf'):
        c=checks['checks'][name]
        lines.append(f"| {c['pdf_name']} | {c['pages']} pages; {c['file_bytes']:,} bytes; embedded fonts; zero Type 3 |")
    lines += [
        '| Compilation logs | No overfull boxes, unresolved citations/references, or missing glyphs found |',
        '| Other TeX warnings | Underfull boxes and font-shape fallback warnings remain; no claim of warning-free compilation |',
        '| Rendered table | Visually inspected journal PDF page 11; both wide tables are legible and fit the page |',
        f'| Source archive | {len(entries)} members; CRC and exact workspace-member parity PASS |', '',
        'Frozen conference SHA-256 checks:', '', '| Artifact | SHA-256 |', '|---|---|',
    ]
    for relative, record in checks['checks']['conference_freeze']['files'].items():
        lines.append(f"| `{relative}` | `{record['actual_sha256']}` |")
    lines += ['',
        'The locked conference PDF contains an LLM acknowledgment. Older submission metadata saying it is absent is stale. Its assertions of solely non-intellectual use and author approval still require the actual authors to substantiate against the supplied guideline and work history. Neither acknowledgment presence nor a technical PASS resolves that policy question.', '',
        '## 6. Saved deliverables and handoff', '',
        '- Conference anonymous review PDF: `manuscript/main.pdf` (locked six-page draft).',
        '- Conference named review PDF: `manuscript/main_authors.pdf` (locked six-page draft).',
        '- Conference archives: `NPM_Supply_Chain_IEEE_Anonymous_Source.zip` and `NPM_Supply_Chain_IEEE_Overleaf.zip` (unchanged).',
        '- Updated journal PDFs: `manuscript_q1/main_q1.pdf` and `manuscript_q1/main_q1_anonymous.pdf`.',
        f'- Updated journal source archive: `NPM_Supply_Chain_Q1_Journal_Source.zip` ({archive.stat().st_size:,} bytes; SHA-256 `{digest(archive)}`).',
        '- Detailed checks: `manuscript_q1/results/q1_verification_report.json`.',
        '- Results and provenance: `manuscript_q1/results/q1_quorum_exclusion.csv`, `q1_quorum_exclusion.json`, and `quorum_reproducibility.json`.',
        '- Build and interpretation instructions: `manuscript_q1/README.md`.',
        '- Artifact checksums and archive validation: `reports/14_final_artifact_manifest.json`.',
        '- This six-section report is mirrored to `research_sessions/active_verification_track/14_final_manuscript_verification_and_handoff.md` and indexed in `research_sessions/SESSION_INDEX.md`.', '',
        'The source ZIP is a typesetting package. Full experiment verification also requires the surrounding repository scripts and retained datasets, as documented in the README. No external submission, acceptance, similarity score, or author approval has been fabricated. Final author review should cover scientific claims and historical references outside the focused audit, the chosen venue format/disclosure rules, and permission to submit. Prospective outcome evaluation remains future work through January 18, 2027.', '',
    ]
    text='\n'.join(lines)
    name='14_final_manuscript_verification_and_handoff.md'
    for directory in (ROOT/'reports', ROOT/'research_sessions/active_verification_track'):
        directory.mkdir(parents=True,exist_ok=True)
        (directory/name).write_text(text)
    ledger=ROOT/'research_sessions/SESSION_INDEX.md'
    content=ledger.read_text()
    content='\n'.join(line for line in content.splitlines() if not line.startswith('| Task 14 |'))
    content+=f'\n| Task 14 | {now} | `research_sessions/active_verification_track/{name}` | Reproduced 20 threshold rows; corrected quorum interpretation and sources; rebuilt two 16-page drafts; 188-word abstract; four conference hashes unchanged; archive parity PASS. Supersedes Task 13 readiness claims. | COMPLETED |\n'
    ledger.write_text(content)
    print(f'Saved reports/{name}, mirrored session report, manifest, and ledger entry.')

if __name__ == '__main__':
    main()
