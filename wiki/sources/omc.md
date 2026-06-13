---
title: "From Skills to Talent: Organising Heterogeneous Agents as a Real-World Company"
type: source
tags: [agentic-ai, multi-agent, organisational-ai, talent-container, e2r-search, self-evolution, benchmark]
sources: [omc]
created: 2026-04-27
updated: 2026-04-27
---

## Summary

OneManCompany (OMC; Zhengxu Yu, Yu Fu et al., 2026) proposes an organisational layer for multi-agent AI systems, framing a heterogeneous agent workforce as a real company. The central claim is that the human-enterprise pattern — manage, plan, hire, learn — transfers directly to AI agent systems, and that this organisational abstraction is the missing layer between individual agent frameworks and the kind of autonomous, large-scale collaboration imagined in scenarios like AI 2027's Agent-3.

The two foundational data structures are **Talent** (a portable agent identity package: role specification, system prompts, skills, tools, and working principles — runtime-agnostic) and **Container** (a runtime environment exposing six typed organisational interfaces that mirror OS kernel subsystems). Talent encodes *who* an agent is; Container encodes *how* it executes. The decoupling allows heterogeneous backends (LangGraph, Claude Code, script-based, any future runtime) to coexist in a single project under a unified dispatch loop.

Execution is coordinated by **E2R Tree Search** — an MCTS-inspired three-stage loop (Explore → Execute → Review) operating over a DAG task tree that expands dynamically during execution. Neither team composition nor workflow structure is fixed before a project begins; the system calls this the **Wild Dynamic Agentic Workflow**. A finite-state-machine lifecycle and circuit breakers (3-retry limit, 1-hour timeout, cost budget) guarantee termination and deadlock freedom under bounded resources.

Agent supply comes from the **Talent Market**, a community-driven marketplace of verified agent packages available in three sourcing modes: (1) curated from established open-source repos, (2) prompt persona + auto-assembled skills from SkillsMP, (3) fully dynamic on-demand assembly. A founding C-suite (CEO, EA, HR, COO, CSO) provides cold-start bootstrapping so the organisation can hire before any domain specialists exist.

**Self-evolution** operates at two levels: individuals refine their working principles through post-task reflection and CEO one-on-ones; the organisation updates its SOPs through project retrospectives and a formal HR performance pipeline (periodic reviews, performance improvement plans, automated offboarding). This creates persistent improvement without model retraining — a property no prior system in the comparison table achieves at both levels simultaneously.

On PRDBench (50 software engineering tasks), OMC achieves **84.67% success rate (+15.48pp over the best baseline, Claude-4.5 at 69.19%)**. Cost: ~$6.91 per task. The paper introduces an adaptive dispatch mode that routes simple tasks to a single agent and reserves multi-agent coordination for complex projects.

## Architecture: Talent–Container Separation

### Talent (portable agent identity)
A Talent package contains: role specification, base system prompt, tool bindings, skill set, working principles, and runtime hints. It is backend-agnostic — the same Talent can be deployed into a LangGraph Container, a Claude Code Container, or a script-based Container without modification. The Talent Market distributes validated Talent packages with benchmark-verified performance metrics.

### Container (runtime with 6 typed interfaces)

| Interface | Signature | OS Kernel Analogue |
|-----------|-----------|-------------------|
| Execution | execute(task, ctx) → (result, cost) | Process scheduler |
| Task | enqueue(task); dequeue() → task | Process queue / mutual exclusion |
| Context | assemble(role, guidance, memory) → ctx | Memory manager |
| Storage | read(key) → data; write(key, data) | File system |
| Event | publish(event); subscribe(filter) | IPC / message bus |
| Lifecycle | pre_hook(task, ctx); post_hook(task, result) | Security / audit / guardrails |

Three reference backend implementations: LangChain reactive agent, Claude Code session, script-based executor. Agents are stateless per execution; all state is persisted through the Storage interface.

### Founding C-suite

| Role | Function |
|------|----------|
| CEO | External goal injection; policy override; iteration decisions (optimal stopping) |
| EA (Executive Assistant) | Task decomposition; task tree construction; stakeholder relay |
| HR | Talent Market search; candidate shortlisting; hiring pipeline |
| COO | Task dispatch; dependency resolution; review gate enforcement |
| CSO (Chief Strategy Officer) | SOP maintenance; retrospective synthesis; organisational memory |

## E2R Tree Search

MCTS-inspired three-stage loop over a DAG task tree with both decomposition edges (parent → child subtask) and dependency edges (sibling sequencing):

**Stage 1: Explore** — Executive agents select a strategy: how to decompose the current task and whom to assign. Classic exploration–exploitation trade-off: proven employees (exploitation) vs. new hires or Talent Market recruits (exploration). Branching factor unbounded — the LLM decides decomposition granularity at runtime.

**Stage 2: Execute** — Each assigned agent runs the task through the organisational layer. Internal execution function `f_ev(d_v) → (r_v, c_v)` is opaque to the platform for closed-source agents (e.g., Claude Code).

**Stage 3: Review** — Reviewer (parent owner or COO) evaluates result `r_v`, produces quality signal `q_v ∈ {accept, reject}`. Acceptance propagates results downstream; rejection triggers retry or reassignment. After `k_rev = 3` rejections, escalation to higher supervisor. After `T_max = 3600s` timeout, task marked failed. After total cost `B`, system pauses.

**Bounded rationality guarantees**: every search episode terminates in bounded time and cost; the DAG execution layer provides formal deadlock freedom under the FSM lifecycle.

## Talent Market: Three Sourcing Types

| Type | Method | Best For |
|------|---------|----------|
| Type 1 | Curated from open-source repos; distilled into Talent format | Mature, battle-tested domains with existing implementations |
| Type 2 | Prompt persona (Agency-Agents, 140+ specialist personas) + auto-assembled SkillsMP skills | Role exists but no complete implementation |
| Type 3 | Fully dynamic: HR assembles both persona and skill set from SkillsMP on demand | Novel domains; bespoke requirements |

All three types produce standard Talent packages and enter the same runtime pathway. Hired agents start at the same employee level regardless of sourcing type.

## Self-Evolution Mechanisms

**Individual level**:
- Post-task self-reflection appended to the agent's persistent working principles
- CEO one-on-ones: structured feedback on strengths and gaps, updated in the Talent package

**Organisational level**:
- Project retrospectives: lessons learned synthesised into SOPs, injected into future agent contexts
- HR performance pipeline: periodic evaluations, performance improvement plans (PIP), automated offboarding of consistently underperforming agents

This creates a feedback loop where both individual agents and the organisation's playbooks improve without any model weight updates.

## Benchmark Results: PRDBench

| Agent Type | Method | Success Rate (%) |
|------------|--------|-----------------|
| Minimal | GPT-5.2 | 62.49 |
| Minimal | Claude-4.5 | 69.19 |
| Minimal | Gemini-3-Pro | 22.76 |
| Minimal | Qwen3-Coder | 43.84 |
| Minimal | DeepSeek-V3.2 | 40.11 |
| Commercial | CodeX | 62.09 |
| Commercial | Claude Code | 56.65 |
| Commercial | Gemini CLI | 11.29 |
| **Multi-agent** | **OMC (Claude Code Sonnet 4.6 + Gemini 3.1 Flash Lite)** | **84.67 (+15.48pp)** |

Cost per PRDBench task: ~$6.91. Baseline cost data not reported by PRDBench authors, so cost-efficiency comparison is not possible.

## Case Studies

| Case | Task | Team | Cost | Notable |
|------|------|------|------|---------|
| Content generation | GitHub AI Agent weekly trend report + email | GPT-4o (researcher) + Claude Sonnet 4 (writer) | $4.49 / <10 min | All 15 repository links verified real and accurate |
| Game development | Street-fighting web game | Claude Sonnet 4 + Gemini 2.5 + NanoBanana | — | Human evaluator triggered one re-exploration; agent created a new SkillsMP skill on-the-fly to fix sprite sheet segmentation |
| Audiobook production | Peaky Blinders retelling with animal characters, 8 scenes/episode, voice-over + video | Novel Writer (Claude Sonnet 4) + AV Producer (Gemini 3.1 Pro) | $1.57 / 1.56M tokens | Cross-modal coordination: script → image → TTS → video |
| Research survey | World models for embodied AI (2021–2026); mind map + 3 research ideas | Research Scientist × 2 (Claude Sonnet 4.6) + AI Engineer (self-hosted) | $16.26 / 15.9M tokens | 17 documents; mind map with 70 nodes, 35+ papers; 3 novel research ideas (HiTeWM, PhysWM, MAWM) |

The research survey case study generated research proposals directly on the [[wiki/concepts/world-modeling|World Modeling]] topic — the same area covered by Chu et al. (2026) in this wiki.

## Key Concepts

- [[wiki/concepts/agentic-ai|Agentic AI]] — OMC is the most organisationally complete multi-agent framework in the wiki; adds workforce management, Talent Market, and org-level self-evolution above the existing agentic frameworks
- [[wiki/concepts/ai-for-scientific-discovery|AI for Scientific Discovery]] — the research survey case study (17 documents, 3 novel research ideas) is the most autonomous academic research demonstration in the wiki
- [[wiki/sources/ai-agents-vs-agentic-ai|AI Agents vs. Agentic AI]] — the formal taxonomy that classifies OMC squarely in the "Agentic AI" category: multi-agent, orchestrated, adaptive, with emergent system-level behavior

## Key Entities

- [[wiki/entities/openbrain|OpenBrain]] — OMC's "corporation within a corporation" directly maps to the Agent-3 organisational structure described in AI 2027's OpenBrain scenario

## Notable Claims

- Neither team composition nor workflow is fixed before execution — the first system in the comparison to achieve both "Multi-Exec" support and "Org. Evol." simultaneously
- The OS kernel analogy is structurally grounded: each of the 6 typed interfaces maps to a canonical OS kernel subsystem, providing a principled abstraction rather than an ad-hoc orchestration API
- Self-evolution operates without model retraining — persistent improvement through working-principle updates and SOP injection
- PRDBench SOTA surpassed by +15.48pp (84.67% vs 69.19% Claude-4.5)
- The research survey case study produces genuinely novel research ideas (MAWM: meta-learning + conformal prediction for sim-to-real transfer verified as novel by the authors)

## Contradictions / Open Questions

- Self-evolution mechanisms (one-on-ones, retrospectives, performance reviews) are implemented but not ablated — unclear how much each contributes individually
- Evaluation confined to PRDBench (coding); cross-domain performance claims rest on uncontrolled case studies, not systematic benchmarks
- Cost overhead (~$6.91/task) is significant — adaptive dispatch mitigates this but the threshold for routing is not specified
- Talent Market ecosystem is described but not empirically assessed — how does agent quality vary across sourcing types?
- The human-in-the-loop (CEO optimal stopping) is modelled as a meta-level controller but its failure modes are not addressed — what happens when human judgment is poor or unavailable?

## Raw Source

`raw/2604.22446v1.pdf`
