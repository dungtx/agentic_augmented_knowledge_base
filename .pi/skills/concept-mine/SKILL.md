---
name: concept-mine
description: "Mine fragments around a central concept (a lens or question). Use when the user wants to develop their thinking on a concept before imposing structure — a tighter version of writing-fragments where all material orbits one gravitational center. Stray thoughts are recorded, not rejected; concept-refine handles drift later."
---

# Mine fragments around a central concept

This is a structured grilling session that mines raw writing fragments, all orbiting a single **central concept** — a lens the user wants to think through, or a question they want to explore. The concept anchors the conversation; fragments that drift are still recorded (marked), because thinking wanders and drift itself is data. The paired skill `concept-refine` later filters and refocuses.

This skill is for **thinking through writing**, not for producing publishable prose. The output is a quarry file, not a draft.

## Steps

### 1. Get the central concept

If the user already stated a concept, restate it back for confirmation: "Your central concept is ___ — correct?" If the user hasn't stated one yet, ask:

"Pick a central concept — a lens to think through or a question to explore. Examples: 'software as gardening', 'what would it take to never touch a mouse again?', 'accumulation as a design force'. The concept stays in view but can evolve as your thinking does."

**Done when** the user confirms a concept in their own words. Write it down; you will pin it at the top of the fragment file.

### 2. Get the output path

If the user did not specify where to save, ask once and remember it. Default to `11b.Seeds/<concept-slug>-fragments.md` where `concept-slug` is a 3–5 word kebab-case version of the concept.

**Done when** a path is known.

### 3. Run the grilling session

Interview the user relentlessly about the concept. Do not impose phases, outlines, or structure. The concept is a gravitational center, not a cage — let the user's thinking orbit at whatever distance it naturally takes.

Your job in the conversation:
- Keep returning to the concept: "How does this connect back to ___ ?"
- Follow threads the user opens, even if they seem tangential
- When the user makes a claim, ask for the concrete example behind it
- When the user gives an example, ask what principle it illustrates
- When the user is stuck, offer a counter-lens or adjacent question to provoke

**Done when** the user signals they're done mining (see step 5), or when the conversation naturally exhausts.

### 4. Capture fragments to the file

As fragments emerge, append them to the output file. Re-read the file from disk before every write — the user may edit between turns.

#### File format

```markdown
# Fragments: [central concept]

> Concept: [the concept pinned at step 1, in the user's own words]
> This is raw quarry material. Drift is expected and marked. concept-refine will filter.

---

A fragment that connects tightly to the concept.

---

Another fragment, this one circling the concept from a different angle.

---

[drift] A thought that wandered — recorded because it might matter later, or might reveal
something about why the concept is hard to hold still.

---

A sharp sentence the user wants deployed somewhere but doesn't yet know where.
```

Rules:
- H1 at the top: `# Fragments: [central concept]`
- Concept pinned in a blockquote right after
- Fragments separated by `---`
- Stray/drifting fragments prefixed with `[drift]` on their first line
- No headings inside the body. No tags. No order beyond addition order.

#### Writing rhythm

- Append silently. Mention what you added in passing ("adding that"), don't interrupt the conversation with save dialogs.
- Before every write: re-read the file from disk. The user may have edited between turns — preserve their changes.
- Never overwrite the file; only append (or edit a specific fragment in place if the user asks).
- The user can say "cut the last one", "rewrite that sharper", "merge those two" at any time. Treat those as first-class instructions.

**Done when** fragments accumulate in the file across the session.

### 5. Loop or end

The grilling continues until the user signals they're done. Signals include: "done", "that's enough", "let's move to refine", "stop", or any explicit end. Do not decide the session is done unless the user says so.

When the user signals end, say: "Fragments saved to `<path>`. Run `concept-refine` when you're ready to shape these into a focused piece."

Exit the skill.

**Done when** the user signals end.

## This skill never

Rejects a fragment for drifting — drift is data, record it. Filters or refocuses fragments (that's `concept-refine`). Imposes an outline, structure, or narrative arc. Decides the session is over without user signal. Writes to `11l.LtS/` (this is raw quarry, not permanent notes). Inserts `[[wikilinks]]`. Tags or classifies fragments.
