# O13 Claims Register: Note v1.1 (decisions recorded)

Blockchain for Impact Funding Evidence Map pilot. Phase D step 3, 19 October 2026 (amended the same day with Michael's follow-up decisions and rule approval). Published 19 October 2026 at Gate 4, with GSR's approval of public release. Replaces note v1.0 for results; v1.0 keeps the rules (R1, R2, V1–V6) and the build description.

## What was done

Michael decided the 45 Decide rows (32 coder-flagged conflicts under V5, 7 partial figure matches under V3, 6 word-overlap matches under V4) and the 11 Check rows. He worked from 56 decision cards in five batches (`O13_decision_cards_v1.0.md`, restricted; built by `scripts/phaseD/o13_decision_cards.py`). The orchestrator proposed no status for these rows. V5 cards were grouped only by mechanical pattern: 3 later-dated source with larger figure, 6 different unit or population wording, 22 dates missing, 1 other (no same-date pairs). His answers are in `O13_michael_answers_v1.0.csv` and were written into `michael_status` and `michael_note` by `o13_record_answers.py`. `build_o13.py` and `build_visuals.py` were rerun; no searches, fetches or model calls. Checks passed: 167 rows, no blank status among the 56 rows, and the register, V5 table and summary JSON agree.

Status definitions applied (Michael, 19 October): **Corroborated**, another held source with a different producer reports the same result; **Consistent**, another held source agrees but has the same producer or unclear independence, or the difference is explained by period, scope or rounding; **Contradicted**, another held source reports a different value for the same quantity, population and period, or says the result did not happen; **Unverifiable**, no held source addresses the claim, or the "conflicting" figure measures something else.

## Results

| Status | All 167 | Both-coder rows (72) | 56 decided rows |
|---|---|---|---|
| Corroborated | 0 | 0 | 0 |
| Consistent | 53 | 21 | 53 |
| Contradicted | 0 | 0 | 0 |
| Unverifiable | 114 | 51 | 3 (MCV-01-C01, MCV-01-C06, MCV-16-C04) |

- **Metric 6, claims that held up (Corroborated or Consistent):**
  - (a) Held up as a share of all claims: **53 of 167 (32%)**.
  - (b) Held up against contradicted, among rated claims: **53 of 53 (100%)**.
  - Unverifiable alongside: **114 of 167 (68%)**.
  - No claim is Corroborated: no held source from a different producer was judged to confirm any result.
- **Both-coder sensitivity:** (a) 21 of 72 (29%); (b) 21 of 21 (100%); unverifiable 51 of 72 (71%). Non-calibration cases only: 41 of 133 (31%).
- **Coder-flagged conflicts (V5, 32 rows):** 30 Consistent, 2 Unverifiable, none Contradicted. Even the opposite descriptions (UNI-12-C05/C08, custodial versus non-custodial) and the UNI-07 cessation claim were judged Consistent.
- **Changes from proposed status (4):** the four V1 Corroborated rows (MCV-01-C02, C03, C04; MCV-05-C01) became Consistent. The proposed status for MCV-16-C04 (Unverifiable) stands.

## Rule exceptions and method notes

1. **MCV-16-C04 (resolved).** First rated Consistent, although no other held source addresses the claim. Michael changed it to Unverifiable (follow-up 1), so no exception remains.
2. **BitcoinKE support (resolved).** BitcoinKE (S04) supports MCV-05-C01, C03 and C08. Michael rated all three Consistent (follow-up 2).
3. **Override of V1 proposals.** For MCV-01-C02 to C04, the support (TechCrunch) is coded Independent but quotes MCV's statement. Michael rated these rows Consistent; the reason is not recorded.
4. **Cards 13, 15, 17 and 18 (MCV-05-C02, C07; MCV-06-C03, C07).** First answered Corroborated, then changed to Consistent to follow the definition (same producer). Not an exception.
5. **V1 compares producer types, not organisations.** Exame and Livecoins are both coded Independent, so V1 treated them as the same producer (UNI-18).
6. **Passages and the figure parser.** On two cards (MCV-06-C03, UNI-07-C05), the overlap pick missed the point, so a passage was added by keyword search of the same flagged source; it is marked in the cards. The R2 parser misses split or written-out figures ("$9, 697", "51,8339", "Ninety-six percent").

## Decisions recorded and remaining open

1. Recorded (19 October): MCV-16-C04 is Unverifiable; MCV-05-C03 and C08 are Consistent.
2. Recorded (19 October, note v1.0, decision 6): the 25-word quote limit is confirmed, and the coders' model-written claim summaries may be published.
3. Adopted by Michael's instruction of 19 October: register unit of 167 rows with the both-coder sensitivity; metric 6 reported both ways; no searches.
4. Recorded (19 October, note v1.0, decision 2, option 2): R2 and V1–V6 are approved after a local recheck. `o13_v6_recheck.py` reran the 111 Routine V6 rows with numbers cleaned (split thousands, decimal commas, numbers in words, non-breaking-space thousands); there were no searches or model calls. A control run without cleaning reproduced the build. With cleaning, the matcher found the matches it had missed on decided rows MCV-05-C03/C08 and UNI-18-C01/C05. **No Routine row left V6** (figures changed on 3 rows, none matched), so no new cards and no status change. Number cleaning and organisation-level producer comparison in V1 move to codebook v1.3. Files: `O13_v6_recheck_v1.0.csv`, `O13_v6_recheck_cards_v1.0.md`.
5. Recorded (19 October): Michael checked the 111 Routine V6 rows using `O13_v6_review_cards_v1.0.md` (built by `o13_v6_review_cards.py`; restricted). He reviewed all 111 card by card and kept all 111 Unverifiable. His statuses are in `O13_michael_answers_v6_v1.0.csv` and in the register, so every one of the 167 rows now carries `michael_status`.
6. **Open, outside O13:** the O14 code-by-code review. V3 and V5 keep a draft banner until Gate 4, and Gate 4 has not passed.
