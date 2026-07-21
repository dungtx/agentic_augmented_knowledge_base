---
status: triaged
kind: idea
captured_at: 2026-07-17T16:12:00+07:00
tags: []
needs_review: false
triaged_at: 2026-07-21T11:44:49+07:00
triaged_to: "[[../../11c.Projects/AI-Delivery-Pipeline/README.md]]"
---

AI research agenda — multiple threads to explore:

## 1. Prompt chaining vs. context-up-front

Comparing two approaches: **prompt chaining / conversation using Harness** vs. **providing full context up front with defined instructions**. Which leads to better outcomes, and under what conditions?

## 2. Human gates for AI

Where should human verification gates sit in an AI workflow? How to verify AI results honestly — not just rubber-stamping generated output? How to stop the human apathy that sets in when reading generated text (the "looks good enough" effect)?

## 3. AI-first vs. human-first

What does it mean to be AI-first vs. human-first in a workflow? What would AI-first mean for the human — their role, their skills, their value?

## 4. AI pain points across the SDLC (ITO context)

Biggest pain points at each SDLC phase, and what AI can help with. Example: **discovery phase** lacks domain knowledge to ask correct questions. Map intents and counter-arguments for each.

Phases to cover: discovery, requirements, design, implementation, testing, deployment, operations, maintenance.

## Existing research (merged from prompting-techniques note)

Preliminary findings on context engineering and harness engineering, sourced from Anthropic, OpenAI, Martin Fowler, GitHub Spec Kit, Kiro Specs, BMAD Method, HumanLayer ACE, and academic papers. Key conclusion: not a library of large SDLC prompts, but a **context compiler** that constructs a different context packet per phase/task.

### Context model (4 layers)
- **Layer 1 — Project constitution:** non-negotiable principles, security boundaries, tech constraints, canonical commands
- **Layer 2 — Repository map:** navigational index (where docs/tests/schemas live), not a full description
- **Layer 3 — SDLC phase packet:** per-phase provide/require pairs (discovery → requirements → architecture → planning → implementation → review → operations)
- **Layer 4 — Task context + runtime feedback:** one unit of work, tests/logs/screenshots as verification

### Key practices
- **Progressive disclosure** over giant prompts (OpenAI, Anthropic both recommend)
- **Phase separation:** research → plan → implement, with context resets and handoff artifacts between phases
- **Spec artifacts as context pipeline:** GitHub Spec Kit (Spec → Plan → Tasks → Implement), Kiro Specs (EARS-style testable requirements), BMAD Method (4 phases, depth by task size)
- **Verification in the prompt environment:** every phase specifies not just output but how it will be evaluated
- **Warning:** more context can reduce performance (ETH Zurich, June 2026 — context files increased cost 20%+, broad overviews unhelpful)

### Sources to revisit
Anthropic context engineering, OpenAI harness engineering, GitHub Spec Kit, BMAD Method, Kiro Specs, HumanLayer ACE, 2026 AGENTS.md studies.

See archived note `202607061358-prompting-techniques-context-drift.md` for full source list and citations.
