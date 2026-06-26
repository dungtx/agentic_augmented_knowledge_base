---
name: capture-fleeting
description: Capture a fleeting note from a thought the user offloads. Use when the user dumps a raw fragment, jot, brain-dump, or one-liner to get it out of their head, or says capture / jot / note-down / dump this. If the message might be a question or request instead, ask one disambiguation question before acting. Asks clarifying questions one at a time with hints to jog memory, writes to 11a1.Inbox/, then loops for the next fragment.
---

# Capture a fleeting note

A **fleeting** note is a raw, perishable record of the user's own thought — the kind they dump before it leaks. Capture is **lossy**: a missed idea is gone, an extra note is deletable, so bias toward capturing and asking. This skill captures only; later skills classify, tag, link, and promote.

## Steps

### 1. Confirm capture intent

If the message is a raw fragment or names capture (jot / note-down / dump / capture this), go to step 2.

If it might instead be a question or request to you, ask exactly one disambiguation question — "Capture this, or were you asking me something?" — and proceed only on a capture answer.

**Done when** you are treating the message as a capture fragment, unambiguously or after the one-question gate.

### 2. Jog the fragment clear

Ask clarifying questions **one at a time**, not as a batch. Each question must carry a **hint** to jog the user's memory. Build hints in this order, stopping at the first that yields something useful:

1. `rg` the vault for terms in the fragment; surface nearby note titles the user might be referring to.
2. Only if the vault has nothing, fall back to model knowledge.

Ask up to 3. Stop early only when no **load-bearing ambiguity** remains — a missing *what*, *why*, or *context* that would make the note unusable later. Do not invent questions to fill the budget.

If the user signals "enough" or "just write it", stop immediately.

**Done when** 3 are answered, the user signals stop, or no load-bearing ambiguity remains — whichever first.

### 3. Write the fleeting note

Write to `11a1.Inbox/` only.

If the message holds multiple clearly-separate fragments, ask the user: "These look like N fragments — N notes, or one?" and obey. Keep a routine or one multi-step thought as a single note.

Filename: `YYYYMMDDHHmm-slug.md`, timezone `+07:00`, slug = 3–6 kebab-case words from the fragment's core idea. Increment the minute per note when writing several in one pass.

Frontmatter — exactly these fields:
```
---
status: fleeting
captured_at: <ISO 8601, +07:00>
tags: []
needs_review: false
---
```
Set `needs_review: true` if step 2 ended by budget exhaustion or user stop before clarification was complete.

Body: the fragment in the user's voice, lightly cleaned (fix typos; expand abbreviations only if obvious). Do **not** insert `[[wikilinks]]`.

Preview the full note in chat; write the file only on the user's "yes" (or after their tweak).

**Done when** the file exists at the path above with the user-approved body and frontmatter.

### 4. Loop or end

Ask one short prompt: "Another fragment, or done?"

On "done" (or any end-of-session signal), exit. Otherwise return to step 1 with the next fragment.

**Done when** the user signals done.

## This skill never

Promotes a fleeting to a permanent note. Triages Inbox into Deferred or Someday. Adds tags beyond `[]`. Inserts `[[wikilinks]]`. Touches the spaced-repetition plugin or any review schedule. Writes outside `11a1.Inbox/`. Appends to `.memory/` or `.ai/`.