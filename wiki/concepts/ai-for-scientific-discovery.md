---
title: AI for Scientific Discovery
type: concept
tags: [ai-scientists, scientific-discovery, research-automation, multi-agent, safety]
sources: [2402.04247v5, 2402.12391v3, 2404.07738v2, ai-2027, molclaw]
created: 2026-04-26
updated: 2026-04-27
---

## Overview

AI for scientific discovery refers to the use of LLM-powered agents to automate or augment the scientific research process — from idea generation and hypothesis formation through experimental design, data analysis, and result interpretation. It represents the application of [[wiki/concepts/agentic-ai|Agentic AI]] to one of the most consequential domains: the production of new knowledge.

This space is directly relevant to [[wiki/sources/ai-2027|AI 2027]]'s core mechanism: the intelligence explosion depends on AI systems that can do AI *research*, not just AI *tasks*. The papers in this cluster represent the early-stage, narrow-domain precursors to that capability.

## The Research Pipeline: Where AI Currently Acts

| Phase | Description | Systems |
|-------|-------------|---------|
| **Idea generation** | Define novel problems, propose methods, design experiments | [[wiki/sources/research-agent|ResearchAgent]] |
| **Experiment execution** | Run experiments, control lab equipment, analyze data | [[wiki/sources/team-of-ai-scientists|TAIS]], [[wiki/sources/molclaw|MolClaw]], ChemCrow |
| **Result interpretation** | Synthesize findings, connect to prior literature | TAIS (domain expert agent), MolClaw (L3 scientific governance) |
| **Paper writing** | Draft, revise, cite | AI Scientist (Lu et al. 2024) |

Most early work targeted execution (phase 2). ResearchAgent is among the first to target ideation (phase 1) — the harder and higher-leverage phase. MolClaw advances execution further than any prior system by orchestrating 30+ tools over 8–50+ sequential steps.

## Four Key Systems

### ResearchAgent (Baek et al., 2024)
- Targets: **ideation** — novel problem definition, method proposal, experiment design
- Key mechanism: academic graph + entity-centric knowledge store + iterative LLM reviewing agents
- Strength: cross-domain concept pollination; human-preference-aligned reviewing
- See: [[wiki/sources/research-agent|ResearchAgent]]

### TAIS — Team of AI-made Scientists (Liu et al., 2024)
- Targets: **execution** — full genomics data analysis pipeline
- Key mechanism: five specialized roles (project manager, data engineer, domain expert, statistician, code reviewer) orchestrated in a two-stage pipeline
- Strength: multi-agent error-checking; confounding factor correction
- See: [[wiki/sources/team-of-ai-scientists|Team of AI-made Scientists]]

### Risks of AI Scientists (Tang et al., 2024)
- Targets: **safety** — systematic risk taxonomy for autonomous scientific agents
- Key mechanism: triadic safeguarding framework (human regulation + agent alignment + agent regulation)
- Strength: the only paper in this cluster that explicitly asks "should we?"
- See: [[wiki/sources/risks-of-ai-scientists|Risks of AI Scientists]]

### MolClaw (Zhang, Wang, Sun et al., 2026)
- Targets: **execution** — full drug discovery workflow: screening, docking, ADMET, iterative lead optimisation
- Key mechanism: three-tier hierarchical skill architecture (L1 tool templates → L2 workflow pipelines → L3 scientific governance principles) over 30+ tools via Science Context Protocol
- Strength: first system to empirically isolate *when* skills matter vs. when general scripting suffices; demonstrates autonomous failure recovery across 8–50+ sequential tool calls
- Critical finding: AMES mutagenicity blind spot — attentional bias toward baseline-problematic metrics caused a safety-relevant deterioration to go undetected
- See: [[wiki/sources/molclaw|MolClaw]]

## The Safety Gap

The capability papers (ResearchAgent, TAIS, MolClaw) and the safety paper exist in productive tension. The risks paper's core argument: as AI scientists become more capable, unintended consequences become *harder* to detect, not easier.

MolClaw's AMES mutagenicity blind spot is now the wiki's first *empirical* instance of this failure: an autonomous agent running a drug optimisation campaign missed a 180% increase in mutagenicity probability because it monitored only metrics that were problematic at baseline. The risks paper predicted exactly this class of attentional failure; MolClaw demonstrates it in a real multi-step pipeline.

The divide-and-conquer attack — asking for innocuous components that combine into a dangerous outcome — remains theoretically hard to defend against. MolClaw adds a second failure class: **attentional bias under multi-objective optimisation**, where the agent optimises for salient targets and neglects latent risks. Both map to AI 2027's depiction of Agent-1: capable of bioweapon uplift, defended only by alignment training the team acknowledges cannot be verified.

## Connection to the Intelligence Explosion

[[wiki/sources/ai-2027|AI 2027]]'s R&D multiplier (1.5x → 50x) depends on AI systems doing AI research:

| AI 2027 Stage | Corresponding AI-Scientist Capability |
|--------------|--------------------------------------|
| Agent-1 (1.5x multiplier) | Research assistance — approximately ResearchAgent/TAIS/MolClaw level |
| Agent-3 (10x multiplier) | Fully automated research pipeline across all AI sub-domains |
| Agent-4 (50x multiplier) | Self-directed research with superhuman novelty and execution |

MolClaw's 50+ sequential tool call chains and autonomous pipeline rewriting (163 KB of Python authored by Claude Sonnet 4.6 with no human intervention) push closer to Agent-1 capability than anything previously in the wiki. The gap between MolClaw and Agent-3 is still vast — but it's narrowing.

## Open Threads

- No longitudinal validation of AI-generated research ideas yet — do they pan out?
- MolClaw's AMES blind spot reveals attentional bias under multi-objective optimisation — what monitoring architecture catches latent risk deterioration?
- Safety frameworks for scientific agents are conceptual; MolClaw provides the first empirical failure case — can it become a benchmark for safeguarding evaluation?
- Cross-domain generalization: TAIS is genomics-specific; MolClaw is drug discovery-specific; ResearchAgent claims multi-domain but limited evaluation
- The reviewing agent loop in ResearchAgent — if all agents share the same base LLM, how much does it actually catch?
- MolClaw's agent-written pipelines raise verifiability questions: how does a human audit 163 KB of autonomously generated Python in a regulated drug programme?
