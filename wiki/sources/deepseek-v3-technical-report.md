---
title: "DeepSeek-V3 Technical Report"
type: source
tags: [deepseek, moe, mla, mtp, fp8, grpo, infrastructure, benchmark, open-source]
sources: [deepseek-v3-technical-report]
created: 2026-04-27
updated: 2026-04-27
---

## Summary

The primary technical report for DeepSeek-V3 (DeepSeek-AI, December 2024; arXiv:2412.19437). DeepSeek-V3 is a 671B-parameter Mixture-of-Experts language model with 37B parameters activated per token, trained on 14.8 trillion tokens. The report documents architecture, infrastructure, pre-training, post-training, and benchmarks in full engineering detail.

The headline result: DeepSeek-V3 achieves performance competitive with GPT-4o and Claude-3.5-Sonnet across most benchmarks — and outperforms both on math and coding — while requiring only **$5.576M total training cost** (2.788M H800 GPU hours). The paper provides the first complete, transparent training cost breakdown at this capability level.

The technical report is the primary source for [[wiki/sources/deepseek-innovations|DeepSeek Innovations (Dickson, 2025)]], which is a secondary explainer. Architecture descriptions here are more precise with full mathematical formulation.

## Model Specification

| Property | Value |
|----------|-------|
| Total parameters | 671B |
| Activated parameters per token | 37B |
| Architecture | MoE (DeepSeekMoE) + MLA |
| Pre-training tokens | 14.8 trillion |
| Context length | 128K (extended from 4K via YaRN) |
| Vocabulary | 128K tokens (Byte-level BPE) |
| Training hardware | 2048 H800 GPUs |
| Training framework | HAI-LLM (in-house) |

## Training Cost Breakdown

| Stage | GPU Hours | Cost (@ $2/hr) |
|-------|-----------|-----------------|
| Pre-training | 2,664K | $5.328M |
| Context extension | 119K | $0.238M |
| Post-training | 5K | $0.010M |
| **Total** | **2,788K** | **$5.576M** |

Training rate: **180K H800 GPU hours per trillion tokens** = 3.7 days/trillion tokens on a 2048-GPU cluster. Pre-training completed in under two months. No irrecoverable loss spikes; no rollbacks — notable training stability at this scale.

## Architecture

### Multi-Head Latent Attention (MLA)

MLA compresses the KV cache through low-rank joint compression. During inference, only two vectors are cached per token per layer:
- `c^KV_t` — the compressed latent vector (d_c << d_h × n_h)
- `k^R_t` — the decoupled RoPE key

This is a dramatic reduction from standard MHA, which caches full-dimensional keys and values for all heads. Queries also undergo low-rank compression during training to reduce activation memory. The RoPE pathway is fully decoupled: positional information flows through a separate branch so MLA's compression does not interfere with relative position encoding.

### DeepSeekMoE with Auxiliary-Loss-Free Load Balancing

Each Transformer block's FFN is replaced by DeepSeekMoE:

```
h'_t = u_t + Σ(shared experts) + Σ(top-Kr gated routed experts)
```

- N_s shared experts: always active for every token (learn universal knowledge)
- N_r routed experts: top-K_r selected per token via affinity scoring

**Auxiliary-loss-free load balancing** is a key innovation. Standard MoE uses an auxiliary loss to penalise uneven routing — but large auxiliary losses degrade model performance. DeepSeek-V3 instead adds a per-expert bias term `b_i` that adjusts routing decisions without entering the loss function:
- Routing uses `s_i,t + b_i` to select top-K
- Gating values (multiplied with FFN outputs) still use raw `s_i,t`
- Bias updates: decrease if overloaded, increase if underloaded (step γ = 0.001)
- Result: effective load balance with no performance penalty

### Multi-Token Prediction (MTP)

Instead of predicting only the next token, DeepSeek-V3 adds D MTP modules that each predict one additional future token. Each depth-k module:
1. Concatenates the main model's representation with the embedding of the already-predicted token at position i+k
2. Runs through a dedicated Transformer block
3. Uses the shared output head to predict token at position i+k+1

MTP loss is weighted (λ=0.3 for first 10T tokens, 0.1 for remaining 4.8T) and averaged across depths. **At inference**, the D=1 MTP module enables speculative decoding with 85–90% acceptance rate for the second token, achieving **1.8× tokens-per-second speedup**.

## Infrastructure

### Parallelism Strategy
- 16-way Pipeline Parallelism (PP)
- 64-way Expert Parallelism (EP) across 8 nodes
- ZeRO-1 Data Parallelism (DP)
- No Tensor Parallelism (avoided to reduce memory overhead)

### DualPipe

A novel pipeline parallelism algorithm designed to address the heavy communication overhead of cross-node expert parallelism. DeepSeek-V3's computation-to-communication ratio is ~1:1, making standard 1F1B pipeline parallelism inefficient.

DualPipe runs forward and backward chunks in opposite directions simultaneously, overlapping computation and communication. Compared to 1F1B and ZB1P:
- Fewer pipeline bubbles
- Computation and communication fully hidden from each other
- Cost: 2× model parameter copies in memory (acceptable given large EP size)

### FP8 Mixed Precision Training

DeepSeek-V3 is the **first model at this scale to validate FP8 training effectiveness**. The framework:
- Uses FP8 for compute-intensive operations (matrix multiplications)
- Maintains higher precision (BF16/FP32) for precision-sensitive operations (loss scaling, normalisations)
- Custom quantisation and block-wise precision management to maintain training stability

### Cross-Node All-to-All Communication

Custom kernels fully exploit InfiniBand and NVLink bandwidth for MoE token dispatching/combining. Communication overhead fully hidden by DualPipe's overlap strategy.

## Pre-Training

- **Data**: 14.8T tokens; enhanced ratio of mathematical and programming samples; multilingual beyond English/Chinese; document packing without cross-sample attention masking
- **Fill-in-Middle (FIM)**: Applied at 10% rate using Prefix-Suffix-Middle (PSM) format — enables the model to predict middle text from context without degrading next-token prediction
- **Learning rate**: Peak 2.2×10⁻⁴; cosine decay to 2.2×10⁻⁵ over 4.3T tokens; final 500B tokens at reduced LR
- **Batch size**: Gradually scaled from 3072 to 15360 sequences in first 469B tokens
- **Long context extension**: YaRN applied post-pre-training; extended to 128K; validated via Needle in a Haystack test across full 128K window

## Post-Training

### Supervised Fine-Tuning

SFT on curated instruction-following data covering reasoning, code, writing, factual QA, and role-playing.

### Reinforcement Learning (GRPO)

GRPO (Group Relative Policy Optimization) replaces PPO's separate value model. For each prompt, a group of responses is sampled, each scored, and gradient updates derived from scores relative to group mean — memory-efficient RL alignment.

Reward model covers: rule-based verification (math, code correctness), format compliance, general preference via a trained reward model, and **self-rewarding via constitutional AI** — DeepSeek-V3 evaluates its own outputs using voting and uses these as reward signals, enabling self-improvement without external human labels.

### R1 Knowledge Distillation

Reasoning patterns from [[wiki/entities/deepseek|DeepSeek-R1]] — verification and reflection behaviour from chain-of-thought reasoning — are distilled into DeepSeek-V3 during post-training, improving reasoning performance while maintaining controlled output style and length.

## Benchmark Results

### Base Model (vs. open-source)

| Benchmark | DeepSeek-V3 Base | Qwen2.5-72B | LLaMA-3.1-405B |
|-----------|-----------------|-------------|----------------|
| MMLU | 87.1 | 85.0 | 84.4 |
| MMLU-Pro | 64.4 | 58.3 | 52.8 |
| BBH | 87.5 | 79.8 | 82.9 |
| HumanEval | 65.2 | 53.0 | 54.9 |
| MATH | 61.6 | 54.4 | 49.0 |
| C-Eval | 90.1 | 89.2 | 72.5 |

Note: 37B activated params vs. 72B (Qwen) and 405B (LLaMA) — better performance at lower active compute.

### Chat Model (vs. closed-source)

| Benchmark | DeepSeek-V3 | GPT-4o | Claude-3.5-Sonnet |
|-----------|------------|--------|-------------------|
| MMLU-Pro | 75.9 | 72.6 | 78.0 |
| GPQA-Diamond | 59.1 | 49.9 | 65.0 |
| MATH-500 | **90.2** | 74.6 | 78.3 |
| AIME 2024 | **39.2** | 9.3 | 16.0 |
| Codeforces (pct) | **51.6** | 23.6 | 20.3 |
| SWE-bench Verified | 42.0 | 38.8 | **50.8** |

Strongest open-source model on math and coding at publication. Competitive with GPT-4o and Claude-3.5-Sonnet on knowledge benchmarks; trails Claude on GPQA and SWE-bench.

## Key Concepts

- [[wiki/concepts/mixture-of-experts|Mixture of Experts]] — DeepSeekMoE with auxiliary-loss-free balancing; the primary scaling mechanism
- [[wiki/concepts/transformer-architecture|Transformer Architecture]] — MLA, MTP as architectural extensions
- [[wiki/entities/deepseek|DeepSeek]] — the organisation; V3 is its flagship model at publication

## Notable Claims

- First complete transparent training cost breakdown for a frontier-class model: $5.576M total
- First FP8 training validation at 671B scale
- Auxiliary-loss-free load balancing outperforms auxiliary-loss approaches without performance penalty
- 37B activated parameters outperform 405B dense model (LLaMA-3.1-405B) on most benchmarks — MoE efficiency at work
- MTP second-token acceptance rate 85-90%; 1.8× inference speedup via speculative decoding
- Training stability: no irrecoverable loss spikes across the full 14.8T token run

## Contradictions / Open Questions

- $5.576M covers only the official training run — ablations, architecture experiments, and prior research excluded; true total investment is larger
- GRPO self-rewarding relies on DeepSeek-V3 evaluating its own outputs — potential for reward hacking or value drift over successive self-improvement cycles
- Future directions explicitly acknowledge Transformer architectural limitations; DeepSeek plans to "break through" them — suggesting the current architecture is not the endpoint
- The benchmark advantage over closed-source narrows on agentic tasks (SWE-bench) — consistent with the token consumption findings that agentic capability requires more than raw benchmark performance

## Raw Source

`raw/2412.19437v1.pdf`
arXiv: https://arxiv.org/abs/2412.19437
