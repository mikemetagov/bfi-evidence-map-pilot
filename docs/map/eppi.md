---
hide:
  - toc
---

# EPPI-Mapper version

The same pilot data as the [interactive map](index.md), in the Campbell and 3ie style format made by [EPPI-Mapper](https://eppi.ioe.ac.uk/cms/er4/EPPI-Mapper). Columns are outcome domains and rows are use-case domains. Bubble colours show the strength of evidence, using the same five steps and colours as the [evidence spectrum](index.md#the-evidence-spectrum): 1. Claims only, 2. Operational data, 3. Outcomes, no comparison, 4. Outcomes with comparison and 5. Proven impact. No pilot case reached steps 4 or 5.

Hover over a bubble to see how many records it holds, and click it to list them with their source links. Use **Filters** to narrow by strength of evidence, portfolio, traced status, blockchain added value or region. A record is one use case reporting one outcome, so a use case can appear in several cells (113 records from 27 of the 30 cases; three cases had no outcome coded).

<iframe class="eppi-frame" src="eppi-mapper/index.html" title="EPPI-Mapper evidence gap map"></iframe>

??? note "Technical notes"
    **Codes.** The protocol, codebook and data files use the codes L1 to L5 for the five steps. In the EPPI-Mapper data each step's description gives its code, for example "Protocol code L2".

    **How the page is built.** `scripts/build.py` writes [`eppi-mapper.json`](../data/downloads/eppi-mapper.json) from the published data. `scripts/build_eppi_map.py` then fills an HTML map exported by EPPI-Mapper v2.4.5 with that data, using the saved setup in `map-config/eppi-map-settings.json` (rows, columns, colours and filters). Both run on every update, so this page always matches the interactive map.

    **Filter gaps.** As on the interactive map, minor fields where the two coders differed are blank for the pilot, so filtering on region leaves some cases out.

    **Rebuilding in EPPI-Mapper.** To check or restyle the map in EPPI-Mapper itself, load `eppi-mapper.json` at the [EPPI-Mapper site](https://eppimapper.digitalsolutionfoundry.co.za/) with the settings above, download the HTML and compare it with this page.
