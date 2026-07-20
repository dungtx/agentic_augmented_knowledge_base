---
status: triaged
kind: idea
captured_at: 2026-07-06T13:58:40+07:00
triaged_to: "[[../202607171612-ai-research-agenda-sdlc-gates.md]]"
triaged_at: 2026-07-17T16:15:00+07:00
---

Explore prompting techniques: find the best way to provide context to an LLM so intent stays clear and the conversation/output doesn't drift.

## Preliminary findings

Your idea is closely aligned with what the industry now calls **context engineering**, **spec-driven development**, and increasingly **harness engineering**.

The main correction I would make is:

> Do not give the model "as much context as possible." Give it the **smallest sufficient set of high-signal context for the current SDLC phase**, plus reliable ways to retrieve more.

Anthropic describes context as "a critical but finite resource for AI agents." Its recommended goal is the smallest set of high-signal tokens that maximizes the chance of the desired result. ([Anthropic][1])

### 1. The current shift: prompt engineering → context engineering

The older approach concentrated on wording one large prompt correctly. The newer approach manages the complete information environment surrounding each model call:

* System and repository instructions
* Current task instructions
* Requirements and design artifacts
* Relevant source files
* Tool descriptions
* Retrieved documentation
* Previous decisions
* Test results and runtime observations
* Progress and handoff files

Anthropic defines context engineering as curating and maintaining the optimal information available during inference — not merely writing the system prompt. It recommends hybrid retrieval: load a small amount of persistent context initially, then let the agent retrieve files and evidence "just in time." ([Anthropic][1])

Martin Fowler's February 2026 overview uses the simpler definition:

> "Context engineering is curating what the model sees so that you get a better result."

It separates context into reusable instructions, guidance or guardrails, tools, MCP servers, skills, and workflow artifacts such as specifications. ([martinfowler.com][2])

This directly supports an SDLC-based approach: the main engineering problem is deciding **what the model should see at each stage**, not merely creating different prompt wording.

---

### Practices showing the strongest convergence

#### 2. Progressive disclosure instead of a giant project prompt

OpenAI's strongest statement from its February 2026 Codex engineering report is:

> "give Codex a map, not a 1,000-page instruction manual."

OpenAI reported that a single enormous `AGENTS.md` crowded out the actual task and relevant code, made all guidance appear equally important, became stale, and was difficult to verify. Their replacement was a small entry point that directed the agent toward a structured repository knowledge base. ([OpenAI][3])

This is usually implemented as:

1. A small persistent project context.
2. A repository or documentation map.
3. Task- or phase-specific artifacts.
4. On-demand retrieval of deeper material.
5. Mechanical checks for documentation freshness.

OpenAI calls this **progressive disclosure**: agents begin with a stable entry point and learn where to look next rather than receiving everything at once. They also use CI and "doc-gardening" agents to detect stale knowledge. ([OpenAI][3])

Anthropic independently recommends the same pattern. Agents can retain lightweight identifiers — paths, links, query names — and progressively retrieve the underlying material when it becomes relevant. ([Anthropic][1])

**Implication:** a discovery prompt should not contain every design and implementation document. It should contain the discovery objective, business/customer sources, existing known constraints, a source index, instructions for retrieving additional evidence, and the expected discovery artifact. Likewise, an implementation prompt should receive only the approved plan section, relevant requirements, affected architecture decisions, likely files, and verification commands.

#### 3. Explicit separation of research, planning, and implementation

Anthropic's Claude Code guidance summarizes the workflow as:

> "Explore first, then plan, then code."

The four documented phases are exploration, planning, implementation, and verification. Plan mode is intentionally read-only during exploration so the agent does not begin solving the wrong problem before understanding the codebase. ([Anthropic][4])

HumanLayer's Advanced Context Engineering workflow uses a similar sequence: "research, plan, implement." Its key idea is **frequent intentional compaction**: each phase generates a concise artifact, then the next phase starts with a cleaner context containing the reviewed artifact rather than the entire conversation. Human review sits between research and planning, and between planning and implementation. ([GitHub][5])

Each phase should have: a fresh or mostly clean context, a clearly defined goal, approved upstream artifacts, phase-appropriate evidence, a constrained output schema, a quality gate, and a handoff artifact for the next phase. The conversation history itself should not be the primary handoff mechanism.

#### 4. Specification artifacts become the context pipeline

**GitHub Spec Kit** — core process: "Spec → Plan → Tasks → Implement." Each phase produces a Markdown artifact that becomes structured input to the next phase. Full workflow: Constitution → Specify → Clarify → Plan → Checklist → Tasks → Analyze cross-artifact consistency → Implement → Converge. Separates the **what and why** (spec) from technology/architecture choices (plan). As of 2026-05-27: 106,000+ GitHub stars, 200 contributors, 30 integrations, 100+ community extensions. ([GitHub Pages][6], [7])

**Kiro Specs** — "Requirements → Design → Tasks," with a design-first alternative for technically constrained systems. Requirements use EARS-style statements ("WHEN [condition/event] THE SYSTEM SHALL [expected behavior]"), making them testable and traceable into implementation. Distinguishes feature specs from bug-fix specs — different SDLC work needs different context shapes, not just different wording. ([Kiro][8], [9])

**BMAD Method** — "builds that context progressively across 4 distinct phases": Analysis (brainstorming, market/domain/technical research, product brief) → Planning (PRD, UX, requirements) → Solutioning (architecture, epics, stories, readiness checks) → Implementation (story prep, dev, testing, review). Adjusts artifact depth to task size (small fix = tech spec; large product = PRD + architecture + UX; enterprise = + security/DevOps). ~50.1k stars, July 2026 release. Notably separates planning (conversational web model) from implementation (IDE agent with repo/terminal access). ([BMAD][10], [11], [12])

#### 5. Persistent context files: useful, but only when minimal

`AGENTS.md`, `CLAUDE.md`, Copilot custom instructions, Cursor rules are all variations of persistent project guidance. AGENTS.md calls itself a "README for agents," used in 60,000+ open-source projects, with nested instructions where the file closest to the code takes precedence. ([Agents][13]; [GitHub Docs][14])

Anthropic's more restrictive advice for `CLAUDE.md`: include commands the agent can't infer, unusual coding/testing rules, architecture decisions and non-obvious gotchas; exclude general language conventions, detailed API docs, file-by-file repo descriptions, and rapidly changing information — move occasional domain workflows into on-demand skills instead. ([Anthropic][4])

Central distinction:

```text
Persistent context = things applicable to almost every task
Phase context      = information relevant to one SDLC stage
Task context        = information relevant to one unit of work
Retrieved context   = evidence loaded only when needed
Runtime context      = tests, logs, screenshots and observations
```

Do not combine these into one project-wide prompt.

#### 6. Verification is now treated as part of the prompt environment

Anthropic: "Give Claude a check it can run" — tests, builds, linters, output fixtures, browser journeys, screenshot comparisons. Without these the agent stops when work merely *appears* complete. OpenAI exposed browser state, logs, metrics, traces directly to Codex, letting prompts express observable conditions (e.g. startup latency, max span duration) that the agent could reproduce, fix, and re-verify against. Anthropic's long-running-agent work (March 2026) uses separate planner/generator/evaluator agents and treats structured artifacts + executable evaluation criteria as essential for sustaining long work. ([Anthropic][4], [15]; [OpenAI][3])

Every phase prompt should specify not only **what to produce** but **how it will be evaluated**.

#### 7. Context resets and handoff artifacts

For long-running work, current approaches reset model context between phases/slices. Anthropic recommends: compaction that retains architectural decisions, unresolved bugs, and important implementation details; persistent notes outside the context window; specialized subagents that return concise summaries; fresh-context handoffs for long autonomous tasks. Its long-running harness recommends reading git history and progress files at the start of a new session, then selecting the next incomplete feature. ([Anthropic][1], [16])

A good handoff artifact contains: current objective, completed work, changed files, decisions made, assumptions, failed approaches and why, tests already run, known failures, unresolved questions, next recommended task, exact commands for resuming.

---

### Important contradictory evidence

#### 8. More context can reduce performance

A June 2026 ETH Zurich-led study: "context files does not generally improve task success rates." Repository context files increased inference cost by 20%+ on average; instructions were generally followed, but broad repo overviews weren't helpful — recommend restricting persistent context to genuinely non-standard practices. A separate June 2026 study of popular `AGENTS.md`/`CLAUDE.md` files found recurring problems: context bloat, tool-specific instruction leakage, conflicting rules. ([arXiv][17], [18])

This doesn't disprove the idea — it changes the optimization target:

```text
Wrong target:   Maximum available context
Better target:  Minimum sufficient, phase-specific, evidence-backed context
```

Context files and skills should be treated like code: versioned, reviewed, linted, tested, and deleted when they no longer improve outcomes.

---

### Recommended context model

**Layer 1 — Project constitution** (always available, very short): non-negotiable engineering principles, security/compliance boundaries, supported tech constraints, forbidden operations, canonical build/test commands, links to deeper knowledge, definition of done.

**Layer 2 — Repository map** (navigational index, not a description): where ADRs/PRDs/service docs live, how to locate tests, inspect schemas/APIs, access logs/observability, who owns each subsystem. Load underlying documents on demand.

**Layer 3 — SDLC phase packet** — provide/require pairs per phase:
- *Discovery*: problem statement, stakeholder/customer evidence, current process, domain terms, existing-system docs, constraints, sources, assumptions → evidence-linked findings, contradictions, unknowns, risks, questions, product brief.
- *Requirements*: approved discovery artifact, personas, business rules, scope, existing capabilities, NFRs → scenarios, functional requirements, testable acceptance criteria, out-of-scope, assumption register, traceability.
- *Architecture/solutioning*: approved requirements, current architecture map, relevant ADRs, tech constraints, integration contracts, deployment/perf/security targets → alternatives considered, explicit decisions, trade-offs, component/data-flow design, migration strategy, failure modes, verification approach.
- *Planning*: approved requirements + architecture, focused codebase research, dependency/ownership info → vertical slices, file/subsystem impact, task dependencies, test strategy, rollback points, completion checks, blocking questions.
- *Implementation*: only one slice, relevant plan section, directly related requirements, relevant ADRs/interfaces, likely code locations, examples to imitate, exact validation commands, explicit boundaries. Avoid attaching the entire discovery history or complete PRD unless genuinely needed.
- *Review/QA*: diff/changed files, requirements covered, architecture constraints, test evidence, known risks, DoD → requirement-to-code traceability, regression analysis, security/perf concerns, missing tests, unnecessary changes, evidence-based approval/rejection.
- *Operations/incidents*: symptoms/timeline, logs/traces/metrics, runbooks, recent deployments, dependencies, blast-radius limits, rollback options → require reproduction/diagnosis before modification (relevant: agents often act when gathering more evidence would be safer — [arXiv][19]).

---

### Sources to prioritize next round

1. GitHub Spec Kit — artifact sequencing, validation gates, agent-neutral implementation.
2. BMAD Method — full lifecycle coverage, discovery through implementation.
3. Kiro Specs — requirements-first vs. design-first routing, testable EARS requirements.
4. Anthropic context engineering — progressive retrieval, notes, compaction, subagent isolation.
5. OpenAI harness engineering — repo knowledge design, runtime feedback, mechanically maintained docs.
6. HumanLayer ACE — brownfield research → plan → implementation, human approval points.
7. 2026 AGENTS.md studies — warning against generic/bloated context.

Overall conclusion: not a library of large SDLC prompts, but a **context compiler** that constructs a different context packet per phase/task:

```text
Persistent constraints
+ phase objective
+ approved upstream artifacts
+ retrieved relevant evidence
+ task boundaries
+ expected output schema
+ executable validation
+ handoff requirements
```

**Sources:**
[1]: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
[2]: https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html
[3]: https://openai.com/index/harness-engineering/
[4]: https://www.anthropic.com/engineering/claude-code-best-practices
[5]: https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md
[6]: https://github.github.com/spec-kit/
[7]: https://github.github.com/spec-kit/quickstart.html
[8]: https://kiro.dev/docs/specs/feature-specs/
[9]: https://kiro.dev/docs/specs/
[10]: https://docs.bmad-method.org/tutorials/getting-started/
[11]: https://github.com/bmad-code-org/bmad-method
[12]: https://docs.bmad-method.org/explanation/web-bundles/
[13]: https://agents.md/
[14]: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions
[15]: https://www.anthropic.com/engineering/harness-design-long-running-apps
[16]: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
[17]: https://arxiv.org/abs/2602.11988
[18]: https://arxiv.org/abs/2606.15828
[19]: https://arxiv.org/abs/2605.07769
