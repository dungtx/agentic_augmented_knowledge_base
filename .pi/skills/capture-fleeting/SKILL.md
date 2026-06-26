---
name: capture-fleeting
description: Capture a fleeting note from a thought the user offloads. Use when the user dumps a raw fragment, jot, brain-dump, or one-liner to get it out of their head, or says capture / jot / note-down / dump this. If the message might be a question or request instead, ask one disambiguation question before acting. Supports live capture: the user keeps adding until an end signal, then clarification begins. Writes to 11a1.Inbox/ and loops.
---

# Capture a fleeting note

A **fleeting** note is a raw, perishable record of the user's own thought — the kind they dump before it leaks. Capture is **lossy**: a missed idea is gone, an extra note is deletable, so bias toward capturing and asking. This skill captures only; later skills classify, tag, link, and promote.

## Steps

### 1. Confirm capture intent

If the message is a raw fragment or names capture (jot / note-down / dump / capture this), treat it as a capture fragment. If the user asks for live capture, set mode = `live`; otherwise set mode = `normal`.

If it might instead be a question or request to you, ask exactly one disambiguation question — "Capture this, start live capture, or were you asking me something?" On a non-capture answer, **exit this skill** and treat the message as a normal question or request. Do not capture it.

**Done when** you are treating the message as a capture fragment in `normal` or `live` mode, unambiguously or after the one-question gate.

### 2. Live capture buffer, if requested

If mode = `normal`, skip to step 3.

If mode = `live`, treat the user's initial fragment as the first draft item unless it was only a command to start live capture. Then say: "Live capture started. Send more; type `end` when done."

For each user message until an end signal, append the content to the draft buffer and give only a short acknowledgement: "Added. Keep going, or type `end`." Do **not** ask clarifying questions, search the vault, summarize, or write a file during live capture.

End signals include `end`, `done`, `that's it`, `stop live capture`, and `finish capture`. When the user gives an end signal, proceed to step 3 using the accumulated draft.

**Done when** live capture has either been skipped or ended with an accumulated draft ready for clarification.

### 3. Jog the fragment clear

Use the accumulated live-capture draft if step 2 ran; otherwise use the initial fragment.

Ask clarifying questions **one at a time**, not as a batch. Each question must carry a **hint** to jog the user's memory. Build hints in this order, stopping at the first that yields something useful:

1. `rg` the vault for terms in the fragment; surface nearby note titles the user might be referring to.
2. Only if the vault has nothing, fall back to model knowledge.

Ask up to 3. Stop early only when no **load-bearing ambiguity** remains — a missing *what*, *why*, or *context* that would make the note unusable later. Do not invent questions to fill the budget.

If the user signals "enough" or "just write it", stop immediately.

**Done when** 3 are answered, the user signals stop, or no load-bearing ambiguity remains — whichever first.

### 4. Write the fleeting note

Write to `11a1.Inbox/` only.

If the collected material holds multiple clearly-separate fragments, ask the user: "These look like N fragments — N notes, or one?" and obey. Keep a routine or one multi-step thought as a single note.

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
Set `needs_review: true` if step 3 ended by budget exhaustion or user stop before clarification was complete.

Body: the fragment in the user's voice, lightly cleaned (fix typos; expand abbreviations only if obvious). Preserve live-capture details unless they are duplicate or purely procedural. Do **not** insert `[[wikilinks]]`.

Preview the full note in chat; write the file only on the user's "yes" (or after their tweak).

**Done when** the file exists at the path above with the user-approved body and frontmatter.

### 5. Loop or end

Ask one short prompt: "Another fragment, live capture, or done?"

On "done" (or any end-of-session signal), exit. Otherwise return to step 1 with the next fragment.

**Done when** the user signals done.

## This skill never

Promotes a fleeting to a permanent note. Triages Inbox into Deferred or Someday. Adds tags beyond `[]`. Inserts `[[wikilinks]]`. Touches the spaced-repetition plugin or any review schedule. Writes outside `11a1.Inbox/`. Appends to `.memory/` or `.ai/`.