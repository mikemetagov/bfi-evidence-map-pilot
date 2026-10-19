# Changelog

## 2026-10-19 – EPPI-Mapper map published
- The [EPPI-Mapper version](map/eppi.md) of the map is now live, built from the published pilot data (113 records, 30 cases). It uses the same plain evidence names and colours as the evidence spectrum; the codes L1 to L5 stay in the data descriptions.
- `scripts/build_eppi_map.py` and the saved setup in `map-config/` rebuild the page on every update, so it stays in step with the interactive map.

## 2026-10-19 – Plain-language evidence spectrum
- The map, visuals and methods pages now use plain names for the five evidence levels: claims only, operational data, outcomes without comparison, outcomes with comparison, and proven impact. The codes L1 to L5 stay in the protocol, codebook and data files; the [methods page](methods/index.md#evidence-spectrum) shows how the two match.
- New evidence-spectrum explainer and "three things to know" on the [map](map/index.md) and [visuals](visuals/index.md) pages. Technical notes moved into collapsible boxes.
- Map and charts now share one colour scale, light (weaker) to dark (stronger). In both, "gap" marks a cell with no evidence.
- Visuals reissued as v1.1: same data, plain labels, question titles. The v1.0 images are kept.
- "Ask the map" v0.5 answers with the plain names, gives the protocol code in brackets, and understands either form. It passed the frozen test set again (35 of 35).
- "Ask the map" is now also on the [map page](map/index.md#ask-the-map), below the interactive map.
- Removed the statement that partners will fact-check their own cases during full-study preparation. Partner review is now covered in the partner memos.

## 2026-10-19 – "Ask the map" launched (code-only)
- New page [Ask the map](assistant/index.md): answers questions about the 30 pilot cases with cited sources. The tested answering code runs in the browser; no AI model and no server are used, and questions are not logged. It passed the frozen 35-question test set in code-only mode (35 of 35), and the browser answers match the tested code exactly.

## 2026-10-19 – Gate 4 passed; pilot dataset published
- Gate 4 note approved by Michael: 2 of 4 threshold metrics met (agreement κ 0.64, not met; public-source coverage 30 of 30, met; taxonomy fit 2 of 30, met; status confirmed 3 of 30, not met). Recommendation: codebook v1.3 and a fresh calibration round before scaling.
- Published with GSR's approval of public release (partners approved publication and will fact-check their own cases during full-scale preparation): O3 sample and plan; O5 search logs and document inventories; O10 main agreement summary and G3 calibration report; O12 final dataset, data dictionary and non-core differences; O13 claims register and notes; O14 status tracing; O15 visuals V1–V3 and V5; O16 method lessons log; the Gate 4 note. The map now shows the 30 pilot cases.
- Quotes are cut to 25 words, with SHA-256 hashes of the full quote. Evidence packets, status-signal texts, raw coder outputs and adjudication and audit sheets are not published.
- Gate log: Gate 4 row; deviations 5–8 added.

## 2026-10-17 – Correction: conflict-of-interest statement removed
- An erroneous statement that the research lead had previously worked with the UNICEF Venture Fund, and the related double human-audit rate for UNICEF cases, were removed from every version of the protocol (v0.1–v0.5, Section 13). Section 13 now reads "Conflict of interest: none declared". The human audit rate is the same for every portfolio. No audit had been drawn, so no pilot results are affected. The declared-interest flag for cases where GSR is itself the donor is unchanged.

## 2026-10-17 – Gate 3 passed; protocol v0.5
- Gate 3 passed with the approved fix plan. Codebook v1.2 (v1.1 plus two worked status examples) is frozen for main coding, with prompt and schema v1.2.
- Protocol v0.5 records the fix plan and the cost limits on collection and coding. Deviation added for the cost limits.

## 2026-10-17 – Gate 3 calibration results
- Two calibration rounds on six cases (codebook v1.0, then v1.1). Posted codebook v1.1 (tested; pending approval) with change log entries v1.1-17 to v1.1-23, coder prompt and schema v1.1, `scripts/agreement.py`, and the O10 calibration agreement summary.
- Gate log: G3 results submitted with a proposed fix plan. Deviation added for collection step 5 on the calibration packets.

## 2026-10-17 – Codebook v1.0 and coding method posted
- Posted codebook v1.0, its change log and hash manifest (O7), the coder prompt, output schema and model register (O8), and `scripts/check_coder_output.py`. `data/codebook.csv` now holds the v1.0 values. Case-level materials stay restricted.

## 2026-10-16 – Gate 2 passed
- Codebook v1.0 frozen, with the coder prompt, output schema and model register (Coder A GPT-6 Astra; Coder B Gemini 3.8 Flash). The dry run on one case outside the sample passed all Gate 2 criteria.

## 2026-10-16 – Gate 1 passed
- GSR confirmed the pilot and deployment definitions in protocol v0.4, Section 5.5. Gate 1 (sample and definitions) is passed.

## 2026-10-16 – protocol v0.4 (Gate 1 parameters)
- Posted protocol v0.4. New Section 5.5 records the Gate 1 definitions, eligibility rulings, allocation (11 MCV, 11 UNICEF, 5 Filecoin, 3 GSR), random seed, quota results and the search cap of 12. Related updates in Sections 1, 5.1–5.3, 6.1, 6.3 and 13. Definitions await GSR confirmation.
- Gate log: G1 parameters recorded; deviation added for the pre-draw status check.

## 2026-10-16 – protocol v0.3 and open licence
- Posted protocol v0.3: pilot unchanged; Annex A adds participatory milestones (A7), data management, security and privacy (A10) and an itemised data request (A11). v0.2 (an interim draft of A10) is superseded and not posted.
- Added the open licence: CC BY 4.0 for content and data, MIT for code and prompts.

## 2026-10-16 – protocol approved and published
- GSR approved the pilot design v0.1 at Gate 0. The repository was made public as the protocol site. Restricted working outputs moved to a separate private workspace.

## 2026-10-16 – workspace created
- Repository set up with the protocol (O1 v0.1), the outputs register, draft codebook v0.1 and an empty evidence map.
