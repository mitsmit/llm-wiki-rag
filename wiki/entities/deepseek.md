---
title: DeepSeek
type: entity
tags: [deepseek, china, open-source, llm, frontier-model, ai-lab]
sources: [deepseek-innovations, deepseek-v3-technical-report]
created: 2026-04-27
updated: 2026-04-27
---

## Overview

DeepSeek is a Chinese AI research company (founded 2023, Hangzhou) that disrupted the AI industry in early 2025 by releasing DeepSeek-V3 and DeepSeek-R1 — open-source models achieving performance competitive with or exceeding GPT-4o, o1, and Claude 3.5 Sonnet at a fraction of their training cost. DeepSeek's significance is not just capability but methodology: they published their weights, architecture details, and training recipes openly, providing a replicable blueprint that accelerated the global research community.

DeepSeek is the real-world analog to [[wiki/entities/deepcent|DeepCent]] in the [[wiki/sources/ai-2027|AI 2027]] scenario — a Chinese AI lab capable of frontier performance — though the real DeepSeek operates through open publication rather than state-directed secrecy.

## Key Models

| Model | Type | Notable Properties |
|-------|------|--------------------|
| DeepSeek-V2 | MoE | Introduced MLA + DeepSeekMoE; validated architecture for V3 |
| DeepSeek-V3 | MoE | 671B total / 37B active; 14.8T tokens; $5.576M total training; MATH-500: 90.2, AIME: 39.2 |
| DeepSeek-R1-Zero | Reasoning | Pure RL from V3-Base, no SFT; strong reasoning, poor readability |
| DeepSeek-R1 | Reasoning | Cold-start SFT → RL → SFT → RL; reasoning distilled back into V3 |

## Technical Innovations

DeepSeek's efficiency comes from a coordinated stack of innovations — no single magic bullet:

- **MLA**: Low-rank KV cache compression; only the compressed latent vector and decoupled RoPE key cached at inference — dramatic KV memory reduction vs. standard MHA
- **DeepSeekMoE**: Fine-grained expert segmentation + shared expert isolation; **auxiliary-loss-free load balancing** via per-expert dynamic bias terms (avoids the performance penalty of auxiliary loss approaches)
- **Multi-Token Prediction**: Parallel prediction heads at each position; 85–90% acceptance rate for second token; **1.8× inference TPS speedup** via speculative decoding
- **Algorithm-hardware co-design**: FP8 mixed-precision (first validated at this scale); DualPipe pipeline parallelism; custom all-to-all communication kernels for cross-node MoE
- **GRPO**: Memory-efficient RL alignment without a separate value model; self-rewarding via constitutional AI
- **R1 distillation**: Reasoning verification/reflection patterns from DeepSeek-R1 distilled into V3 post-training

See [[wiki/sources/deepseek-v3-technical-report|DeepSeek-V3 Technical Report]] for full mathematical and engineering detail, and [[wiki/sources/deepseek-innovations|DeepSeek Innovations (Dickson)]] for a conceptual explainer.

## Strategic Significance

**Cost disruption**: DeepSeek-V3 total training cost **$5.576M** (pre-training $5.328M + context extension $0.238M + post-training $0.01M; 2.788M H800 GPU hours) — compared to estimated hundreds of millions for comparable Western models. The full breakdown, published openly, challenged the assumption that frontier AI required near-unlimited compute budgets and spooked markets.

**Open-source frontier**: By releasing weights and training details, DeepSeek demonstrated that SOTA performance does not require secrecy. This sharply contradicts the strategy of closed Western labs and the AI 2027 assumption that frontier capability stays concentrated.

**Chip constraint workaround**: DeepSeek trained on H800 GPUs (the export-controlled downgrade from H100s), demonstrating that US chip export restrictions, while costly, did not prevent frontier model development. The co-design approach was partly a response to hardware constraints.

**Geopolitical implications**: DeepSeek's success is evidence for both sides of the US-China AI race debate — it demonstrates Chinese capability parity while also showing Chinese labs remain under hardware disadvantage and rely on architectural efficiency rather than raw compute scale.

## Relationship to AI 2027 Scenario

The AI 2027 scenario's [[wiki/entities/deepcent|DeepCent]] is described as consistently 6 months behind [[wiki/entities/openbrain|OpenBrain]], relying on state resources and eventually stolen model weights to catch up. DeepSeek's real-world trajectory is more complex:

- DeepSeek achieved competitive performance through *published* innovation rather than espionage
- The scenario assumes frontier capability requires closed, resource-intensive development; DeepSeek disproves this
- The scenario may underestimate how quickly open-source development can close capability gaps without state-directed secrecy or model theft

This is a live tension in the wiki: the AI 2027 geopolitical frame assumes a world of closed frontier labs; DeepSeek is evidence that this assumption is already fraying.

## Open Questions

- Can DeepSeek maintain frontier performance as model scale continues to increase, or does the MoE/efficiency approach hit diminishing returns?
- How does US chip export policy evolve in response to DeepSeek demonstrating H800-based frontier training?
- Does DeepSeek's open publication strategy represent a durable competitive choice or a temporary positioning decision?
- What is DeepSeek's relationship with the Chinese government — independent, loosely affiliated, or subject to direction?
