---
status: fleeting
kind: idea
captured_at: 2026-07-10T15:00:00+07:00
tags: []
needs_review: false
---

Onboarding onto two projects for ZLP (client codename), both for the same product. Role: data engineer with agentic-programming background. Two weeks to ramp via Confluence/Jira docs, with a QA session next week. Need DB credentials and access details.

**Project 1 — Purchase Order Automation (POA):** pharma/logistics domain, 9 markets (Thai largest). AI-powered workflow that processes incoming emails and purchase order PDFs — VLM extracts data from forms (tricky: handwriting, unknown languages, schema extraction from varied layouts). AI alone isn't enough for Thai annotations. Extracted data validated against SAP, then forwarded to an ecommerce system. Main flows: customer matching and material matching. Material matching is harder: find an item from the PO in internal data sources. Problematic edge cases — items not found, name mismatches between item and material names, different customer-specific naming, poorly maintained DB, multiple similar products returned. Long but not deeply complex flow. Also handles invoices and EZRX (internal system). Stack: PostgreSQL, SAP, BigQuery (recently added). Existing data pipeline already in place. SAP has many APIs that need access.

**Project 2 — Workato-to-Airflow Migration:** separate project, same product. Migrating existing pipelines from Workato (legacy, costly) to Airflow. Workato stores pipeline logic as JSON with heavy GUI metadata — most of it noise that burns context when fed to an LLM. Strategy appears to be either static pre-extraction of the useful skeleton (first ~100 lines), or a specialized prompt to filter out cruft. A SKILL exists for Workato-json-to-Airflow mapping, and mapping is the hardest step. Migration approach: side-by-side lift-and-shift onto prod, write to a new sink, compare against live data — match = success. Vibe-coding attempts have been painful. Agent needs external credentials to verify data integrity. Core challenge: prod migration safety.
