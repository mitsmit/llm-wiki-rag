---
title: Clinical AI
type: concept
tags: [clinical-ai, healthcare, fairness, digital-twin, alzheimer, deployment]
sources: [cognitivetwin]
created: 2026-04-28
updated: 2026-04-28
---

## Definition

Clinical AI refers to AI systems designed for deployment in healthcare contexts — diagnosis, prognosis, treatment planning, and patient monitoring. Relative to research AI or agentic task-completion systems, clinical AI carries additional requirements: calibrated uncertainty (the model must know what it doesn't know), demographic fairness across patient populations, robustness to the messy realities of clinical data (missing values, irregular sampling, informative dropout), and interpretability sufficient for clinician decision support.

Clinical AI is distinct from [[wiki/concepts/ai-for-scientific-discovery|AI for Scientific Discovery]] in both purpose and constraint. Scientific AI targets knowledge production; clinical AI targets patient outcomes. Scientific AI tolerates false positives and iteration; clinical AI requires reliability under distribution shift and must not harm identifiable demographic groups.

## Requirements for Clinical Deployment

| Requirement | Why it matters | Failure mode |
|-------------|----------------|-------------|
| Predictive accuracy | Drives correct clinical decisions | Misclassified risk; missed progression |
| Calibrated uncertainty | Risk score must match empirical frequency | Overconfident predictions lead to wrong interventions |
| Demographic fairness | All patient populations must receive equitable care | Higher error for minority groups reinforces care gaps |
| MNAR robustness | Clinical data is missing non-randomly (sicker patients miss visits) | Model degrades precisely for the patients who need it most |
| Interpretability | Clinicians must understand and trust predictions | Black-box opacity blocks adoption |

## CognitiveTwin: Primary Example

[[wiki/sources/cognitivetwin|CognitiveTwin (Soykan et al., 2026)]] is the primary clinical AI paper in the wiki. It addresses all five requirements for Alzheimer's disease cognitive trajectory prediction:

- **Accuracy**: MAE 1.619 MMSE points (24-month), approaching the 1.5–2.0 test-retest floor of the instrument
- **Calibration**: ECE 0.054 uniformly across demographic groups — the probabilistic uncertainty estimates carry the same clinical meaning for every patient
- **Fairness**: Sex MAE delta 0.008 points; age-cohort delta 0.027 points; zero ECE disparity
- **MNAR robustness**: 0.3% MAE degradation under 15% informative missingness (MRI dropped for cognitively impaired patients)
- **Architecture transparency**: Transformer attention weights and DMM latent trajectories are in principle interpretable, though the paper does not present attention visualisations

## Fairness as a Design Requirement vs. Harm as an Emergent Property

CognitiveTwin provides the direct empirical counterpoint to [[wiki/concepts/representational-harm|Representational Harm]]:

| | Representational Harm (Nguyen et al.) | Clinical AI Fairness (CognitiveTwin) |
|--|--------------------------------------|--------------------------------------|
| Source of disparity | Embedded in training data and [[wiki/concepts/rlhf\|RLHF]] objectives | Architectural and evaluation choices |
| Demographic dimension | Global Majority nationality | Sex, age cohort |
| Disparity direction | Systematic bias against marginalised groups | Near-zero disparity by design |
| Detection | Post-hoc evaluation of outputs | Prospective fairness audit built into evaluation framework |
| Implication | Harm is systemic and hard to fix | Fairness is achievable with deliberate design |

The contrast does not mean clinical AI is free of fairness risks. CognitiveTwin does not audit race/ethnicity fairness, and APOE4 allele count is a genetic proxy that may carry latent demographic signal. The paper shows parity within the axes it tests, not across all axes.

## Missing Not At Random (MNAR)

A key clinical data challenge: missingness is informative. Patients with severe cognitive decline miss neuroimaging appointments specifically *because* they are declining — the very patients the model most needs to predict accurately. Standard models that assume missingness is random (MCAR) systematically degrade for this high-risk subgroup.

CognitiveTwin addresses MNAR through the Deep Markov Model's bidirectional inference: the model infers latent disease state from observations at `t+1, t+2, ...` even when `t` is missing. This is architecturally different from imputation-based approaches, which fill missing values before modelling.

## Model Update Risks: The Deployment Lifecycle

[[wiki/sources/clinical-model-updates|Bilionis et al. (2026)]] provide the operational companion to CognitiveTwin: while CognitiveTwin addresses initial training quality, this paper addresses what happens when a deployed clinical model must be updated as training data goes stale. Three risk dimensions emerge that aggregate AUC cannot detect:

**Stability**: Individual-patient predictions flip between retraining phases. Flip rates of 0–7% per retraining cycle; low temporal self-consistency (TSC) affects 31.9% of patients on average. A patient may be classified high-risk this week and low-risk next week, not because their condition changed but because the model was retrained on new data.

**Arbitrariness**: Multiple near-equally-accurate models (the Rashomon set) disagree on 20–32% of individual predictions. Which member of this set is deployed is determined by random initialisation and data ordering — effectively arbitrary from a performance standpoint, but consequential for the patient. See [[wiki/concepts/model-multiplicity|Model Multiplicity]].

**Fairness drift**: Update strategies affect demographic groups differently, and in contradictory directions across fairness criteria. Last-batch retraining — the simplest strategy — consistently amplifies subgroup disparities. Critically, instability disproportionately targets vulnerable groups: older children, female children, and patients from lower-income and lower-education households show the highest flip rates and lowest TSC.

**The core finding**: performance-preserving updates do not imply stable or equitable individual-level decisions. Standard monitoring (tracking aggregate AUC across updates) misses all three risk dimensions. The paper proposes a governance framework — tracking stability, arbitrariness, multiplicity, and uncertainty metrics alongside accuracy — as a prerequisite for safe clinical AI deployment.

**Regulatory gap**: FDA's Predetermined Change Control Plan (PCCP) acknowledges the problem; almost no approved AI medical devices report post-deployment retraining in practice.

## Connection to the Intelligence Explosion

Clinical AI does not feature in the [[wiki/sources/ai-2027|AI 2027]] timeline directly, but it sits at the intersection of two of the wiki's threads:

1. **AI for scientific discovery**: If AI scientists can automate research across domains (ResearchAgent, TAIS, MolClaw), healthcare is among the most consequential targets. CognitiveTwin is what the precursor-stage clinical AI looks like before research automation arrives.

2. **Present harms**: Representational harm in LLM outputs is one form of AI harm. Demographic bias in clinical AI is another — and arguably higher stakes, since clinical models make decisions about individual patient care, not just narrative descriptions.

## Open Threads

- CognitiveTwin demonstrates parity across sex and age but does not assess race/ethnicity — the most consequential axis of healthcare AI fairness given documented disparities in Alzheimer's diagnosis and care access
- APOE4 allele count may encode latent racial signal; the paper does not test for this
- External validation on non-ADNI, real-world clinical cohorts is absent — TADPOLE is a research dataset with higher data quality than typical EHR data
- The digital twin framing implies continuous patient-specific updating; the paper evaluates static training; the gap between batch-trained and online-updating systems is now directly addressed by Bilionis et al. — continuous updating requires the governance framework they propose
- At what capability level does clinical AI become an AI scientist in the medical domain — and what safeguarding framework applies at that point?
- Bilionis et al. find that conformal abstention can simultaneously improve one fairness criterion and worsen another — is there a principled way to choose between fairness criteria in clinical deployment?
- Last-batch retraining is worst on all dimensions yet is the most common practice — what organisational and regulatory factors explain this gap?

## Relationship to Other Concepts

- [[wiki/concepts/digital-twin|Digital Twin]] — the patient modelling paradigm underlying CognitiveTwin
- [[wiki/concepts/transformer-architecture|Transformer Architecture]] — cross-modal self-attention is the fusion mechanism; modality-type embeddings extend the language model paradigm to heterogeneous clinical data
- [[wiki/concepts/representational-harm|Representational Harm]] — the inverse case: demographic parity by design vs. demographic bias by omission
- [[wiki/concepts/ai-for-scientific-discovery|AI for Scientific Discovery]] — clinical AI is adjacent but distinct; the convergence point is AI-automated medical research
- [[wiki/concepts/model-multiplicity|Model Multiplicity]] — the Rashomon set analysis is a governance tool for clinical AI update cycles; 20–32% DR under full cumulative retraining
- [[wiki/sources/clinical-model-updates|Clinical Model Updates]] — empirical evaluation of stability, arbitrariness, and fairness risks during continual retraining; operational companion to CognitiveTwin
