# Interview Playbook — Dao Chan Hung (Ethan)

> **Role**: AI/Frontend Engineer  
> **CV**: `19z.Resources/Cv_Dao_Chan_Hung_FE.pdf`  
> **Track prediction**: Borderline, lean Track 2. Pivot to Track 1 if WebMeet walkthrough shows architectural reasoning.  
> **Date**: 2026-06-29

---

## Pre-interview

- [ ] Check if he researched the company before the interview (Proactiveness indicator)
- [ ] Note: AI tooling section on CV may be inflated — challenge directly

---

## Question Set

### Q1 — Router (~5-7 min)

> **"Walk me through a system you designed or built."**

If he doesn't pick one, guide: *"You mentioned WebMeet on your CV — tell me about that one."*

**Branch rule:** Can he explain *why* (Chime over WebRTC, tradeoffs, seam decisions)? If yes → switch to Track 1 spine. If only *what* → continue below.

**Follow-up ladder** (only use the next rung if he didn't volunteer it — stop when you have enough signal):

| Rung | Follow-up | Ethan-specific angle |
|------|-----------|---------------------|
| 1 | "Why did you structure it that way?" | Does he explain Chime SDK placement, state management choices, or just "the tech lead decided"? |
| 2 | "What tradeoffs did you make?" | Chime SDK (batteries-included, higher cost) vs. WebRTC (cheaper, more control). Did he weigh this? |
| 3 | "What alternative did you seriously consider and reject?" | Can he name an alternative — Agora, Twilio, raw WebRTC? If not, Decision-Range is weak. |
| 4 | "What broke or surprised you after it was built?" | WebMeet had screen sharing + media sync — plenty of failure surface. "Nothing broke" is a red flag. |
| 5 | "Anything you'd do differently now?" | With 5+ years hindsight, can he critique his own work? Bonus: CI/CD pipeline or state management changes. |
| 6 | "How much of the frontend architecture did you drive vs. being handed a spec?" | Did he lead stack decisions, or was he an implementer in a 5-person team? |

**Rung 0** (none needed) = he volunteered *why*, *tradeoffs*, *what broke* unprompted → strong Proactiveness + Systems Thinking. Track 1 territory.

---

### Q2 — Critical Thinking Gate (~8-10 min)

**Part 1:**
> *"Your team is building an AI assistant for the Pochi wallet — a chatbot that helps users understand their transactions, explains gas fees, and answers questions about their balance. The PM says 'just connect it to the LLM and ship it — no filtering needed, it's not giving financial advice, it's just explaining things.' What concerns you?"*

| Listen for | Gate |
|------------|------|
| Flags hallucination risk, prompt injection, PII leakage (wallet addresses/balances), regulatory, "just explaining" is still financial context | **Pass** |
| Names 1-2 generic risks | Borderline |
| Agrees with PM, no concerns | **Fail** |

**Part 2:**
> *"Two hours until the demo. Your AI coding agent — Cursor, which you already use — generated 200 lines implementing this chatbot inside the Pochi app. Walk me through what you check before opening a PR."*

| Listen for | Gate |
|------------|------|
| Specific checks: input sanitization, output validation, adversarial test cases, error handling, flags risk to PM | **Pass** |
| "I'd review the code, test the happy path" — generic | Borderline |
| "I'd accept if it looks correct" or "I trust Cursor" | **Fail** |

---

### Q3 — Adaptability (~3-5 min)

> *"Back to WebMeet. Your US client just had a meeting where 3 enterprise customers said they can't use the platform because it doesn't support real-time captions — some team members are deaf or non-native English speakers. They want it in the next release. You're mid-sprint, nobody has built captioning before. What do you do?"*

| Listen for | Signal |
|------------|--------|
| Checks Chime SDK for built-in transcription, prototypes Web Speech API for MVP, flags latency/cost, scopes pragmatically | **Strong** |
| Researches APIs, estimates effort, brings to sprint planning | Adequate |
| "Never done captioning — someone else should handle it" | Weak |

---

### Q4 — Proactiveness (~5-7 min)

> *"Looking at your projects — WebMeet, Pochi, Kikan — tell me about a feature or piece of work you owned end-to-end. Something you drove from idea to delivery, not just picked up tickets for."*

| Listen for | Signal |
|------------|--------|
| Names concrete outcome, describes non-code work (convincing PM, scoping, deployment), clear ownership | **Strong** |
| Names a feature he drove within his scope, clear but bounded | Adequate |
| Only describes assigned tickets, collaborative language, no "I drove" stories | Weak |

---

### Q5 — Confidence (~3-5 min)

> *"You list AI-assisted engineering as a skill — Cursor, Copilot, MCP, AI agents. But your project descriptions read as standard frontend development. If I'm a customer, I'd look at this and wonder: where does AI actually change how you work? Walk me through it."*

| Listen for | Signal |
|------------|--------|
| Specific workflow example with concrete time savings, acknowledges human judgment still central, not defensive | **Strong** |
| Generic "it speeds things up" — not defensive but shallow | Adequate |
| Gets defensive, marketing answer with no substance | Weak |

---

### Q6 — Optional A: Curiosity Velocity (~3-5 min)

> *"You mentioned researching AI-assisted workflows — Cursor, MCP, AI agents. What's the most interesting thing you've learned from that in the last 6 months — something you went after yourself, not assigned? And what did you do with it?"*

Use if he passed Critical Thinking but was shallow elsewhere. Tests intrinsic motivation.

---

### Q7 — Optional B: Scrappiness (~3-5 min)

> *"Tell me about a time you delivered something with too little time, too little information, or both. Maybe a Pochi feature with a hard dApp Store deadline. What did you do — and what would you do differently with more time?"*

Use if he shows promise but lacks depth elsewhere. Tests resourcefulness + self-critique.

---

## Verdict

| Gate | Result |
|------|--------|
| Critical Thinking | PASS / FAIL |
| Adaptability | Strong / Adequate / Weak |
| Proactiveness | Strong / Adequate / Weak |
| Confidence | Strong / Adequate / Weak |

| Decision Rule |
|---------------|
| Pass Critical Thinking + 2+ Strong | **Hire** |
| Pass Critical Thinking + 1 Strong, rest Adequate | **Hire with reservations** |
| Fail Critical Thinking | **No hire** |

---

## Track 1 fallback (if router passed → switch here)

| Probe | Question (WebMeet-anchored) |
|-------|---------------------------|
| Depth | "What was the hardest technical challenge in WebMeet?" |
| Proactiveness | "How much of the frontend architecture did you drive vs. being handed a spec?" |
| Decision-Range | "You used Chime SDK. What alternative did you seriously consider — WebRTC, Twilio? Why Chime?" |
| Openness | "Tell me about a time you pushed back on the US client — something they wanted that you thought was wrong." |
| Confidence | "I'm a skeptical CTO. I think Chime SDK for WebMeet was overkill — WebRTC with signaling would be cheaper and simpler. Convince me." |
| Adaptability | "New constraint: WebMeet needs 500 concurrent participants per meeting, not 50. What breaks first in your frontend?" |

---

## Related

- [[candidate-evaluation-rubric]]
- [[ai-engineer-interview-protocol]]
- [[Hypothetical Scenario Menu for Technical Interviews]]
- [[Track 2 Interviewer Reference]]
