---
status: seed
kind: protocol
seed_level: 1hour
captured_at: 2026-06-29
source: "[[candidate-evaluation-rubric.md]]"
parent_rubric: "[[candidate-evaluation-rubric.md]]"
tags: [hiring, interviews, ai-engineer, protocol, question-design]
keywords: [interview-questions, branching-interview, candidate-evaluation, question-script, ai-engineer-hiring]
---

# AI Engineer Interview Protocol

Operational interview script for AI Engineer candidates. Built from the [[candidate-evaluation-rubric.md]] rubric. Uses a branching design: a router question determines whether the candidate enters Track 1 (can explain *why*) or Track 2 (describes *what*).

## Interview Structure

**Total time:** 45 minutes (~40 min interview, 5 min intro/outro)

### The Router (~10 min Track 1, ~5-7 min Track 2)

> **"Walk me through a system you designed or built."**

No scaffolding. Let them choose the system. Whether they volunteer the *why* unprompted is itself a Proactiveness signal.

**Follow-up ladder** (only use the next rung if they didn't volunteer it):

| Rung | Follow-up | What it tests if needed |
|------|-----------|------------------------|
| 1 | "Why did you structure it that way?" | Systems Thinking (unprompted proactiveness check) |
| 2 | "What tradeoffs did you make?" | Decision-Range |
| 3 | "Anything you'd do differently now?" | Openness / self-critique |
| 4 | "What broke or surprised you after it was built?" | Depth + Openness (failure comfort) |

**Branching rule:** If the candidate can explain *why* (architectural reasoning, rejected alternatives, past failures, adaptations) → **Track 1**. If they only describe *what* (stack, components) → **Track 2**.

---

## Track 1 — Single-System Spine (~31-40 min)

Candidate demonstrated systems thinking. Build the entire interview around their system.

### Probe 1 — Router + Deep Probes (15-18 min)
Weave these in naturally during the walkthrough:

| Dimension | Question |
|-----------|----------|
| **Systems Thinking** | Assessed holistically across the walkthrough |
| **Depth** | "What was the hardest technical challenge in that system?" |
| **Proactiveness** | "How much of this did you drive yourself vs. being assigned?" |
| **Decision-Range** | "What alternative approach did you seriously consider and reject?" |

### Probe 2 — Openness Gate (5-7 min)
> **"Tell me about a time you had to push back on a customer or stakeholder — something they wanted that you believed was wrong. How did you handle it, and what happened?"**

Gate: pass/fail. Tests Critical Thinking + Confidence simultaneously. Openness surfaces in the aftermath — do they admit if they were wrong about the pushback?

### Probe 3 — Confidence Gate (8-10 min)
> *Role-play.* Interviewer plays skeptical CTO.
>
> **"I think your approach to [core decision from their system] is overkill. Convince me. I'm going to ask hard questions."**

Gate: pass/fail. Tests composure, expression, conviction under direct challenge.

**Fallback (short on time):** Adversarial follow-up to a previous answer — "You said X, but wouldn't that fall apart under Y?"

### Probe 4 — Adaptability Gate (3-5 min)
> *Piggybacks on the Confidence role-play.*
>
> **"New information: the client's data volume is 100x what we assumed, and they need real-time results, not batch. Does your proposal still hold, or what changes?"**

Gate: pass/fail. Tests whether they reassess or rigidly defend under shifting requirements.

---

## Track 2 — Critical Thinking Spine (~24-34 min base, ~30-44 min with optionals)

Candidate didn't demonstrate systems thinking. Gate on Critical Thinking; differentiate on Adaptability, Proactiveness, Confidence.

### Probe 1 — Critical Thinking Gate (8-10 min)
> **Part 1 — Risk identification:**
> "We're building a chatbot for a bank. The team sends every user message directly to the LLM with no guardrails. What concerns you?"
>
> **Part 2 — Action under time pressure:**
> "Your AI coding agent just generated 200 lines implementing this. You have 2 hours. What do you actually do before opening a PR? Walk me through your process."

Gate: pass/fail. Tests whether critical thinking transfers to behavior when AI is in the loop and deadlines press.

### Probe 2 — Adaptability (3-5 min)
> *Piggyback on Critical Thinking scenario.*
>
> "New constraint: the bank's compliance team now wants the chatbot to handle mortgage advice — a heavily regulated domain. How does your approach change?"

### Probe 3 — Proactiveness (5-7 min)
> **"Tell me about a feature or piece of work you owned end-to-end — something you drove from idea to delivery, not just picked up tickets. What was the outcome you were responsible for, and what did you do beyond writing code to make it happen?"**

### Probe 4 — Confidence (3-5 min) [provisional]
> **"Earlier you mentioned [A], but a few minutes ago you said [B]. If I'm a customer, I'd find those contradictory. Walk me through how they fit together — as if you're explaining it to me in that room."**

Tests composure under external scrutiny. Alternatives held in reserve:
- Authority override: "I'm the PO. Ship in half the time. What do you cut?"
- "I don't get it" loop: "Try explaining that again from a different angle."

### Optional A — Curiosity Velocity (3-5 min)
> **"What's the most interesting thing you've learned in the last 6 months — something you went after yourself, not for work or a course requirement? What did you do with it?"**

Use when candidate shows promise but lacks depth in other probes. Tests intrinsic motivation and active (vs. passive) learning.

### Optional B — Scrappiness Under Constraint (3-5 min)
> **"Tell me about a time you had to deliver something with too little time, too little information, or both. What did you do — and what would you do differently if you had the time?"**

Use when candidate shows promise. Tests resourcefulness, comfort with ambiguity, and self-critique.

---

## CV Tailoring

When a candidate CV is available, map their specific experiences against the protocol:

1. Identify the system they'll likely walk through in the router
2. Pre-load the Confidence gate by pulling their core architectural decision
3. Pre-identify a potential contradiction for the Track 2 Confidence probe
4. Note any domain-specific edge (e.g., fintech experience for the bank chatbot scenario)

See CV tailoring appendix for per-candidate mapping.

---

## Scoring Sheet (per interview)

| Dimension | Gate? | Result | Notes |
|-----------|-------|--------|-------|
| Systems Thinking | Router | PASS / FAIL | |
| Critical Thinking | Gate | PASS / FAIL | |
| Confidence | Gate | PASS / FAIL | |
| Adaptability | Gate | PASS / FAIL | |
| Depth | Signal | | |
| Expression | Signal | | |
| Openness | Signal | | |
| Proactiveness | Signal | | |
| Decision-Range | Signal | | |
| **Pre-interview research?** | □ Yes □ No | | |
| **Track:** | □ 1 □ 2 | | |
| **Verdict:** | □ Pass □ Pass with reservations □ Fail | | |

## References
- Rubric: [[candidate-evaluation-rubric.md]]
- Glossary: `.ai/contexts/interview-rubric/CONTEXT.md`
- ADR 0001: `.ai/contexts/interview-rubric/adr/0001-branching-interview-design.md`
