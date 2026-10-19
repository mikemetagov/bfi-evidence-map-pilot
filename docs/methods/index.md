# Methods

A summary of the protocol. The [protocol](../protocol/index.md) is the authoritative version.

## Unit of analysis
A use case. Each use case is given an evidence level separately for each outcome domain it reports on. This adapts study-based Campbell and 3ie conventions to sparse, mostly non-experimental evidence.

## Roles
| Role | Who |
|---|---|
| Principal investigator and sole human reviewer | Michael Cooper |
| Orchestrator | LLM research assistant (Anthropic Claude family); does not code cases |
| Coder A | Frontier LLM from a second developer (proposed: OpenAI GPT family) |
| Coder B | Frontier LLM from a third developer (proposed: Google Gemini family) |
| Adjudication assistant | Orchestrator model in a separate session; Michael decides |

## Evidence levels
| Level | Definition |
|---|---|
| L1 Claim | Describes what the solution does and why it should work. No data on results. |
| L2 Operational | Data on outputs, usage or operational performance, with no measure of user outcomes. |
| L3 Outcome, no comparison | Outcome data from participants without a comparison group. |
| L4 Outcome with comparison | Compared with a comparison group or non-blockchain alternative, without strong identification. |
| L5 Counterfactual impact | Randomised or strong quasi-experimental impact estimate, ideally independent. |

## Reliability bands
| Band | Threshold | Action |
|---|---|---|
| Decision metric | Weighted kappa ≥ 0.70 on evidence level | Counts toward the scale-up decision |
| Good | ≥ 0.80 | Used as coded |
| Acceptable for a pilot | 0.67–0.79 | Used, flagged, revised for full scope |
| Below acceptable | < 0.67 | Revised and recoded once; if still low, not used to shade the matrix |

## Pilot metrics
| Metric | Threshold | Result |
|---|---|---|
| 1. Agreement between the two models | ≥ 0.70 | Not met: weighted κ 0.64 (95% CI 0.43–0.80), 30 cases |
| 2. Public-source coverage | ≥ 80% | Met: 30 of 30 (no core field coded "insufficient information" in the final codes) |
| 3. Taxonomy fit ("none fits") | ≤ 10% | Met: 2 of 30 (7%) |
| 4. Post-pilot status confirmed | ≥ 75% | Not met: 3 of 30 (10%) at medium or high confidence |
| 5. Evidence level and scaling | Descriptive | See [V3](../outputs/10_Analysis_and_Visuals/V3_deployment_pathway_v1.0.png); 23 of 30 traced Unknown |
| 6. Claims that held up | Reported as a finding | 53 of 167 claims Consistent (32%), none Contradicted, 114 Unverifiable |
