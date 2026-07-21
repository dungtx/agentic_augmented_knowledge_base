---
project: BJP26110-RIC
client: RIC (Ricoh APAC)
status: bid
started: 2026-07-17
---

# BJP26110-RIC — AI Transformation Consultant Bid

**Customer:** Ricoh APAC branch — Japanese conglomerate (printers & cameras). Engagement is with the APAC branch specifically.

**Customer goal:** Learn our AI transformation technique to apply internally. Currently have bottom-up understanding; we provide top-down structure.

**Customer stance:** Automate as much as possible while keeping ownership and increasing speed. **We consult, their in-house team builds the toolings themselves** (delivery vehicle is their hands).

**Case study for:** [[../AI-Delivery-Pipeline/README|AI-Delivery-Pipeline]] (reusable research hub; fuzzy seam).

## Client & AI maturity

Middle maturity. Non-technical staff already use Claude Code agents + MCP + skills to automate daily workflows (kintai attendance, report generation, reminders, video highlights, data tasks). But engagement stops at consuming tools — **no governance, no enterprise-level direction** ("bottom-up" by our definition). Current focus is on small repetitive tasks with marginal speedups; example — monthly attendance report automation that barely beats a normal script. See [[client-and-maturity]].

## Engagement (this bid)

**The ask:** a review of their current system + a sample MCP server.

**Their current system under review:**
- Claude-code **skill marketplace** + publishing pipeline (skill-audit gate).
- Per-user **cost-tracking dashboard** (likely derived from Claude Code OTEL).
- A few **in-house MCPs**; hooks in Claude Code instances that collect and (token-permitting) write to **Tasky** (in-house Jira-like) and **Kintone** (in-house business-task product).

**Sample MCP (we build):** for **RSI Data Platform** (Airflow-like, in-house). Doubles as a demonstration of our AI maturity.

**Deliverables:**
1. **The review** — content still to define: judging metrics, what to write, update suggestions for their current system, post-engagement success tracking, and anything else beneficial. See [[deliverables]].
2. **RSI Data Platform MCP server** — prototype from best practices + residue knowledge (same stack as the docuware-tools case study in [[../../11l.LtS/11l05.AI/mcp-server-design-fundamentals|MCP Server Design Fundamentals]]). Access to RSI pending NDA; they only interact with it via GUI.

**Scope now:** these two deliverables only. Proposal hints at future engagement grounded in our platform knowledge — nothing beyond committed. No engagement length decided. **Effectively still Scout stage**; they've expressed desire to become AI-native, which could mean a long engagement "as long as we have things to show for it."

## Consultant engagement strategy (from senior)

1. **Top-down org chart** (like AIX handbook) + **sidebar of AI integration components** (governance, harness, observability, feedback loop, etc.)
2. **Engagement stages:**
   - Scout — assess current state (in progress)
   - Evaluate — feedback on what exists
   - Design — architect missing parts of AI structure
   - Run — sample project on new system
   - Operate — alongside them
   - Train & transfer — hand over

## People & politics

- **Champion / main contact:** Mr. Yamano Kenta — technical, appears in charge of the branch from our side (exact position unclear).
- **Decision-maker / approver:** unnamed older gentleman in meetings, probably part of decision-makers. Name TBD.
- **Blockers:** none surfaced with names. Real lift is cultural — Japanese company, slower to change; bottom-up reflects caution, not lack of appetite. **We must prove effectiveness before we can do anything else.** First review/MCP must land well to unlock further work.

See [[people-and-politics]].

## Risks & unknowns

- Missing NDA → no RSI Data Platform access → designing blind for the sample MCP deliverable.
- Decision-maker unnamed. Champion's exact position unclear.
- **Cultural uphill battle** — effectiveness must be proven before expansion is possible.
- 8 problems in their system already enumerated (see [[mcp-internal-notes]]): missing signposts for non-tech users; no quick agent-output review; no auto feedback collection; staff lack prompt/context-engineering skills; no drift detection; E2E skills lack gates; two trust failure modes (over-trusting, reflexively untrusting); hidden Obsidian complexity for new hires.

See [[risks-and-unknowns]] and [[deliverables]] for the items still open.

## Related notes

- [[mcp-internal-notes]] — MCP components, team composition, problems list
- [[deliverables]] — review + sample MCP, open questions on each
- [[client-and-maturity]] — Ricoh context, AI maturity assessment, current-tool inventory
- [[people-and-politics]] — champ / decision-maker / cultural blockers
- [[risks-and-unknowns]] — consolidated risk list
- [[../../AI-Delivery-Pipeline/evidence-base|AI-Delivery-Pipeline evidence base]] — permanent notes this project feeds back into
- Original captures: [[../../11a.Capture/11a1.Inbox/_processed/202607171519-ric-ai-transformation-consultant-bid|Inbox capture 1]], [[../../11a.Capture/11a1.Inbox/_processed/202607171535-ric-dashboard-improvement-loop|Inbox capture 2]] (dashboard QA question bank)
- Bottom-up/top-down AI transformation structure note (to be seeded from this project)
- AIX handbook (internal asset, to be distilled into vault later)

## Status log

| Date | Event |
|------|-------|
| 2026-07-17 | Project created; strategy captured from senior |
| 2026-07-21 | Kickoff resumed; grilling completed 5 categories. README expanded, 4 new notes added (deliverables, client-and-maturity, people-and-politics, risks-and-unknowns); original 2 Inbox captures archived into project. |