# Handoff: Secretary/Capture Subagent Design — Grilling Session 1

> **Status:** IN PROGRESS. Session paused to distill to memory. Next agent resumes grilling.
> **Date:** 2026-06-25
> **Goal of overall work:** Design + write an `AGENTS.md` and skill(s) that turn pi (running *inside* this Obsidian vault) into a "knowledge secretary": capture fragments → clarify → fleeting notes → reviewed permanent zettelkasten notes. Must keep agent-only memory (`.memory/`) and agent-facing quick-ref (`.ai/`).
> **What this file is NOT:** the final `AGENTS.md`. It is the *grilling record + decided questions + next question*. The permanent doc gets written only after grilling completes.

---

## 1. The user's stated intentions (full original ask)

1. Build a "secretary helper": user dumps short input (sometimes a single jotted line); agent asks **one** clarifying question at a time WITH related hints to jog the user's memory, then writes a *fleeting distilled note* into this folder (Obsidian vault).
2. The agent must always be aware of the user's **vision for the folder**.
3. After user reviews the fleeting note, agent rewrites — based on feedback given in-file OR verbally — into a **permanent knowledge note** following **zettelkasten practice**, **Obsidian wikilinking**, and **KM best practices for human notes**.
4. Agent keeps **`.memory/`** for agent-only memory, and **`.ai/`** for agent-focused quick-lookups / lessons learned.
5. User is **new to note-taking** generally. At the END of the grilling, walk them through **15–20 note-taking concepts**, explain each, suggest integration into *their* vault.
6. During grilling: **warn about bad practices / wrong ideas** about note-taking and tell the user what to do instead, inline.

## 2. Conversation context discovered by exploring the vault

- Vault root: `/srv/dzdir/10.Personal/11.KnowledgeBase`
- Layout (PARA-ish / Johnny-decimal style):
  - `11a.Capture/` — `11a1.Inbox/`, `11a2.Deferred/`, `11a3.Someday/`
  - `11l.LtS/` — "Lessons to Self": distilled permanent notes; has `MOC.md` (map-of-content); subfolders `11l01.Linux`, `11l05.AI`, `11l06.Presales`
  - `19z.Resources/` — cloned external repos (skills-main, market-my-spec, codemyspec)
- Existing conventions in use: Obsidian `[[wikilinks]]`, glossary/MOC pattern (see `11l.LtS/11l06.Presales/00 - Presales Glossary.md`), per-domain deep subfolders.
- Capture notes today are very RAW and mixed: bare bullet lists (`Japanese Dailies.md`), task lists (`AIX-bootstrap-todos.md`), pure link dumps with no context (`skills-collections.md`).
- pi already configured here: `.pi/settings.json` sets subagent models (delegate/scout/worker/reviewer via opencode models). `.atl/` = pi skill-registry cache (gitignored in `.gitignore`). No `AGENTS.md`, no `.memory/`, no `.ai/` exist yet.

## 3. CONFIRMED decisions (from the grilling so far)

1. **Three artifacts, two mechanisms — split (option A).**
   - `AGENTS.md` at vault root → always-on: vault vision + conventions + KB layout + dispatch rules.
   - **Two** skills (auto-invokable + `/skill:` manual fallback):
     - `capture-fleeting` — the capture session.
     - `distill-permanent` — the review→rewrite session.
   - Single-responsibility per skill; user rarely runs both in one sitting.

2. **Auto-invocation: YES.** User asked if the agent can invoke a skill without user input. Check of `docs/skills.md` confirmed: skills are auto-invokable by the agent based on description match (progressive disclosure). `disable-model-invocation: true` would BLOCK auto-invocation (we do NOT set it). Manual fallback `/skill:name` always available.
   - **IMS caveat raised and accepted**: auto-invocation is probabilistic (docs say "models don't always do this"), and for a *capture* tool where dropping input = lost knowledge, "probably fired" is not good enough. Defense in depth: aggressive skill descriptions + `AGENTS.md` restates dispatch + manual `/skill:` backup.

3. **Invocation aggressiveness (option A).** Strong dispatch w/ one-question confirmation gate. `AGENTS.md` rule: if the latest user message looks like a raw fragment OR mentions capture/jot/note-down → immediately load `capture-fleeting` and run its flow (do not pre-summarize). If ambiguous → ask ONE disambiguation question first ("Capture this, or were you asking me something?") then act.
   - Accepted principle: cost of false capture (one extra note to delete) is recoverable; cost of missed capture (lost idea) is not → bias toward capturing.

## 4. Open question — IN THE MIDDLE OF THIS ONE (paused mid-answer)

**Question 3 was:** Where do fleeting notes live, and how do they relate to the existing GTD-style `11a.Capture` folders?

User response (final message of session): *"11a.Capture is not using zettelkasten properly I admit that… if you think it doesn't line up with the correct design then we can retire them into 19y.Relics."*

I pushed BACK (in-progress answer, NOT yet accepted by user) on retiring wholesale. My recommendation was:
- **Don't retire `11a.Capture`**. The buckets aren't wrong — they're GTD (Inbox / Deferred / Someday) which legitimately coexists with zettelkasten. Confusion = knowledge fragments + task items share folders with no labels. **Two pipelines, not one**.
- Proposed: keep `11a1.Inbox` (redefine: GTD/triage for tasks, links-to-read, decisions — non-knowledge; capture skill must NOT write knowledge here), keep `11a2.Deferred` (fix typo from `Deffered`), keep `11a3.Someday`, ADD new `11a0.Fleeting/` as the ONLY place the capture skill writes knowledge fragments, with enforced TTL.
- `19y.Relics/` reserved ONLY for notes with a clear SUPERSESSION reason — never a junk drawer for "stuff unsure about".
- Offered options: A=keep+add-fleeting (recommended), B=retire GTD wholesale (user's last leaning, but I argued against), C=triage case-by-case.

**Next agent's job:** present this pushback/options cleanly to the user, get a decision on A vs B vs C, THEN keep grilling down the design tree. NEXT QUESTIONS to resolve after that:

**Pending branch (Q4 onward) — not yet discussed / user has not answered any of these:**
- Q4: Fleeting note lifecycle — after distillation, archive to `_processed/` OR hard-delete the original? Recommend archive for audit trail (can cull later); user leans to "feels like junk"; user is wrong (archive is best practice — never delete knowledge capture, supersede it).
- Q5: Fleeting note *structure/schema* — frontmatter fields (id, captured-at, source-context, status, tags)? Recommend minimal frontmatter: `status: fleeting|distilled|discarded`, `captured_at`, `tags`. (Bad practice to avoid: tagging-schema-by-vibe → settle a controlled vocab early.)
- Q6: The clarifying-questions mechanic — how many rounds, do hints come from (a) the fragment text itself, (b) similar existing notes, (c) agent world-knowledge, (d) session history? Recommend: bounded to N=3 questions max, hints sourced from existing vault content FIRST (pulls `[[links]]` to nearby notes), then fallback to model knowledge.
- Q7: Permanent note placement rules — a note on X goes where in `11l.LtS/`? Domain-fits by subfolder, ambiguous → goes to a `Kasten/` or `Concepts/` flat layer (zettelkasten notes are organized by CONNECTIONS not folders)? Flag practice issue: zettelkasten proper says notes are index-card atomic, ONE idea per note, linked not nested. Current LtS notes lock to domain folders → anti-pattern but acceptable hybrid ("folder index + link graph").
- Q8: Note atomicity rule — one idea per note vs topic-cluster notes? Recommend ONE-idea-per-note (classic zettelkasten); current LtS notes are cluster-length → flag + ask.
- Q9: **Naming/ID convention for permanent notes** — sequential ID (`202606251543`), slug-title (`kill-tty`), or Luhmann-style ID branch? Existing files mix — e.g. `kill-tty.md` (slug), `Customer Persona.md` (title w/ space), `00 - Presales Glossary.md` (prefixed number). Needs decision; recommend: `YYYYMMDDHHmm-slug.md` for permanent (date-prefixed, sortable, collision-proof); reject title-with-space (breaks shell + URLs).
- Q10: Linking convention — `[[free-title]]` Obsidian wikilinks vs `[[slug|alias]]` for readback. Recommend: link by slug, display alias when slug is stiff.
- Q11: MOC handling — one `MOC.md` at LtS root (exists, minimal) vs map-of-contents per domain subfolder (Presales already has a glossary working as a MOC). Recommend: per-domain MOC + a root MOC that links to sub-MOCs (hierarchical MOCs).
- **`.memory/` structure question** (user's stated vision, not yet designed): is `.memory/` an append-log (timeline, like this very doc) OR a key-value store of accumulated facts OR both? Recommend: both — append-log of sessions chronologically prefixed `NNNN-*.md` (decisions over time) + a distilled `facts.md` that gets rewritten each session as a flat summary the always-on context can pull. (This very doc *is* the first append-log entry, named `0001-`.)
- **`.ai/` structure question** (stated vision, not designed): what goes here vs `.memory/`? Recommend: `.ai/` = cargosman-facing quick-lookups / cheat-sheets / lessons (the user's words: "agent focus lessons learned or quick retrieval anything agents need"); `.memory/` = the agent's episodic memory of working WITH the user. Concretely: `.ai/` holds `vault-conventions.md`, `zettelkasten-cheatsheet.md`, `skill-dispatch-map.md` (rules for when to fire which skill), etc. Loaded as context when relevant (low cost).
- Q12: Does `AGENTS.md` `@`-import `.ai/` files or `.memory/facts.md`? Need to check pi's include mechanism. **Next agent: read `docs/extensions.md` or `docs/skills.md` import/include syntax** — the `AGENTS.md` should NOT inline everything (bloats always-on context); use pi's import mechanism to pull only needed pieces on demand.
- Q13: The 15–20 note-taking concept walkthrough — WHEN? User said "at end of grill session". Confirm that means "after all design questions resolved, BEFORE writing AGENTS.md/skills". Recommend: inline these as a `concepts-walkthrough.md` in `.ai/` that gets read to user once via the grill, not re-generated each session.
- Concepts to plan to cover (non-exhaustive, refine to 15-20): Zettelkasten, fleeting/literature/permanent notes, atomicity (one idea per note), map of content (MOC), index cards, link graph vs folder hierarchy, PARA vs Zettelkasten vs GTD vs I-A-R (immediate/active/relevant), spaced-repetition-for-ideas (re-reading), progressive summarization, evergreen notes (Andy Matuschak), the "slow burn" / incubation, the "outline of one" (Niik), titles as claims, the "daily note" log, tags vs links, the "second brain" (Fortel), "searchability vs findability", the "collector's fallacy" (stop hoarding, start processing), "CCC" (capture-consolidate-cache), impermanence of fleeting notes (TTL), single source of truth, "anti-library" (keep unread books, knowledge of what you DON'T know), the "13 Paths"/commonplace book.

## 5. Bad-practice warnings already issued (track so none are re-issued)

- W1: Auto-invocation treated as guaranteed → defense-in-depth decreed (Q above).
- W2: "Probably fired" capture reliability not good enough → aggressive descriptions + manual fallback.
- W3: Passive capture (only on explicit `/skill:`) → high friction → user skips → ideas lost. AVOID.
- W4: Conflating fleeting-notes with inbox/triage items → set up `11a0.Fleeting/` as separate lane.
- W5: Treating "Relics" as a junk drawer for "unsure" things → Relics = supersession-only.
- (more warnings to come as grilling continues)

## 6. How the next agent should resume

1. Read this file in full.
2. Frame Q3 pushback to user (paragraph 4 above) — get A/B/C decision on Capture folder fate.
3. Continue one-question-at-a-time down the Q4+ tree above, EACH with a recommended answer, EACH flagging bad practices inline when relevant.
4. Do NOT write `AGENTS.md` or skill files yet — finish grilling first.
5. When grilling complete: walk user through 15-20 note-taking concepts (Q13), THEN generate `AGENTS.md`, `.pi/skills/capture-fleeting/SKILL.md`, `.pi/skills/distill-permanent/SKILL.md`, `.ai/*` files, and update `.memory/facts.md` with the locked decisions.
6. Keep append-log discipline: every future grilling session appends `NNNN-*.md` in `.memory/`; update `facts.md` as the flat summary.

## 7. Open pi-mechanism unknowns to resolve before final implementation

- Exact `AGENTS.md` include/`@`-import syntax (check `docs/extensions.md` / SDK). Needed for Q12.
- Whether `AGENTS.md` is auto-loaded from project root only or also ancestor dirs. Check docs.
- Whether `.memory/` and `.ai/` need to be in `.gitignore` or tracked (user's call; `.atl` already ignored).
- Whether skills live in `.pi/skills/` (auto-discovered after project trust) or elsewhere. Per `docs/skills.md`: project skills live in `.pi/skills/` and `.agents/skills/`; recommend `.pi/skills/`.

---
*Session 1 of grilling. Paused by user leaving. ~3 questions resolved, ~13+ to go.*