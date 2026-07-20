# Tag glossary

> Controlled vocabulary for tags across all notes. When assigning tags during `seed-inbox` or `distill-permanent`, pick from this list. Standardize: **lowercase, kebab-case, singular noun** unless the concept is inherently plural (`interviews`, `demos`). Add a new tag only when a note genuinely introduces a new category — this glossary catches up after.

## Career & Interviews

```
career
   Professional development, job trajectories, career moves.
  interviews
     The interview process: preparation, conduct, post-mortem.
    hiring
       The organizational side: recruiting, selecting, pipeline management.
    evaluation
       Assessing candidates — skills, fit, potential, weaknesses.
      rubric
         Structured scoring frameworks and evaluation criteria grids.
    question-design
       Crafting interview questions that reveal capability, not just knowledge.
    ai-engineer
       Role-specific: hiring and evaluating AI engineering candidates.
    storytelling
       Narrative techniques for structuring interview answers (STAR, CARL, etc.).
  leadership
     Management, mentorship, organizational leadership.
  decision-making
     Frameworks for making, justifying, and communicating decisions.
```

**See also:** `evaluation-metrics` (AI), `skill-design` (Meta)

## Presales

```
presales
   The presales function end-to-end: from lead to handoff.
  deal-qualification
     Assessing whether an opportunity is worth pursuing (BANT, MEDDIC, etc.).
  pitching
     Presenting capabilities and value to prospects.
  demos
     Product or service demonstrations — structure, narrative, follow-up.
  consulting
     Advisory engagement: discovery, diagnosis, recommendation.
  value-proposition
     Articulating what we offer, why it matters, and how it maps to pain points.
  sales-pipeline
     Deal flow from lead to close — stages, velocity, forecasting.
  client-engagement
     Building and maintaining relationships with prospects and clients.
  delivery-handoff
     Transitioning a won deal from sales to delivery without knowledge loss.
  enterprise-architecture
     Understanding client org structures (HR, management, sales orgs).
  lead-generation
     Sourcing new opportunities: cold outreach, networking, seminars.
```

**See also:** `decision-making` (Career), `storytelling` (Career)

## AI & Engineering

```
ai
   Artificial intelligence — the broad domain.
  prompt-engineering
     Crafting effective prompts for LLMs — structure, constraints, iteration.
  agent-design
     Designing autonomous AI agent systems: tool use, memory, planning.
  mcp
     Model Context Protocol — the tool-discovery/tool-call contract LLM clients use to reach external systems.
  agents
     Using AI agents as tools or assistants within a larger workflow.
  verification
     Validating AI outputs — human-in-the-loop gates, correctness checks.
  evaluation-metrics
     Measuring AI system performance: accuracy, latency, cost, reliability.
  ocr
     Optical character recognition — document parsing, handwriting, multilingual.
  data-quality
     Accuracy, cleanliness, and reliability of data fed into systems.
```

**See also:** `evaluation` (Career), `rubric` (Career), `workflow` (Meta)

## Language & Habit

```
japanese
   Japanese language learning specifically — reading, writing, listening, speaking.
  language-learning
     Language acquisition methods, theory, and tools (general).
routine
   Daily or weekly practice structures — scheduling, rotation, minimums.
habit
   Habit formation psychology: triggers, atomic habits, behavior design.
```

**See also:** `workflow` (Meta)

## Meta / Process

```
zettelkasten
   The note-taking methodology: atomic notes, link graph, MOCs.
note-taking
   General note-taking practices, tools, and theory (broader than zettelkasten).
capture
   The capture phase of the knowledge pipeline — getting thoughts down fast.
distillation
   Processing raw notes into permanent knowledge — the refine-and-link phase.
skill-design
   Designing agent skills: SKILL.md authoring, dispatch rules, guardrails.
workflow
   Repeatable processes, automation, and pipeline design.
protocol
   Structured step-by-step process documents (interview protocol, deployment runbook).
```

**See also:** `habit` (Language & Habit), `routine` (Language & Habit)

## Home & Lifestyle

```
home
   Home goods, domestic purchases, living space improvements.
  fabric
     Textile materials, fabric properties, material selection for clothing and home.
  grooming
     Personal grooming: skin care, hair care, hygiene routines.
  vietnam
     Vietnam-specific context: local shopping, climate adaptations, living in VN.
```

## Conventions

- **Case:** lowercase, hyphens between words (`deal-qualification` not `deal_qualification` or `Deal Qualification`).
- **Number:** singular unless the concept is inherently plural (`interviews` as a domain, `demos` as a category).
- **Granularity:** precise over broad. `deal-qualification` over `sales`. `prompt-engineering` over `ai`. The broader tag is the domain heading, not a tag you assign.
- **Budget:** 2–6 tags per note. Fewer is better — tags are retrieval hooks, not a full classification.
- **Noise:** drop words that carry no signal for retrieval — `notes`, `thoughts`, `ideas`, `misc`.
- **Adding new tags:** when a note genuinely introduces a new category, add it to the appropriate domain here with a one-line definition. Don't bloat — if an existing tag covers 80% of the concept, use it.
- **Cross-domain tags:** a note can pull tags from multiple domains (e.g., an AI-driven presales tool might use both `agents` and `presales`). The "See also" lines are for glossary navigation, not a restriction.
