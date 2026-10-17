# Codebook v1.2

Blockchain for Impact Funding Evidence Map pilot. v1.0 was frozen at Gate 2 (16 October 2026). v1.1 (17 October 2026) adds the Gate 3 calibration rules O2, O3, E6, E7, S1, V2 and A1 (change log v1.1-17 to v1.1-23). Michael approved them at Gate 3. v1.2 (17 October 2026) adds two worked examples to rule S1 (change v1.2-24) and is the version for main coding. Versions v1.x are calibration changes approved at Gate 3. Every change is logged in `codebook_changelog.csv`.

## General rules

These rules apply to every field.

- **R1 Evidence only from the packet.** Code only from the evidence packet. Do not use outside knowledge, even if you believe it is correct.
- **R2 Quote and source for every code.** Every code other than "not reported" or "not applicable" needs a source ID (for example S01) and a verbatim quote. The quote must be copied character for character from one source and be 300 characters or fewer. Use the shortest span that supports the code. Do not join text from different places.
- **R3 Not reported versus not applicable.**
  - Use "not reported" when the field applies but the packet says nothing about it.
  - Use "not applicable" only when the field cannot apply (for example, a cash-transfer case has no "children" population unless the sources name one).
  - Never treat silence as evidence of no effect.
- **R4 Confidence for every code.**
  - High: the source states the code directly.
  - Medium: the code needs a short, clear inference.
  - Low: the code needs a judgement between plausible options. Low-confidence codes go to human review.
- **R5 Insufficient information.** List a field in `insufficient_information` only when the packet has relevant evidence but it does not let you choose between options. Use this instead of guessing. Do not list fields coded "not reported".
- **R6 Sources disagree.** Code the figure or statement from the most specific source: an endline report is more specific than a summary page, which is more specific than a promotional page. Record the conflict in the claims fields (field 17).
- **R7 Funder text.** Partner or funder pages are evidence produced by the partner or funder (field 12). They are not independent evidence, even when written in a neutral tone.

## Fields

The orchestrator pre-fills the identification fields from the sampling frame (O2). Coders do not code them: case ID, lineage ID, organisation ID, name, primary portfolio and all funders.

### 1. Country, region and year launched

- **Country:** ISO 3166-1 alpha-3 codes, as a list.
- **Region:** World Bank region.
- **Year launched:** the year the pilot or use case started, as stated in the sources.

Use "not reported" if absent.

Example (hypothetical): "In March 2021 we began testing the wallet with traders in Kisumu" gives year 2021, KEN, Sub-Saharan Africa.

### 2. Problem addressed

One sentence describing the problem the use case targets, with a quote.

Example (hypothetical): "Smallholders wait weeks for insurance payouts after drought" gives the problem "slow insurance payouts to smallholders after drought".

### 3. Stated objectives (up to 3)

Objectives the sources state for this use case, in their own terms.

- Prefer explicit aims ("to test…", "aims to…").
- If none are explicit, use the stated purpose of the pilot, and set confidence to medium.

Example (hypothetical): "The pilot aims to cut the cost of sending remittances to rural families" gives one objective.

### 4. Use-case domain (single choice) and subcategory

| Code | Domain | Subcategories (examples) |
|---|---|---|
| 1 | Payments and cash transfers | Humanitarian cash, anticipatory cash, remittances, merchant payments, wages |
| 2 | Credit, savings and insurance | Micro-lending, savings tools, parametric insurance, guarantees, asset-backed finance |
| 3 | Identity, records and data integrity | Digital ID, credentials, provenance, archiving and storage |
| 4 | Supply chain and traceability | Vaccines, food, commodities, traceability of goods |
| 5 | Climate and natural assets | Carbon and environmental credits, regenerative finance, climate data |
| 6 | Governance, funding and coordination | DAOs, community treasuries, crowdfunding, grant and donor flows, yield-funded giving |
| none | None fits | Explain in a note. Counts toward taxonomy fit (metric 3) |

Decision rules:

- **D1 Classify by the service delivered to users, not by the technology or the sector goal.** Sector goals go in outcome domain E.
  - Tokenised assets sold to users as a savings plan: 2, not 3.
  - Rent-to-own finance for climate-smart homes: 2. The climate benefit is an E outcome.
- **D2 Tokenised goods.**
  - Tokenised goods used as collateral for credit: 2.
  - Tokenised goods used to trace origin or movement: 4.
- **D3 Payments versus credit.**
  - Transfers with no repayment: 1.
  - Anything with repayment, premiums or deposits: 2.
- **D4 Yield and staking used to fund social programmes:** 6.
- **D5 Connectivity, internet access, mesh networking and information access:** code none fits with the note "connectivity". This keeps the approved six-by-six framework intact and tests taxonomy fit. It will be reviewed at Gate 3.
- **D6 Tie-break.** If two services are equally central, choose the one named first in the stated objectives, and set confidence to low.

### 5. Blockchain function(s) (multiple choice)

| Code | Function |
|---|---|
| F1 | Stablecoin or payment rail |
| F2 | Smart-contract automation (payouts, interest, conditions) |
| F3 | Tokenisation or fractionalisation of assets |
| F4 | Tamper-evident record or traceability ledger |
| F5 | Decentralised storage |
| F6 | Decentralised governance (DAO, on-chain voting) |
| F7 | Digital identity or verifiable credentials |
| other | Other (describe) |

Code only the functions the sources describe for this use case, not features of the organisation's wider platform.

Example (hypothetical): "Payouts are triggered automatically by a smart contract when rainfall data crosses a threshold" gives F2.

### 6. Blockchain component status (single choice)

| Code | Meaning |
|---|---|
| Used as designed | The sources describe the blockchain component operating in the pilot |
| Partly used | Some planned blockchain functions were used and others were dropped |
| Removed or not used | The pilot ran without its planned blockchain component, or dropped it |
| Unclear | The sources do not show whether the component was used |

Example (hypothetical): "the team ran the pilot on a conventional database instead of the planned ledger" gives Removed or not used.

### 7. Implementation model (single choice), delivery partners and funding model

- **Implementation model:** Start-up; NGO; UN agency or country office; Government; Consortium (three or more organisations with named roles); Other.
- **Delivery partners:** free text, listing named organisations.
- **Funding model:** Grant; Equity or venture investment; Recoverable grant or convertible instrument; Blended (more than one of these); Yield- or staking-funded; Not reported.

Example: a pilot run by a start-up with funder support gives Start-up. Funding is "not reported" unless the sources state how the pilot was financed.

### 8. Population group(s) (multiple choice) and reported reach

- **Population groups:** include every group the sources name as a target or participant segment, including segments named only in the results. Values: Women; Youth; Children; Refugees or displaced people; Smallholder farmers; Micro-entrepreneurs or MSMEs; Unbanked or underbanked; Low-income individuals; Rural communities; Other (describe); Not reported.
- **Reach:** the number and unit (people, households, merchants and so on), with a quote.
  - Use the figure for the pilot period. If pilot-period sources agree within rounding (for example "over 3,000" and "3,214"), use the most precise number.
  - When sources give different figures (for example, a later page reporting a larger total), follow R6 and log both figures as claims.

Example (hypothetical): "reached 2,400 market vendors, 60% of them women" gives 2,400 people, with Micro-entrepreneurs or MSMEs and Women.

### 9. Outcome domains reported (multiple choice)

| Code | Domain | Includes |
|---|---|---|
| A | Delivery efficiency | Transaction cost, speed, administrative burden, minimum ticket size, yield or fee compared with alternatives |
| B | Reach and access | Adoption, active use, activation, first-time access, inclusion of women, unbanked and displaced people |
| C | Transparency, trust and accountability | Traceability, leakage, fraud, user trust |
| D | Financial resilience and wellbeing | Income, savings, coping with shocks, financial control or stress |
| E | Sector outcomes | Health, education, climate adaptation, human rights and justice, culture |
| F | Risks, harms and unintended effects | Privacy, volatility, cash-out failure, exclusion, security incidents |

Code a domain as reported when the packet gives a result, or a claimed result, in that domain. A general claim such as "increased transparency" counts: code it at L1. Leave out domains that are not reported.

- **O2 Purpose is not a result.** Statements of purpose, target need or intended benefit (for example, "addressing needs from water access to education") are not outcome claims. Code a domain at L1 only when the sources claim that a result occurred (for example, "reduced fraud", "built trust").
- **O3 Where common results belong.**
  - Insurance coverage, loan volumes, number of campaigns and similar measures of uptake or access: B.
  - Trust in the product or provider: C.
  - Payout or transfer speed and cost: A.
  - E is only for sector results such as health, education, climate adaptation, justice or culture.
- **O1 Terms are not outcomes.** Product terms, design features and safeguards (for example, an interest penalty for early withdrawal) are not outcomes in domain F. Code F only when the sources present something as a risk, harm, failure or unintended effect of this use case, or explicitly report that none occurred. General commentary on sector or regulatory risks (for example, "overregulation may lead to…") is not coded.

Example (hypothetical): "30% of recipients had never held a mobile wallet before" gives B.

### 10. Evidence level for each reported outcome domain (L1–L5)

| Level | Definition | Decision rule |
|---|---|---|
| L1 Claim | Describes what the solution does or should achieve. No result data | Statements of intended or general benefit with no figures or observed result |
| L2 Operational | Data on outputs, usage or operational performance | Counts of users, transactions, value saved, cost, speed, activation rates. On-chain data is capped at L2 |
| L3 Outcome, no comparison | Outcome data from participants without a comparison group | Survey or self-report of changes in participants' situation, behaviour or wellbeing |
| L4 Outcome with comparison | Outcomes compared with a comparison group or a non-blockchain alternative, without strong identification | A comparison group, before-and-after with a comparison, or a comparison of delivery channels on outcomes |
| L5 Counterfactual impact | Randomised or strong quasi-experimental estimate | RCT, regression discontinuity, robust difference-in-differences |

- **E1 Grade the highest level reached within that domain** across all sources.
- **E2 A comparison of operational features is not L4.** For example, "fees were half those of bank transfers" is L2 in domain A. L4 needs outcomes for people compared with a comparison group.
- **E3 Self-reported survey results** ("58% of users reported eating more meals") are L3, even when the survey is small or its method is not described. Note any missing method in `key_result`.
- **E6 Anecdotes and unquantified statements are L1.** A single participant's testimonial, an individual story or a case narrative is L1, as in the protocol's L1 examples. So is a qualitative statement that a result happened, with no figures or systematic data behind it (for example, "credit strengthened households" or "helped reopen a case").
- **E7 What counts as a comparison for L4.** L4 needs outcomes for people exposed to the use case compared with people who were not exposed, or compared with a non-blockchain alternative. Comparisons between subgroups of participants (for example, payout recipients versus non-recipients within the insured group) are L3.
- **E5 Who was reached is not a change.** Survey answers about users' status at sign-up (for example, "had never had a savings account") are L2 in domain B. They describe who was reached, not a change in their situation. L3 needs a reported change in participants' behaviour, situation or wellbeing.
- **E4 Comparing acquisition channels inside the pilot** (for example, agent-led versus SMS onboarding) is L2 in domain B. It compares operations, not outcomes against a non-participant group.

Each outcome record needs: domain, level, key result (one sentence), quote, source ID, evidence producer (field 12) and confidence.

### 11. Objective achievement (one record per objective in field 3)

Values: Achieved; Partly achieved; Not achieved; Unclear. Each needs a quote.

- **A1 Achievement needs a result.** "Achieved" or "Partly achieved" needs a result at L2 or above in the matching outcome domain. If only L1 claims support the objective, code Unclear.
- For objectives framed as "test whether X", code by the result on X, not by whether the test ran.
- List objectives in the order the most specific source states them. Prefer the pilot's own stated learning questions or hypotheses.

- Code "Achieved" only when a result directly matches the objective.
- A launch or a reach figure alone does not show achievement of an outcome objective: code it as Unclear or Partly achieved.

Example (hypothetical): the objective "to test whether vendors will adopt the wallet", with "1,200 vendors used it weekly", gives Achieved. The objective "to raise vendor incomes", with only usage data, gives Unclear.

### 12. Evidence producer (one per source)

Values: Implementer; Partner or funder; Independent; Peer-reviewed.

- Pages from the funder or portfolio manager are coded Partner or funder.
- Pages written "in partnership with" or "developed with" the funder are also coded Partner or funder.
- Independent means an organisation with no funding or delivery role.

### 13. Blockchain added value (0–3)

| Code | Meaning |
|---|---|
| 0 | Not addressed |
| 1 | Asserted: the sources say blockchain helped, with no comparison |
| 2 | Descriptive comparison with a prior or alternative channel (for example, fees or minimums compared with the legacy product) |
| 3 | Tested comparison against a non-blockchain alternative on the same outcome, with a comparison design |

- **V2 A figure is not a comparison.** A figure with no explicit prior or alternative channel (for example, "fees stay low at 2%") scores 1. Comparisons of a governance or delivery model that are not attributed to the ledger (for example, community-managed versus externally managed funds) score 1.
- **V1 Credit the blockchain only when the comparison isolates the ledger's contribution.** If the gain could come from the licence, the app or the agents, the comparison is still 2 when the sources attribute it to blockchain, but it is never 3.

Example (hypothetical): "The blockchain made the programme more transparent" alone gives 1. "Transfers arrived in minutes, compared with five days through the previous bank channel" gives 2.

### 14. Risks or harms reported

Yes or No, with a list and quotes.

- Include risks that are mitigated, and statements that no harms were observed. A statement of no harm is a reported result, not silence.
- Code No when the packet does not mention risks.

### 15. Deployment status as stated in the sources

Use the definitions GSR confirmed at Gate 1.

| Code | Meaning |
|---|---|
| Pilot | A time-bound test with named users. Use this when the sources describe the pilot and its end, and nothing after |
| Extended pilot | The pilot was continued or enlarged by the same operator, still described as a pilot |
| Scaled | Use of the same solution beyond the pilot period with wider reach, as routine operation. This is a deployment |
| Handed over | Use by a new operator (a government, a partner or a country office). This is a deployment |
| Discontinued | The sources say the use case ended or the organisation closed |
| Unknown | The sources do not state what happened after the pilot |

- **S1 Counting deployments.**
  - One described deployment: Pilot.
  - Further deployments by the same operator, still framed as pilots or phases: Extended pilot.
  - A provider's solution used in further projects for new clients or programmes after the first pilot: Scaled.
  - Run by a new operator without the original provider: Handed over.
  - Ongoing activity described without pilot framing and without further deployments: Unknown, with a note.
  - Worked examples:
    - "Findings from phase one; the final report will cover the concluding phase" gives Extended pilot.
    - "Deployed in three humanitarian projects with different partner organisations" gives Scaled.

Code only what the packet states. Current status is traced separately after coding (O14). Coders do not search for it.

Example (hypothetical): a later funder page reporting a larger user count than the pilot endline suggests growth, but does not state routine operation. That gives Extended pilot or Scaled at low confidence, so it goes to human review.

### 16. Not used in v1.0

Traced current status, signals and confidence are coded by the orchestrator in the status-tracing step (O14), after coding. They are not part of the coder output.

### 17. Headline claims (up to 5)

Record each headline quantitative or outcome claim with:

- text, quote and source ID;
- claim type: cost, speed, reach, outcome, value or other;
- `conflicts_with`: the source ID of any packet source giving a different figure for the same quantity.

Priority when there are more than five claims:

1. Figures that conflict across sources.
2. Outcome claims (L3 or above).
3. Cost, speed and value claims.
4. Reach.

Figures that agree within rounding count as one claim and do not conflict.

Coders do not rate whether a claim was verified. That is done later in the claims register (O13).

Example (hypothetical): S01 says "3,000 households" and S02 says "5,000+ households". These are two claims, each with `conflicts_with` pointing to the other source.

### 18. Quality control

- **Insufficient information:** a list of field names where R5 applies.
- **Coder notes:** free text, 600 characters or fewer.
- **Coder ID and codebook version:** set by the run script.
