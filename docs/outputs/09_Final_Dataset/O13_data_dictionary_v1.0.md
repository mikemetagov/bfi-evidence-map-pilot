# O13 Claims Register v1.0: Data Dictionary

Built by `scripts/phaseD/build_o13.py`; rules in `O13_claims_register_note_v1.0.md`; decisions and results in `O13_claims_register_note_v1.1.md`. Michael's answers (`O13_michael_answers_v1.0.csv`) are written into `michael_status`/`michael_note` by `scripts/phaseD/o13_record_answers.py`; the summary JSON adds `metric6` (both denominators; all rows, both-coder rows, non-calibration) and `michael_decisions`. One row per distinct headline claim (codebook v1.2 field 17).

## O13_claims_register_v1.0.csv (publishable at Gate 4)

| Column | Meaning |
|---|---|
| `claim_id` | `<case>-Cnn`, ordered by source then position of the quote in the source |
| `case_id`, `calibration_case`, `use_case_domain_final` | From O12 |
| `coders` | Both, A only or B only (merge rule R1) |
| `claim_type` | Coder claim type(s): cost, speed, reach, outcome, value, other |
| `claim_text_A`, `claim_text_B` | Each coder's one-line summary of the claim (model-written) |
| `figures` | Figures read from the quote by the script (rule R2); blank for non-numeric claims |
| `source_id`, `source_url`, `source_sha256`, `source_published` | The cited packet source, its URL, the SHA-256 of its frozen text and its reported publication date |
| `source_producer_coded` | Evidence producer of the source as coded; "Coders differ" when A and B disagree (non-core, not adjudicated) |
| `quote_short` | The claim quote cut to 25 words or fewer |
| `quote_sha256` | SHA-256 of the full normalised quote (whitespace, curly quotes and dashes normalised as in `check_coder_output.py`) |
| `quote_B_short` | Coder B's quote, 25 words or fewer, when it differs from A's |
| `conflicts_with` | Source IDs given by either coder as reporting a different figure |
| `support_ids`, `support_urls`, `support_sha256`, `support_quote_short` | Other held sources (packet `S..` or status signal `T..`) containing every figure, or the overlapping sentence under V4 |
| `partial_ids` | Sources containing only some of the figures (V3) |
| `traced_status_O14`, `stated_status_final` | From O14 and O12 |
| `proposed_status` | Corroborated, Consistent or Unverifiable; blank when Michael must decide |
| `rule` | V1 to V6 |
| `review` | Routine, Check or Decide |
| `review_reason` | Why the row needs review |
| `michael_status`, `michael_note` | Michael's decision (Corroborated, Consistent, Contradicted, Unverifiable) and note; kept on rerun |

## O13_review_sheet_v1.0.csv (restricted; do not publish)

`claim_id`, `review`, `proposed_status`, `rule`, `review_reason`, full `quote_A` and `quote_B`, `merge_score` (1 = one quote contains the other), and the full supporting and partial passages.
