# Vault conventions

> Single source of truth. Referenced by every skill; update here and the change propagates. Cross-reference with `.memory/facts.md` for the executive summary.

## Lanes (writing targets)

| Lane | Purpose | Write authority |
|------|---------|-----------------|
| `11a.Capture/11a1.Inbox/` | Landing area, ~24h horizon. Every capture starts here. | `capture-fleeting` |
| `11a.Capture/11a1.Inbox/_processed/` | Archived captures (after seeding) | `seed-inbox` |
| `11a.Capture/11a2.Deferred/` | Important-not-urgent, promoted at triage | `morning-review` |
| `11a.Capture/11a3.Someday/` | Nice-to-have idea resurfacing; future SRS deck | `morning-review` |
| `11b.Seeds/` | Workable rough drafts. Flat folder. | `seed-inbox`, `concept-mine` |
| `11b.Seeds/_processed/` | Archived seeds (after distillation or concept-refine) | `distill-permanent`, `concept-refine` |
| `11c.Projects/<ProjectName>/` | Active projects — multiple related notes, external artifacts, project-specific context. Each project has a `README.md` as its entry point. | Manual, `seed-inbox` (for seeding into a project) |
| `11l.LtS/` | Permanent notes. Flat by default; place into existing `11lNN.<Domain>/` subfolder only when the note clearly belongs to one. **Never create new subfolders** — categories emerge organically. | `distill-permanent`, `concept-refine` |
| `19z.Resources/` | Cloned external repos (read-only) | Manual |
| `.memory/` | Agent episodic memory: append-log `NNNN-<slug>.md` + `facts.md` snapshot | Any agent |
| `.ai/` | Agent-facing reference (conventions, cheatsheets, retrieval index) | Any agent |

## Frontmatter schemas

### Fleeting (capture output → `11a1.Inbox/`)

```yaml
status: fleeting
kind: idea | task | routine | lit-note
captured_at: 2026-01-01T12:00:00+07:00
tags: []
needs_review: false
```

- `status` — always `fleeting` at capture. `distilled` / `discarded` set by later skills.
- `kind` — orthogonal to `status`. `idea` is the default if unclassifiable. `task` and `routine` share Shape C in seed-inbox; `idea` and `lit-note` share Shape A.
- `captured_at` — ISO 8601, `+07:00` timezone.
- `tags` — empty at capture; distill assigns.
- `needs_review` — `true` if the question budget was exhausted before clarification was complete.

### Seed (draft → `11b.Seeds/`)

```yaml
status: seed
kind: idea | task | routine | lit-note
seed_level: 10min | 1hour | project
captured_at: <carried from capture>
seeded_at: 2026-01-01T12:00:00+07:00
source: "[[../../11a.Capture/11a1.Inbox/_processed/<filename>.md]]"
tags: [tag1, tag2, tag3]
keywords: [kw1, kw2, kw3]
```

- `seed_level` — remaining effort: `10min` = quick polish; `1hour` = focused sit-down; `project` = needs research/multiple sessions (**blocked from distill-permanent**).
- `source` — wikilink to the archived capture in Inbox `_processed/`. Compute the correct relative path from the seed's location.
- `tags` — 2–6 tags from a controlled vocabulary (see tag-glossary).
- `keywords` — budget: **3** for `idea`/`lit-note`, **5** for `task`/`routine`.

### Permanent note (→ `11l.LtS/`)

```yaml
status: permanent
source: "[[<relative path to archived seed in 11b.Seeds/_processed/>]]"
tags: [tag1, tag2, tag3]
keywords: [kw1, kw2, kw3]
summary: "Concrete, self-contained, 3–5 sentences. No cross-references. Specific claims with concrete referents. The scan-line future-you reads in 6 months to decide whether to go deeper. Also the embedding target for future vector search — must be a standalone unit of meaning."
parents: ["[[Parent MOC]]", "[[Broader permanent note]]"]
siblings: ["[[Adjacent note 1]]"]
```

7 fields — none optional. Notes:
- `source` — wikilink to the archived seed (not the original capture). Compute the correct relative path from the note's location.
- `summary` — the scan-line. Must be concrete ("X breaks in three specific ways when Y happens"), not abstract ("X is important"). Self-contained — no "as mentioned above," no cross-references. This is the embedding target for future vector search.
- `parents` — MOCs or broader permanent notes that sit above this one in scope. **A note with no parent is an orphan — invalid.** A note can have multiple parents (domain MOC + concept MOC). Best guess, no approval gate.
- `siblings` — adjacent permanent notes at the same level. Discovered by grep on tags/keywords during distill plan phase.
- `tags` — 2–6, refined against controlled vocabulary from the seed's original tags.
- `keywords` — 3–5 precise search terms (grep targets).
- `kind` is deliberately dropped — signal/noise too low for permanent notes (nearly always `idea` or `lit-note`).

### Archived seed (→ `11b.Seeds/_processed/`)

```yaml
status: distilled
permanent_note: "[[<relative path to permanent note>]]"
# all other seed fields left intact
```

- The seed moves to `_processed/archived-<original-slug>.md` — the `archived-` prefix frees the original keyword-slug for the permanent note.
- Multiple permanent notes → multiple wikilinks in `permanent_note`.
- Never delete — provenance chain (capture → seed → permanent) is the vault's intellectual history.

## Filename conventions

| Note type | Pattern | Example | Rationale |
|-----------|---------|---------|-----------|
| Capture (fleeting) | `YYYYMMDDHHmm-slug.md` | `202606261148-cedar-cdi-bid-preproposal.md` | Sortable, collision-proof |
| Seed | `keyword-slug.md`, kebab-case, ≤6 words | `candidate-evaluation-rubric.md` | Readable, keyword-rich |
| Permanent note | `keyword-slug.md`, kebab-case, ≤6 words | `verification-gates.md` | **No date prefix** — permanent notes are timeless. Sortability comes from MOC/link graph. |
| Archived capture | `<original-filename>.md` | `202606261148-cedar-cdi-bid-preproposal.md` | Preserved as-is |
| Archived seed | `archived-<original-slug>.md` | `archived-verification-gates.md` | Non-keyword prefix frees the original slug |

## Slug rules (applies to seed + permanent note)

- Kebab-case, lowercase, hyphens only.
- Maximum 6 words.
- Keyword-rich — the terms the user would grep to find this note.
- No dates, no IDs, no sequential numbering.
- If a slug collides with an existing file, append `-2` (never silently overwrite).

## Project lane (`11c.Projects/`)

### Project workflow

Two pipelines share the Inbox but diverge: **capture → seed → permanent** and **capture → project**.

| Phase | What happens |
|-------|-------------|
| **Trigger** | 2+ related Inbox items → agent asks to start a project; or user invokes directly ("start project X") |
| **Kickoff** | Project-specific skill grills user from Inbox clues → generates `README.md` + scattered initial notes. Replaces `seed-inbox` for project-bound items. |
| **Active** | User invokes "work on project X." All session output lives inside `11c.Projects/<ProjectName>/`. New captures during active work still go to Inbox; agent periodically surfaces relevant Inbox items and asks "promote to project or leave?" |
| **Closed** | Project stays in `11c.Projects/`. `README.md` status updated to `closed`. Retro session surfaces old notes: what went wrong, why, what to do differently, what to set up first next time. Lessons may be distilled to `11l.LtS/`. |

### Project README frontmatter

```yaml
project: <ProjectCode-ClientSlug>
client: <codename, no real names under NDA>
status: bid | delivery | closed
started: 2026-01-01
closed: 2026-06-15  # only when status = closed
```

### Project structure

- `11c.Projects/<ProjectName>/README.md` — entry point (overview, status log, links to project notes)
- Flat `.md` files alongside README — no subfolders until volume demands it
- **No client documents** (NDA). Agent must flag PII or client-identifying info and ask user to remove.
- New captures during active work → Inbox (not project). Agent surfaces relevant ones.

### Project agent rules

- **Flag PII/client info** — if you see real names, internal company documents, or identifying details, pause and ask user to remove.
- **Don't create subfolders** inside a project until volume clearly justifies it (user will say when).
- **Update README status log** on every substantive project event.
- **Project notes use readable filenames** — `mcp-internal-notes.md`, not date-prefixed (dates live in frontmatter or status log).

### TODO — project skills (not yet built)

- **project-kickoff skill** — grills user from Inbox clues, generates README + initial notes. Replaces seed-inbox for project-bound items. Seam between raw capture and project note TBD.
- **project-retro skill** — surfaces old notes when project closes, asks: what went wrong, why, how to do better, redo-priorities. Distills lessons to `11l.LtS/`.
- **Seam clarification** — during active project work, the boundary between "keep in Inbox" vs. "move to project" needs a concrete rule. Current policy: capture always → Inbox; agent surfaces relevant ones.

## Controlled vocabulary (tags)

A central tag-glossary lives at `11l.LtS/tag-glossary.md`. When assigning tags:
- Pick from the glossary. Each tag has a one-line definition — use the most precise match.
- 2–6 tags per note.
- Adding a genuinely new tag is fine — add it to the glossary with a definition after.

## Agent hard rules

- **Never delete.** Archive only (`_processed/` folders).
- **Never commit files you didn't create** (W14).
- **Never write outside the lane** a skill owns.
- **Never create a new `11l.LtS/` subfolder.** Place into an existing one only.
- **Never use a date prefix in a permanent note filename.**
- **One question at a time when grilling** (mp-grilling discipline).
- **Write skills per `mp-writing-great-skills`** (`~/.pi/agent/skills/mattpocock-skills/skills/productivity/writing-great-skills/`).
- **Preview then write** for permanent notes; write directly for capture (live mode) and seeds.
