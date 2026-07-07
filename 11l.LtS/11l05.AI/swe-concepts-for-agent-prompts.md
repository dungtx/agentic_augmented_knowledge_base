# Software-Development Concepts to Embed in Agent Prompts

A practical checklist: the ingredients a prompt for a coding/delivery agent needs to carry to get
correct, safe, gate-able work — not generic prompting advice, specifically the *software-engineering*
content a prompt should encode. Companion to [[prompt-engineering-process-lessons|Prompt Engineering —
Process & Lessons]] and [[ai-product-architecture-patterns|AI-Product Architecture Patterns]]; all three
distilled from the same case study (kcc-platform's Implementation-Map prompt engine).

## A. Scope & boundaries

- **State which files/modules may be touched.** kcc-platform's "mapped files" concept (the story's
  artifact slots) is the model of this — don't let an implementation prompt roam the whole repo when the
  task only concerns three files.
- **State what NOT to do, explicitly.** An unscoped "implement this" invites scope creep (extra
  abstractions, unrequested refactors, speculative future-proofing). Say what's out of bounds, not just
  what's in.
- **Encode architecture/module-boundary rules the CI already enforces.** If the codebase has a rule like
  "modules/* → core/*|common/* only, core/* ↛ modules/*", state it in the prompt — don't make the agent
  discover it by failing a lint/CI gate after the fact.
- **Name the existing conventions to follow** (naming style, formatter, lint config, commit format)
  instead of leaving the agent to infer or reinvent them per task.

## B. Requirements & acceptance

- **Thread one stable identifier through every artifact.** REQ-id / ticket-id in the branch name, commit
  message, test titles, and any trace/change-log file. Traceability should be greppable, not something
  reconstructed manually later.
- **Give acceptance criteria in a testable, unambiguous shape**, not vague prose. EARS
  ("the system shall...") or an equivalent fixed grammar — a prompt that hands over "the system shall
  allow the user to use the feature" (a tautology) produces exactly the tautological, unimplementable
  output you'd expect. Garbage-in, garbage-out applies to AC quality as much as to code.
- **State which test types are required and require each AC map to at least one test.** Don't assume
  "write tests" implies coverage of every acceptance criterion — say so, and ask for the mapping
  explicitly (AC → test) so a reviewer can check it mechanically.
- **Call out non-functional requirements explicitly** — perf targets, security constraints, compliance
  frameworks, data sensitivity. NFRs are the first thing silently dropped when a prompt only states
  functional behavior; they don't show up unless someone asks for them by name.

## C. Grounding & truthfulness

- **State a source-of-truth hierarchy for when inputs conflict** (e.g. client docs > project brief >
  inferred assumption). Without an explicit precedence, the agent picks one arbitrarily and you won't
  know which it picked until the output is wrong in a specific way.
- **Pair "never invent" with a concrete escape hatch.** Prohibiting guessing is only half the
  instruction — give the agent somewhere legal to put genuine uncertainty (mark `TBD`, emit
  `[NEEDS CLARIFICATION]`, ask a clarifying question) instead of it quietly filling the gap with a
  plausible-sounding guess.
- **Don't imply access to material the agent doesn't actually have.** If a prompt lists "reference
  documents" but only passes their titles, don't call them "the source of truth to read" — that phrasing
  oversells what the agent can act on and invites false confidence in citations it can't actually check.
- **If upstream content was machine-generated, say so and ask for a sanity check.** Auto-generated
  backlogs/specs can carry templating bugs (placeholder text, duplicated words, broken interpolation)
  into every downstream prompt that trusts them at face value. Ask the consuming prompt to flag anything
  that looks like unresolved template output as a first-class finding, not just work around it silently.

## D. Output contract

- **Give a schema, not a hint, when anything downstream parses the output.** A markdown heading naming
  the columns is not a grammar — specify the exact delimiter/structure, or provide a literal worked
  example, whenever a parser (not just a human) will consume the result.
- **Give a structural skeleton even for human-read output** — required sections, consistent ordering —
  so review is fast and consistent across many outputs of the same prompt type.
- **Require a self-contained change report as part of the output for any code-modifying task**: files
  created / modified / deleted, one line each. Converts "trust me, I made these changes" into a
  reviewable, greppable artifact instead of requiring the reviewer to diff the whole tree to find out
  what happened.

## E. Safety & reversibility

- **Flag high-blast-radius or hard-to-reverse actions and require explicit sign-off before they're
  taken** (plan-then-apply / human gate). Default risky operations to *proposed*, not *applied*.
- **State the rule for ambiguous or destructive state**: investigate before overwriting/deleting; never
  silently discard unfamiliar in-progress work (uncommitted changes, unknown branches, existing files).
- **Name security-sensitive surfaces explicitly** (auth, input validation, injection risk, secrets
  handling) rather than trusting the agent to remember to think about them unprompted — the same way a
  human reviewer's checklist calls these out by name instead of hoping the author considers them.

## F. Process & verification

- **Build in a dedicated adversarial/verification pass, separate from the generation step.** A
  "review your own output" clause appended to the same prompt that generated the output is a weaker
  check than a fresh pass framed adversarially (red-team it, try to break it, argue it should NOT ship).
- **Require bidirectional coverage checks where they apply**: every requirement has an implementation
  *and* every implementation traces back to a requirement. Checking only one direction misses either
  under-build (missing requirements) or over-build (undocumented scope creep), not both.
- **Keep verification prompts and generation prompts as separate steps**, even when the same model runs
  both — the framing (build vs. attack) matters more than which model is doing it.

## G. Consistency across a prompt family

- **Define shared vocabulary once and reference it everywhere** — severity levels, status labels,
  artifact-type names, taxonomy for "what kind of problem is this." Two prompts in the same family
  independently inventing different scales for the same concept (e.g. Critical/High/Medium vs.
  missing/conflict/edge-case/implied-NFR) makes their outputs impossible to aggregate or compare later.
- **Reuse one grounding/context-assembly strategy across the whole family** of prompts operating on
  related work, so every role reasons over the same substrate instead of each prompt re-deriving its own
  partial view of the same project.
