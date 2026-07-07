---
name: morning-review
description: "Consent-first Inbox triage with cross-lane surfacing. Use when the user says start my day, morning, triage inbox, triage, or wants to sort their Inbox. Groups Inbox items by topic, surfaces related Deferred/Someday items as context, and asks one decision per item. Never auto-fires — always asks for consent first."
---

# Morning review — Inbox triage

The Inbox accumulates raw captures. This skill processes the backlog: for each item, decide whether it's important-now (keep in Inbox for seeding), important-later (promote to `11a2.Deferred/`), nice-to-have (park in `11a3.Someday/` for future resurfacing), ready-to-process (hand off to `seed-inbox`), or no longer relevant (discard).

The value-add is **cross-lane surfacing**: when you look at an Inbox item about Japanese practice, the skill also shows you the Japanese items already in Deferred and Someday — so you see the full picture before deciding.

This skill fires **only with consent**. It never auto-hijacks a session.

## Steps

### 1. Count and ask consent

Read `11a.Capture/11a1.Inbox/` (files with `status: fleeting`, excluding `_processed/`). Count them.

- If **0**: say "Inbox is empty." Exit.
- If **> 0**: present the count and a one-line summary of what's there (inferred topics from filenames and body previews). Then ask: "Run morning-review?"

Example: "3 items in Inbox — a presales deal note (CDI), an Android app idea for Japanese practice, and an emergency bid context. Run morning-review?"

**Done when** the user says yes (proceed to step 2) or no (exit).

### 2. Group by topic and surface cross-lane items

Read each Inbox item in full. Infer a topic label for each (best-effort from body — look for domain signals: presales, AI, Japanese, career, habit, etc.). Group items with overlapping topics.

For each group, search `11a.Capture/11a2.Deferred/` and `11a.Capture/11a3.Someday/` for related items. Search by:
- Grep for the topic label and related keywords in filenames and body text
- Also check any tags or keywords in the frontmatter of Deferred/Someday items

Record the cross-lane matches per group. If none found, note that too — it's useful signal ("this is new ground").

**Done when** every Inbox item is assigned to a topic group, and each group has its cross-lane matches identified.

### 3. Triage each group (one at a time)

For each topic group, present:

```
## <topic label>

**Inbox:**
- `<filename>` — <one-line body preview>

**Related:**
- Deferred: <list or "none">
- Someday: <list or "none">
```

Then ask for each Inbox item: **"Deferred, Someday, seed now, keep, or discard?"**

| Decision | What happens |
|----------|-------------|
| **Deferred** | Important, not urgent. Move to `11a2.Deferred/`. Archive Inbox original. |
| **Someday** | Nice-to-have. Park in `11a3.Someday/` for future resurfacing. Archive Inbox original. |
| **Seed now** | Ready to process. Hand off to `seed-inbox` skill (this skill does NOT seed — tell the user to run seed-inbox next). Keep in Inbox for now. |
| **Keep** | Not ready to decide. Leave in Inbox. |
| **Discard** | No longer relevant. Archive to `_processed/` with `status: discarded`. |

If the user picks "seed now," flag it and move on — do not run seed-inbox inline. At the end of triage, remind the user which items are marked for seeding.

Process one group fully before moving to the next. Ask decisions for one item at a time if the group has multiple Inbox items.

**Done when** every Inbox item has a decision.

### 4. Execute decisions

For each decided item, apply the move:

**Deferred / Someday:**
- Write the item to the target lane with the original filename
- Update frontmatter:
  ```yaml
  status: deferred  # or someday
  triaged_at: <now, ISO 8601 +07:00>
  ```
  Keep `kind`, `captured_at`, and any other fields from the original.
- Archive the original Inbox file to `11a1.Inbox/_processed/<original-filename>.md`
- Update the archived file's frontmatter: add `triaged_to: "[[../../<target-lane>/<filename>.md]]"` and set `status: triaged`

**Discard:**
- Archive the Inbox file to `11a1.Inbox/_processed/<original-filename>.md`
- Update the archived file's frontmatter: set `status: discarded`, add `discarded_at: <now, ISO 8601 +07:00>`
- Do NOT delete the file

**Keep / Seed now:**
- Do not move. For "seed now," record the filename for the end-of-session reminder.

**Done when** all files are written to their target locations and all archived originals have updated frontmatter.

### 5. Summary and seed reminder

Report what happened:

```
Morning review done.
- → Deferred: <count> (<filenames>)
- → Someday: <count> (<filenames>)
- Discarded: <count> (<filenames>)
- Kept in Inbox: <count> (<filenames>)
```

If any items were marked "seed now," add: "Ready to seed: <filenames>. Run seed-inbox when you're ready."

**Done when** summary is delivered.

## This skill never

Auto-fires without explicit consent (D14, W7). Classifies at capture time — capture is already done. Seeds an Inbox item (that's `seed-inbox`). Writes to `11b.Seeds/` or `11l.LtS/`. Hard-deletes any file (archive only). Creates new lanes or subfolders. Writes to `.memory/` or `.ai/`. Re-triages existing Deferred/Someday items (this skill triages Inbox only). Tags items during triage (tags are assigned at seed/distill time, not triage time). Makes decisions for the user — every item gets an explicit user choice.
