# 0007 — New pickup task: web-research skill (2026-07-01)

User requested a skill that can access the web and do research on their behalf, then note findings back into the vault. Recorded here so it's not lost; to be grilled and built later. Slotted as **T10** in the pickup-task list (`.memory/0003-…-pickup-tasks.md` §5).

## T10 — Web-research skill (planned)

**Current state:** not built, not yet grilled. User raised it 2026-07-01 after the distill-permanent skill was committed.

**Goal:** a skill where the agent accesses the web on the user's behalf, researches a topic, and writes the findings back into the vault — likely as a literature note (`kind: lit-note`) in `11l.LtS/` or a research-seed in `11b.Seeds/`, with provenance (source URLs).

**Open questions to grill (one at a time, before building):**

1. **Mechanism / capability.** What web access does the agent actually have? Pure research task — check pi's available tools (custom tools, bash `curl`, any built-in browse/fetch). If no network egress, this skill is blocked until a tool exists. Unblocks everything else.
2. **Output shape.** Where do findings land?
   - A literature note in `11l.LtS/` (permanent, atomic, with `source` as URLs)?
   - A research-seed in `11b.Seeds/` for later distill?
   - An Inbox capture (`11a1.Inbox/`) if it's raw?
   Recommend: literature note for settled findings, seed for raw research dumps — matches the two existing pipelines.
3. **Provenance discipline.** Every claim cites its source URL. No unsourced assertions in the output. How are citations formatted — inline markdown links, a `sources:` frontmatter array, footnotes? Recommend `sources:` array + inline links.
4. **Scope / trust.** Does the agent judge source credibility, or just fetch and report? Recommend: fetch + report with a credibility flag (primary source / blog / vendor marketing), let the user judge.
5. **Trigger words.** "research X", "look up X", "find out about X", "web search X". Confirm.
6. **Relationship to capture/distill.** Is web-research its own pipeline (research → LtS), or does it feed the existing capture → seed → distill flow? Recommend: outputs land as seeds or lit-notes that the existing skills then handle — don't build a parallel graph.
7. **Model-invoked vs user-invoked.** Probably model-invoked (the user will say "research X" naturally), but the description must distinguish "research this topic" (web) from "capture this thought" (capture-fleeting) and "explain this concept" (general knowledge, no web needed). Worth grilling the boundary.

**Practice warnings to issue when grilling:**

- **Collector's fallacy** (W-series from `0002`): hoarding web research without processing it. The skill should produce *distilled* findings, not a link dump.
- **Unsourced claims** — the single biggest risk. A web-research note without citations is worse than no note (it looks authoritative but isn't traceable). Hard rule: no `status: permanent` without a `sources:` field.
- **Stale web content** — pages change. Capture the access date alongside each URL.
- **Distinguish "research" from "explain"** — the agent's own pretrained knowledge is not web research. If the user wants the agent's knowledge, that's a normal answer, not this skill. Only fire on an explicit "go find out" intent.

**Dependencies:** none hard, but T9 (pi `@`-import verification) and T1 (full AGENTS.md) should land first so the new skill's dispatch rule has a home in the always-on layer.

**Suggested position in ordering:** after T1 (full AGENTS.md) so its dispatch rule is written into the real brain, alongside T3 (morning-review) — both are "last roster" skills. Not before the retrieval layer (T7) since web-research *produces* retrievable notes, it doesn't *consume* them.
