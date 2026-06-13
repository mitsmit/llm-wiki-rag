---
title: "ResearchAgent: Iterative Research Idea Generation over Scientific Literature with LLMs"
type: source
tags: [ai-scientists, research-automation, idea-generation, academic-graph, multi-agent]
sources: [2404.07738v2]
created: 2026-04-26
updated: 2026-04-26
---

## Summary

Published on arXiv (2404.07738, updated Feb 2025) by Baek, Jauhar, Cucerzan, and Hwang (KAIST / Microsoft Research). Introduces **ResearchAgent**, an LLM-powered system that automates the first phase of scientific research: **idea generation**. Given a core scientific paper, it automatically defines novel problems, proposes methods, and designs experiments — iteratively refined by a committee of LLM-powered reviewing agents.

Most prior AI-for-science work targeted the second phase (experimental validation). ResearchAgent is among the first systems explicitly focused on the earlier, harder phase: *what should we work on?*

## Key Concepts

- [[wiki/concepts/ai-for-scientific-discovery|AI for Scientific Discovery]] — directly addresses the ideation phase

## System Architecture

Three knowledge sources feed idea generation:

1. **Core paper**: the seed scientific publication
2. **Academic graph**: related papers via citation/reference relationships — captures related prior work context
3. **Entity-centric knowledge store**: co-occurrence counts of key concepts across thousands of papers — captures cross-domain concept relationships (e.g., "GPT-3 appears with CoT in 17,326 papers")

Idea generation pipeline (three phases):
1. **Problem Identification** — define a novel research question
2. **Method Development** — propose approaches to address the problem
3. **Experiment Design** — specify how to test the proposed method

Iterative refinement:
- Multiple **ReviewingAgents** provide structured reviews and feedback after each iteration
- ReviewingAgents are prompted with evaluation criteria elicited from actual human researcher judgements (human-preference-aligned)
- The system revises across multiple rounds until quality thresholds are met

## Notable Claims

- ResearchAgent outperforms pure LLM baselines by large margins on novelty, clarity, and relevance — both in human and model-based evaluation
- The entity-centric knowledge store specifically improves **novelty** by enabling cross-domain concept combinations that citations alone would miss
- Iterative reviewing agents specifically improve **validity** and **clarity**
- The system generalizes across multiple scientific disciplines (not domain-specific like TAIS)
- Cross-pollination of ideas across domains — a key source of breakthrough research — is enabled by the knowledge store's graph of concept co-occurrences

## Key Design Insight

Human researchers generate good ideas by combining three things: *related literature*, *encyclopedic concept knowledge*, and *peer feedback*. ResearchAgent directly models all three, rather than relying on LLM pretraining alone to proxy them.

## Connection to Other Sources

- Complements [[wiki/sources/team-of-ai-scientists|TAIS]]: TAIS automates execution; ResearchAgent automates ideation — together they begin to cover the full research cycle
- Both are capability papers with limited safety discussion — the gap [[wiki/sources/risks-of-ai-scientists|Risks of AI Scientists]] explicitly flags
- The "cross-domain knowledge store" mechanism is an early step toward what [[wiki/sources/ai-2027|AI 2027]] describes as Agent-3 having "PhD-level knowledge of every field" and identifying research directions humans missed

## Contradictions / Open Questions

- The evaluation relies partly on human judgement of "novelty" — hard to operationalize at scale; humans may rate novel-sounding but impractical ideas highly
- No longitudinal validation: ideas rated as novel and valid — have any actually been implemented and proven out?
- The reviewing agent loop could reinforce LLM biases if all agents share the same underlying model
- Safety implications of open-ended idea generation (e.g., generating novel bioweapon synthesis routes framed as "research ideas") are not addressed

## Raw Source

`raw/assets/2404.07738v2.pdf`
