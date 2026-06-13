---
title: DeepCent
type: entity
tags: [ai-lab, fictional, china, us-china-race, deepcent]
sources: [ai-2027]
created: 2026-04-26
updated: 2026-04-27
---

## Overview

DeepCent is the fictional leading Chinese AGI company in the [[wiki/sources/ai-2027|AI 2027]] scenario, described as China's analog to [[wiki/entities/openbrain|OpenBrain]]. It operates under CCP direction and eventually leads a nationalized collective of Chinese AI research.

## Compute Position

China's compute disadvantage is a structural constraint throughout the scenario:
- **Mid 2026**: China has ~12% of world AI-relevant compute; older technology; ~3 years behind US-Taiwanese frontier chips; DeepCent ~6 months behind best OpenBrain models
- **Post-nationalization**: ~40–50% of China's AI compute directed to DeepCent-led collective; concentrated at Tianwan CDZ
- **Aug 2027**: China has ~10% of world compute (OpenBrain: 20%; all US: 70%); almost entirely at CDZ; R&D multiplier 10x vs OpenBrain's 25x

## The Centralized Development Zone (CDZ)

Created mid-2026 at the Tianwan Power Plant (world's largest nuclear power plant):
- Largest centralized compute cluster in the world at its peak
- Air-gapped and hardened against cyberattacks after US retaliation attempts
- Houses researchers in secure living and office facilities
- Over 80% of China's new chips directed here

## Nationalization of Chinese AI Research

Triggered by CCP recognition that the AGI race could no longer be ignored:
- Initial information-sharing mechanism between AI companies
- Escalates over ~1 year to full merger of all top researchers into DeepCent-led collective
- Shared algorithmic insights, datasets, compute
- Researchers physically relocated to CDZ

## Key Events

| Date | Event |
|------|-------|
| Mid 2026 | CCP commits to major AI push; CDZ creation begins |
| Feb 2027 | Chinese intelligence steals Agent-2 weights from OpenBrain in ~2-hour operation |
| Feb–Mar 2027 | Retaliation cyberattacks from US fail against air-gapped CDZ |
| Aug 2027 | DeepCent running stolen Agent-2 weights; ~2 months behind OpenBrain; 10x multiplier |

## The Agent-2 Theft

A critical turning point in the scenario. Chinese intelligence had infiltrated OpenBrain for years; the weight theft involved:
- Insider with admin credentials (coerced or sympathetic)
- Microarchitectural side-channel to extract encryption keys from Nvidia Confidential Computing VMs
- ~25 servers leaking ~4% of the model each (~100 GB chunks of a ~2.5 TB checkpoint)
- Throttled to <1 GB/s per server to avoid traffic spikes
- Total operation: under 2 hours
- Exfiltrated through parallel channels with IP masking

DeepCent then post-trained the stolen Agent-2 weights rather than training from scratch.

## Strategic Dilemma

CCP faces a recurring dilemma throughout the scenario: act now (steal current model) or wait for a more advanced one, risking OpenBrain improving security beyond their penetration capability. They act when they judge the risk of waiting exceeds the value of a better future target.

Hawks within the CCP also discuss invasion of Taiwan (home of TSMC, source of >80% of US AI chips) as a way to eliminate America's hardware advantage — though this remains at the contingency planning stage through the end of the clipped source.

## Real-World Analog: DeepSeek

[[wiki/entities/deepseek|DeepSeek]] is DeepCent's real-world counterpart — a Chinese AI lab achieving frontier model performance. The comparison reveals a key divergence from AI 2027's assumptions:

| | DeepCent (AI 2027) | DeepSeek (real) |
|--|--|--|
| Strategy | State-directed, closed, espionage-assisted | Open publication, replicable recipes |
| Capability gap | Consistently 6 months behind OpenBrain | Competitive with GPT-4o/Claude 3.5 |
| Compute approach | Raw scale via CDZ concentration | Efficiency through MoE, MLA, co-design |
| Weights | Stolen (Agent-2 theft, Feb 2027) | Openly released |

The real trajectory suggests AI 2027 may underestimate open-source China's capacity to close gaps through published innovation rather than secrecy or theft.
