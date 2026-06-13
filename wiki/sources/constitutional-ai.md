---
title: "Constitutional AI: Harmlessness from AI Feedback"
type: source
tags: [constitutional-ai, alignment, rlhf, rlaif, harmlessness, anthropic, self-critique]
sources: [constitutional-ai-arxiv]
created: 2026-05-14
updated: 2026-05-14
---

## Summary

Bai, Kadavath, Kundu, Askell et al. (Anthropic, December 2022) introduce Constitutional AI (CAI), a training methodology for producing harmless AI systems without requiring human labellers to identify harmful outputs. The method replaces the human-labelling step of RLHF harmlessness training with a written "constitution" — a list of principles — that the model uses to critique and revise its own outputs.

The core insight is that writing principles is cheaper than labelling responses, and that a sufficiently capable model can self-apply those principles to generate training signal. This reduces the human bottleneck in safety training while also making the model's values explicit and auditable — the constitution can be read, debated, and updated by humans, unlike the implicit values encoded in a trained reward model.

The resulting model is "harmless but non-evasive": rather than refusing harmful queries with blanket refusals, it engages with the query and explains its objections. Anthropic describes this as a step toward making AI systems that can be aligned through written values rather than extensive human labelling.

## Key Concepts

- [[wiki/concepts/constitutional-ai|Constitutional AI]] — the full concept page for this methodology
- [[wiki/concepts/rlhf|RLHF]] — CAI replaces the human-labelling phase of harmlessness RLHF; RLAIF (RL from AI Feedback) is CAI's RL phase
- [[wiki/concepts/alignment-failure-modes|Alignment Failure Modes]] — CAI is Anthropic's operational response to the goal-distortion problem; the constitution externalises the values that RLHF tries to implicitly instil

## Key Entities

- Anthropic — developed CAI; it underpins all Claude model alignment training

## Notable Claims

- **SL-CAI (Supervised phase)**: The model generates a response to a potentially harmful prompt, then critiques it against a principle from the constitution, then revises the response to be less harmful. Repeat across principles. Fine-tune on the revised responses.
- **RLAIF (RL phase)**: Use a separate model to compare pairs of responses on harmlessness (guided by the constitution), generating preference data without human labellers. Train a preference model on these AI-generated comparisons; use it as a reward signal for PPO.
- **Chain-of-thought feedback**: Using reasoning traces during the AI feedback phase improves the quality of the preference model and makes the model's reasoning about harmlessness more transparent.
- **Human labels still needed for helpfulness**: CAI only replaces human labelling for *harmlessness*. Helpfulness training still relies on human feedback. The method does not claim to eliminate human oversight entirely.
- **Constitution = auditable values**: Unlike a trained reward model, the constitution is a human-readable document. Its contents determine what the model optimises for; this is both a feature (transparency) and a risk (who writes it, from whose perspective).

## Contradictions / Open Questions

- The constitution itself encodes values — who writes it, and whose perspective does it represent? CAI shifts the value-encoding problem from labellers to constitution authors, but does not eliminate it. See [[wiki/concepts/rlhf|RLHF]] open question: does CAI reduce or amplify representational harms?
- CAI was published in 2022; the wiki's RLHF page already notes CAI as Anthropic's method and DeepSeek's self-rewarding variant as analogous. The relationship between the original CAI, RLAIF, and GRPO needs explicit mapping.
- Empirical evidence that the resulting model is "harmless but non-evasive" (rather than just less refusal-happy) is model-scale dependent; no data on whether CAI-trained models at smaller scales show the same profile.

## Raw Source

`raw/2026-04-28-research.md` (link: https://arxiv.org/abs/2212.08073)
