# O12 Final Coded Dataset v1.0: Data Dictionary

Blockchain for Impact Funding Evidence Map pilot. Phase D step 1, 18 October 2026. Published 19 October 2026 at Gate 4, with GSR's approval of public release.

**Public copy:** in `O12_outcomes_v1.0.csv` and `O12_objectives_v1.0.csv`, every quote column is cut to 25 words (" ..." marks a cut) and followed by a `<column>_sha256` column holding the SHA-256 of the full normalised quote. The map's `data/coding.csv` quotes are cut the same way; their hashes are in `quote_final_sha256`.

## What O12 is

O12 holds the final code for every core field in all 30 pilot cases. Each final code sits next to both coders' original codes, as protocol section 8.5 requires. Coder A is GPT-6 Astra and Coder B is Gemini 3.8 Flash. Both coded under codebook v1.2. Final codes come from Michael's decisions in the O11 adjudication batch (125 rows, all decided). Where the coders agreed and no review was needed, the agreed code is final.

`scripts/phaseD/build_o12.py` builds the dataset locally, with no model calls and no searches. The build stops if any core-field disagreement has no adjudication row, if any adjudication row goes unused, if the codes in the sheet differ from the frozen outputs, or if any final code falls outside codebook v1.2. The v1.0 build passed every check. Before the build, all input hashes were re-verified (packets 30/30, outputs 60/60, codebook files 3/3). The hashes of the adjudication and matching inputs are recorded in `O12_build_summary_v1.0.json`.

## Files

| File | Unit | Rows |
|---|---|---|
| `O12_cases_v1.0.csv` | One case | 30 |
| `O12_outcomes_v1.0.csv` | One case × outcome domain (A–F), including absent domains | 180 |
| `O12_objectives_v1.0.csv` | One objective pair, or one unpaired objective | 86 |
| `O12_noncore_differences_v1.0.csv` | One non-core field where the coders differ (review sheet) | 98 |
| `O12_build_summary_v1.0.json` | Counts, checks and input hashes | – |
| `site_staging/cases.csv`, `site_staging/coding.csv` | Final codes in the `data/` column format | 30, 113 |

The staging files are not copied to `data/` until the Gate 4 publish (Phase D step 7). `deployment_status_traced` (and `status_confidence` in staging) were filled from O14 v1.0 in Phase D step 2 by `scripts/phaseD/build_o14.py`; with them the site build passes.

## Shared conventions

- Suffix `_A` / `_B`: the coder's original code, exactly as in the frozen output. Suffix `_final`: the code used for analysis.
- `basis`: one of `Agreed` (same code from both coders, no review), `Reviewed agreed code` (both agreed, and Michael reviewed it under protocol 8.4), `Adjudicated disagreement` (Michael decided), `Coders differ (not adjudicated)` (non-core field only) or `Not compared; not adjudicated` (unpaired objective).
- `item_id`, `decision`, `error_type`: these link to the matching row of `08_Agreement_and_Adjudication/O11_adjudication_batch_v1.csv`. That row holds both quotes, the assistant's two suggestions and rationales, and Michael's note. They are blank when `basis = Agreed`.
- `decision` values: `Accept suggestion` (109 rows where both assistant runs agreed), `Use A` or `Use B` (16 rows Michael decided from the packets).
- `error_type` values: `Coder A error`, `Coder B error`, `Both`, `Not an error`. These are derived by the agreed rule.
- `calibration_case`: `Yes` for the six calibration cases, which were recoded blind under v1.2. Run sensitivity analyses on the 24 `No` cases.
- Allowed code values and labels are in `data/codebook.csv` and `05_Codebook/codebook_v1.2.md`.

## O12_cases_v1.0.csv

| Column(s) | Meaning |
|---|---|
| `case_id`, `lineage_id`, `name`, `primary_portfolio`, `all_funders` | From the O3 sample (not coded) |
| `calibration_case`, `codebook_version` | See conventions; always `1.2` |
| `use_case_domain_{A,B,final,basis,item_id,decision,error_type}` | Core field. Values `1`–`6` or `none`. 29 agreed, 1 adjudicated (FIL-05: final `5`, Use B) |
| `stated_deployment_status_{…}` | Core field. This is what the packet states, not what happened later. All 30 were reviewed by Michael: 24 confirmed agreed codes, 6 adjudicated. UNI-07 changed from Discontinued to Unknown on review |
| `blockchain_added_value_{…}` | Core field, `0`–`3`. 15 agreed, 12 reviewed (codes 2 or 3), 3 adjudicated. No final code of 3 |
| `use_case_subcategory_{A,B}` | Coder free text, not adjudicated |
| `country`, `region`, `year_launched`, `blockchain_functions`, `blockchain_component_status`, `implementation_model`, `funding_model`, `population_groups`, `reach` (each `_A`, `_B`, `_final`, `_basis`) | Non-core descriptive fields. `_final` is filled only where the coders agree; otherwise it is blank and `_basis = Coders differ (not adjudicated)`. List fields are sorted and joined with `; `. `reach` = number plus unit, or `not reported` |
| `deployment_status_traced` | From O14 v1.0 (Phase D step 2, protocol 6.3), after Michael's code-by-code review (19 October 2026: 26 confirmed, 4 changed). Confidence and signals are in `O14_status_tracing_v1.0.csv`. Metric 4 uses this field, not the stated status |
| `problem_addressed_{A,B}`, `risks_reported_{A,B}` | Coder text and Yes/No flag, kept for reference |

## O12_outcomes_v1.0.csv

| Column(s) | Meaning |
|---|---|
| `case_id`, `outcome_domain` (`A`–`F`), `calibration_case` | Unit keys |
| `level_A`, `level_B` | Each coder's highest evidence level for the domain (`L1`–`L5`), or `absent`. This is the same rule `agreement.py` uses when a coder lists a domain twice. `entries_A` / `entries_B` give how many entries each coder made |
| `level_final` | Final level or `absent`. 128 agreed, 52 adjudicated. Totals: L1 60, L2 44, L3 9, absent 67. No L4 or L5 |
| `present_any_final`, `present_L2_final` | 0/1 presence at any level (113 cells) and at L2 or above (53 cells), the two Gate 3 fix-plan thresholds. Shade V1 by `present_L2_final` |
| `claim_only_final` | 1 where the final level is L1 (60 cells). Mark these cells in V1 as claim only |
| `basis`, `item_id`, `decision`, `error_type` | See conventions |
| `display_text_from` | Which coder's entry supplies the `_final` text: `A` when the final level equals A's level (this includes all agreed cells; the display rule picks A, and B's text is kept), `B` when only B's level matches (5 cells), `none` when absent. No present cell has a final level that neither coder gave |
| `key_result_final`, `quote_final`, `source_id_final`, `evidence_url_final`, `evidence_producer_final`, `confidence_final` | Text from the selected coder's entry. The URL comes from the frozen packet header for that source |
| `key_result_{A,B}`, `quote_{A,B}`, `source_id_{A,B}`, `evidence_producer_{A,B}`, `confidence_{A,B}` | Both coders' entries, kept as corroborating evidence (lesson A2) |

Quotes passed the normalised quote check (whitespace, curly quotes and dashes normalised). This shows traceability to the source block. It does not prove the quote is byte-identical.

## O12_objectives_v1.0.csv

| Column(s) | Meaning |
|---|---|
| `pair_status` | `Confirmed pair (primary)`: one of the 56 pairs Michael confirmed, using the option 2 split rule. `In a split group, not the primary pair` (11). `Unmatched (one coder only)` (19) |
| `match_source` | `Lexical` or `Assistant-proposed (Luna)`; both were confirmed by Michael |
| `objective_id_{A,B}`, `objective_{A,B}`, `quote_{A,B}` | Each coder's objective and achievement quote |
| `achievement_{A,B}` | Each coder's original code: `Achieved`, `Partly achieved`, `Unclear` or `Not achieved` |
| `achievement_final` | Filled only on the 56 primary pairs: 29 agreed, 27 adjudicated. Totals: Unclear 24, Partly achieved 18, Achieved 14. Blank on unpaired rows, which were not compared or adjudicated |

## Reliability flags for users of O12

Protocol 8.3 governs how fields may be used. Evidence level (κ 0.64), L2+ presence (κ 0.61) and achievement (κ 0.42 on matched pairs) are below 0.67. Final codes in these fields are human-adjudicated, but each field must carry its reliability label in any visual or finding. Michael's plan is codebook v1.3 and a fresh calibration after the pilot. Michael checked the 92 agreed fields in the audit (92 of 92 matched), but the audit tests only agreed codes; it does not test the Coder A preference (M10).

## Non-core differences: decision (18 October 2026)

Protocol 8.3–8.5 adjudicates core fields only, so non-core differences were not guessed. `O12_noncore_differences_v1.0.csv` lists all 98; 37 are fields shown on the site (country 5, region 4, year launched 9, blockchain functions 12, implementation model 7). All 9 year differences are Coder A reporting "not reported" while Coder B gives a year.

**Michael's decision (option 3):** these fields stay blank in `_final` (and in site staging) for the pilot. No pilot resolution is made. The non-core rules (year source, country of delivery versus organisation, list completeness) are fixed in codebook v1.3, and the protocol will state how non-core fields are handled at full scale. Both coders' values remain in O12. The map's filters on these fields will show gaps for differing cases; the Gate 4 note and O17 must say so. See lesson D1.
