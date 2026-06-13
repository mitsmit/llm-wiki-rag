---
title: "Toward a Team of AI-made Scientists for Scientific Discovery from Gene Expression Data"
type: source
tags: [ai-scientists, multi-agent, genomics, scientific-discovery, tais]
sources: [2402.12391v3]
created: 2026-04-26
updated: 2026-04-26
---

## Summary

Published on arXiv (2402.12391, updated Sep 2025) by Liu, Li, Jian et al. from UIUC, UCSD, and collaborating institutions. Introduces **TAIS (Team of AI-made Scientists)**, a multi-agent LLM system designed to automate the scientific discovery pipeline for gene expression data analysis — specifically identifying disease-predictive genes under various patient conditions.

TAIS is a concrete working instantiation of [[wiki/concepts/agentic-ai|Agentic AI]] applied to a real scientific domain. It demonstrates that specialized role-based agent teams can replicate the multi-step workflow of human data scientists, with results corroborated by biomedical literature.

## Key Concepts

- [[wiki/concepts/agentic-ai|Agentic AI]] — TAIS is a direct implementation of multi-agent orchestration for scientific work
- [[wiki/concepts/ai-for-scientific-discovery|AI for Scientific Discovery]] — one of the key systems in this emerging space

## System Architecture

TAIS organizes five specialized LLM agents in a two-stage pipeline:

| Role | Responsibilities |
|------|----------------|
| **Project Manager** | Receives user query; decomposes task; assigns subtasks to agents; integrates results |
| **Data Engineer** | Dataset selection from GEO/TCGA; preprocessing; missing value handling; data cleaning |
| **Domain Expert** | Scientific consulting; interpretation of results; confounding factor identification |
| **Statistician** | Regression analysis (Lasso); confounding factor correction; two-step regression for missing conditions |
| **Code Reviewer** | Quality assurance; code validation; error detection before execution |

Two-stage pipeline:
1. **Data preparation**: dataset selection → preprocessing → confounding factor correction → condition prediction (two-step regression)
2. **Regression-based association analysis**: identify disease-predictive genes under specified conditions

## Notable Claims

- TAIS successfully performs intricate data analysis on genetic datasets; identified genes corroborated by biomedical literature
- Iterative agent collaboration (agents reviewing and correcting each other's outputs) improves performance over single-pass analysis
- 457 disease-condition pair benchmark created as evaluation dataset (manual gold standard)
- The confounding factor correction step — often omitted in automated pipelines — is critical for avoiding false discoveries
- Two-step regression handles missing patient condition data, a practical necessity for real-world genomics datasets

## Comparison to TAIS vs. Single-Agent Baselines

- Multi-agent team outperforms single LLM on complex data science tasks due to role specialization and error-catching through inter-agent review
- The project manager's task decomposition is the key orchestration layer — it determines which agents are invoked and in what order

## Connection to Other Sources

- Contrasts with [[wiki/sources/risks-of-ai-scientists|Risks of AI Scientists]]: TAIS demonstrates capability without a dedicated safety framework — the tension the risks paper warns about
- Extends [[wiki/concepts/agentic-ai|Agentic AI]] taxonomy from [[wiki/sources/ai-agents-vs-agentic-ai|AI Agents vs. Agentic AI]] into a concrete domain application
- Prefigures the "specialized AI researchers" envisioned in [[wiki/sources/ai-2027|AI 2027]] (Agent-3's AI R&D corps), but at a much earlier and narrower scale

## Contradictions / Open Questions

- Benchmark is domain-specific (gene expression / genomics) — generalizability to other scientific domains is unclear
- No discussion of failure modes when agents produce conflicting outputs — how does the project manager adjudicate?
- Safety/misuse analysis absent — noted as a gap by [[wiki/sources/risks-of-ai-scientists|Risks of AI Scientists]]

## Raw Source

`raw/assets/2402.12391v3.pdf`
