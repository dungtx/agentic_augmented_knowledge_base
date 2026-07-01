---
name: distill-permanent
description: "Distill a seed from 11b.Seeds/ into one or more atomic permanent notes in 11l.LtS/. Use when the user wants to distill, promote, or finalize a seed, or says 'distill this'. Proposes splits when a seed holds more than one idea, interrogates for gaps, plants forward-links, and updates MOCs. Won't pass the atomicity gate without a specific idea, not a broad topic."
---

# Distill a seed into permanent notes

This is the final gate: `capture-fleeting` → `seed-inbox` → **distill-permanent**. It takes a shaped seed from `11b.Seeds/` and promotes it to one or more permanent notes in `11l.LtS/`. Where capture is lossy (a missed thought is gone), distill is the opposite — a bad permanent note clutters the record you build on, so the bar is higher than at capture.

A permanent note is **atomic**: one idea, one gravitational center. Supporting material (examples, context, implications) orbits that center; a cluster or a tour of related thoughts is not atomic. If a seed holds multiple distinct ideas, it splits into multiple permanent notes, each atomic.

The agent is a meticulous editor — it proposes split points, challenges over-broad notes, grills for gaps, and plants forward-links to notes that should exist but don't. Not adversarial, but willing to push back with reasoning.

**Two paths reach `11l.LtS/`.** Path A: capture → seed-inbox → **this skill**. Path B: capture → concept-mine → `concept-refine` (writes permanent notes directly). Do not run this skill on `concept-refine` output unless the user explicitly asks — it already produces permanent notes. If you meet a `concept-refine` output that bundles multiple ideas (violates atomicity), alert the user; they split it or treat it as a deliberate exception.

The work runs in three phases — **plan** (step 3), **draft + interrogate** (step 4), **forward-link** (step 5) — then write, archive, and loop.

## Steps

### 1. Pick the seed

If the user specified a seed (by slug, keyword, or path), resolve it. Otherwise, list `11b.Seeds/` files with `status: seed` (excluding `_processed/`) and ask: "Which seed should I distill?"

**Done when** exactly one seed is identified.

### 2. Read and judge (ready-gate)

Read the seed in full. Route by its state:

- **`seed_level: project`** → stop immediately. Tell the user this seed belongs to a different workflow (not yet designed) and isn't distillable here. Exit.
- **Raw / quarry-style fragments** (from `concept-mine`, unshaped) → suggest `concept-refine` instead; this seed isn't shaped for distillation.
- **Shaped draft** (from `seed-inbox` or `concept-refine`) → proceed.
- **Thin or fuzzy** → present your best understanding of what the seed is trying to say, then ask: "Distill anyway, leave it, or route elsewhere?" Do not silently barrel through a half-baked seed.

**Done when** the seed passes the ready-gate (or the user overrides for a thin/fuzzy one).

### 3. Phase 1 — Plan

Map the seed into a distillation plan and present it for approval before writing anything.

#### 3a. Identify ideas and run the atomicity gate

Read the seed body. Identify distinct ideas. For each candidate note, apply the **atomicity gate**:

> *If someone reads only this note, what single thing will they understand?*

If the answer has an "and" in it, split. If the answer is a broad topic ("Machine Learning"), not a specific idea ("ML is a general term overused as a marketing shortcut"), push back — ask the user to name the specific claim. Challenges to use:

- "This feels like two notes — the X part and the Y part. Keep them combined and future-you searching for Y won't find it under X's summary. Split?"
- "That's a topic, not an idea. What's the specific claim?"

Do not proceed until each proposed note has a specific, narrow concept — named by the user, not just a territory.

#### 3b. Search for siblings

Grep the frontmatter (`tags`, `keywords`, `summary`) of every note under `11l.LtS/` (including subfolders) for keyword/tag overlap with each planned note. Surface the best candidates as proposed **siblings** — adjacent permanent notes at the same level.

#### 3c. Propose summaries, parents, tags, keywords

For each planned note, propose:

- **Summary** (3–5 sentences): concrete and self-contained, no cross-references ("as mentioned above"), no abstractions ("X is important"). Specific claims with concrete referents — "X matters because when Y happens, Z breaks in three specific ways," not "X is important." This is the scan-line for future-you *and* the embedding target for future vector search; it must be a standalone unit of meaning.
- **Parents** (wikilinks): domain MOCs, concept MOCs, or broader permanent notes that sit above this one in scope. A note can have multiple parents. Best guess, no approval gate — if it fits multiple MOCs, link both; if a concept MOC doesn't exist yet, plan to create it. A note with no parent is an **orphan** and is invalid.
- **Tags** (2–6): refine the seed's tags against a controlled vocabulary — standardize terms, drop noise, add tags the note earns once distilled. `11l.LtS/presale-glosary.md` is the existing model for a tag glossary.
- **Keywords** (3–5): precise search terms — what the user would grep to find this note later.
- **Slug**: pure keyword-slug, kebab-case, up to 6 words, no date prefix. Permanent notes are timeless; sortability comes from MOCs and graph links, not chronological naming.

#### 3d. Present the plan

Present the full plan as a structured outline — one section per proposed permanent note, with: slug, summary, parents, tags, keywords, siblings. Flag any splits and why. Flag any new MOCs to be created.

The user can reshape — merge, split differently, redirect parents, rename slugs, adjust summaries.

**Done when** the user approves the plan.

### 4. Phase 2 — Draft and Interrogate

Draft every permanent note from the approved plan, then interrogate across all of them in one batch.

#### 4a. Draft the notes

For each permanent note:

**Body** — transplant the relevant portion of the seed body (a split gives each note only its portion). Light editing for clarity. Add inline wikilinks to siblings and parents. If the seed body carries summary-like content (e.g. a "Claim" blockquote from `seed-inbox`), extract it into the frontmatter `summary` and **strip** it from the body — no duplication between frontmatter and body. The body starts clean where the idea unfolds.

**Frontmatter (7 fields):**
```yaml
---
status: permanent
source: "[[<relative path to archived seed in 11b.Seeds/_processed/>]]"
tags: [tag1, tag2, tag3]
keywords: [kw1, kw2, kw3]
summary: "Concrete, self-contained, 3–5 sentences. No cross-references. Specific claims with concrete referents. The scan-line future-you reads in 6 months to decide whether to go deeper."
parents: ["[[Parent MOC]]", "[[Broader permanent note]]"]
siblings: ["[[Adjacent note 1]]", "[[Adjacent note 2]]"]
---
```
- `status` — always `permanent`.
- `source` — wikilink to the archived seed in `11b.Seeds/_processed/` (set in step 6 once the seed is renamed; compute the correct relative path from the note's location).
- `tags` / `keywords` / `summary` / `parents` / `siblings` — as proposed in the plan.

**Placement** — flat at `11l.LtS/<slug>.md` by default. Place into an existing `11l.LtS/11lNN.<Domain>/` subfolder only when the note clearly belongs to one that already exists. Never create a new subfolder during distill; categories emerge organically from real notes, not upfront taxonomy.

#### 4b. Interrogate (batch, across all notes)

Grill the user about gaps across every drafted note — a persistent interview, not one polite question. Continue until the user says "enough."

**Standard questions (living list — run through these each time):**
1. "What's the counter-argument to this?"
2. "What's the simplest concrete example that proves this?"
3. "What would someone who disagrees say — and what would you say back?"
4. "What adjacent idea should be here but isn't?"
5. "If this note is wrong, what would prove it wrong?"
6. "What's the one sentence version?" (tests atomicity from the user's side)

**Content-driven gaps** — beyond the standard list, read each draft and surface gaps specific to it: a claim lacking an example, an argument skipping a step, a concept the note implies but doesn't unpack. Follow up on answers; push back on vague ones. The bar is: *would future-you, reading this note cold in 6 months, find it complete enough to act on?*

**Done when** the user says "enough" (or any end signal). Update the drafts with any new material from the interrogation.

### 5. Phase 3 — Forward-link

Plant inline `[[wikilinks]]` to notes that don't exist yet but should — **forward-links**, future distillation targets. Obsidian renders them as uncreated (dim) nodes in the graph — the visible frontier of what to explore next.

- **Key concepts first** — plant wikilinks for concepts that clearly deserve their own note: core dependencies, natural next-explorations, ideas the note leans on but doesn't explain.
- **Optional links** — propose up to 2 more that are interesting but less certain, gated through the user: "Also worth planting [[X]] and [[Y]]?" The user approves, rejects, or renames. Keep the graph navigable, not cluttered with dim-node noise.

Forward-links live inline in the body — the body is the planting ground. No separate frontmatter field.

**Done when** key forward-links are planted and optional ones are gated.

### 6. Write permanent notes, update MOCs, archive the seed

#### 6a. Write the permanent notes

Write each note to its resolved location (`11l.LtS/<slug>.md` or `11l.LtS/11lNN.<Domain>/<slug>.md`). If a slug collides with an existing note, append `-2` — never silently overwrite.

#### 6b. Update MOCs

For each parent MOC link in each note:

- Read the MOC. Find the H2 section where the note fits and append the wikilink as a bullet.
- No fitting section → create a new H2 section.
- The MOC doesn't exist yet → create it:
  ```markdown
  # [Concept] MOC

  ## [Section]

  - [[note one]]
  ```
- A note with multiple parent MOCs → update all of them.

Best guess throughout, no approval gate — the user sorts out misfires later. The cost of a misplaced MOC link is low (move it); the cost of an approval step is high (friction).

#### 6c. Archive the seed

1. Move the seed to `11b.Seeds/_processed/archived-<original-slug>.md` — the `archived-` prefix frees the original keyword-slug in case a permanent note wants it.
2. Update the moved seed's frontmatter: set `status: distilled`, add `permanent_note: "[[<relative path to the permanent note>]]"` (multiple wikilinks if the seed spawned several notes). Leave all other fields intact.
3. Set each permanent note's `source` field to the renamed seed path (compute the correct relative path from the note's location).

Never delete the seed — the provenance chain (capture → seed → permanent) is the vault's intellectual history.

**Done when** every permanent note exists in `11l.LtS/`, every relevant MOC is updated, and the seed sits in `11b.Seeds/_processed/` with `status: distilled` and a `permanent_note` backlink.

### 7. Loop or end

Surface adjacent work — topic-contiguous, not random-next-seed:

1. Read the `siblings` field of the just-written notes. If any sibling permanent notes exist, offer them: "We identified sibling notes [[X]] and [[Y]] during distillation. Want to explore one of those?"
2. Grep `11b.Seeds/` (excluding `_processed/`) for unprocessed seeds with keyword/tag overlap. If any, offer them: "There's a related seed — [[seed-slug]] — that touches the same topic. Distill it next?"

Ask: "Explore a sibling, distill a related seed, or done?"

On "done" (or any end signal), exit. Otherwise return to step 1 with the chosen seed.

**Done when** the user signals done.

## This skill never

Writes a permanent note without a specific, named idea — the atomicity gate is hard. Writes a note the user hasn't approved in the plan phase. Stops interrogating before the user says "enough". Deletes the seed (archive only). Creates a new `11l.LtS/` subfolder (place into an existing one only). Uses a date prefix in a permanent note filename. Silently passes a `seed_level: project` seed. Leaves a note an orphan (no parent link). Duplicates summary text between frontmatter and body. Runs on `concept-refine` output unless explicitly asked. Writes to `.memory/` or `.ai/`.
