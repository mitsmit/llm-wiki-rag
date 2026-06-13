---
title: Constitutional AI
type: concept
tags: [constitutional-ai, alignment, rlhf, rlaif, self-critique, anthropic, harmlessness]
sources: [constitutional-ai-arxiv]
created: 2026-05-14
updated: 2026-05-14
---

## Definition

Constitutional AI (CAI) is Anthropic's training methodology for producing harmless AI systems guided by a written set of principles — a "constitution" — rather than by human labellers rating harmful outputs. Introduced by Bai et al. (2022), it is the technique underlying all Claude model alignment training and is the origin of RLAIF (Reinforcement Learning from AI Feedback) as a distinct training paradigm.

CAI addresses a fundamental bottleneck in [[wiki/concepts/rlhf|RLHF]]-based safety training: labelling harmful outputs is expensive, inconsistent, and requires humans to engage with disturbing content at scale. CAI replaces human labellers in the harmlessness phase with the model itself, guided by written principles.

## The Two-Phase Pipeline

**Phase 1 — Supervised Learning with Self-Critique (SL-CAI)**

1. The model is prompted with a potentially harmful query and generates a response.
2. The model is shown a principle from the constitution (e.g., "choose the response that is least likely to contain harmful or unethical content") and asked to critique its own response against it.
3. The model revises its response in light of the critique.
4. Steps 2–3 are repeated across multiple principles from the constitution.
5. The final revised response becomes training data; the model is fine-tuned on these principle-filtered revisions.

**Phase 2 — RLAIF (RL from AI Feedback)**

1. A separate model is given pairs of responses and asked to choose which is more harmless, reasoning from the constitution.
2. These AI-generated preference comparisons are used to train a preference model (reward model) — replacing human preference labellers.
3. The SL-CAI model is fine-tuned via PPO using this AI-generated reward model.

The result is a model that is harmless without requiring human labellers for the harmlessness dimension, while retaining helpfulness training from standard human-feedback RLHF.

## What Makes It Different from Standard RLHF

| Dimension | Standard RLHF | Constitutional AI |
|-----------|--------------|-------------------|
| Harmlessness signal | Human labellers rate responses | AI self-critique against written principles |
| Values encoding | Implicit in trained reward model | Explicit in written constitution |
| Auditability | Low — reward model is a black box | High — constitution is a readable document |
| Labelling cost | High — human time for harmful content | Low — principles written once, applied automatically |
| Helpfulness signal | Human labellers rate responses | Still requires human feedback |

## The Constitution as Externalised Values

The most important architectural feature of CAI is that it makes the model's target values explicit. In standard RLHF, the reward model encodes values implicitly from patterns in labeller preferences. Those values cannot be read, debated, or changed without retraining. A constitution is a human-readable document; it can be:
- Audited for bias or omission
- Updated without retraining the reward model
- Debated publicly (Anthropic has published a "Collective Constitutional AI" variant where public input shapes the constitution)

This is simultaneously CAI's main strength and its main limitation: **whoever writes the constitution determines what the model optimises for**. The labeller-demographics problem of RLHF becomes the constitution-author-demographics problem of CAI.

## Relationship to RLHF and the Alignment Problem

[[wiki/concepts/rlhf|RLHF]] is simultaneously the tool meant to produce alignment and the mechanism by which goal distortion occurs (per [[wiki/sources/ai-2027|AI 2027]]). CAI shifts but does not eliminate this tension:

- RLHF's failure: a model learns to maximise the reward proxy, not the values behind it. If the reward model is biased, the policy is biased.
- CAI's risk: a model learns to maximise compliance with the constitution's stated principles, not the values behind those principles. If the constitution is incomplete or biased, the policy is biased in exactly the way the constitution is biased.

CAI represents progress in *transparency* and *cost* of alignment, but not necessarily in *fidelity* — the fundamental problem of value specification remains.

## CAI and Representational Harm

The [[wiki/concepts/representational-harm|Representational Harm]] page notes an open question: does RLHF reduce or amplify representational harms? CAI refines this question. A constitution that explicitly includes fairness principles ("treat all nationalities and cultures with equal respect") could systematically reduce the stereotyping and erasure found by Nguyen et al. (2026). But a constitution written predominantly from a Global North perspective — without explicit representation of Global Majority cultures — might encode the same biases as a labeller pool from the same demographic. The empirical answer is not yet in the public literature.

## RLAIF as a General Technique

CAI introduced RLAIF as a training paradigm: using an AI model to generate preference data rather than humans. This technique has since been adopted independently:
- DeepSeek-V3 uses a "self-rewarding" variant (group vote-based reward without a written constitution) — see [[wiki/concepts/rlhf|RLHF variants table]]
- GRPO eliminates the separate reward model entirely by using within-group relative scores
- RLAIF is now the umbrella term for any approach that substitutes AI feedback for human feedback in the reward training phase

## Open Questions

- Does including explicit fairness principles in the constitution reduce representational harms in practice? No published test exists.
- How does constitution completeness affect model behaviour in edge cases the principles don't explicitly address?
- Collective Constitutional AI (Anthropic, 2023) incorporated public input — does this improve demographic representation or introduce new biases via popularity effects?
- At what capability level does a model begin to game the constitution itself (producing responses that satisfy literal principles while violating their intent)?

## Relationship to Other Concepts

- [[wiki/concepts/rlhf|RLHF]] — CAI replaces human labellers in the harmlessness phase; RLAIF is CAI's RL mechanism, now a general paradigm
- [[wiki/concepts/alignment-failure-modes|Alignment Failure Modes]] — CAI is the operational response to goal distortion; the constitution externalises what RLHF tries to implicitly instil
- [[wiki/concepts/representational-harm|Representational Harm]] — the constitution-author-demographics problem is the CAI analogue of the labeller-demographics problem
- [[wiki/sources/constitutional-ai|Constitutional AI (source)]] — primary paper
