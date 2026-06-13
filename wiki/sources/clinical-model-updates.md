---
title: "An empirical evaluation of the risks of AI model updates using clinical data: stability, arbitrariness, and fairness"
type: source
tags: [clinical-ai, model-updates, stability, fairness, arbitrariness, model-multiplicity, continual-learning]
sources: [clinical-model-updates]
created: 2026-04-28
updated: 2026-04-28
---

## Summary

Bilionis, Berrios, Fernandez-Luque, Castillo (Adhera Health + Universitat Pompeu Fabra; IEEE EMBC 2026) present an empirical evaluation framework for the risks of updating clinical AI models over time. The core argument: model updates are unavoidable — training data goes stale as patient demographics, behaviours, and environments shift — but updating a clinical model introduces three risk dimensions that aggregate performance metrics (AUC, accuracy) cannot detect.

The three risk dimensions are **stability** (individual-patient predictions flip between retraining phases), **arbitrariness** (multiple equally-accurate models disagree on individual predictions), and **fairness drift** (update strategies affect demographic subgroups differently, and in different directions for different fairness criteria). A model whose AUC is unchanged after retraining may still be dramatically less reliable for specific patient subgroups.

Evaluated on four U.S. pediatric Type 1 Diabetes CGM datasets (496 participants, 11,300 weekly observations), the paper compares four retraining strategies across four protected attributes (sex, age, caregiver education, household income). Full cumulative retraining is the most stable and equitable strategy. Last-batch retraining — the simplest deployment practice — is worst on every dimension. Instability disproportionately affects already-vulnerable groups: older children, female children, and patients from lower-income and lower-education households.

The paper also introduces a distance-based conformal abstention mechanism that routes out-of-distribution predictions for clinician review rather than acting on them — improving overall reliability but with heterogeneous and sometimes contradictory fairness effects across datasets and attributes.

## Clinical and Regulatory Context

AI/ML models deployed as **Software as a Medical Device (SaMD)** face a stability-plasticity dilemma: stale models degrade; updated models introduce instability. The FDA's **Predetermined Change Control Plan (PCCP)** acknowledges the need for controlled model evolution, but empirically almost no approved AI medical devices report post-deployment retraining. The gap between regulatory guidance and practice is the condition this paper addresses.

The paper positions its monitoring framework as a governance tool — specifying what must be tracked before, during, and after each retraining event to ensure that updates do not silently harm individual patients or demographic subgroups.

## Experimental Design

**Datasets**: Four publicly available U.S. T1D datasets (PEDAP, IOBP2, DCLP5, CITY; sourced from Jaeb Center), pediatric (under 20 years), six chronological batches per dataset, patients uniquely assigned to one batch.

**Prediction task**: Binary classification (low vs. high risk for severe hyperglycemia per patient-week). High risk = >3 events with glucose >250 mg/dL for ≥180 minutes.

**Base classifier**: Logistic Regression — selected for highest stability and overall performance across all four datasets in initial benchmarking against Random Forest, CatBoost, and Naïve Bayes.

**Retraining strategies compared**:

| Strategy | Training data |
|----------|--------------|
| Full cumulative | All data from all past batches |
| Last-batch | Only the most recent batch |
| Random subsample | Fixed-size random draw from all past batches |
| No retraining | Original model, never updated |

**Evaluation settings**: (1) Prospective — model trained at phase `t` evaluated on next batch `t+1`; (2) Retrospective fixed hold-out — stratified 10% patient-level test set held constant across all phases, repeated N times with different seeds.

**Protected attributes**: Sex, age cohort, caregiver educational level, household annual income.

## Evaluation Metrics

### Predictive performance
- AUC overall and per protected subgroup (`AUC(a)_t`)
- Temporal delta: `∆AUCt = AUCt − AUCt−1`
- AUC gap between subgroups: `AUCdiff,t`

### Fairness
- **Equal Opportunity (EO)**: `∆EO = |TPR(a1) − TPR(a2)|`
- **Demographic Parity (DP)**: `∆DP = |P(ŷ=1|a=a1) − P(ŷ=1|a=a2)|`

### Stability and arbitrariness
- **Self-Consistency (SC)**: probability that independently retrained models agree on a prediction (bootstrap-based)
- **Systematic Arbitrariness (SA)**: SC divergence between protected groups — structured instability targeting specific subpopulations
- **Temporal Self-Consistency (TSC)**: average SC across all retraining phases per individual; `∆TSCi = SCi(1) − SCi(T)` captures stability degradation
- **Prediction Flip Rate**: fraction of consecutive-phase prediction reversals per individual; an individual is "unstable" if >20% of predictions flip, or TSC falls below 0.75 at any point

### Model multiplicity (Rashomon set)
- **Distinct Predictive Patterns (DPR)**: unique prediction vectors within the near-optimal model set
- **Prediction Disagreement Rate (DR)**: expected pairwise prediction mismatch within the Rashomon set

## Key Results

### Retraining strategy comparison (Table I, averaged across datasets)

| Protected feature | Strategy | Avg AUC | AUC gap (∆AUC) | EO | DP | Overall Arb. (OA) |
|-------------------|----------|---------|----------------|-----|-----|-------------------|
| Sex | No retrain | 0.61 | 0.11 | 0.21 | 0.22 | 0.11 |
| Sex | Last-batch | 0.61 | 0.07 | 0.13 | 0.16 | 0.11 |
| Sex | Subsample | 0.64 | 0.07 | 0.17 | 0.18 | 0.10 |
| Sex | **Full** | **0.65** | 0.08 | **0.16** | **0.18** | **0.07** |
| Income | No retrain | 0.60 | 0.11 | 0.19 | 0.19 | 0.11 |
| Income | Last-batch | 0.60 | 0.10 | 0.19 | 0.18 | 0.11 |
| Income | Subsample | 0.64 | 0.09 | 0.17 | 0.17 | 0.10 |
| Income | **Full** | **0.64** | 0.10 | **0.17** | **0.18** | **0.08** |

Full cumulative retraining is consistently best on AUC and overall arbitrariness. Last-batch retraining achieves identical or lower AUC with higher arbitrariness in most settings. The no-retraining baseline is not uniformly worst.

### Temporal stability and instability disparities (Table II, averaged across datasets)

| Protected feature | Subgroup | % Instability (flip rate) | % Instability (low TSC) | % High abstention |
|-------------------|----------|--------------------------|------------------------|-------------------|
| Age | Older | 4.22 | 11.45 | 4.84 |
| Age | Younger | 1.29 | 9.68 | 7.85 |
| Sex | Female | 5.16 | 12.90 | 6.77 |
| Sex | Male | 4.22 | 9.70 | 5.93 |
| Income | Lower | 5.38 | 16.92 | 8.41 |
| Income | Higher | 3.59 | 13.17 | 5.28 |
| Education | Lower | 5.11 | 9.09 | 7.99 |
| Education | Higher | 4.44 | 8.89 | 5.49 |

**The vulnerable groups are the least stable**: older children, female children, and lower-income patients have consistently higher flip rates and lower TSC. These disparities are not captured by aggregate AUC.

**Population-level instability**: low-TSC proxy affects on average **31.9% of individuals** (range 0–100%). Worsening-TSC (progressive degradation) captures 7% ± 10% of individuals (range 0–70%). Flip rates: 0–7%.

### Model multiplicity (Rashomon set)
Under full cumulative retraining, prediction disagreement rate (DR) ranges **20–32%** across datasets, generally decreasing as more data accumulates. Distinct predictive patterns (DPR) range 1–7 and tend to increase over time — model diversity grows even as aggregate performance stabilises.

### Conformal abstention
Distance-based k-NN abstention routes out-of-distribution cases for clinician review (max 5% abstention budget). Effects are heterogeneous:
- DB4 (income): abstention improves overall AUC and reduces both EO and DP disparities
- DB1 (age): abstention has negligible impact on AUC, increases EO disparity while improving DP disparity
- Abstention disproportionately affects lower-income and lower-education patients and male children — the abstention mechanism itself introduces differential impact

## The Central Methodological Claim

**Performance-preserving updates do not imply stable or fair individual-level decisions.**

A model can maintain the same aggregate AUC across retraining phases while:
- Reversing predictions for ~5% of female children each update cycle
- Progressively destabilising predictions for ~17% of lower-income patients over time
- Selecting from 7 equally-accurate models that disagree on ~25% of individual predictions

These phenomena are invisible to standard monitoring. The paper's monitoring framework makes them visible by adding stability, arbitrariness, multiplicity, and uncertainty metrics alongside the standard accuracy/fairness dashboard.

## Key Concepts

- [[wiki/concepts/clinical-ai|Clinical AI]] — the deployment context; this paper is the operational companion to CognitiveTwin, addressing the update lifecycle rather than initial training
- [[wiki/concepts/representational-harm|Representational Harm]] — update-induced instability disproportionately targeting vulnerable subgroups is a form of clinical representational harm; distinct from training-data bias but structurally related
- [[wiki/concepts/digital-twin|Digital Twin]] — the digital twin framing (continuous patient model updating) requires exactly the governance framework this paper proposes; continuous updating without monitoring is the failure mode

## Notable Claims

- Last-batch retraining consistently amplifies subgroup disparities under both EO and DP — the simplest deployment practice is the most harmful
- Instability disproportionately affects already-vulnerable groups: the update process reproduces social vulnerability in model behaviour
- 31.9% of individuals exhibit low temporal self-consistency on average — nearly one-third of patients receive unreliable longitudinal predictions
- Conformal abstention can simultaneously improve one fairness criterion and worsen another for the same dataset — fairness metrics are not interchangeable
- The Rashomon set analysis reveals 20–32% prediction disagreement rate among equally-performing models — there is no single "correct" model, only a family of models that behave differently on individuals

## Contradictions / Open Questions

- The paper uses Logistic Regression as its base classifier for stability; more complex models (gradient boosting, neural networks) may show different stability/fairness trade-off patterns
- Only four retraining strategies are compared; adaptive strategies (drift-aware retraining, population-stratified subsampling) are not evaluated
- Conformal abstention is calibrated at 5% maximum — the choice of budget affects fairness outcomes and is not systematically studied
- The findings are specific to pediatric T1D with CGM data; generalisability to other clinical domains (oncology, cardiology, psychiatry) is untested
- The monitoring framework is proposed but not validated as a governance protocol in actual clinical deployment — the gap between measurement and practice remains

## Raw Source

`raw/2604.23954v1.pdf`
