# 0006 — distill-permanent grilling (partial session, 2026-06-30)

Grilling session on `distill-permanent` skill design, cut short — another agent is already working on this skill. This file records what was locked here and what gaps remain for that agent to resolve.

**Source context:**
- Fragments quarry: `../11b.Seeds/distill-permanent-requirements-fragments.md` (22 fragments, read in full)
- Task brief: `.memory/0003-state-of-system-and-pickup-tasks.md` §T2
- Structural sibling: `.pi/skills/concept-refine/SKILL.md` (same shape, different gate)

---

## Locked decisions (this session)

### D18 — Singular job of distill-permanent
Take a seed → produce one or more atomic permanent notes in `11l.LtS/`, each covering a **specific, narrow concept**, never a broad topic. The agent is brutal about splitting anything that tries to cover too much ground. The standard: "Machine Learning" is a topic, not atomic. "The definition of Machine Learning" or "AI is a general term that has been overused as a marketing shortcut" are atomic.

### D19 — Conversation flow: three-phase
**Plan** (all-at-once: read seed, present split plan with proposed summaries/parents/tags, user approves) → **Draft+Interrogate** (per-note, one at a time: draft note, then grill for gaps/counter-arguments/examples, then next note) → **Forward-link** (final sweep: plant inline `[[wikilinks]]` to ghost notes that should exist but don't yet).

### D20 — Atomicity gate mechanism: relentless challenger (model B)
The agent actively pushes back on over-broad notes. Gate question every note must answer: *"If someone reads only this note, what single thing will they understand?"* If the answer has an "and" in it, split. The agent won't proceed until the user names the specific idea — not the broad territory. Even if the user says "one note about Machine Learning," the agent pushes back: "ML is a topic, not an idea. What's the specific claim?"

### D21 — Input routing (ready-gate)
The agent judges the seed's state and routes:
- **Raw fragments** (quarry-style, unshaped) → suggest `concept-refine` first
- **Shaped drafts** (from seed-inbox or concept-refine) → proceed with distill-permanent
- **`seed_level: project`** → blocked immediately (different workflow, not yet designed)
- **Thin/fuzzy seeds** → agent presents its best understanding, asks user whether to distill anyway, leave, or route elsewhere

---

## Unresolved gaps (for the other agent to resolve)

### G1 — Frontmatter fields (final set)
We were mid-debate. Proposed 8: `status`, `kind`, `source`, `tags`, `keywords`, `summary`, `parents`, `siblings`. The user pushed back on `kind` — in practice, are permanent notes ever not `idea` or `lit-note`? If always one of two values, `kind` carries little signal. **Unresolved:** keep all 8, drop `kind`, or drop something else?

### G2 — MOC maintenance rules
Fragments say: agent-handled, no approval required. Agent reads existing MOCs, appends wikilinks, creates sections as needed, creates new MOCs for new concepts. **Not grilled.** Questions:
- What counts as "fits an existing section" vs "needs a new section"?
- When creating a new MOC, what structure does it get? Template?
- If a note fits multiple MOCs, link to all — but does the agent propose or just do it?

### G3 — Seed archival pattern
Fragments propose: archive to `11b.Seeds/_processed/<slug>.md` with `status: distilled` and `permanent_note` wikilink. Seed file renamed so its slug is reclaimed for the permanent note. **Not grilled.** Questions:
- Is `_processed/` a flat folder or mirroring the Seeds structure?
- Does the agent update the seed's own frontmatter or create a new file?
- What happens to the seed's original keywords/tags — do they transfer to the permanent note or get cleaned?

### G4 — Naming convention
Fragments: keyword-rich kebab-case slug, up to ~6 words. Archived seed renamed to reclaim slug. **Not grilled.** Question: what makes a slug "keyword-rich"? Agent proposes or user names?

### G5 — Tag handling / controlled vocabulary
Fragments reference a `tag-glossary.md` (modeled on `presale-glosary.md`) in `11l.LtS/`. Agent refines seed's tags against controlled vocabulary, standardizes terms, drops noise. **Not grilled.** Questions:
- Does the tag-glossary exist yet? If not, who creates it and when?
- How does the agent know which terms are in the controlled vocabulary?
- What happens when a note introduces a genuinely new tag not in the glossary?

### G6 — Loop behavior / topic-contiguous
Fragments: after finishing one seed, agent surfaces adjacent seeds or sibling permanent notes in the same conceptual neighborhood. Loop stays topic-contiguous rather than jumping randomly. **Not grilled.** Question: how does the agent discover "adjacent" seeds? Grep tags? Keyword overlap? The sibling frontmatter field in existing notes?

### G7 — Forward-link mechanics
Fragments: inline `[[wikilinks]]` to nonexistent notes — Obsidian renders them as dim nodes. Simple mechanism. **Not grilled.** Questions:
- How aggressively does the agent plant forward-links? Every mentioned concept that doesn't have a note?
- Are forward-links in the body only, or also in frontmatter (separate field)?
- Should the agent distinguish "this should definitely be distilled later" from "this might be worth exploring"?

### G8 — CDI worked-example test case
From `0003 §3.1`: the CDI note should split into (a) deal note under `11l06.Presales/` + (b) human-in-the-loop verification design note under `11l05.AI/`. **Not discussed in this session.** The building agent should use this as a concrete test case to validate the skill design.

### G9 — Sibling link discovery
Fragments: `siblings` frontmatter field for adjacent permanent notes. Agent should search `11l.LtS/` during Plan phase and surface them. **Not grilled.** Questions:
- Search mechanism? Grep keywords? Read all LtS summaries? Both?
- How many siblings is too many? Cap?
- What distinguishes a sibling from a parent? (Both are wikilinks to other permanent notes.)

### G10 — Note body structure
Fragments: summary lives in frontmatter as `summary` field, not in the body. Body starts where the idea unfolds — seed body transplanted below, lightly edited, with inline wikilinks. **Not grilled.** Question: if there's a conceptual summary in the seed body already (from seed-inbox rewrite), does the agent extract it into frontmatter `summary` and strip it from the body, or duplicate?

### G11 — Interaction with concept-refine pipeline
Both concept-refine and distill-permanent output to `11b.Seeds/` (concept-refine writes the final seed there; distill-permanent reads from there). **Not discussed.** Questions:
- Does concept-refine's output seed carry a flag marking it "distill-ready"?
- Can a seed go concept-refine → distill-permanent in one session, or is there an intentional pause between them?
- What prevents the user from running distill-permanent on a concept-refine output before concept-refine is done?

### G12 — Summary-as-embedding-target design
Fragments decided: start with grep (Option B), but structure `summary` field to be embedding-ready for future vector search. **Not grilled.** Question: what makes a summary "embedding-ready"? Length constraint? Self-contained (no "as mentioned above")? Specific formatting?

---

## In-scope but not yet reached in grilling tree

These are in the fragments file and T2 brief but we didn't get to them:
- Parent link validation (what makes a valid parent?)
- Multi-parent rules (domain MOC + concept MOC simultaneously)
- The interrogate protocol (specific questions the agent must ask — counter-arguments, examples, disagreements)
- Permanent note placement (flat in `11l.LtS/` initially — fragments say yes, not grilled)
- `status` value for permanent notes (`permanent`? `distilled`? something else?)

---

## What the other agent should read first

1. **`../11b.Seeds/distill-permanent-requirements-fragments.md`** — the full quarry. This is the canonical requirements source.
2. **`.memory/0003-state-of-system-and-pickup-tasks.md`** §T2 — the build brief with grilling questions Q4–Q11.
3. **This file** — locked D18–D21 + gaps G1–G12.
4. **`.pi/skills/concept-refine/SKILL.md`** — the structural template. Distill-permanent mirrors its shape; swap the concept-gate for the atomicity-gate.
