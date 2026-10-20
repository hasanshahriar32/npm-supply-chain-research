#!/usr/bin/env python3
"""Render the implemented measurement architecture as a native SVG topology.

Original geometric technical icons and explicit orthogonal routes are exported
through librsvg. Device glyphs describe logical service/analysis roles, not an
observed inventory of physical or virtual hosts. No package code or network is used.
"""
from __future__ import annotations

from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import shutil
import subprocess

from technical_icons import icon_use, svg_symbols

PAPER = Path(__file__).resolve().parents[1]
INK = '#263645'
MUTED = '#667581'
BLUE = '#356d93'
TEAL = '#008b91'
GOLD = '#a67529'
DATA = '#8a96a1'
FONT = 'Noto Sans'
EPOCH = str(int(datetime(2026, 10, 20, tzinfo=timezone.utc).timestamp()))


class Drawing:
    def __init__(self):
        self.parts = []

    def add(self, value):
        self.parts.append(value)

    def text(self, x, y, text, size=20, color=INK, weight=400, anchor='start'):
        self.add(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
                 f'fill="{color}" text-anchor="{anchor}">{escape(text)}</text>')

    def icon(self, name, x, y, size=80):
        self.add(icon_use(name, x, y, size))

    def route(self, points, color=DATA, *, dashed=False, width=2.3, marker=True):
        coordinates = ' '.join(f'{x},{y}' for x,y in points)
        dash = ' stroke-dasharray="8 5"' if dashed else ''
        end = f' marker-end="url(#{self.marker(color)})"' if marker else ''
        self.add(f'<polyline points="{coordinates}" fill="none" stroke="{color}" '
                 f'stroke-width="{width}" stroke-linejoin="round"{dash}{end}/>')

    @staticmethod
    def marker(color):
        return 'arrow_' + color.lstrip('#')

    def legend(self, x, y, label, color, dashed=False):
        self.route([(x,y-6),(x+38,y-6)],color,dashed=dashed,width=2.7)
        self.text(x+50,y,label,size=18,color=MUTED)

    def svg(self):
        defs = svg_symbols()
        arrows = []
        for color in (DATA,BLUE,TEAL,GOLD):
            arrows.append(f'<marker id="{self.marker(color)}" viewBox="0 0 12 10" '
                          f'refX="10" refY="5" markerWidth="8" markerHeight="7" orient="auto-start-reverse">'
                          f'<path d="M1 1 L10 5 L1 9" fill="none" stroke="{color}" stroke-width="1.6" '
                          f'stroke-linecap="round" stroke-linejoin="round"/></marker>')
        return ('<svg xmlns="http://www.w3.org/2000/svg" width="7.1in" height="3.35in" '
                'viewBox="0 0 1420 670" role="img" aria-labelledby="title desc">\n'
                '<title id="title">Technical architecture of npm structural measurement</title>\n'
                '<desc id="desc">Public npm, deps.dev and GitHub observations feed a collection workstation and '
                'frozen SQLite archive. An illustrative maintainer-package-repository topology is evaluated '
                'using SCC condensation, endpoint unions and budgeted identity selection.</desc>\n'
                +defs+'\n<defs>'+''.join(arrows)+'</defs>\n'
                f'<g font-family="{FONT},sans-serif">\n'+''.join(self.parts)+'\n</g>\n</svg>\n')


def architecture_svg(data):
    p = data['population']
    primary = data['primary_budget_100']
    g = Drawing()
    # Logical boundaries rather than serial cards: the model and analysis share
    # a local research workspace; public services remain outside that boundary.
    g.add('<rect width="1420" height="670" fill="white"/>')
    g.text(22, 33, 'A  PUBLIC OBSERVATIONS', 23, weight=700)
    g.text(350, 33, 'B  COLLECTION + EVIDENCE', 23, weight=700)
    g.text(845, 33, 'D  EXACT OFFLINE ANALYSIS', 23, weight=700)
    g.add('<path d="M282 54V586" fill="none" stroke="#c8d2da" stroke-width="1.7" stroke-dasharray="6 5"/>')

    # External, explicitly named data resources.
    services = [
        ('registry_server', 98, 'npm registry', 'maintainer records', '/latest + repository URL'),
        ('api_service', 244, 'deps.dev API', 'dependency graph', 'versioned adjacency rows'),
        ('git_repository', 390, 'GitHub GraphQL', 'workflow directory', 'HEAD presence observation'),
    ]
    for icon, y, title, first, second in services:
        g.icon(icon,22,y,82)
        g.text(112,y+28,title,21.5,weight=700)
        g.text(112,y+55,first,17.5,color=MUTED)
        g.text(22,y+105,second,17.5,color=MUTED)
    g.text(22,553,'HTTPS / API observations',18,color=MUTED)

    # Collection fan-in routes. All gray routes are movement of observations,
    # whereas colored routes below are relations in the analytical graph.
    g.route([(104,164),(332,164),(332,154),(370,154)])
    g.route([(104,310),(316,310),(316,178),(370,178)])
    g.route([(104,456),(300,456),(300,202),(370,202)])
    g.icon('workstation',365,96,116)
    g.text(423,235,'Collector',20.5,weight=700,anchor='middle')
    g.text(423,259,'collect_data.py',18,color=MUTED,anchor='middle')
    g.route([(485,159),(582,159)])
    g.text(533,142,'persist',17.5,color=MUTED,anchor='middle')
    g.icon('database',579,98,116)
    g.text(637,235,'SQLite archive',20.5,weight=700,anchor='middle')
    g.text(637,259,'hash-pinned source',17,color=MUTED,anchor='middle')
    g.route([(638,276),(638,303)])
    g.text(628,293,'extract relations',17,color=MUTED,anchor='end')

    # Large analytical topology, with concrete account/package/repository glyphs.
    g.add('<rect x="350" y="305" width="1048" height="288" rx="3" '
          'fill="#fbfcfd" stroke="#cbd6df" stroke-width="1.5" stroke-dasharray="7 5"/>')
    g.text(369,337,'C  TYPED EXPOSURE MODEL',24,weight=700)
    g.text(1378,337,'Illustrative topology',18,color=MUTED,anchor='end')

    # These are representative labels, not identities or accounts drawn from
    # the individual maintainer rankings.
    for icon,x,y,size in [
        ('maintainer',408,363,78),('maintainer',408,484,78),
        ('package',592,365,78),('package',592,486,78),
        ('package',841,365,78),('package',841,486,78),
        ('git_repository',1175,403,104),('workflow',1264,451,60),
    ]:
        g.icon(icon,x,y,size)
    for x,y,label in [(447,458,'identity a'),(447,580,'identity b'),
                      (631,458,'package p₁'),(631,580,'package p₂'),
                      (880,458,'dependent d₁'),(880,580,'dependent d₂')]:
        g.text(x,y,label,18.5,anchor='middle')
    # Observed maintainer membership.
    g.route([(486,402),(590,402)],BLUE,width=2.8)
    g.route([(486,523),(590,523)],BLUE,width=2.8)
    g.text(538,383,'maintains',18,color=BLUE,anchor='middle')
    # Reverse dependency orientation, including shared downstream exposure.
    g.route([(670,402),(840,402)],TEAL,width=2.8)
    g.route([(670,523),(840,523)],TEAL,width=2.8)
    g.route([(704,523),(741,523),(741,421),(839,421)],TEAL,width=2.8)
    g.text(753,383,'reverse dependency',17.5,color=TEAL,anchor='middle')
    # Several package endpoints can map to one repository key.
    g.route([(919,402),(1080,402),(1080,445),(1184,445)],GOLD,dashed=True,width=2.5)
    g.route([(919,523),(1080,523),(1080,478),(1184,478)],GOLD,dashed=True,width=2.5)
    g.text(1043,383,'repository map',18,color=GOLD,anchor='middle')
    g.text(1224,542,'one repository key r',19.5,weight=700,anchor='middle')
    g.text(1224,568,'.github/workflows: presence only',17,color=MUTED,anchor='middle')
    g.text(1023,570,'deduplicate',17.5,color=GOLD,anchor='middle')

    # Topology -> local exact analysis. The gray route carries derived sets,
    # not malicious execution or a claimed CI credential path.
    g.route([(1333,469),(1410,469),(1410,292),(775,292),(775,164),(846,164)])
    g.text(1105,285,'typed graph + repository map',16.5,color=MUTED,anchor='middle')
    g.icon('compute_server',845,101,104)
    g.text(897,234,'SCC engine',20.5,weight=700,anchor='middle')
    g.text(897,258,'DAG + endpoint bitsets',18,color=MUTED,anchor='middle')
    g.route([(953,160),(1029,160)])
    g.text(990,142,'sets',17.5,color=MUTED,anchor='middle')
    g.icon('ranking',1030,101,104)
    g.text(1081,234,'Identity ranking',20.5,weight=700,anchor='middle')
    g.text(1081,258,'5 rules + random',18,color=MUTED,anchor='middle')
    g.route([(1137,160),(1203,160)])
    g.text(1170,142,'evaluate',17,color=MUTED,anchor='middle')
    # A technical results display whose numbers come directly from saved rows.
    g.add('<path d="M1210 104h177v109h-177Z" fill="#eef3f7" stroke="#263645" stroke-width="2.3"/>')
    g.add('<path d="M1220 115h157v85h-157Z" fill="white" stroke="#bacbd8" stroke-width="1.2"/>')
    g.add('<path d="M1280 214v18h37v-18M1258 238h81" fill="none" stroke="#263645" stroke-width="2.3"/>')
    for y,letter,value,color in [
        (139,'C',f"{primary['covered_endpoints']:,}",BLUE),
        (166,'H',f"{100*primary['scenario_exposure_reduction_fraction']:.2f}%",TEAL),
        (193,'P',f"{primary['fully_protected_endpoints']:,}",GOLD),
    ]:
        g.text(1231,y,letter,21,color=color,weight=700)
        g.text(1365,y,value,21,color=color,weight=700,anchor='end')
    g.text(1298,258,'Greedy, k = 100',18,color=MUTED,anchor='middle')

    # Measured corpus totals and relation-encoding legend.
    g.add('<path d="M22 613H1398" stroke="#c4d0d9" stroke-width="1.5"/>')
    g.text(710,637,
        f"{p['identities']:,} identities   ·   {p['packages']:,} graph IDs ({data['context_identifiers']:,} contextual)   ·   "
        f"{p['maintainer_package_relations']:,} maintainer links   ·   {p['unique_package_edges']:,} package-name edges",
        18.5,color=MUTED,anchor='middle')
    g.legend(35,661,'Observed membership',BLUE)
    g.legend(385,661,'Dependency → dependent',TEAL)
    g.legend(820,661,'Repository mapping',GOLD,True)
    g.legend(1175,661,'Data movement',DATA)
    return g.svg()


def render_architecture(data):
    if not shutil.which('rsvg-convert'):
        raise RuntimeError('Install librsvg (rsvg-convert) to render the native SVG architecture.')
    results=json.loads((PAPER/'results/structural_interventions/results.json').read_text())
    data['primary_budget_100']=next(r for r in results['deterministic_curves'] if
        r['endpoint']=='workflow_repositories' and r['method']=='greedy_coverage' and r['budget']==100)
    data['architecture_renderer']={
        'engine':subprocess.check_output(['rsvg-convert','--version'],text=True).strip(),
        'source':'Original SVG geometry and reusable technical glyphs',
        'font_family':FONT,'svg_viewbox':[0,0,1420,670],
        'physical_dimensions_inches':[7.1,3.35],
        'pdf_format':'pdf1.5','preview_dpi':300,'source_date_epoch':int(EPOCH),
        'device_semantics':'Logical service and analysis roles, not measured physical/VPS deployment',
        'graph_semantics':'Illustrative maintainer/package/repository topology; counts and displayed result are empirical',
    }
    out=PAPER/'figures';out.mkdir(exist_ok=True)
    svg=out/'study_system.svg';svg.write_text(architecture_svg(data))
    env=dict(os.environ,SOURCE_DATE_EPOCH=EPOCH)
    subprocess.run(['rsvg-convert','--format=pdf1.5','--output',str(out/'study_system.pdf'),str(svg)],check=True,env=env)
    subprocess.run(['rsvg-convert','--format=png','--width=2130','--output',str(out/'study_system.png'),str(svg)],check=True,env=env)
    from export_drawio import export_drawio
    data['architecture_renderer']['drawio_export']=export_drawio(svg,out/'study_system.drawio')
    data['dimensions_inches']['study_system']=[7.1,3.35]
    return data


if __name__=='__main__':
    data=json.loads((PAPER/'results/system_figure_data.json').read_text())
    render_architecture(data)
    (PAPER/'results/system_figure_data.json').write_text(json.dumps(data,indent=2)+'\n')
    print('Rendered native SVG infrastructure architecture through librsvg.')
