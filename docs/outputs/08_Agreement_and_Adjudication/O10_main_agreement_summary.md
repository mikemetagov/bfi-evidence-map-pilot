# Main Coding Agreement Summary (O10, main coding)

Published 19 October 2026 at Gate 4, with GSR's approval of public release. 17 October 2026. Phase C step 1. Protocol v0.5, Section 8.3. Codebook, prompt and schema v1.2. Approver: Michael Cooper.

## What was done

- All inputs were hash-checked before the run: 60 main outputs, 5 retest outputs, coding inputs v1.2, codebook/prompt/schema v1.2 and the 30 frozen packets. All passed.
- `scripts/agreement.py` was run on Coder A (GPT-6 Astra) against Coder B (Gemini 3.8 Flash) for all 30 cases and for the 24 non-calibration cases. The script now also reports outcome-domain presence at L2 or above, as the Gate 3 fix plan requires.
- Coder A's retest outputs were compared with Coder A's main outputs for the same five cases.
- Statistics: percent agreement, Cohen's kappa (quadratic-weighted for ordinal fields), Krippendorff's alpha and Gwet's AC1/AC2, with 95% bootstrap intervals from 2,000 case resamples (seed 20261017). Full results are in `agreement_main_all30.json`, `agreement_main_noncal24.json` and `agreement_retest.json`.

## Agreement between coders

| Core field | Units (30 / 24) | Agreement 30 | κ 30 [95% CI] | Gwet 30 | Agreement 24 | κ 24 [95% CI] | Gwet 24 | Band (κ, 30 cases) |
|---|---|---|---|---|---|---|---|---|
| Use-case domain | 30 / 24 | 97% | 0.96 [0.87, 1.00] | 0.96 (AC1) | 96% | 0.95 [0.83, 1.00] | 0.95 | Good |
| Outcome domain present, any level | 180 / 144 | 84% | 0.68 [0.56, 0.78] | 0.70 (AC1) | 85% | 0.71 [0.59, 0.81] | 0.71 | Acceptable |
| Outcome domain present, L2 or above | 180 / 144 | 82% | 0.61 [0.48, 0.74] | 0.68 (AC1) | 83% | 0.60 [0.45, 0.75] | 0.70 | Below |
| Evidence level (shared domains) | 91 / 67 | 74% | 0.64 [0.43, 0.80] | 0.96 (AC2) | 72% | 0.61 [0.35, 0.79] | 0.96 | Below; under the 0.70 decision metric |
| Stated deployment status | 30 / 24 | 80% | 0.73 [0.52, 0.91] | 0.76 (AC1) | 79% | 0.72 [0.50, 0.93] | 0.75 | Acceptable |
| Blockchain added value | 30 / 24 | 90% | 0.80 [0.59, 1.00] | 0.98 (AC2) | 88% | 0.74 [0.46, 1.00] | 0.97 | Good |
| Objective achievement (ID-paired; invalid, superseded) | 64 / 52 | 47% | 0.36 [0.18, 0.57] | 0.64 (AC2) | 46% | 0.33 [0.13, 0.56] | 0.65 | Below |
| Objective achievement (confirmed pairs, best pair per split; step 3) | 56 / 44 | 52% | 0.42 [0.22, 0.64] | 0.71 (AC2) | 50% | 0.41 [0.21, 0.63] | 0.73 | Below |

Out-of-sample check: the 24 non-calibration cases give results within 0.05 κ of the full 30 on every field, so calibration cases do not inflate agreement.

## What drives the disagreements

128 disagreements across 30 cases (102 in the 24 non-calibration cases).

- **Evidence level is a one-way L1/L2 split.** 21 of 24 level disagreements are Coder A at L1 and Coder B at L2. This is the boundary that v1.1 rules addressed, and it is systematic rather than random. It also explains why L2-or-above presence agrees less well than any-level presence, the reverse of calibration round 2 (κ 0.72).
- **Achievement is also one-way.** 32 of 34 disagreements have Coder B more favourable (for example Unclear against Achieved, or Partly against Achieved).
- **Achievement is invalid as computed.** Step 3 found that objective IDs do not line up across coders. Objectives were paired by ID only (A 69, B 73, 64 paired). Protocol 8.3 requires the adjudicator to match objectives before achievement agreement is final, so this figure will be recomputed after step 3.
- **Recomputed on confirmed pairs (step 3, 17 October).** Michael confirmed 70 objective pairs (41 lexical, 29 from GPT-6 Luna; 1 Luna link rejected): 41 one-to-one and 29 in split/merge groups. Michael chose split option 2: keep one best pair per split group (the lexical pair where one exists, else the highest-confidence Luna pair), giving 56 pairs. κ 0.42 / 0.41 (30 / 24 cases), AC2 0.71 / 0.73. Sensitivity, one-to-one pairs only (41 / 31): κ 0.41 / 0.36, AC2 0.69 / 0.71. Every disagreement has Coder B more favourable (27 of 27). Achievement stays below 0.67. Output: `agreement_achievement_matched_v1.json`; script `scripts/achievement_matched.py`.
- **Gwet AC2 for evidence level (0.96) is much higher than κ.** Quadratic weights over five levels credit adjacent-level disagreements heavily. Report κ as the decision metric and AC2 only as context.

## Test-retest (Coder A, five cases)

Same-model stability is high: use-case domain, status and added value 100%; presence any level κ 0.93; evidence level κ 0.93 (one L1/L2 change in UNI-10); achievement 5 of 10 identical, AC2 0.87. Caveat (deviation 5): the retest ran the same day as main coding, not two days later, so stability may be overstated.

## Implications for Gate 4

- Evidence level misses the 0.70 decision metric (κ 0.64). Because the split is directional, adjudication of the 24 L1/L2 cases may resolve most of it, but the raw figure stands as the reliability result.
- Under protocol 8.3, fields below 0.67 are revised and recoded once, or reported as unreliable and not used to shade the matrix. Michael's plan: finish the pilot as designed and fix the codebook with a fresh calibration after the pilot.
- Matrix shading by L2 or above relies on a field at κ 0.61. Adjudicated codes, not raw codes, should drive the shading.
