"""Original, code-drawn SVG glyphs for the npm research architecture.

All symbols have a 64 by 64 view box.  They use paths and geometric shapes
only, so PDF export does not require an icon font, external artwork, or a
network connection.  ``svg_symbols()`` belongs inside the root SVG element;
``icon_use()`` places one of its symbols at the requested size.

The server and workstation glyphs denote collection/analysis components.
They do not assert that a particular physical host or deployment was used.
"""

from html import escape


ICON_NAMES = (
    "registry_server",
    "api_service",
    "git_repository",
    "database",
    "workstation",
    "maintainer",
    "package",
    "workflow",
    "compute_server",
    "ranking",
)

# A restrained technical palette.  Every symbol retains a dark silhouette
# and remains intelligible when printed in grayscale or reduced to 24 px.
INK = "#263645"
BLUE = "#356d93"
TEAL = "#008b91"
PALE = "#e9f0f5"
SIDE = "#becfdd"
TOP = "#f6f9fc"


_SYMBOLS = r'''
<symbol id="registry_server" viewBox="0 0 64 64">
  <g stroke="#263645" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <path d="M11 15 18 9h35l-7 6Z" fill="#f6f9fc"/>
    <path d="m46 15 7-6v39l-7 7Z" fill="#becfdd"/>
    <rect x="11" y="15" width="35" height="40" rx="2" fill="#e9f0f5"/>
    <path d="M11 28h35M11 41h35" fill="none"/>
    <path d="M17 21h16M17 34h16M17 47h16" stroke="#356d93" stroke-width="2.2"/>
    <path d="M17 24h11M17 37h11M17 50h11" stroke="#9bb4c6" stroke-width="1.3"/>
    <circle cx="40" cy="21.5" r="1.9" fill="#008b91" stroke="none"/>
    <circle cx="40" cy="34.5" r="1.9" fill="#008b91" stroke="none"/>
    <circle cx="40" cy="47.5" r="1.9" fill="#008b91" stroke="none"/>
  </g>
</symbol>

<symbol id="api_service" viewBox="0 0 64 64">
  <g stroke="#263645" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <path d="M17 36a9 9 0 0 1-1.5-17.9 12 12 0 0 1 23-4.5 9 9 0 0 1 11 5.5A8.5 8.5 0 0 1 48 36Z" fill="#e9f0f5"/>
    <path d="M32 36v8M13 48v-4h38v4" fill="none" stroke="#356d93" stroke-width="2"/>
    <path d="M24 22 20 26l4 4m16-8 4 4-4 4m-5-10-6 12" fill="none" stroke="#008b91" stroke-width="2"/>
    <rect x="8" y="48" width="10" height="9" rx="2" fill="#f6f9fc"/>
    <rect x="27" y="48" width="10" height="9" rx="2" fill="#f6f9fc"/>
    <rect x="46" y="48" width="10" height="9" rx="2" fill="#f6f9fc"/>
    <path d="M11 52.5h4m15 0h4m15 0h4" stroke="#008b91" stroke-width="1.6"/>
  </g>
</symbol>

<symbol id="git_repository" viewBox="0 0 64 64">
  <g stroke="#263645" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <path d="M10 18V12h18l5 6h20v33H10Z" fill="#becfdd"/>
    <path d="M10 23h43l-4 30H7Z" fill="#e9f0f5"/>
    <path d="M7 53h42l4-30" fill="none"/>
    <path d="M25 31v13m0-6c0-5 12-1 12-8" fill="none" stroke="#356d93" stroke-width="2.4"/>
    <circle cx="25" cy="30" r="3" fill="#f6f9fc" stroke="#008b91" stroke-width="2"/>
    <circle cx="25" cy="45" r="3" fill="#f6f9fc" stroke="#008b91" stroke-width="2"/>
    <circle cx="37" cy="29" r="3" fill="#f6f9fc" stroke="#008b91" stroke-width="2"/>
  </g>
</symbol>

<symbol id="database" viewBox="0 0 64 64">
  <g stroke="#263645" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <path d="M11 15v34c0 5 9.4 9 21 9s21-4 21-9V15Z" fill="#d9e5ee"/>
    <path d="M32 23v35c11.6 0 21-4 21-9V15Z" fill="#becfdd" stroke="none"/>
    <ellipse cx="32" cy="15" rx="21" ry="8" fill="#f6f9fc"/>
    <path d="M11 27c0 5 9.4 9 21 9s21-4 21-9M11 38c0 5 9.4 9 21 9s21-4 21-9M11 49c0 5 9.4 9 21 9s21-4 21-9" fill="none"/>
    <path d="M18 28.5c3 1.3 7.5 2.2 12 2.3M18 39.5c3 1.3 7.5 2.2 12 2.3M18 50.5c3 1.3 7.5 2.2 12 2.3" stroke="#008b91" stroke-width="1.9"/>
  </g>
</symbol>

<symbol id="workstation" viewBox="0 0 64 64">
  <g stroke="#263645" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <path d="m9 10 4-3h43v32l-4 4H9Z" fill="#becfdd"/>
    <rect x="7" y="10" width="45" height="33" rx="2" fill="#e9f0f5"/>
    <rect x="11" y="14" width="37" height="23" rx=".6" fill="#f6f9fc"/>
    <path d="m22 20-5 5 5 5m15-10 5 5-5 5m-6-12-5 14" fill="none" stroke="#008b91" stroke-width="2"/>
    <path d="M25 43v7h10v-7M20 50h20" fill="#becfdd"/>
    <path d="M13 53h38l6 6H7Z" fill="#e9f0f5"/>
    <path d="M18 55.8h27M22 58h20" stroke="#7892a7" stroke-width="1.2"/>
  </g>
</symbol>

<symbol id="maintainer" viewBox="0 0 64 64">
  <g stroke="#263645" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <path d="M22 15c0-5.7 4.5-10 10-10s10 4.3 10 10v6c0 6-4.5 11-10 11s-10-5-10-11Z" fill="#e9f0f5"/>
    <path d="M22 16c0-7 4.5-11 10-11s10 4 10 11c-5 .2-8.1-1.9-10-5-2.2 3.1-5.5 4.8-10 5Z" fill="#becfdd"/>
    <path d="M27 31v5l5 5 5-5v-5M12 58v-8c0-7 6.5-11 15-14l5 5 5-5c8.5 3 15 7 15 14v8Z" fill="#d9e5ee"/>
    <path d="m27 36-6 3 7 10 4-8 4 8 7-10-6-3" fill="#f6f9fc"/>
    <path d="M21 50v8M43 50v8" stroke="#7892a7"/>
    <rect x="39" y="48" width="7" height="5" rx=".6" fill="#008b91" stroke="none"/>
  </g>
</symbol>

<symbol id="package" viewBox="0 0 64 64">
  <g stroke="#263645" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <path d="m8 20 24-13 24 13-24 13Z" fill="#f6f9fc"/>
    <path d="M8 20v26l24 13V33Z" fill="#d9e5ee"/>
    <path d="M32 33v26l24-13V20Z" fill="#becfdd"/>
    <path d="m19 14 24 13v10l6-3V24L25 11Z" fill="#68b1b6" stroke-width="1.3"/>
    <path d="m14 37 9 5v8l-9-5Z" fill="#f6f9fc" stroke="#7892a7" stroke-width="1.1"/>
    <path d="m16 41 5 3m-5 0 3 1.8" fill="none" stroke="#7892a7" stroke-width="1.1"/>
  </g>
</symbol>

<symbol id="workflow" viewBox="0 0 64 64">
  <g stroke="#263645" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <path d="M13 6h27l12 12v40H13Z" fill="#f6f9fc"/>
    <path d="M40 6v12h12" fill="#becfdd"/>
    <path d="M23 31v8h19m-19 0v10m19-10v10" fill="none" stroke="#356d93" stroke-width="1.8"/>
    <rect x="18" y="22" width="10" height="9" rx="1.4" fill="#d9e5ee"/>
    <rect x="18" y="46" width="10" height="8" rx="1.4" fill="#d9e5ee"/>
    <rect x="37" y="46" width="10" height="8" rx="1.4" fill="#68b1b6"/>
    <path d="m21 26 1.5 1.5 3-3M40 50h4" fill="none" stroke="#008b91" stroke-width="1.5"/>
    <path d="M32 24h11M32 28h8" stroke="#9bb4c6" stroke-width="1.3"/>
  </g>
</symbol>

<symbol id="compute_server" viewBox="0 0 64 64">
  <g stroke="#263645" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <path d="m15 11 6-5h32l-6 5Z" fill="#f6f9fc"/>
    <path d="m47 11 6-5v34l-6 5Z" fill="#becfdd"/>
    <rect x="15" y="11" width="32" height="34" rx="1.8" fill="#e9f0f5"/>
    <path d="M15 23h32M15 34h32" fill="none"/>
    <path d="M21 17h13M21 28.5h13M21 39.5h13" stroke="#356d93" stroke-width="2"/>
    <circle cx="40.5" cy="17" r="1.7" fill="#008b91" stroke="none"/>
    <circle cx="40.5" cy="28.5" r="1.7" fill="#008b91" stroke="none"/>
    <circle cx="40.5" cy="39.5" r="1.7" fill="#008b91" stroke="none"/>
    <path d="M31 45v7H13m18 0h18" fill="none" stroke="#356d93"/>
    <circle cx="13" cy="52" r="3.4" fill="#f6f9fc"/>
    <circle cx="31" cy="55" r="3.4" fill="#68b1b6"/>
    <circle cx="49" cy="52" r="3.4" fill="#f6f9fc"/>
  </g>
</symbol>

<symbol id="ranking" viewBox="0 0 64 64">
  <g stroke="#263645" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <path d="m16 10 4-3h31v47l-4 4H16Z" fill="#becfdd"/>
    <rect x="12" y="10" width="35" height="48" rx="2" fill="#f6f9fc"/>
    <path d="M23 10V7a6 6 0 0 1 12 0v3h4v7H19v-7Z" fill="#d9e5ee"/>
    <circle cx="29" cy="7" r="1.7" fill="#f6f9fc"/>
    <circle cx="20" cy="27" r="2.1" fill="#008b91" stroke="none"/>
    <circle cx="20" cy="38" r="2.1" fill="#356d93" stroke="none"/>
    <circle cx="20" cy="49" r="2.1" fill="#7892a7" stroke="none"/>
    <path d="M26 25h15v4H26Z" fill="#008b91" stroke="none"/>
    <path d="M26 36h11v4H26Z" fill="#356d93" stroke="none"/>
    <path d="M26 47h7v4h-7Z" fill="#7892a7" stroke="none"/>
  </g>
</symbol>
'''


def svg_symbols() -> str:
    """Return self-contained SVG definitions for all ten technical glyphs."""
    return "<defs>\n" + _SYMBOLS.strip() + "\n</defs>"


def icon_use(name: str, x: float, y: float, width: float = 40,
             height: float | None = None, *, opacity: float = 1.0) -> str:
    """Place a glyph using a standard SVG ``use`` element.

    ``name`` must be in :data:`ICON_NAMES`; width and height are in the root
    SVG coordinate system.  A square size is used when height is omitted.
    Both modern ``href`` and legacy ``xlink:href`` are unnecessary together;
    modern librsvg and browser renderers support ``href`` directly.
    """
    if name not in ICON_NAMES:
        raise ValueError(f"Unknown technical icon: {name!r}")
    height = width if height is None else height
    if width <= 0 or height <= 0:
        raise ValueError("Icon width and height must be positive")
    if not 0 <= opacity <= 1:
        raise ValueError("Icon opacity must be between zero and one")
    return (
        f'<use href="#{escape(name, quote=True)}" x="{x:g}" y="{y:g}" '
        f'width="{width:g}" height="{height:g}" opacity="{opacity:g}"/>'
    )
