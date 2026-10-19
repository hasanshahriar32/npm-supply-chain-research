#!/usr/bin/env python3
"""Check both actual PDF variants against the supplied author record."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

PAPER = Path(__file__).resolve().parents[1]
record = json.loads((PAPER / 'submission_files/authors.json').read_text())
authors = [a['name'] for a in record['authors_in_supplied_order']]
report = {}
for job in ('main', 'main_authors'):
    pdf = PAPER / (job + '.pdf')
    info = subprocess.check_output(['pdfinfo', str(pdf)], text=True)
    pages = int(re.search(r'^Pages:\s+(\d+)', info, re.M).group(1))
    page_info = subprocess.check_output(['pdfinfo', '-f', '1', '-l', str(pages), str(pdf)], text=True)
    sizes = [(float(w), float(h)) for w, h in re.findall(r'^Page\s+\d+ size:\s+([\d.]+) x ([\d.]+) pts', page_info, re.M)]
    fonts = subprocess.check_output(['pdffonts', str(pdf)], text=True).splitlines()[2:]
    fonts = [line for line in fonts if line.strip()]
    text = ' '.join(subprocess.check_output(['pdftotext', str(pdf), '-'], text=True).split())
    metadata = re.search(r'^Author:\s*(.*)$', info, re.M)
    metadata = metadata.group(1).strip() if metadata else ''
    checks = {
        'at_most_six_pages': pages <= 6,
        'under_three_mb': pdf.stat().st_size <= 3_000_000,
        'all_pages_a4': len(sizes) == pages and all(abs(w-595.276) < 1 and abs(h-841.89) < 1 for w,h in sizes),
        'all_fonts_embedded': bool(fonts) and all(line.split()[-5] == 'yes' for line in fonts),
        'no_type_3_fonts': not any(re.search(r'\bType\s+3\b', line) for line in fonts),
    }
    if job == 'main':
        checks.update({'pdf_author_metadata_empty': not metadata,
            'anonymous_author_block': 'Anonymous Authors' in text,
            'recorded_author_names_absent': all(name not in text for name in authors),
            'recorded_institution_absent': record['institution'] not in text})
    else:
        checks.update({'recorded_author_names_present': all(name in text for name in authors),
            'recorded_institution_present': record['institution'] in text,
            'departments_present': all(a['department'] in text for a in record['authors_in_supplied_order']),
            'supplied_order': all(name in text for name in authors) and text.index(authors[0]) < text.index(authors[1]),
            'pdf_author_metadata': all(name in metadata for name in authors)})
    log = PAPER / ('build/' + job + '.log')
    if log.exists():
        content = log.read_text(errors='replace')
        checks['no_overfull_boxes'] = 'Overfull' not in content
        checks['references_resolved'] = not re.search(r'(?:Citation|Reference)\s+.*?undefined|There were undefined references', content)
    report[job] = {'pages': pages, 'file_bytes': pdf.stat().st_size, 'font_count': len(fonts),
        'sha256': hashlib.sha256(pdf.read_bytes()).hexdigest(), 'checks': checks}
(PAPER / 'results/author_versions_validation.json').write_text(json.dumps(report, indent=2)+'\n')
for job, result in report.items():
    passed = all(result['checks'].values())
    print(f"{'PASS' if passed else 'FAIL'} {job}: {result['pages']} pages, {result['file_bytes']:,} bytes, {result['font_count']} fonts")
sys.exit(0 if all(all(r['checks'].values()) for r in report.values()) else 1)
