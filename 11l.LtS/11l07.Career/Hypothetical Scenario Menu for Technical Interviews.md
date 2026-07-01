# Hypothetical Scenario Menu for Technical Interviews

A grab-bag of live design problems organized by tech stack. Use when a candidate's own system is too thin to sustain a full retrospective spine, or as a cross-check. Pick the scenario closest to their strongest stack, surfaced during the router walkthrough.

Each scenario tests 2–3 dimensions simultaneously — Systems Thinking (seams, failure modes), Decision-Range (alternatives considered), and Depth (what breaks first under constraint changes).

## Backend / API

- **Rate-limited API gateway**: "Design an API gateway that sits in front of 10 microservices. Each downstream service has its own rate limit. You need to enforce those limits without adding latency. Walk me through the shape."
- **Idempotent payment processing**: "Design a payment endpoint that must never double-charge, even if the client retries the same request 3 times. What's the architecture?"
- **Job queue with priorities**: "You have a job queue processing ML inference jobs. Some jobs are priority 1, some are priority 3. Design the system so P1 jobs never starve but P3 jobs still get processed."

## Frontend / Fullstack

- **Real-time collaborative editor**: "Design a Google Docs clone — two users editing the same document simultaneously. How do you handle conflicts?"
- **Offline-first form app**: "Build a form-heavy app that must work offline for field workers. They fill forms, submit when back online. What's your sync strategy?"
- **Component library design**: "Design a shared UI component library used by 5 product teams. How do you handle versioning, breaking changes, and team autonomy?"

## AI / ML Engineering

- **LLM guardrails pipeline**: "Design a system that validates LLM output before showing it to the user. The validation includes: no PII, no hallucinated facts (cite-check against a knowledge base), no toxic content. Latency budget: 500ms total."
- **RAG system for documentation**: "Design a retrieval-augmented generation system for a company's internal docs — 10,000 pages. Users ask questions, the system retrieves relevant docs and generates answers. What's your retrieval strategy?"
- **Model deployment with canary**: "You're deploying a new version of an ML model to production. You can't just swap it — if it's worse, revenue drops. Design a deployment strategy that minimizes risk."

## DevOps / Infrastructure

- **Multi-region deployment**: "Design a deployment for a latency-sensitive app serving users in Asia, EU, and US. Data must be consistent across regions. What's the shape?"
- **Secrets rotation without downtime**: "Design a secrets rotation system — database passwords, API keys — that rotates every 30 days without causing downtime."

## Data Engineering

- **Real-time dashboard pipeline**: "Design a pipeline that ingests 10,000 events/sec, aggregates them by minute, and serves a real-time dashboard. Stale data is worse than no data."
- **Schema evolution**: "Your data pipeline ingests JSON from 50 partners. Each partner changes their schema whenever they want, with no notice. Design the ingestion so your downstream consumers don't break."

## Usage in the interview

1. Router surfaces the candidate's strongest stack.
2. After the single-system retrospective (or if the system is too thin), pick **one scenario** from the matching category.
3. Ask the prompt. Let them think. Probe: "What breaks first?", "What's an alternative you rejected?", "If I change requirement X, what changes?"
4. Each scenario tests 2–3 dimensions simultaneously — you get signal without burning a separate question per dimension.

Related: [[Technical Interview Approaches]], [[Make Decision-Making Visible in Interviews]], [[Problem-Solving Narrative Interview Answers]], [[Decision-Based Interview Answers]]
