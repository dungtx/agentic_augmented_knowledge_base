# AI-Knowledge System Design Critique — When an Analytics Platform Is the Wrong Shape

Lessons from critiquing an `arch.drawio` data-platform diagram that was proposed as the architecture for a
company AI-knowledge assistant meant to help *deliver software*. Term definitions live in
[[../data-platform-glossary|Data Platform Glossary]]; this note is the *judgement* layer on top —
which components earn their place for a RAG/knowledge assistant and which are dead weight. Companion to
[[ai-product-architecture-patterns|AI-Product Architecture Patterns]] and the
[[../anti-patterns-pitfalls-checklist|Anti-Patterns & Pitfalls Checklist]].

## The core mistake: an analytics platform wearing a knowledge-system costume

The diagram was a textbook **enterprise analytics/BI platform** (Sources → ETL → Landing/Staging/Curated →
Warehouse/Mart, governed underneath). That skeleton is *right* — but it is over-built on the analytics
side and under-built on the retrieval side. For a knowledge assistant, the entire product lives in the
box the diagram compressed into two words: "AI Agent." **Lesson:** a BI-platform reference architecture
and a RAG reference architecture share only their outer frame; copying the BI one and bolting a vector DB
on the side gets the hard 80% wrong.

## What was genuinely good (keep these)

- **Zoned storage (Landing → Staging → Curated).** Keeping an untouched raw copy means you can re-chunk / re-embed later without re-fetching. Most naive RAG projects skip this and regret it.
- **Vector DB *and* Knowledge Graph together.** Enables GraphRAG — semantic similarity plus relationship traversal. For software ("what depends on this module?", "who owns this incident?") the graph is a real asset.
- **Metadata as a first-class layer.** It is what lets the assistant *cite its sources* — the line between a trustworthy tool and a plausible liar.
- **Governance + Monitoring cross-cutting.** Mature instinct; most teams bolt these on too late.

## Gap 1 — The data sources didn't match the domain

The sources were generic corporate (RDBMS, ERP, Log, Documents, Media) and the entities read like a
tender/consulting business (Bid, Client, Project). A *software-delivery* assistant feeds on completely
different material: **Git repos/PRs/reviews, Jira/Linear issues, Confluence/Notion wikis, ADRs/RFCs/design
docs, CI/CD logs, incident postmortems/runbooks, and Slack/Teams threads** (where most tribal knowledge
actually lives). **Lesson:** fix the source layer first — it silently defines everything downstream. A
knowledge system is only as good as the corpus it can see.

## Gap 2 — The retrieval pipeline was invisible

"AI Agent" hid every hard component: **chunking** (code needs syntax-aware splits, not 512-token cuts),
the **embedding pipeline**, a **retriever + reranker**, **hybrid search** (pure vector search is weak on
code, where exact tokens — function names, error codes, config keys — matter), **context assembly**, the
**LLM serving layer**, and **guardrails** (a malicious PR description can hijack the assistant via prompt
injection). **Lesson:** for a knowledge assistant, the retrieval pipeline *is* the product; if it's one
box on the diagram, the design isn't finished.

## Gap 3 — No evaluation or feedback loop (the #1 omission)

Every arrow flowed one way. A knowledge system with no way to measure itself rots quietly: magical for two
weeks, then wrong. Needs an **eval harness** (golden question sets, retrieval precision/recall), **feedback
capture** (thumbs up/down, "was this source relevant?"), and **re-embedding on eval failure**. **Guard:**
if you can't answer "how do we know retrieval got better after this change?", you haven't built a system,
you've built a demo.

## Gap 4 — Batch ETL is too slow, and there's no update/delete path

Software knowledge changes hourly. The one-way batch ETL flow has no story for **edits or deletions** —
so old vectors keep getting cited after the source changed or was removed (a top source of "the AI told me
something no longer true"). **Lesson:** prefer **event-driven / incremental sync** (Git/Jira webhooks) and
design **tombstoning** (kill stale vectors on change/delete) as a first-class path, not an afterthought.

## Gap 5 — Warehouse + Mart are probably scope creep

Warehouse and Data Mart are for *numeric analytics/reporting*; a retrieval assistant barely touches them.
Keep them **only if** you also want delivery *metrics* (cycle time, DORA) — but recognize that's a
**separate product** from the assistant. **Guard:** the disambiguating question is *"answer questions
about the software (pure RAG — warehouse is dead weight) vs. manage delivery status/metrics (needs the
warehouse)?"* The diagram straddled both and committed to neither. Force the choice early.

## Gap 6 — Governance was passive; for AI it must be active at query time

Two AI-specific risks the passive-layer drawing missed: **permission-aware retrieval** (only retrieve what
the *asking* user may see — otherwise a junior's query can pull a restricted repo or HR doc, i.e. a
data-leak machine) and **secret/PII redaction before embedding** (repos are full of API keys; once a
secret is embedded it's queryable forever). **Lesson:** in a RAG system, access control and redaction move
from a background policy into the hot path of every query and every ingest.

## The revised shape (retrieval platform, not analytics platform)

```
SOURCES (code, Jira, wiki, Slack, CI, incidents)
  → INGESTION (event-driven + incremental, with delete handling)
  → PROCESSING (parse → redact secrets/PII → chunk → embed)
  → STORAGE (Vector DB + Knowledge Graph + object store for raw)   [drop/deprioritize Warehouse+Mart]
  → RETRIEVAL (hybrid search → rerank → permission filter → context assembly)
  → LLM + Guardrails (injection defense, citation enforcement)
  → AI Agent / Dashboard
       ↑ EVAL + FEEDBACK LOOP (golden sets, thumbs up/down → re-curate/re-embed)
  cross-cutting: Metadata/Lineage · Governance (active, query-time) · Monitoring (+ AI quality metrics)
```

Build priority: (1) fix the source list, (2) make retrieval explicit (hybrid + rerank + permission
filter), (3) add eval + feedback, (4) incremental ingestion with delete handling, (5) query-time access
control + secret redaction, (6) re-decide whether the warehouse belongs at all.
