---
title: "Attention Is All You Need"
type: source
tags: [transformer, architecture, attention, nlp, foundational]
sources: [1706.03762v7]
created: 2026-04-26
updated: 2026-04-26
---

## Summary

Published at NeurIPS 2017 by Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser, and Polosukhin (Google Brain / Google Research). This paper introduced the **Transformer**, the sequence transduction architecture that replaced recurrent and convolutional networks and became the foundation of all modern large language models — including every system described in [[wiki/sources/ai-2027|AI 2027]].

The central insight is that attention mechanisms alone — without any recurrence or convolution — are sufficient to achieve state-of-the-art performance on sequence tasks, while being dramatically more parallelizable and cheaper to train. The paper demonstrated this on machine translation, but the architecture generalized to virtually every domain in NLP and beyond.

The Transformer is the architectural origin of GPT-3, GPT-4, and every Agent in the AI 2027 scenario. Without it, the compute scaling curves that drive the [[wiki/concepts/intelligence-explosion|intelligence explosion]] narrative do not exist.

## Key Concepts

- [[wiki/concepts/transformer-architecture|Transformer Architecture]] — the full model: encoder-decoder stacks, multi-head attention, positional encoding, feed-forward sublayers
- [[wiki/concepts/ai-capability-milestones|AI Capability Milestones]] — all milestones in AI 2027 are built on Transformer-derived models

## Key Entities

- **Ashish Vaswani** — lead author; designed and implemented the first Transformer models
- **Noam Shazeer** — proposed scaled dot-product attention and multi-head attention
- **Jakob Uszkoreit** — proposed replacing RNNs with self-attention as the core idea
- **Google Brain / Google Research** — institutional home

## Notable Claims

- A model based solely on attention, with no recurrence or convolution, achieves new SOTA on EN-DE translation (28.4 BLEU, +2 over all prior ensembles) and EN-FR (41.8 BLEU)
- Training cost: 3.5 days on 8 P100 GPUs — "a small fraction of the training costs of the best models from the literature"
- Self-attention connects all positions with O(1) sequential operations; recurrent layers require O(n) — this is the parallelization unlock
- Self-attention path length for long-range dependencies: O(1) constant vs O(n) for recurrent, O(log_k(n)) for dilated convolutions
- Attention heads learn interpretable structure: individual heads specialize in syntactic dependencies, anaphora resolution, long-range verb phrases
- Positional encoding via sinusoids (PE(pos,2i) = sin(pos/10000^(2i/d_model))) may generalize to sequence lengths longer than those seen in training

## Architecture Specs (base model)

| Hyperparameter | Value |
|---|---|
| Encoder/decoder layers (N) | 6 |
| Model dimension (d_model) | 512 |
| Feed-forward dimension (d_ff) | 2048 |
| Attention heads (h) | 8 |
| Key/value dimension (d_k, d_v) | 64 |
| Dropout | 0.1 |
| Parameters | 65M |
| Training steps | 100K |

Big model: d_model=1024, h=16, 213M params, 300K steps → 28.4 BLEU EN-DE, 41.8 BLEU EN-FR.

## Contradictions / Open Questions

- The paper notes self-attention has O(n²·d) complexity per layer — for very long sequences this becomes a bottleneck (addressed by later work: sparse attention, linear attention, etc.)
- Positional encoding is fixed sinusoidal in the original; later work shows learned embeddings work equally well (Table 3 row E)
- The paper restricts evaluation to translation and parsing — generalization to generation, reasoning, and agent tasks was demonstrated by subsequent work (GPT series)

## Raw Source

`raw/1706.03762v7.pdf`
