"""Validate a coder output against the v1.0 schema and check every quote against the frozen packet.
Usage: python check_coder_output.py OUTPUT.json PACKET.md SCHEMA.json
Quote rule: after normalising whitespace and typographic quotes, each quote must appear verbatim inside the named source block. Failures go to human review (protocol 8.1)."""
import json, re, sys
from jsonschema import Draft202012Validator
out, packet, schema = sys.argv[1:4]
o = json.load(open(out)); s = json.load(open(schema)); txt = open(packet).read()
errs = sorted(Draft202012Validator(s).iter_errors(o), key=lambda e: list(e.path))
blocks = {m.group(1): m.group(2) for m in re.finditer(r"=== BEGIN (S\d\d) ===\n(.*?)\n=== END \1 ===", txt, re.S)}
def norm(t):
    t = t.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"').replace("\u2013", "-").replace("\u2014", "-")
    return re.sub(r"\s+", " ", t).strip()
nb = {k: norm(v) for k, v in blocks.items()}
quotes = []
def walk(x, path):
    if isinstance(x, dict):
        if isinstance(x.get("quote"), str) and x["quote"].strip():
            quotes.append((path, x.get("source_id"), x["quote"]))
        for k, v in x.items(): walk(v, f"{path}.{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x): walk(v, f"{path}[{i}]")
walk(o, "$")
fails = []
for path, sid, q in quotes:
    if sid not in nb: fails.append((path, sid, "unknown source", q)); continue
    if norm(q) not in nb[sid]:
        other = [k for k in nb if norm(q) in nb[k]]
        fails.append((path, sid, f"not found in {sid}" + (f" (found in {other})" if other else ""), q))
rep = {"output": out, "schema_valid": not errs, "schema_errors": [f"{'/'.join(map(str, e.path))}: {e.message[:160]}" for e in errs],
       "quotes_checked": len(quotes), "quote_failures": [{"path": p, "source": s_, "reason": r, "quote": q} for p, s_, r, q in fails]}
print(json.dumps(rep, indent=1))
