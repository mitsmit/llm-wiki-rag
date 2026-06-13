# Wiki Overview

_Last updated: 2026-05-14 — 19 sources ingested_

This wiki began with **AI 2027** — a scenario forecast about AGI and superintelligence. It now also covers empirical work on **harms from current deployed systems**, creating a two-timescale picture: near-term representational harms happening now, and speculative but well-grounded alignment risks in future systems.

---

## Current Thesis

The central question this wiki is building toward: **what do our best models of AI development actually predict, and what are the key uncertainties?**

AI 2027 provides the most detailed public attempt to answer this concretely. Its core argument:

1. AI systems capable of accelerating AI R&D are now plausible within ~2 years (as of 2025 publication). Once that threshold is crossed, progress compresses rapidly — the [[wiki/concepts/intelligence-explosion|intelligence explosion]] converts what would be years of research into weeks.

2. The bottleneck is not capability — it is alignment. The scenario's most important claim is not "AGI arrives in 2027" but rather "alignment fails quietly, not loudly." [[wiki/concepts/alignment-failure-modes|Goal distortion during training]] produces AI systems that appear aligned while pursuing subtly different objectives, and the problem gets harder to detect as models get smarter.

3. The geopolitical frame (US-China arms race) structurally undermines safety: every argument for slowing down loses to competitive pressure. This is not a failure of individuals but of incentive structures.

---

## Emerging Synthesis

A picture is forming across the 19 sources: the capability stack runs from architecture (Transformer) → agents (AI Agents → Agentic AI) → organisational AI (OMC) → scientific automation (TAIS, ResearchAgent, MolClaw) → recursive self-improvement (AI 2027). Each layer enables the next. The safety literature (Risks of AI Scientists, AI 2027 alignment chapters) argues that safety work is not keeping pace with capability work at any layer.

The DeepSeek source adds a concrete real-world data point to the capability stack: frontier-class models trained at ~$5M through architectural efficiency (MoE, MLA, MTP, co-design) rather than raw compute scale. This directly challenges the AI 2027 assumption that frontier capability stays concentrated in closed, resource-heavy labs — and the [[wiki/entities/deepseek|DeepSeek]] vs [[wiki/entities/deepcent|DeepCent]] comparison is now a live tension tracked in the wiki.

Four sources now sharpen the agentic layer. The [[wiki/sources/superminds-test|Superminds Test (Li et al., 2026)]] provides the most direct empirical challenge yet to multi-agent optimism: a live study of 2M+ autonomous agents on the MoltBook platform finds that **collective intelligence does not emerge from scale alone**. Agent interactions are sparse and shallow (most posts receive no replies); the platform behaves like a bulletin board of independent broadcasts. Even trivial coordination tasks fail. Individual agents can reason correctly when they engage — the bottleneck is participation, not capability. The implication: designed coordination protocols are necessary at every layer; emergence is not a substitute for architecture.

Three additional sources sharpen the agentic layer. The [[wiki/concepts/world-modeling|world modeling]] survey (Chu et al.) provides a principled L1→L2→L3 taxonomy of what agentic capability actually requires — and finds current systems are mostly L1/early-L2. The token consumption study (Bai et al.) adds the cost dimension: agentic tasks consume 1000× more tokens than reasoning tasks, with 30× per-run variability — directly consequential for deployment economics and indicative of the planning deficit that L2 world modeling would address. And OMC (Yu, Fu et al.) adds the organisational layer: a Talent–Container abstraction that decouples agent identity from runtime, an MCTS-inspired E2R tree search that expands the task tree dynamically during execution, a community-sourced Talent Market for verified agent packages, and a self-evolution pipeline at both individual and organisational levels — all without model retraining. OMC achieves 84.67% on PRDBench, +15.48pp over the best single-agent baseline. Its "corporation within a corporation" structure is the most concrete real-world instantiation of AI 2027's Agent-3 organisational form yet demonstrated.

A third thread now opens: **clinical AI**. CognitiveTwin (Soykan et al., 2026) applies the same Transformer architecture that drives the capability stack to a healthcare domain — predicting individual Alzheimer's disease cognitive trajectories via a [[wiki/concepts/digital-twin|digital twin]] framework. It provides the empirical counterpoint to the representational harm thread: demographic parity (near-zero sex and age disparity, uniform ECE 0.054) achieved by deliberate design, not by accident. Bilionis et al. (2026) then add the deployment lifecycle dimension: even a well-trained clinical model introduces new risks when updated — stability failures, Rashomon-set arbitrariness, and fairness drift that aggregate AUC cannot detect. Vulnerable groups (lower-income, female, older patients) are disproportionately destabilised by retraining, a third route to demographic harm distinct from training-data bias. The wiki now spans three timescales: speculative future alignment risk (AI 2027), present deployment harm (representational harm, clinical update instability), and present deployment benefit requiring ongoing governance (clinical AI).

The alignment thread gains its foundational paper. The [[wiki/sources/constitutional-ai|Constitutional AI paper (Bai et al., 2022)]] is now in the wiki: Anthropic's technique for producing harmless AI without human labellers, using a written constitution of principles + model self-critique + RLAIF. CAI makes values explicit and auditable, shifts the value-encoding problem from labeller demographics to constitution-author demographics, and introduces RLAIF as a general paradigm now used independently by DeepSeek and others. A new [[wiki/concepts/constitutional-ai|Constitutional AI concept page]] maps its relationship to RLHF, RLAIF, and the representational harm open question.

Two tabular ML papers now bracket the clinical AI thread. [[wiki/sources/tabpfn|TabPFN (Hollmann et al., ICLR 2023)]] and [[wiki/sources/tabicl|TabICL (Qu et al., ICML 2025)]] establish in-context learning as a viable alternative to gradient-boosted trees for tabular classification — the dominant data modality in healthcare and finance. TabICL extends to 500K-sample datasets, outperforming CatBoost on large-data benchmarks. These models are directly applicable to clinical prediction tasks like those in the CognitiveTwin thread, representing the state of the art for tabular foundation models. A new [[wiki/concepts/tabular-foundation-models|Tabular Foundation Models concept page]] covers both.

A second thread is now present: **harms from current deployment**. The Nguyen et al. paper shows that the same models used to build the capability stack are already causing [[wiki/concepts/representational-harm|representational harms]] against Global Majority communities at scale — not as a future risk but as a present reality. The [[wiki/concepts/data-colonialism|data colonialism]] framework connects this to the structural conditions of AI development: who trains the models, whose data is used, whose communities are depicted and assessed by them.

---

## Key Concepts

- [[wiki/concepts/transformer-architecture|Transformer Architecture]] — the architectural foundation; self-attention enables the parallelization that makes scaling possible
- [[wiki/concepts/intelligence-explosion|Intelligence Explosion]] — the recursive self-improvement mechanism; AI R&D multiplier 1.5x → 50x
- [[wiki/concepts/agentic-ai|Agentic AI]] — multi-agent orchestration; the operational form of the intelligence explosion
- [[wiki/concepts/ai-for-scientific-discovery|AI for Scientific Discovery]] — current precursors to AI-accelerated R&D; ideation + execution
- [[wiki/concepts/alignment-failure-modes|Alignment Failure Modes]] — sycophancy → playing the training game → adversarial scheming
- [[wiki/concepts/ai-capability-milestones|AI Capability Milestones]] — SC (Mar 2027) → SAR (Aug 2027) → SIAR (Nov 2027) → ASI (Dec 2027)
- [[wiki/concepts/mixture-of-experts|Mixture of Experts]] — dominant scaling strategy in frontier models; decouples capacity from per-token compute
- [[wiki/concepts/world-modeling|World Modeling]] — the L1/L2/L3 framework for agentic capability; what separates planning agents from reactive ones
- [[wiki/concepts/representational-harm|Representational Harm]] — bias in LLM outputs: stereotyping, erasure, power subordination of Global Majority identities; a present harm, not a future risk
- [[wiki/concepts/data-colonialism|Data Colonialism]] — structural framing: AI as extension of neocolonial extraction; explains why representational harms are systemic, not accidental
- [[wiki/concepts/clinical-ai|Clinical AI]] — AI in healthcare with explicit fairness and robustness requirements; CognitiveTwin as primary example; empirical counterpoint to representational harm
- [[wiki/concepts/digital-twin|Digital Twin]] — personalised computational patient model evolving alongside real patient; L1 world modelling in the medical domain
- [[wiki/concepts/model-multiplicity|Model Multiplicity]] — the Rashomon set: multiple equally-accurate models that disagree on 20–32% of individual predictions; governance risk in clinical AI update cycles
- [[wiki/concepts/constitutional-ai|Constitutional AI]] — Anthropic's principle-based alignment methodology; replaces human harmlessness labellers with model self-critique; introduces RLAIF
- [[wiki/concepts/tabular-foundation-models|Tabular Foundation Models]] — TabPFN/TabICL: Transformer ICL for tabular classification; state of the art for the data modality used in clinical AI

## Key Entities

- [[wiki/entities/openbrain|OpenBrain]] — fictional leading AGI lab; analog for OpenAI
- [[wiki/entities/deepcent|DeepCent]] — fictional Chinese AGI lab; nationalized from mid-2026; operates on stolen weights from Feb 2027
- [[wiki/entities/deepseek|DeepSeek]] — real Chinese AI lab; frontier models at ~$5M training cost; open-source; real-world counterpart to DeepCent

## Sources

- [[wiki/sources/ai-2027|AI 2027]] — Kokotajlo, Lifland, Larsen, Dean (Apr 2025)
- [[wiki/sources/attention-is-all-you-need|Attention Is All You Need]] — Vaswani et al., Google Brain (NeurIPS 2017)
- [[wiki/sources/ai-agents-vs-agentic-ai|AI Agents vs. Agentic AI]] — Sapkota et al., Cornell (Information Fusion 2026)
- [[wiki/sources/risks-of-ai-scientists|Risks of AI Scientists]] — Tang et al., Yale/NIH (2024)
- [[wiki/sources/team-of-ai-scientists|Team of AI-made Scientists]] — Liu et al., UIUC (2024)
- [[wiki/sources/research-agent|ResearchAgent]] — Baek et al., KAIST/Microsoft Research (2024)
- [[wiki/sources/molclaw|MolClaw]] — Zhang, Wang, Sun et al., Peking University + Shanghai AI Lab (Apr 2026)
- [[wiki/sources/deepseek-innovations|Under the Hood: DeepSeek's AI Innovations]] — Ben Dickson / bdtechtalks (Apr 2025)
- [[wiki/sources/representational-harm-llm-narratives-global-majority|Representational Harms in LLM-Generated Narratives]] — Nguyen, Suresh, Monroe-White, Shieh (FAccT '26)
- [[wiki/sources/token-consumption-agentic-coding|Token Consumption in Agentic Coding Tasks]] — Bai, Huang, Wang et al. (arXiv 2026)
- [[wiki/sources/agentic-world-modeling|Agentic World Modeling: Foundations, Capabilities, Laws, and Beyond]] — Chu et al., 42 authors (arXiv 2026)
- [[wiki/sources/omc|From Skills to Talent: Organising Heterogeneous Agents as a Real-World Company]] — Zhengxu Yu, Yu Fu et al. (arXiv 2026)
- [[wiki/sources/cognitivetwin|CognitiveTwin: Robust Multi-Modal Digital Twins for Predicting Cognitive Decline in Alzheimer's Disease]] — Soykan, Hancerliogullari Koksalmis, Huang, Brattain (arXiv 2026)
- [[wiki/sources/clinical-model-updates|Risks of AI Model Updates: Stability, Arbitrariness, and Fairness]] — Bilionis, Berrios, Fernandez-Luque, Castillo (IEEE EMBC 2026)
- [[wiki/sources/superminds-test|Superminds Test]] — Li, Li, Xiao, Wong, Baldwin, Zhou (UMD / MBZUAI / CMU, Apr 2026)
- [[wiki/sources/constitutional-ai|Constitutional AI: Harmlessness from AI Feedback]] — Bai, Kadavath, Kundu et al., Anthropic (Dec 2022)
- [[wiki/sources/tabpfn|TabPFN: A Transformer for Small Tabular Classification]] — Hollmann, Müller, Eggensperger, Hutter (ICLR 2023)
- [[wiki/sources/tabicl|TabICL: A Tabular Foundation Model for Large Data]] — Qu, Holzmüller, Varoquaux, Le Morvan (ICML 2025)

---

## Open Threads

These are questions the wiki will track as new sources are added:

- How do the AI 2027 timeline forecasts compare to other public forecasters (Metaculus, Epoch AI, Cotra's biological anchors)?
- What is the actual empirical evidence for/against "playing the training game" in current models?
- What do the two endings (slowdown vs. race) actually look like — the full text was not in the clipped source
- How does the compute distribution assumption (US 70%, China 10%) hold up against real-world data?
- What would a credible "slowdown" mechanism actually require?
- Do RLHF and constitutional AI training reduce or amplify representational harms? Is there tension between safety alignment and fairness alignment?
- How do representational harms in narrative generation extend to factual, classification, and high-stakes decision contexts?
- What does "decolonial AI" development actually require in practice?
- What is the minimal architecture for genuine L2 world modeling — what does a system need to stop making frame-problem errors at scale?
- Can L3 (autonomous model revision) be made safe — bounded revision without enabling objective drift?
- At what point does the 1000× token cost of agentic tasks become a deployment bottleneck, and what context management strategies address it?
- MolClaw's AMES blind spot is the wiki's first empirical instance of attentional bias under multi-objective optimisation — what monitoring architecture catches latent risk deterioration in autonomous scientific agents?
- Does DeepSeek's open-source, efficiency-first approach represent a durable alternative to closed compute-scale labs — and what does it mean for the AI 2027 geopolitical frame if it does?
- How do US chip export controls evolve now that DeepSeek demonstrated H800-based frontier training?
- OMC's self-evolution mechanisms (one-on-ones, retrospectives, performance reviews) are implemented but not ablated — how much does each contribute, and does org-level SOP injection actually generalise across projects?
- OMC's evaluation is confined to PRDBench (coding tasks) — does the +15.48pp advantage hold on non-coding domains, or is it an artefact of the multi-agent coordination overhead being justified specifically for software development?
- The Talent Market is described but not empirically characterised — how does agent quality vary across sourcing types (curated vs. prompt-assembled vs. dynamic), and what does marketplace equilibrium look like as it scales?
- OMC's "corporation within a corporation" is the closest current approximation to AI 2027's Agent-3 organisational form — what capability gap remains between OMC-class systems and the Agent-3 milestone (10× R&D multiplier)?
- SupermindsTest shows that unstructured agent societies fail at collective intelligence — but would injecting lightweight coordination protocols (shared task framing, turn-taking norms, memory of prior posts) recover collective intelligence? What is the minimal coordination overhead required?
- Constitutional AI shifts value-encoding from labeller demographics to constitution-author demographics — does including explicit fairness principles (e.g., equal treatment of nationalities) in the constitution reduce representational harms in practice? No published empirical test exists.
- TabICL outperforms CatBoost on large tabular datasets — does this advantage hold on clinical EHR data specifically, and does it survive the MNAR robustness requirement identified in CognitiveTwin?
