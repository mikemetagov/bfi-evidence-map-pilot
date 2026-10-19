# O14 Status Tracing v1.0: Note for Michael

Blockchain for Impact Funding Evidence Map pilot. Phase D step 2, 18 October 2026. Published 19 October 2026 at Gate 4, with GSR's approval of public release.

## What was done

O14 gives each of the 30 cases a traced current status, using only the status signals collected in protocol step 4 (25 documents in `03_Collection/main/status_signals/` and 6 in `calibration/status_signals/`). The protocol 6.3 confidence scale applies: **High** means an explicit source states the status; **Medium** means several indirect signals agree; **Low** means a single indirect signal. The orchestrator (Claude Opus 5.5) assigned the codes after coding was complete, so the coders never saw the signals. There were no new searches, no fetches and no model calls. Every signal hash matches the O5 inventory. `scripts/phaseD/build_o14.py` writes the table and fills `deployment_status_traced` in O12 and in site staging, plus `status_confidence` in staging. The build stops if any other column changes. With the staging files in place, the site build passes. Stated status stays exactly as coded.

## Tracing rules applied (for approval)

- **T1:** An explicit dated statement about the use case, or about the organisation closing, gives that status at High confidence.
- **T2:** Signals of further phases, deployments or new clients give Extended pilot or Scaled under codebook S1. Several agreeing signals give Medium; one signal gives Low (the codebook growth example).
- **T3:** Signals showing only that the organisation or a product is still active give Unknown. Applies when they do not show the funded blockchain solution in wider use (S1: "ongoing activity … Unknown, with a note"). The activity is recorded in `activity_signal`.
- **T4:** Signals from the pilot period, or about a different product, are not used for the trace. The case is Unknown.
- **T5:** No signal held: Unknown, with confidence left blank.

## Results

| Traced status | Cases | Confidence |
|---|---|---|
| Discontinued | 1 (MCV-16, Haraka wound down in March 2026) | High |
| Pilot | 1 (FIL-05, "upcoming 2026") | High |
| Extended pilot | 2 (FIL-03; MCV-02) | Medium; Low |
| Scaled | 5 (UNI-10; GSR-02, UNI-03, UNI-08, UNI-15) | Medium; Low ×4 |
| Unknown | 21 (T3 ×11, T4 ×5, T5 ×5) | blank |

**Metric 4 was 4 of 30 (13%) against the 75% target before Michael's review (now 3 of 30; see below).** It is 3 of 24 for the non-calibration cases. The traced status matches the stated status in 9 cases. Four stated Scaled cases trace to Unknown, and none traces to Handed over. The shortfall comes from the collection design: one step-4 search per case, about one document per case, and five cases with no signal at all (MCV-01, MCV-03, MCV-12, MCV-24, UNI-12). Rule choice cannot fix this. Moving T3 cases to Low-confidence codes would change the status mix, but not metric 4.

## What to check first

17 codes are marked `Check first` in `O14_status_tracing_v1.0.csv`; Michael reviews all 30 under L5. The most open calls are:

- FIL-05: "upcoming" coded as Pilot.
- FIL-03: Medium confidence, but all signals come from one ledger.
- UNI-03: the article may repeat older text.
- MCV-06 and UNI-16: product live, but the site does not mention blockchain.
- MCV-11: matches lesson S9, but the S9 source is excluded.

Record decisions in `michael_decision` / `michael_note`, then rerun the build after any edit to `o14_codes_v1.0.json`.

## Decisions (Michael, 18 October 2026)

1. Rules T1–T5 approved, including T3.
2. Metric 4: 13% is reported as a pilot finding. No extra status search. After pilot completion, partners do written spot checks on their own cases (deviation 8). Results go in a labelled addendum, and the pilot figure stays.
3. MCV-11: the pre-draw MCV blog is not added. MCV-11 stays Unknown, and the findings will not describe it as a failure case. Of the seven cases drawn for the failure quota, only MCV-16 traces to Discontinued.

## Code-by-code review (Michael, 19 October 2026): closed

Michael reviewed all 30 rows as coder of record (deviation 7), working from numbered tables with one question per row: 26 codes confirmed, 4 changed. His answers are in `scripts/phaseD/o14_michael_decisions_v1.0.json`, and the original proposals are kept in `o14_codes_v1.0.json` and in the `proposed_*` columns of the table. The build reads the decision file.

| Row | Case | Proposed | Final |
|---|---|---|---|
| 1 | FIL-05 | Pilot, High (T1) | Unknown (T3) |
| 6 | UNI-15 | Scaled, Low (T2) | Unknown (T3) |
| 7 | MCV-02 | Extended pilot, Low (T2) | Unknown (T4) |
| 14 | FIL-02 | Unknown (T3) | Extended pilot, Low (T2) |

The orchestrator assigned the rules for the changed rows (T3 for FIL-05 and UNI-15; T4 for MCV-02, as an undated signal that may predate the packet); Michael to confirm. Row 10 (MCV-11): Unknown confirmed, and failure-case wording is not approved.

**Final result: Unknown 23, Scaled 4, Extended pilot 2, Discontinued 1. Metric 4: 3 of 30 (10%), 2 of 24 non-calibration.** Traced matches stated in 7 of 30. The O13 register changed only in its `traced_status_O14` column (22 rows); no claim status changed. V3 was redrawn, with the banner now "DRAFT: pre-Gate 4".

## Decisions as first posed

1. Approve rules T1–T5, especially T3 (activity alone gives Unknown).
2. Metric 4. **(a)** Report 13% as a pilot finding and carry partner-supplied status (A11 item 7) and T3 interviews into the full scope. **(b)** Ask MCV, UNICEF, FIL and GSR for post-funding status on the 30 cases before Gate 4. **(c)** Run a bounded extra status search. That would be a new deviation (at most 2 searches for each of 21 cases means about 42 searches, in checkpoints of 6). Recommendation: (a), plus (b) if partners can reply before Gate 4.
3. MCV-11: should the 2026 MCV blog found in the pre-draw check be added as a documented status signal? That needs one fetch. Protocol 6.3 bars the check result itself as the status code, not the document.
