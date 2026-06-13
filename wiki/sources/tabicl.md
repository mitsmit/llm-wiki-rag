---
title: "TabICL: A Tabular Foundation Model for In-Context Learning on Large Data"
type: source
tags: [tabular-ml, in-context-learning, foundation-models, tabular-foundation-models, scalability, icml]
sources: [2502.05564v2]
created: 2026-05-14
updated: 2026-05-14
---

## Summary

Qu, Holzmüller, Varoquaux, Le Morvan (INRIA Saclay / ENS Paris, ICML 2025) introduce TabICL, a tabular foundation model that extends the in-context learning (ICL) paradigm of TabPFN to large datasets. TabPFN's alternating column-and-row-wise attention becomes computationally prohibitive beyond ~10K samples; TabICL replaces it with a two-stage architecture that handles up to 500K samples and 500 features on a single GPU (≈20GB memory).

**Stage 1 — Row embedding**: Each row is compressed into a fixed-dimensional dense vector via a Set Transformer applied column-wise (distribution-aware feature embedding capturing per-column statistical regularities) followed by attention-based row-wise interaction (cross-feature dependencies). This collapses the variable-feature-count table into compact, semantically grounded row representations.

**Stage 2 — ICL**: The row embeddings (with labels for training examples) are fed to a standard Transformer that performs in-context learning over the compressed dataset, outputting class probabilities for test rows in a single forward pass.

On the TALENT benchmark (200 classification datasets), TabICL matches TabPFNv2 on medium datasets and significantly outperforms all methods on 53 large datasets (>10K samples), including TabPFNv2 and CatBoost — demonstrating that ICL can scale to regimes where gradient-boosted trees have historically dominated.

## Key Concepts

- [[wiki/concepts/tabular-foundation-models|Tabular Foundation Models]] — TabICL is the most scalable tabular ICL model as of ICML 2025; extends [[wiki/sources/tabpfn|TabPFN]]
- [[wiki/concepts/transformer-architecture|Transformer Architecture]] — used in both stages; Set Transformer for column-wise embedding; standard Transformer for ICL

## Notable Claims

- **Scalability breakthrough**: TabPFN/TabPFNv2 are limited to ~10K samples by quadratic attention cost. TabICL handles 500K samples by compressing rows into fixed-size embeddings before the ICL Transformer — O(n) in training samples for the embedding stage.
- **Cross-table transferability**: Distribution-aware column-wise embedding using a Set Transformer (with rotary positional embeddings) allows sharing embedding parameters across tables with different feature counts — critical for pre-training on diverse synthetic datasets.
- **Large-data advantage**: On >10K sample datasets, TabICL outperforms both TabPFNv2 and CatBoost. This is the first tabular ICL model to beat gradient-boosted trees on large real-world datasets.
- **Speed**: Up to 10× faster than TabPFNv2 at inference; efficiency gain grows with dataset size.
- **Curriculum pre-training**: Pre-training dataset size scaled from 1K to 60K samples; tree-based data-generating model added to prior alongside the existing BNN/SCM priors.
- **Hierarchical classification**: Handles >10 classes by decomposing into hierarchical sub-problems of ≤10 classes each.

## Contradictions / Open Questions

- TabICL is evaluated on classification only; regression and survival analysis tasks are not covered (unlike some tree-based competitors).
- Pre-training is on synthetic data; the gap between synthetic prior and specific real-world domain distributions remains a ceiling on performance in narrow domains.
- TabICL does not support fine-tuning on domain data by design; for tasks with substantial prior mismatch, how does it compare to a domain-fine-tuned LLM approach?

## Raw Source

`raw/2502.05564v2.pdf`
