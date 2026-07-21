---
status: triaged
kind: idea
captured_at: 2026-07-17T15:35:31+07:00
tags: []
needs_review: false
triaged_at: 2026-07-21T18:34:11+07:00
triaged_to: "[[../../11c.Projects/BJP26110-RIC/README.md]]"
---

For the RIC AI transformation consultant bid, the current system is a Claude skill marketplace plus a usage dashboard. They already have a skill creation → self-refinement → publishing pipeline, but the missing seam is usage monitoring and improvement.

The useful framing is to treat usage monitoring not as “more analytics,” but as an improvement control loop: dashboard data should feed decisions about which skills to improve, retire, scale, govern more tightly, or turn into standard operating practice.

A good business-oriented QA question for RIC is:

“Given your current skill marketplace and usage dashboard, what decisions should usage data help RIC make about AI transformation — for example, which skills to improve, retire, scale, govern more tightly, or turn into standard operating practice?”

This sits in the middle: grounded in their current marketplace/dashboard, but not trapped in implementation steps. It exposes the seam between usage data, decision rights, continuous improvement, and transformation governance.

Additional QA direction from grilling:

- RIC’s skill marketplace is still seed-stage and currently applied only inside one team/branch. Their focus is conservative: automate mundane daily workflows first, such as clock-in support, report generation, and demo reel video creation.
- Their current publishing flow allows anyone to share a new skill after verifying it on their own side for a while. A `skill-audit` SKILL acts as the gate/checklist before publishing. They do not want a complex approval workflow yet because it would slow adoption.
- A useful reuse question is: “For the skills that work correctly in your current team, if another branch wanted to use them, would they be able to run them as-is, or would the skills need to be adapted to that branch’s tools, workflows, and local rules?” This probes the seam between local automation and reusable capability.
- The likely insight: current skills are scoped closely to local tooling. Reuse requires separating skill logic from environment assumptions; otherwise the marketplace remains a local automation library rather than a broader transformation platform.
- Security setup: skills mostly act through Playwright/browser automation and internal MCPs connected to internal services. Long-lived tokens are saved in Claude settings. The sharper security angle is not generic permission hygiene, but business-impact failure and human checkpoints.
- A useful security question is: “For AI skills that operate through the browser or internal MCPs, what kind of mistake would be unacceptable even if the skill is automating a mundane task — and where should the human checkpoint sit before that mistake can happen?”
- Concrete Kintai/accountability framing: “For the Kintai skill that bulk-approves attendance, what evidence should remain afterward so the team can tell which attendance records the AI prepared, which approvals the human confirmed, and who is accountable if an incorrect approval is made?”
- Concrete report QA framing: “For report-generation skills that already run without human review, what kinds of report errors would be serious enough to add a review checkpoint or redesign the skill?”
- Future accountability framing for read-only MCPs: “If RIC creates an MCP that lets AI pull data from the RSI Data Platform for reports or analysis, who is responsible when the final output is wrong: the user who requested it, the skill that transformed it, the MCP/data platform that supplied it, or the process owner who allowed this automation?”
- Usage dashboard value framing: “For the usage dashboard, which signals would tell you that a skill is genuinely creating business value, rather than just being used frequently?”
- Usage dashboard lifecycle framing: "When the dashboard shows that a skill is rarely used, how would you decide whether the skill should be improved, better promoted, left alone, or retired?"
- Usage dashboard observability framing: "When the usage dashboard shows failures, retries, or abandoned runs for a skill, what detail should it provide so the team can tell whether the problem came from the user input, the skill design, the browser/MCP step, or the source data?"

## Session summary — QA questions by theme

All questions target RIC's current state (seed-stage marketplace, mundane task automation, conservative adoption) but open seams toward broader AI transformation thinking.

**Ownership & reuse**
1. "For the skills that work correctly in your current team, if another branch wanted to use them, would they be able to run them as-is, or would the skills need to be adapted to that branch's tools, workflows, and local rules?"

**Security**
2. "For AI skills that operate through the browser or internal MCPs, what kind of mistake would be unacceptable even if the skill is automating a mundane task — and where should the human checkpoint sit before that mistake can happen?"

**Accountability**
3. "For the Kintai skill that bulk-approves attendance, what evidence should remain afterward so the team can tell which attendance records the AI prepared, which approvals the human confirmed, and who is accountable if an incorrect approval is made?"
4. "If RIC creates an MCP that lets AI pull data from the RSI Data Platform for reports or analysis, who is responsible when the final output is wrong: the user who requested it, the skill that transformed it, the MCP/data platform that supplied it, or the process owner who allowed this automation?"

**QA & quality standards**
5. "For report-generation skills that already run without human review, what kinds of report errors would be serious enough to add a review checkpoint or redesign the skill?"

**Usage dashboard & improvement loop**
6. "Given your current skill marketplace and usage dashboard, what decisions should usage data help RIC make about AI transformation — for example, which skills to improve, retire, scale, govern more tightly, or turn into standard operating practice?"
7. "For the usage dashboard, which signals would tell you that a skill is genuinely creating business value, rather than just being used frequently?"
8. "When the dashboard shows that a skill is rarely used, how would you decide whether the skill should be improved, better promoted, left alone, or retired?"
9. "When the usage dashboard shows failures, retries, or abandoned runs for a skill, what detail should it provide so the team can tell whether the problem came from the user input, the skill design, the browser/MCP step, or the source data?"

**Key grilling insight:** Every question anchors in their current reality (skill marketplace, dashboard, Playwright, MCPs, Kintai, report generation) but probes a seam toward the larger shift — from local automation library to reusable AI capability with defined ownership, evidence, and improvement loops.
