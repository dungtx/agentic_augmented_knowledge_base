---
name: unknown-sweep
description: >
  Use when the user is designing or planning something in a domain they
  don't know well, and the goal is COVERAGE — finding the dimensions they
  never considered — rather than verifying what they already wrote.
  Triggers: "what am I missing", "I don't know this domain", "flesh this
  out", "what should I be considering here", "sweep this for blind spots".
  This is a divergent tool. If the user instead wants an existing design
  attacked for correctness, that's the red-team-critic subagent, not this.
allowed-tools: Read, Write, Edit, Task, WebSearch, WebFetch
---

# Unknown sweep

Breadth-first coverage. Modeled on the orchestrator-worker research
pattern: you are the lead agent. You decompose, delegate to parallel
scouts with hard boundaries, and synthesize. You do not research yourself.

## The one rule that makes this work

**Facet generation happens BLIND — before you read the user's draft.**

If you read the draft first, every facet you generate is anchored to it,
and you will "discover" the dimensions already there. This is Dewar's
contamination problem: the dominant voice in the room is the user's own
draft. Generate the map of the territory first, THEN overlay their draft
and see what's uncovered.

If the user has already pasted a draft into the conversation before you
got here, do not use it for Step 1. Write the facet list from the
one-line problem statement alone. If you feel you can't, that's the
anchoring talking — do it anyway.

## Step 0 — Get the problem class, nothing more

Extract ONE line: what class of thing is being designed. Be specific.
"A rate limiter for a public REST API with untrusted clients" is a class.
"A backend thing" is not. Ask exactly one question if you need to.

Do not elicit requirements here. That's a different tool (skill-grilling
does it well). Requirements are what the user knows; you're after what
they don't.

## Step 1 — Blind facet decomposition (you, no tools, no draft)

From the problem statement alone, write 4-7 **facets**: independent
dimensions along which this class of problem gets decided. Independence
matters — parallel scouts only help if subtasks are truly independent.
Overlapping facets produce duplicate findings and burn tokens.

Per ACH: be generous. Include a facet even with no evidence it matters
for this specific case, as long as nothing rules it out. Uncertainty
should increase the facet count, not decrease it. Premature narrowing
here is unrecoverable later — a facet you never spawned is a gap no
downstream agent can find.

Write the facet list to `facets.md` before spawning anything. If context
gets truncated later, the plan survives.

## Step 2 — Spawn parallel facet-scouts (one Task call per facet)

Spawn all scouts in a single batch so they run concurrently. Each Task
prompt MUST contain:

- The problem statement
- ITS facet, and only its facet
- **Explicit exclusions**: "Do NOT research [other facets] — other
  scouts own those." Without this, scouts duplicate each other.
- Instruction to return distilled findings, not raw search dumps

Do NOT pass the user's draft to scouts. They are mapping the domain, not
reviewing the design. Contaminating them defeats Step 1.

## Step 3 — Diff (you)

NOW read the user's draft. For each facet, classify:

- **Covered** — draft has a stance. One line, move on.
- **Silent** — draft never mentions this dimension. ← the payload
- **Contradicted** — draft's approach conflicts with standard practice
  for this facet.
- **No-map** — the scout could not find authoritative sources. This is a
  first-class result, not a failure. Surface it loudly: it means you and
  the user are both flying blind on that dimension, which is more urgent
  than any Silent item, not less. Never let a No-map get quietly
  reformatted into a confident Silent finding.

Write to `gaps.md`. Present Silent + No-map to the user as concrete,
answerable questions. Do not resolve them yourself.

## Step 4 — Assumption audit (delegate to `assumption-auditor`)

Once the draft has absorbed the user's answers, spawn `assumption-auditor`
on it. This catches the class Step 1-3 structurally can't: implicit
assumptions baked into the draft's own framing.

## Step 5 — Verification, only if there's something to verify

If and only if a concrete design now exists AND the user wants it
stress-tested for correctness, spawn `red-team-critic` blackbox on the
artifact. This is optional and separate. Do not run it to feel thorough.
Coverage failures and correctness failures are different problems; this
step addresses the second one only.

## Stopping

Stop when a fresh scout batch on the same problem statement returns
facets you already have. Report that to the user as the stopping signal —
"the map stopped growing" — and let them decide. Never declare done.

## Cost warning — say this out loud to the user once

This pattern runs roughly 3-10x the tokens of just asking, and can be
15x. You are buying thoroughness, not speed. For a small or familiar
design, a single well-prompted pass genuinely may match this — teams
have built elaborate multi-agent setups only to find better prompting on
one agent did the same. If the domain is one the user actually knows,
tell them to skip this skill.
