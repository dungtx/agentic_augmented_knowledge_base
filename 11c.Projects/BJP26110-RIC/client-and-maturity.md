# Client & AI maturity — BJP26110-RIC

## Client
Ricoh — Japanese conglomerate (printers & cameras). Our engagement is with the **APAC branch**
specifically.

## Customer stance
- Automate as much as possible while keeping ownership and increasing speed.
- **We consult; their in-house team builds the toolings themselves** — the delivery vehicle is their
  hands, not ours. Any recommendations must respect this constraint.

## AI maturity (middle)
- Non-technical staff already use AI coding agents (Claude Code) + MCP + skills to automate daily
  workflows.
- Engagement stops at **consuming tools** — no governance, no enterprise-level direction. This is
  the "bottom-up" label (our definition).
- Current focus: automation of repetitive tasks, but only small tasks with marginal speedups.

## Concrete example
Monthly attendance-report automation — sounds good, but a human could do it in a day; barely above
a normal automation script.

## Known tooling inventory (under review)
- Claude-code skill marketplace + publishing pipeline (skill-audit gate).
- Per-user cost-tracking dashboard (likely derived from Claude Code OTEL).
- In-house MCPs into internal systems.
- Hooks in Claude Code instances — collect and (token-permitting) write to **Tasky** (in-house
  Jira-like) and **Kintone** (in-house business-task product — we know little as it's their product).
- See [[mcp-internal-notes]] for the component breakdown (common / tasks / kintai / reminder /
  video-highlight / data).

## What "bottom-up" means here
Caution, not lack of appetite for top-down. Japanese company, slower to change — they need
effectiveness proven before expanding scope.