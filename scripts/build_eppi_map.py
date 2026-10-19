"""Build the EPPI-Mapper HTML map from docs/data/downloads/eppi-mapper.json.

The page engine is an HTML file exported by EPPI-Mapper (map-config/eppi-mapper-template.html, from the
sandbox format test). This script replaces only the data and display constants in that file, using the
setup in map-config/eppi-map-settings.json. Local; no network calls. Run after scripts/build.py.

    python scripts/build_eppi_map.py
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = json.loads((ROOT / "docs/data/downloads/eppi-mapper.json").read_text(encoding="utf-8"))
cfg = json.loads((ROOT / "map-config/eppi-map-settings.json").read_text(encoding="utf-8"))
html = (ROOT / "map-config/eppi-mapper-template.html").read_text(encoding="utf-8")
out = ROOT / "docs/map/eppi-mapper/index.html"

sets = {s["AttributeName"]: s for s in src["CodeSets"][0]["Attributes"]["AttributesList"]}
refs = src["References"]
kids = lambda name: sets[name]["Attributes"]["AttributesList"]
errors = []

# Grid: column headers (depth 2), then one row-header group (depth 1)
col, row = sets[cfg["columns"]], sets[cfg["rows"]]
item = lambda a, span, is_col, parent: {"span": span, "isColumn": is_col, "id": a["AttributeId"],
                                        "title": a["AttributeName"], "description": a.get("AttributeDescription", ""),
                                        "setDescription": a.get("AttributeDescription", ""),
                                        "parentId": parent}
ckids, rkids = kids(cfg["columns"]), kids(cfg["rows"])
rows = [[item(col, len(ckids), True, None)], [item(c, 1, True, col["AttributeId"]) for c in ckids]]
for n, r in enumerate(rkids):
    rows.append(([item(row, len(rkids), False, None)] if n == 0 else []) + [item(r, 1, False, row["AttributeId"])])
item_map = {str(x["id"]): x for line in rows for x in line}
csv_data = {"rows": rows, "totalColBreadth": len(ckids), "totalColDepth": 2, "totalRowBreadth": len(rkids),
            "totalRowDepth": 1, "itemMap": item_map}

filters = [{"id": sets[f]["AttributeId"], "label": f, "checked": False,
            "children": [{"id": k["AttributeId"], "label": k["AttributeName"], "checked": False, "children": []}
                         for k in kids(f)]} for f in cfg["filters"]]
ext = []
for name, s in sorted(sets.items()):
    ext.append({"AttributeId": s["AttributeId"], "AttributeName": name, "AttributeDescription": ""})
    ext += [{"AttributeId": k["AttributeId"], "AttributeName": f"{name} - {k['AttributeName']}",
             "AttributeDescription": k.get("AttributeDescription", "")} for k in kids(name)]
segs = kids(cfg["segments"])
if len(segs) != len(cfg["segment_colours"]):
    errors.append("segment colours do not match the number of evidence levels")
segments = [{"attribute": {**{k: s[k] for k in ("AttributeId", "AttributeName", "AttributeDescription", "AttributeType")}},
             "color": c, "isLight": light} for s, c, light in zip(segs, cfg["segment_colours"], cfg["segment_is_light"])]
about = ("<p>Pilot evidence gap map of 30 publicly documented blockchain use cases. Columns are outcome domains and rows are "
         "use-case domains. Bubble colours show the strength of evidence, from 1. Claims only (lightest) to 5. Proven impact "
         "(darkest), the same five steps as the site's evidence spectrum. The protocol and data files use the codes L1 to L5 "
         "for these steps. One record is one use case reporting one outcome, so a use case can appear in several cells. "
         "This is not a representative sample, and the evidence type describes public sources, not project quality.</p>")

valid = {k["AttributeId"] for s in sets.values() for k in kids(s["AttributeName"])}
for r in refs:
    bad = [c["AttributeId"] for c in r["Codes"] if c["AttributeId"] not in valid]
    if bad:
        errors.append(f"{r['ShortTitle']}: unknown codes {bad}")
    if sum(c["AttributeId"] in {s["AttributeId"] for s in segs} for c in r["Codes"]) != 1:
        errors.append(f"{r['ShortTitle']}: needs exactly one evidence level")

J = lambda v: json.dumps(v, ensure_ascii=False).replace("</", "<\\/")
repl = {"csvData": J(csv_data), "filters": J(filters), "externalURLedAttributes": J(ext),
        "segmentAttributes": J(segments), "referenceData": J(refs), "aboutContent": J(about),
        "title": J(cfg["title"]), "topHeaderColors": J(cfg["header_colours"]),
        "sideHeaderColors": J(cfg["header_colours"]), "topHeaderFontColor": J(cfg["header_font_colour"]),
        "sideHeaderFontColor": J(cfg["header_font_colour"]), "dataColor": J(cfg["data_colour"]),
        "showRecordCount": J(cfg["show_record_count"]), "showColumnDescriptions": J(cfg["show_descriptions"]),
        "showRowDescriptions": J(cfg["show_descriptions"])}
for name, value in repl.items():
    pat = re.compile(r"(\n\s*const " + name + r" = )([^\n]*?)(;?\n)")
    html, n = pat.subn(lambda m: m.group(1) + value + m.group(3), html, count=1)
    if n != 1:
        errors.append(f"template constant not found: {name}")
html = html.replace("<title>EPPI Mapper</title>", f"<title>{cfg['title']}</title>", 1)
html = re.sub(r'(<div class="header-title"><span>)[^<]*(</span>)', lambda m: m.group(1) + cfg["title"] + m.group(2), html)
if re.search(r"Mock|MOCK|example\.org", html):
    errors.append("template test data left in output")
if errors:
    sys.exit("EPPI map not built:\n" + "\n".join(errors))
out.write_text(html, encoding="utf-8")
print(f"OK: {out.relative_to(ROOT)}: {len(refs)} records, {len(rkids)} rows x {len(ckids)} columns, {len(segs)} evidence levels")
