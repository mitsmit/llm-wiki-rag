---
title: "CognitiveTwin: Robust Multi-Modal Digital Twins for Predicting Cognitive Decline in Alzheimer's Disease"
type: source
tags: [clinical-ai, digital-twin, alzheimer, multi-modal, fairness, deep-markov-model, transformer]
sources: [cognitivetwin]
created: 2026-04-28
updated: 2026-04-28
---

## Summary

CognitiveTwin (Soykan, Hancerliogullari Koksalmis, Huang, Brattain; University of Toledo + University of Central Florida, 2026) is a clinical AI framework for predicting individualised cognitive decline trajectories in Alzheimer's disease. It frames each patient as a **digital twin** — a personalised computational model that evolves alongside the real patient — rather than fitting a population-level statistical average.

The architecture combines a Transformer-based multi-modal fusion layer (integrating cognitive scores, MRI volumetrics, PET/CSF biomarkers, and APOE4 genetics) with a Deep Markov Model (DMM) that captures the non-linear temporal dynamics of disease progression as a probabilistic latent variable sequence. The DMM provides calibrated uncertainty estimates and handles missing-not-at-random (MNAR) data naturally — both critical for clinical deployment.

Evaluated on TADPOLE (1,666 ADNI patients), the full model achieves MAE 1.619 MMSE points for 24-month prediction — approaching the 1.5–2.0 point test-retest floor of the instrument itself — and AUROC 0.912 for binary rapid-progression classification. It substantially outperforms all baselines (LSTM, CNN-LSTM, plain Transformer, GNN). Demographic fairness is near-perfect: sex MAE delta 0.008 points; age-cohort MAE delta 0.027 points; ECE uniformly 0.054 across all groups. Under 15% MNAR (MRI dropped for cognitively impaired patients, the realistic clinical dropout pattern), MAE degrades only 0.3%.

Source code and data: `github.com/bulentsoykan/cognitivedt`, `pypi.org/project/cognitive-digital-twin`.

## Architecture

### Multi-Modal Fusion (Transformer)

Four input modalities, 32 total features per visit:

| Modality | Features | Completeness |
|----------|----------|--------------|
| Cognitive scores | 9 (MMSE, ADAS-Cog 11/13, CDR-SB, RAVLT, FAQ) | 98.7% |
| Biomarkers | 15 (FDG/AV45 PET, Aβ42/tau/p-tau CSF, demographics) | 35.8–42.1% |
| Neuroimaging (MRI) | 7 (hippocampus, ventricles, temporal/fusiform, entorhinal cortex) | 76.3% |
| Genetics | 1 (APOE4 allele count) | — |

Each modality is projected to a 256-dimensional embedding with a learned modality-type embedding (analogous to token-type embeddings in BERT). Four Transformer encoder layers with 8 attention heads perform cross-modal self-attention at each visit, allowing the model to dynamically re-weight modalities based on clinical context (e.g., prioritising amyloid PET when cognitive scores are stable). Mean pooling across modality tokens produces a 256-dim fused patient state per visit.

A boolean mask tensor travels alongside the feature tensors, explicitly encoding missingness — the attention mechanism can attend to this signal rather than treating missingness as zero-filling.

### Deep Markov Model (DMM)

The fused representations feed into a DMM with 64-dimensional latent states. The DMM formulates disease progression as a generative process:

- **Prior transition**: `p_θ(z_t | z_{t-1})` — gated MLP that mixes linear preservation (stability periods) and non-linear transformation (rapid decline phases)
- **Emission**: `p_θ(x_t | z_t)` — 3-layer MLP projecting latent state back to 256-dim fused space, then to MMSE prediction
- **Inference**: Bidirectional GRU over the full sequence produces a posterior `q_ϕ(z_t | z_{t-1}, x_{1:T})` — using both past and future observations to infer current latent state

The variational ELBO is minimised jointly with the supervised prediction loss. The bidirectional inference network means that even when a modality is missing at time `t`, the model can use observations at `t+1, t+2, ...` to infer the latent state — this is the mechanism behind MNAR robustness.

### Training Configuration

| Component | Value |
|-----------|-------|
| Transformer: d_model | 256 |
| Transformer: heads | 8 |
| Transformer: layers | 4 |
| DMM: latent dim | 64 |
| Total parameters | 3.2M |
| Optimizer | AdamW, lr=8×10⁻⁴ |
| Regularisation | Dropout 0.15, cosine annealing, early stopping (patience=10) |

## Results

### Primary Performance (TADPOLE, n=252 test patients)

| Method | MAE ↓ | RMSE ↓ | R² ↑ | AUROC ↑ |
|--------|--------|---------|------|---------|
| LSTM | 3.420 | 4.680 | 0.220 | 0.730 |
| CNN-LSTM | 3.180 | 4.510 | 0.280 | 0.760 |
| Transformer | 2.940 | 4.230 | 0.350 | 0.780 |
| Graph Neural Net | 2.670 | 3.980 | 0.410 | 0.810 |
| **CognitiveTwin** | **1.619** | **2.248** | **0.682** | **0.912** |

MAE 1.619 approaches the 1.5–2.0 MMSE test-retest variability floor — the model's residual error is largely irreducible clinical noise rather than algorithmic bias.

### Demographic Fairness

| Group | MAE | AUROC | ECE |
|-------|-----|-------|-----|
| Overall | 1.619 | 0.912 | 0.054 |
| Male | 1.622 | 0.920 | 0.054 |
| Female | 1.614 | 0.893 | 0.054 |
| Age <65 | 1.608 | — | 0.054 |
| Age 65–75 | 1.619 | — | 0.054 |
| Age >75 | 1.635 | — | 0.054 |
| Max sex delta | 0.008 | 0.027 | 0.000 |
| Max age delta | 0.027 | — | 0.000 |

ECE 0.054 uniformly across all groups: the model's risk estimates carry the same clinical meaning for every patient.

### MNAR Robustness

Under 15% MNAR (MRI features masked for patients with MMSE <24 — the realistic clinical dropout pattern):
- MAE: 1.619 → 1.625 (+0.3%)
- AUROC: 0.912 → 0.910

### Ablation Study

| Configuration | MAE | AUROC | MAE Degradation |
|---------------|-----|-------|-----------------|
| Full CognitiveTwin | 1.619 | 0.912 | — |
| No DMM dynamics | 1.749 | 0.866 | +8.0% |
| No APOE4 genetics | 1.700 | 0.884 | +5.0% |
| Single modality (cognitive only) | 1.862 | 0.839 | +15.0% |
| Baseline (no fusion, no DMM) | 3.080 | 0.363 | +90.2% |

Multi-modal fusion is the decisive component (+90.2% without it); DMM temporal dynamics are the second key contributor (+8.0%).

## Key Concepts

- [[wiki/concepts/clinical-ai|Clinical AI]] — CognitiveTwin is the primary example in the wiki of clinical AI: AI deployed in a healthcare context with explicit fairness and robustness requirements
- [[wiki/concepts/digital-twin|Digital Twin]] — CognitiveTwin operationalises the digital twin concept in medicine: a personalised computational model evolving alongside the patient
- [[wiki/concepts/transformer-architecture|Transformer Architecture]] — cross-modal self-attention is the mechanism that enables CognitiveTwin's multi-modal fusion; modality-type embeddings parallel token-type embeddings in language models
- [[wiki/concepts/representational-harm|Representational Harm]] — CognitiveTwin provides a direct empirical contrast: demographic parity by design, rather than demographic bias embedded in outputs

## Notable Claims

- MAE 1.619 approaches the MMSE test-retest floor — residual error is largely irreducible rather than algorithmic
- Demographic fairness: ECE 0.054 uniformly across sex and age cohorts — the model's uncertainty estimates are equally reliable for all patients
- MNAR robustness: only 0.3% MAE degradation under realistic clinical dropout — the DMM propagates latent state from remaining modalities
- Multi-modal fusion is the decisive architectural choice: removing it collapses AUROC from 0.912 to 0.363

## Contradictions / Open Questions

- TADPOLE is a relatively clean research cohort; real-world clinical deployment will face noisier data, more heterogeneous populations, and higher missingness rates — external validation on non-ADNI data is absent
- Fairness is evaluated only across sex and age; race/ethnicity fairness is not assessed, despite race being a known factor in APOE4 risk distribution and healthcare access patterns
- The model uses APOE4 allele count, which is a genetic proxy for race in some populations — latent demographic leakage into the model is not tested
- Comparison baselines do not include the current SOTA for AD progression prediction; the paper does not position against other digital twin systems
- Digital twin framing implies continuous updating as new patient data arrives; the paper evaluates static training, not online updating
- Calibrated uncertainty (ECE 0.054) is reported for overall population; uncertainty calibration for rare patient subtypes (e.g., early-onset AD) is not evaluated

## Raw Source

`raw/2604.22428v1.pdf`
