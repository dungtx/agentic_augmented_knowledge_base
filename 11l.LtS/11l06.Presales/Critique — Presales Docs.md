# Presales Docs — Critique

> Review of the current presales knowledge base. Focus: missing information and what feels off.

---

## 1. Structural Issues

### 1.1 Sales Pipeline has stage-order problems
- **Closing** is listed *after* Development and Delivery, but closing (contract signing) happens *before* development starts. The current sequence implies you deliver first, then close the deal — which is backwards for ITO.
- **Presale** is listed as a pipeline stage (step 5), but the entire folder is *about* presales. Having "presale" as one step inside "sales pipeline" is confusing. It should be either removed from the pipeline (since it's the meta-concept) or clarified as "presale validation" — the formal technical/commercial check *before* contract.
- **Consulting** and **Demo** are mentioned as separate stages but overlap heavily with the presale validation step. The boundary between "engagement → consulting → demo → presale" is unclear.

### 1.2 Presale Steps vs Sales Pipeline — overlap and no cross-reference
- `Presale Steps.md` describes Presentation → RFI → RFP → Proposal → RFQ/WBS → Negotiation → Contract, which is essentially a *more detailed* version of the Sales Pipeline. The two notes duplicate the same process at different granularities but neither references the other.
- The `Sequence` diagram in Presale Steps stops at Contract — it doesn't connect to what happens after (delivery, upsale), which is where Sales Pipeline picks up. The gap between them is a reader trap.

### 1.3 Lead Generation and Sales Pipeline — where does one end and the other begin?
- Lead Generation describes *how* you get prospects; Sales Pipeline describes *stages* of progress. But Lead Generation's "in-person pitching" and "meeting" overlap with the Pipeline's "Pitching" and "Engagement" stages. No note clarifies the boundary.

---

## 2. Missing Information

### 2.1 No ITO-specific context anywhere
- Every note is written generically. None mention ITO-specific dynamics:
  - **Staff augmentation vs project-based delivery** — fundamentally different presale motions, but absent.
  - **Offshore/nearshore pricing models** — day rate, monthly rate, blended teams — critical to ITO proposals.
  - **SLA structuring** — uptime, response time, escalation paths — mentioned nowhere.
  - **Timezone and language factors** — central to ITO value propositions but invisible.
  - **Compliance certifications** (ISO 27001, SOC 2) — often hard requirements in ITO RFQs.

### 2.2 No competitive positioning
- Service Offering and Value Proposition describe *what* to say, but not *how you differentiate from other ITO vendors*. In a commoditized market, "we have good people" isn't enough.
- Missing: competitor analysis frameworks, win/loss review process, differentiation checklist.

### 2.3 No metrics or KPIs
- No note covers how to measure presale effectiveness:
  - Win rate, pipeline velocity, deal size, sales cycle length, cost of sale.
- Without metrics, there's no feedback loop to improve.

### 2.4 No objection handling
- Presale Skills lists "negotiation and objection handling" as a bullet point but doesn't expand it. In ITO presales, common objections (cost, offshore risk, quality doubt, timezone) are predictable and deserve their own note.

### 2.5 No risk or qualification framework
- There's no concept note for **deal qualification** — how to decide whether to pursue a lead or walk away. Approaches like BANT, MEDDIC, or SPIN are not mentioned.
- No risk assessment for presale investment (how much effort to spend before you know if the deal is real).

### 2.6 No stakeholder map or buying committee
- Enterprise Architecture lists HR, Management, Sales as functions — but these are the *customer's* org, and the note doesn't say that. More critically, there's no concept for **buying committee dynamics**: who sponsors, who blocks, who influences, who signs.

### 2.7 No pricing or commercial note
- RFQ/WBS is mentioned in Presale Steps, but there's no note on **pricing strategy**, **rate cards**, **margin targets**, or **discount authority**. This is a huge gap for ITO presales.

### 2.8 No post-sale handoff concept
- Sales Pipeline includes Delivery and Upsale but no note covers the **presale-to-delivery handoff** — the single most failure-prone transition in ITO. Knowledge transfer, expectation continuity, and SLA alignment all get lost here.

---

## 3. What Feels Off

### 3.1 Customer Persona is too thin
- Two bullet points ("sale-oriented" and "business mindset") barely qualify as a persona. A real persona needs:
  - Role (CTO? VP Engineering? Procurement?)
  - Buying motivations and fears
  - Decision authority level
  - Typical objections
  - Information sources they trust

### 3.2 Enterprise Architecture note is vague
- "HR, Management, Sales, …" could apply to literally any company. It reads as a placeholder, not as useful presale intelligence about how customer orgs are structured and how to navigate them.

### 3.3 Mixed languages
- Service Offering still contains "phân tích" (Vietnamese). Either commit to English or create a bilingual convention. Mixing without explanation is jarring.

### 3.4 Value Proposition is inward-facing
- The three pillars describe what *we* want to say, not what the *customer* needs to hear. A stronger framing would pair each pillar with the customer question it answers:
  - "What do you do?" → Describe SO
  - "Why should I care?" → Fit vs pain point
  - "Why should I trust you?" → Assurance

### 3.5 Presale Skills — "How to get?" is a question, not content
- The heading "How to get?" under Management Skills is still a raw note, not answered. Either flesh it out or mark it explicitly as a open question.

### 3.6 No canonical definitions
- Several terms are used loosely: "presale" vs "presales" vs "pre-sale", "SO" vs "service offering" vs "service portfolio", "pitching" vs "pitch", "proposal" vs "bid". The glossary note should own the definitions but currently only has a link table.

---

## 4. Suggested Additions

| New Note | Why |
|----------|-----|
| Deal Qualification | BANT/MEDDIC frameworks; when to pursue vs walk away |
| Competitive Positioning | How to differentiate in a commodity ITO market |
| Pricing & Commercial Strategy | Rate cards, margin targets, discount authority, WBS pricing |
| Objection Handling | Common ITO objections and rebuttals |
| Presale-to-Delivery Handoff | Knowledge transfer, expectation continuity, SLA alignment |
| Buying Committee Mapping | Sponsor, blocker, influencer, signer dynamics |
| Presale Metrics & KPIs | Win rate, pipeline velocity, cost of sale |
| ITO Service Models | Staff augmentation, project-based, managed services, blended teams |

---

*Generated as critique — not all gaps need immediate filling; prioritize by what blocks your next presale conversation.*