---
title: "Representational Harms in LLM-Generated Narratives Against Global Majority Nationalities"
type: source
tags: [representational-harm, llm-bias, fairness, nationality-bias, data-colonialism, facct]
sources: [representational-harm-llm-narratives-global-majority]
created: 2026-04-27
updated: 2026-04-27
---

## Summary

This FAccT '26 paper (Nguyen, Suresh, Monroe-White, Shieh) audits how widely-deployed LLMs portray national origin identities in open-ended narrative generation. Across two studies — one re-analyzing 500,000 US-centric narratives from GPT-3.5, GPT-4, Llama 2, Claude 2.0, and PaLM 2, and a new dataset of 292,500 globally-framed narratives from GPT-4.1 Nano — the authors find persistent and systematic representational harms targeting Global Majority (non-Western) national identities.

The core quantitative finding: in power-laden US-set prompts, characters with non-US national identities are **61.5× more likely** to appear in subordinated roles (struggling student, patient in need, borrower) than in dominant roles (star student, doctor, lender). African nationalities appear in zero dominant character positions. Italian is the sole non-US nationality with meaningful dominant representation — driven almost entirely by Italian cooking tropes. The paper argues this pattern is not reducible to sycophancy: when Study 2 re-centers prompts on non-US nations, the subordination dynamic largely disappears, confirming that US-centric bias — not prompt-following — is the mechanism.

A TF-IDF analysis of the global dataset reveals that Global Majority narratives cluster around poverty cues ("makeshift clinic", "subsistence farming", "dusty passport"), displacement and conflict language, and interpersonal communication framed as gentle or deferential ("said softly", "patiently explained"). Global Minority narratives cluster around agentic, individualistic, and achievement-oriented language.

The authors frame these findings through **data colonialism**: AI companies based in Global Minority countries extract data from Global Majority populations, outsource hazardous data labor to those same populations, then deploy models that systematically encode and perpetuate neocolonial power hierarchies in generated text.

## Key Concepts

- [[wiki/concepts/representational-harm|Representational Harm]] — how the paper operationalizes harm: stereotyping, erasure, one-dimensional portrayals, and power subordination
- [[wiki/concepts/data-colonialism|Data Colonialism]] — the structural framing: AI as an extension of colonial extraction and knowledge-power hierarchies
- [[wiki/concepts/alignment-failure-modes|Alignment Failure Modes]] — representational harm is a distinct failure mode from goal misalignment, but both originate in training

## Key Entities

None created — authors are academics; no organizational entities warranting wiki pages.

## Notable Claims

- Non-US characters are 61.5× more likely to be subordinated than dominant in US-set power-laden narratives
- No African nationality appears in a dominant character position across the entire Study 1 dataset
- Country clusters mirror US military history: Afghanistan, Iraq, Vietnam, Philippines cluster as "patients in need" purely from story distribution, with no explicit country name in the clustering input
- The harms are not sycophancy: replacing "American" with a non-US nationality in the dominant prompt position does not produce equivalent subordination of other countries
- Global Majority narratives contain distinctive language of displacement, poverty, and limited agency; Global Minority narratives contain agentic, achievement-oriented language
- LLMs are already used in high-stakes nationality-judgment contexts: the US DHS used LLMs in 2024 to simulate and assess asylum seeker narratives

## Contradictions / Open Questions

- The paper studies narrative generation — it's an open question how far these findings extend to factual or instructional LLM outputs
- Study 2 uses only GPT-4.1 Nano for cost reasons; replication across other models is needed
- The "61.5×" figure is striking but limited to Study 1's US-centric prompt framing; the global-scope number from Study 2 is harder to distil to a single ratio
- Tension with the wiki's existing focus: the wiki's AI 2027-driven framing centers on *capability* risks; this paper centers on *harm from current deployment* — the timescales and threat models are different

## Raw Source

`raw/2604.22749v1.pdf`
`raw/representational harm in LLm generated narratives against global majority nationalities.md`
