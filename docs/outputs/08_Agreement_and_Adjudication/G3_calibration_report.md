# Gate 3 Calibration Report

Published 19 October 2026 at Gate 4, with GSR's approval of public release. 17 October 2026. Protocol v0.4, Sections 8.2–8.3. Approver: Michael Cooper.

## What was done

1. **Collection** (protocol 6.1) for the six calibration cases: MCV-01, UNI-15, FIL-01, GSR-01, MCV-16 and MCV-02.
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

## Error analysis

### Round 1 (26 disagreements)

| Cause | Count | Where | Fix in v1.1 |
|---|---|---|---|
| Codebook ambiguity | 22 | 11 outcome-presence cases (testimonials, purpose statements, sector risk commentary, claim-only statements); 7 evidence-level cases (testimonials, unquantified results, recipients versus non-recipients counted as L4, where coverage belongs); 2 deployment status; 2 objective achievement (achievement credited from a description) | E6, E7, O2, O3, the F limit, S1 and A1 |
| Omission by one coder | 2 | Coder B left out reach (domain B) in GSR-01 and MCV-02 | Completeness check in the prompt |
| Misreading | 1 | GSR-01: a fee figure with no alternative scored as a comparison (added value 2) | V2 |
| Genuine judgement | 1 | UNI-15: the coders extracted different second objectives | Adjudicator matches objectives |
| Fabricated quote | 0 | – | – |

### Round 2 (18 disagreements)

| Cause | Count | Detail |
|---|---|---|
| L1-only domain left out by Coder B | 7 | Coder A coded a domain at L1 from a testimonial or an unquantified claim, as E6 requires. Coder B left it out. With L2 or above as the threshold, presence agreement is κ 0.72 |
| Other presence differences | 2 | MCV-02: Coder B left out a survey result in domain F ("97% … not burdensome", L3). GSR-01: Coder B coded a claim in domain D that Coder A treated as a purpose statement (O2) |
| L1 versus L2, or placement of an operational statement | 4 | UNI-15: "real-time reconciliation and full transparency" (C), and a testimonial against a count of 43 households (E). FIL-01: "archiving 10,000 web pages", placed in B by one coder and C by the other |
| Rule A1 not applied by Coder B | 3 | Coder B coded Achieved where the support was a launch statement, a framework description or a count of live campaigns. Coder A coded Unclear, as A1 requires |
| Deployment-status boundary | 2 | UNI-15: three humanitarian projects with different partners (A Scaled, B Extended pilot). MCV-16: phase one of two (A Pilot, B Extended pilot). Under S1, the correct codes are Scaled and Extended pilot, so each coder was right once |
| Fabricated quote | 0 | – |

### Interpretation

The revision worked where the rules were the problem: evidence level, added value and domain are now at or above the threshold. The remaining disagreement has a different character:

- It is concentrated in claim-only (L1) cells, in the stated-status boundary, and in Coder B not applying rule A1.
- It is mostly one-directional: in 8 of the 9 presence disagreements, Coder B left out a domain; in all 3 achievement disagreements, Coder B credited achievement.
- That pattern fits the capability gap between the coders (lessons log K2) better than unclear rules.

A third round on the same six cases would mainly retest Coder B, and six cases are too few to separate the two explanations.

## Proposed decisions for Gate 3

The protocol's pass rule is "no core field below 0.67 after revision, or an approved fix plan". Three fields are below 0.67, so I recommend passing Gate 3 with the fix plan below rather than running a third round.

1. **Approve codebook v1.1 as tested, plus a v1.2 clarification for main coding.**
   - S1 gets two worked examples: "phase one of two is Extended pilot" and "projects for several partners is Scaled".
   - Nothing else changes.
2. **Fix plan: outcome domains present.**
   - Report agreement at two thresholds: any level, and L2 or above.
   - The evidence matrix (V1) is shaded only by L2-or-above evidence. Claim-only cells are marked "claims only".
   - Every L1-only presence disagreement goes to human adjudication. All disagreements are already reviewed.
   - This needs a small protocol amendment (v0.5, Sections 8.3 and 9).
3. **Fix plan: stated deployment status.**
   - Human review of every stated-status code.
   - Metric 4 continues to use traced status (O14), which is coded after coding, as Section 6.3 sets out. Stated status is a secondary field.
4. **Fix plan: objective achievement.**
   - An automatic consistency check flags any Achieved or Partly achieved code that has no outcome at L2 or above. Every flag goes to adjudication.
   - The adjudicator matches objectives across coders before agreement is computed.
   - AC2 is reported alongside kappa because of the prevalence effect.
5. **Coder B model:**
   - (a) Keep Gemini 3.8 Flash and disclose the limitation. This is the recommended option: it has the lowest cost and the fix plan covers its errors.
   - (b) Switch Coder B to Gemini 4 Argon, which needs a full separate session for each coding run and your approval of each session. This would require recoding the calibration cases.
6. **Deviation 3 (collection step 5).** The backward-citation check (step 5) was not run for the calibration packets. It will be run for all 30 cases during main collection. Any new documents found are added to the main-coding packets, and the calibration packets stay as they were for the record.

## Files

- **Codebook v1.1, change log and prompt v1.1:** `05_Codebook/` and `06_Prompts_and_Models/`.
- **Agreement outputs:** `agreement_round1.json` and `agreement_round2.json`, produced by `scripts/agreement.py` (seed 20261017).
- **Collection records:** search log, document inventory and status signals in `03_Collection/calibration/`; packets in `04_Evidence_Packets/calibration/`.
- **Raw outputs:** `07_Coding_Raw/calibration/round1/` and `round2/`.
