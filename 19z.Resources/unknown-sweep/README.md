# unknown-sweep kit (v2)

Coverage-first. Replaces the deep-grill kit, which was built on the wrong
shape.

## What changed from v1, and why

| v1 | v2 | Reason |
|---|---|---|
| Serial elicit → scout → critique | Blind decompose → **parallel** scouts → diff | v1 was problem-centric decomposition (planner/implementer/reviewer). Anthropic tested that exact split and the subagents spent more tokens coordinating than working. "Independent research paths" is a *good* boundary; sequential phases of the same work is a *bad* one. |
| One scout, sequential | N scouts, parallel, hard exclusions in each prompt | Coverage is breadth-first search. Anthropic's Research feature found subagents duplicate each other without explicit "don't research X, that's another subagent's job" boundaries. |
| Scout reads the draft first | Scout **never** sees the draft; facets generated blind, then diffed | Dewar's contamination problem — the draft is the dominant voice in the room. v1's scout was anchored by the thing it was supposed to find gaps in. |
| Scout must return findings | **NO-MAP** is a valid terminal answer; sources tiered T1/T2/T3 | v1's biggest hole: it failed silently in exactly the domains you needed it for, and a listicle counted as a citation. |
| Critic told to always find something | Fabrication pressure removed; "couldn't break it" is valid; early-victory checklist instead | v1 literally instructed the critic to treat zero findings as its own failure. That's a fabrication engine you can't audit. |
| Critic was the centerpiece | Critic demoted to optional step 5; **assumption-auditor** added | Red-teaming is convergent — it can't find what isn't written down. Your problem is divergent. |
| No turn limits, unbounded loop | `maxTurns` on every agent, stop signal = map stops growing | v1 didn't terminate. |

## Install

```
.claude/
  skills/unknown-sweep/SKILL.md
  agents/facet-scout.md
  agents/assumption-auditor.md
  agents/red-team-critic.md
```

Project-level as above, or `~/.claude/` for every project. Claude Code
picks up new agent files within seconds; restart once if you're creating
the first file in a brand-new `agents/` directory mid-session.

## Use

> "I'm designing a rate limiter for a public API. Sweep it for unknowns."

Sweep first, draft second, audit third, critic last and only if you want
it. Running the critic on a design that hasn't been swept just gives you
a confident review of a design with a hole in it.

## Where each tool actually belongs

- **skill-grilling** — extracts your explicit knowns. Fast, keep it.
- **unknown-sweep** — divergent. Finds dimensions you never had.
- **assumption-auditor** — finds what your draft assumes without saying.
  Per Dewar this is the highest-yield step, because explicit assumptions
  are usually not the important ones.
- **red-team-critic** — convergent. Attacks what's written. Last.

## What this still doesn't fix

**Correlated blind spots.** Every agent here is the same base model. If
Claude has a systematic misconception about your domain, all four scouts
share it, and running them in parallel gives you four confident copies of
the same error, not four independent checks. Parallelism buys search
breadth; it does not buy epistemic independence.

**Structure isn't rigor.** Fifty trained intelligence analysts given ACH
didn't actually follow all its steps. An LLM has the opposite failure: it
will follow the steps *perfectly* and hand you a beautifully-formatted
matrix that's structurally identical to the Iraq WMD failure mode — where
uncertainty got assessed at each separate stage rather than across the
whole chain of reasoning. A clean-looking sweep is not a cleared sweep.

**The real fix is still out-of-band.** One conversation with someone who
has built this thing beats every agent in this kit. Use the sweep to
figure out *what to ask them* — that's a genuinely good use of it, and
arguably the best one. Treat NO-MAP results as your interview agenda.

## Sources worth reading directly

- Anthropic, *Building multi-agent systems: When and how to use them* —
  the decomposition guidance this kit is built on
- Anthropic, *How we built our multi-agent research system* — the
  orchestrator-worker pattern being copied here
- Dewar, *Assumption-Based Planning* (RAND, 2002) — load-bearing +
  vulnerable assumptions
- Heuer, *Psychology of Intelligence Analysis* (CIA, 1999) — ACH; free
  online
- Dhami et al. (2019), *Applied Cognitive Psychology* — the empirical
  critique of ACH; read this one alongside Heuer, not after
