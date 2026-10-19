/* Hover evidence gap map, driven by map-data.json (built by scripts/build.py).
   Rows, columns, bubble colours and filters come from the "config" block, and
   labels from the codebook. Hover or focus a bubble to preview the cases behind
   it; click to pin the card so its links can be followed; Esc closes. */
(function () {
  function el(tag, attrs, ...kids) {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (k === "class") n.className = v;
      else if (k === "text") n.textContent = v;
      else if (k.startsWith("on")) n.addEventListener(k.slice(2), v);
      else if (v !== null && v !== undefined) n.setAttribute(k, v);
    }
    for (const k of kids.flat()) if (k) n.append(k);
    return n;
  }
  const plural = (n, w) => `${n} ${w}${n === 1 ? "" : "s"}`;

  async function init(root) {
    if (root.dataset.ready) return;
    root.dataset.ready = "1";
    let data;
    try {
      const res = await fetch(root.dataset.src || "map-data.json", { cache: "no-store" });
      if (!res.ok) throw new Error(res.status);
      data = await res.json();
    } catch (e) {
      root.append(el("p", { class: "egm-error", text: "The map data could not be loaded. Check that the latest build finished without errors." }));
      return;
    }
    const { config: cfg, codebook: cb } = data;
    const vals = (dim) => (cb[dim] || []).map((v) => v.value);
    const lab = (dim, v) => ((cb[dim] || []).find((x) => x.value === v) || {}).label || v || "";
    const def0 = (dim, v) => ((cb[dim] || []).find((x) => x.value === v) || {}).definition || "";
    // Plain-language evidence names used on the site (20 Oct 2026). The data files and protocol keep the codes L1-L5.
    const PLAIN = { L1: "Claims only", L2: "Operational data", L3: "Outcomes, no comparison", L4: "Outcomes with comparison", L5: "Proven impact" };
    const PLAIN_DEF = {
      L1: "The sources describe what the project does and why it should work, but give no data on results.",
      L2: "The sources give data on activity, such as payments made or users reached, but not on whether people are better off.",
      L3: "The sources report changes for participants, such as income or savings, with nothing to compare against.",
      L4: "The sources compare participants with a similar group or a non-blockchain alternative.",
      L5: "A randomised trial or strong quasi-experimental study estimates the project's impact." };
    const glab = (g) => PLAIN[g] || lab(cfg.grade.dim, g);
    const def = (dim, v) => (dim === cfg.grade.dim && PLAIN_DEF[v]) || def0(dim, v);
    const gradeTitle = "Strength of evidence";
    const caseById = Object.fromEntries(data.cases.map((c) => [c.case_id, c]));
    const rows = vals(cfg.row.dim), cols = vals(cfg.col.dim), grades = vals(cfg.grade.dim);
    const gIdx = Object.fromEntries(grades.map((g, i) => [g, i + 1]));
    const state = {};

    // controls
    const controls = el("div", { class: "egm-controls", role: "group", "aria-label": "Filter the map" });
    for (const f of cfg.filters) {
      const options = f.dim ? vals(f.dim) : [...new Set(data.cases.map((c) => c[f.field]).filter(Boolean))].sort();
      const id = "egm-f-" + f.field;
      const sel = el("select", { id, onchange: (e) => { state[f.field] = e.target.value; render(); } },
        el("option", { value: "", text: "All" }), options.map((v) => el("option", { value: v, text: f.dim ? lab(f.dim, v) : v })));
      controls.append(el("label", { for: id, class: "egm-filter" }, el("span", { text: f.title }), sel));
    }
    controls.append(el("button", { type: "button", class: "egm-reset", text: "Clear filters",
      onclick: () => { controls.querySelectorAll("select").forEach((s) => (s.value = "")); for (const k in state) state[k] = ""; render(); } }));
    const legend = el("div", { class: "egm-legend", "aria-label": cfg.grade.title + " key" },
      el("span", { class: "egm-legend-title", text: gradeTitle + ", weakest to strongest:" }),
      grades.map((g) => el("span", { class: "egm-legend-item", title: def(cfg.grade.dim, g) },
        el("span", { class: "egm-dot g" + gIdx[g] }), el("span", { text: glab(g) + (data.records.some((r) => r[cfg.grade.field] === g) ? "" : " (none in pilot)") }))),
      el("span", { class: "egm-legend-note", text: "Bubble size and number = use cases. \u201cgap\u201d = no evidence found." }));
    const summary = el("p", { class: "egm-summary", "aria-live": "polite" });
    const gridWrap = el("div", { class: "egm-scroll" });
    const listWrap = el("div", { class: "egm-records" });
    root.append(controls, legend, summary, gridWrap, listWrap);

    // card
    const card = el("div", { class: "egm-card", role: "dialog", "aria-modal": "false", hidden: "" });
    document.body.append(card);
    let hideTimer = null, pinned = null, lastPointer = "mouse";
    document.addEventListener("pointerdown", (e) => { lastPointer = e.pointerType; }, true);
    const cancelHide = () => clearTimeout(hideTimer);
    const scheduleHide = () => { cancelHide(); if (!pinned) hideTimer = setTimeout(hideCard, 220); };
    function hideCard() { card.hidden = true; if (pinned) pinned.setAttribute("aria-expanded", "false"); pinned = null; }
    card.addEventListener("mouseenter", cancelHide);
    card.addEventListener("mouseleave", scheduleHide);
    document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !card.hidden) { const b = pinned; hideCard(); if (b) b.focus(); } });
    document.addEventListener("click", (e) => { if (!card.hidden && !card.contains(e.target) && !e.target.closest(".egm-bubble")) hideCard(); });
    window.addEventListener("scroll", () => { if (!pinned) card.hidden = true; }, { passive: true });

    function showCard(btn, cell) {
      cancelHide();
      card.replaceChildren(
        el("div", { class: "egm-card-head" },
          el("div", { class: "egm-card-cell", text: lab(cfg.row.dim, cell.row) + " \u00d7 " + lab(cfg.col.dim, cell.col) }),
          el("div", { class: "egm-card-grade" }, el("span", { class: "egm-dot g" + gIdx[cell.grade] }),
            el("span", { text: glab(cell.grade) })),
          el("div", { class: "egm-card-count", text: plural(cell.items.length, "use case") }),
          el("button", { type: "button", class: "egm-card-close", "aria-label": "Close", text: "\u00d7",
            onclick: () => { const b = pinned; hideCard(); if (b) b.focus(); } })),
        el("ul", { class: "egm-card-list" }, cell.items.map(({ c, r }) => el("li", {},
          c.case_url ? el("a", { href: c.case_url, target: "_blank", rel: "noopener", class: "egm-case-link", text: c.name || c.case_id })
                     : el("span", { class: "egm-case-link", text: c.name || c.case_id }),
          el("div", { class: "egm-meta", text: [c.case_id, lab("primary_portfolio", c.primary_portfolio), c.country || c.region,
            c.deployment_status_traced && ("Status: " + c.deployment_status_traced + (c.status_confidence ? " (" + c.status_confidence.toLowerCase() + " confidence)" : ""))].filter(Boolean).join(" \u00b7 ") }),
          c.blockchain_added_value !== "" ? el("div", { class: "egm-meta", text: "Blockchain added value: " + lab("blockchain_added_value", c.blockchain_added_value) }) : null,
          r.key_result ? el("div", { class: "egm-rationale", text: r.key_result }) : null,
          r.quote ? el("blockquote", { class: "egm-quote", text: "\u201c" + r.quote + "\u201d" }) : null,
          el("div", { class: "egm-meta" },
            r.evidence_url ? el("a", { href: r.evidence_url, target: "_blank", rel: "noopener", class: "egm-evidence-link", text: "Source " + (r.source_id || "") + " \u2197" }) : (r.source_id ? "Source " + r.source_id : null),
            r.evidence_producer ? " \u00b7 " + r.evidence_producer : null)))),
        el("p", { class: "egm-card-hint", text: pinned ? "Press Esc to close" : "Click the bubble to pin this card" }));
      card.hidden = false;
      if (window.innerWidth < 600) { card.classList.add("egm-sheet"); card.style.left = ""; card.style.top = ""; return; }
      card.classList.remove("egm-sheet");
      const b = btn.getBoundingClientRect(), w = card.offsetWidth, h = card.offsetHeight;
      let left = b.right + 10, top = b.top - 8;
      if (left + w > window.innerWidth - 8) left = Math.max(8, b.left - w - 10);
      if (top + h > window.innerHeight - 8) top = Math.max(8, window.innerHeight - h - 8);
      card.style.left = left + "px"; card.style.top = top + "px";
    }

    function render() {
      hideCard();
      const keep = data.cases.filter((c) => cfg.filters.every((f) => !state[f.field] || c[f.field] === state[f.field]));
      const keepIds = new Set(keep.map((c) => c.case_id));
      const recs = data.records.filter((r) => keepIds.has(r.case_id));
      const shown = new Set(recs.map((r) => r.case_id));
      summary.textContent = data.records.length === 0
        ? `No cases coded yet (${plural(data.cases.length, "use case")} listed). The map fills in when the final coded dataset (O12) is added at Gate 4. Cells marked \u201cgap\u201d have no evidence.`
        : `Showing ${plural(shown.size, "use case")} (${plural(recs.length, "use case\u2013outcome record")}).`;

      const cells = {};
      for (const r of recs) {
        const c = caseById[r.case_id];
        const key = c[cfg.row.field] + "|" + r[cfg.col.field];
        ((cells[key] ||= {})[r[cfg.grade.field]] ||= []).push({ c, r });
      }
      const maxN = Math.max(1, ...Object.values(cells).flatMap((g) => Object.values(g).map((a) => a.length)));
      const thead = el("thead", {}, el("tr", {},
        el("th", { class: "egm-corner", scope: "col" }, el("span", { text: cfg.row.title + " \u2193 / " + cfg.col.title + " \u2192" })),
        cols.map((o) => el("th", { scope: "col", title: def(cfg.col.dim, o), text: lab(cfg.col.dim, o) }))));
      const tbody = el("tbody", {}, rows.map((rv) => el("tr", {},
        el("th", { scope: "row", title: def(cfg.row.dim, rv), text: lab(cfg.row.dim, rv) }),
        cols.map((cv) => {
          const byGrade = cells[rv + "|" + cv] || {};
          const td = el("td", Object.keys(byGrade).length ? {} : { class: "egm-empty", "aria-label": "gap: no evidence found" });
          const wrap = el("div", { class: "egm-bubbles" });
          for (const g of grades) {
            const items = byGrade[g];
            if (!items) continue;
            const size = Math.round(26 + 22 * Math.sqrt(items.length / maxN));
            const cell = { row: rv, col: cv, grade: g, items };
            const btn = el("button", { type: "button", class: "egm-bubble g" + gIdx[g], style: `width:${size}px;height:${size}px`,
              "aria-label": `${lab(cfg.row.dim, rv)}, ${lab(cfg.col.dim, cv)}: ${glab(g)}, ${plural(items.length, "use case")}. Press Enter to open details.`,
              "aria-expanded": "false", "aria-haspopup": "dialog", text: String(items.length) });
            btn.addEventListener("mouseenter", () => { if (!pinned && lastPointer === "mouse") showCard(btn, cell); });
            btn.addEventListener("mouseleave", () => { if (lastPointer === "mouse") scheduleHide(); });
            btn.addEventListener("focus", () => { if (!pinned && lastPointer === "mouse") showCard(btn, cell); });
            btn.addEventListener("blur", (e) => { if (!pinned && !card.contains(e.relatedTarget)) scheduleHide(); });
            btn.addEventListener("click", (e) => {
              e.stopPropagation();
              if (pinned === btn) { hideCard(); return; }
              if (pinned) pinned.setAttribute("aria-expanded", "false");
              pinned = btn; btn.setAttribute("aria-expanded", "true");
              showCard(btn, cell);
              const first = card.querySelector("a"); if (first && e.detail === 0) first.focus();
            });
            wrap.append(btn);
          }
          td.append(wrap);
          return td;
        }))));
      gridWrap.replaceChildren(el("table", { class: "egm-grid" },
        el("caption", { class: "egm-sr", text: `Evidence gap map: rows are ${cfg.row.title.toLowerCase()}s, columns are ${cfg.col.title.toLowerCase()}s` }), thead, tbody));

      if (!recs.length) { listWrap.replaceChildren(); return; }
      const sorted = [...recs].sort((a, b) => (gIdx[b[cfg.grade.field]] - gIdx[a[cfg.grade.field]]) || a.case_id.localeCompare(b.case_id));
      listWrap.replaceChildren(el("details", {},
        el("summary", { text: `List all ${plural(recs.length, "record")} shown on the map` }),
        el("table", { class: "egm-list" },
          el("thead", {}, el("tr", {}, ["Use case", cfg.col.title, cfg.row.title, gradeTitle, "Portfolio"].map((h) => el("th", { scope: "col", text: h })))),
          el("tbody", {}, sorted.map((r) => { const c = caseById[r.case_id]; return el("tr", {},
            el("td", {}, c.case_url ? el("a", { href: c.case_url, target: "_blank", rel: "noopener", text: c.name || c.case_id }) : (c.name || c.case_id)),
            el("td", { text: lab(cfg.col.dim, r[cfg.col.field]) }), el("td", { text: lab(cfg.row.dim, c[cfg.row.field]) }),
            el("td", { text: glab(r[cfg.grade.field]) }),
            el("td", { text: lab("primary_portfolio", c.primary_portfolio) })); })))));
    }
    render();
  }

  function boot() { document.querySelectorAll("#egm").forEach(init); }
  if (window.document$ && typeof window.document$.subscribe === "function") window.document$.subscribe(boot);
  else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
