---
title: Data Colonialism
type: concept
tags: [data-colonialism, fairness, global-majority, geopolitics, llm-bias, power]
sources: [representational-harm-llm-narratives-global-majority]
created: 2026-04-27
updated: 2026-04-27
---

## Overview

Data colonialism is a framework — developed by sociologist Nick Couldry and communication scholar Ulises Mejias — for analyzing how the extraction, commodification, and deployment of data by AI platforms extends and reinforces neocolonial power relationships. The term explicitly draws the analogy to historical colonialism: just as colonial empires extracted raw materials from the Global Majority to produce goods sold back to (or used to dominate) those same populations, AI companies extract data from Global Majority populations to produce AI systems that then shape how those populations are perceived, assessed, and governed.

In [[wiki/sources/representational-harm-llm-narratives-global-majority|Nguyen et al. (FAccT '26)]], data colonialism is introduced as the structural context for understanding why LLMs generate representationally harmful narratives about Global Majority nationalities — and why those harms are not accidents or edge cases but predictable outputs of the current AI development political economy.

## The Colonial Analogy

| Historical Colonialism | Data Colonialism |
|---|---|
| Extract raw materials (land, labor, resources) | Extract raw data (text, behavior, annotations) |
| Manufacturing and value creation in the colonial center | Model training and product development in Global Minority countries (US, UK, EU) |
| Sell products back to or impose governance on colonies | Deploy AI systems that classify, assess, and generate narratives about Global Majority populations |
| Labor exploitation: dangerous work outsourced to colonized populations | Data labor: hazardous content moderation outsourced to workers in Eritrea, Syria, Kenya, etc. |
| Epistemic colonialism: whose knowledge counts as knowledge | Whose perspectives are centered in training data; whose cultural defaults become model defaults |

## The AI Labor Chain

The full pipeline of AI development is structured along colonial lines:

- **Capital and IP**: Major AI labs (Anthropic, OpenAI, Google, Meta, Microsoft, Amazon) are based in Global Minority countries. Equity and profit flow to shareholders in those countries.
- **Highest-paid roles**: AI researchers and engineers in Global Minority locations hold employee-shareholder positions with aligned financial incentives.
- **Hazardous labor**: Content moderation — scrubbing training data of illegal and harmful content (violence, human mutilation, child abuse material) — is disproportionately outsourced to data workers in Global Majority countries. Workers from Eritrea, Syria, Kenya, and similar contexts are recruited as data annotators, often due to political displacement.
- **Health consequences**: Data workers report PTSD, coping-based drug addiction, and other trauma responses from exposure to harmful content. Multiple lawsuits have been filed against outsourcing companies (Scale AI, Sama) for exploitative labor practices.

## How Data Colonialism Produces Representational Harm

Data colonialism is the structural cause; [[wiki/concepts/representational-harm|representational harm]] is the observable output. The causal chain:

1. Training data is disproportionately produced by and for Global Minority populations → US cultural defaults become model defaults
2. Global Majority perspectives are underrepresented in training data → models have impoverished, stereotype-dependent knowledge of those communities
3. Models trained on this corpus then generate narratives that reproduce and amplify the same hierarchies present in the training data
4. These models are then deployed in high-stakes contexts affecting Global Majority populations — immigration assessment, asylum narrative evaluation, education, healthcare

The US Department of Homeland Security's 2024 pilot to use LLMs for simulating and assessing asylum seeker narratives is cited as a concrete, already-deployed example of this feedback loop: a model trained on Global Minority-centered data, generating narratives that subordinate Global Majority characters, deployed to judge the credibility of asylum seekers from those same countries.

## Global Majority / Global Minority Distinction

The paper uses "Global Majority" (UN Group of 77 members, roughly the non-Western world) and "Global Minority" (non-G77, roughly the Western developed world) rather than "developed/developing" or "Global North/South." This terminological choice is deliberate: Global Majority nations contain the majority of the world's population. The framing foregrounds numerical and demographic reality rather than economic hierarchy.

## Relationship to Other Wiki Concepts

- [[wiki/concepts/representational-harm|Representational Harm]] — the observable manifestation of data colonialism in LLM outputs
- [[wiki/concepts/alignment-failure-modes|Alignment Failure Modes]] — AI 2027-focused; primarily about goal distortion in future systems. Data colonialism operates at the level of current deployed systems and the political economy of AI development.
- [[wiki/concepts/ai-for-scientific-discovery|AI for Scientific Discovery]] — the scientific discovery agenda raises parallel questions: whose scientific problems get prioritized, whose data gets used, whose communities benefit

## Open Questions

- Does open-source model development change the data colonialism dynamic, or replicate it?
- What would "decolonial AI" development actually require — representation-balanced data, community-led annotation, localized models?
- How do travel bans and immigration restrictions (20+ countries subject to partial US travel bans as of 2026) interact with AI deployment that uses nationality as a classification variable?
- Is there a tension between safety-oriented arguments for model centralization and decolonial arguments for distributed, community-controlled AI?
