# Prompt Engineering — Process & Lessons

Distilled from reading a real production prompt engine end-to-end: kcc-platform's Implementation-Map
prompt catalogue (35 `PromptDef`s driving Requirement-Engineering + Vibe-Implementation across a
delivery platform). Concrete sources cited inline; the lessons themselves are meant to generalize past
this one codebase.

Companion notes: [[swe-concepts-for-agent-prompts|SWE Concepts for Agent Prompts]] (what a prompt should
contain) and [[ai-product-architecture-patterns|AI-Product Architecture Patterns]] (the system design one
level up from the prompt text).

Case-study files:
- `packages/shared-types/src/prompts.ts` — the prompt catalogue (data, not scattered strings)
- `apps/api/src/modules/app/prompt.service.ts` — `resolve()` (grounding) + `render()` (templating)
- `apps/api/src/modules/app/context.service.ts` — the connected-knowledge assembler
- `packages/ai/src/gateway.ts` — the single egress point to the model

## The process (a pipeline for building a *prompt engine*, not a single prompt)

1. **Define prompts as data, not scattered strings.** One `PromptDef[]` catalogue (code, role, phase,
   process steps, output shape, which UI rows expose it) beats 35 hand-written prompt strings sprinkled
   through the codebase — one render function, one place to fix a systemic issue, diffable in review.
2. **Separate grounding from templating.** `resolve()` (fetch + assemble context) and `render()` (turn
   context + `PromptDef` into text) are different concerns with different failure modes — don't fuse them.
3. **Prefer distilled knowledge over raw source dumps.** Feed the model pre-extracted, structured facts
   (KCC artifacts) instead of re-parsing/re-sending raw RFP/Proposal/WBS text on every call. Cheaper,
   more focused, and keeps confidential source material out of the hot path.
4. **Use graph-aware retrieval when the knowledge has structure.** Flat top-K RAG returns disconnected
   fragments. `ContextService.assemble()`'s Tier-2 (semantic anchor → N-hop adjacency expansion) keeps
   the *relationships* between concepts, not just the concepts — genuinely better than naive chunking
   when the underlying knowledge is a graph (concepts + relations + known gaps).
5. **Sandwich the instruction around long context — don't state it once at the tail.** This engine's
   `render()` puts a 24-48k char knowledge block *before* the PROCESS/task instruction. On long items
   this is a known attention risk (the ask gets buried). Put the instruction before the context AND
   repeat it after, especially as context length approaches the budget ceiling.
6. **Isolate hard constraints into their own unmissable block.** "Never invent, mark unknowns TBD" was
   found sharing a sentence with unrelated governance metadata ("Phase B · AI proposes, human owns
   gate") at the very end of a long prompt. Anti-hallucination / safety constraints need their own
   labeled section, and arguably a mention in the system message too — don't let them compete for
   attention with procedural trivia.
7. **Make OUTPUT a contract, not a hint, whenever something downstream parses it.** `## Gaps (type ·
   description · affected REQ · resolution)` names the columns but not the grammar (delimiter, one entry
   per line vs. per paragraph, how to represent "none found"). Worked once because the model was good,
   not because the spec forced it. If a human is the only reader, a loose skeleton is fine; if anything
   re-parses the text, give a schema or a literal worked example.
8. **Let task risk decide "run automatically" vs. "copy to a human-owned surface."** This engine's
   `defaultMode: 'run' | 'copy'` per prompt is a good instinct: Phase A/B (analysis, drafting) runs
   in-platform; Phase C (actual code changes) defaults to copy-into-IDE, keeping the highest-blast-radius
   step under direct human control rather than auto-applying it.
9. **Give an explicit escape hatch for "I don't know," not just a prohibition on guessing.** "Never
   invent" is half an instruction — pair it with a concrete legal way out (mark `TBD`, emit
   `[NEEDS CLARIFICATION]`, ask a question) so the model has somewhere to put genuine uncertainty instead
   of quietly filling the gap.
10. **Tag every call for attribution from day one.** Cost/trace tags (`tags: { prompt: code }`) are cheap
    to add at the call site and expensive to retrofit once a budget/alerting feature depends on them
    existing from day one. If the product promises per-project budget alerts, the attribution tag needs
    the project id in it *before* that promise ships, not after.

## Prompt ideas worth stealing (concrete patterns observed here)

- **The small-menu copilot pattern.** Rather than one do-everything prompt, expose a fixed set of cheap,
  sharp, single-purpose actions on every item (`Validate` / `Suggest` / `Gaps & Conflicts` / `Red Team` /
  `Coach` / `Ask`). Each one has a narrow, obvious job — easier to get each one right, and the user picks
  the tool instead of hoping one mega-prompt reads their mind.
- **A dedicated adversarial pass, separate from generation.** `P15 Red Team` and `VP-REDTEAM` exist as
  their *own* prompts, not a "please double-check yourself" clause tacked onto the generation prompt. A
  fresh, adversarially-framed pass catches more than self-review folded into the same breath as creation.
- **Bidirectional coverage checking.** `C2b Gap Collector` checks forward (every AC has a test) *and*
  backward (every file traces to a REQ-id, else scope drift) — catches under-build and over-build with
  one prompt, rather than only checking that requirements were satisfied.
- **A required, structured self-reported diff.** Every Vibe-Implementation prompt appends a mandatory
  postscript: write `.vnx/trace/{REQ-id}.md` with Created/Modified/Deleted sections after all changes.
  This turns "trust me, I made these changes" into a parseable, reviewable artifact the platform can sync
  back into its own map — cheap to ask for, high leverage for traceability.
- **One identifier threaded through everything.** The REQ-id runs through branch name, commit message,
  test titles, and the trace file. Pick one id per unit of work and insist every artifact type carries it
  — traceability becomes mechanical (greppable) instead of a manual reconciliation exercise later.
- **One canonical requirement-shape reused by every role.** EARS-format acceptance criteria are produced
  by BA prompts and consumed unchanged by Dev/QA prompts. Define the shape once; don't let each role
  invent its own version of "what a requirement looks like."

## Failure modes actually observed, generalized

- **Upstream machine-generated content silently carries bugs into every downstream prompt.** A draft
  backlog generated by an earlier AI step produced a templating artifact ("...so that the chat interface
  workflow is fulfilled" duplicated the word "user" in an AC). The downstream Risk/Gap Hunt prompt caught
  it — but only because the model happened to notice, not because anything instructed it to sanity-check
  upstream content for placeholder/broken text. If one prompt's output feeds another prompt's input,
  explicitly ask the consuming prompt to flag suspicious/templated text as a first-class finding.
- **Model competence quietly compensates for an underspecified prompt — don't rely on that.** The
  Risk/Gap Hunt output was genuinely good despite the OUTPUT line being a loose hint rather than a
  contract. That the model bailed out a weak spec is not evidence the spec is fine; it's evidence to
  tighten the spec anyway, because the next model (or the same model on a harder case) won't always do
  the work the prompt should have specified.
- **Sibling prompts in the same family drift into different taxonomies for conceptually identical
  things.** `VP-VALIDATE` classifies issues as Critical/High/Medium; `B5a Risk / Gap Hunt` classifies them
  as missing/conflict/edge-case/implied-NFR. Both are "how bad is this problem" schemes for closely
  related tasks, but they don't share a vocabulary. Define one taxonomy per concept family and reference
  it from every prompt that touches that concept — don't let each prompt author invent their own labels.
