# Data

Rebuilt from the `data/` folder on every update.

| File | Contents |
|---|---|
| [cases.csv](downloads/cases.csv) | One row per use case: identification, domain, functions, portfolio, stated and traced status, blockchain added value, case link. |
| [coding.csv](downloads/coding.csv) | One row per use case and outcome domain: evidence level, key result, quote, source ID and link, evidence producer, confidence. |
| [codebook.csv](downloads/codebook.csv) | Allowed values, labels, order and definitions. Codebook values (v1.0 frozen at Gate 2; rules in codebook v1.2). |
| [outputs_register.csv](downloads/outputs_register.csv) | Status and file location of outputs O1–O19. |
| [eppi-mapper.json](downloads/eppi-mapper.json) | The same data formatted for EPPI-Mapper. |

## Fields the map uses

| Field | Table | Meaning |
|---|---|---|
| case_id | both | Stable use-case ID. Never reuse or renumber. |
| lineage_id | cases | Links the case to its sampling-frame record (O2). |
| use_case_domain | cases | 1–6, or `none` if no domain fits (metric 3). Map rows. |
| primary_portfolio | cases | MCV, UNICEF, FIL or GSR. |
| deployment_status_traced | cases | Pilot, Extended pilot, Scaled, Handed over, Discontinued or Unknown (O14). |
| blockchain_added_value | cases | 0–3. |
| outcome_domain | coding | A–F. Map columns. |
| evidence_level | coding | L1–L5. Bubble colour. |
| quote, source_id, evidence_url | coding | The supporting quote (cut to 25 words) and its source. |

Fields with several values, such as `blockchain_functions`, use semicolons: `Payments; Tokens`.
