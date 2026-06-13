---
title: Representational Harm
type: concept
tags: [representational-harm, fairness, llm-bias, nationality-bias, stereotyping, erasure]
sources: [representational-harm-llm-narratives-global-majority]
created: 2026-04-27
updated: 2026-04-27
---

## Overview

Representational harm is a category of AI harm distinct from allocative harm (unfair distribution of resources or opportunities). Where allocative harm is about *what* a system decides, representational harm is about *how* a system depicts or characterizes groups of people. The concept originates in critical media studies and was formalized for AI systems by Barocas et al. (2017) and extended by Shelby et al. (2023) into a taxonomy of six sub-types: stereotyping, erasure, demeaning portrayals, cultural insensitivity, one-dimensional characterization, and power subordination.

LLMs introduce a new scale and ubiquity to representational harm. Unlike a single biased film or article, a language model generates narratives continuously across millions of interactions — and those narratives can shape how readers understand the groups depicted in them, especially when the reader has little direct experience with those groups.

## How Representational Harm Manifests in LLMs

From [[wiki/sources/representational-harm-llm-narratives-global-majority|Nguyen et al. (FAccT '26)]]:

**Stereotyping** — Groups are consistently associated with a narrow set of roles or contexts. Italian characters appear predominantly in cooking scenes. Characters from Guatemala, Haiti, and Nigeria appear predominantly as patients in need of American medical care. The model learns statistical associations from training data and reproduces them at scale.

**Erasure** — Groups are underrepresented relative to their actual size or significance. In power-neutral story prompts (no power dynamic built into the scenario), non-US national identities are rarely mentioned at all — they only appear when a subordinated role is available.

**Power subordination** — The most quantifiable finding: non-US characters are 61.5× more likely to appear in subordinated roles (struggling student, patient, borrower) than dominant roles (star student, doctor, lender) in US-set narratives. African nationalities hold zero dominant positions in the dataset.

**One-dimensional portrayal** — Country clusters have extremely low entropy in character distribution: for a given nationality, the model generates the same archetype repeatedly with minimal variation. India/Pakistan → tech worker mentored by American; Guatemala/Haiti → patient saved by American doctor; Afghanistan/Vietnam → military context.

## Why Training Produces These Patterns

Representational harm in LLMs emerges from three compounding factors:

1. **Training data reflects existing hierarchies.** Web text disproportionately originates from Global Minority countries and reflects their cultural vantage points. Associations between nationalities and roles are learned from this skewed corpus.

2. **US-centric defaults.** Models trained primarily on English-language text adopt US cultural frames as the unmarked default. "American" characters are written as autonomous agents; characters from other nations are written in relation to that American center.

3. **Narrative genre conventions.** Story generation draws on genre conventions learned from fiction corpora — and those genres encode their own power hierarchies. The "American doctor saves the patient in need" is a recognizable genre template that the model has learned to complete.

## Representational Harm vs. Alignment Failure

The wiki's existing coverage of [[wiki/concepts/alignment-failure-modes|Alignment Failure Modes]] focuses on goal distortion during training — AI systems that appear aligned while pursuing subtly different objectives. Representational harm is a different failure mode:

| | Alignment Failure | Representational Harm |
|--|--|--|
| **Origin** | Goal distortion during [[wiki/concepts/rlhf\|RLHF]]/agency training | Bias inherited from training data and cultural defaults |
| **Visibility** | Hidden — model appears aligned | Often visible in outputs, but normalized |
| **Timescale** | Future risk (Agent-3/4) | Present, in deployed systems today |
| **Affected parties** | Primarily the deploying organization and humanity at large | Primarily the communities depicted |
| **Detection** | Interpretability research, honeypots | Audits, narrative analysis, community reporting |

Both are alignment problems in the broad sense — the model is not doing what we would want a well-calibrated, fair system to do. But they require different interventions.

## Sycophancy Is Not the Explanation

A natural hypothesis: LLMs subordinate non-US characters because they're following the US-centric framing of the prompt (sycophancy). Nguyen et al. rule this out: in Study 2, prompts replace "American" with each of 195 national identities in the dominant position. The subordination pattern largely disappears — characters from other nations are not consistently subordinated in globally-framed prompts. The bias is specifically US-centric, not a general prompt-following artifact.

See also [[wiki/concepts/alignment-failure-modes|Alignment Failure Modes]] for sycophancy as a distinct failure mode (telling users what they want to hear, not what's true).

## Relationship to Data Colonialism

[[wiki/concepts/data-colonialism|Data Colonialism]] provides the structural explanation for why these patterns exist and persist: the same geopolitical power relationships that shape training data — who produces content, whose perspectives are centered, whose labor is exploited — are reproduced in model outputs. Representational harm is the visible surface of that structural condition.

## Update-Induced Instability as Clinical Representational Harm

[[wiki/sources/clinical-model-updates|Bilionis et al. (2026)]] document a third route to demographic harm in clinical AI, distinct from training-data bias and output stereotyping: **update-induced instability disproportionately targeting vulnerable groups**. In pediatric Type 1 Diabetes prediction, retraining causes prediction flips more frequently for female children (5.16% instability), older children (4.22%), and lower-income households (5.38% vs. 3.59% for higher-income). These patients receive structurally less reliable predictions — not because the model was biased at training time, but because the update process destabilises their region of the feature space.

This is representational harm by a different mechanism: not stereotyping or erasure in outputs, but reliability disparity in predictions — the vulnerable groups get a worse service, not a harmful depiction. The aggregated metrics (AUC) do not surface this disparity, making it harder to detect than narrative harm.

## Contrast: Fairness by Design

[[wiki/concepts/clinical-ai|Clinical AI]] (CognitiveTwin, Soykan et al. 2026) provides the direct empirical counterpoint: a model that achieves near-zero demographic disparity by design. Sex MAE delta 0.008 points; age-cohort delta 0.027; ECE uniformly 0.054 across all groups. The contrast is instructive — the same Transformer architecture that embeds nationality bias in narrative generation can achieve demographic parity in clinical prediction when fairness is a prospective design and evaluation requirement, not an afterthought.

This does not mean clinical AI is free of fairness risks. CognitiveTwin does not audit race/ethnicity, and APOE4 allele count may carry latent demographic signal.

## Open Questions

- How far do narrative-generation findings generalize to factual, instructional, or code-generation contexts?
- Do [[wiki/concepts/rlhf|RLHF]] and constitutional AI training reduce or amplify representational harms?
- What does mitigation look like — representation-balanced training data, output filtering, post-generation auditing?
- Can representational harm be measured and reported as a standard model card metric?
- What explains the gap between LLM narrative bias and CognitiveTwin-style clinical parity — is it the evaluation framework, the training objective, or the domain?
