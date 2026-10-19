#!/usr/bin/env python3
"""Check delivered ZIP contents and optionally compile the anonymous package."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

PAPER = Path(__file__).resolve().parents[1]
ROOT = PAPER.parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--compile-anonymous', action='store_true')
args = parser.parse_args()
authors = json.loads((PAPER/'submission_files/authors.json').read_text())
private = [a['name'] for a in authors['authors_in_supplied_order']] + [authors['institution']]
checks = {}
archives = {}
for label, name in [('working', 'NPM_Supply_Chain_IEEE_Overleaf.zip'), ('anonymous', 'NPM_Supply_Chain_IEEE_Anonymous_Source.zip')]:
    path = ROOT / name
    with zipfile.ZipFile(path) as archive:
        members = set(archive.namelist())
        checks[label+'_archive_integrity'] = archive.testzip() is None
        checks[label+'_pdf_matches_current'] = archive.read('main.pdf') == (PAPER/'main.pdf').read_bytes()
        checks[label+'_research_inputs_present'] = {'results/research_numbers.tex','results/research_method_rows.tex'} <= members
        if label == 'working':
            checks['named_pdf_matches_current'] = archive.read('main_authors.pdf') == (PAPER/'main_authors.pdf').read_bytes()
            checks['both_entry_points_present'] = {'main.tex','main_authors.tex','config/authors.tex'} <= members
        else:
            checks['named_material_excluded'] = not any(name in members for name in ('main_authors.tex','main_authors.pdf','config/authors.tex','submission_files/authors.json'))
            checks['working_research_notes_excluded'] = not any(n.startswith(('research/','submission_files/')) for n in members)
            checks['no_authors_in_text_sources'] = all(not any(s.casefold() in archive.read(n).decode().casefold() for s in private) for n in members if Path(n).suffix in {'.tex','.bib','.md','.sh'})
        archives[label] = {'filename': name, 'files':len(members), 'bytes':path.stat().st_size,
            'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
if args.compile_anonymous:
    with tempfile.TemporaryDirectory(prefix='npm-anonymous-source-') as directory:
        with zipfile.ZipFile(ROOT / archives['anonymous']['filename']) as archive:
            archive.extractall(directory)
        build = subprocess.run(['bash','compile.sh'], cwd=directory, capture_output=True, text=True)
        checks['standalone_anonymous_compilation'] = build.returncode == 0
        if build.returncode:
            print(build.stdout[-3000:]+build.stderr[-3000:])
        else:
            pdf = Path(directory)/'main.pdf'
            text = ' '.join(subprocess.check_output(['pdftotext',str(pdf),'-'], text=True).split())
            checks['standalone_pdf_anonymous'] = 'Anonymous Authors' in text and all(name not in text for name in private)
            log = (Path(directory)/'build/main.log').read_text(errors='replace')
            checks['standalone_no_overfull_boxes'] = 'Overfull' not in log
            checks['standalone_citations_resolved'] = 'There were undefined references' not in log and 'Citation `' not in log
            original = ' '.join(subprocess.check_output(['pdftotext',str(PAPER/'main.pdf'),'-'], text=True).split())
            checks['standalone_text_matches_current_pdf'] = text == original
report = {'archives':archives, 'checks':checks, 'all_checks_pass':all(checks.values()),
    'scope':'Archive integrity, current PDF binding, identity exclusions, generated inputs and optional standalone compilation; manual indirect-identity review remains separate.'}
(PAPER/'results/package_validation.json').write_text(json.dumps(report, indent=2)+'\n')
for name, passed in checks.items():
    print(('PASS ' if passed else 'FAIL ')+name)
raise SystemExit(0 if all(checks.values()) else 1)
