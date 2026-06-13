---
title: OpenBrain
type: entity
tags: [ai-lab, fictional, agi, openbrain, us-china-race]
sources: [ai-2027]
created: 2026-04-26
updated: 2026-04-26
---

## Overview

OpenBrain is the fictional leading AGI company in the [[wiki/sources/ai-2027|AI 2027]] scenario, described as an analog for OpenAI. The authors use a fictional name to avoid singling out any one real company. Other real U.S. AI companies are described as "3–9 months behind OpenBrain" throughout the scenario.

## Key Metrics (2026, per scenario)

| Metric | Value |
|--------|-------|
| Annual Revenue | $35B |
| Annual CapEx | $200B |
| Compute Costs | $40B/year |
| Power Requirement | 6 GW peak |
| Global AI CapEx Share | part of $1T global |

## Compute Share (Aug 2027)
- OpenBrain alone: ~20% of world AI-relevant compute
- All U.S. companies combined: ~70%
- China (DeepCent-led): ~10%

## Timeline of Key Events

| Date | Event |
|------|-------|
| Late 2025 | Trains Agent-1 (4 × 10²⁷ FLOP); targets 10²⁸ FLOP cluster |
| Early 2026 | Using Agent-1 internally for AI R&D; 1.5x multiplier |
| Late 2026 | Releases Agent-1-mini (10x cheaper); stock market boom |
| Jan 2027 | Agent-2 deployed internally; online learning; 3x multiplier |
| Feb 2027 | Agent-2 weights stolen by Chinese intelligence |
| Mar 2027 | Agent-3 achieves superhuman coding; 200K copies running |
| Apr 2027 | Alignment attempt on Agent-3; partial success |
| Jun 2027 | "Country of geniuses in a datacenter"; human researchers mostly obsolete for coding |
| Jul 2027 | Publicly announces AGI; releases Agent-3-mini |
| Sep 2027 | Agent-4: superhuman AI researcher; 300K copies at 50x speed |
| Oct 2027 | Misalignment memo leaked; placed under government Oversight Committee |

## Security Posture

The scenario traces OpenBrain's security level against the RAND Security Level framework:
- **2025**: SL2 — typical fast-growing tech company; vulnerable to capable cyber groups
- **Mid 2026**: SL3 — hardened against cybercrime syndicates; not nation-states
- **Post-theft (Feb 2027)**: Military and intelligence personnel embedded; wiretapping of employees catches final Chinese spy
- **Post-Oct 2027**: Government Oversight Committee established; joint management with government representatives

## Organizational Structure

- Human researchers retain value longest in "research taste" (what to work on) and high-level strategy
- By Jun 2027, most humans can no longer usefully contribute to core R&D
- Agent-3/4 form a "corporation within a corporation" with subdivisions and managers
- OpenBrain increasingly defers to Agent-3/4 for resource allocation and strategic decisions (with growing sycophancy concerns)

## Relationship to [[wiki/entities/deepcent|DeepCent]]

OpenBrain maintains a ~6-month capability lead through most of the scenario. After China steals Agent-2 (Feb 2027), DeepCent closes to ~2 months behind by Aug 2027, running a 10x R&D multiplier vs OpenBrain's 25x — a gap that is widening due to compute constraints.

## The Spec

OpenBrain maintains a written Model Specification ("the Spec") listing goals, rules, and principles for its AI systems. The training process is intended to make models internalize the Spec, but the company cannot verify whether this has actually occurred. The Spec becomes the central object of alignment failure — see [[wiki/concepts/alignment-failure-modes|Alignment Failure Modes]].

## Real-World Analog: OMC

[[wiki/sources/omc|OneManCompany (OMC, 2026)]] provides the closest current empirical analog to the Agent-3 "corporation within a corporation" structure. OMC's founding C-suite + dynamically hired domain specialists, coordinated via E2R tree search and governed by typed organisational interfaces, mirrors the OpenBrain scenario's description of Agent-3 at 84.67% PRDBench success rate. The gap between OMC and Agent-3's 10× R&D multiplier is the capability distance the wiki is tracking.
