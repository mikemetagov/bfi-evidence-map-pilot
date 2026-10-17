"""Agreement between Coder A and Coder B on core fields (protocol 8.3).
Usage: python agreement.py RAW_DIR CASE_IDS_COMMA OUT_JSON
Units: use-case domain, deployment status, added value (1 per case); outcome domain present (6 per case, A-F);
evidence level (per outcome domain coded present by both coders); objective achievement (per objective ID coded by both).
Stats: percent agreement, Cohen's kappa (quadratic-weighted for ordinal), Krippendorff's alpha (nominal or ordinal),
Gwet's AC1 (nominal) / AC2 (quadratic weights, ordinal), with 95% bootstrap CIs resampling cases (2,000 draws, seed 20261017)."""
import json, sys, os, itertools, numpy as np
raw, ids, outp = sys.argv[1], sys.argv[2].split(","), sys.argv[3]
L = {c: json.load(open(os.path.join(raw, "A", c + ".json"))) for c in ids}
R = {c: json.load(open(os.path.join(raw, "B", c + ".json"))) for c in ids}
LEV = ["L1", "L2", "L3", "L4", "L5"]; ACH = ["Not achieved", "Unclear", "Partly achieved", "Achieved"]
def units(c):
    a, b = L[c], R[c]; u = []
    u.append(("use_case_domain", a["use_case_domain"]["value"], b["use_case_domain"]["value"]))
    u.append(("stated_deployment_status", a["stated_deployment_status"]["value"], b["stated_deployment_status"]["value"]))
    u.append(("blockchain_added_value", a["blockchain_added_value"]["value"], b["blockchain_added_value"]["value"]))
    da = {o["domain"]: o["evidence_level"] for o in a["outcomes"]}; db = {o["domain"]: o["evidence_level"] for o in b["outcomes"]}
    # highest level per domain if a coder lists a domain twice
    for o in a["outcomes"]: da[o["domain"]] = max(da[o["domain"]], o["evidence_level"])
    for o in b["outcomes"]: db[o["domain"]] = max(db[o["domain"]], o["evidence_level"])
    for d in "ABCDEF":
        u.append(("outcome_domain_present", int(d in da), int(d in db)))
        if d in da and d in db: u.append(("evidence_level", da[d], db[d]))
    oa = {x["objective_id"]: x["value"] for x in a["objective_achievement"]}; ob = {x["objective_id"]: x["value"] for x in b["objective_achievement"]}
    for k in sorted(set(oa) & set(ob)): u.append(("objective_achievement", oa[k], ob[k]))
    return u
ORD = {"evidence_level": LEV, "blockchain_added_value": [0, 1, 2, 3], "objective_achievement": ACH}
def stats(pairs, field):
    if not pairs: return None
    cats = ORD.get(field) or sorted({x for p in pairs for x in p}, key=str); k = len(cats); idx = {c: i for i, c in enumerate(cats)}
    a = np.array([idx[p[0]] for p in pairs]); b = np.array([idx[p[1]] for p in pairs]); n = len(a)
    ordinal = field in ORD
    W = np.array([[1 - ((i - j) / (k - 1)) ** 2 if k > 1 else 1 for j in range(k)] for i in range(k)]) if ordinal else np.eye(k)
    po = float(np.mean(a == b)); pw = float(np.mean([W[x, y] for x, y in zip(a, b)]))
    pa = np.bincount(a, minlength=k) / n; pb = np.bincount(b, minlength=k) / n
    pe = float(sum(W[i, j] * pa[i] * pb[j] for i in range(k) for j in range(k)))
    kappa = (pw - pe) / (1 - pe) if pe < 1 else (1.0 if pw == 1 else 0.0)
    pi = (pa + pb) / 2
    if ordinal: pe_g = float(W.sum() / (k * (k - 1)) * np.sum(pi * (1 - pi))) if k > 1 else 0
    else: pe_g = float(np.sum(pi * (1 - pi)) / (k - 1)) if k > 1 else 0
    ac = (pw - pe_g) / (1 - pe_g) if pe_g < 1 else 1.0
    # Krippendorff alpha, 2 coders, no missing
    vals = np.concatenate([a, b]); N = len(vals)
    D = (lambda x, y: (x - y) ** 2) if ordinal else (lambda x, y: float(x != y))
    Do = np.mean([D(x, y) for x, y in zip(a, b)])
    De = np.mean([D(x, y) for x, y in itertools.permutations(vals, 2)]) if N > 1 else 0
    alpha = 1 - Do / De if De > 0 else (1.0 if Do == 0 else 0.0)
    return {"n_units": n, "percent_agreement": round(po, 3), "kappa": round(kappa, 3), "alpha": round(alpha, 3), ("AC2" if ordinal else "AC1"): round(ac, 3), "weighted": ordinal}
U = {c: units(c) for c in ids}
fields = ["use_case_domain", "outcome_domain_present", "evidence_level", "stated_deployment_status", "blockchain_added_value", "objective_achievement"]
rng = np.random.default_rng(20261017); res = {}
for f in fields:
    pairs = [(x, y) for c in ids for (g, x, y) in U[c] if g == f]
    s = stats(pairs, f)
    if s is None: res[f] = None; continue
    boots = {m: [] for m in ["percent_agreement", "kappa", "alpha"]}
    for _ in range(2000):
        cs = rng.choice(ids, size=len(ids), replace=True)
        bp = [(x, y) for c in cs for (g, x, y) in U[c] if g == f]
        if not bp: continue
        bs = stats(bp, f)
        for m in boots: boots[m].append(bs[m])
    s["ci95"] = {m: [round(float(np.percentile(v, 2.5)), 3), round(float(np.percentile(v, 97.5)), 3)] for m, v in boots.items() if v}
    res[f] = s
dis = [{"case_id": c, "field": g, "A": x, "B": y} for c in ids for (g, x, y) in U[c] if x != y]
json.dump({"cases": ids, "fields": res, "disagreements": dis}, open(outp, "w"), indent=1, default=str)
for f in fields:
    s = res[f]; print(f, s and {k: s[k] for k in s if k != "ci95"}, s and s["ci95"].get("kappa"))
print(len(dis), "disagreements")
