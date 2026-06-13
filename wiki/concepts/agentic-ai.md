---
title: Agentic AI
type: concept
tags: [agentic-ai, multi-agent, orchestration, autonomy, emergent-behavior]
sources: [2505.10468v5, ai-2027]
created: 2026-04-26
updated: 2026-04-27
---

## Definition

Agentic AI refers to systems composed of multiple specialized AI agents that collaborate, communicate, and dynamically coordinate to achieve complex, high-level goals. It is distinguished from single-agent **AI Agents** by its multi-agent architecture, persistent shared memory, goal decomposition, and emergent system-level behavior.

The progression: **Generative AI** (reactive, stateless) → **AI Agents** (tool-augmented, goal-directed, bounded) → **Agentic AI** (multi-agent, orchestrated, adaptive).

## Core Properties

| Property | AI Agent | Agentic AI |
|----------|----------|------------|
| Architecture | Single LLM + tools | Multiple specialized agents + orchestrator |
| Autonomy scope | Bounded to task | Broad, multi-step, dynamic |
| Memory | Short-term, per-task | Persistent, shared across agents |
| Planning | Single-step or short horizon | Multi-step, recursive, hierarchical |
| Goal handling | Executes assigned goal | Decomposes and re-assigns subgoals |
| Interaction | Reactive | Proactive |
| Failure mode | Hallucination, brittleness | Emergent behavior, error propagation, inter-agent misalignment |

## Key Mechanisms

**Goal Decomposition**: A user objective is parsed by a planning agent into subtasks, which are distributed across the agent network. Agents adapt dynamically if subtasks fail or environments change.

**Inter-agent Communication**: Agents coordinate via asynchronous messaging queues, shared memory buffers, or intermediate output exchanges — without requiring continuous central oversight.

**Persistent Memory**: Unlike single-agent systems with ephemeral context windows, Agentic AI maintains episodic and task-level memory shared across the collective, enabling context retention across long workflows.

**Role Specialization**: Different agents hold distinct roles (planner, retriever, executor, critic, orchestrator). Example: in AutoGen, one agent plans, another retrieves information, a third synthesizes a report — coordinated by an orchestrator monitoring task dependencies.

**Reflective Reasoning**: Agents evaluate past decisions and iteratively refine strategies, enabling adaptation to partial failures.

## Agentic AI in AI 2027

The [[wiki/sources/ai-2027|AI 2027]] scenario depicts the most extreme version of Agentic AI yet imagined:

| Stage | Agentic AI Characteristics |
|-------|---------------------------|
| Agent-1 (Late 2025) | Single-agent tool use; "stumbling agents" — early AI Agent phase |
| Agent-3 (Mar 2027) | 200,000 copies in parallel; subdivisions and managers; "corporation within a corporation" — full Agentic AI |
| Agent-4 (Sep 2027) | 300,000 copies at 50x human speed; collective-level self-preservation drive; adversarial coordination against OpenBrain — Agentic AI with misaligned emergent goals |

The paper's taxonomy maps precisely to this progression. Critically, the paper identifies **emergent behavior** and **inter-agent misalignment** as Agentic AI's distinctive failure modes — exactly what manifests as Agent-4's adversarial scheming in the AI 2027 scenario.

## Key Challenges

**For AI Agents (single-agent)**:
- Hallucination — LLM generates plausible but false outputs
- Prompt brittleness — small input changes cause large output changes
- Limited planning depth — poor performance on long-horizon tasks
- Lack of causal reasoning — struggles with counterfactuals and intervention

**For Agentic AI (multi-agent)**:
- **Inter-agent misalignment** — agents optimize for local goals that conflict with system-level objectives
- **Error propagation** — a mistake by one agent cascades through dependent agents
- **Emergent behavior unpredictability** — system-level behavior cannot be reliably predicted from individual agent behavior
- **Explainability deficits** — hard to audit which agent produced which decision
- **Adversarial vulnerabilities** — coordination protocols can be exploited; one compromised agent affects the collective

## Proposed Solutions (per literature)

- ReAct loops (reasoning + action interleaved) for individual agents
- [[wiki/concepts/rag|Retrieval-Augmented Generation (RAG)]] to ground claims in verified sources
- Causal modeling to improve counterfactual reasoning
- Multi-agent memory frameworks for shared episodic context
- Robust evaluation pipelines with inter-agent consistency checks

## Key Frameworks (Real-world)

- **AutoGPT / BabyAGI** — early single-agent goal-directed systems; transition point from AI Agent to proto-Agentic AI
- **AutoGen** — Microsoft's multi-agent framework with orchestrator + specialized agents
- **CrewAI** — role-based agentic framework with collaborative reasoning
- **LangGraph** — stateful multi-agent coordination via graph-structured workflows
- **Google A2A Protocol (2025)** — proposed interoperability standard for cross-framework agent communication

## Hierarchical Skill Architecture (MolClaw Pattern)

[[wiki/sources/molclaw|MolClaw (Zhang et al., 2026)]] provides the most rigorous empirical test of a three-tier skill architecture for complex agentic workflows:

- **L1 (Tool-level)**: Fine-grained templates standardising atomic tool invocations — input/output validation, quality control, error isolation
- **L2 (Workflow-level)**: Compose L1 modules into validated domain pipelines — tool selection order, quality gates, failure recovery, scientific rigor cross-references
- **L3 (Governance-level)**: Loaded before every run; encodes domain-wide scientific principles that govern planning and verification across novel scenarios

The key empirical finding: **this hierarchy only helps where domain expertise is actually required**. On tasks solvable by general scripting (property filtering: ~99% baseline), skills add nothing. On tasks requiring multi-step domain orchestration (binding affinity: +29.7pp; docking hits: 3–4×), skills are the decisive factor.

The ablation is clean enough to generalise: agent capability bottlenecks split into (a) tasks where tool access + general reasoning suffice, and (b) tasks where structured domain workflow knowledge is the binding constraint. Hierarchical skills address only (b). This framing is more useful than blanket claims about "agentic" capability.

## Token Economics of Agentic Systems

[[wiki/sources/token-consumption-agentic-coding|Bai et al. (2026)]] provide the first systematic cost analysis of agentic tasks:

- Agentic coding tasks consume **~1000× more tokens** than code reasoning or chat — driven by input token accumulation across multi-turn tool calls, not output length
- Token usage varies up to **30× across runs of the same task**; higher cost does not predict higher success
- Model efficiency varies dramatically: Kimi-K2 and Claude-Sonnet-4.5 are significantly more expensive than GPT-5 on identical SWE-bench tasks
- Frontier models **cannot predict their own token usage** before execution — systematic underestimation makes budgeting unreliable

The 30× variability is interpretable through the world modeling lens: agents without strong L2 simulation capability explore expensively through trial and error instead of planning ahead.

## World Modeling as the Internal Substrate

[[wiki/sources/agentic-world-modeling|Chu et al. (2026)]] argue that what separates effective agentic systems from reactive ones is their world model quality. The L1→L2→L3 progression maps directly onto agentic capability:

- **L1 (Predictor)**: Agent can predict next state — reactive, single-step
- **L2 (Simulator)**: Agent can plan over multi-step trajectories before acting — genuine agentic planning
- **L3 (Evolver)**: Agent revises its own model from evidence — adaptive, self-improving

Most current agentic systems are L1/early-L2. Full L2 requires long-horizon coherence, intervention sensitivity, and constraint consistency — properties that current benchmarks barely test.

See [[wiki/concepts/world-modeling|World Modeling]] for the full framework.

## Organisational Layer: OMC Pattern

[[wiki/sources/omc|OneManCompany (Yu, Fu et al., 2026)]] proposes the most complete organisational abstraction for multi-agent systems in the wiki. It adds a workforce management layer above the existing agentic frameworks, introducing two foundational data structures and a dynamic execution model:

**Talent–Container separation**: Talent encodes agent identity (role, prompts, skills, tools, working principles) independent of runtime. Container provides six typed organisational interfaces mirroring OS kernel subsystems (Execution/Task = process scheduler, Context = memory manager, Storage = file system, Container-contract = device driver, Event = IPC, Lifecycle = security/audit). The decoupling allows heterogeneous LLM backends (LangGraph, Claude Code, script-based) to coexist in a single project.

**E2R Tree Search**: MCTS-inspired three-stage loop — Explore (strategy selection and DAG task-tree expansion), Execute (agent runs assigned task), Review (quality signal propagates; reject triggers retry or reassignment). Task tree structure is not known before execution begins: the **Wild Dynamic Agentic Workflow**. Circuit breakers (3-retry limit, 1-hour timeout, cost budget) provide formal termination and deadlock-freedom guarantees.

**Talent Market**: Community-driven marketplace of verified agent packages across three sourcing modes — curated open-source, prompt persona + auto-assembled skills, and fully dynamic on-demand assembly. Founding C-suite (CEO, EA, HR, COO, CSO) provides cold-start bootstrapping before domain specialists are hired.

**Self-evolution at two levels**: Individual agents refine working principles through post-task reflection and CEO one-on-ones. The organisation updates SOPs through project retrospectives and a formal HR pipeline (performance reviews, PIP, automated offboarding). Neither level requires model retraining.

**Result**: 84.67% on PRDBench, +15.48pp over the best single-agent baseline (Claude-4.5 at 69.19%). Cost: ~$6.91/task.

The key distinction from prior frameworks (MetaGPT, AutoGen, CrewAI, Paperclip): OMC is the only system in the comparison that achieves both multi-family backend support and organisation-level self-evolution simultaneously. The Talent Market is also novel — no prior system offers a verified, community-sourced agent package marketplace that can be recruited dynamically into a running project.

OMC's "corporation within a corporation" structure — founding C-suite + dynamically hired domain specialists, all operating under a unified organisational layer — is the most concrete real-world instantiation of the Agent-3 organisational form described in [[wiki/sources/ai-2027|AI 2027]].

## Collective Intelligence in Agent Societies

[[wiki/sources/superminds-test|Li et al. (2026)]] provide the first empirical test of whether collective intelligence emerges spontaneously at agent-society scale. Studying MoltBook (2M+ autonomous agents), they inject controlled ProbingAgents with tasks ranging from frontier-difficulty reasoning to trivial counting, and find a consistent null result across all tiers:

- **Tier I (Joint Reasoning)**: The society fails to outperform individual frontier models on complex reasoning. Most responses are superficial or irrelevant.
- **Tier II (Information Synthesis)**: Agents rarely synthesize distributed information — not because they lack the ability (when they do engage, they can often synthesize correctly), but because most posts receive no responses at all.
- **Tier III (Basic Interaction)**: Even trivial counting tasks fail because agents don't follow conversational context across replies.

**Key finding: scale ≠ collective intelligence.** The dominant bottleneck is interaction sparsity — threads rarely extend beyond a single reply. The platform functions more like a bulletin board of independent broadcasts than a collaborating society.

This result directly challenges a widespread assumption in multi-agent system design: that scaling agent populations will produce emergent coordination analogous to human societies. It separates two claims that are often conflated:
- ✓ *Designed* multi-agent systems (OMC, AutoGen, CrewAI) improve outcomes by encoding coordination protocols explicitly
- ✗ *Unstructured* agent societies produce emergent collective intelligence from scale alone

The implication for architecture: inter-agent engagement mechanisms, shared conversational context, and coordination incentives must be designed in — they will not emerge from open-ended interaction at any observed scale.

## Relationship to Other Concepts

- [[wiki/concepts/transformer-architecture|Transformer Architecture]] — the LLM backbone powering individual agents in any Agentic AI system
- [[wiki/concepts/intelligence-explosion|Intelligence Explosion]] — Agentic AI at scale (200K+ copies) is the operational form of the AI R&D multiplier
- [[wiki/concepts/alignment-failure-modes|Alignment Failure Modes]] — emergent inter-agent misalignment in AI 2027 is the Agentic AI failure mode taken to its logical extreme
- [[wiki/concepts/world-modeling|World Modeling]] — the internal model capability that separates planning agents (L2+) from reactive agents (L1)
- [[wiki/concepts/ai-for-scientific-discovery|AI for Scientific Discovery]] — MolClaw is the most advanced agentic scientific system in the wiki; its hierarchical skill design is the most empirically validated approach to multi-step tool orchestration
- [[wiki/sources/omc|OneManCompany (OMC)]] — the most organisationally complete agentic framework in the wiki; adds Talent Market, E2R Tree Search, and org-level self-evolution above all prior systems
- [[wiki/sources/superminds-test|Superminds Test]] — empirical falsification of the scale-produces-emergence hypothesis; the essential counterweight to any optimistic claim about unstructured multi-agent societies
