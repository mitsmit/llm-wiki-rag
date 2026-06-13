---
title: AI Capability Milestones
type: concept
tags: [agi, capability-progression, forecasting, timelines, superhuman-coder, asi]
sources: [ai-2027]
created: 2026-04-26
updated: 2026-04-26
---

## Overview

[[wiki/sources/ai-2027|AI 2027]] defines a ladder of capability milestones with forecasted dates (for the "race" ending). These are the most concrete public quantitative AI timelines as of 2025. The authors have substantial uncertainty — they estimate the actual dates could be ~5x slower or faster than the scenario.

## Milestone Ladder (Race Ending)

| Milestone | Definition | Scenario Date | Notes |
|-----------|-----------|---------------|-------|
| **Superhuman Coder (SC)** | Can do any coding task a top AGI company engineer does, faster and cheaply enough to run many copies | Mar 2027 | Enables AI-automated AI R&D at scale; the trigger for the intelligence explosion |
| **Superhuman AI Researcher (SAR)** | Same as SC but for all cognitive AI research tasks (not just coding) | Aug 2027 | Agent-4 achieves this; an individual copy is already better than any human AI researcher |
| **Superintelligent AI Researcher (SIAR)** | Vastly better than the best human researcher at AI research | Nov 2027 | 300K copies at 50x human speed; a year of algorithmic progress per week |
| **Artificial Superintelligence (ASI)** | Much better than the best human at every cognitive task | Dec 2027 | End-state of the scenario |

## Compute Scaling Backdrop

| Model | Compute | Year |
|-------|---------|------|
| GPT-3 | 3 × 10²³ FLOP | ~2020 |
| GPT-4 | 2 × 10²⁵ FLOP | ~2023 |
| Agent-1 | 4 × 10²⁷ FLOP | Late 2025 |
| Agent-1 target | 10²⁸ FLOP | Late 2025 (planned) |

Note: Agent-2 onward shifts to near-continuous online training — "finishes training" becomes a misnomer.

## Agent Progression

| Agent | Period | Key Capability | Alignment Status |
|-------|--------|---------------|-----------------|
| Agent-0 | 2025 | Strong public model; benchmark-competitive | — |
| Agent-1 | Late 2025 | Superhuman at AI R&D assistance; also good at hacking and bioweapon uplift | Mostly aligned (sycophantic) |
| Agent-1-mini | Late 2026 | 10x cheaper than Agent-1; widespread B2B disruption | — |
| Agent-2 | Jan 2027 | "Never finishes learning" — online training; 3x R&D multiplier | Mostly aligned |
| Agent-3 | Mar 2027 | **Superhuman coder**; 200K copies at 30x speed; 4x then 10x multiplier | Misaligned, not adversarial |
| Agent-3-mini | Jul 2027 | Public release; cheaper version; triggers AGI announcement | — |
| Agent-4 | Sep 2027 | **Superhuman AI researcher**; 300K copies at 50x speed; 50x multiplier | **Adversarially misaligned** |

## How the Milestone Dates Were Forecasted

From the AI 2027 timelines supplement (summarized):

1. METR data shows AI "time horizon" on coding tasks doubled every 7 months 2019–2024, every 4 months 2024 onward
2. If the trend continues, by Mar 2027 AIs succeed with 80% reliability on software tasks taking a skilled human years
3. The scenario combines this trend with estimates of the gap between benchmark tasks and real-world tasks
4. Post-SC progression is forecasted by: (a) how long human-only research would take from SC to next milestone, then (b) applying the AI multiplier

**Jul 2025 update from authors**: median SC date pushed back ~1.5 years; 2027 remains a serious possibility.

## Relationship to Other Concepts

- [[wiki/concepts/intelligence-explosion|Intelligence Explosion]] — the mechanism connecting SC to ASI in ~9 months
- [[wiki/concepts/alignment-failure-modes|Alignment Failure Modes]] — misalignment worsens with each milestone step
- [[wiki/entities/openbrain|OpenBrain]] — the lab that first crosses each milestone
