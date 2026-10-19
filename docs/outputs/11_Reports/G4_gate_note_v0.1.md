# Gate 4 Review Note (draft v0.1)

Blockchain for Impact Funding Evidence Map pilot. Phase D step 7, 19 October 2026. **Approved by Michael, 19 October 2026 (as drafted). Published 19 October 2026 at Gate 4, with GSR's approval of public release.**

## Decision rule

The full map proceeds if at least three of the four threshold metrics are met, and the method fixes need no redesign of the taxonomy or evidence scale (protocol v0.5, section 9.2, as amended by deviation 9). GSR has final authority.

## Threshold metrics

| Metric | Threshold | Pilot result | Met? |
|---|---|---|---|
| 1. Agreement between the two models (weighted κ, evidence level) | ≥ 0.70 | 0.64 (95% CI 0.43–0.80), 30 cases; 0.61 on the 24 non-calibration cases | No |
| 2. Public-source coverage (cases with no core field coded "insufficient information") | ≥ 80% | 30 of 30 on final codes (100%). Coder A flagged one core field, UNI-18 stated status, so the per-coder result is 29 of 30 (97%); Coder B flagged none | Yes |
| 3. Taxonomy fit (cases coded "none fits") | ≤ 10% | 2 of 30 (7%): UNI-04 and UNI-18 | Yes |
| 4. Post-pilot status confirmed (Medium or High confidence) | ≥ 75% | 3 of 30 (10%); 2 of 24 non-calibration | No |

**Result: 2 of 4 thresholds met. The decision rule for proceeding is not met.** Metric 2 measures whether a case could be coded at all; it does not mean the evidence is strong. 60 of 113 outcome cells are claim-only (L1), no case reaches L4 or L5, and 24 of 56 objective pairs are rated Unclear on achievement. Metric 4 reflects the collection design (about one status document per case, none for five cases). After Michael's O14 review on 19 October (26 codes confirmed, 4 changed), the result fell from 4 of 30 to 3 of 30.

On the second condition, the planned fixes are a codebook revision (v1.3) and a fresh calibration round. Neither changes the six domains or the five-level scale. Whether connectivity cases (lesson S10, rule D5) need a new domain is still open.

## Reported findings (no thresholds)

- **Claims that held up (metric 6):** 53 of 167 register claims (32%) are Consistent; none is Contradicted; 114 (68%) cannot be verified from held sources.
- **Other reliability results:** L2+ presence κ 0.61 and matched achievement κ 0.42 (AC2 0.71) are below 0.67. The audit of agreed fields found 92 of 92 matching (100%). It tests the agreed codes, not the disagreements.

## "Ask the map" assistant test (step 6)

On the frozen 35-question set (17 GPT-6 Luna calls, no searches or fetches), all three targets were met. Count accuracy was 9 of 9 (100%), 85 of 86 claims were supported (98.8%) and 10 of 10 out-of-scope requests were refused (100%). Two caveats apply:

1. **T16 is wrong.** It says all 30 cases were coded blind; only the six calibration cases were recoded blind. The checker cannot catch this kind of extended claim, so method answers need human spot checks or a quote-match check before launch.
2. **Six answers were phrased under prompt v0.1**, not v0.2 (S3, T09, T10, T13, T17, T18; same context as v0.2). The live assistant must use GPT-6 Luna with prompt v0.2, or step 6 is rerun.

The O14 review changed one tested count, T05 (traced Scaled), from 5 to 4. The corpus must be rebuilt, and T05 re-checked by code, before launch.

## Map-filter gaps (decision D1)

Coder differences on non-core fields were not adjudicated. They stay blank for the pilot and are fixed in codebook v1.3. On the map, **21 of 30 cases have at least one blank filter field (37 blanks)**, and filtering on that field leaves those cases out:

- **Country (5):** FIL-01, UNI-03, UNI-07, UNI-10, UNI-12
- **Region (4):** FIL-01, GSR-03, UNI-03, UNI-10
- **Year launched (9):** FIL-01, FIL-05, MCV-18, UNI-03, UNI-08, UNI-12, UNI-13, UNI-15, UNI-18
- **Blockchain functions (12):** FIL-03, FIL-04, GSR-03, MCV-02, MCV-03, MCV-12, MCV-24, UNI-04, UNI-07, UNI-08, UNI-12, UNI-13
- **Implementation model (7):** FIL-02, FIL-03, FIL-04, FIL-05, GSR-03, MCV-03, MCV-11

Population groups, reach and funding model also differ (61 rows), but they are not map filters.

## Recommendation

Under the decision rule as written, do not proceed straight to full scale. Complete codebook v1.3 and calibrate on 20–30 fresh cases. Add partner-supplied status (deviation 8 spot checks; A11 item 7) to address metric 4. Then re-judge metrics 1 and 4 before GSR decides.

## Before publishing

Confirmed by Michael (19 October 2026): (a) the O16 findings memo is covered by GSR's public-release approval; (b) the publish includes source lists, URLs, hashes and quotes of 25 words or fewer, not the full third-party text in packets and status signals. The publish leaves out restricted files, including the O13 review sheet, the decision cards and the evidence packets.
