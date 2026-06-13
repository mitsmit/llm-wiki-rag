---
title: RAG — Retrieval-Augmented Generation
type: concept
tags: [rag, retrieval, grounding, hallucination, agentic-ai, memory]
sources: [2402.12391v3, ai-agents-vs-agentic-ai]
created: 2026-04-28
updated: 2026-04-28
---

## Definition

Retrieval-Augmented Generation (RAG) is a technique that augments an LLM's context at inference time with documents retrieved from an external knowledge store, rather than relying solely on knowledge encoded in model weights during pretraining. The model receives both the original prompt and the retrieved passages, and generates a response grounded in that retrieved evidence.

RAG addresses two fundamental limitations of standalone LLMs: **hallucination** (generating confident but false claims) and **knowledge cutoff** (no awareness of events after the training data ends). Both limitations become acute when LLMs are deployed as agents that need to reason over current, specialised, or verifiable information.

## Standard Pipeline

```
Query → Retriever → Relevant documents → [Query + Documents] → LLM → Grounded response
```

**Step 1: Indexing**
A corpus of documents (wiki pages, papers, codebases, databases) is chunked, embedded into dense vector representations using an embedding model, and stored in a vector database.

**Step 2: Retrieval**
At query time, the query is embedded and the most semantically similar document chunks are retrieved (typically via cosine similarity / approximate nearest-neighbour search). The `k` most relevant chunks are selected.

**Step 3: Augmented Generation**
Retrieved chunks are prepended to the prompt as context. The LLM generates a response conditioned on both the original query and the retrieved evidence. The response is grounded in the retrieved documents — the model can cite, quote, and synthesise from them.

## Variants

| Type | How retrieval is triggered | Use case |
|------|--------------------------|----------|
| Naive RAG | Single retrieval before generation | Simple QA |
| Iterative RAG | Multiple retrieval rounds interleaved with reasoning | Complex multi-hop questions |
| Agentic RAG | LLM decides when and what to retrieve as a tool call | General-purpose agentic systems |
| Graph RAG | Retrieval over knowledge graphs, not flat text | Structured domain knowledge |

## RAG in the Wiki's Agentic Systems

[[wiki/concepts/agentic-ai|Agentic AI]] lists RAG as a proposed solution for hallucination in single-agent systems. In practice, RAG shows up across the wiki's scientific discovery systems:

**ResearchAgent** ([[wiki/sources/research-agent|Baek et al., 2024]]) explicitly builds a RAG-like architecture: an academic knowledge graph + entity-centric knowledge store is queried during idea generation to retrieve relevant prior work. The iterative reviewing agents then ground their critiques in the retrieved literature. This is the closest thing to a systematic RAG implementation in the wiki's scientific AI sources.

**MolClaw** ([[wiki/sources/molclaw|Zhang et al., 2026]]) uses the Science Context Protocol to query external computational chemistry tools and databases — a form of structured retrieval (tool-based rather than text-based) integrated into the L1 skill layer.

**OMC** ([[wiki/sources/omc|Yu, Fu et al., 2026]]) uses the Talent Market as a retrieval system for agent packages: the HR agent queries the marketplace and retrieves ranked Talent candidates. The Storage interface provides persistent key-value retrieval for cross-agent memory across the organisation. Both are RAG-adjacent mechanisms applied to agent rather than document retrieval.

## RAG and World Modeling

The relationship between RAG and [[wiki/concepts/world-modeling|World Modeling]] is structurally important:

- An L1 predictor (reactive, single-step) benefits most from RAG: its internal world knowledge is shallow, so external retrieval compensates
- An L2 simulator (planning over multi-step trajectories) depends less on retrieval if its world model is comprehensive — but still benefits for rapidly-changing or domain-specific knowledge
- An L3 evolver (revises its own model from evidence) can in principle update its internal parameters in a way that makes retrieval redundant for stable knowledge — but no current system achieves this

Current agentic systems are mostly L1/early-L2. RAG is therefore load-bearing: it is compensating for the weakness of internal world models. As L2 capability increases, the role of RAG may shift from knowledge compensation to real-time grounding of events the world model could not have anticipated.

## Token Cost

RAG adds tokens to every context: the retrieved passages must fit within the context window alongside the reasoning and output. For agentic tasks that already consume ~1000× more tokens than reasoning tasks ([[wiki/sources/token-consumption-agentic-coding|Bai et al., 2026]]), RAG creates additional pressure. Iterative RAG compounds this — each retrieval round adds more context.

This creates a direct tension: RAG improves grounding but increases token cost and latency, exacerbating the already high per-run variability documented in the token consumption study.

## Limitations

| Limitation | Description |
|------------|-------------|
| Retrieval ceiling | Model can only use what's retrieved; poor retrieval silently produces confident wrong answers |
| Context window pressure | Retrieved documents compete with reasoning and output for context budget |
| Chunk boundary artefacts | Splitting documents into fixed-size chunks can cut across the precise information needed |
| Embedding model dependence | Retrieval quality depends entirely on embedding model quality; domain mismatch degrades recall |
| Latency | Each retrieval round adds network/compute latency; iterative RAG multiplies this |
| No grounding verification | The LLM can still hallucinate about retrieved content, or misattribute information |

## Open Questions

- At what L-level of world modeling does RAG become unnecessary — or does real-time retrieval remain useful even for L3 systems?
- Can RAG be combined with the token consumption budgeting literature (Bai et al.) to limit retrieval to only the questions where internal model uncertainty is above a threshold?
- For agentic systems with persistent shared memory (Agentic AI pattern), is the shared episodic store a form of RAG, or something qualitatively different?
- MolClaw's L3 scientific governance principles are "retrieved" (loaded at the start of every run) from a fixed document — is this RAG, few-shot prompting, or something else? The distinction matters for how we think about updating scientific governance as knowledge advances.

## Relationship to Other Concepts

- [[wiki/concepts/agentic-ai|Agentic AI]] — RAG is proposed as the primary solution to hallucination in single-agent systems; persistent shared memory in multi-agent systems is a RAG-adjacent architecture
- [[wiki/concepts/world-modeling|World Modeling]] — RAG compensates for weak L1/L2 world models; as internal modeling improves, the role of retrieval may shift
- [[wiki/sources/research-agent|ResearchAgent]] — the most explicit RAG-like architecture in the wiki's scientific AI cluster; academic knowledge graph + entity-centric store
- [[wiki/sources/token-consumption-agentic-coding|Token Consumption in Agentic Coding]] — RAG adds context tokens to an already token-expensive task class; creates compound cost pressure
