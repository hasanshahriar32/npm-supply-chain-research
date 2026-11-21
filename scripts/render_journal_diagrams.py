"""Render editable one-column diagrams for the current journal manuscript."""
from hashlib import sha256
from html import escape
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
JOURNAL = ROOT / "manuscript_q1"
ART = ROOT / "manuscript/scripts"
sys.path.insert(0, str(ART))
from export_drawio import export_drawio
from technical_icons import icon_use, svg_symbols
RESULT = ROOT / "research/consumer_holdout/runs/selfhosted-v1/results.json"
W = 248
INK = "#1e3241"
TEAL = "#126567"
BLUE = "#2a577e"
OCHRE = "#8a510e"
LIGHT = "#eef4f8"
LINE = "#c6d2db"
GRAY = "#526576"


class Diagram:
    def __init__(self, title, desc, height, *, illustrated=False):
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}pt" height="{height}pt" '
            f'viewBox="0 0 {W} {height}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title>',
            f'<desc id="desc">{escape(desc)}</desc>',
            '<defs><pattern id="unresolved" width="5" height="5" patternUnits="userSpaceOnUse">'
            '<rect width="5" height="5" fill="#e9eef2"/><path d="M-1 1 1-1 M0 5 5 0 M4 6 6 4" '
            'stroke="#9aaebd" stroke-width=".75"/></pattern></defs>',
        ]
        if illustrated:
            self.parts.append(svg_symbols())
            markers = []
            for color in (TEAL, BLUE, GRAY, OCHRE):
                markers.append(
                    f'<marker id="arrow-{color[1:]}" viewBox="0 0 8 8" refX="7" refY="4" '
                    f'markerWidth="6" markerHeight="6" orient="auto">'
                    f'<path d="M1 1 7 4 1 7" fill="none" stroke="{color}" stroke-width="1.2" '
                    'stroke-linecap="round" stroke-linejoin="round"/></marker>'
                )
            self.parts.append("<defs>" + "".join(markers) + "</defs>")

    def icon(self, name, x, y, size):
        self.parts.append(icon_use(name, x-size/2, y-size/2, size))

    def label(self, x, y, label, *, size=9, color=INK, weight=400, anchor="start"):
        self.parts.append(
            f'<text x="{x}" y="{y}" fill="{color}" font-family="Noto Sans, sans-serif" '
            f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(label)}</text>'
        )

    def rect(self, x, y, w, h, fill, stroke="none", radius=0, *, dashed=False):
        dash = ' stroke-dasharray="3 2"' if dashed else ""
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" '
                          f'stroke="{stroke}" rx="{radius}"{dash}/>')

    def route(self, coords, *, color=GRAY, dashed=False, arrow=False):
        points = " ".join(f"{x},{y}" for x, y in coords)
        dash = ' stroke-dasharray="3 2"' if dashed else ""
        marker = f' marker-end="url(#arrow-{color[1:]})"' if arrow else ""
        self.parts.append(f'<polyline points="{points}" fill="none" stroke="{color}" '
                          f'stroke-width="1.15" stroke-linejoin="round"{dash}{marker}/>')

    def finish(self):
        return "\n".join([*self.parts, "</svg>", ""])


def packages():
    d = Diagram("Version splicing", "The name graph joins p to r through intermediate package d. "
                "The illustrated exact-version paths end at different versions of d, "
                "so their reverse reach does not compose.", 153, illustrated=True)
    d.rect(1, 1, 246, 64, "#fbfcfd", LINE, 2, dashed=True)
    d.rect(1, 72, 246, 80, "#fbfcfd", LINE, 2, dashed=True)
    d.label(9, 14, "(a) Package-name graph", size=9.5, weight=700)
    d.label(9, 85, "(b) Exact-version graph", size=9.5, weight=700)
    d.rect(106, 20, 36, 29, "#fff2dc", radius=4)

    def package(x, y, label, color):
        d.icon("package", x, y, 28)
        d.label(x, y+24, label, size=10, color=color, weight=700, anchor="middle")

    for x, label in ((34, "p"), (124, "d"), (214, "r")):
        package(x, 35, label, OCHRE)
    d.route([(47, 35), (109, 35)], color=OCHRE, dashed=True, arrow=True)
    d.route([(138, 35), (200, 35)], color=OCHRE, dashed=True, arrow=True)

    for x, label in ((29, "p@1"), (88, "d@1"), (160, "d@2"), (219, "r@1")):
        package(x, 108, label, TEAL)
    d.route([(42, 108), (74, 108)], color=TEAL, arrow=True)
    d.route([(173, 108), (205, 108)], color=TEAL, arrow=True)
    d.route([(102, 108), (116, 108)], color=GRAY, dashed=True)
    d.route([(132, 108), (146, 108)], color=GRAY, dashed=True)
    d.route([(121, 105), (127, 111)], color=OCHRE)
    d.route([(121, 111), (127, 105)], color=OCHRE)
    d.label(124, 145, "Version mismatch", color=OCHRE, size=8.6, anchor="middle")
    return d.finish()


def methodology():
    d = Diagram("Reach analysis and checks", "The observed graph is condensed into exact reach sets. "
                "These sets supply parallel portfolio scoring and independent verification branches.",
                153, illustrated=True)
    d.rect(1, 1, 246, 65, "#fbfcfd", LINE, 2, dashed=True)
    d.icon("maintainer", 24, 24, 20)
    d.icon("package", 43, 24, 20)
    d.route([(30, 23), (35, 23)], color=BLUE, arrow=True)
    d.icon("compute_server", 122, 25, 32)
    d.icon("database", 208, 25, 34)
    d.label(39, 51, "Observed graph", size=9.1, weight=700, anchor="middle")
    d.label(122, 51, "SCC engine", size=9.1, weight=700, anchor="middle")
    d.label(208, 51, "Reach sets", size=9.1, weight=700, anchor="middle")
    d.label(122, 62, "Condensed DAG", size=8.2, color=GRAY, anchor="middle")
    d.label(208, 62, "Exact bitsets", size=8.2, color=GRAY, anchor="middle")
    d.route([(54, 27), (106, 27)], color=GRAY, arrow=True)
    d.route([(137, 27), (192, 27)], color=GRAY, arrow=True)

    d.rect(1, 87, 118, 65, "#f6f9fc", LINE, 2, dashed=True)
    d.rect(129, 87, 118, 65, "#f6f9fc", LINE, 2, dashed=True)
    d.route([(225, 25), (236, 25), (236, 78), (60, 78)], color=GRAY)
    d.route([(60, 78), (60, 93)], color=BLUE, arrow=True)
    d.route([(188, 78), (188, 93)], color=TEAL, arrow=True)
    d.icon("ranking", 60, 108, 29)
    d.icon("workflow", 188, 108, 29)
    d.label(60, 134, "Score portfolios", size=9.3, color=BLUE, weight=700, anchor="middle")
    d.label(188, 134, "Verify reach sets", size=9.3, color=TEAL, weight=700, anchor="middle")
    d.label(60, 146, "Coverage · pair mass · P", size=8.1, anchor="middle")
    d.label(188, 146, "Traversal · incidence · hashes", size=8.1, anchor="middle")
    return d.finish()


def holdout():
    result = json.loads(RESULT.read_text())
    primary = result["comparisons"]["version_1"]
    cells = primary["documented_cells"]
    n = result["denominator"]
    # This design labels the specific primary result. Any future shape needs
    # new labels before generating publication graphics.
    resolved = [row["feasible"][0] for row in primary["projects"] if len(row["feasible"]) == 1]
    both, neither = resolved.count([1, 1]), resolved.count([0, 0])
    assert cells["01"] == cells["10"] == 0 and both == cells["11"] and len(resolved) == both + neither
    unknown = n - both - neither
    low, high = primary["complete_reference_turnover_bounds"]
    assert low == 0 and abs(high - unknown / n) < 1e-12
    d = Diagram(f"Evidence for paired coverage on {n} projects",
                f"{both} covered by both, {neither} covered by neither and {unknown} unresolved. "
                f"The full-reference turnover bound ranges from 0 to {high:.1%}.", 142)
    left, width = 6, 236
    d.label(left, 12, f"(a) Paired coverage status ({n} projects)", size=9.8, weight=700)
    x = left
    for value, color in [(both, TEAL), (neither, "#657786"), (unknown, "url(#unresolved)")]:
        span = width * value / n
        d.rect(x, 22, span, 14, color)
        x += span
    d.rect(left, 22, width, 14, "none", LINE)
    d.rect(6, 45, 8, 8, TEAL)
    d.label(18, 52, f"Both  {both}", size=8.9)
    d.rect(72, 45, 8, 8, "#657786")
    d.label(84, 52, f"Neither  {neither}", size=8.9)
    d.rect(153, 45, 8, 8, "url(#unresolved)", LINE)
    d.label(165, 52, f"Unresolved  {unknown}", size=8.9)
    d.route([(6, 64), (242, 64)], color=LINE)
    d.label(6, 80, "(b) Possible coverage reassignment", size=9.8, weight=700)
    x0, x1, y = 10, 237, 109
    d.route([(x0, y), (x1, y)], color=LINE)
    for value in (0, .25, .50, .75, 1):
        x = x0 + (x1-x0)*value
        d.route([(x, y + 4), (x, y + 8)], color=GRAY)
        d.label(x, y + 20, f"{value:.0%}", size=8, color=GRAY, anchor="middle")
    end = x0 + (x1-x0)*high
    d.rect(x0, y - 3, end-x0, 6, BLUE, radius=1)
    d.route([(end, y-8), (end, y+4)], color=BLUE)
    d.label(end, y - 11, f"{high:.1%}", size=9.1, color=BLUE, weight=700, anchor="middle")
    return d.finish()


ILLUSTRATED = {"graph_semantics": packages, "study_methodology": methodology}
DESIGNS = {**ILLUSTRATED, "consumer_holdout_evidence": holdout}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def render():
    out = JOURNAL / "figures"
    record = {"renderer_sha256": digest(Path(__file__)),
              "holdout_data_sha256": digest(RESULT), "figures": {}, "drawio": {},
              "shared_sources_sha256": {
                  str(source.relative_to(ROOT)): digest(source)
                  for source in (ART / "technical_icons.py", ART / "export_drawio.py")
              }}
    for stem, draw in DESIGNS.items():
        svg = out / f"{stem}.svg"
        svg.write_text(draw())
        for ext in ("pdf", "png"):
            subprocess.run(["rsvg-convert", "--format=pdf1.5" if ext == "pdf" else "--format=png", "--dpi-x=240", "--dpi-y=240",
                            "--output", str(out / f"{stem}.{ext}"), str(svg)], check=True,
                           env={**os.environ, "SOURCE_DATE_EPOCH": "1795219200"})
        record["figures"][stem] = {ext: digest(out / f"{stem}.{ext}") for ext in ("svg", "pdf", "png")}
        if stem in ILLUSTRATED:
            record["drawio"][stem] = export_drawio(svg, out / f"{stem}.drawio")
    original = JOURNAL / "tables/q1_heterogeneous_weights_table.tex"
    table = original.read_text()
    table = table.replace(r"\begin{table*}[t]", r"\begin{table}[!t]").replace(r"\end{table*}", r"\end{table}")
    table = table.replace(r"\begin{tabular}", r"\setlength{\tabcolsep}{2.2pt}" + "\n" + r"\begin{tabular}")
    table = table.replace(
        r"Selection & C & H (\%) & Account-sole (\%) & Log (\%) & Package-sole (\%) & P",
        r"Selection & $C$ & \shortstack{$H$\\(\%)} & \shortstack{Acct. sole\\(\%)}"
        r" & \shortstack{Log\\(\%)} & \shortstack{Pkg. sole\\(\%)} & $P$"
    )
    for long, short in [("Log-portfolio aware", "Log aware"),
                        ("Package-sole aware", "Pkg. sole aware"),
                        ("Account-sole aware", "Acct. sole aware")]:
        table = table.replace(long, short)
    table = table.replace("% Generated by scripts/reconcile_full_manuscript.py",
                          "% Compact layout generated by scripts/render_journal_diagrams.py")
    compact = JOURNAL / "tables/q1_heterogeneous_weights_compact.tex"
    compact.write_text(table)
    record["appendix_table"] = {"source_sha256": digest(original), "output_sha256": digest(compact)}
    (JOURNAL / "results/journal_diagrams.json").write_text(json.dumps(record, indent=2) + "\n")
    return record


if __name__ == "__main__":
    render()
