/* "Ask the map", code-only version (option 4, phase 1).
   Runs the tested answering code (assistant/ask.py v0.4, unchanged) in the browser with Pyodide.
   No model, no server, nothing logged. Files are in docs/assistant/files/. */
(function () {
  const PYODIDE = "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/";
  const EXAMPLES = [
    "How many cases have a traced status of Scaled?",
    "Which cases have outcome evidence or stronger?",
    "Tell me about MCV-02.",
    "Is there any evidence on climate and natural assets?",
    "What does operational data mean?",
    "How were the cases coded?",
  ];
  const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  function inline(s) {
    let t = esc(s);
    t = t.replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, (m, a, u) => `<a href="${u}" target="_blank" rel="noopener">${a}</a>`);
    t = t.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    return t;
  }
  function md(text) {
    const lines = text.split("\n").filter((l) => !l.startsWith("**Question:**"));
    let html = "", list = 0;
    const close = (to) => { while (list > to) { html += "</ul>"; list--; } };
    for (const raw of lines) {
      const m = raw.match(/^(\s*)- (.*)$/);
      if (m) {
        const depth = m[1].length >= 2 && list >= 1 ? 2 : 1;
        while (list < depth) { html += "<ul>"; list++; }
        close(depth);
        html += `<li>${inline(m[2])}</li>`;
        continue;
      }
      close(0);
      if (!raw.trim()) continue;
      if (/^Route: /.test(raw) || /^Check note: /.test(raw)) html += `<p class="atm-meta">${inline(raw)}</p>`;
      else html += `<p>${inline(raw)}</p>`;
    }
    close(0);
    return html;
  }
  function el(tag, cls, html) { const n = document.createElement(tag); if (cls) n.className = cls; if (html !== undefined) n.innerHTML = html; return n; }

  let ready = null;
  function loadScript(src) {
    return new Promise((res, rej) => { const s = document.createElement("script"); s.src = src; s.onload = res; s.onerror = () => rej(new Error("load " + src)); document.head.append(s); });
  }
  async function boot(base) {
    if (!window.loadPyodide) await loadScript(PYODIDE + "pyodide.js");
    const py = await window.loadPyodide({ indexURL: PYODIDE });
    py.FS.mkdirTree("/atm/corpus");
    for (const f of ["ask.py", "corpus/map.json", "corpus/chunks.jsonl", "corpus/manifest.json"]) {
      const r = await fetch(base + f, { cache: "no-store" });
      if (!r.ok) throw new Error(f + " " + r.status);
      py.FS.writeFile("/atm/" + f, await r.text());
    }
    // prepare() also builds the (unused) model request, which reads the system prompt; the code-only
    // version never calls a model, so a placeholder stands in and the prompt is not published.
    py.FS.mkdirTree("/atm/prompts");
    py.FS.writeFile("/atm/prompts/system_v0.2.md", "(Not used: code-only version, no model call.)");
    py.FS.writeFile("/atm/answer_schema_v0.2.json", "{}");
    py.runPython("import sys\nsys.path.insert(0, '/atm')\nimport ask");
    return py;
  }
  function answer(py, q) {
    py.globals.set("atm_q", q);
    return py.runPython("p = ask.prepare(atm_q)\nask.finish(p, None)[0] if p['model_needed'] else p['answer']");
  }

  function init(root) {
    if (root.dataset.ready) return;
    root.dataset.ready = "1";
    const base = root.dataset.base || "files/";
    const form = el("form", "atm-form");
    form.innerHTML = '<label class="atm-label" for="atm-q">Your question</label>' +
      '<div class="atm-row"><input id="atm-q" class="atm-input" type="text" maxlength="500" autocomplete="off" placeholder="For example: which cases are in Kenya?">' +
      '<button class="atm-btn md-button md-button--primary" type="submit">Ask</button></div>';
    const chips = el("div", "atm-chips");
    chips.append(el("span", "atm-chips-label", "Try:"));
    for (const ex of EXAMPLES) {
      const b = el("button", "atm-chip"); b.type = "button"; b.textContent = ex;
      b.addEventListener("click", () => { input.value = ex; form.requestSubmit(); });
      chips.append(b);
    }
    const status = el("p", "atm-status"); status.setAttribute("role", "status"); status.setAttribute("aria-live", "polite");
    const log = el("div", "atm-log"); log.setAttribute("aria-live", "polite");
    root.append(form, chips, status, log);
    const input = form.querySelector("input"), btn = form.querySelector("button");
    root.atmAsk = async (q) => { if (!ready) ready = boot(base); return answer(await ready, q); };  // used by the parity test

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const q = input.value.trim();
      if (!q) { input.focus(); return; }
      btn.disabled = true;
      try {
        if (!ready) { status.textContent = "Loading the answering code (first question only, a few seconds)…"; ready = boot(base); }
        const py = await ready;
        status.textContent = "";
        const item = el("article", "atm-item");
        item.append(el("p", "atm-q", "<strong>Q:</strong> " + esc(q)));
        item.append(el("div", "atm-a", md(answer(py, q))));
        log.prepend(item);
        input.value = "";
      } catch (err) {
        ready = null;
        status.textContent = "The answering code could not be loaded. Check your connection and try again.";
        console.error(err);
      } finally { btn.disabled = false; input.focus(); }
    });
  }
  const start = () => document.querySelectorAll("#atm").forEach(init);
  if (window.document$ && window.document$.subscribe) window.document$.subscribe(start);
  else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
