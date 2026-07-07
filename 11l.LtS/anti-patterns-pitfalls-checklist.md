# Anti-Patterns & Pitfalls — Checklist

A "what NOT to do" cut across the three companion clusters — [[11l05.AI/prompt-engineering-process-lessons|prompt
text]], [[11l05.AI/ai-product-architecture-patterns|AI-system architecture]], and
[[monorepo-structure-devex-lessons|general project structure/DevEx]] — all from the same case study
(kcc-platform). Each entry: the concrete instance observed, then a **Guard:** — the generalized check to
run against your own system to see if you have the same problem.

## The meta-pattern underneath most of these

Three unrelated-looking bugs (a mislabeled error, a wrong status checkmark, and wrong-but-plausible
generated content) are actually the same failure shape: **the system produced a confident, specific,
wrong signal instead of an honest "something's off."** A crash is annoying but obvious. A checkmark that
lies, an error message that names the wrong cause, or generated text that looks right but isn't — each of
those costs more, because the first time someone catches it, they stop trusting *every* signal from that
system, not just the one that was wrong.

**Guard:** for every place your system emits a status (✓/✕, a claimed success, generated content, an
error message), ask: *if this is wrong, would anyone notice before it causes damage?* If the answer is
"only by accident," that's this pattern.

## Prompt-text pitfalls

1. **Instruction-last on long prompts.** The task instruction (PROCESS) is stated once, *after* a
   24-48k-char context block, with no repeat before/after it (no "sandwich"). Worked here because the
   model is capable; degrades first on the longest, most context-heavy items. **Guard:** grep your
   longest prompts — is the actual ask closer to the front or buried at the end of the context dump?
2. **Redundant, inconsistently-worded role framing.** System message says "You are a {role}"; the user
   message's first line restates "ROLE {role} — {task}" in a different shape. Not harmful, just
   duplicated with no clear reason. **Guard:** pick one place role lives (system message) and stop
   repeating it differently in the body.
3. **A safety-critical constraint sharing a sentence with unrelated procedural trivia.** "Never invent —
   mark unknowns TBD" was tacked onto the end of a CONDITION line that also carried governance metadata,
   at the very tail of a long prompt. **Guard:** does your one anti-hallucination clause have its own
   labeled section, ideally echoed in the system message — or is it riding along with something else?
4. **Output described as a loose hint when something downstream actually parses it.** A markdown heading
   naming columns (`## Gaps (type · description · ...)`) is not a grammar. **Guard:** if any code parses
   a model's free-text output, does the prompt specify the *exact* delimiter/shape, or just a vibe?
5. **Claiming the model can "read" something it was only given a title for.** "Client documents — read
   these as the source of truth" followed by five bare titles, no content. **Guard:** for every input
   section, can the model actually act on what's there, or only cite that it exists?
6. **No instruction to sanity-check upstream machine-generated input.** A prior AI step's draft backlog
   contained obviously templated/broken text; nothing told the consuming prompt to flag that as a finding
   — it caught it by luck. **Guard:** if a prompt's input was itself AI-generated, does it explicitly ask
   the model to treat "this looks like unresolved template output" as a first-class thing to report?
7. **Leaning on model competence to cover an underspecified prompt.** Good output happened despite a weak
   spec, not because of a strong one. **Guard:** would a less capable model, or the same model on a
   harder case, still get this right — or did you get lucky this time?
8. **Sibling prompts inventing their own taxonomy for the same concept.** One prompt classifies issues
   Critical/High/Medium; a closely related one classifies missing/conflict/edge-case/implied-NFR — same
   underlying idea, two incompatible vocabularies. **Guard:** do all prompts touching "how bad is this"
   or "what kind of problem is this" share one defined vocabulary, or did each one invent its own?

## AI-system architecture pitfalls

9. **Catching every error class identically and reporting a specific-but-wrong cause.** Any gateway
   failure — timeout, 500, rate limit — gets swallowed with no logging and reported to the user as
   "Gateway disabled," even when it's up and just erroring. **Guard:** does your fallback message name
   the *actual* failure, or a plausible-sounding default that may not be true? Is the real error logged
   anywhere, or gone the moment it's caught?
10. **Dead grounding code that still runs on every call.** A real search + DB hydration executes on every
    single prompt invocation, producing data the render step never reads. Pure cost, zero function.
    **Guard:** for every field your context-assembly step computes, is it actually consumed downstream —
    or is it a leftover from a design that moved on?
11. **No caching of an expensive, unchanged context block across rapid repeated calls.** Clicking five
    different actions on the same item rebuilds the same large knowledge block from scratch five times in
    one sitting, even though nothing about the underlying data changed between clicks. **Guard:** if a
    user can trigger the same expensive context-assembly multiple times in quick succession on the same
    target, is there any reuse, or is every click a full rebuild?
12. **A stated product promise missing the one field it depends on.** Per-project budget alerts were
    promised at project creation; the actual model-call attribution tags never include the project id.
    **Guard:** for every governance/cost feature you've promised in the UI, trace it to the exact call
    site — does the data it needs actually get captured there, or does the promise stop being true one
    layer down?
13. **A hard constraint approximated by an unverified soft proxy.** Model context-window limits (a token
    count) are approximated by a character-count budget, with no check that the proxy actually holds for
    the model in use. Works today on headroom, not by design. **Guard:** wherever you're trimming to
    "fit," are you measuring the thing that actually has the limit, or a stand-in for it?
14. **Paid AI calls triggered as a side effect of navigation.** Opening an item's detail tab auto-fires a
    costly prompt with no explicit user action and no visible cost/opt-out. **Guard:** can a user
    accidentally spend money just by clicking around to look at something, with no "are you sure" or
    visible cost signal first?

## Product / live-system pitfalls (the ones only a real walkthrough catches)

15. **A pipeline step reports ✓ for something that isn't actually there yet.** Bootstrap claimed "Generate
    project package ✓"; the dedicated Package page said "No package generated yet" until manually
    regenerated. **Guard:** for every step that reports success, does it check the *same read path* the
    user will later use to verify — or just "the write call didn't throw"?
16. **Fallback-generated content that's wrong in a specific, plausible-looking way.** A demo/fallback
    backlog for a "TDCX Support Portal" project contained generated user stories written as "a PEXA user"
    (a different real client) and an unrelated "Chat UI" epic — not obviously fake, just quietly wrong.
    **Guard:** when your system falls back to generic/demo content, does it ever accidentally carry over
    specifics (another client's name, an unrelated domain) that make the wrong content look legitimate?
17. **Failed sub-steps surfaced as a bare ✕ with no next action.** A multi-step pipeline showed some steps
    failed (repo provisioning, workspace publish) with no explanation of why or what the user should do
    about it. **Guard:** when a step in a visible pipeline fails, does the UI say anything actionable, or
    just show the failure and stop?

## Project-structure / DevEx pitfalls

18. **Dev convenience that's one environment-promotion mistake from a real vulnerability.** A seeded
    default admin account makes every fresh environment instantly usable — and is exactly the kind of
    thing that becomes a production incident if it's not *strictly, visibly* gated out of prod. **Guard:**
    for every "seed a known-good account/secret for convenience" pattern, is the "never in production"
    rule as loud and explicit as the convenience itself, or an assumed unwritten rule?
19. **Infra tooling that silently uses the wrong default instead of failing loudly.** Docker Compose
    quietly ignores your `.env` file if you forget `--env-file`, rather than erroring — a footgun the docs
    had to call out by hand. **Guard:** for your own required config, does the missing/misapplied case
    fail loudly, or silently fall back to something that looks like it worked?
20. **A "ready" gate that only checks required fields creates false confidence.** GO/NO-GO in the wizard
    only enforces the required (*) fields; several quality-relevant fields (tech stack, KCC inheritance,
    governance gates) are optional and can be empty while the gate still shows green. **Guard:** does your
    readiness gate mean "will produce good output," or only "won't be rejected" — and do the people
    reading GO know which one they're getting?
