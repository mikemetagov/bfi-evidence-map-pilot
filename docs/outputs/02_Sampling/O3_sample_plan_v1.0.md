# O3 Sample Plan and Actual Sample (v1.0)

Gate 1, 16 October 2026. Published 19 October 2026 at Gate 4, with GSR's approval of public release. The rules follow protocol v0.4, Sections 5.3 and 5.5.

## Planned versus actual

| Portfolio | Protocol target | Eligible in frame | Allocated | Drawn |
|---|---|---|---|---|
| MCV | 8 | 25 | 11 | 11 |
| UNICEF | 8 | 20 | 11 | 11 |
| Filecoin | 7 | 5 | 5 | 5 |
| GSR | 7 | 3 | 3 | 3 |
| Total | 30 | 53 | 30 | 30 |

## Procedure

- Seed: 20261016, using NumPy `default_rng`. The draw can be reproduced with `draw.py`.
- Step 1: Filecoin and GSR are below target, so they are included in full.
- Step 2: The stalled and discontinued quota (6) is drawn first, split by each portfolio's share of stalled cases in the frame: MCV 5, UNICEF 1.
- Step 3: one high-richness case is drawn for any portfolio that has none. UNICEF was topped up (UNI-14).
- Step 4: remaining MCV and UNICEF places are filled by proportional random draws within domain-by-status strata.
- Step 5: six calibration cases are drawn: one stalled case first, then one for each remaining portfolio, then two more at random.

## Quota results

- Domains: all 6 represented (1 Payments: 9, 2 Credit/savings/insurance: 7, 5 Climate/natural assets: 2, 4 Supply chain: 1, 3 Identity/records: 6, 6 Governance/funding: 5).
- Stalled or discontinued: 7, against a target of at least 6. Met.
- High-richness cases per portfolio: MCV 4, UNICEF 3, Filecoin 1, GSR 0. GSR has no high-richness case because its grantees are early pilots. This shortfall is accepted and explained.
- Status groups: Moved on (stalled/discontinued) 7, Moved on 8, Active 15.
- Lineage overlap tests in the sample: UNI-14 (UNICEF and GSR), MCV-24 (MCV and GSR), and FIL-04 with GSR-01 (linked by organisation).
- Declared-interest flag: GSR-02 and GSR-03.

## Calibration set

| Case | Use case |
|---|---|
| MCV-01 | Celo stablecoin payments for digital microwork (youth) |
| UNI-15 | Convexity CHATS cash and voucher platform |
| FIL-01 | Starling Lab Capture-Store-Verify data integrity |
| GSR-01 | Relay Funder aid platform for displaced communities |
| MCV-16 | Haraka & Grameen Foundation onchain microfinance for VSLAs |
| MCV-02 | Smart-contract weather index insurance (inX/Etherisc/ACRE Africa) |

## Actual sample

| Case | Use case | Portfolio | Domain | Status group | Richness | Route |
|---|---|---|---|---|---|---|
| FIL-01 | Starling Lab Capture-Store-Verify data integrity | Filecoin | 3 Identity/records | Active | High | Census (portfolio frame below target) |
| FIL-02 | EASIER Data geospatial data preservation | Filecoin | 3 Identity/records | Active | Medium | Census (portfolio frame below target) |
| FIL-03 | TRANSFER Data Trust artist-owned archive | Filecoin | 3 Identity/records | Active | Low | Census (portfolio frame below target) |
| FIL-04 | Akashic refugee digital memory archive | Filecoin | 3 Identity/records | Active | Low | Census (portfolio frame below target) |
| FIL-05 | Oceanic Whispers marine data trust (CROSSLUCID/RadicalxChange/Serpentine) | Filecoin | 5 Climate/natural assets | Active | Low | Census (portfolio frame below target) |
| GSR-01 | Relay Funder aid platform for displaced communities | GSR | 6 Governance/funding | Active | Medium | Census (portfolio frame below target) |
| GSR-02 | Stablecoin for Impact (Launchnodes) yield to Giga school connectivity | GSR | 6 Governance/funding | Active | Low | Census (portfolio frame below target) |
| GSR-03 | Lido Impact Staking yield to MCV, UNICEF and Giga | GSR | 6 Governance/funding | Active | Medium | Census (portfolio frame below target) |
| MCV-01 | Celo stablecoin payments for digital microwork (youth) | MCV | 1 Payments | Moved on (stalled/discontinued) | High | Stratified draw: 1 Payments / Moved on (stalled/discontinued) |
| MCV-02 | Smart-contract weather index insurance (inX/Etherisc/ACRE Africa) | MCV | 2 Credit/savings/insurance | Moved on | High | Stratified draw: 2 Credit/savings/insurance / Moved on |
| MCV-03 | DeFi merchant digitisation | MCV | 1 Payments | Moved on (stalled/discontinued) | Medium | Stalled/discontinued quota draw |
| MCV-05 | DeFi salary advances / credit for smallholders | MCV | 2 Credit/savings/insurance | Moved on (stalled/discontinued) | High | Stalled/discontinued quota draw |
| MCV-06 | Stablecoin buy-now-pay-later for MSMEs/informal vendors | MCV | 2 Credit/savings/insurance | Moved on (stalled/discontinued) | Medium | Stalled/discontinued quota draw |
| MCV-11 | Forest Carbon Web3 carbon projects | MCV | 5 Climate/natural assets | Moved on (stalled/discontinued) | Medium | Stalled/discontinued quota draw |
| MCV-12 | Blockchain anticipatory cash transfers for pastoralists (pilot + scale-up 2025-26) | MCV | 1 Payments | Moved on | High | Stratified draw: 1 Payments / Moved on |
| MCV-16 | Haraka & Grameen Foundation onchain microfinance for VSLAs | MCV | 2 Credit/savings/insurance | Moved on (stalled/discontinued) | Medium | Stalled/discontinued quota draw |
| MCV-18 | Anticipatory cash transfers for flood-prone areas | MCV | 1 Payments | Active | Medium | Stratified draw: 1 Payments / Active |
| MCV-21 | Anzi grain tokenisation and credit guarantees | MCV | 4 Supply chain | Active | Low | Stratified draw: 4 Supply chain / Active |
| MCV-24 | Aleo/Humanity Link privacy-preserving USDCx aid (with DRC) | MCV | 1 Payments | Active | Low | Stratified draw: 1 Payments / Active |
| UNI-03 | OS City (blockchain government records/credentials) | UNICEF | 3 Identity/records | Moved on | Medium | Stratified draw: 3 Identity/records / Moved on |
| UNI-04 | W3 Engineers TeleMesh blockchain-backed offline mesh messaging | UNICEF | 3 Identity/records | Moved on (stalled/discontinued) | Low | Stalled/discontinued quota draw |
| UNI-07 | BX Smart Labs smart-contract savings circles | UNICEF | 2 Credit/savings/insurance | Active | Low | Stratified draw: 2 Credit/savings/insurance / Active |
| UNI-08 | Kotani Pay transfers, savings and payments | UNICEF | 1 Payments | Moved on | Medium | Stratified draw: 1 Payments / Moved on |
| UNI-10 | Rumsan Rahat cash and voucher assistance | UNICEF | 1 Payments | Active | High | Stratified draw: 1 Payments / Active |
| UNI-12 | Xcapit blockchain wealth management and financial learning | UNICEF | 2 Credit/savings/insurance | Moved on | Medium | Stratified draw: 2 Credit/savings/insurance / Moved on |
| UNI-13 | GovBlocks decentralised decision-making tools | UNICEF | 6 Governance/funding | Moved on | Medium | Stratified draw: 6 Governance/funding / Moved on |
| UNI-14 | Grassroots Economics community currency / emergency payments | UNICEF | 1 Payments | Moved on | High | High-richness quota draw |
| UNI-15 | Convexity CHATS cash and voucher platform | UNICEF | 1 Payments | Moved on | High | Stratified draw: 1 Payments / Moved on |
| UNI-16 | WiiQare health-savings vouchers | UNICEF | 2 Credit/savings/insurance | Active | Medium | Stratified draw: 2 Credit/savings/insurance / Active |
| UNI-18 | Investtools blockchain resource-delivery marketplace | UNICEF | 6 Governance/funding | Active | Low | Stratified draw: 6 Governance/funding / Active |

## Replacements

None so far. If a case proves ineligible on full reading, a replacement is drawn from the same stratum with the next values from the same seeded generator, and is logged here and in O18.
