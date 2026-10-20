# Technical architecture figure design

The reference supplied during the figure review is a network topology, with recognizable infrastructure symbols, named relationships, domain boundaries and annotations. A serial pipeline with rounded cards communicates a different kind of structure, even when both figures use vector graphics. A game engine is unnecessary for either drawing.

## Reference inspection

The local GOAD image `docs/img/diagram-GOAD_compromission_Path.png` contains embedded draw.io XML identifying draw.io 13.7.3. Its stencils include Citrix directory servers, web servers, databases and laptops, and user/group symbols. The newer `docs/img/diagram-GOADv3-full.png` identifies draw.io Desktop 24.6.4. The thesis scripts `enhance_fig61_topology.py` and `enhance_fig62_attack_paths.py` use Python/Pillow to add topology badges and attack-stage banners. Thus the reference combines a diagram editor and infrastructure symbol libraries with programmatic annotations. This inspection describes the local files, rather than inferring the tool from appearance.

The [official draw.io network-diagram documentation](https://www.drawio.com/docs/diagram-types/network-diagrams/) describes device symbols, groups, labeled connections and networking shape libraries. These are the design elements relevant to the requested style. This public documentation was consulted on 20 October 2026. No GOAD content or third-party icon artwork is incorporated into our paper figure.

## Implemented figure

`scripts/render_technical_architecture.py` explicitly positions the implemented collector, frozen SQLite archive, typed exposure model, SCC analysis, identity ranking and result display. Original reusable SVG geometry in `scripts/technical_icons.py` depicts the services and logical analysis roles. Colored relations distinguish observed maintainer membership, reverse dependency exposure and repository mapping; gray connectors carry observations and derived data. The graph is explicitly illustrative, while population totals and the budget-100 result display are read from saved experiment outputs.

The rendering path is Python-authored SVG → librsvg `rsvg-convert` → vector PDF and 300-dpi PNG. PDF 1.5 matches the manuscript's TeX output. Noto Sans is selected explicitly and the conversion fixes `SOURCE_DATE_EPOCH` for repeatable exports. The separate draw.io exporter creates editable text, individually movable SVG glyphs and native connector cells; the SVG/PDF remain the publication rendering sources. Visual edits in draw.io do not modify the Python source automatically.

Machine symbols represent logical roles in the study, not an experimentally observed inventory of PCs, VPS hosts or deployed services. Workflow presence does not establish execution, and maintainer membership does not independently establish publishing authority. Adding machine types or trust paths beyond the evidence would misdescribe the study.

The statistical figures retain chart marks derived from measured results. Infrastructure symbols belong in the architecture drawing; the quantitative plots communicate coverage, conditional exposure, source partitions and representation sensitivity through axes, curves and bars.

Regeneration commands, dependencies, source mappings and previews are in [the figure gallery](../figures/README.md). The combined figure manifest binds the numerical inputs, all generator modules and current exports by SHA-256.
