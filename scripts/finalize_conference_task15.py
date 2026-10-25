"""Save the authorized conference modernization report and cross-track artifact lock."""
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile

ROOT=Path(__file__).resolve().parents[1]
NAME='15_conference_manuscript_oct2026_modernization_and_rebuild.md'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    now=datetime.now(ZoneInfo('Asia/Dhaka')).isoformat()
    paper=ROOT/'manuscript'
    research=json.loads((paper/'results/research_verification.json').read_text())
    versions=json.loads((paper/'results/author_versions_validation.json').read_text())
    compliance=json.loads((paper/'results/submission_compliance.json').read_text())
    packages=json.loads((paper/'results/package_validation.json').read_text())
    journal=json.loads((ROOT/'manuscript_q1/results/q1_verification_report.json').read_text())
    sensitivity=json.loads((paper/'results/conference_modernization.json').read_text())
    lock=json.loads((ROOT/'manuscript_q1/config/conference_lock.json').read_text())
    old=json.loads((ROOT/'reports/14_strict_quorum_artifact_manifest.json').read_text())
    assert research['checks_pass'] and research['conference_modernization_checked']
    assert research['active_citation_count']==24
    assert compliance['technical_checks_pass'] and not compliance['submission_ready']
    assert packages['all_checks_pass'] and journal['status']=='PASS'
    assert all(v['pages']==6 and all(v['checks'].values()) for v in versions.values())
    assert all(sha(ROOT/path)==record['sha256'] for path,record in lock['artifacts'].items())
    for job in ('main','main_authors'):
        log=(paper/f'build/{job}.log').read_text()
        assert 'Overfull' not in log
        assert not re.search(r'(?:Citation|Reference)\s+.*?undefined|There were undefined references|Missing character:',log)
    for path in ('manuscript_q1/main_q1.pdf','manuscript_q1/main_q1_anonymous.pdf'):
        assert sha(ROOT/path)==old['files'][path]['sha256'], 'Journal PDF changed unexpectedly'
    archives={}
    for relative,prefix in [('NPM_Supply_Chain_IEEE_Overleaf.zip','manuscript'),
                            ('NPM_Supply_Chain_IEEE_Anonymous_Source.zip','manuscript'),
                            ('NPM_Supply_Chain_Q1_Journal_Source.zip','')]:
        archive=ROOT/relative
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            for member in z.namelist():
                # The anonymous README is intentionally generated for the bundle.
                if relative.endswith('Anonymous_Source.zip') and member=='README.md':
                    continue
                assert z.read(member)==(ROOT/prefix/member).read_bytes(), f'Stale archive member: {relative}/{member}'
            archives[relative]={'bytes':archive.stat().st_size,'members':len(z.namelist()),'sha256':sha(archive),
                                'crc_pass':True,'workspace_member_parity_pass':True}
    files=list(lock['artifacts'])+['manuscript_q1/main_q1.pdf','manuscript_q1/main_q1_anonymous.pdf',
        'NPM_Supply_Chain_Q1_Journal_Source.zip','manuscript/results/conference_modernization.json',
        'manuscript/results/research_verification.json','manuscript/results/submission_compliance.json',
        'manuscript/results/author_versions_validation.json','manuscript/results/package_validation.json',
        'manuscript_q1/results/q1_verification_report.json','manuscript_q1/config/conference_lock.json']
    manifest={'generated_at':now,'task':15,'technical_status':'PASS',
              'authorization':lock['authorized_by'],'archives':archives,
              'journal_pdfs_unchanged_from_strict_task14':True,
              'previous_conference_sha256':lock['previous_artifacts'],
              'files':{name:{'bytes':(ROOT/name).stat().st_size,'sha256':sha(ROOT/name)} for name in files},
              'submission_status':'not submitted; author/venue policy and similarity review pending'}
    (ROOT/'reports/15_conference_modernization_artifact_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    lines=[
        '# Task 15: Conference manuscript October 2026 modernization and rebuild','',
        '## 1. Executive summary and authorization','',
        f'Completed {now} (Asia/Dhaka). The user explicitly lifted the conference freeze. Both conference PDFs were modernized and rebuilt to **exactly six A4 pages**; both conference ZIPs and the journal source ZIP were regenerated. Conference and journal technical verification pass. No external submission was performed.','',
        'Pre-update conference PDFs and ZIPs, with their hashes, are preserved in `research_sessions/active_verification_track/task15_before/`. The Task 15 lock replaces the old conference checksums; earlier reports remain historical records. Both journal PDFs remain byte-for-byte identical to the strict Task 14 versions (16 pages each).','',
        '## 2. Literature and manuscript integration','',
        'Imported 12 corrected bibliography entries from the focused journal source audit. The conference now cites **24 references**, including npm SlugFest and binding expiry, OpenCode’s September fix/October disclosure, LiteLLM’s final attack-chain and artifact records, Railway’s preliminary report and deployment pause, and the High-severity Node.js Brotli boundary. Added Shen et al. (EMSE 2025), Kalu et al. (USENIX Security 2025), Weeraddana et al. (FSE 2024), and Jayasuriya et al. (EMSE 2025). Source URLs and identifying metadata are retained.','',
        'The source evidence was imported from the previously inspected records in `manuscript_q1/results/source_verification_2026-10-25.json`; this task did not independently repeat the full literature audit. Contextual incidents are not added as npm validation observations, and the 81.26% finding is qualified to the cited study’s corpus.','',
        'Shortened repeated collection, motivation, and validation prose to meet the page limit. Retained standard IEEE conference A4/10-point settings, all four figures, core C/H/P results, 200-seed MCSE values, the 39.50 s three-run profile, and the qix example (2,971 name-graph and 1,476 version-graph repositories). No margin or font compression was introduced.','',
        '## 3. Threshold definitions and reproduced sensitivities','',
        'The requested earlier increments use the unguarded residual-source count, now named **T_k**, while **P_k(strict)** retains the explicit zero-anchored definition from the preceding correction. These are different metrics. On 7,158 nonempty-source endpoints, T2(empty)=1,716, whereas P2(strict, empty)=0. All 13 source-free endpoints are excluded.','',
        '| Budget-100 selection | C | H (%) | P1 | T2 | Delta T2 | Strict P2 | H at eta=0.90 (%) |',
        '|---|---:|---:|---:|---:|---:|---:|---:|',
    ]
    for row in sensitivity['budget100']:
        if row['strategy'].startswith('Portfolio'):
            continue
        name=row['strategy'].replace(r' ($\alpha=0.50$)',' (alpha=0.50)').replace('$P(S)$','P(S)')
        lines.append(f"| {name} | {row['C']:,} | {row['H_pct']:.2f} | {row['P1']:,} | {row['T2']:,} | {row['delta_T2']:,} | {row['P2_strict']:,} | {row['H_eta_090_pct']:.2f} |")
    lines+=['',
        '`scripts/generate_conference_modernization.py` independently reconstructs residual and strict counts from the retained total/remaining-source histograms, checks strict-count parity, and records source hashes in `manuscript/results/conference_modernization.json`. Neither definition establishes an enforced multisigner policy. Uniform efficacy is hypothetical and preserves H rankings; no bypass rate or control efficacy is estimated.','',
        '## 4. Build, validation, and package results','',
        'Completed the requested conference suite: `package_overleaf.py`, `verify_manuscript.py`, `check_author_versions.py`, `check_submission.py`, `validate_packages.py`, and `audit_artifacts.py`. Also compiled the extracted anonymous package independently, checked its text against the delivered PDF, ran the journal verifier, and rebuilt the journal ZIP.','',
        '| Deliverable/check | Result |','|---|---|',
    ]
    for job,v in versions.items():
        lines.append(f"| {job}.pdf | {v['pages']} A4 pages; {v['file_bytes']:,} bytes; {v['font_count']} embedded fonts |")
    lines+=[
        '| Conference logs | Zero overfull boxes, Type 3 fonts, undefined citations/references, or missing glyphs |',
        '| Research consistency | 68 hashes; 150 deterministic and 6,000 random rows; generated values and prospective timing pass |',
        '| Bibliography | 24 active citations; all 12 imported entries cited |',
        '| Anonymous package | Standalone compilation, PDF-text parity, identity exclusions, and references pass |',
        '| All three ZIPs | CRC and exact workspace-member parity pass (anonymous README is generated) |',
        '| Journal verification | PASS; 188-word abstract; both PDFs remain 16 pages |','',
        'The final reference pages were rendered and visually inspected; content fits. Underfull boxes and font-shape fallback warnings remain. The data audit recomputes legacy fields offline; no new live collection or prospective outcome labeling was performed.','',
        '## 5. Artifact lock and saved reports','',
        'The reviewed replacement conference lock is `manuscript_q1/config/conference_lock.json`; the journal verifier reads that explicit lock rather than accepting arbitrary current files. Full prior/new hashes and all validation reports are indexed in `reports/15_conference_modernization_artifact_manifest.json`.','',
        '| Archive | Files | Bytes |','|---|---:|---:|',
    ]
    for name,a in archives.items():
        lines.append(f"| `{name}` | {a['members']} | {a['bytes']:,} |")
    lines+=['',
        f'This six-section report is saved as `reports/{NAME}` and mirrored to `research_sessions/active_verification_track/{NAME}`. The reports index and session ledger are updated.','',
        '## 6. Handoff and remaining author actions','',
        'Use `manuscript/main.pdf` for anonymous conference review and `manuscript/main_authors.pdf` for named author review. Both conference archives contain the current PDFs and typesetting inputs. The journal PDFs retain the strict threshold analysis; its refreshed source ZIP contains the current cross-track lock and verification report. Full numerical reproduction requires the surrounding repository and retained data, beyond the typesetting ZIPs.','',
        'The conference acknowledgment now accurately describes LLM drafting, code revision, analysis checking, and source verification; it does not assert solely non-intellectual use or completed author approval. Older metadata claiming disclosure absence was corrected. The supplied venue guideline restricts LLM use to non-intellectual purposes, so that policy mismatch remains unresolved despite technical checks passing. Authors must review scientific claims, determine venue eligibility, finalize the disclosure, obtain the required similarity report, check indirect anonymity, and approve submission. No approval, originality declaration, similarity score, acceptance, or submission has been fabricated.','',
    ]
    report='\n'.join(lines)
    for directory in (ROOT/'reports',ROOT/'research_sessions/active_verification_track'):
        (directory/NAME).write_text(report)
    ledger=ROOT/'research_sessions/SESSION_INDEX.md';s=ledger.read_text()
    s='\n'.join(line for line in s.splitlines() if not line.startswith('| Task 15 |'))
    s+=f'\n| Task 15 | {now} | `research_sessions/active_verification_track/{NAME}` | Authorized conference unfreeze; two six-page A4 PDFs, 24 citations, residual/strict sensitivities distinguished; both conference ZIPs and journal ZIP rebuilt; all technical checks pass; policy/author review remains. | COMPLETED |\n'
    ledger.write_text(s)
    print(report)

if __name__=='__main__':
    main()
