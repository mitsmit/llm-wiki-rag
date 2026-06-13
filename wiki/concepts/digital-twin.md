---
title: Digital Twin
type: concept
tags: [digital-twin, clinical-ai, simulation, personalised-modelling]
sources: [cognitivetwin]
created: 2026-04-28
updated: 2026-04-28
---

## Definition

A digital twin is a dynamic computational replica of a physical system that evolves continuously alongside its real-world counterpart by integrating live data streams. Originally developed in aerospace and manufacturing (equipment monitoring, predictive maintenance), the concept has migrated to healthcare, where a **cognitive digital twin** aims to mirror a patient's underlying pathophysiology — synthesising multi-modal clinical data to forecast personalised disease trajectories.

The defining features that distinguish a digital twin from a conventional predictive model:

| Feature | Conventional model | Digital twin |
|---------|--------------------|-------------|
| Scope | Population-level statistics | Individual-level personalised model |
| Updating | Static; retrained on batch | Continuously updated with new observations |
| Output | Point prediction | Full trajectory with calibrated uncertainty |
| Latent state | None (or implicit) | Explicit latent state tracking underlying system state |
| Missing data | Imputed or excluded | Propagated through latent state dynamics |

## CognitiveTwin Implementation

[[wiki/sources/cognitivetwin|CognitiveTwin (Soykan et al., 2026)]] is the wiki's primary instantiation of a medical digital twin. Its architecture implements the digital twin pattern:

- **Multi-modal data fusion** (Transformer): integrates cognitive scores, MRI volumetrics, PET/CSF biomarkers, and APOE4 genetics into a unified 256-dimensional patient state representation at each visit
- **Latent state tracking** (Deep Markov Model): maintains a 64-dimensional probabilistic latent disease state `z_t` that evolves via learned non-linear transition dynamics — modelling the underlying pathophysiology (amyloid accumulation, tau spread, neurodegeneration) rather than just the observable symptoms
- **Calibrated uncertainty**: the variational posterior produces 95% prediction intervals that accurately bound individual patient trajectories
- **MNAR handling**: bidirectional inference allows the model to infer latent state from future observations when current-visit data is missing

The paper demonstrates individual-level trajectory forecasting — tracking a single high-risk patient's 22-point MMSE decline over 40 months with the true trajectory within the 95% interval throughout.

**Current limitation**: CognitiveTwin is evaluated as a static batch-trained model. True digital twin operation requires online updating as new patient data arrives — the paper establishes the architecture but not the deployment loop.

## Relationship to World Modeling

The Deep Markov Model in CognitiveTwin is structurally related to the [[wiki/concepts/world-modeling|World Modeling]] framework (Chu et al., 2026):

- The DMM is an L1 predictor in the world modeling taxonomy — it predicts the next disease state given the current latent state
- A genuine clinical digital twin that could simulate counterfactual trajectories ("what happens if we start this treatment?") would require L2 simulation capability
- An L3-level clinical digital twin would revise its own disease model as new biomarker data accumulates

CognitiveTwin is at the L1 boundary — it predicts but does not yet support intervention simulation or self-revision.

## Relationship to Other Concepts

- [[wiki/concepts/clinical-ai|Clinical AI]] — the deployment context; digital twin is the patient modelling paradigm within clinical AI
- [[wiki/concepts/world-modeling|World Modeling]] — structural parallel: DMM = disease state predictor; L2 would add treatment counterfactual simulation
- [[wiki/concepts/transformer-architecture|Transformer Architecture]] — the cross-modal fusion layer enabling the patient state representation
