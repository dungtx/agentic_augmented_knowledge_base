# Minimalist `capture-fleeting` Skill — Requirements (for review, NOT the prompt)

> **Status:** DRAFT for your review. No `SKILL.md` is to be written until you sign off on this.
> **Date:** 2026-06-25 (grilling session 2)
> **Scope:** ONLY the minimalist `capture-fleeting` skill + a stub `AGENTS.md`. `distill-permanent`, `morning-review`, full SRS integration, full AGENTS.md, `.ai/` layout all remain to be grilled separately.

---

## 1. How to read this doc

- **§2 Decisions locked** — black-and-white, came out of grilling. Not editable except by re-grilling.
- **§4 Functional requirements** — the actual behavior the skill must implement. Each is sourced from a locked decision.
- **§5 Proposed defaults pending your veto** — small choices I'm defaulting; you can override any during review without re-grilling.
- **§7 Out of scope** — explicit list of what the minimalist skill must NOT do, so it doesn't creep.
- **§9 Remaining grilling** — what still needs designing after this skill is built (the rest of the system).

---

## 2. Decisions locked (from grilling sessions 1–2)

| ID | Decision | Source |
|----|----------|--------|
| D1 | Architecture = `AGENTS.md` (always-on, vault root) + auto-invokable skills. Minimalist build needs a stub `AGENTS.md` with the dispatch rule. | Q1 |
| D2 | Auto-invocation enabled (`disable-model-invocation` NOT set). Manual `/skill:capture-fleeting` fallback always available. | Q1/2 |
| D3 | Dispatch strength = "strong dispatch w/ one-question confirmation gate." Capture-biased: false-positive (extra note) is recoverable; false-negative (lost idea) is not. | Q2 |
| D4 | Capture destination = `11a1.Inbox/` (unified). No new `11a0.Fleeting/` folder for now; "two pipelines" rigor deferred. | Q3 |
| D5 | No classification at capture time. Capture is dumb + fast; triage is distill's job. | Q3 |
| D6 | Inbox horizon = ~24h (target, not hard delete). Slipping a day ≠ failure; chronic slipping = the signal that distill needs to run. | Q3 |
| D7 | `11a2.Deferred/` = important-not-urgent. `11a3.Someday/` = nice-to-have idea resurfacing. Kept (current items become first distill practice batch). | Q4a |
| D8 | Capture always writes to `11a1.Inbox/`. NEVER routes directly to Deferred/Someday — that routing is distill-time triage. | Q4b |
| D9 | SRS = surfacing frequency only, NEVER a priority taxonomy. ("don't repurpose Anki buttons for urgency"). | Q5 |
| D10 | Inbox is NOT an Anki deck. Capture skill is SRS-coupling-free. | Q5 |
| D11 | Someday + permanent knowledge are *candidates* for future SRS deck via `obsidian-spaced-repetition`, folder-scoped to `11a3.Someday/`. Integrated in distill, not capture. | Q5 |
| D12 | SRS for permanent notes → PINNED for later. Preferred mechanism is AI retrieval (semantic search of LtS via `.ai/`/`.memory/`), NOT timer-based SRS. | Q5 |
| D13 | Three skills on the roadmap: `capture-fleeting`, `distill-permanent`, `morning-review`. Only `capture-fleeting` is in scope for the minimalist build. | Q6 |
| D14 | `morning-review` fires consent-first: only on trigger phrase OR an explicit yes/no offer at session start. NEVER auto-hijacks the session. | Q6 |
| D15 | Minimalist capture skill contains NO morning-review, NO SRS, NO retrieval logic. It only: listen → clarify one-at-a-time w/ hints → write Inbox note → ask "another or done?" → exit. | Q6 |

---

## 3. Scope of the minimalist build

Produces exactly two files:

1. `.pi/skills/capture-fleeting/SKILL.md` — the skill itself.
2. `AGENTS.md` (vault root) — **stub**, containing only:
   - One-paragraph vault vision (placeholder, refined later).
   - One-paragraph KB layout note (the lane definitions D4/D7).
   - The dispatch rule (D3): "if user message looks like a fragment OR mentions capture/jot/note-down → load `capture-fleeting`. If ambiguous, ask ONE disambiguation question first."
   - A "skills roadmap" stub listing the three planned skills with one-liners.

**NOT produced in this build:** `distill-permanent`, `morning-review`, full AGENTS.md vision, `.ai/` files, SRS plugin config.

---

## 4. Functional requirements for `capture-fleeting`

Each requirement is sourced from a locked decision so nothing here is invented.

### F1 — Trigger (D2, D3)
- **Auto-invoked** by the agent when the user's latest message is a raw fragment (short, ungated, no question to the agent) OR explicitly mentions capture/jot/note-down/dump.
- **Manual fallback:** user can type `/skill:capture-fleeting` to force it.
- **Ambiguity gate:** if the agent is unsure whether the message is a capture fragment or a question/request, it asks **exactly one** disambiguation question ("Capture this, or were you asking me something?") before acting. No multi-question preambles.

### F2 — Clarifying-question loop (D5, D15)
- Upon entering the skill, the agent asks the user clarifying questions **one at a time**, NOT a batch.
- Each question must come with **hints** to jog memory. Hint sources, in priority order:
  1. Existing vault content (`rg` the vault for related terms, surface `[[links]]` to nearby notes the fragment might relate to).
  2. Model world-knowledge (only if no vault hits).
- **Question budget: max 3 per fragment** (see C3 default below — veto-able).
- After the budget is exhausted OR the user says "enough"/"just write it", the agent writes the note as-is with a `needs_review: true` flag and stops asking.

### F3 — Write target (D4, D8)
- Writes **only** to `11a1.Inbox/`. Never to `11a2.Deferred/`, `11a3.Someday/`, or `11l.LtS/`.
- Filename pattern: see C2 (default — veto-able).
- Does NOT classify the fragment (task vs fleeting vs lit-note) at capture time. Classification is distill's job.

### F4 — Session cadence (D15, B2 default)
- After writing each note, the agent asks one short prompt: *"Another fragment, or done?"*
- On "done" (or end-session signal the user gives), the skill exits.
- No auto-exit on silence (CLI can't detect it); always ends on user signal.

### F5 — Note format (C1 default — veto-able)
Minimal frontmatter only:
```yaml
---
status: fleeting
captured_at: 2026-06-25T18:45:00+07:00
tags: []
needs_review: false
---
```
- `status: fleeting` — fixed for capture output (other statuses `distilled`/`discarded` set by distill).
- `captured_at` — ISO 8601 with timezone.
- `tags` — empty array at capture; distill assigns.
- `needs_review` — `true` if the question budget was hit before clarification was complete; `false` otherwise.

### F6 — Preview vs direct-write (B1 default — veto-able)
- Default: agent **drafts the note in chat**, waits for user "yes" / "tweak X", THEN writes the file.
- Rationale: you're new to this; 2-second confirm prevents junk notes.
- If you veto this to "write directly then show", the skill writes immediately and pastes the result for the user to edit in Obsidian.

### F7 — Bundling rule (B3 default — veto-able)
- If a single user message contains multiple lines that clearly belong to one logical fragment (e.g. a routine / multi-step thought), the agent bundles them into **one** note.
- If the lines are clearly separate fragments, the agent asks: *"These look like N separate fragments — write as N notes, or one?"* then obeys.
- One-note-per-fragment is the default for clearly-distinct items.

### F8 — Linking (B4 default — veto-able)
- Capture does **not** insert `[[wikilinks]]` into the body. Linking is distill's job.
- Capture is dumb and fast; distill does the smart graph work.
- (Hints in F2 may *reference* existing notes to jog the user's memory, but the written note does not contain links.)

---

## 5. Proposed defaults pending your veto (the B/C items)

| ID | Default | My recommendation | Veto option |
|----|---------|-------------------|-------------|
| B1 | Preview-then-write | (keep) | Change to write-directly-then-show |
| B2 | "Another fragment, or done?" after each write | (keep) | Change signal word/phrase |
| B3 | Bundle if clearly one fragment; ask if ambiguous | (keep) | Always-one-per-fragment OR always-bundle-per-message |
| B4 | No links at capture, links at distill | (keep) | Insert best-guess `[[links]]` at capture |
| C1 | Frontmatter = `status`, `captured_at`, `tags`, `needs_review` | (keep) | Add/remove fields |
| C2 | Filename = `YYYYMMDDHHmm-slug.md` (sortable, collision-proof) | (keep) | Use Luhmann-style fixed IDs / sequential integers / title-with-spaces |
| C3 | Max 3 clarifying questions per fragment, then write-as-is | (keep) | Lower to 1 / raise to 5 / unbounded |

**Review action:** for each row, say "keep" or "change to X." Anything you don't mention stays at default.

---

## 6. Non-functional requirements / constraints

- **N1** — Skill lives at `.pi/skills/capture-fleeting/SKILL.md` (auto-discovered after project trust, per pi docs `docs/skills.md`).
- **N2** — Frontmatter `name: capture-fleeting`, lowercase + hyphens, ≤64 chars. `description` ≤1024 chars, aggressive + specific trigger wording (so auto-invocation matches reliably).
- **N3** — `disable-model-invocation` NOT set (auto-invocation allowed).
- **N4** — No external dependencies: no scripts, no plugin calls (SRS plugin excluded by design per D10).
- **N5** — All hints come from reading the existing vault via `rg`/`read`; no network calls.
- **N6** — Timezone-aware timestamps (`+07:00` assumed by default since you're Asia-based — confirm or veto).
- **N7** — Stub `AGENTS.md` must parse as valid Obsidian-flavored markdown (links must resolve to real files; no broken links).

---

## 7. Out of scope (explicit, to prevent creep)

The minimalist `capture-fleeting` skill MUST NOT:

- Promote a fleeting note to a permanent note (that's distill).
- Triage Inbox → Deferred/Someday (that's distill + morning-review).
- Add tags beyond the empty-`[]` placeholder.
- Insert `[[wikilinks]]` (D5/B4).
- Touch the SRS plugin or any "review scheduling" (D10).
- Run on session-start automatically without user trigger (consent-first per D14, applies to morning-review but capture-fleeting inherits the same discipline).
- Modify `11a2.Deferred/` or `11a3.Someday/` contents.
- Append to `.memory/` or `.ai/` (those are owned by other workflows).

---

## 8. Files to be created after your sign-off

```
AGENTS.md                                                  # stub
.pi/skills/capture-fleeting/SKILL.md                        # the skill
```
(Plus a `.pi/skills/capture-fleeting/` directory implicitly. No scripts/assets for it; one-file skill.)

---

## 9. Remaining grilling (out of this build's scope, on the roadmap)

For the **distill skill** (next grill): Q4 (fleeing lifecycle — archive vs delete, with warned-against practice of "deleting knowledge capture, prefer supersede"), Q5 (fleeting structure refactor?), Q7 (permanent-note placement in `11l.LtS/`), Q8 (atomicity — one-idea-per-note vs cluster), Q9 (permanent note naming), Q10 (linking convention final form), Q11 (MOC handling per-domain + root), SRS deck integration for Someday (D11), AI-retrieval design for LtS via `.ai/` (D12).

For the **morning-review skill**: triage-loop mechanics, cross-lane surfacing of related Deferred/Someday items, consent-fire vocabulary (D14), what counts as "morning"/"start of day" trigger.

For the **AGENTS.md** (full, not stub): full vault vision wording, the `.ai/` file inventory and which ones get imported into always-on context (pi `@`-import mechanism — needs verification via `docs/extensions.md`), `.memory/` structure policy confirmation (append-log + `facts.md` summary as I assumed in the handoff — confirm).

For the **15–20 note-taking concept walkthrough** (your original ask): to be done at end of full grilling. My draft list is in §7 of `0001-...-grilling-session.md`. To be refined + actually walked through with you verbally once all design grilling is done.

---

## 10. Bad-practice warnings issued this session (for the record)

- W6: "auto-invocation = guaranteed" → defense-in-depth (D2 + aggressive descriptions + manual fallback).
- W7: passive capture (only on `/skill:`) → friction → habit death. Rejected.
- W8: classify at capture time → friction. Rejected (D5).
- W9: `19y.Relics/` as junk drawer → graveyard. Relics = supersession-only.
- W10: repurposing SRS buttons as priority taxonomy → algorithmically wrong. Rejected (D9).
- W11: SRS on Inbox → wrong lifecycle fit. Rejected (D10).
- W12: letting "I was busy" become permanent → backlog-rot → guilt pile. Structural fix: visible backlog + distill cadence (D6), not shaming.
- W13: morning-review auto-firing on session start → agent hijacks session. Rejected (D14).

---

*End of grilling session 2. ~6 substantive questions resolved this session (Q3 final, Q4a, Q4b, Q5 (4 sub-decisions), Q6). Ready for your review of this requirements doc before any SKILL.md is written.*