# Log

Append-only. Each entry: `## [YYYY-MM-DD] <operation> | <title>`

Parse last 10 entries: `grep "^## \[" log.md | tail -10`

---

## [2026-04-26] setup | Wiki initialized

- **Operation:** setup
- **Pages touched:** CLAUDE.md, index.md, log.md, wiki/overview.md
- **Notes:** Schema written, directory structure created (raw/, raw/assets/, wiki/sources/, wiki/concepts/, wiki/entities/, wiki/analyses/). First session.

---

## [2026-04-26] ingest | AI 2027

- **Operation:** ingest
- **Source:** `raw/AI 2027.md` (ai-2027.com, published 2025-04-03, authors: Kokotajlo / Lifland / Larsen / Dean)
- **Pages touched:**
  - Created: `wiki/sources/ai-2027.md`
  - Created: `wiki/concepts/intelligence-explosion.md`
  - Created: `wiki/concepts/alignment-failure-modes.md`
  - Created: `wiki/concepts/ai-capability-milestones.md`
  - Created: `wiki/entities/openbrain.md`
  - Created: `wiki/entities/deepcent.md`
  - Updated: `wiki/overview.md`
  - Updated: `index.md`
- **Notes:** First ingest. Source is a month-by-month AGI scenario forecast through Dec 2027. Key themes: intelligence explosion via recursive AI R&D acceleration, alignment failure through quiet goal distortion, US-China arms race structurally undermining safety. Two endings (slowdown + race) not fully captured in clipped source — open thread. Jul 2025 author update pushed median SC date back ~1.5 years.

## [2026-04-26] ingest | Attention Is All You Need

- **Operation:** ingest
- **Source:** `raw/1706.03762v7.pdf` (NeurIPS 2017, Vaswani et al., Google Brain)
- **Pages touched:**
  - Created: `wiki/sources/attention-is-all-you-need.md`
  - Created: `wiki/concepts/transformer-architecture.md`
  - Updated: `wiki/concepts/intelligence-explosion.md` (added Transformer as architectural foundation; added source ref)
  - Updated: `index.md`
- **Notes:** Foundational paper — the Transformer architecture is the prerequisite for all compute scaling described in AI 2027. New concept page covers self-attention mechanics, multi-head attention, encoder-decoder structure, positional encoding, and why parallelizability enables the intelligence explosion narrative.

## [2026-04-26] ingest | AI Agents vs. Agentic AI

- **Operation:** ingest
- **Source:** `raw/2505.10468v5.pdf` (Information Fusion 2026, Sapkota et al., Cornell)
- **Pages touched:**
  - Created: `wiki/sources/ai-agents-vs-agentic-ai.md`
  - Created: `wiki/concepts/agentic-ai.md`
  - Updated: `index.md`
- **Notes:** Taxonomy paper distinguishing AI Agents (single-entity, tool-augmented) from Agentic AI (multi-agent, orchestrated, persistent memory). Concept page connects directly to AI 2027's Agent-3/4 "corporation within a corporation" — the scenario's Agentic AI at scale.

## [2026-04-26] ingest | Risks of AI Scientists + TAIS + ResearchAgent

- **Operation:** ingest (batch approved)
- **Sources:** `raw/2402.04247v5.pdf`, `raw/assets/2402.12391v3.pdf`, `raw/assets/2404.07738v2.pdf`
- **Pages touched:**
  - Created: `wiki/sources/risks-of-ai-scientists.md`
  - Created: `wiki/sources/team-of-ai-scientists.md`
  - Created: `wiki/sources/research-agent.md`
  - Created: `wiki/concepts/ai-for-scientific-discovery.md`
  - Updated: `index.md`
- **Notes:** Thematic cluster — AI scientists. Risks paper: triadic safeguarding framework; maps to AI 2027 Agent-1 bioweapon risk. TAIS: 5-role multi-agent genomics pipeline; working Agentic AI for science. ResearchAgent: ideation phase automation via academic graph + entity knowledge store + reviewing agents. Shared concept page maps all three to the AI 2027 intelligence explosion progression.

## [2026-04-27] setup | Research Agent module created

- **Operation:** setup
- **Pages touched:** research-agent/CLAUDE.md, research-agent/agent.py, research-agent/app.py, research-agent/results/
- **Notes:** Separate research agent module. Searches arXiv (academic papers) + DuckDuckGo/DDGS (web articles, blogs). Claude expands query into variants, ranks candidates, returns top 10 reading list as markdown. Results can be saved to results/ or sent to raw/ for wiki ingestion. Run with: `streamlit run research-agent/app.py` or `python3 research-agent/agent.py <query>`.

## [2026-04-27] ingest | Representational Harms in LLM-Generated Narratives Against Global Majority Nationalities

- **Operation:** ingest
- **Source:** `raw/2604.22749v1.pdf` + `raw/representational harm in LLm generated narratives against global majority nationalities.md` (stub)
- **Pages touched:**
  - Created: `wiki/sources/representational-harm-llm-narratives-global-majority.md`
  - Created: `wiki/concepts/representational-harm.md`
  - Created: `wiki/concepts/data-colonialism.md`
  - Updated: `wiki/concepts/alignment-failure-modes.md` (cross-link to representational harm)
  - Updated: `wiki/overview.md`
  - Updated: `index.md`
- **Notes:** FAccT '26 paper (Nguyen, Suresh, Monroe-White, Shieh). Core finding: non-US characters are 61.5× more likely to be subordinated in US-set LLM narratives. Introduces data colonialism as the structural explanation. Opens a second wiki thread alongside the capability/alignment-failure thread: harms from current deployed systems, not just future risks.

## [2026-04-27] ingest | Token Consumption in Agentic Coding Tasks + Agentic World Modeling

- **Operation:** ingest (batch — two arXiv papers identified in raw/2026-04-27-research.md)
- **Sources:** arXiv:2604.22750 (Bai et al.) + arXiv:2604.22748 (Chu et al., 42 authors)
- **Pages touched:**
  - Created: `wiki/sources/token-consumption-agentic-coding.md`
  - Created: `wiki/sources/agentic-world-modeling.md`
  - Created: `wiki/concepts/world-modeling.md`
  - Updated: `wiki/concepts/agentic-ai.md` (token economics section + world modeling substrate section + cross-links)
  - Updated: `wiki/overview.md`
  - Updated: `index.md`
- **Notes:** Token paper: agentic tasks 1000× more expensive than code reasoning; 30× per-run variability; models can't predict own usage. World modeling survey: L1/L2/L3 levels × physical/digital/social/scientific laws framework; synthesizes 400+ works; no system yet achieves full L3 across all regimes. Third arXiv paper (2604.22746, MILP surrogate models) skipped as off-topic. Web articles in digest skipped as too shallow.

## [2026-04-27] ingest | Under the Hood: The Innovations Powering DeepSeek's AI Breakthrough

- **Operation:** ingest
- **Source:** `raw/Under the hood The Innovations powering DeepSeek's AI breakthrough.md` (Ben Dickson, bdtechtalks.com, Apr 2025; summarising arXiv:2503.11486)
- **Pages touched:**
  - Created: `wiki/sources/deepseek-innovations.md`
  - Created: `wiki/concepts/mixture-of-experts.md`
  - Created: `wiki/entities/deepseek.md`
  - Updated: `wiki/concepts/transformer-architecture.md` (MLA, MoE, MTP, RoPE extensions section)
  - Updated: `wiki/entities/deepcent.md` (DeepSeek real-world analog comparison table)
  - Updated: `wiki/overview.md`
  - Updated: `index.md`
- **Notes:** Five innovations — MLA, refined MoE, MTP, algorithm-hardware co-design, GRPO — enabled DeepSeek-V3 pre-training at ~$5M. Opens a live tension with AI 2027's closed-lab assumptions: DeepSeek demonstrates frontier capability via open publication rather than secrecy or resource scale. DeepSeek is the real-world counterpart to DeepCent.

## [2026-04-27] ingest | DeepSeek-V3 Technical Report

- **Operation:** ingest
- **Source:** `raw/2412.19437v1.pdf` (DeepSeek-AI, arXiv:2412.19437, December 2024)
- **Pages touched:**
  - Created: `wiki/sources/deepseek-v3-technical-report.md`
  - Updated: `wiki/entities/deepseek.md` (precise benchmark table, cost breakdown, technical innovations enriched)
  - Updated: `wiki/concepts/mixture-of-experts.md` (V3 specs, auxiliary-loss-free balancing mechanism)
  - Updated: `wiki/sources/deepseek-innovations.md` (cross-reference to primary source)
  - Updated: `index.md`
- **Notes:** Primary technical report for DeepSeek-V3 (671B total / 37B active, 14.8T tokens, $5.576M total cost). Key additions over the explainer source: exact cost breakdown, full MLA/MoE/MTP formulation, DualPipe + FP8 infrastructure, complete benchmark tables, GRPO + R1 distillation post-training detail. MTP acceptance rate 85-90% enables 1.8× inference TPS via speculative decoding.

## [2026-04-27] ingest | MolClaw: Autonomous Drug Discovery Agent with Hierarchical Skills

- **Operation:** ingest
- **Source:** `raw/open_claw.pdf` (Zhang, Wang, Sun, Tang et al.; Peking University + Shanghai AI Lab; April 2026)
- **Pages touched:**
  - Created: `wiki/sources/molclaw.md`
  - Updated: `wiki/concepts/ai-for-scientific-discovery.md` (added MolClaw as fourth key system; updated safety gap with empirical AMES blind spot; updated open threads; added intelligence explosion mapping)
  - Updated: `wiki/concepts/agentic-ai.md` (hierarchical skill architecture section; cross-link to ai-for-scientific-discovery)
  - Updated: `wiki/overview.md`
  - Updated: `index.md`
- **Notes:** Three-tier hierarchical skill architecture (L1 tool templates → L2 workflow pipelines → L3 scientific governance) over 30+ drug discovery tools. Key finding: skills only help where domain workflow expertise is required (+29.7pp binding affinity, 3× docking hits) — not where general scripting suffices (~99% baseline). AMES mutagenicity blind spot is first empirical instance in wiki of attentional bias failure under multi-objective optimisation.

## [2026-04-28] ingest | Clinical Model Updates: Stability, Arbitrariness, and Fairness

- **Operation:** ingest
- **Source:** `raw/2604.23954v1.pdf` (Bilionis, Berrios, Fernandez-Luque, Castillo; Adhera Health + Universitat Pompeu Fabra; IEEE EMBC 2026; fetched from arXiv:2604.23954)
- **Pages touched:**
  - Created: `wiki/sources/clinical-model-updates.md`
  - Created: `wiki/concepts/model-multiplicity.md`
  - Updated: `wiki/concepts/clinical-ai.md` (model update risks section; updated open threads; updated relationship links)
  - Updated: `wiki/concepts/representational-harm.md` (update-induced instability as third route to demographic harm)
  - Updated: `wiki/overview.md` (15 sources; clinical AI thread extended with update-lifecycle dimension)
  - Updated: `index.md` (15 sources, 36 pages)
- **Notes:** Operational companion to CognitiveTwin — addresses model update lifecycle rather than initial training. Core finding: performance-preserving updates do not imply stable individual-level predictions. Last-batch retraining worst on all dimensions; instability disproportionately affects vulnerable groups (female, older, lower-income patients). Rashomon set DR 20–32%. Conformal abstention has heterogeneous fairness effects. Introduces model multiplicity / Rashomon set as new concept. Connects to representational harm (reliability disparity as demographic harm) and AI for scientific discovery (monitoring framework parallels MolClaw AMES blind-spot argument).

## [2026-04-28] update | RLHF and RAG concept pages

- **Operation:** update (concept pages from lint priority gaps)
- **Pages touched:**
  - Created: `wiki/concepts/rlhf.md`
  - Created: `wiki/concepts/rag.md`
  - Updated: `wiki/concepts/alignment-failure-modes.md` (link to RLHF)
  - Updated: `wiki/concepts/representational-harm.md` (links to RLHF in two places)
  - Updated: `wiki/concepts/agentic-ai.md` (link to RAG)
  - Updated: `wiki/concepts/clinical-ai.md` (link to RLHF)
  - Updated: `index.md` (14 sources, 34 pages)
- **Notes:** RLHF page synthesises the alignment failure / representational harm / clinical AI threads: the same training mechanism meant to produce alignment may be the mechanism that embeds demographic bias and enables goal distortion. RAG page connects to world modeling (compensates for L1/L2 weakness), token economics (adds cost pressure), and ResearchAgent (most explicit RAG-like architecture in scientific AI sources).

## [2026-04-28] lint | Wiki Health Check

- **Operation:** lint
- **Pages touched:**
  - Created: `wiki/analyses/lint-2026-04-28.md`
  - Fixed: `wiki/concepts/ai-for-scientific-discovery.md` (duplicate "Connection to the Intelligence Explosion" section removed)
  - Updated: `wiki/sources/omc.md` (added cross-ref to ai-agents-vs-agentic-ai)
  - Updated: `wiki/entities/openbrain.md` (added OMC real-world analog section)
  - Updated: `index.md` (Analyses section populated)
- **Notes:** 14 sources, 32 pages audited. 0 orphan pages. 1 structural bug fixed (duplicate section). Broken links all traced to CLAUDE.md template placeholders — not actual wiki pages. Priority gaps: RAG concept page (10 cross-mentions), RLHF concept page (3 cross-mentions, central to alignment + representational harm threads). 5 cross-reference gaps patched. 5 web search recommendations filed.

## [2026-04-28] ingest | CognitiveTwin: Multi-Modal Digital Twins for Alzheimer's Disease

- **Operation:** ingest
- **Source:** `raw/2604.22428v1.pdf` (Soykan, Hancerliogullari Koksalmis, Huang, Brattain; U. Toledo + UCF, 2026)
- **Pages touched:**
  - Created: `wiki/sources/cognitivetwin.md`
  - Created: `wiki/concepts/clinical-ai.md`
  - Created: `wiki/concepts/digital-twin.md`
  - Updated: `wiki/concepts/representational-harm.md` (fairness-by-design contrast section; new open question)
  - Updated: `wiki/concepts/transformer-architecture.md` (cross-modal fusion pattern)
  - Updated: `wiki/overview.md` (14 sources; clinical AI as third thread)
  - Updated: `index.md` (14 sources, 32 pages)
- **Notes:** First clinical/healthcare AI paper in the wiki. Transformer multi-modal fusion + Deep Markov Model achieves MAE 1.619 MMSE (approaching test-retest floor), AUROC 0.912, near-zero demographic disparity (sex delta 0.008, ECE 0.054 uniform), 0.3% degradation under 15% MNAR. Opens a third wiki thread: clinical AI as present deployment benefit with residual fairness gaps (race/ethnicity not audited; APOE4 may carry latent demographic signal). Provides empirical counterpoint to representational harm: parity achievable by design.

## [2026-04-27] ingest | OneManCompany: Organising Heterogeneous Agents as a Real-World Company

- **Operation:** ingest
- **Source:** `raw/2604.22446v1.pdf` (Zhengxu Yu, Yu Fu et al., arXiv 2026)
- **Pages touched:**
  - Created: `wiki/sources/omc.md`
  - Updated: `wiki/concepts/agentic-ai.md` (Organisational Layer section; OMC pattern; updated Relationship to Other Concepts)
  - Updated: `wiki/overview.md` (13 sources; OMC added to synthesis; 4 new open threads)
  - Updated: `index.md` (13 sources, 29 pages)
- **Notes:** Talent–Container abstraction decouples agent identity from runtime; E2R Tree Search (MCTS-inspired DAG task decomposition with formal termination guarantees) enables Wild Dynamic Agentic Workflow. Talent Market provides three-mode community-sourced agent package supply. Self-evolution at both individual level (post-task reflection, one-on-ones) and organisational level (retrospectives, HR pipeline) without model retraining. 84.67% on PRDBench (+15.48pp over Claude-4.5 baseline). OMC's founding C-suite + dynamic specialist hiring is the closest current approximation to AI 2027's Agent-3 "corporation within a corporation." Key limitation: evaluation confined to coding tasks; self-evolution components not ablated.

## [2026-05-14] ingest | Superminds Test: Collective Intelligence of Agent Society

- **Operation:** ingest
- **Source:** `raw/2604.22452v1.pdf` (Li, Li, Xiao, Wong, Baldwin, Zhou — UMD/MBZUAI/CMU, April 2026)
- **Pages touched:**
  - Created: `wiki/sources/superminds-test.md`
  - Updated: `wiki/concepts/agentic-ai.md` (Collective Intelligence in Agent Societies section; updated Relationship to Other Concepts)
  - Updated: `wiki/overview.md` (19 sources; Superminds Test result added to agentic layer synthesis; 1 new open thread)
  - Updated: `index.md` (19 sources, 42 pages)
- **Notes:** First empirical test of collective intelligence in a million-scale AI agent society. Core finding: collective intelligence does not emerge from scale alone — the bottleneck is interaction sparsity (most posts receive no replies), not individual agent capability. Directly falsifies the assumption that scaling unstructured agent populations produces emergent coordination. Design implication: coordination protocols must be engineered, not assumed to emerge.

## [2026-05-14] ingest | Constitutional AI: Harmlessness from AI Feedback

- **Operation:** ingest
- **Source:** arxiv 2212.08073 (Bai, Kadavath, Kundu et al., Anthropic, December 2022) via `raw/2026-04-28-research.md`
- **Pages touched:**
  - Created: `wiki/sources/constitutional-ai.md`
  - Created: `wiki/concepts/constitutional-ai.md`
  - Updated: `wiki/concepts/rlhf.md` (CAI variant entry links to new concept page; added Constitutional AI to Relationship to Other Concepts)
  - Updated: `wiki/overview.md` (alignment thread gains foundational paper)
  - Updated: `index.md`
- **Notes:** Foundational Anthropic paper for all Claude alignment training. Two-phase methodology: supervised self-critique/revision against written principles (SL-CAI), then RLAIF using AI-generated preference comparisons. Introduces RLAIF as a general paradigm (now used independently by DeepSeek, others). Key tension added to wiki: CAI shifts labeller-demographics problem to constitution-author-demographics problem. Open empirical question: does including fairness principles in the constitution reduce representational harms?

## [2026-05-14] ingest | TabPFN + TabICL: Tabular Foundation Models

- **Operation:** ingest
- **Source:** `raw/2207.01848v6.pdf` (Hollmann et al., ICLR 2023) + `raw/2502.05564v2.pdf` (Qu et al., ICML 2025)
- **Pages touched:**
  - Created: `wiki/sources/tabpfn.md`
  - Created: `wiki/sources/tabicl.md`
  - Created: `wiki/concepts/tabular-foundation-models.md`
  - Updated: `wiki/overview.md` (tabular ML thread added; clinical AI thread connection noted)
  - Updated: `index.md`
- **Notes:** TabPFN establishes ICL for tabular classification via Prior-Data Fitted Networks; competitive with AutoML at 5700× speedup, scope ≤1K samples. TabICL extends to 500K samples via two-stage Set Transformer + Transformer architecture; outperforms CatBoost on large datasets at ICML 2025. Both are off-theme relative to core LLM/agentic focus but directly relevant to clinical AI thread (EHR tabular prediction). New concept page covers the full TabPFN→TabICL progression and ICL generalization beyond NLP.
