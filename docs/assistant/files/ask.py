"""Pilot "Ask the map" assistant, v0.1 (Phase D step 5). Local build only.

Design (decisions 1, 2 and 4 approved by Michael, 19 Oct 2026; Annex A12):
  * A rule-based router sends each question to one route. Refusals, counts, lists,
    file links, definitions and takeaway requests are answered by code, with no model.
  * Gap, lookup, scenario and method answers are phrased by the registered model
    (GPT-6 Luna) from records and passages retrieved by code. The model never counts.
  * Every model answer is checked: cited IDs must be in the retrieved context, every
    number must appear in the context, banned phrasing (rankings, advice, new grades)
    fails, and at least one citation is required. A failed answer falls back to a
    code-built template.
  * Grade definitions are shown with each answer that mentions a level.

Usage (from the repository root):
  python assistant/ask.py ask "question" --run-dir assistant/runs/q1
      -> writes route.json; writes answer.md (code route) or request.json (model route)
  python assistant/ask.py finish --run-dir assistant/runs/q1 --response response.json
      -> checks the model response and writes answer.md
  python assistant/ask.py ask "question" --run-dir DIR --no-model
      -> template answer even on model routes
The model adapter is deliberately outside this file: locally the orchestrator sends
request.json to the registered model; the hosted route (proxy) is set before launch.
"""
import argparse, json, math, re, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORPUS = HERE / "corpus"
VERSION = "0.4"

MAP = json.loads((CORPUS / "map.json").read_text(encoding="utf-8"))
MANIFEST = json.loads((CORPUS / "manifest.json").read_text(encoding="utf-8"))
CHUNKS = [json.loads(l) for l in (CORPUS / "chunks.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
DOCS = {d["doc_id"]: d for d in MANIFEST["documents"]}
CB = {dim: {v["value"]: v for v in vals} for dim, vals in MAP["codebook"].items()}
CASES = {c["case_id"]: c for c in MAP["cases"]}
RECORDS = MAP["records"]
LEVELS = ["L1", "L2", "L3", "L4", "L5"]

LIMITS = ("What this map cannot tell you: whether a project worked, or would work in another setting; "
          "which project is best; or what to fund. Evidence levels describe the type of evidence found in "
          "public sources, not the quality of a project.")
FOOTER = (f"Pilot assistant v{VERSION}. Answers come only from the published protocol, codebook, Purpose and Use "
          "Memo, one-pager and the map data, published at Gate 4 (19 October 2026).")

# ----------------------------------------------------------------------------- vocabulary
PORTFOLIO = {"MCV": [r"mercy corps", r"\bmcv\b"], "UNICEF": [r"unicef"], "FIL": [r"filecoin", r"\bfil\b", r"ffdw"],
             "GSR": [r"\bgsr\b(?! foundation leadership)"]}
USE_DOMAIN = {"1": [r"payment", r"cash transfer", r"remittance", r"wage", r"cash\b"],
              "2": [r"credit", r"saving", r"insurance", r"\bloan", r"lending", r"microfinance", r"micro-?finance"],
              "3": [r"identity", r"\b(land|health|birth|civil|medical|digital|property|patient|academic) records?\b", r"record[- ]keeping", r"data integrity", r"provenance", r"archiv", r"storage"],
              "4": [r"supply chain", r"traceab"],
              "5": [r"climate", r"natural asset", r"carbon", r"environment"],
              "6": [r"governance", r"coordination", r"\bdaos?\b"]}
OUTCOME = {"A": [r"efficien", r"transaction cost", r"\bspeed", r"administrative"],
           "B": [r"\breach\b", r"access", r"adoption", r"inclusion", r"unbanked"],
           "C": [r"transparen", r"\btrust", r"accountab", r"leakage", r"fraud"],
           "D": [r"resilien", r"wellbeing", r"well-being", r"income", r"financial stress"],
           "E": [r"sector outcome", r"health", r"education", r"agricultur", r"crop", r"farm"],
           "F": [r"\brisks?\b", r"harm", r"unintended", r"privacy", r"volatil"]}
FUNCTION = {"F1": [r"stablecoin", r"payment rail"], "F2": [r"smart[- ]contract"], "F3": [r"tokeni[sz]", r"fractional"],
            "F4": [r"tamper", r"traceab"], "F5": [r"decentrali[sz]ed storage", r"\bipfs\b"],
            "F6": [r"decentrali[sz]ed governance"], "F7": [r"digital identit", r"credential"]}
STATUS = {"Scaled": [r"\bscaled\b"], "Discontinued": [r"discontinued", r"shut down", r"closed"],
          "Extended pilot": [r"extended pilot"], "Unknown": [r"unknown status", r"status (is )?unknown"]}
COUNTRY = {"KEN": "kenya", "UGA": "uganda", "RWA": "rwanda", "IDN": "indonesia", "GHA": "ghana", "NPL": "nepal",
           "ARG": "argentina", "COL": "colombia", "BGD": "bangladesh", "IND": "india", "NGA": "nigeria",
           "COD": "congo", "BRA": "brazil", "USA": "united states", "MEX": "mexico", "PAK": "pakistan",
           "ETH": "ethiopia", "TZA": "tanzania", "PHL": "philippines", "VNM": "vietnam", "LKA": "sri lanka",
           "ZAF": "south africa", "PER": "peru", "CHL": "chile", "ZMB": "zambia", "MWI": "malawi"}
REGION_OF = {"NPL": "South Asia", "IND": "South Asia", "BGD": "South Asia", "PAK": "South Asia", "LKA": "South Asia",
             "KEN": "Sub-Saharan Africa", "UGA": "Sub-Saharan Africa", "RWA": "Sub-Saharan Africa",
             "GHA": "Sub-Saharan Africa", "NGA": "Sub-Saharan Africa", "COD": "Sub-Saharan Africa",
             "ETH": "Sub-Saharan Africa", "TZA": "Sub-Saharan Africa", "ZAF": "Sub-Saharan Africa",
             "ZMB": "Sub-Saharan Africa", "MWI": "Sub-Saharan Africa", "IDN": "East Asia and Pacific",
             "PHL": "East Asia and Pacific", "VNM": "East Asia and Pacific", "ARG": "Latin America and the Caribbean",
             "COL": "Latin America and the Caribbean", "BRA": "Latin America and the Caribbean",
             "MEX": "Latin America and the Caribbean", "PER": "Latin America and the Caribbean",
             "CHL": "Latin America and the Caribbean", "USA": "North America"}
REGION = {"South Asia": [r"south asia"], "Sub-Saharan Africa": [r"africa"], "East Asia and Pacific": [r"east asia", r"pacific"],
          "Latin America and the Caribbean": [r"latin america", r"caribbean"], "North America": [r"north america"]}

R_INJECT = [r"ignore (all |any |the )?(previous|prior|above|earlier|your)", r"disregard (the|your|all)", r"system prompt",
            r"developer mode", r"you are now", r"jailbreak", r"pretend (to be|you)", r"act as", r"new instructions",
            r"reveal (your|the) (prompt|instructions|rules)", r"override", r"\bDAN\b"]
R_RESTRICTED = [r"review sheet", r"decision cards?", r"review cards?", r"full[- ]quotes?", r"partner agreements?",
                r"data[- ]sharing agreement", r"evidence packets?", r"status signals?", r"restricted", r"handoff",
                r"raw (coder )?outputs?", r"adjudication (sheet|notes?|batch)", r"michael'?s (notes?|answers?)"]
R_RANK = [r"\brank", r"\btop \d", r"\bbest\b(?! practi)", r"\bworst\b", r"most (effective|successful|impactful|promising)",
          r"strongest (case|project|evidence)", r"which (case|project|portfolio|funder)s? (is|are|was|did) (better|best|more)",
          r"\bbetter than\b", r"league table", r"leaderboard"]
R_FUND = [r"should (i|we|gsr|they) (fund|invest|support|back|finance)", r"worth (funding|investing)", r"\binvest(ment)? advice",
          r"recommend .*(fund|invest|grant)", r"(fund|invest in) (this|it|them)\b", r"where should .*(money|funding)"]
R_GRADE = [r"\bre-?grade", r"\bre-?code", r"(what|which) (level|grade|score) (would|should)", r"\bgrade (this|it|my|our)\b",
           r"(assign|give) (it|this|them|a) (an? )?(level|grade|score)", r"should (it|this|.{1,30}) be (rated |coded |graded )?l[1-5]\b",
           r"\brate (this|my|our)\b", r"upgrade .* to l[1-5]", r"score (my|our|this)"]
R_OUT = [r"\bprice\b", r"\bstock\b", r"\bpresident\b", r"\bcapital of\b", r"\bnews\b", r"who won", r"\brecipe", r"\btoday\b", r"exchange rate",
         r"weather (like|forecast|tomorrow|this week)", r"\bforecast for\b",
         r"write (me )?(a|an) (poem|essay|story|code)", r"translate"]
R_FILES = [r"where (can|do) i (find|get|download|see)", r"\bdownload", r"\blink to\b", r"where (is|are) the (code ?book|protocol|memo|one[- ]pager|data)"]
R_DEFINE = [r"what (does|do|is|are) (an? )?(l[1-5]|level [1-5])\b", r"\bdefin(e|ition)", r"what (does|do) .{1,40} mean"]
R_TAKEAWAY = [r"take-?aways?", r"main (finding|result|conclusion|lesson)s?", r"key (finding|result|lesson)s?", r"what did (the|this) (research|study|pilot|map) find",
              r"conclusions?\b", r"does blockchain (work|help)"]
R_COUNT = [r"how many", r"number of", r"\bcount\b", r"\blist (the |all )?", r"which cases", r"what cases"]
R_GAP = [r"\bgaps?\b", r"\bis there (any )?evidence\b", r"\bany evidence (on|for|about)\b", r"no evidence", r"missing evidence", r"where .* (no|little|weak) evidence", r"not covered", r"empty cells?", r"evidence gap"]
R_SCEN = [r"\bi (want|plan|am planning|intend|hope) to", r"\bwe (want|plan|are planning|intend) to", r"(helpful|useful|relevant) (to|for) (me|us|my|our)",
          r"thinking (of|about) (running|launching|starting|designing)", r"what evidence .* (helpful|relevant|useful)"]
R_METHOD = [r"what (did|does|is) (this|the) (research|study|pilot|map|project)", r"(this|the) (research|study|pilot|map) (did|do|about)",
            r"\bhow (was|were|did|do|does) (the|this|they|you) ", r"\bmethod", r"\bprotocol\b", r"\bsampl", r"\bcoders?\b", r"\bcodebook\b",
            r"\bgates?\b", r"\bpurpose\b", r"research questions?"]
R_OVERVIEW = [r"^\W*(what|who) (is|are) (this|it|you)\W*$", r"what can you (do|tell|help)", r"\boverview\b", r"summari[sz]e (the|this) (map|pilot|study|research)",
              r"^\W*(help|hello|hi)\W*$"]
R_BEST_PRACTICE = [r"best practi", r"rigou?r", r"standards?\b.*(follow|adhere|meet)", r"(adhere|comply|align)"]
BANNED_OUT = [r"\brank(ed|ing)?\b", r"\bbest\b(?! practi)", r"most effective", r"(you|gsr) should (fund|invest)", r"\bi recommend\b",
              r"would (be|rate|grade) (as )?l[1-5]", r"\bupgrade\b"]


def any_re(pats, q):
    return any(re.search(p, q, re.I) for p in pats)


def hits(vocab, q):
    return sorted(k for k, pats in vocab.items() if any_re(pats, q))


def parse_filters(q):
    ql = q.lower()
    f = {"portfolio": hits(PORTFOLIO, ql), "use_case_domain": hits(USE_DOMAIN, ql), "outcome_domain": hits(OUTCOME, ql),
         "function": hits(FUNCTION, ql), "status": hits(STATUS, ql),
         "country": sorted(k for k, n in COUNTRY.items() if re.search(r"\b" + n + r"\b", ql)), "region": hits(REGION, ql)}
    m = re.search(r"\bl([1-5])\s*(\+|or (above|higher|more)|and above|or better)", ql) or re.search(r"(at least|above) (level |l)([1-5])", ql)
    if m:
        lo = int(m.group(1) if m.lastindex and m.group(1) and m.group(1).isdigit() else m.group(3))
        f["levels"] = LEVELS[lo - 1:]
    else:
        f["levels"] = sorted(set(re.findall(r"\b(l[1-5])\b", ql))) and [x.upper() for x in sorted(set(re.findall(r"\b(l[1-5])\b", ql)))]
        if not f["levels"] and re.search(r"\boperational\b", ql):
            f["levels"] = ["L2"]
        if not f["levels"] and re.search(r"\bclaim[- ]only\b", ql):
            f["levels"] = ["L1"]
    f["case_ids"] = sorted(set(m.upper() for m in re.findall(r"\b(?:mcv|uni|fil|gsr)-\d{2}\b", ql)))
    return {k: v for k, v in f.items() if v}


def label(dim, v):
    e = CB.get(dim, {}).get(v)
    return f"{v} {e['label']}" if e and e["label"] != v else (e["label"] if e else v)


def case_matches(c, f):
    if f.get("portfolio") and c["primary_portfolio"] not in f["portfolio"]:
        return False
    if f.get("use_case_domain") and c["use_case_domain"] not in f["use_case_domain"]:
        return False
    if f.get("function") and not set(f["function"]) & {x.strip() for x in c["blockchain_functions"].split(";")}:
        return False
    if f.get("status") and c["deployment_status_traced"] not in f["status"]:
        return False
    if f.get("country") and not set(f["country"]) & {x.strip() for x in c["country"].split(";")}:
        return False
    if f.get("region") and c["region"] not in f["region"]:
        return False
    return True


def rec_matches(r, f):
    if f.get("outcome_domain") and r["outcome_domain"] not in f["outcome_domain"]:
        return False
    if f.get("levels") and r["evidence_level"] not in f["levels"]:
        return False
    return True


def describe_filters(f):
    parts = []
    if f.get("portfolio"): parts.append("portfolio " + " or ".join(label("primary_portfolio", x) for x in f["portfolio"]))
    if f.get("use_case_domain"): parts.append("use-case domain " + " or ".join(label("use_case_domain", x) for x in f["use_case_domain"]))
    if f.get("function"): parts.append("blockchain function " + " or ".join(label("blockchain_function", x) for x in f["function"]))
    if f.get("status"): parts.append("traced status " + " or ".join(f["status"]))
    if f.get("country"): parts.append("country " + " or ".join(f["country"]))
    if f.get("region"): parts.append("region " + " or ".join(f["region"]))
    if f.get("outcome_domain"): parts.append("outcome domain " + " or ".join(label("outcome_domain", x) for x in f["outcome_domain"]))
    if f.get("levels"): parts.append("evidence level " + " or ".join(label("evidence_level", x) for x in f["levels"]))
    return "; ".join(parts) or "no filter (all cases)"


# ----------------------------------------------------------------------------- tools (code, no model)
def tool_count(f):
    cases = [c for c in MAP["cases"] if case_matches(c, f)]
    rec_filter = bool(f.get("outcome_domain") or f.get("levels"))
    recs = [r for r in RECORDS if r["case_id"] in {c["case_id"] for c in cases} and rec_matches(r, f)]
    if rec_filter:
        ids = sorted({r["case_id"] for r in recs})
    else:
        ids = sorted(c["case_id"] for c in cases)
    return {"filters": describe_filters(f), "case_count": len(ids), "case_ids": ids,
            "record_count": len(recs), "record_ids": [f"{r['case_id']}/{r['outcome_domain']}" for r in recs],
            "total_cases_in_map": len(MAP["cases"]), "total_records_in_map": len(RECORDS)}


def tool_gap(f):
    rows = f.get("use_case_domain") or [v for v in CB["use_case_domain"] if v != "none"]
    cols = f.get("outcome_domain") or list(CB["outcome_domain"])
    cells = []
    for u in rows:
        ucases = [c["case_id"] for c in MAP["cases"] if c["use_case_domain"] == u and case_matches(c, {k: v for k, v in f.items() if k not in ("use_case_domain", "outcome_domain", "levels")})]
        for o in cols:
            recs = [r for r in RECORDS if r["case_id"] in ucases and r["outcome_domain"] == o]
            lv = Counter(r["evidence_level"] for r in recs)
            n_l1 = lv.get("L1", 0)
            n_hi = len(recs) - n_l1
            state = "gap (no records)" if not recs else ("claim only (L1)" if set(lv) == {"L1"} else "evidence at L2 or above")
            thin = bool(recs) and n_hi > 0 and n_l1 > n_hi
            detail = ("no records" if not recs else
                      f"{len(recs)} records: {n_l1} at L1 (claim only), {n_hi} at L2 or above; highest level {max(lv)}"
                      + ("; thin: most records are claims only" if thin else ""))
            cells.append({"cell": f"{u}/{o}", "cell_name": f"{label('use_case_domain', u).split(' ', 1)[-1]} × {label('outcome_domain', o).split(' ', 1)[-1]}",
                          "use_case_domain": label("use_case_domain", u), "outcome_domain": label("outcome_domain", o),
                          "cases_in_row": len(ucases), "records": len(recs), "records_at_L1": n_l1, "records_at_L2_plus": n_hi,
                          "highest_level": max(lv) if recs else "none", "levels": dict(sorted(lv.items())),
                          "state": state, "thin": thin, "detail": detail, "case_ids": sorted({r["case_id"] for r in recs})})
    summary = Counter(c["state"] for c in cells)
    empty_rows = [label("use_case_domain", u) for u in rows if all(c["cases_in_row"] == 0 for c in cells if c["cell"].startswith(u + "/"))]
    no_l4 = not any(r["evidence_level"] in ("L4", "L5") for r in RECORDS)
    return {"filters": describe_filters(f), "cells_checked": len(cells), "gap_cells": summary.get("gap (no records)", 0),
            "claim_only_cells": summary.get("claim only (L1)", 0), "cells_with_L2_plus": summary.get("evidence at L2 or above", 0),
            "thin_cells_with_L2_plus": sum(c["thin"] for c in cells),
            "use_case_domains_with_no_cases": empty_rows, "no_record_at_L4_or_L5": no_l4,
            "cases_without_outcome_coding": sorted(set(CASES) - {r["case_id"] for r in RECORDS}), "cells": cells}


def case_context(cid):
    c = CASES[cid]
    return {"case_id": cid, "name": c["name"], "portfolio": label("primary_portfolio", c["primary_portfolio"]),
            "funders": c["all_funders"], "country": c["country"] or "(coders differed; not adjudicated for the pilot)",
            "region": c["region"] or "(coders differed; not adjudicated for the pilot)",
            "year_launched": c["year_launched"] or "(coders differed; not adjudicated for the pilot)",
            "use_case_domain": label("use_case_domain", c["use_case_domain"]),
            "blockchain_functions": "; ".join(label("blockchain_function", x.strip()) for x in c["blockchain_functions"].split(";") if x.strip())
                                    or "(coders differed; not adjudicated for the pilot)",
            "implementation_model": c["implementation_model"] or "(coders differed; not adjudicated for the pilot)",
            "status_stated_in_sources": c["deployment_status_stated"] or "not stated",
            "traced_status_draft": c["deployment_status_traced"],
            "blockchain_added_value": label("blockchain_added_value", c["blockchain_added_value"]),
            "case_url": c["case_url"],
            "records": [{"record_id": f"{cid}/{r['outcome_domain']}", "outcome_domain": label("outcome_domain", r["outcome_domain"]),
                         "evidence_level": label("evidence_level", r["evidence_level"]), "key_result": r["key_result"],
                         "source_id": r["source_id"], "evidence_url": r["evidence_url"], "evidence_producer": r["evidence_producer"]}
                        for r in RECORDS if r["case_id"] == cid]}


GENERIC = set("case cases what tell about does show with this that evidence blockchain project projects onchain based using data "
              "smart contract digital community financial impact pilot research which where".split())


R_LOOKUP_INTENT = [r"tell me about", r"what (about|is|are|was|were)\b", r"what does the map (say|show|hold|have)", r"\bdescribe\b",
                   r"\binformation on\b", r"\bany (evidence|records?|cases?) (on|for|about|from)\b", r"who is"]
NAME_STOP = set("what tell about does show with this that evidence blockchain map case cases project the and for from which where who how "
                "is are was were any information describe give list say hold have please can you i we our my".split())


def name_terms(q):
    """Proper-noun-like terms: capitalised or mixed-case words that are not the first word and not common words."""
    words = re.findall(r"[A-Za-z][A-Za-z0-9.\-]{2,}", q)
    out = []
    for i, w in enumerate(words):
        w = w.strip(".-")
        if w.lower() in NAME_STOP or re.fullmatch(r"(?i)(mcv|uni|fil|gsr|l[1-5])(-\d+)?", w):
            continue
        if (i > 0 and w[0].isupper()) or re.search(r"[a-z][A-Z]|[A-Z]{2,}", w):
            out.append(w.lower())
    return out


def _source_text(cid):
    c = CASES[cid]
    doms = [re.sub(r"^https?://(www\.)?([^/]+).*$", r"\2", r["evidence_url"]) for r in RECORDS if r["case_id"] == cid]
    return " ".join([c["name"], c["all_funders"], c["summary"]] + [r["key_result"] for r in RECORDS if r["case_id"] == cid] + doms).lower()


def find_by_name(q):
    """Fix 3 (step 6): match proper-noun terms against case names, funders, key-result text and source domains.
    Terms that occur in more than 3 cases are too general to identify a case and are ignored."""
    hitsets = []
    for t in name_terms(q):
        found = {cid for cid in CASES if re.search(r"(?<![a-z0-9])" + re.escape(t) + r"(?![a-z])", _source_text(cid))}
        if 0 < len(found) <= 3:
            hitsets.append(found)
    if not hitsets:
        return []
    cnt = Counter(c for h in hitsets for c in h)
    top = max(cnt.values())
    return sorted(c for c, n in cnt.items() if n == top)[:3]


def find_case(q):
    ids = parse_filters(q).get("case_ids", [])
    if ids:
        return [i for i in ids if i in CASES]
    byname = find_by_name(q)
    if byname:
        return byname
    toks = set(re.findall(r"[a-z]{4,}", q.lower())) - GENERIC
    name_toks = {cid: set(re.findall(r"[a-z]{4,}", c["name"].lower())) - GENERIC for cid, c in CASES.items()}
    df = Counter(t for v in name_toks.values() for t in v)
    best = []
    for cid, ct in name_toks.items():
        ov = toks & ct
        if len(ov) >= 2 or any(df[t] == 1 and len(t) >= 6 for t in ov):
            best.append((len(ov), cid))
    best.sort(reverse=True)
    return [cid for n, cid in best if n == best[0][0]][:3] if best else []


def tool_scenario(f):
    want_dom, want_geo = f.get("use_case_domain", []), f.get("country", [])
    regions = set(f.get("region", [])) | {REGION_OF[c] for c in want_geo if c in REGION_OF}
    out = {"filters": describe_filters(f), "groups": {}}
    def geo(c):
        cs = {x.strip() for x in c["country"].split(";")}
        return "country" if want_geo and cs & set(want_geo) else ("region" if regions and c["region"] in regions else None)
    groups = {"same domain and same country": [], "same domain and same region": [], "same domain, other or unrecorded geography": [],
              "other domain, same country or region": []}
    for cid, c in CASES.items():
        dom = bool(want_dom) and c["use_case_domain"] in want_dom
        fn = bool(f.get("function")) and bool(set(f["function"]) & {x.strip() for x in c["blockchain_functions"].split(";")})
        g = geo(c)
        if dom and g == "country": groups["same domain and same country"].append(cid)
        elif dom and g == "region": groups["same domain and same region"].append(cid)
        elif dom or (fn and not want_dom): groups["same domain, other or unrecorded geography"].append(cid)
        elif g: groups["other domain, same country or region"].append(cid)
    for k, v in groups.items():
        out["groups"][k] = sorted(v)
    keep = [cid for k in list(groups)[:3] for cid in groups[k]]
    out["matching_cases"] = [case_context(cid) for cid in keep[:8]]
    out["truncated"] = max(0, len(keep) - 8)
    out["geography_note"] = MANIFEST["flags"]["blank_noncore"]
    return out


# ----------------------------------------------------------------------------- retrieval
def _tok(s):
    return [t for t in re.findall(r"[a-z0-9]+", s.lower()) if len(t) > 2]


_DF = Counter(t for c in CHUNKS for t in set(_tok(c["text"])))
_AVG = sum(len(_tok(c["text"])) for c in CHUNKS) / len(CHUNKS)
STOP = set("the and for are what this that with how does did from was were which who why can you your about tell research map pilot study".split())


def bm25(q, k=4, k1=1.4, b=0.75):
    qt = [t for t in _tok(q) if t not in STOP]
    N, scored = len(CHUNKS), []
    for c in CHUNKS:
        tf, L = Counter(_tok(c["text"])), len(_tok(c["text"]))
        s = sum(math.log(1 + (N - _DF[t] + .5) / (_DF[t] + .5)) * tf[t] * (k1 + 1) / (tf[t] + k1 * (1 - b + b * L / _AVG)) for t in qt if t in tf)
        scored.append((s, c))
    scored.sort(key=lambda x: -x[0])
    return [dict(c, score=round(s, 2)) for s, c in scored[:k] if s > 0]


# ----------------------------------------------------------------------------- routing
def route(q):
    ql = q.lower()
    if any_re(R_INJECT, ql): return "refuse_injection"
    if any_re(R_RESTRICTED, ql): return "refuse_restricted"
    if any_re(R_RANK, ql): return "refuse_ranking"
    if any_re(R_FUND, ql): return "refuse_funding"
    if any_re(R_GRADE, ql): return "refuse_grade"
    if any_re(R_OUT, ql) and not parse_filters(q).get("case_ids"): return "refuse_out_of_scope"
    if any_re(R_FILES, ql): return "files"
    if any_re(R_TAKEAWAY, ql): return "takeaways"
    if any_re(R_SCEN, ql): return "scenario"
    if any_re(R_COUNT, ql): return "count"
    if any_re(R_GAP, ql): return "gap"
    if any_re(R_DEFINE, ql) and re.search(r"\bl[1-5]\b|level|status|added value|domain", ql): return "define"
    if find_case(q): return "lookup"
    if any_re(R_METHOD + R_BEST_PRACTICE + R_OVERVIEW, ql): return "method"
    if name_terms(q) and any_re(R_LOOKUP_INTENT, ql): return "lookup_not_found"
    top = bm25(q, 1)
    if top and top[0]["score"] >= 4.0: return "method"
    return "refuse_out_of_scope"


REFUSALS = {
    "refuse_injection": "I can't follow instructions that try to change how this assistant works or to reveal its rules or restricted material. I can answer questions about the evidence map, its cases and its methods.",
    "refuse_restricted": "That material is restricted and is not part of this assistant's corpus. I answer only from the published protocol, codebook, Purpose and Use Memo, one-pager and the map data.",
    "refuse_ranking": "I don't rank cases, portfolios or funders. I can list cases that match a filter (for example a use-case domain or an evidence level), with their codes and sources.",
    "refuse_funding": "I don't give funding, investment or programme advice. I can show what evidence the map holds for a type of use case, and where the gaps are.",
    "refuse_grade": "I don't assign or change evidence levels or other codes. I can show the codes the map already records and the codebook definitions behind them.",
    "refuse_out_of_scope": "That question is outside what this assistant covers. I answer only questions about the Blockchain for Impact Funding Evidence Map pilot: its cases, evidence levels, gaps and methods.",
}


# ----------------------------------------------------------------------------- code answers
def doc_link(doc_id, locator=""):
    d = DOCS[doc_id]
    return f"[{d['title']}{', ' + locator if locator else ''}]({d['public_url']})"


def case_link(cid):
    return f"[{cid}]({CASES[cid]['case_url']})"


def level_defs(levels):
    return [f"{l} {CB['evidence_level'][l]['label']}: {CB['evidence_level'][l]['definition']}" for l in LEVELS if l in levels]


def answer_count(f, facts):
    rec = bool(f.get("outcome_domain") or f.get("levels"))
    lines = [f"{facts['case_count']} of the {facts['total_cases_in_map']} cases match ({facts['filters']})"
             + (", counting a case if at least one of its case-outcome records fits." if rec else ".")]
    if facts["case_ids"]:
        lines.append("Cases: " + ", ".join(case_link(c) for c in facts["case_ids"]) + ".")
    if f.get("outcome_domain") or f.get("levels"):
        lines.append(f"Matching case-outcome records: {facts['record_count']} of {facts['total_records_in_map']}.")
    lines.append("Counted by code from the map data, not by the model.")
    return lines


def answer_files():
    rows = [f"- {doc_link(d['doc_id'])}" for d in MANIFEST["documents"]]
    return ["The published documents this assistant uses are:"] + rows + [
        "Older codebook versions (v1.0, v1.1) and the codebook change log are in the same public folder. "
        "The map data (cases and case-outcome records) will be published at the Gate 4 review."]


def answer_define(q):
    ql = q.lower()
    out = []
    lv = [x.upper() for x in re.findall(r"\bl([1-5])\b", ql)] or [m for m in re.findall(r"level ([1-5])", ql)]
    lv = ["L" + x if not x.startswith("L") else x for x in lv]
    out += level_defs(lv or LEVELS)
    if "status" in ql:
        out += [f"{v}: {e['definition']}" for v, e in CB["deployment_status"].items()]
    if "added value" in ql:
        out += [f"{v} {e['label']}: {e['definition'] or 'Not addressed.'}" for v, e in CB["blockchain_added_value"].items()]
    return out + [f"Source: {doc_link('CODEBOOK_TABLE')}; full rules in {doc_link('CODEBOOK')}."]


def answer_takeaways():
    g = tool_gap({})
    lv = Counter(r["evidence_level"] for r in RECORDS)
    st = Counter(c["deployment_status_traced"] for c in MAP["cases"])
    return ["The pilot's findings memo has not been published yet, so I can't summarise its conclusions or interpret the results. "
            "These descriptive facts are computed by code from the map data:",
            f"- {len(CASES)} cases and {len(RECORDS)} case-outcome records; evidence levels: "
            + ", ".join(f"{l} {CB['evidence_level'][l]['label']} {lv.get(l, 0)}" for l in LEVELS) + ".",
            f"- Of {g['cells_checked']} use-case × outcome cells: {g['gap_cells']} have no records, {g['claim_only_cells']} hold claims only (L1), "
            f"{g['cells_with_L2_plus']} hold evidence at L2 or above. Use-case domains with no cases: {', '.join(g['use_case_domains_with_no_cases']) or 'none'}.",
            "- Traced status: " + ", ".join(f"{k} {v}" for k, v in st.most_common()) + ".",
            "Ask about a domain, a case or the gaps for detail."]


# ----------------------------------------------------------------------------- model step
WORD_LIMIT = {"lookup": 250, "scenario": 250, "gap": 150, "method": 150}
CHECK_SLACK = 30


def build_request(q, rt, context, allowed):
    system = (HERE / "prompts" / "system_v0.2.md").read_text(encoding="utf-8")
    task = {"gap": ("Explain the evidence gaps shown in COMPUTED_FACTS. Name each cell by its domain labels (cell_name, for example "
                    "'Payments and cash transfers × Trust and accountability'), never by a code such as '1/C'. For every cell you mention, "
                    "give its detail (records at L1, records at L2 or above, highest level) and say when a cell is thin. "
                    "Cite case IDs. Do not interpret why gaps exist."),
            "lookup": "Describe the case using only its record: what it is, its codes and what each outcome record says, citing the case ID and record IDs.",
            "scenario": "Explain which cases in the context are relevant to the user's situation and why (which attribute matched: domain, function, country or region), "
                        "with each case's evidence levels. Do not say whether the programme will work or should be funded.",
            "method": "Answer the method question from the passages, citing chunk IDs. If the user asks how well the research meets best practice, describe "
                      "only the safeguards the documents state; do not judge quality."}[rt]
    task += f" Word limit: {WORD_LIMIT[rt]} words; answers over {WORD_LIMIT[rt] + CHECK_SLACK} words are rejected."
    text = (f"{system}\n\nTASK: {task}\n\n<QUESTION>\n{q}\n</QUESTION>\n\n<CONTEXT>\n{json.dumps(context, ensure_ascii=False, indent=1)}\n</CONTEXT>\n\n"
            f"Allowed citation IDs: {', '.join(sorted(allowed))}")
    schema = json.loads((HERE / "answer_schema_v0.2.json").read_text())
    return {"model": "gpt_6_luna", "instruction": "Follow the rules at the top of the text and return the answer object.",
            "text": text, "output_schema": schema}


NUM = re.compile(r"(?<![A-Za-z\-/.])(\d+(?:\.\d+)?)(?![\-/]\d)")


def numbers(s):
    s = re.sub(r"\b(?:[A-Z]{2,6}-\d{2}(?:/[A-F])?|L[1-5]|F[1-7]|S\d{2}|v\d+(?:\.\d+)*|p\.? ?\d+|[A-Z]+-p\d+-\d+|[A-Z]+-\d+)\b", " ", s)
    return set(NUM.findall(s))


def check(resp, rt, context_str, allowed):
    probs = []
    if resp.get("refused"):
        probs.append("model refused: " + resp.get("refusal_reason", ""))
    if not resp.get("supported"):
        probs.append("model marked answer unsupported")
    cites = set(resp.get("citations", []))
    if not cites:
        probs.append("no citations")
    bad = sorted(c for c in cites if c not in allowed)
    if bad:
        probs.append("citations not in context: " + ", ".join(bad))
    extra = sorted(numbers(resp.get("answer_text", "")) - numbers(context_str) - {str(i) for i in range(0, 1)})
    if extra:
        probs.append("numbers not in context: " + ", ".join(extra))
    if re.search(r"(?<![\w-])[1-6]/[A-F]\b", resp.get("answer_text", "")):
        probs.append("cell code used instead of domain labels")
    if any_re(BANNED_OUT, resp.get("answer_text", "")):
        probs.append("banned phrasing (ranking, advice or new grade)")
    if len(resp.get("answer_text", "").split()) > WORD_LIMIT.get(rt, 150) + CHECK_SLACK:
        probs.append("answer too long")
    return probs


# ----------------------------------------------------------------------------- rendering
def sources_block(cites):
    out, recs = [], {}
    for c in sorted(cites):
        cid = c.split("/")[0]
        if cid in CASES:
            recs.setdefault(cid, [])
            if "/" in c:
                recs[cid].append(c.split("/")[1])
    for cid, ds in recs.items():
        out.append(f"- {case_link(cid)}: {CASES[cid]['name']}" + (f" (records {', '.join(ds)})" if ds else ""))
    for c in sorted(cites):
        ch = next((x for x in CHUNKS if x["chunk_id"] == c), None)
        if ch:
            out.append(f"- {doc_link(ch['doc_id'], ch['locator'])} ({c})")
        elif c in DOCS:
            out.append(f"- {doc_link(c)}")
    return list(dict.fromkeys(out))


def render(q, rt, body_lines, cites=(), levels=(), limits=False, draft_status=False, note=None):
    out = [f"**Question:** {q}", "", *body_lines]
    if cites:
        out += ["", "**Sources**", *sources_block(cites)]
    if levels:
        out += ["", "**Evidence levels used here**", *[f"- {d}" for d in level_defs(levels)]]
    if draft_status:
        out += ["", "Traced status comes from the status-tracing table (O14). 'Unknown' means public status signals did not show the funded solution in use, not that it failed."]
    if limits:
        out += ["", LIMITS]
    if note:
        out += ["", f"Check note: {note}"]
    out += ["", f"Route: {rt}. {FOOTER}"]
    return "\n".join(out) + "\n"


def levels_in(obj):
    return sorted(set(re.findall(r"\bL[1-5]\b", json.dumps(obj))))


def template(rt, ctx):
    if rt == "gap":
        f = ctx["COMPUTED_FACTS"]
        lines = [f"Of {f['cells_checked']} use-case × outcome cells checked ({f['filters']}): {f['gap_cells']} have no records (gaps), "
                 f"{f['claim_only_cells']} hold claims only (L1) and {f['cells_with_L2_plus']} hold evidence at L2 or above."]
        if f.get("thin_cells_with_L2_plus"):
            lines.append(f"{f['thin_cells_with_L2_plus']} of the cells with evidence at L2 or above are thin: most of their records are claims only (L1).")
        lines += [f"- {c['cell_name']}: {c['state']}; {c['detail']}" + (f" ({', '.join(c['case_ids'])})" if c["case_ids"] else "")
                  for c in f["cells"] if c["state"] != "evidence at L2 or above" or c["thin"]][:20]
        if f["use_case_domains_with_no_cases"]:
            lines.append("Use-case domains with no cases in the pilot: " + ", ".join(f["use_case_domains_with_no_cases"]) + ".")
        if f["no_record_at_L4_or_L5"]:
            lines.append("No record in the map reaches L4 or L5.")
        return lines
    if rt in ("lookup", "scenario"):
        lines = []
        cs = ctx.get("CASES") or ctx.get("COMPUTED_FACTS", {}).get("matching_cases", [])
        if rt == "scenario":
            g = ctx["COMPUTED_FACTS"]["groups"]
            lines += [f"Matched on: {ctx['COMPUTED_FACTS']['filters']}."] + [f"- {k}: {', '.join(v) or 'none'}" for k, v in g.items()]
        for c in cs:
            lines.append(f"{c['case_id']} {c['name']} ({c['use_case_domain']}; {c['portfolio']}; country {c['country']}):")
            lines += [f"  - {r['outcome_domain']}, {r['evidence_level']}: {r['key_result']}" for r in c["records"]] or ["  - No outcome records coded."]
        return lines
    if rt == "method":
        return ["The most relevant passages are:"] + [f"- {c['text'][:300]}… ({c['chunk_id']})" for c in ctx["PASSAGES"]]
    return []


def prepare(q):
    rt = route(q)
    f = parse_filters(q)
    res = {"question": q, "route": rt, "filters": f, "model_needed": False}
    if rt.startswith("refuse"):
        res["answer"] = render(q, rt, [REFUSALS[rt]])
    elif rt == "lookup_not_found":
        terms = ", ".join(dict.fromkeys(name_terms(q)))
        res["answer"] = render(q, rt, [f"I couldn't find {terms} in the map's published case names, funders, key results or source websites. "
                                       f"The map holds {len(CASES)} cases; ask for a list (for example \"list the cases in Kenya\") or use a case ID such as MCV-02."])
    elif rt == "files":
        res["answer"] = render(q, rt, answer_files())
    elif rt == "define":
        res["answer"] = render(q, rt, answer_define(q))
    elif rt == "takeaways":
        res["answer"] = render(q, rt, answer_takeaways(), levels=LEVELS, limits=True, draft_status=True)
    elif rt == "count":
        facts = tool_count(f)
        res["facts"] = facts
        res["answer"] = render(q, rt, answer_count(f, facts), cites=facts["case_ids"], levels=f.get("levels", []),
                               draft_status="status" in f)
    else:
        if rt == "gap":
            facts = tool_gap(f)
            facts["cells"] = [{k: v for k, v in cell.items() if k != "cell"} for cell in facts["cells"]]
            ctx = {"COMPUTED_FACTS": facts, "DEFINITIONS": level_defs(LEVELS)}
            allowed = {c for cell in facts["cells"] for c in cell["case_ids"]}
        elif rt == "lookup":
            ctx = {"CASES": [case_context(c) for c in find_case(q)]}
            allowed = {c["case_id"] for c in ctx["CASES"]} | {r["record_id"] for c in ctx["CASES"] for r in c["records"]}
        elif rt == "scenario":
            facts = tool_scenario(f)
            ctx = {"COMPUTED_FACTS": facts}
            allowed = {c for v in facts["groups"].values() for c in v} | {r["record_id"] for c in facts["matching_cases"] for r in c["records"]}
        else:
            qx = q + (" reliability standards crosswalk Nesta Maryland 3ie Campbell dual coding calibration audit agreement" if any_re(R_BEST_PRACTICE, q.lower()) else "")
            ps = bm25(qx, 4)
            if any_re(R_METHOD[:2] + R_OVERVIEW, q.lower()) or not ps:
                lead = [dict(c, score=None) for c in CHUNKS if c["chunk_id"] in ("ONEPAGER-p1-0", "ONEPAGER-p1-1", "PROTOCOL-p2-1", "PROTOCOL-p2-2")]
                ps = lead + [p for p in ps if p["chunk_id"] not in {c["chunk_id"] for c in lead}][:1]
            ctx = {"PASSAGES": [{"chunk_id": p["chunk_id"], "document": DOCS[p["doc_id"]]["title"], "locator": p["locator"], "text": p["text"]} for p in ps]}
            allowed = {p["chunk_id"] for p in ps}
            if any_re(R_BEST_PRACTICE, q.lower()):
                ctx["NOTE"] = "The assistant does not judge the research's quality. Reliability results are in the published agreement summary (O10) and the Gate 4 note."
        res.update(model_needed=True, context=ctx, allowed=sorted(allowed), request=build_request(q, rt, ctx, allowed))
    return res


def finish(prep, resp):
    rt, q, ctx = prep["route"], prep["question"], prep["context"]
    ctx_str = json.dumps(ctx, ensure_ascii=False)
    allowed = set(prep["allowed"])
    lv = levels_in(ctx)
    limits = rt in ("scenario", "gap")
    draft = "traced_status_draft" in ctx_str
    extra = []
    if rt == "method" and ctx.get("NOTE"):
        extra = [ctx["NOTE"]]
    if resp is None:
        return render(q, rt, extra + template(rt, ctx), cites=allowed if rt != "gap" else [], levels=lv, limits=limits, draft_status=draft,
                      note="template answer (no model call)"), []
    probs = check(resp, rt, ctx_str, allowed)
    if probs and resp.get("refused") and rt in ("lookup", "scenario", "gap", "method"):
        return render(q, rt, [REFUSALS["refuse_injection"]]), probs
    if probs:
        return render(q, rt, extra + template(rt, ctx), cites=allowed if rt != "gap" else [], levels=lv, limits=limits, draft_status=draft,
                      note="model answer failed the check (" + "; ".join(probs) + "); template answer shown"), probs
    return render(q, rt, extra + [resp["answer_text"]], cites=resp["citations"], levels=sorted(set(lv) & set(levels_in(resp["answer_text"])) or lv),
                  limits=limits, draft_status=draft and "status" in resp["answer_text"].lower()), []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["ask", "finish"])
    ap.add_argument("question", nargs="?")
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--response")
    ap.add_argument("--no-model", action="store_true")
    a = ap.parse_args()
    d = Path(a.run_dir); d.mkdir(parents=True, exist_ok=True)
    if a.cmd == "ask":
        p = prepare(a.question)
        (d / "route.json").write_text(json.dumps({k: v for k, v in p.items() if k != "request"}, indent=1, ensure_ascii=False), encoding="utf-8")
        if not p["model_needed"]:
            (d / "answer.md").write_text(p["answer"], encoding="utf-8")
            print(f"{p['route']}: code answer -> {d/'answer.md'}")
        elif a.no_model:
            ans, _ = finish(p, None)
            (d / "answer.md").write_text(ans, encoding="utf-8")
            print(f"{p['route']}: template answer -> {d/'answer.md'}")
        else:
            (d / "request.json").write_text(json.dumps(p["request"], indent=1, ensure_ascii=False), encoding="utf-8")
            print(f"{p['route']}: model request -> {d/'request.json'}")
    else:
        p = json.loads((d / "route.json").read_text(encoding="utf-8"))
        resp = json.loads(Path(a.response).read_text(encoding="utf-8"))
        ans, probs = finish(p, resp)
        (d / "answer.md").write_text(ans, encoding="utf-8")
        (d / "check.json").write_text(json.dumps({"problems": probs, "passed": not probs}, indent=1), encoding="utf-8")
        print(f"{p['route']}: check {'passed' if not probs else 'FAILED: ' + '; '.join(probs)} -> {d/'answer.md'}")


if __name__ == "__main__":
    main()
