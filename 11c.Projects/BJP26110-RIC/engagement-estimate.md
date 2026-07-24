---
project: BJP26110-RIC
status: draft
created: 2026-07-23
---

# Engagement Estimate — BJP26110-RIC

## Staffing

1 person, full-time.

## Constraints

- D1: Review scope is **skill marketplace + cost dashboard only**. No MCP access.
- D2: Build starts **after NDA signed**. RSI access available from day one of build — no separate validation phase.

## Option A — Core scope

| Deliverable | Working days | Calendar |
|---|---|---|
| D1 — Review (slide deck + walkthrough) | 7-10 | Weeks 1-2 |
| D2 — RSI MCP, Tier 1 (typed tools + governance gate) | 7-10 | Weeks 3-4 |
| **Total** | **14-20 days** | **~3-4 weeks** |

## Option B — Full reference implementation

| Deliverable | Working days | Calendar |
|---|---|---|
| D1 — Review (slide deck + walkthrough) | 7-10 | Weeks 1-2 |
| D2 — RSI MCP, Tier 1+2 (+ resources, prompts, feedback collector) | 12-18 | Weeks 3-5 |
| **Total** | **19-28 days** | **~4-5 weeks** |

## D1 — Review (7-10 days)

| Unit | Days |
|---|---|
| Discovery: marketplace pipeline walkthrough + dashboard walkthrough | 1-2 |
| Architecture: marketplace schema quality, dashboard observability coverage | 1-1.5 |
| Security: access boundaries, permission scoping, data exposure | 1 |
| Guardrails: skill-audit gate, error-handling UX, output quality gates | 0.5-1 |
| Accountability: HIL architecture, trust calibration, audit trail | 0.5-1 |
| Synthesis: findings heat-map, prioritized roadmap, maturity baseline, adoption recommendations | 1-2 |
| Slide deck + walkthrough + one iteration round | 1.5-2 |

## D2 — RSI MCP

### Tier 1 (7-10 days)

| Unit | Days |
|---|---|
| Project scaffold: MCP skeleton, transport layer, tool registry, config, dev env | 1 |
| Typed query tools: 3 use cases with parameter schemas, validation, RSI query mapping, error handling | 2-3 |
| Governance Gate: auth enforcement, audit logging, cost attribution, permission authorization | 2-3 |
| Testing + edge cases | 1-2 |
| Docs + deployment guide | 1 |

### Tier 2 (+5-8 days on top of Tier 1)

| Unit | Days |
|---|---|
| MCP Resources: browsable catalog of report templates with parameter schemas | 1-2 |
| MCP Prompts: scaffolded workflows for common report patterns | 1-2 |
| Feedback Collector: per-invocation ratings, invocation metadata aggregation, trend + drift detection | 2-3 |
| Integration testing: Tiers 1+2 end-to-end | 1 |

## Assumptions

- 1 person, full-time.
- Client review cycles not included (Yamano turnaround unknown). Each round adds ~1 week calendar.
- NDA timing: critical path. If NDA isn't signed by D1 completion, D2 stalls. Recommend separable-phase pricing or NDA-timing clause in proposal.
- All remote. No travel.
- D2 stack follows docuware-tools pattern (Python/FastMCP or equivalent).

## Uncertainty

- Number of skills visible in marketplace (estimated 10-20; more = +1-2d on D1 inspection).
- RSI API surface shape (clean endpoints = low end; inconsistent schemas = high end of D2 range).
- Client review cycle speed (Japanese company, thorough; budget 1 round, 2 rounds = +3-4d calendar).
