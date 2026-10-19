# O13 Claims Register v1.0: Note for Michael

Blockchain for Impact Funding Evidence Map pilot. Phase D steps 3 and 4, 18 October 2026. Published 19 October 2026 at Gate 4, with GSR's approval of public release.

## What was done

O13 records each coder's headline claims (codebook field 17) and proposes a verification status for each one. Claims are a non-core field, so O11 never adjudicated them and O12 does not hold them. O13 therefore starts from both coders' frozen outputs: 239 claims (A 118, B 121) across all 30 cases. When A and B quote the same passage, or the same figure, from the same source, their claims are merged into one row (rule R1). That leaves 167 rows: 72 from both coders, 46 from A only and 49 from B only. Each claim is checked against the sources already held: the other sources in its packet, the case's status signals and O14. `scripts/phaseD/build_o13.py` ran locally, with no searches, fetches or model calls. Every output, packet and signal hash matches its frozen record, and all 239 quotes were found in their cited sources. The script proposes statuses by fixed rules and does not grade. Your decisions go in `michael_status` and `michael_note`, and they survive a rerun.

## Rules applied (for approval)

- **R2 (matching a figure):** a figure matches when another source gives the same value, within 2% for rounding, with the same type of unit (a percentage matches only a percentage) and in a sentence that shares at least two content words with the claim. Years, dates and timestamps are ignored.
- **V1 Corroborated:** every figure in the claim appears in another packet source whose producer is different, where both coders agree on the producer codes.
- **V2 Consistent:** every figure appears in another held source, but that source has the same producer, or its independence cannot be determined.
- **V3 Decide:** only some of the claim's figures appear in another source.
- **V4 Decide:** a claim without figures shares at least half of its content words with a sentence in another source.
- **V5 Decide:** a coder recorded `conflicts_with`. You decide whether the claim is Contradicted, Consistent (for example, growth over time or a different period) or not about the same quantity.
- **V6 Unverifiable:** no other held source mentions the claim.

## Results

| Proposed status | Rows | Review |
|---|---|---|
| Corroborated (V1) | 4 | Check |
| Consistent (V2) | 6 | Check |
| Unverifiable (V6) | 112 | Routine (1 Check: MCV-16-C04, where the case is traced as Discontinued) |
| To decide (V3 7, V4 6, V5 32) | 45, in 17 cases | Decide |

- **Metric 6, claims that held up (provisional; formerly metric 7):** 10 of 167 claims hold up (6%) and none is contradicted yet. If all 45 open rows held up, the figure would be 55 of 167 (33%). Restricted to rows from both coders: Corroborated 2, Consistent 2, Unverifiable 51, To decide 17.
- **Why most claims are unverifiable:** 134 of 167 claims come from sources the coders rated as implementer, partner or funder. For 13 cases, no claim can be checked against any other held source. The publication date is missing for 117 of the 127 held documents, so a packet source cannot be shown to be later than the claim. Only the status signals are post-funding by design, and they support just 2 claims (FIL-04-C01 and MCV-18-C06).
- **Coder-flagged conflicts:** 32 rows in 11 cases. Most are reach figures that grow between a launch account and later pages (lesson K6), such as UNI-08 (2,598 users versus 15,000 beneficiaries) and UNI-12 (14,000 versus 4M+).

## Step 4: visuals (O15 draft)

`scripts/phaseD/build_visuals.py` builds V1 (shaded by the highest level at L2 or above, with claim-only cells hatched and empty cells labelled gap), V2, V3 and V5 as PNG files, each with its data table, in `10_Analysis_and_Visuals/`. V3 and V5 carry a draft banner until the O14 review and the O13 decisions close; then rerun the script. No case reaches L4 or L5, and Supply chain has no cases, so its row in V1 and V2 is all gap.

## Publishing boundary

The register (`O13_claims_register_v1.0.csv`) holds only IDs, URLs, SHA-256 hashes, quotes of 25 words or fewer and the coders' own one-line claim summaries. The review sheet (`O13_review_sheet_v1.0.csv`) holds full quotes and supporting passages, so it stays restricted and is left out of the step 7 publish.

## Open decisions

1. **Register unit.** (a) Use all 167 rows, with the `coders` column, and report the both-coder figures as a sensitivity check (recommended). (b) Use only the 72 both-coder rows.
2. **Approve rules R2 and V1 to V6.** The protocol names the four statuses but does not define them.
3. **Decide the 45 open rows and confirm the 11 Check rows** in the register. Then rerun `build_o13.py` and `build_visuals.py`.
4. **Metric 6 denominator.** (a) Report held up as a share of all claims (6% for now). (b) Report held up against contradicted among the rated claims only. Recommended: report both, and state the unverifiable share alongside.
5. **Searches.** None is proposed. No single claim would change a gate outcome, because metric 6 is reported as a finding. If you want any searches, the UNI-07 cessation claim (UNI-07-C05/C06) is the strongest candidate, within the 6-search cap.
6. **Publication.** Confirm the 25-word quote limit, and that the coders' model-written claim summaries may be published.
