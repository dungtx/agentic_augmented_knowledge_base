# AI-Product Architecture — Patterns Beyond the Prompt Text

Third note from the same case study (kcc-platform's Implementation-Map prompt engine). The other two —
[[prompt-engineering-process-lessons|Prompt Engineering — Process & Lessons]] and
[[swe-concepts-for-agent-prompts|SWE Concepts for Agent Prompts]] — are about the prompt itself. This one
is about the *system design decisions* around the prompt: how the platform is built so that good prompts
are even possible, observed one level up from the text that gets sent to the model.

## Single-egress gateway, enforced structurally, not just by convention

Every model call in kcc-platform routes through one `@vnx/ai` gateway client; a lint rule (VNX-014)
*bans* direct provider-SDK imports anywhere else in the codebase. This is the same "encode the rule in
CI/lint, not just in a prompt or a doc" idea from the SWE-concepts note, applied one level up — to the
platform's own architecture rather than to a single task. **Lesson:** anything that must always be true
(cost governance, audit trail, a security invariant) should be a static-analysis failure if violated, not
a hope that every future prompt/dev remembers the rule.

## Provider routing designed at the gateway boundary, even with one provider live today

`gateway.ts` reads `AI_PROVIDER_SORT` / `AI_PROVIDER_ORDER` env vars to build an OpenRouter routing
object, applied uniformly inside `complete()` rather than at each call site. **Lesson:** put the
provider-selection knob at the boundary where all calls already funnel through, so switching providers,
adding a fallback chain, or A/B-ing models later is a config change, not a refactor touching every caller.

## Correlation IDs persisted next to every AI-generated artifact

Every `gateway.complete()` call returns a `traceId` (pulled from a response header or the provider's own
id), and the caller stores it (`aiTraceId`) alongside the record the call produced. **Lesson:** never let
an AI-generated artifact exist in your database without a pointer back to the exact call that produced
it. It's a single extra column, and it's the difference between "we can pull the exact provider-side
trace to see why the model said this" and "we have no idea, it's gone."

## Privacy-by-design: raw sensitive documents never reach the model

The project wizard's document drop-zones are captioned "Read locally; nothing is uploaded." Client
`Document` rows store only a MinIO object-key pointer, never inline text. Every prompt consumes
*distilled* KCC artifacts (facts already extracted by a separate, presumably human-reviewed, ingestion
step) — never the raw client file. **Lesson:** put a curated extraction layer between confidential
source material and any model call, so "did we just send a client's raw contract to a third-party API"
is structurally impossible to even ask, rather than a policy people have to remember to follow.

## Dual identifiers: opaque UUID for the database, stable human code for everything else

Every entity carries both a DB `id` (uuid) and a business code (`US-0001`, `FT-001`, `EP-001`).
**Lesson:** expose the human code — not the UUID — in prompts, UI, commit messages, branch names, and
test titles. It's the identifier a human (or a model) can actually reason about, remember, and grep for;
keep the UUID strictly as an internal foreign key that never has to leave the database layer.

## State the system's own invariants inside any prompt that could violate them

CLAUDE.md states a platform-wide rule: "Status percentages / parent statuses are derived from leaves,
never hand-set." That exact invariant is *also* written inline inside the `B6a` prompt's PROCESS steps
("Status stays derived — never hand-set"). **Lesson:** don't assume a model will infer an architectural
invariant from having "seen the docs somewhere." If violating an invariant would corrupt data, restate it
explicitly inside every prompt whose output could touch that data — redundant with the docs is fine;
silently relying on the model to already know is not.

## Gate expensive or consequential AI actions behind a visible, scored readiness check

The New Project wizard computes a required-vs-optional checklist and a numeric completeness score, and
disables the (slow, costly, hard-to-partially-undo) "Bootstrap Project" action until required items pass
— showing GO/NO-GO and exactly which checks are missing, rather than a button that's simply always
clickable. **Lesson:** for costly or consequential automated actions, make the trigger conditional on a
visible checklist. It turns validation into a UX affordance the user can act on, instead of either a
silent rejection or — worse — letting a badly-configured run through.

## A claimed-success step and its later read-path must agree, or trust erodes fast

Observed directly in this case study: the bootstrap pipeline reported "Generate project package ✓," but
the dedicated Project Package page then showed "No package generated yet" until the package was manually
regenerated. **Lesson:** when a multi-step pipeline reports per-step ✓/✕, each ✓ must be verified against
the *exact same read path* the user will later check, not just "the write call didn't throw." A green
checkmark that doesn't match what's actually persisted is worse than an honest ✕ — it teaches users to
stop trusting the checkmarks at all, which is a much larger cost than one failed step would have been.
