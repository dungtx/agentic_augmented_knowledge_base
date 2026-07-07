# Data Platform Glossary — Terms for an AI-Knowledge System

Plain-language definitions of the components in a data-platform / RAG architecture, written from a
data-engineering-novice starting point. Built while reading an `arch.drawio` diagram for a company
AI-knowledge assistant. Companion to [[11l05.AI/ai-knowledge-system-design-critique|AI-Knowledge System
Design Critique]] (which argues which of these actually matter for a *software-delivery* assistant) and
sits alongside the other glossaries: [[presale-glosary|Presales]], [[tag-glossary|Tags]].

The organizing spine is the flow every data platform follows: **Sources → Ingestion → Processing &
Storage → Access**, with **Metadata · Governance · Monitoring** running underneath the whole thing. The
one-line theme: *raw and scattered → clean and unified → useful.*

## Stage 1 — Data Sources (where data is born)

- **RDBMS** — Relational Database Management System. Structured data in rows/columns (PostgreSQL, MySQL, SQL Server).
- **ERP** — the large system that runs company operations: finance, procurement, inventory (e.g. SAP).
- **Log** — automatic event records ("user X did Y at 10:03").
- **Unstructured documents** — Excel/Word/PDF files people author; no fixed schema.
- **Media files** — images, audio, video; hardest to analyze automatically.
- **Key idea** — real companies never keep data in one place; everything downstream exists to *unify* it.

## Stage 2 — Ingestion (getting data into the platform)

- **Ingestion** — collecting data from all sources and pulling it in.
- **Batch** — grab everything on a schedule (e.g. nightly). Simple; stale between runs.
- **Streaming** — pull continuously, near real-time. More infra, fresher data.
- **CDC (Change Data Capture)** — capture only what *changed* in a source, incrementally, instead of re-reading everything. The efficient way to keep a copy fresh.
- **ETL** — Extract → **Transform** → Load. Clean/reshape data *before* storing it.
- **ELT** — Extract → Load → **Transform**. Store raw first, transform later inside the store. Preferred when storage is cheap and you may want to reprocess.
- **Pipeline** — an automated, repeatable, scheduled sequence of these steps; no human copy-paste.

## Stage 3 — Processing & Storage (the zones of increasing cleanliness)

- **Landing / Raw Area** — the receiving dock. Data stored exactly as it arrived, untouched — your safety net for reprocessing.
- **Staging Area** — the prep counter. Cleaned, deduplicated, reshaped.
- **Curated Storage** — the finished pantry. Clean, trustworthy, ready to use.
- **Data Lake** — a massive, cheap store holding *everything* in *any* format (tables, PDFs, images), even before you know its use. Landing/Staging/Curated often live inside it.
- **Lakehouse** — a lake with warehouse-like structure/query features bolted on; blurs the lake/warehouse line.
- **Data Warehouse** — a highly-organized store optimized for company-wide *analytics/reporting* over structured, historical data.
- **Data Mart** — a small, team-focused slice of a warehouse (e.g. just Sales). A mini-warehouse.
- **Object store** — cheap blob storage for raw files (S3, MinIO, GCS); the physical floor a lake sits on.

## Stage 3b — The AI-specific stores

- **Embedding** — a piece of text/code turned into a list of numbers that captures its *meaning*. Similar meanings → nearby numbers.
- **Embedding model** — the model that produces embeddings. Choice of model largely determines retrieval quality.
- **Vector DB** — stores embeddings and finds the *most similar* ones fast. Powers semantic search ("find things similar in meaning," not by keyword).
- **Knowledge Graph** — stores data as a web of *relationships* (Client → owns → Project → contains → Bid). Answers connected questions traversal-style.

## Stage 4 — Access & Consumption (serving it)

- **Dashboard / BI** — visual charts and reports for humans (Power BI, Tableau, Looker).
- **Semantic layer** — a shared definition of business metrics so every consumer computes "revenue" the same way.
- **AI Agent** — an LLM-powered assistant that answers using the vector DB / knowledge graph ("chat with your data").

## Cross-cutting — the three support systems

- **Metadata** — "data about the data": what each dataset is, where it came from, what columns mean. The library index. Also what lets an AI *cite its sources*.
- **Data Catalog** — the searchable product built on metadata; how people discover what exists.
- **Data Governance** — the rules: access control, quality standards, privacy/compliance, ownership.
- **Data Lineage** — the traceable path of where each number came from and what transformed it. Essential for trust and debugging.
- **Monitoring / Observability** — watching pipelines for failures, delays, and drift. The "is anything on fire?" alarm.

## RAG-specific terms (missing from the classic diagram, but the real work of an AI assistant)

- **RAG (Retrieval-Augmented Generation)** — retrieve relevant chunks first, then feed them to the LLM to ground its answer. The core pattern of a knowledge assistant.
- **GraphRAG** — RAG that also traverses a knowledge graph, combining semantic similarity with explicit relationships.
- **Chunking** — splitting a document into retrievable pieces. Code needs syntax-aware chunking; naive fixed-size splits break it.
- **Retriever** — the component that fetches candidate chunks for a query.
- **Reranker** — a second-pass model that reorders retrieved candidates by true relevance. Big quality lever.
- **Hybrid search** — keyword (BM25) + semantic search combined. Necessary for code/technical text where exact tokens (function names, error codes) matter and pure vectors are weak.
- **Guardrails** — defenses on model I/O: prompt-injection protection, output validation, hallucination checks.
- **Permission-aware retrieval** — filtering retrieved chunks to only what the *asking user* is allowed to see. Without it the assistant is a data-leak machine.
- **Eval harness** — a golden-question test set measuring retrieval and answer quality over time. The thing that keeps a knowledge system from silently rotting.
- **Tombstoning** — marking a deleted/edited source's old vectors as dead so the AI stops citing stale content. The update/delete story a one-way ETL diagram forgets.
