# Seed-Inbox Skill Design — Grilling Session 4

> **Date:** 2026-06-29
> **Status:** DRAFT complete. Skill written, not yet tested on real Inbox items.
> **Goal:** Design a POC skill to process Inbox items into workable drafts, bridging the gap between raw capture and full zettelkasten permanent notes.

---

## 1. Context entering this session

- `capture-fleeting` is built and working. Pipe ends at Inbox — nothing processes notes into anything usable.
- `distill-permanent` is planned but the user doesn't have time for full zettelkasten research right now.
- User wants a stepping stone: "workable notes that can be updated later."
- User rejected a separate `11a0.Fleeting/` folder in earlier grilling (D4) but wanted a new lane here: `11b.Seeds/`.

---

## 2. Locked decisions from this session

| ID | Decision |
|----|----------|
| S1 | New lane: `11b.Seeds/` — flat folder, no sub-levels. Parallel to `11a.Capture/` and `11l.LtS/`. |
| S2 | `seed_level` frontmatter field uses **effort-remaining** axis: `10min` \| `1hour` \| `project`. NOT completeness-based (avoided taxonomy rabbit hole). |
| S3 | Agent drafts substantively, not just metadata. Rewrites the fragment with a fresh perspective + broad overview. |
| S4 | Draft shapes by `kind`: **A** (restatement + expansion) for idea/lit-note; **C** (contextualized brief) for task/routine. |
| S5 | Shape **B** (interrogation-in-writing) deferred to a future skill. Agent may offer it conversationally during review but does not implement it inline. |
| S6 | Clarifying approach: **C** — agent fills in best guesses for everything, asks only genuinely ambiguous gaps (max one question). |
| S7 | Keywords: **3** for idea/lit-note, **5** for task/routine. Drives the slug + retrieval. |
| S8 | Slug: kebab-case from keywords (up to 6 words). Agent proposes, user confirms (A). Slug reflects user's mental retrieval vocabulary, not zettelkasten claim-title. |
| S9 | Original Inbox file archived to `11a1.Inbox/_processed/<original>.md` with `status: seeded` + `seed:` wikilink back to the seed. |
| S10 | Seed frontmatter: `status: seed`, `kind:`, `seed_level:`, `captured_at:` (carried forward), `seeded_at:` (now), `source:` (wikilink to archived original), `tags:`, `keywords:`. |
| S11 | Skill name: `seed-inbox`. Lives at `.pi/skills/seed-inbox/SKILL.md`. Model-invoked (has description). |
| S12 | Pipeline is now 3-stage: Inbox → Seeds → LtS. `distill-permanent` will handle Seeds → LtS when built. |
| S13 | `AGENTS.md` updated: `11b.Seeds/` added to vault layout, `seed-inbox` added to skills roadmap (status: built). Dispatch rule added for "seed / process / promote" triggers. |
| S14 | `kind` correction included — capture defaults to `idea`; seeding may reassign (e.g. `task`, `routine`). |

---

## 3. Skill structure (what was built)

`.pi/skills/seed-inbox/SKILL.md` — 5 steps:

1. **Pick** — resolve which Inbox note (user specifies or agent lists + asks)
2. **Draft** — read raw note, produce full rewritten seed (body by shape, frontmatter enriched, slug from keywords)
3. **Review** — present draft + summary of decisions + ask only genuinely ambiguous gaps (max 1 question)
4. **Write + archive** — seed to `11b.Seeds/<slug>.md`; original to `11a1.Inbox/_processed/` with `status: seeded` + `seed:` wikilink
5. **Loop/end**

Guardrail list: never promotes to LtS, never hard-deletes originals, never writes outside Seeds, never exceeds keyword budgets, never asks >1 clarifying question, never runs shape B inline.

---

## 4. What changed in the vault

- `11b.Seeds/` folder created (empty)
- `AGENTS.md` updated: vault layout + dispatch + roadmap
- `.pi/skills/seed-inbox/SKILL.md` written

---

## 5. Not yet done / follow-up

- Skill not yet tested on real Inbox items (6 waiting: CDI, Android lockout, 3 untracked, Japanese Dailies)
- `distill-permanent` (Seeds → LtS) still planned, not built
- `morning-review` still planned, not built
- `.memory/facts.md` still not created (T6)
- `.ai/` still not created (T7)
- Live mode for capture (T4) still not implemented
- 15–20 note-taking concept walkthrough (T5) still not delivered

---

*End of grilling session 4. ~14 decisions locked. 1 skill built (POC). Pipeline now Inbox → Seeds → (future) LtS.*
