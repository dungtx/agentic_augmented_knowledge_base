---
status: seed
kind: framework
seed_level: 1hour
captured_at: 2026-06-26T17:50:43+07:00
seeded_at: 2026-06-29T09:45:00+07:00
refined_at: 2026-06-29
source: "[[../11a.Capture/11a1.Inbox/_processed/202606261750-ai-engineer-candidate-rubric.md]]"
sprout_of: "[[candidate-evaluation-rubric.md]]"
sibling: "[[ai-engineer-interview-protocol.md]]"
tags: [hiring, interviews, evaluation, rubric]
keywords: [candidate-evaluation, systems-thinking, interview-rubric, scoring-guide, dimensions]
---

# Candidate Evaluation Rubric

A structured framework for evaluating engineering candidates beyond technical correctness. Focused on *how they think*, not just what they know. Reusable across roles and hiring rounds.

## Dimensions

| # | Dimension | Core signal |
|---|-----------|-------------|
| 1 | **Systems Thinking** | Breadth + foresight. Sees the whole, identifies seams, anticipates edge cases and failure modes before anything is built. |
| 2 | **Critical Thinking** | Skepticism + pushback. Doesn't accept designs or AI output at face value. Identifies what "feels wrong" and articulates why. |
| 3 | **Depth** | Persistence + self-awareness. Can sit with a hard problem for an extended time, but knows when to ask for help. |
| 4 | **Expression** | Articulates reasoning clearly, verbally and in text. Not charisma — clarity. |
| 5 | **Adaptability** | Reactive flexibility. Adjusts approach when the ground shifts (new stack, new requirements, changed scope). |
| 6 | **Openness** | Curiosity about new ideas, admits mistakes and learns from them. Growth-mindset. Includes self-critique. |
| 7 | **Confidence** | Composure under pressure. Has a floor (not rattled) and a ceiling (presence / commanding the room). |
| 8 | **Proactiveness** | Self-starting initiative — drives things nobody assigned, including pre-interview research as a cheap early indicator. |
| 9 | **Decision-Range** | Considers multiple technical options with pros/cons before committing. Doesn't default to the known tool. |

## Priority Split

How the dimensions weigh for Dzung (hiring manager) vs. the company.

| # | Dimension | Dzung | Company |
|---|-----------|-------|---------|
| 1 | Systems Thinking | **High** — rare, hard to learn, invaluable in offshore context | Low — cost-driven hiring |
| 2 | Critical Thinking | **Non-negotiable** — core to LLM guardrails work | Latent need — would feel the absence |
| 3 | Depth | Nice-to-have | Low — prefers breadth over depth |
| 4 | Expression | Nice-to-have | Low — LLM-assisted comms |
| 5 | Adaptability | **Mandatory** | **Mandatory** |
| 6 | Openness | **High** — needed to stay competitive, improve | Conditional — stops at face-cost |
| 7 | Confidence | **Mandatory floor** (composure), bonus ceiling (presence) | **Aligned** — key to passing client interviews |
| 8 | Proactiveness | **High** — on-job initiative > interview prep | Implied through Preparedness indicator |
| 9 | Decision-Range | Cherry-on-top — not expected at hiring level | Not valued |

## Scoring Method

Hybrid — different layers use different formats:

| Layer | Format | Dimensions |
|-------|--------|------------|
| **Hard Gates** | Binary (pass/fail) | Critical Thinking, Confidence (floor), Adaptability |
| **Router** | Binary (pass/fail) | Systems Thinking — "can they explain *why*?" |
| **Signal-Collect** | Narrative (2-3 bullet observations) | Depth, Expression, Openness, Proactiveness, Decision-Range |

If a candidate fails any hard gate, they're rejected regardless of other strengths. Signal-collect dimensions differentiate between candidates who pass all gates.

## Glossary & Decisions

- Domain glossary: `.ai/contexts/interview-rubric/CONTEXT.md`
- ADRs: `.ai/contexts/interview-rubric/adr/`

## Relationship to Interview Protocol

This rubric defines *what* to evaluate. The interview protocol (`[[ai-engineer-interview-protocol.md]]`) defines *how* — the questions, branching logic, and time budget for a specific role.
