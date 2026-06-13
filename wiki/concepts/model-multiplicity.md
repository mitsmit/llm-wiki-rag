---
title: Model Multiplicity and the Rashomon Set
type: concept
tags: [model-multiplicity, rashomon-set, arbitrariness, stability, clinical-ai, fairness]
sources: [clinical-model-updates]
created: 2026-04-28
updated: 2026-04-28
---

## Definition

**Model multiplicity** refers to the existence of multiple models that achieve near-identical aggregate performance (accuracy, AUC) on a given task while making meaningfully different predictions for individual inputs. The **Rashomon set** is the formal name for this family of near-optimal models — all models within an acceptable performance tolerance of the best model.

The practical implication: when a model is selected from the Rashomon set by the training process (which depends on random initialisation, data ordering, hyperparameter choices, or minor implementation differences), the choice is effectively **arbitrary** from a performance standpoint but **consequential** at the individual level. Two patients with identical clinical profiles may receive different predictions depending on which near-equally-good model was chosen.

## Why This Matters for Clinical AI

In most ML deployments, model selection from the Rashomon set is treated as a technical detail — pick the model with the highest validation AUC and deploy it. In clinical contexts, this is a governance failure:

- A patient's predicted risk category may depend on which random seed was used during training
- Two patients from different demographic groups may be affected unequally by this arbitrary selection
- After retraining, a new model is selected from the (updated) Rashomon set — predictions can flip for individual patients even when aggregate AUC is unchanged

[[wiki/sources/clinical-model-updates|Bilionis et al. (2026)]] quantify this concretely: under full cumulative retraining on pediatric T1D data, the **prediction disagreement rate (DR) among near-optimal models is 20–32%**. Roughly one in four individual predictions would differ depending on which well-performing model was chosen. The number of distinct predictive patterns (DPR) ranges from 1 to 7 across datasets and retraining phases.

## Rashomon Set Metrics

| Metric | Definition | Interpretation |
|--------|-----------|----------------|
| Distinct Predictive Patterns (DPR) | Number of unique prediction vectors within the Rashomon set | How many behaviourally different models are equally valid |
| Prediction Disagreement Rate (DR) | Expected pairwise prediction mismatch across Rashomon set members | Fraction of individuals who would receive different predictions from different well-performing models |
| Systematic Arbitrariness (SA) | DR disparity between protected groups | Whether arbitrary model selection harms some demographic groups more than others |

## Relationship to Stability and Fairness

Model multiplicity interacts with the other two risk dimensions identified in Bilionis et al.:

**Multiplicity → Arbitrariness**: When DR is high, retraining with the same algorithm on the same data (but different random state) selects a different member of the Rashomon set. Individual predictions change not because the patient's condition changed, but because the training process made a different arbitrary choice.

**Multiplicity → Fairness risk**: If the Rashomon set contains models that perform similarly overall but differ systematically in their treatment of protected subgroups, model selection from that set has implicit fairness consequences. A high-DR Rashomon set is a signal that no single model reliably represents the right answer — and that which "right answer" the system provides may depend on factors irrelevant to the patient.

**Multiplicity + Temporal updates = compounding instability**: At each retraining phase, a new model is selected from the updated Rashomon set. If DR remains at 20–32%, patients experience prediction variability not just from true clinical changes but from accumulated arbitrary selections across update cycles.

## Relationship to World Modeling and Agentic AI

Model multiplicity is not limited to clinical settings. In agentic AI systems, the same phenomenon appears as **non-deterministic agent behaviour under repeated sampling**: two runs of the same agentic task with the same inputs but different random seeds produce different results — the [[wiki/sources/token-consumption-agentic-coding|30× per-run token variability]] documented by Bai et al. (2026) is partly an expression of this. The agentic equivalent of DR is the fraction of task steps where the agent makes different choices under different sampling conditions despite identical context.

In the [[wiki/concepts/world-modeling|World Modeling]] framework, L2 systems (simulators that plan before acting) should be less susceptible to arbitrariness than L1 systems (reactive predictors), because planning under a world model is more deterministic than sampling from a distribution of equally-plausible next actions.

## Open Questions

- Is there a principled way to select from the Rashomon set that minimises arbitrariness for protected groups — e.g., choosing the model that minimises within-set prediction variance across demographic subgroups?
- Does model multiplicity scale with model complexity — do larger, more expressive models have larger or smaller Rashomon sets?
- In the context of AI scientists ([[wiki/concepts/ai-for-scientific-discovery|MolClaw]], OMC research survey), does the Rashomon set phenomenon appear in research output — multiple equally-valid research strategies that lead to different conclusions?
- Can the Rashomon set analysis be operationalised as a routine pre-deployment audit for clinical AI models?

## Relationship to Other Concepts

- [[wiki/concepts/clinical-ai|Clinical AI]] — model multiplicity is a governance risk in clinical deployment; the Rashomon set analysis is a proposed audit tool
- [[wiki/sources/clinical-model-updates|Clinical Model Updates]] — primary source; quantifies DR at 20–32% under full cumulative retraining of pediatric T1D models
- [[wiki/concepts/representational-harm|Representational Harm]] — Systematic Arbitrariness (SA) captures whether arbitrary model selection harms protected subgroups more than others
- [[wiki/concepts/world-modeling|World Modeling]] — L2 simulation capability may reduce agentic analogs of arbitrariness by providing more deterministic planning
