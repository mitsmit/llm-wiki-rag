---
title: World Modeling
type: concept
tags: [world-modeling, agentic-ai, model-based-rl, planning, simulation, l1-l2-l3]
sources: [agentic-world-modeling]
created: 2026-04-27
updated: 2026-04-27
---

## Overview

World modeling is an AI system's capacity to maintain and use an internal model of how its environment works — enabling planning, counterfactual reasoning, and autonomous adaptation rather than purely reactive behavior. The distinction between an agent with a world model and one without is the difference between a system that can *simulate* consequences before acting and one that only responds to what it observes.

The [[wiki/sources/agentic-world-modeling|Agentic World Modeling survey]] (Chu et al., 2026) provides the most comprehensive current taxonomy: the "levels × laws" framework, which organizes world modeling capability along two orthogonal axes — three levels of capability and four governing-law regimes.

## The Levels × Laws Framework

### Capability Levels

**L1 Predictor** — single-step local prediction. The model learns to predict the next state given the current state and action. This is what most trained neural networks achieve: statistical association without multi-step coherence or causal understanding. Dreamer, MuZero, TD-MPC2, and most video prediction models operate here.

**L2 Simulator** — multi-step, decision-usable rollout. The model composes L1 predictions into coherent long-horizon trajectories that remain usable for planning. Three boundary conditions define genuine L2:
1. **Long-horizon coherence** — rollouts don't degrade into noise over the planning horizon
2. **Intervention sensitivity** — changing an action produces the expected counterfactual trajectory change
3. **Constraint consistency** — rollouts stay within domain-law feasibility (physical possibility, valid API calls, social norms)

Failure to meet these conditions is the "residual frame problem" — the model doesn't know what should stay the same when something changes.

**L3 Evolver** — autonomous model revision. The model updates itself based on evidence: failures trigger diagnosis, targeted revision, and gated validation before the update takes effect. L3 requires three properties:
1. **Evidence-grounded diagnosis** — failure is traced to a specific, actionable cause
2. **Persistent asset updates** — new knowledge is stored as reusable skills or rules, not discarded after a run
3. **Governed validation** — regression testing before the updated model is enabled

L3 is the frontier. Physical and scientific domains show the most mature L3 implementations (robotics that revise grasp strategies from contact failures; closed-loop materials discovery); digital and social domains lag.

### Governing-Law Regimes

| Regime | Domain | Constraint Type | Validation Method |
|--------|--------|-----------------|-------------------|
| Physical | Robotics, AV, video | Physics laws | Physics engines, analytical solutions |
| Digital | Web agents, code, GUI | Program semantics | Formal verification, test suites |
| Social | Dialogue, multi-agent | Norms, beliefs | Human judgment, convention |
| Scientific | Molecules, weather, drug design | Latent causal laws | Experimental measurement |

The scientific regime is the most demanding: governing equations are not known in advance and must be discovered from data — every prediction is a hypothesis, and validation requires running a real experiment.

## Why World Modeling Matters for Agentic AI

Without a world model, an agent must act to observe — it learns by doing. With an L2+ world model, an agent can simulate outcomes before committing, enabling:
- **Planning over long horizons** without executing every intermediate step
- **Counterfactual reasoning** ("what would happen if I took action B instead?")
- **Safe exploration** (simulate dangerous actions rather than executing them)
- **Efficient resource use** (explore the model, not the real environment)

The [[wiki/sources/token-consumption-agentic-coding|token consumption research (Bai et al.)]] provides indirect evidence that current coding agents lack strong L2 models: the 30× token variability per task suggests agents explore expensively through trial and error rather than simulating trajectories before acting.

## Connection to the Intelligence Explosion

The [[wiki/concepts/intelligence-explosion|Intelligence Explosion]] scenario in AI 2027 implicitly requires L3-class world modeling: AI systems that can autonomously revise their own understanding of how AI research works, what experiments to run, and how to interpret results. The Agentic World Modeling survey's L3 framework makes this capability concrete and highlights why it's currently missing — and why its arrival would be a meaningful threshold event.

The survey also flags the safety implication it doesn't fully engage with: L3 evolvers that autonomously revise governing laws are precisely the systems that make [[wiki/concepts/alignment-failure-modes|alignment oversight]] hardest. An L3 system can update its own objectives as well as its world model.

## Evaluation: Prediction-Centric vs. Decision-Centric

Traditional world model evaluation measures prediction accuracy (MSE, pixel SSIM). The survey argues this is the wrong metric: a model with higher pixel error might enable better planning than a more accurate model with worse constraint consistency. Decision-centric evaluation asks: does the world model improve downstream task performance?

Current benchmark landscape:
- Most benchmarks test L1 prediction accuracy
- L2 constraint consistency testing is sparse (SWE-bench partially covers digital constraint consistency)
- L3 adaptation benchmarks are almost entirely absent

## Symbolic vs. Latent for L3

A key architectural claim: L1 and L2 work well with latent neural representations (efficient, scalable, generalizable). But genuine L3 — revising governing principles rather than fine-tuning parameters — may require surfacing laws as first-class symbolic objects. The survey points to physics history: Newton's laws, Maxwell's equations, and the Standard Model are all explicit symbolic structures that scientists could inspect, debate, and revise. Neural latents enable efficient prediction but make principled revision opaque.

This suggests a possible convergence between world modeling and program synthesis / scientific discovery: the endpoint of L3 is not just a neural model that updates weights, but a system that maintains an explicit, falsifiable, revisable theory of its domain.

## Open Questions

- What is the minimal architecture for L2 coherence — what does a system need to stop making frame-problem errors?
- Can L3 be made safe? Autonomous model revision is exactly what makes alignment harder; can revision be bounded without breaking the L3 property?
- Does latent L3 (parameter updates) suffice for scientific discovery, or does symbolic L3 (law revision) become necessary at some complexity threshold?
- How does the L1→L2→L3 progression relate to the capability milestones in AI 2027 (SC → SAR → SIAR)?

## Related Concepts

- [[wiki/concepts/agentic-ai|Agentic AI]] — world modeling is the internal substrate enabling effective agentic behavior
- [[wiki/concepts/ai-for-scientific-discovery|AI for Scientific Discovery]] — scientific discovery is the L3/scientific-regime intersection; the hardest world modeling problem
- [[wiki/concepts/intelligence-explosion|Intelligence Explosion]] — requires L3-class world modeling of the AI R&D process itself
- [[wiki/concepts/alignment-failure-modes|Alignment Failure Modes]] — L3 evolvers that revise their own objectives are the hardest alignment case
