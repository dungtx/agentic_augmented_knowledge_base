---
name: project-retro
description: "Close a project and run a retrospective. Auto-retro on close writes a draft retro.md with summary, identified points, and remaining questions. On-demand deep retro grills across 6 phases and distills permanent lessons to 11l.LtS/. Use when user says close project, retro on project X, or wrap up project."
---

# Project retro

Closes a project and captures lessons. Two modes: **auto-retro** (lightweight, fires on close) and **deep retro** (on-demand, full grilling with permanent-note distillation).

## Steps — auto-retro (on close)

Triggered by "close project X" or when README status changes to `closed`.

### 1. Read all project material

Read everything in `11c.Projects/<ProjectName>/`:
- `README.md`
- All `.md` notes in the project folder
- All archived Inbox items listed in those notes' frontmatter (follow `source` wikilinks back to `11a1.Inbox/_processed/`)

Build a timeline of events from dated entries (README status log, file creation dates, capture timestamps in archived Inbox items).

### 2. Write the retro draft

Create `11c.Projects/<ProjectName>/retro.md`:

```yaml
retro_type: auto
created: <today, YYYY-MM-DD>
deep_retro_done: false
```

Body:

```
# Retro — <ProjectName>

## Project summary
<3-5 sentences: what the project was, what we delivered, how it ended. Factual, not evaluative.>

## What I noticed
<Bullet list of major points the agent can identify from the project material:
- Patterns: recurring issues, things that kept coming up
- Gaps: things that were flagged but never resolved
- Surprises: status log entries that indicate unexpected turns
- Decisions: key choices and their visible consequences
- Strengths: what clearly worked based on the record
Keep each to one line. Don't reach — only surface what's visible in the material.>

## Questions for deeper retro
<Bullet list of open questions the material raises but can't answer. Each should invite reflection:
- "What was the root cause of X?"
- "If you could redo Y, what would you do differently?"
- "What did you learn about Z that you didn't know before?"
Aim for 5-10. These become the starting points for a deep retro session.>

## Your notes
<_Leave this section blank with a prompt:_>
<!-- Add your own reflections here — stream of thoughts, feelings about the project, what happened from your POV. I'll parse it into structured form when you run deep retro. -->
```

Present the draft to the user. If they want to add stream-of-thought reflections now, take them and append to the "Your notes" section. If they defer, leave the prompt in place.

### 3. Close the project

Update `README.md` frontmatter:
```yaml
status: closed
closed: <today, YYYY-MM-DD>
```

Add a status log entry: "Project closed. Auto-retro written."

**Done when** README is updated, `retro.md` exists, and user has seen the draft.

---

## Steps — deep retro (on demand)

Triggered by "retro on project X" or "deep retro on project X." Can run on any project (open or closed).

### 1. Load existing material

Read `retro.md` if it exists (auto-retro draft or previous deep retro). If not, run auto-retro step 1 first to gather the base material.

Also read the user's stream-of-thought notes from `retro.md` "Your notes" section if present. Parse them — extract claims, observations, feelings, and questions. These are first-class input, not decoration.

### 2. Grill phase by phase

Walk through these phases in order. Ask one question at a time. After each phase ask "Next phase or done?"

**Phase 1 — What happened**
Start from the timeline. Ask: did anything major happen that's not in the record? Were there turning points? What was the emotional arc — when were you confident, when were you worried?

**Phase 2 — What went wrong**
Failures, near-misses, surprises. Push for specifics: not "communication was bad" but "the handoff between X and Y broke because Z." What was the cost of each?

**Phase 3 — Why**
Root causes. For each failure from phase 2: why did it happen? Was it a one-off or systemic? What early signal did we miss? What assumption turned out wrong?

**Phase 4 — What to keep**
Things that worked and should be repeated. Tools, patterns, decisions, habits. What saved us? What would you absolutely do again?

**Phase 5 — Redo priorities**
If starting this project fresh tomorrow, knowing what you know now: what must be set up first? What would you skip? What order would you do things in?

**Phase 6 — Permanent lessons**
From everything above: what belongs in `11l.LtS/` so future projects can find it? Each lesson must be specific ("Always do X before Y when Z is true"), not generic ("communication matters").

**Stop conditions:** user says "done" at any time. Remaining phases become open questions in `retro.md`.

### 3. Write permanent notes

For each lesson identified in phase 6, write a permanent note to `11l.LtS/`. Follow permanent-note conventions:
- Full 7-field frontmatter (`status: permanent`, `source` wikilink to `retro.md`, `tags`, `keywords`, `summary`, `parents`, `siblings`)
- Keyword-slug filename, no date prefix
- Source links back to the project's `retro.md`

Present each note for approval before writing. One at a time.

For notes that clearly belong to an existing `11lNN.<Domain>/` subfolder, place them there. Otherwise flat in `11l.LtS/`.

### 4. Update retro.md

Update `retro.md` frontmatter:
```yaml
retro_type: deep
deep_retro_done: true
deep_retro_date: <today, YYYY-MM-DD>
```

Append under the auto-retro content:

```
## Deep retro — <date>

### What happened
<summarize phase 1 answers>

### What went wrong
<summarize, with root causes from phase 3 linked>

### What to keep
<summarize>

### Redo priorities
<summarize>

### Permanent notes created
- [[note-1]]
- [[note-2]]
```

If phases were skipped, add an "## Open questions" section listing what wasn't covered.

### 5. Done

Report: "Deep retro complete. `retro.md` updated. N permanent notes written to `11l.LtS/`."

If phases remain: "Uncovered phases saved as open questions in `retro.md`."

---

## This skill never

Blames individuals — focus on systems, decisions, patterns. Invents lessons the user didn't say. Fills in missing phases with guesses. Writes permanent notes without approval. Creates new `11l.LtS/` subfolders. Deletes project files (closed projects stay in place).
