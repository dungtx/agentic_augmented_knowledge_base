---
name: project-kickoff
description: "Kick off a new project from related Inbox items. Grills the user one category at a time to extract everything they know, then generates a project README and initial notes. Use when morning-review surfaces a project cluster, or the user says start project, kick off project, or create project for X."
---

# Project kickoff

Kicks off a new project in `11c.Projects/` from Inbox clues. Replaces `seed-inbox` for project-bound items — the project pipeline is separate from the capture → seed → permanent pipeline.

## Steps

### 1. Gather Inbox items and present summary

If invoked from `morning-review`, the items are already identified. Otherwise, ask the user which Inbox items belong, or scan `11a1.Inbox/` for filenames/body mentions of the project name.

Read every related Inbox item in full. Synthesize a summary:

```
## Project: <name>

**From your Inbox (N items):**
- <bullet-list of what each item says, in plain language>

**What I can infer:**
- Client/domain: <best guess>
- What they want: <best guess>
- Our role: <best guess>
- Known gaps: <what's clearly missing>

Starting point look right? Anything to add or correct before we dig in?
```

Wait for the user to confirm or amend. If they add new info, fold it in and re-confirm.

**Done when** the user says "go ahead" or signals readiness.

### 2. Grill category by category

Walk through these categories in order. For each, ask open-ended questions derived from the Inbox clues. After each category, ask "Next category or done?"

**Categories (ask in this order):**

1. **Client & domain** — what they do, industry, size, what problem they solve. What's their current AI maturity (bottom-up experiments? nothing?). What's the real reason they're talking to us?

2. **Engagement** — what's the scope? What are we being asked to do? Stages, deliverables, timeline. Our role vs. their team's role. Who does what?

3. **Technical landscape** — their stack, tooling, constraints. Known gaps or pain points. What systems would our work touch?

4. **People & politics** — champion, decision-maker, blockers. Internal dynamics that help or hurt. Who has skin in the game?

5. **Risks & unknowns** — what could go wrong? What don't we know yet? What assumptions are we making?

**Question rules:**
- Ask one at a time. Wait for each answer before the next.
- Derive questions from the Inbox clues — don't ask generic template questions.
- Ask delivery-side questions you can likely answer. For sales-side questions (budget, competitor intel, deal timeline), ask starter questions ("Do you happen to know X?") — but if user answers "don't know" to most, say "I'll flag these as ask-sales" and move on. Do not dwell.
- The blindspot pass: after all categories, ask one final round: "Is there anything about this project you haven't thought about that I should raise?" — one chance for the user to surface something the categories missed.

**Stop conditions:**
- User says "done" or "enough" at any time → proceed to step 3.
- All categories completed with user consent → proceed to step 3.

**Done when** the grilling ends (user stop or categories exhausted).

### 3. Generate project files

Create `11c.Projects/<ProjectName>/README.md` with:

```yaml
project: <ProjectCode-ClientSlug>
client: <codename>
status: bid
started: <today, YYYY-MM-DD>
```

Body: synthesize the grilling answers into:
- **Customer goal** — one paragraph
- **Engagement** — scope, stages, deliverables
- **Technical landscape** — key constraints, gaps
- **People** — champion, decision-makers (codename only)
- **Risks & open questions** — what we know we don't know
- **Status log** — single entry: "Project kicked off"

Create scattered initial notes alongside the README — one `.md` file per distinct topic that emerged in grilling that deserves its own space (e.g., `technical-constraints.md`, `stakeholder-map.md`). Use readable kebab-case filenames, no date prefix. Keep notes sparse — capture only what the user said, don't invent.

Present the README and all notes to the user for approval. Make edits on request, re-preview, then write only on final "yes."

**Stopped early:** If step 2 ended before all categories were covered, also write remaining questions to `.ai/projects/<ProjectName>/remaining-questions.md`:

```markdown
# Remaining questions — <ProjectName>

_Generated <date>. These categories were not covered or partially covered._

## <Category>
- [ ] <question>
- [ ] <question>
```

This file is for future agents to pick up. Tag it clearly so a later session can resume.

**Done when** all files exist at their paths with user-approved content.

### 4. Archive Inbox items

For each Inbox item that fed this kickoff:
- Archive the original to `11a1.Inbox/_processed/<original-filename>.md`
- Update archived frontmatter:
  ```yaml
  status: triaged
  triaged_to: "[[../../11c.Projects/<ProjectName>/README.md]]"
  triaged_at: <now, ISO 8601 +07:00>
  ```
- Do NOT delete the file. Provenance chain intact.

**Done when** all source Inbox items are archived with correct frontmatter.

### 5. Done

Report: "Project <ProjectName> kicked off. README + <N> notes written. <M> Inbox items archived."

If remaining questions exist, add: "Incomplete categories saved to `.ai/projects/<ProjectName>/remaining-questions.md` — resume with 'work on project <ProjectName>' to continue."

## Project naming

Derive `<ProjectName>` from the bid code or client codename. Pattern: `<BidCode>-<ClientSlug>` (e.g., `BGB26195-CDI`, `BJP26110-RIC`). **Always ask the user for the bid code** during kickoff — if one exists, the folder must use it. If no code exists yet, use the client slug alone and the user will rename when the code is assigned. Kebab-case, no spaces.

If `11c.Projects/<ProjectName>/` already exists: this is a resume, not a new kickoff. Load `.ai/projects/<ProjectName>/remaining-questions.md` if present and continue from where the last session stopped.

## This skill never

Asks sales-only questions after the user signals "I don't know" twice in that category. Creates projects without user consent on the README. Deletes Inbox items (archive only). Writes outside `11c.Projects/` and `.ai/projects/`. Generates content the user didn't say (no inventions — if user said "not sure about X," write "Not yet known" not a guess).
