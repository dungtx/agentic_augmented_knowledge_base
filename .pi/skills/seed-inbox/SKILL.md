---
name: seed-inbox
description: "Promote an Inbox note to a workable seed in 11b.Seeds/. Use when the user wants to process / seed / promote an inbox item, turn a fleeting note into a rough draft, or clear the inbox. Reads the raw fragment, drafts a rewritten seed with fresh perspective, enriches frontmatter, and archives the original."
---

# Seed an Inbox note

Capture writes raw fragments to `11a1.Inbox/`. This skill promotes one into a **seed** — a workable rough draft in `11b.Seeds/` that can be refined later into a permanent note. The agent does substantive drafting (not just metadata annotation): it rewrites the fragment from a fresh perspective, infers best-guess enrichment, and only asks you for genuinely ambiguous gaps.

A seed is NOT a zettelkasten permanent note. It is deliberately unfinished — `seed_level` tracks the remaining effort (`10min`, `1hour`, `project`). The eventual `distill-permanent` skill will promote seeds to `11l.LtS/`.

## Steps

### 1. Pick the Inbox note

If the user specified a note (by slug, keyword, or "the CDI one"), resolve it. Otherwise, list the current Inbox (`11a1.Inbox/` files with `status: fleeting`) and ask: "Which note should I seed?"

**Done when** exactly one Inbox note is identified.

### 2. Draft the seed

Read the selected Inbox note in full. Then draft a best-effort seed with the shape determined by `kind`:

**For `kind: idea` or `kind: lit-note` — Shape A (restatement + expansion):**
```
## Claim
> [One sentence — your take on the core idea, sharper than the capture]

[Body: rewrite the fragment in your own words. Flesh out implications the user may not have written down.
Connect to domains and concepts from model knowledge and the vault. The result reads like a short blog-post
stub — what this is, why it matters, where it fits.]

## Keywords
kw1, kw2, kw3
```

**For `kind: task` or `kind: routine` — Shape C (contextualised brief):**
```
## Situation
[What triggered this? What's the context?]

## Key insight
[The actionable takeaway — what matters and why now]

## Unknowns
[What's still unclear or needs discovery]

## Next actions
[Concrete steps; each actionable]

## Keywords
kw1, kw2, kw3, kw4, kw5
```

Enrich the frontmatter with best guesses for everything you can infer. Draft the slug from the keywords (kebab-case, 3–5 words). Do everything you can before showing the user — this is a **best-effort first pass**, not a skeleton.

**Inferred frontmatter (make best guesses):**
```yaml
status: seed
kind: <corrected from capture default if wrong; idea|task|routine|lit-note>
seed_level: <10min|1hour|project — your estimate of remaining effort to make it permanent-ready>
captured_at: <carried forward from original>
seeded_at: <now, ISO 8601 +07:00>
source: "[[../11a.Capture/11a1.Inbox/_processed/<original-filename>.md]]"
tags: [<2–4 tags from a controlled, consistent vocabulary>]
keywords: [<3 for idea/lit-note, 5 for task/routine — the terms the user would search to find this later>]
```

Slug: kebab-case from the top keywords (e.g. `co2-ai-verification-gates`). Up to 6 words.

**Done when** a complete draft (body + frontmatter + proposed slug) is ready to present.

### 3. Review with the user

Present the draft in chat with a quick summary of what you decided:
- What you set `kind` and `seed_level` to, and why
- Which tags and keywords you picked
- The proposed slug
- A one-line signal if anything was genuinely ambiguous

Then ask ONE question covering only genuinely ambiguous gaps (if any). Do not manufacture questions to fill a budget. If nothing is ambiguous, skip straight to approval: "Look good? I'll write it."

If the user gives feedback, apply it and re-present the affected parts. Do not re-present the whole draft unless the user asks.

**Done when** the user approves the draft (explicit "yes", "looks good", "write it", or equivalent).

### 4. Write the seed + archive the original

Write the approved seed to `11b.Seeds/<slug>.md`. If the file exists, append `-2` to the slug (do not silently overwrite).

Then archive the original Inbox file:
- Move it to `11a1.Inbox/_processed/<original-filename>.md`
- Update the moved file's frontmatter: set `status: seeded` and add a `seed: "[[../../11b.Seeds/<slug>.md]]"` field pointing back to the seed
- Leave all other frontmatter fields intact

**Done when** the seed file exists at `11b.Seeds/<slug>.md` AND the original exists at `11a1.Inbox/_processed/<original-filename>.md` with `status: seeded` and a `seed:` wikilink.

### 5. Loop or end

Ask: "Seed another, or done?"

On "done" (or any end signal), exit. Otherwise return to step 1.

**Done when** the user signals done.

## Reference

### Keyword budget
- **3 keywords** for `kind: idea` or `kind: lit-note`
- **5 keywords** for `kind: task` or `kind: routine`

### seed_level meanings
- `10min` — a quick polish pass is enough; the idea is nearly clear
- `1hour` — needs a focused sit-down to shape
- `project` — needs research, multiple sessions, or external input before it's permanent-ready

### Shape B (interrogation-in-writing) — deferred
If the user asks for shape B during review, note that it is planned for a future skill and offer to do it as a conversation instead (ask the open questions directly rather than writing them into the draft). Do not implement shape B inline.

## This skill never

Promotes a seed to a permanent note in `11l.LtS/` (that's `distill-permanent`). Writes outside `11b.Seeds/`. Hard-deletes the original Inbox file (archive only). Classifies at capture time — capture is already done when this skill runs. Tags with more than 6 or fewer than 2. Generates a slug longer than 6 words. Asks more than one clarifying question per review. Runs shape B (interrogation-in-writing) inline. Touches `11a2.Deferred/` or `11a3.Someday/`. Writes to `.memory/` or `.ai/`.
