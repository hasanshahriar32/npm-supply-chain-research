"""Prepare journal vector artwork without changing the frozen conference figures.

Only presentation changes are made: remove duplicated figure-level headings,
replace internal task notes, add line-pattern distinctions and darken text.
The original vector/PDF/PNG inputs and hashes are retained for verification.
"""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
Q = ROOT / 'manuscript_q1'
FIG = Q / 'figures'
INPUT = FIG / 'editorial_inputs'
NS = '{http://www.w3.org/2000/svg}'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    INPUT.mkdir(exist_ok=True)
    manifest = json.loads((Q / 'config/revision_artifact_manifest.json').read_text())
    remove = {
        'ANALYSIS AND VALIDATION WORKFLOW',
        'WHY VERSION CONTINUITY CHANGES REACH',
        'Covered does not mean all sources selected',
        'Budget 100 · all three segments labeled by count',
        'Representation sensitivity at budget 100',
        'Illustrative reverse-reach example; not a measured installation.',
        'Gray: name projection    Teal: version continuity',
    }
    edits = {
        'A  PUBLIC OBSERVATIONS': '(a) PUBLIC OBSERVATIONS',
        'B  COLLECTION + EVIDENCE': '(b) COLLECTION + EVIDENCE',
        'C  TYPED EXPOSURE MODEL': '(c) TYPED EXPOSURE MODEL',
        'D  EXACT OFFLINE ANALYSIS': '(d) EXACT OFFLINE ANALYSIS',
        'Graph identifiers': '(a) Graph identifiers',
        'Workflow endpoint map': '(b) Workflow endpoint map',
        'Frozen metadata pilot': '(c) Metadata pilot',
        'C: repositories': '(a) C: repositories',
        'H: evaluation pair mass (%)': '(b) H: pair mass (%)',
        'P: all-source exclusion': '(c) P: all-source exclusion',
        'Outcomes still pending': 'No execution evidence',
        'All 100 outcomes pending.': '',
        'Hybrid + threshold counts': 'Model assumptions',
    }
    patterns = {'#00858b': '5,2', '#007f83': '5,2', '#285d85': '1.5,1.5',
                '#28618a': '1.5,1.5', '#b57720': '6,2,1,2', '#a56b16': '6,2,1,2',
                '#8660a8': '3,1,1,1', '#8054a3': '3,1,1,1'}
    record = {'renderer_sha256': sha(Path(__file__)), 'inputs': {}, 'figures': {}}
    for pdf in manifest['active_figures']:
        stem = Path(pdf).stem
        for ext in ('svg', 'pdf', 'png'):
            source = INPUT / f'{stem}.{ext}'
            if not source.exists():
                shutil.copy2(FIG / source.name, source)
        record['inputs'][stem] = {ext: sha(INPUT / f'{stem}.{ext}') for ext in ('svg', 'pdf', 'png')}
        tree = ET.parse(INPUT / f'{stem}.svg')
        root = tree.getroot()
        parents = {child: parent for parent in root.iter() for child in parent}
        for element in list(root.iter(NS + 'text')):
            text = ''.join(element.itertext()).strip()
            if text in remove or text in edits and not edits[text]:
                parents[element].remove(element)
                continue
            if text in edits:
                element.text = edits[text]
                for child in list(element):
                    element.remove(child)
            # Colored diagram text remains legible on the pale/white backgrounds.
            if element.get('fill', '').lower() not in ('', '#ffffff', 'white'):
                element.set('fill', '#213547')
            style = element.get('style', '')
            color = re.search(r'fill:\s*(#[0-9a-fA-F]{6})', style)
            if color and color[1].lower() not in ('#ffffff', '#000000'):
                element.set('style', style[:color.start(1)] + '#213547' + style[color.end(1):])
        # Line patterns distinguish curves without relying only on color.
        for group in root.iter(NS + 'g'):
            if not group.get('id', '').startswith('line2d_'):
                continue
            for path in group.findall(NS + 'path'):
                style = path.get('style', '')
                color = re.search(r'stroke:\s*(#[0-9a-fA-F]{6})', style)
                if color and color[1].lower() in patterns and 'stroke-dasharray' not in style:
                    path.set('style', style + '; stroke-dasharray: ' + patterns[color[1].lower()])
        svg = FIG / f'{stem}.svg'
        tree.write(svg, encoding='utf-8', xml_declaration=True)
        svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines()) + '\n')
        subprocess.run(['rsvg-convert', '--format=pdf', '--output', str(FIG / pdf), str(svg)], check=True)
        subprocess.run(['rsvg-convert', '--format=png', '--dpi-x=240', '--dpi-y=240',
                        '--output', str(FIG / f'{stem}.png'), str(svg)], check=True)
        record['figures'][stem] = {ext: sha(FIG / f'{stem}.{ext}') for ext in ('svg', 'pdf', 'png')}
    out = Q / 'results/emse_figure_presentation.json'
    out.write_text(json.dumps(record, indent=2) + '\n')
    print(f'Prepared {len(record["figures"])} journal figures; original inputs retained.')


if __name__ == '__main__':
    main()
