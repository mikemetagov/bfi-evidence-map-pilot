# Gate 3 Calibration Agreement Summary (O10, calibration)

Public summary. Case-level codes, quotes and disagreements are restricted to GSR and Metagov. 17 October 2026. Protocol v0.4, Sections 8.2–8.3. Approver: Michael Cooper.

## What was done

1. **Collection** (protocol 6.1) for the six calibration cases (one per portfolio, plus two more drawn at random).
   - 4–5 logged searches per case, against a cap of 12.
   - 25 evidence documents frozen into packets, each with a SHA-256 hash.
   - 8 status-signal documents held outside the packets for later status tracing (O14).
2. **Round 1:** both coders coded the six cases under codebook v1.0.
3. **Error analysis:** each disagreement was sorted by cause.
4. **Codebook v1.1:** seven rule changes (v1.1-17 to v1.1-23) and a completeness check added to the prompt.
5. **Round 2:** both coders, in new sessions, recoded the six cases under v1.1.

Every output passed schema validation. All 623 quotes across both rounds were verified, with 0 failures and no fabricated quotes.

## Agreement on core fields

Six cases is a very small sample, so the confidence intervals are wide. Kappa can be low even when percent agreement is high if one value dominates (the prevalence effect); AC1 and AC2 are less affected by this. The intervals in the table are 95% bootstrap intervals from resampling cases.

| Core field | Units (R1 / R2) | R1 agreement | R1 κ | R2 agreement | R2 κ [95% CI] | R2 α | R2 Gwet | κ ≥ 0.67 after revision |
|---|---|---|---|---|---|---|---|---|
| Use-case domain | 6 / 6 | 100% | 1.00 | 100% | 1.00 [1.00, 1.00] | 1.00 | 1.00 (AC1) | Yes |
| Outcome domains present (any level) | 36 / 36 | 64% | 0.20 | 75% | 0.39 [0.11, 0.57] | 0.36 | 0.59 (AC1) | No |
| Evidence level (per shared domain) | 20 / 22 | 65% | 0.54 | 82% | 0.77 [0.26, 1.00] | 0.77 | 0.98 (AC2) | Yes |
| Stated deployment status | 6 / 6 | 67% | 0.46 | 67% | 0.52 [0.00, 1.00] | 0.53 | 0.51 (AC1) | No |
| Blockchain added value | 6 / 6 | 83% | 0.57 | 100% | 1.00 [1.00, 1.00] | 1.00 | 1.00 (AC2) | Yes |
| Objective achievement | 10 / 10 | 70% | 0.40 | 70% | 0.05 [−0.07, 0.27] | −0.06 | 0.78 (AC2) | No |

Supplementary measure: outcome domains present at L2 or above (domains with result data, not just claims). Round 1 agreement 81%, κ 0.61; round 2 agreement 86%, κ 0.72.

## Causes of disagreement

| Cause | Round 1 | Round 2 |
|---|---|---|
| Codebook ambiguity | 22 | 6 (status boundary, L1 versus L2, placement) |
| Claim-only (L1) domain coded by one coder only | – | 7 |
| Other omission by one coder | 2 | 2 |
| Rule not applied by one coder | – | 3 |
| Misreading | 1 | 0 |
| Genuine judgement | 1 | 0 |
| Fabricated quote | 0 | 0 |
| Total | 26 | 18 |

## Status

Evidence level, added value and use-case domain are at or above κ 0.67 after revision. Outcome-domain presence (any level), stated deployment status and objective achievement are below it.

Gate 3 passes on "an approved fix plan" when fields remain below 0.67. The proposed fix plan has five parts:

- Report presence agreement at two thresholds: any level, and L2 or above, where agreement is κ 0.72.
- Shade the evidence matrix by L2-or-above evidence only.
- Have a human review every stated-status code.
- Flag automatically any achievement code that has no result at L2 or above.
- Report AC2 alongside kappa.

The decision is recorded in the gate log.
