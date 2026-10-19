"""Check the pilot data and build every generated file the website reads.

Run from the repository root:  python scripts/build.py
GitHub Actions and Cloudflare run this before building the site. If the data
break a rule, the build stops and lists each problem with its line number.

You edit:
  data/cases.csv            one row per use case (case-level codes)
  data/coding.csv           one row per use case x outcome domain (evidence level)
  data/codebook.csv         allowed values, labels, order, definitions (change only at approved codebook versions)
  data/outputs_register.csv status and file location for outputs O1-O19

Generated (do not edit by hand):
  docs/map/map-data.json
  docs/outputs/index.md and docs/outputs/<section>/index.md
  docs/data/downloads/*
"""
import csv, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA, DOCS = ROOT / "data", ROOT / "docs"
errors, notes = [], []

CASE_FIELDS = ["case_id", "lineage_id", "name", "primary_portfolio", "all_funders", "country", "region", "year_launched",
               "use_case_domain", "blockchain_functions", "implementation_model", "deployment_status_stated",
               "deployment_status_traced", "status_confidence", "blockchain_added_value", "case_url", "summary",
               "codebook_version"]
CODING_FIELDS = ["case_id", "outcome_domain", "evidence_level", "key_result", "quote", "source_id", "evidence_url",
                 "evidence_producer", "confidence"]
REGISTER_FIELDS = ["id", "output", "contents", "gate", "folder", "status", "file", "updated"]
# field -> codebook dimension it must match (blank values allowed only where listed in OPTIONAL)
CASE_CODED = {"primary_portfolio": "primary_portfolio", "use_case_domain": "use_case_domain",
              "deployment_status_stated": "deployment_status", "deployment_status_traced": "deployment_status",
              "status_confidence": "confidence", "blockchain_added_value": "blockchain_added_value"}
CODING_CODED = {"outcome_domain": "outcome_domain", "evidence_level": "evidence_level",
                "evidence_producer": "evidence_producer", "confidence": "confidence"}
OPTIONAL = {"deployment_status_stated", "status_confidence", "evidence_producer", "confidence"}
SECTIONS = ["00_Admin_and_Approvals", "01_Design", "02_Sampling", "03_Collection", "04_Evidence_Packets",
            "05_Codebook", "06_Prompts_and_Models", "07_Coding_Raw", "08_Agreement_and_Adjudication",
            "09_Final_Dataset", "10_Analysis_and_Visuals", "11_Reports", "12_Full_Scope"]
MAX_LEVELS = 6  # EPPI-Mapper limit on bubble colours


def read(name, fields):
    with open(DATA / name, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        missing = [c for c in fields if c not in (reader.fieldnames or [])]
        if missing:
            errors.append(f"{name}: missing columns {missing}")
        rows = []
        for n, r in enumerate(reader, start=2):
            if None in r:
                errors.append(f"{name} line {n}: too many commas; put text containing commas in double quotes")
            rows.append({k: (v or "").strip() for k, v in r.items() if k is not None})
    return rows


cases = read("cases.csv", CASE_FIELDS)
coding = read("coding.csv", CODING_FIELDS)
cb_rows = read("codebook.csv", ["dimension", "value", "label", "order", "definition"])
register = read("outputs_register.csv", REGISTER_FIELDS)

codebook = {}
for r in sorted(cb_rows, key=lambda r: (r["dimension"], int(r["order"] or 0))):
    codebook.setdefault(r["dimension"], []).append({"value": r["value"], "label": r["label"] or r["value"],
                                                    "definition": r["definition"]})
allowed = {d: {v["value"] for v in vals} for d, vals in codebook.items()}
label = {(d, v["value"]): v["label"] for d, vals in codebook.items() for v in vals}
definition = {(d, v["value"]): v["definition"] for d, vals in codebook.items() for v in vals}

# ---- checks ----------------------------------------------------------------
ids = [c["case_id"] for c in cases]
for i in sorted({i for i in ids if ids.count(i) > 1}):
    errors.append(f"cases.csv: case_id {i} appears more than once")
case_by_id = {c["case_id"]: c for c in cases}
for n, c in enumerate(cases, start=2):
    if not c["case_id"]:
        errors.append(f"cases.csv line {n}: case_id is blank")
    for field, dim in CASE_CODED.items():
        v = c.get(field, "")
        if not v and field in OPTIONAL:
            continue
        if v not in allowed.get(dim, set()):
            errors.append(f"cases.csv line {n}: {field} '{v}' is not in the codebook ({dim})")
    if c.get("case_url") and not c["case_url"].startswith("http"):
        errors.append(f"cases.csv line {n}: case_url must be a full link starting with http")
pairs = set()
for n, r in enumerate(coding, start=2):
    if r["case_id"] not in case_by_id:
        errors.append(f"coding.csv line {n}: case_id {r['case_id']} is not in cases.csv")
    for field, dim in CODING_CODED.items():
        v = r.get(field, "")
        if not v and field in OPTIONAL:
            continue
        if v not in allowed.get(dim, set()):
            errors.append(f"coding.csv line {n}: {field} '{v}' is not in the codebook ({dim})")
    if (r["case_id"], r["outcome_domain"]) in pairs:
        errors.append(f"coding.csv line {n}: {r['case_id']} is coded twice on outcome {r['outcome_domain']}")
    pairs.add((r["case_id"], r["outcome_domain"]))
    if r.get("evidence_url") and not r["evidence_url"].startswith("http"):
        errors.append(f"coding.csv line {n}: evidence_url must be a full link starting with http")
if len(codebook.get("evidence_level", [])) > MAX_LEVELS:
    errors.append("codebook.csv: EPPI-Mapper allows at most 6 evidence levels")
for n, r in enumerate(register, start=2):
    if r["folder"] not in SECTIONS:
        errors.append(f"outputs_register.csv line {n}: folder '{r['folder']}' is not one of the 13 sections")
    if r["file"] and not (DOCS / r["file"]).exists():
        errors.append(f"outputs_register.csv line {n}: file docs/{r['file']} does not exist")
uncoded = sorted(set(ids) - {r["case_id"] for r in coding})
if uncoded:
    notes.append(f"cases with no outcome coding yet: {', '.join(uncoded)}")

if errors:
    print("BUILD STOPPED - fix these problems:\n  " + "\n  ".join(errors))
    sys.exit(1)

# ---- map data ---------------------------------------------------------------
config = {
    "row": {"field": "use_case_domain", "dim": "use_case_domain", "title": "Use-case domain"},
    "col": {"field": "outcome_domain", "dim": "outcome_domain", "title": "Outcome domain"},
    "grade": {"field": "evidence_level", "dim": "evidence_level", "title": "Evidence level"},
    "filters": [
        {"field": "primary_portfolio", "dim": "primary_portfolio", "title": "Portfolio"},
        {"field": "region", "dim": None, "title": "Region"},
        {"field": "deployment_status_traced", "dim": "deployment_status", "title": "Traced status"},
        {"field": "blockchain_added_value", "dim": "blockchain_added_value", "title": "Blockchain added value"},
    ],
}
(DOCS / "map").mkdir(parents=True, exist_ok=True)
json.dump({"config": config, "cases": cases, "records": coding, "codebook": codebook},
          open(DOCS / "map" / "map-data.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---- outputs pages ----------------------------------------------------------
def link(r, from_dir):
    """Link to a file given relative to docs/, from outputs/ ('top') or outputs/<section>/ ('section')."""
    if not r["file"]:
        return "Not yet added"
    prefix = "../../" if from_dir == "section" else "../"
    return f"[Open]({prefix}{r['file']})"

out_dir = DOCS / "outputs"
for old in out_dir.glob("*/index.md"):
    old.unlink()
lines = ["# Outputs", "",
         "Outputs O1 to O19 from the pilot design report, grouped by the same 13 sections as the restricted project folder. "
         "Only O1 (the protocol) is public; the other outputs are held in the restricted workspace, and this page shows their structure and status only. "
         "This page is generated from `data/outputs_register.csv`; edit that file, not this page.", "",
         "| ID | Output | Gate | Section | Status | Updated | File |", "|---|---|---|---|---|---|---|"]
for r in register:
    lines.append(f"| {r['id']} | {r['output']} | {r['gate']} | [{r['folder']}]({r['folder']}/index.md) | {r['status']} | "
                 f"{r['updated'] or '–'} | {link(r, 'top')} |")
(out_dir / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
for s in SECTIONS:
    d = out_dir / s
    d.mkdir(exist_ok=True)
    rows = [r for r in register if r["folder"] == s]
    files = sorted(p for p in d.iterdir() if p.is_file() and p.name != "index.md" and p.name != "placeholder.txt")
    body = [f"# {s.replace('_', ' ')}", ""]
    if rows:
        body += ["| ID | Output | Contents | Gate | Status | File |", "|---|---|---|---|---|---|"]
        for r in rows:
            body.append(f"| {r['id']} | {r['output']} | {r['contents']} | {r['gate']} | {r['status']} | {link(r, 'section')} |")
    else:
        body.append("Supporting records for this section. No numbered output is assigned here.")
    body += ["", "## Files in this section", ""]
    body += [f"- [{p.name}]({p.name})" for p in files] or ["No files yet. Upload files to `docs/outputs/" + s + "/`."]
    (d / "index.md").write_text("\n".join(body) + "\n", encoding="utf-8")

# ---- downloads --------------------------------------------------------------
dl = DOCS / "data" / "downloads"
dl.mkdir(parents=True, exist_ok=True)
for name in ["cases.csv", "coding.csv", "codebook.csv", "outputs_register.csv"]:
    shutil.copy(DATA / name, dl / name)

# EPPI-Mapper JSON: one reference per use case x outcome domain
PLAIN = {"L1": "Claims only", "L2": "Operational data", "L3": "Outcomes, no comparison",
         "L4": "Outcomes with comparison", "L5": "Proven impact"}
PLAIN_DEF = {
    "L1": "The sources describe what the project does and why it should work, but give no data on results.",
    "L2": "The sources give data on activity, such as payments made or users reached, but not on whether people are better off.",
    "L3": "The sources report changes for participants, such as income or savings, with nothing to compare against.",
    "L4": "The sources compare participants with a similar group or a non-blockchain alternative.",
    "L5": "A randomised trial or strong quasi-experimental study estimates the project's impact."}
dims = [("evidence_level", "Evidence level", "record"), ("outcome_domain", "Outcome domain", "record"),
        ("use_case_domain", "Use-case domain", "case"), ("primary_portfolio", "Portfolio", "case"),
        ("deployment_status_traced", "Traced status", "case"), ("blockchain_added_value", "Blockchain added value", "case"),
        ("region", "Region", "case")]
attr, sets = {}, []
for i, (field, title, _) in enumerate(dims, start=1):
    dim = {"deployment_status_traced": "deployment_status"}.get(field, field)
    values = [v["value"] for v in codebook.get(dim, [])] or sorted({c[field] for c in cases if c.get(field)})
    kids = []
    for v in values:
        aid = i * 1000 + len(kids) + 1
        attr[(field, v)] = aid
        name = label.get((dim, v), v)
        desc = definition.get((dim, v), "")
        if field == "evidence_level":
            # Plain names as on the site's evidence spectrum (19 Oct 2026); the code L1-L5 stays in the description.
            name = f"{int(v[1:])}. {PLAIN[v]}"
            desc = f"{PLAIN_DEF[v]} Protocol code {v}."
        kids.append({"AttributeId": aid, "AttributeName": name, "AttributeDescription": desc,
                     "AttributeType": "Selectable (show checkbox)"})
    if field == "evidence_level":
        title = "Strength of evidence"
    sets.append({"AttributeId": i, "AttributeName": title, "AttributeDescription": "",
                 "AttributeType": "Not selectable (no checkbox)", "Attributes": {"AttributesList": kids}})
BLANK = ["ParentTitle", "DateCreated", "CreatedBy", "DateEdited", "EditedBy", "Year", "Month", "StandardNumber", "City",
         "Country", "Publisher", "Volume", "Pages", "Edition", "Issue", "Availability", "OldItemId", "Comments",
         "TypeName", "Authors", "ParentAuthors", "DOI", "ItemStatus", "ItemStatusTooltip", "QuickCitation", "Keywords"]
refs = []
for n, r in enumerate(coding, start=1):
    c = case_by_id[r["case_id"]]
    merged = {**c, **r}
    ref = {k: "" for k in BLANK}
    ref.update({"Codes": [{"AttributeId": attr[(f, merged[f])], "ItemAttributeFullTextDetails": []}
                          for f, _, _ in dims if merged.get(f) and (f, merged[f]) in attr],
                "Outcomes": [], "ItemId": 100000 + n, "ShortTitle": c["case_id"],
                "Title": f"{c['name']} [{label.get(('outcome_domain', r['outcome_domain']), r['outcome_domain'])}]",
                "URL": c["case_url"], "Abstract": f"{c['summary'].rstrip(' .')}. Result: {r['key_result']}",
                "Institution": label.get(("primary_portfolio", c["primary_portfolio"]), ""),
                "Country": c["country"], "Year": c["year_launched"], "Keywords": c["lineage_id"]})
    refs.append(ref)
json.dump({"CodeSets": [{"SetName": "Pilot evidence map", "SetType": {"SetTypeName": "Standard"},
                         "Attributes": {"AttributesList": sets}}], "References": refs},
          open(dl / "eppi-mapper.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

for note in notes:
    print("note:", note)
print(f"OK: {len(cases)} use cases, {len(coding)} use case-outcome records, {len(register)} outputs. Generated files rebuilt.")
