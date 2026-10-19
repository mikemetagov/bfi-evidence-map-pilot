---
hide:
  - toc
---

# Explore the evidence map

This map shows what public evidence exists for 30 blockchain projects funded by four portfolios: Mercy Corps Ventures, UNICEF Venture Fund, Filecoin Foundation and GSR Foundation. Each row is a type of use, such as payments or credit. Each column is a type of outcome, such as reach or financial resilience. The bubbles show how many projects report that outcome, and how strong the evidence behind it is.

## Three things to know

- **Most evidence is claims or activity data.** Of 113 project-outcome records, 60 are claims only, 44 are operational data and 9 report outcomes without a comparison.
- **No project reached the two strongest steps.** None of the 30 has outcomes measured against a comparison group, or proven impact.
- **Some areas have no evidence at all.** No pilot project works on supply chains. The two climate projects have claims only.

## The evidence spectrum

The map sorts each piece of evidence into one of five steps. Each step answers a harder question than the one before. The colours run from light (weaker) to dark (stronger) and are the same on every page of this site.

<div class="spectrum" role="list" aria-label="Evidence spectrum, from weakest to strongest">
  <div class="step s1" role="listitem"><span class="name">1. Claims only</span>The project describes what it does and why it should work. There are no data on results.<span class="count">Strongest evidence for 4 cases</span></div>
  <div class="step s2" role="listitem"><span class="name">2. Operational data</span>Data on activity, such as payments made, users reached or processing times. It shows the system runs, not whether people are better off.<span class="count">Strongest evidence for 17 cases</span></div>
  <div class="step s3" role="listitem"><span class="name">3. Outcomes, no comparison</span>Changes reported for participants, such as income or savings. With nothing to compare against, we cannot tell whether the project caused them.<span class="count">Strongest evidence for 6 cases</span></div>
  <div class="step s4" role="listitem"><span class="name">4. Outcomes with comparison</span>Participants compared with a similar group, or with a non-blockchain alternative. This starts to show what the project added.<span class="count">No pilot cases</span></div>
  <div class="step s5" role="listitem"><span class="name">5. Proven impact</span>A randomised trial or strong quasi-experimental study estimates the effect, ideally done independently.<span class="count">No pilot cases</span></div>
</div>
<div class="spectrum-axis"><span>Weaker: tells you what was promised or done</span><span>Stronger: tells you what difference it made</span></div>

The spectrum describes the type of evidence found in public sources. It does not rate the quality of a project. A new or small project may be doing well and simply not have been evaluated yet. Three of the 30 projects had no outcome coded from their sources, so they do not appear in the grid. The protocol and data files use the codes L1 to L5 for these five steps; see [how the levels were set](../methods/index.md#evidence-spectrum).

## How to read the map

1. **Hover over, tap or tab to a bubble** to see the projects behind it. Click it to keep the card open and follow the source links. Press Esc to close.
2. **Use the filters** to look at one portfolio, region or status.
3. A project appears once for each outcome it reports, so the numbers across a row can add up to more than the number of projects.
4. A cell marked "gap" means no evidence was found.

!!! info "Pilot data, published 19 October 2026"
    This is a pilot of 30 projects chosen to cover different uses. It is not a representative sample of all funded projects. See also the [visuals](../visuals/index.md), or [ask the map](../assistant/index.md) a question in plain language.

<div id="egm" class="egm" data-src="map-data.json"></div>

??? note "Technical notes"
    **Filter gaps.** Where the two coders differed on a minor field, it was left blank for the pilot and will be fixed in codebook v1.3. 21 of 30 cases have at least one blank (37 in all): country 5, region 4, year launched 9, blockchain functions 12, implementation model 7. Filtering on one of these fields leaves those cases out. The coders' values are in the [non-core differences table](../outputs/09_Final_Dataset/O12_noncore_differences_v1.0.csv).

    **Quotes.** Quotes are cut to 25 words. Full-text hashes are in the [O12 outcomes table](../outputs/09_Final_Dataset/O12_outcomes_v1.0.csv).

    **Gap types.** Absolute, outcome, counterfactual, added-value and harms gaps are defined in section 9.1 of the [protocol](../protocol/index.md).
