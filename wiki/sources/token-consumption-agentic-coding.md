---
title: "How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding Tasks"
type: source
tags: [agentic-ai, token-efficiency, llm-economics, coding-agents, swe-bench]
sources: [token-consumption-agentic-coding]
created: 2026-04-27
updated: 2026-04-27
---

## Summary

This paper (Bai, Huang, Wang, Sun, Mihalcea, Brynjolfsson, Pentland, Pei) provides the first systematic analysis of token consumption in agentic coding tasks, benchmarked across eight frontier LLMs on SWE-bench Verified. It measures not just whether agents solve tasks but *how much they spend doing so* — a question that matters enormously at deployment scale but has been largely ignored by the capability-focused literature.

The headline finding is that agentic tasks consume **1000× more tokens than code reasoning or code chat** — primarily driven by input tokens (context accumulation across multi-turn tool calls) rather than output tokens. This has direct implications for cost modeling, model selection, and the economics of deploying agentic systems at scale.

## Key Findings

**Scale of consumption:** Agentic tasks consume ~1000× more tokens than code reasoning benchmarks. Input tokens dominate: agents spend most tokens reading accumulated context (prior actions, tool outputs, repo contents) rather than generating responses.

**Extreme variability:** Token usage on the same task across different runs can differ by up to **30×**. Higher token consumption does not correlate with better task success — expensive runs are not reliably more accurate than cheap ones.

**Model efficiency varies dramatically:** Kimi-K2 and Claude-Sonnet-4.5 consume substantially more tokens than GPT-5 on identical SWE-bench tasks. Model selection is therefore a cost lever independent of capability ranking.

**Human difficulty ratings are unreliable cost proxies:** Expert-assigned difficulty scores correlate poorly with actual computational costs, revealing a systematic gap between perceived and real complexity. Tasks humans rate as "easy" may be expensive; "hard" tasks may be cheap.

**Models cannot predict their own token usage:** Frontier models systematically underestimate their own consumption when asked to forecast it before execution. Weak correlations and consistent underestimation make pre-execution cost planning unreliable using model self-assessment.

## Methodology

- **Benchmark:** SWE-bench Verified (real GitHub issues requiring code changes)
- **Models tested:** 8 frontier LLMs (includes GPT-5, Kimi-K2, Claude-Sonnet-4.5, and others)
- **Analysis:** Token breakdown by input/output, task-level variability, model-level efficiency comparison, human difficulty vs. cost correlation, self-prediction accuracy

## Relationship to Other Concepts

- [[wiki/concepts/agentic-ai|Agentic AI]] — adds the cost and efficiency dimension absent from capability-focused agentic AI research; multi-turn tool calls are the primary driver of token explosion
- [[wiki/concepts/ai-for-scientific-discovery|AI for Scientific Discovery]] — agentic scientific pipelines face the same token accumulation problem; long-horizon research tasks will be even more expensive than coding tasks

## Notable Claims

- Token consumption is a first-class concern for agentic deployment, not a secondary operational detail
- The input token dominance suggests context management (compression, summarization, retrieval) is as important as model capability for cost-effective agentic systems
- Cost unpredictability (30× variance) makes budgeting for agentic deployments fundamentally difficult

## Contradictions / Open Questions

- How do these findings generalize beyond coding tasks to other agentic domains (research, data analysis, multi-agent coordination)?
- Does the 30× variability reflect task ambiguity, model stochasticity, or agent architecture choices — and which is most controllable?
- What context management strategies most effectively reduce input token accumulation without degrading task success?

## Raw Source

arXiv: https://arxiv.org/abs/2604.22750
