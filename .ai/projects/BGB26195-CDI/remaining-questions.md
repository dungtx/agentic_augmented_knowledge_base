# Remaining questions — BGB26195-CDI

_Generated 2026-07-23. Updated after mining project documents._

## ✅ Answered (from project docs)

### Technical unknowns

- **Tech stack / integration surface:** RESOLVED. Proposed stack: React/Vite SPA → API Gateway/ALB → ECS Fargate microservices (FastAPI core, workflow/approval, calculation engine) → RDS Postgres (row-level tenant isolation) → S3 raw store → Textract OCR → Bedrock (Claude) for field normalization + EF mapping (RAG via Bedrock Knowledge Base/OpenSearch) → Redshift/QuickSight for reporting. CDI's platform has 4 layers (L0 Shared Services: auth/RBAC/org hierarchy, L3 Emission Factor Library, L4 Supplier Engagement Portal, L5 Reporting — "not yet built"). No API specs/contracts for those layers exist yet.
- **Data residency:** OPEN — RFP §5.4 flags this as an open question requiring confirmation. Proposed default region is ap-southeast-1 (Singapore), but not a confirmed legal requirement.
- **Correction feedback loop:** RESOLVED. RFP §4.1.5–4.1.6 and process-flow diagram: supplier reviews AI-extracted values → Accept/Correct/Reject → audit trail keeps both original + corrected values, timestamped, tied to user action → low-confidence fields flagged for mandatory human review.

### Document & OCR

- **Paginated/multi-page bills:** PARTIALLY RESOLVED. RFP §5.2 sets a performance target (<100 pages, ≤5 min processing) implying multi-page support, but no explicit stitching/table-continuation logic described.
- **Low-quality photos/glare/crumpled paper:** RESOLVED AS RISK. Acknowledged in AI Solution doc — lists "clean e-invoices, scans, photos, stamped copies" as format variety, states "OCR quality is the ceiling" — but no specific glare/crumple handling described.
- **Handwritten notes / stamps overlapping fields:** UNANSWERED — gap in all documents.
- **Non-standard documents (credit notes, proforma, partial payments):** UNANSWERED — gap. AI Solution doc scopes only Electricity and Gasoline (VN/EN) so far.

### ESG domain

- **Frameworks:** RESOLVED. Phase 1 = Scope 1 & 2 only, ISO + GHG Protocol. Scope 3 deferred. Architecture also name-drops CBAM, ISO 14064-1, SBTi pathway reporting for export/dashboard layer. No CSRD/ISSB mention.
- **Regulatory shifts during build:** UNANSWERED — not discussed.
- **Who maintains EF database long-term:** IMPLIED. AWS diagram assigns "Cedars Admin: Tenants, EF standards, monitoring" as a role. Mapping doc treats "Framework" as Config-level setting. No formal ownership/governance process documented.
- **Audit trail for ESG data provenance:** RESOLVED. RFP §4.1.10 and §5.7 require full traceability: source document → extracted text → extracted fields → correction → approval → EF mapping → final output, with version history and locking after approval.

### Business

- **Customer base (industries/regions/sizes):** UNANSWERED — not documented.
- **Onboarding latency:** RESOLVED. RFP §5.11: standard supplier onboarding target = 2–3 working days, upper bound = 21 working days (when new templates/custom workflow needed). Max scale: 3,000 suppliers, 10 concurrent users/supplier.
- **Walk-in demo threshold:** UNANSWERED — not documented. Closest artifact: demo JSON output showing a fully-populated electricity-invoice mapping (easy case), but no defined "good enough" bar.

---

## ❌ Still open (need people, not files)

### People & politics
- Who are the key people on CDI's side (champion, decision-maker, blockers)?
- Details on the Singapore contact?
- Any internal dynamics beyond the inherited poor showing?

### Remaining document gaps
- Handwritten notes / stamps overlapping fields — how to handle?
- Non-standard documents (credit notes, proforma, partial payments)
- Paginated bill stitching logic — implementation approach TBD
- Low-quality photo handling — tolerance thresholds, fallback flows

### Business & domain gaps
- CDI's customer base composition — industries, regions, sizes
- Walk-in demo threshold — what's "good enough" for a single-bill ESG snapshot?
- Regulatory shifts during build — any known upcoming changes?
- EF database governance — who owns it long-term, what's the update process?
- Data residency — confirmed legal requirements per country (open question per RFP)
