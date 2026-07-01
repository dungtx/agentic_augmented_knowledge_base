GG# Track 2 Interviewer Reference

A one-page summary for interviewers evaluating mid-to-senior AI/fullstack engineers. Share with your panel so everyone knows what you're looking for.

---

## TL;DR

I'm hiring engineers who **think critically under pressure**. Systems-design experience is a bonus, not a requirement — but the candidate must show they question assumptions, adapt when things change, and take initiative. This sheet covers the core signals for candidates who aren't yet strong at architectural reasoning.

---

## What we're looking for (Track 2 priority order)

| # | Dimension | What it means (simple) | Why it matters |
|---|-----------|------------------------|----------------|
| 1 | **Critical Thinking** | They don't accept things at face value. They push back, spot risks, and ask "what could go wrong?" | Our team builds AI guardrails. An engineer who trusts the LLM blindly is dangerous. |
| 2 | **Adaptability** | When requirements shift, they adjust their approach — not freeze or defend the old plan. | Breadth-heavy work across many stacks. The stack changes every project. |
| 3 | **Proactiveness** | They drive things without being asked. They own outcomes, not just tickets. | Offshore context means limited oversight. Self-starters survive; passengers don't. |
| 4 | **Confidence** | They stay composed when challenged. They can explain their thinking to a skeptical audience. | These engineers face vendor teams and client meetings. Composure matters. |

---

## Example questions

### Router (first question, both tracks)

> *"Walk me through a system you designed or built."*

No scaffolding. Let them pick the system. Note whether they volunteer the *why* (architectural reasoning, tradeoffs, failures) or only describe the *what* (stack, components). If they only give *what*, follow up with: "Why did you structure it that way?" If they still can't explain *why*, they're **Track 2** — proceed below.

### Critical Thinking (the gate — must pass)

> *"We're building a chatbot for a bank. The team sends every user message directly to the LLM with no guardrails, no filtering. What concerns you?"*

**Good answer**: Names specific risks (hallucination, PII leakage, prompt injection, brand damage, regulatory). Bonus: connects risks to concrete mitigations.

**Bad answer**: "Seems fine" or only names one vague risk.

> *Follow-up:* "Your AI coding agent just generated 200 lines implementing this. You have 2 hours. What do you actually do before opening a PR?"

**Good answer**: Describes specific review steps (input validation, adversarial test cases, checking error messages, flagging the deadline risk).

**Bad answer**: "I'd just review the code" with no specifics.

---

### Adaptability

> *"New constraint on that bank chatbot: compliance now wants it to handle mortgage advice — a heavily regulated domain. How does your approach change?"*

**Good answer**: Escalates rigor — mentions regulation, audit trails, disclaimers, narrower response scope, human-in-the-loop. Recognizes the domain shift matters.

**Bad answer**: Treats it the same as before. Doesn't mention regulation.

---

### Proactiveness

> *"Tell me about a feature or piece of work you owned end-to-end — something you drove from idea to delivery, not just picked up tickets."*

**Good answer**: Names a concrete outcome, describes non-code work (unblocking, stakeholder alignment, scope negotiation), takes credit for driving it.

**Bad answer**: Only describes tickets assigned to them. Can't name anything they initiated.

---

### Confidence

> *"Earlier you mentioned [A], but a few minutes ago you said [B]. If I'm a customer, I'd find those contradictory. Walk me through how they fit together."*

**Good answer**: Stays calm. Either reconciles the two points clearly, or admits one was poorly stated. Doesn't get defensive.

**Bad answer**: Freezes, gets frustrated, blames the question, or contradicts themselves again.

---

## Optional: promise-signal probes

Use these for junior candidates who show potential but lack depth elsewhere:

- **Curiosity velocity**: *"What's the most interesting thing you've learned in the last 6 months — something you went after yourself, not for work or a course?"*
- **Scrappiness**: *"Tell me about a time you delivered something with too little time, too little information, or both. What did you do?"*

---

## Verdict guidelines

| If they... | Then |
|-------------|------|
| Pass Critical Thinking + at least 2 of the other 3 | **Hire** |
| Pass Critical Thinking + only 1 other | **Hire with reservations** (discuss) |
| Fail Critical Thinking | **No hire** — non-negotiable |
| Pass everything but shows zero curiosity | **Likely pass** — but check growth velocity |

---

Related: [[ai-engineer-interview-protocol]], [[candidate-evaluation-rubric]], [[Hypothetical Scenario Menu for Technical Interviews]]
