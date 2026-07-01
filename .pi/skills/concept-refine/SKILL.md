---
name: concept-refine
description: "Shape a fragment quarry into a focused, concept-driven piece, beat by beat. Reads fragments mined by concept-mine and refocuses them around the central concept — rejecting or reframing beats that weaken the piece. Asks for clarification on weak connections, proposes reframes, and skips if the user says no. Like writing-beats but with a quality filter: every beat must earn its connection to the concept."
---

# Refine fragments into a concept-driven piece

This skill takes a fragment quarry (from `concept-mine`) and shapes it into a focused piece, beat by beat, with the central concept as a quality gate. Every beat must earn its place — the agent pushes back on drift, asks for clarification, proposes reframes, and skips beats the user can't connect.

The output is a draft in `11b.Seeds/` — not yet a permanent note, but a workable piece ready for `distill-permanent` or further refinement.

## Steps

### 1. Locate the fragment file and confirm the concept

If the user specified a path, read it. Otherwise, ask: "Which fragment file should I refine?" List candidates in `11b.Seeds/` that look like quarry files (contain `# Fragments:` H1).

Read the file. Extract the central concept from the pinned blockquote. Confirm with the user: "Your concept was ___ — still right, or has it evolved during mining?"

If the concept evolved, update it. The concept may sharpen, shift, or fork — the fragment file is evidence of thinking, and the concept should reflect where the user ended up, not just where they started.

**Done when** a fragment file is read and the concept is confirmed (or updated).

### 2. Propose starting beats

Re-read the fragment file. Identify 2–3 candidate **starting beats** — each a different entry point into the piece, drawn from fragments that connect tightly to the concept.

For each candidate beat, state:
- The fragment(s) it draws from
- How it connects to the concept (one sentence)
- Where it might lead (a preview of the next 1–2 moves)

Do not write any beat yet. Let the user pick.

**Done when** the user chooses a starting beat.

### 3. Write the chosen beat

Re-read the fragment file and the article file (if it exists) from disk. Write **only the chosen beat** to the output file. Do not write the next beat.

A beat does one move — sets a scene, lands a point, asks a question, drops an aside, twists the angle. It stops at a place where the next beat can pivot. Size: a sentence to a few paragraphs. If a "beat" needs five paragraphs and three subheadings, split it.

Pull material from the fragment quarry. Paraphrase, split, recombine, or quote.

**Done when** the beat is written to disk.

### 4. Propose next beats with concept gate

Re-read the article file from disk. Re-read the fragment file. Then propose 2–3 candidate **next beats** — different directions the piece could pivot to.

For each candidate, run the **concept gate**:

1. **Assess connection.** Does this beat earn its connection to the central concept, or is it drifting? A beat can approach the concept from an unexpected angle — that's fine. But it must visibly connect, not just be adjacent.

2. **If connection is strong:** Propose it normally with a one-line connection statement.

3. **If connection is weak or unclear:** Flag it explicitly. "This beat pulls away from the concept — it's about [X] while the concept is [Y]. Want to clarify how it connects, or should I try a reframe?"

4. **If the user clarifies:** Ask follow-ups until the connection is visible, then propose the beat (or a revised version).

5. **If the user says "reframe it":** Propose a version of the same beat that re-angles it toward the concept. Present the reframe, then ask: "Does this version earn its place?"

6. **If the user says "skip it":** Drop that candidate entirely. Offer the remaining candidates (replenishing to 2 if needed).

Do not write a beat whose connection the user cannot articulate. The quality bar is: *the user can explain, in their own words, how this beat serves the concept.* If they can't, skip it — the piece is stronger without it.

**Done when** the user chooses a beat that passes the concept gate.

### 5. Loop until natural end

Loop steps 3–4 until the piece reaches a natural end. An end is not "the quarry is empty" — leftover fragments are normal. An end is when:
- The user says "that's the end" or "it feels done"
- Beats have addressed the concept from enough angles that adding more would dilute
- The user signals they want to stop and move on

Preserve user edits absolutely. Re-read the article file from disk before every write. If the user edits a previous beat substantially, let it change what comes next. If the user says "rewrite that beat" or "go back and try a different beat 3", edit in place and leave the rest alone.

**Done when** the user signals the piece is complete.

### 6. Write the permanent note

Write the final piece directly to `11l.LtS/<slug>.md` as a permanent note. concept-refine produces permanent notes, not seeds — its output goes straight to LtS.

**Frontmatter (7 fields):**
```yaml
---
status: permanent
source: "[[<quarry-file-path>.md]]"
tags: [tag1, tag2, tag3]
keywords: [kw1, kw2, kw3]
summary: "Concrete, self-contained summary. 3–5 sentences. The concept distilled into a scan-line."
parents: ["[[Relevant MOC]]"]
siblings: []
---
```
- `source` points to the concept-mine quarry file (the original fragment pile)
- `summary` is the concept-driven piece distilled into a concrete scan-line
- `parents` links to the most relevant MOC(s) — best guess, user can adjust later
- `tags` and `keywords` drawn from the concept and the piece's content

**Naming:** pure keyword-slug, kebab-case, up to 6 words. No date prefix.
**Placement:** flat in `11l.LtS/`.

**Done when** the permanent note exists at `11l.LtS/<slug>.md`.

## This skill never

Writes a beat without user choice. Accepts a beat the user can't connect to the concept. Imposes structure the user hasn't chosen. Treats the quarry as a todo list to exhaust. Writes outside `11l.LtS/` for the final output. Writes to `11b.Seeds/` (that's for seeds; concept-refine produces permanent notes directly).
