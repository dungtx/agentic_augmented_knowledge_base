---
status: seed
kind: task
seed_level: 1hour
captured_at: 2026-06-26T16:41:06+07:00
seeded_at: 2026-06-29T09:58:00+07:00
source: "[[../11a.Capture/11a1.Inbox/_processed/202606261641-technical-interview-prep-playbook.md]]"
tags: [interviews, career, agents, workflow]
keywords: [interview-prep, agent-assisted, story-frameworks, technical-interviews, answer-structuring]
---

## Situation

I have interviews coming up for technical roles and I need a repeatable prep process. I know the story-based approach to answering but not much beyond that. The playbook uses agents to do the heavy lifting: context synthesis, approach selection, question generation, story shaping, and artifact management.

## Key insight

This is an **agent-orchestrated pipeline** — the human provides raw material (JD, company info, personal CV/projects), the agent handles structure and alternatives, and the human makes the final judgment calls. The workflow produces tagged, reusable artifacts rather than one-off cramming.

The 9-step pipeline:

| Step | Action | Who drives |
|------|--------|------------|
| 1 | Gather raw context (JD, company info, colleague notes) | Human |
| 2 | Agent clarifies and syncs context | Agent leads |
| 3 | Human provides personal docs + grill session | Human responds |
| 4 | Agent maps fit vs. unfit areas in CV | Agent |
| 5 | Agent proposes multiple answer frameworks beyond story-based | Agent (see [[Technical Interview Approaches]] for the 12 frameworks) |
| 6 | Agent generates 5 highest-ROI prep questions from old projects | Agent |
| 7 | Human answers → agent reshapes into story format (hook, stack, solution, lesson) | Human → Agent |
| 8 | Human flags weak/unfit areas → agent reframes them around concepts, not tech stack | Human → Agent |
| 9 | Agent creates tagged artifacts, lists all tags for retrieval | Agent |

The value is in **step 5**: most engineers default to STAR and miss the signal-optimization opportunity. Matching the answer frame to the question type (bug → problem-solving narrative; architecture → decision-based; failure → failure-and-learning) makes the strongest signal visible for each answer.

## Unknowns

- Has this full 9-step pipeline been tested end-to-end, or is it aspirational?
- How long does a full run take in practice? Is it a 2-hour session or spread across days?
- Which steps need the most refinement — where does the agent's output usually need the most correction?
- Are the tagged artifacts (step 9) saved into the vault, and if so, where? (Candidate for `11l07.Career/`)

## Next actions

- [ ] Run the playbook end-to-end for one upcoming interview to find the rough edges
- [ ] Time each step — identify where the agent output needs the most human correction
- [ ] Decide artifact destination: `11l07.Career/` or a per-interview folder?
- [ ] Refine step 5 (framework matching) with the concrete question→frame map already in [[Technical Interview Approaches]]
- [ ] Add a "prep checklist" preamble: what the human must have ready before starting step 1
- [ ] Consider: does the playbook need a variant for different interview types (presales-facing vs. pure engineering vs. leadership)?

## Keywords
interview-prep, agent-assisted, story-frameworks, technical-interviews, answer-structuring
