# Open threads — AI-Delivery-Pipeline

Near-term threads (named explicitly by the user) and recognize-and-add anchors (grouped; each
grounded in something already in the vault — recognize as something once written, not a new
obligation).

## Near-term / active
- Prompting technique: prompt chaining vs. context-up-front (the 4-layer context model — see
  archived prior `202607061358-prompting-techniques-context-drift`).
- Cost control & observation.
- How-much-context-is-enough.
- Unknown-unknowns coverage (grilling's complementary skill — see Deferred
  `unknown-unknowns-skill-research` and `19z.Resources/unknown-sweep/`).
- **Onboarding into the pipeline (active):** toolings that let a new hire onboard by asking the
  LLM generalized questions, and the toolings route them to where to go / what to do. Design intent,
  not just a future thread.

## Recognize-and-add anchors (5 clusters)

### Pipeline mechanics
- Handoff artifacts between phases (Spec → Plan → Tasks → Implement) — from kcc-platform trio; what's
  the minimum to carry forward.
- Verification-in-prompt-environment — each phase specifies *how it'll be evaluated*, not bolt-on
  after (from SWE-concepts note).
- Context reset / context rot — per-step session resets (from llm-resources workflow); detecting
  drift mid-run (precursor: `prompting-techniques-context-drift`).
- Progressive disclosure vs. giant-prompt — the 4-layer context model (from today's capture).

### Model & cost control
- Model tiering / routing — planning on higher-tier, implementation on Sonnet; when to escalate /
  de-escalate (from llm-resources).
- Single-egress cost/audit enforcement — encode governance as a lint/static failure (from
  `ai-product-architecture-patterns`).
- Per-phase budget / observation — usage dashboard as an improvement control loop (from the RIC
  dashboard item).

### People, accountability, reuse
- Ownership under automation — who is accountable when AI prepares and human approves (Kintai
  framing, from RIC dashboard item).
- Skill reuse / portability seam — local-tooling-bound skills vs. reusable capability; marketplace →
  platform (from RIC dashboard item).
- Raising-the-baseline mechanism — *how* a well-shaped pipeline raises employee baseline (the
  side-effect claim); currently a claim, not a mechanism.
- Human apathy / "looks good enough" — review degradation under fluent generated text (from
  today's capture).

### Discovery & divergence
- Unknown-unknowns coverage — grilling's complementary skill; assumption audit, red-team critic
  (from `unknown-sweep`).
- Divergence vs. convergence tooling — brainstorming skills that fan out multiple ideas (from
  llm-resources meta-plugin).
- Meta-tooling — skills that author skills (recursive plugin-creating-plugin, from llm-resources).

### Quality & failure surface
- Evals per phase — distinct from human gates; structured output-quality assessment.
- Failure modes for agentic skills — browser/MCP-acting skills, the "unacceptable mistake" framing
  (from RIC dashboard item).
- Long-run drift detection — hands-off research agent, stop-on-drift (from unknown-unknowns Deferred
  item).

## Deferred future milestones (recognized during blindspot pass)
- **Reversibility / off-ramp:** fallback when the AI layer degrades (model regression, provider
  outage, cost spike). Pipelines that assume AI can be a single point of failure. Next milestone
  after the AIX-handbook artifact lands.
- **Tooling diversification:** provider-agnostic is the goal, but industry is young and toolings
  immature; for enterprise, use front-running solutions now, diversify later via further research.
- **Baseline-measurement:** tracked via observability + delivery-dashboard metrics; consult other
  departments later. Future milestone.