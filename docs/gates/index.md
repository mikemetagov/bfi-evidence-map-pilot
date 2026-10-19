# Gates and deviations

Output O18. Record every gate decision and every departure from the design.

## Gate log

| Gate | Date | Decision | Approver | Evidence | Notes |
|---|---|---|---|---|---|
| G0 Design | Recorded 2026-10-16 | Approved | GSR | GSR approval of v0.1 | v0.1 submitted 2026-10-09; posted publicly |
| G1 Sample and definitions | 2026-10-16 | Passed. Parameters set (protocol v0.4, Section 5.5); GSR confirmed the pilot and deployment definitions | Michael; GSR (definitions) | Protocol v0.4; O2 and O3 (restricted); GSR confirmation 2026-10-16 | 30 cases: 11 MCV, 11 UNICEF, 5 Filecoin, 3 GSR; seed 20261016; GSR high-richness quota shortfall explained |
| G2 Codebook v1.0, prompts, models | 2026-10-16 | Passed. Codebook v1.0 frozen after a dry run on one case outside the sample; prompt, output schema and model register set | Michael | Dry-run report and frozen files (restricted) | Schema valid 2/2; 53 quotes verified, 0 failures; 5 dry-run disagreements fixed by rules before freezing (v1.0-12 to 16) |
| G3 Calibration | 2026-10-17 | Passed with approved fix plan. Codebook v1.1 approved and v1.2 set for main coding; Coder B kept as Gemini 3.8 Flash (limitation disclosed); cost limits adopted (protocol v0.5) | Michael | O10 calibration summary; codebook v1.2; protocol v0.5 | 3 of 6 core fields at or above κ 0.67; fix plan covers presence (two thresholds), stated status (human review) and achievement (automatic flag, AC2) |
| G4 Dataset and draft map | – | – | Michael | – | – |
| G5 Findings and decision | – | – | GSR and Metagov | – | – |

## Deviations from the design

| # | Date | Section | Deviation | Reason | Effect | Approved by |
|---|---|---|---|---|---|---|
| 1 | 2026-10-16 | Annex A (A7, new A10, new A11) | Added participatory milestones, data management terms and an itemised data request for the full scope (v0.3) | Partners need defined protections and a clear data request before agreements | Full scope only; pilot unchanged | Michael Cooper |
| 2 | 2026-10-16 | 5.3 and 6.3 | Added a one-search pre-draw status check per eligible case to set status strata | Portfolio pages alone did not show which cases had stalled, so the failure quota could not be applied reliably | Sampling aid only; results kept out of evidence packets; formal status tracing still after coding | Michael Cooper |
| 3 | 2026-10-17 | 6.1 (step 5) | Backward-citation check not run for the six calibration packets | Calibration was run on the first available packets so the codebook could be tested quickly | Calibration packets may be thinner; step 5 runs for all 30 cases in main collection, and new documents are added to the main-coding packets only | Michael Cooper |
| 4 | 2026-10-17 | 5.5, 6.1, 6.2, 8.1 | Search cap reduced from 12 to 6; packets limited to 6 documents and about 30,000 characters; documents selected by fixed rules, not a model; step 5 only where a report has references; coding in batched sessions of about 10 cases | Credit and time limits set by Michael; calibration needed 4–5 searches per case | Possible small loss of coverage, monitored through metric 2 and the lessons log | Michael Cooper |
| 9 | 2026-10-19 | Summary, 2.2, 5.4, 7.4, 9.2, 9.3, 14 and Annex A (protocol v0.1–v0.5); Purpose and Use Memo section 8; one-pager | Pilot metric 5 (effort per case, 2 hours or less) removed from all materials, and effort timing dropped. Decision rule changed from at least four of five threshold metrics to at least three of four. Former metrics 6 and 7 renumbered 5 and 6. Dated protocol files v0.1–v0.5, the memo and the one-pager edited in place, with an amendment note | Michael judged the metric not important for the scale-up decision | Under either rule the pilot currently meets 2 of 4 threshold metrics, so the outcome is unchanged. The full-study budget can no longer be re-estimated from measured pilot hours (Annex A v0.6 F1a) | Michael; GSR approved |
