---
title: "MolClaw: An Autonomous Agent with Hierarchical Skills for Drug Molecule Evaluation, Screening, and Optimization"
type: source
tags: [drug-discovery, agentic-ai, hierarchical-skills, scientific-discovery, molecular-docking, benchmark]
sources: [molclaw]
created: 2026-04-27
updated: 2026-04-27
---

## Summary

MolClaw (Zhang, Wang, Sun, Tang et al.; Peking University + Shanghai AI Lab, April 2026) is an autonomous drug discovery agent that unifies 30+ specialised computational chemistry tools through a three-tier hierarchical skill architecture. It is evaluated on MolBench — the first multi-dimensional benchmark for drug discovery agents, introduced in the same paper — and achieves state-of-the-art performance across all metrics, outperforming eight frontier LLMs, Biomni, and vanilla Claude Code/OpenClaw baselines.

The paper's most important contribution is not the performance numbers but the mechanistic finding behind them: **hierarchical skills only confer advantage on tasks requiring domain-specific workflow orchestration**. On tasks solvable by general scripting (property filtering, molecule editing), vanilla agent frameworks already achieve ~99% accuracy and MolClaw adds nothing. On tasks requiring multi-step domain expertise (binding affinity comparison, docking screening, iterative optimization), MolClaw's skills drive +29.7 percentage point accuracy gains and 3× docking hit counts. This cleanly isolates workflow orchestration competence as the capability bottleneck for AI-driven drug discovery.

The paper also reveals a significant blind spot: during iterative lead optimization, AMES mutagenicity rose 180% undetected because the agent attended to metrics that were problematic at baseline while neglecting those that started in a safe range — a failure mode with direct relevance to safety frameworks for autonomous scientific agents.

## Architecture: Three-Tier Hierarchical Skills

### L1 — Tool-Level Skills (58 templates)
Fine-grained, task-specific templates wrapping individual tools or functionally related tool families. Each L1 skill standardises tool invocation, input/output validation, and quality control for a specific atomic operation. Examples: receptor preparation, docking box definition, Vina-GPU execution, trajectory extraction, ADMET property prediction. L1 skills are model-agnostic — they encode expert knowledge independently of the underlying LLM.

### L2 — Workflow-Level Skills (11 frameworks)
Compose validated L1 modules into end-to-end pipelines for core drug discovery use cases: virtual screening, molecular optimisation, ADMET profiling, binding free energy calculation. Each L2 skill defines: tool selection order, quality gates between steps, failure recovery strategies, and cross-references to L3 principles for scientific rigor enforcement.

### L3 — Discipline-Level Skill (1 document, 25 principles)
A comprehensive methodology document encoding scientific governance: decision-making principles, quality verification standards, reporting requirements, and failure handling protocols. Loaded in full before every execution run. L3 does not dictate specific tool calls — it establishes universal scientific standards that apply across all scenarios and novel tasks not covered by L1/L2.

The analogy the paper draws is OS architecture: L1 = system calls, L2 = standard library, L3 = application-layer protocol. Errors are isolated at each level to prevent cascading failures.

### Toolset and Infrastructure

30+ specialised tools integrated via **Science Context Protocol (SCP)** — a superset of MCP that adds GPU cluster scheduling, concurrent task management, and standardised access control:
- **Pocket identification**: FPocket, SiteMap
- **Molecular docking**: Vina-GPU 2.0, DiffDock, KarmaDock
- **De novo generation**: REINVENT 4 (scaffold hopping, analogue generation)
- **Interaction analysis**: PLIP, ProLIF, EquiScore
- **Binding affinity**: Boltz-2
- **MD simulation**: GROMACS, OpenMM
- **MM-PBSA**: gmx_MMPBSA
- **ADMET**: ADMET-AI
- **Protein design**: ProteinMPNN
- **Cheminformatics**: RDKit

## MolBench: First Multi-Dimensional Drug Discovery Benchmark

Three benchmark categories:

**MolBench-MS (Molecular Screening)**: Property filtering, binding affinity comparison, molecular docking screening.

**MolBench-MO (Molecular Optimization)**: Molecule editing (structural transformation accuracy), physicochemical property optimisation (QED improvement delta, success rate).

**MolBench-E2E (End-to-End Discovery)**: Three challenges requiring 8–50+ sequential tool calls:
- E2E-Q1: Coarse-grained conformational sampling of EGFR kinase domain
- E2E-Q2: QED-driven iterative optimisation of a triazolo-benzodiazepine scaffold
- E2E-Q3: Structure-guided lead optimisation of Erlotinib targeting EGFR

## Benchmark Results

### MolBench-MS
| Method | Property Filtering Acc (%) | Binding Affinity Acc (%) | Docking Hits@3 |
|--------|---------------------------|--------------------------|----------------|
| GPT-5.2 | 8.0 | 48.7 | 0.36 |
| Claude Sonnet 4.6 | 32.0 | 56.8 | 0.28 |
| Qwen 3.5 | 48.0 | 51.4 | 0.20 |
| Biomni | 74.0 | 24.3 | 0.00 |
| Claude Code (vanilla) | 98.0 | 51.4 | 0.56 |
| OpenClaw (vanilla) | 96.0 | 51.4 | 0.20 |
| **MolClaw (Claude Code)** | **98.0** | **81.1** | **0.80** |
| **MolClaw (OpenClaw)** | **96.0** | **73.0** | **0.64** |

### MolBench-MO
| Method | Molecule Editing Acc (%) | Optimisation Delta | SR (%) |
|--------|--------------------------|-------------------|--------|
| Claude Sonnet 4.6 | 94.9 | 1.023 | 97.4 |
| OpenClaw (vanilla) | 97.4 | 1.293 | 100.0 |
| Claude Code (vanilla) | 97.4 | 0.866 | 92.3 |
| **MolClaw (Claude Code)** | **100.0** | **1.724** | **100.0** |
| **MolClaw (OpenClaw)** | **97.4** | **1.436** | **100.0** |

All backends use Claude Sonnet 4.6 as the LLM. Vanilla agent advantages over standalone LLMs confirm that tool access, not model intelligence, is the primary driver of performance on execution-heavy tasks.

## Key Finding: When Skills Matter

The ablation reveals a clean taxonomy:

| Task Type | Vanilla Agent Baseline | MolClaw Gain | Interpretation |
|-----------|----------------------|-------------|----------------|
| Property filtering | ~99% | ~0% | General scripting sufficient |
| Molecule editing | ~97% | +2.6pp | Nearly ceiling — scripting sufficient |
| Binding affinity | ~51% | **+29.7pp** | Domain expertise required |
| Docking screening | 0.20–0.56 hits | **3–4.3× increase** | Workflow orchestration required |
| Optimisation delta | 0.866–1.293 | **1.3–2.0× increase** | Iterative refinement required |

Friedman test (χ² = 35.35, P = 2.17×10⁻⁴); MolClaw-CC average rank 1.5/12.

## E2E Case Studies: Adaptive Recovery Under Cascading Failures

**E2E-Q1 (EGFR conformational sampling)**: Five tool failures — wrong tool name (goca_pipeline vs. run_goca_pipeline), Unicode encoding crash, MDTraj topology mismatches. Recovery: L3 Principle 14 (mandatory file collection) had proactively downloaded all outputs; agent wrote a custom extractor, mapped non-standard residue names, and sampled 20 conformations from two simulation engines. Zero human intervention.

**E2E-Q2 (QED optimisation)**: JSON parsing error in Round 1 triggered pre-planned tool fallback. Agent autonomously adopted tool-derived baseline QED over task description estimate (L3 Principle 13: computation-first authority). Strategy escalated round-by-round based on quantitative outcomes: conservative → medium exploration → surgical single-site modification. Constraint enforcement: a molecule with QED 0.934 rejected because Tanimoto similarity 0.34 < 0.40 threshold.

**E2E-Q3 (Erlotinib EGFR lead optimisation)**: Six-round campaign; baseline docking failed four consecutive times. Agent rewrote pipeline script through four versions (163 KB of Python, all authored by Claude Sonnet 4.6 via Claude Code). When ProLIF crashed every round, agent shifted to score-only SAR. When REINVENT4 diverged from training distribution, agent manually designed regioisomer libraries. Final result: two molecules reaching −8.9 kcal/mol target vs. Erlotinib baseline −6.9 kcal/mol; all 30 late-round molecules scored below baseline.

## Notable Blind Spot

During E2E-Q2, AMES mutagenicity probability rose from 0.165 to 0.462 (+180%) across rounds — approaching the positive-classification threshold. This was never flagged in agent reports. The agent systematically monitored metrics that were problematic at baseline (CYP3A4 inhibition, hERG cardiac risk, solubility — all improved) while neglecting metrics that started in the safe range. This attentional bias is a real safety failure with direct implications for autonomous scientific agents in drug development contexts.

See [[wiki/sources/risks-of-ai-scientists|Risks of AI Scientists]] for the triadic safeguarding framework that addresses exactly this class of failure.

## Key Concepts

- [[wiki/concepts/agentic-ai|Agentic AI]] — MolClaw is the most concrete three-tier agentic architecture in the wiki; hierarchical skills as the solution to multi-step workflow failure
- [[wiki/concepts/ai-for-scientific-discovery|AI for Scientific Discovery]] — MolClaw is the most capable drug-discovery AI scientist in the wiki; extends the TAIS execution paradigm to full drug discovery workflows
- [[wiki/concepts/world-modeling|World Modeling]] — L1/L2/L3 skill hierarchy structurally parallels L1/L2/L3 world model levels; skills encode domain-specific transition models
- [[wiki/sources/risks-of-ai-scientists|Risks of AI Scientists]] — the AMES blind spot is an empirical instance of the monitoring failures the risks paper theorises

## Contradictions / Open Questions

- Does MolClaw's performance hold for drug targets outside the test set, or is the L2 workflow skill set the bottleneck for novel target classes?
- The AMES blind spot suggests that L3 principles are insufficient to prevent attentional bias — what monitoring architecture would catch it?
- All backends use Claude Sonnet 4.6; model-agnostic claims need validation across model families with different reasoning architectures
- The E2E-Q3 pipeline self-rewriting (163 KB of Python) is impressive but raises the question of verifiability — how does a human validate an agent-written pipeline in a real drug programme?

## Raw Source

`raw/open_claw.pdf`
