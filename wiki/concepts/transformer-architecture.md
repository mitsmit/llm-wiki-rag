---
title: Transformer Architecture
type: concept
tags: [transformer, attention, architecture, deep-learning, foundational]
sources: [1706.03762v7]
created: 2026-04-26
updated: 2026-04-27
---

## Overview

The Transformer (Vaswani et al., 2017) is the neural network architecture underlying all modern large language models. It replaced recurrent neural networks (RNNs/LSTMs) as the dominant approach to sequence modelling by eliminating sequential computation entirely, enabling training at scales previously impossible. Every AI system in the [[wiki/sources/ai-2027|AI 2027]] scenario — from GPT-3 to Agent-4 — is a descendant of this architecture.

## Why Transformers Replaced RNNs

The fundamental problem with RNNs is sequential dependency: to compute hidden state h_t you need h_{t-1}. This means:
- **No parallelization within a training example** — tokens must be processed one at a time
- **Long-range dependency degradation** — signals must traverse O(n) steps to connect distant positions, making them hard to learn
- **Memory constraints limit batch size** at long sequence lengths

Self-attention solves all three:

| Property | RNN | Transformer (Self-Attention) |
|----------|-----|-------------------------------|
| Sequential ops per layer | O(n) | O(1) |
| Max path length (long-range deps) | O(n) | O(1) |
| Complexity per layer | O(n·d²) | O(n²·d) |
| Parallelizable | No | Yes |

The trade-off: O(n²·d) complexity means quadratic cost in sequence length. For typical sentence-length inputs (n << d), self-attention is faster. For very long sequences, this becomes a bottleneck — addressed by later sparse and linear attention variants.

## Core Components

### 1. Scaled Dot-Product Attention

The fundamental operation. Given queries Q, keys K, and values V:

```
Attention(Q, K, V) = softmax(QKᵀ / √dk) · V
```

- The `√dk` scaling prevents dot products from growing large (pushing softmax into near-zero-gradient regions) when dk is large
- Output is a weighted sum of values, where weights are computed by query-key compatibility

### 2. Multi-Head Attention

Run h attention functions in parallel on different learned projections of Q, K, V:

```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) · W_O
where head_i = Attention(Q·W_Q_i, K·W_K_i, V·W_V_i)
```

- Allows the model to jointly attend to information from different representation subspaces at different positions
- With h=8 heads and d_model=512, each head operates in 64 dimensions — similar total compute to single-head full-dimension attention
- Empirically: individual heads specialize in different syntactic/semantic relationships (anaphora resolution, long-range verb phrases, etc.)

### 3. Encoder-Decoder Structure

**Encoder** (6 identical layers):
- Sub-layer 1: Multi-head self-attention (each position attends to all positions)
- Sub-layer 2: Position-wise feed-forward network
- Both wrapped with residual connection + layer normalization: `LayerNorm(x + Sublayer(x))`

**Decoder** (6 identical layers):
- Sub-layer 1: Masked multi-head self-attention (prevents attending to future positions — causal masking)
- Sub-layer 2: Multi-head cross-attention over encoder output (queries from decoder, keys/values from encoder)
- Sub-layer 3: Position-wise feed-forward network

### 4. Positional Encoding

Since there is no recurrence or convolution, position information must be injected explicitly:

```
PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

Added to input embeddings. Sinusoidal form was chosen because PE(pos+k) can be expressed as a linear function of PE(pos) for any offset k — allowing the model to attend by relative position. May generalize to sequence lengths longer than training data.

### 5. Feed-Forward Sublayers

Applied position-wise (identically at each position, independently):

```
FFN(x) = max(0, xW₁ + b₁)W₂ + b₂
```

d_model=512 → d_ff=2048 → d_model=512. Acts as a per-position nonlinear transformation.

## Three Uses of Attention in the Transformer

1. **Encoder self-attention**: Each position attends to all positions in the encoder input
2. **Decoder masked self-attention**: Each position attends only to earlier positions (causal)
3. **Encoder-decoder cross-attention**: Decoder queries attend over all encoder key-value pairs

## Why This Matters for AI Scaling

The Transformer's parallelizability is the prerequisite for the compute scaling curves that drive the [[wiki/concepts/intelligence-explosion|intelligence explosion]]:
- Efficient GPU utilization requires parallel computation — RNNs waste hardware
- Training on internet-scale text requires processing billions of tokens efficiently
- The FLOP scaling from GPT-3 (3×10²³) to GPT-4 (2×10²⁵) to Agent-1 (4×10²⁷) is only economically viable because Transformer training parallelizes across GPUs
- The AI 2027 concept of [[wiki/concepts/intelligence-explosion|neuralese recurrence]] (residual stream passing between forward passes) is explicitly a proposed extension of the Transformer to overcome its token-bandwidth bottleneck

## Limitations Noted in Original Paper

- Quadratic attention complexity in sequence length — addressed by later sparse/linear attention work
- Fixed context window — addressed by positional encoding improvements and architectural variants
- No explicit mechanism for long-term memory — addressed by memory-augmented Transformers, neuralese recurrence (speculative, per AI 2027)

## Modern Architectural Extensions

The original 2017 Transformer has been extensively extended by the research community. Key developments relevant to the wiki:

**Multi-Head Latent Attention (MLA)** — introduced by [[wiki/entities/deepseek|DeepSeek]]-V2. Replaces standard MHA's KV cache with a low-rank latent compression, drastically reducing memory at long context lengths without sacrificing accuracy. RoPE positional embeddings are decoupled into a parallel pathway to preserve positional accuracy under compression. Addresses the quadratic memory growth of the KV cache for long-context inference.

**Mixture of Experts (MoE)** — replaces the position-wise feed-forward sublayer with a bank of specialised expert networks, routing each token to only a subset. Decouples total model capacity from per-token compute, enabling trillion-parameter models at manageable training FLOPs. Used in GPT-4, Gemini, Llama 4, and DeepSeek-V3. See [[wiki/concepts/mixture-of-experts|Mixture of Experts]] for full detail.

**Multi-Token Prediction (MTP)** — extends the standard next-token prediction objective to simultaneously predict N+k tokens at each position using parallel prediction heads. Improves sample efficiency during training — more learning signal per training example. Used in DeepSeek-V3.

**Rotary Position Embeddings (RoPE)** — replaces the original sinusoidal absolute positional encodings with relative position encodings computed via rotation matrices in the complex plane. Better length generalisation and cleaner integration with attention computation. Now standard in most decoder-only models (LLaMA, Mistral, DeepSeek, Qwen).

**Cross-Modal Fusion (CognitiveTwin pattern)** — Transformers applied to multi-modal clinical data rather than text. Each data modality (cognitive scores, MRI, PET/CSF biomarkers, genetics) is projected to a common embedding dimension with a learned modality-type embedding (analogous to BERT's token-type embedding). Multi-head self-attention then learns cross-modal dependencies at each clinical visit. See [[wiki/concepts/clinical-ai|Clinical AI]] and [[wiki/sources/cognitivetwin|CognitiveTwin]].

## Related Concepts

- [[wiki/concepts/intelligence-explosion|Intelligence Explosion]] — Transformer scaling is the hardware-side prerequisite
- [[wiki/concepts/ai-capability-milestones|AI Capability Milestones]] — all milestones built on Transformer descendants
- [[wiki/concepts/mixture-of-experts|Mixture of Experts]] — the dominant feed-forward sublayer extension in frontier models
- [[wiki/entities/deepseek|DeepSeek]] — primary source for MLA, MTP, and refined MoE innovations
- [[wiki/concepts/clinical-ai|Clinical AI]] — cross-modal fusion for heterogeneous clinical data; the CognitiveTwin pattern
