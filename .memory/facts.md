# facts.md — vault snapshot

> A flat, current-state summary for fast agent bootstrap. Rewrite this file when a substantive task changes the state. The timeline lives in `NNNN-<slug>.md`; this is the "answer me now" layer.
> Last updated: 2026-07-17 (project lane created, BJP26110-RIC kicked off)

## User

Dzung — Presales, AI engineering, career development, Japanese learning. Based in Asia (timezone `+07:00`). New to note-taking; building this vault to develop the habit and surface knowledge over time.

## What this vault is

An Obsidian knowledge base with an AI secretary pipeline: **capture → process → permanent note**, zettelkasten-style (atomic notes, linked graph, MOCs). Two paths reach permanent notes:

- **Path A:** capture-fleeting → seed-inbox → distill-permanent → `11l.LtS/`
- **Path B:** concept-mine → concept-refine → `11l.LtS/` (bypasses seeds)

Capture is lossy — bias toward capturing (a stray note is deletable; a missed thought is gone). Distill is the opposite — the bar is high because a bad permanent note clutters the record.

## Built

| What | Where |
|------|-------|
| 8 skills | `.pi/skills/<name>/SKILL.md` — capture-fleeting, seed-inbox, project-kickoff, project-retro, distill-permanent, concept-mine, concept-refine, morning-review |
| 1 active project | `11c.Projects/BJP26110-RIC/` — AI transformation consultant bid for RIC |
| AGENTS.md (signpost) | Vault root — dispatch table + ambiguity gate + pointers |
| facts.md | `.memory/facts.md` — this file |
| .ai/vault-conventions.md | `.ai/vault-conventions.md` — frontmatter schemas, filenames, lane rules |
| .memory/ append-log | 0001–0008 — grilling sessions, requirements, task inventory, T9/T10 |
| Git | `main` @ `github.com:dungtx/agentic_augmented_knowledge_base.git`, author `dante` |

## Planned / next

In rough priority order (full task briefs: `.memory/0003-state-of-system-and-pickup-tasks.md`):

1. ~~T6 — facts.md~~ ✅
2. ~~T7 — `.ai/vault-conventions.md`~~ ✅
3. ~~Central tag-glossary~~ ✅
4. **G8 — distill test** — run distill-permanent on a real seed to validate the skill
5. ~~T3 — morning-review skill~~ ✅
6. ~~T5 — note-taking concept walkthrough~~ ✅
7. **T10 — web-research skill** — research on user's behalf → cited notes
8. **T8 — SRS for `11a3.Someday/`** — spaced-repetition deck (pinned)
9. ~~T11 — project-kickoff skill~~ ✅
10. **T12 — project-retro skill** — surface lessons when project closes, distill to permanent notes

## Key conventions (hard rules from locked decisions)

**Lanes (writing targets):**
- `11a.Capture/11a1.Inbox/` — every capture lands here (~24h horizon)
- `11a.Capture/11a2.Deferred/` — important-not-urgent (triage-time promotion)
- `11a.Capture/11a3.Someday/` — nice-to-have idea resurfacing
- `11b.Seeds/` — rough drafts; `_processed/` for archived seeds
- `11c.Projects/<ProjectName>/` — active projects (bid/delivery/personal). Capture → project pipeline, separate from capture → seed. README.md as entry point.
- `11l.LtS/` — permanent notes (flat default, place into existing `11lNN.<Domain>/` subfolder when clearly belonging; never create new subfolders)

**Frontmatter — fleeting (capture output):**
`status: fleeting`, `kind: idea|task|routine|lit-note`, `captured_at` (ISO 8601 +07:00), `tags: []`, `needs_review: true|false`

**Frontmatter — seed:**
`status: seed`, `kind`, `seed_level: 10min|1hour|project`, `captured_at`, `seeded_at`, `source` (wikilink to archived Inbox note), `tags`, `keywords`

**Frontmatter — permanent note (7 fields):**
`status: permanent`, `source` (wikilink to archived seed in `11b.Seeds/_processed/`), `tags`, `keywords`, `summary` (concrete, self-contained, 3–5 sentences — the scan-line + future embedding target), `parents` (array of wikilinks to MOCs/broader notes), `siblings` (array of wikilinks to adjacent permanent notes)

**Filenames:**
- Capture: `YYYYMMDDHHmm-slug.md`
- Seed: keyword-slug, kebab-case, up to 6 words
- Permanent: keyword-slug, kebab-case, up to 6 words, **no date prefix** (timeless)

**Agent discipline:**
- Never delete — archive only (`_processed/` folders)
- Never commit files you didn't create (W14)
- One question at a time when grilling (mp-grilling)
- Write skills per `mp-writing-great-skills` (`.pi/skills/` … `GLOSSARY.md`)
- Project folder naming: `<BidCode>-<ClientSlug>` when a bid code exists (e.g., `BGB26195-CDI`, `BJP26110-RIC`); client slug alone otherwise

## Deeper reading

| When you need | Read |
|---------------|------|
| Full task inventory + locked decisions | `.memory/0003-state-of-system-and-pickup-tasks.md` |
| Skill bodies | `.pi/skills/<name>/SKILL.md` |
| Vault conventions (full spec) | `.ai/vault-conventions.md` |
| Session history | `.memory/NNNN-*.md` (chronological) |
