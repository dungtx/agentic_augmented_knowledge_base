# Interview Rubric — AI/Fullstack Engineer Candidate Evaluation

A structured framework for evaluating engineering candidates beyond technical correctness, focused on how they think — not just what they know. Designed for AI engineer and fullstack roles with vendor-facing responsibilities.

## Language

**Systems Thinking**:
The ability to see the whole system, identify seams, anticipate edge cases and failure modes before anything is built. Breadth + foresight; top-down decision-making instinct.
_Avoid_: Architecture knowledge, design sense

**Critical Thinking**:
Skepticism and pushback — not accepting a design, spec, or AI output at face value. Identifying what "feels wrong" and articulating why. Non-negotiable in LLM-guardrails work.
_Avoid_: Analytical thinking, problem-solving (too broad)

**Depth**:
Persistence on a hard problem — can sit with a complex topic for an extended period without skimming, but knows when to reach out for help. Tenacity + self-awareness.
_Avoid_: Technical skill, expertise

**Expression**:
The ability to articulate reasoning clearly and coherently, both verbally and in text. Not charisma — clarity.
_Avoid_: Communication skills, presentation

**Adaptability**:
Reactive flexibility — adjusting approach when the ground shifts (new stack, new requirements, changed scope). Mandatory for breadth-heavy roles.
_Avoid_: Flexibility, agility

**Openness**:
Curiosity about new ideas, willingness to admit mistakes and learn from them, growth-mindset. Includes self-critique — the ability to identify what one got wrong.
_Avoid_: Humility, coachability (only half the picture)

**Confidence**:
Composure under pressure, especially in vendor-facing or adversarial contexts. Has a floor (not rattled) and a ceiling (presence / commanding the room).
_Avoid_: Charisma, assertiveness

**Proactiveness**:
Self-starting initiative — doing things nobody asked for because they need doing. Includes pre-interview research (did they Google us?) as a cheap early indicator.
_Avoid_: Preparedness (narrower — only pre-interview), initiative

**Decision-Range**:
The habit of considering multiple technical options with pros/cons before committing to one. Does not default to the known tool. Cherry-on-top signal; not expected at all levels.
_Avoid_: Options-thinking, breadth of tools

**Router**:
The systems-thinking walkthrough question that branches the interview into Track 1 (candidate explains _why_) or Track 2 (candidate only describes _what_).

**Track 1**:
Interview path for candidates who pass the router. Gates: Openness → Confidence → Adaptability. Deep probes on remaining dimensions.

**Track 2**:
Interview path for candidates who fail the router. Gate: Critical Thinking. Differentiation via Adaptability, Proactiveness, Confidence.

**Hard Gate**:
A dimension scored pass/fail — if failed, the candidate is rejected regardless of other strengths. Currently: Critical Thinking, Confidence (floor), Adaptability.

**Signal-Collect**:
A dimension scored with narrative observations (2-3 bullets), not pass/fail. Used for differentiation between candidates who pass the hard gates.

**Vendor-Facing Readiness**:
The combination of Confidence (composure) + Expression (clarity) that predicts performance in client meetings. Not a separate dimension — an emergent property of two.

**Router Question**:
The single opening prompt that branches the interview: "Walk me through a system you designed or built." No scaffolding. Follow-up ladder (used only if needed): (1) "Why did you structure it that way?" (2) "What tradeoffs did you make?" (3) "Anything you'd do differently now?" (4) "What broke or surprised you after it was built?" Whether the candidate needs the ladder is itself a Proactiveness signal.

**Openness Gate (Track 1)**:
"Tell me about a time you had to push back on a customer or stakeholder — something they wanted that you believed was wrong. How did you handle it, and what happened?" Tests Critical Thinking + Confidence simultaneously; Openness surfaces in aftermath (do they admit if they were wrong?).

**Confidence Gate (Track 1)**:
Default (Option B): Role-play — candidate proposes a technical solution, interviewer plays skeptical CTO pushing back. "I think it's overkill. Convince me." Fallback (Option A, short on time): Adversarial follow-up to a previous answer — "You said X, but wouldn't that fall apart under Y?"

**Adaptability Gate (Track 1)**:
Piggybacks on the Confidence role-play. After they defend their solution: "New information — the client's data volume is 100x what we assumed, and they need real-time results, not batch. Does your proposal still hold, or what changes?"

**Confidence Probe (Track 2)** [provisional]:
Customer-facing contradiction test: "Earlier you mentioned [A], but a few minutes ago you said [B]. If I'm a customer, I'd find those contradictory. Walk me through how they fit together — as if you're explaining it to me in that room." Tests composure under external scrutiny. Alternate options held in reserve: authority-override (PO demands half the time — what do you cut?), "I don't get it" loop (re-explain from a different angle).

**Track 2 Optional A — Curiosity Velocity**:
"What's the most interesting thing you've learned in the last 6 months — something you went after yourself, not for work or a course requirement? What did you do with it?" Tests intrinsic motivation and active (vs. passive) learning.

**Track 2 Optional B — Scrappiness Under Constraint**:
"Tell me about a time you had to deliver something with too little time, too little information, or both. What did you do — and what would you do differently if you had the time?" Tests resourcefulness, comfort with ambiguity, and self-critique.

**Time Budget (45 min interview, ~40 min usable)**:
- Track 1 (single-system spine): Router 15-18m (woven in: Depth, Proactiveness, Decision-range) → Openness gate 5-7m → Confidence gate 8-10m → Adaptability gate 3-5m. Total 31-40m. Cut none.
- Track 2: Router 5-7m → Critical Thinking gate 8-10m → Adaptability 3-5m → Proactiveness 5-7m → Confidence (provisional) 3-5m → Optional A 3-5m → Optional B 3-5m. Total 24-44m. Optionals A and B used when candidate shows promise but lacks depth elsewhere.

**Decision-Range (Track 1 deep probe)**:
Piggyback on the router walkthrough: "When you built that system, what was an alternative approach you seriously considered but didn't pick? Why didn't you go with it?" Tests whether they actually weighed options in the moment (strong signal) vs. post-hoc rationalization.

**Depth (Track 1 deep probe)**:
"Tell me about a time you had to learn something deeply for a project — something you couldn't just skim from docs or StackOverflow. What was it, why did you need to go deep, and what did you come away with?" Tests proactive intellectual persistence, not reactive debugging. Skip if candidate already volunteered a deep-dive during the router walkthrough.

**Critical Thinking Gate (Track 2)**:
Two-part scenario. Part 1: Risk identification — "We're building a bank chatbot. The team sends every user message directly to the LLM with no guardrails. What concerns you?" Part 2: Action under time pressure — "Your AI coding agent just generated 200 lines implementing this. You have 2 hours. What do you actually do before opening a PR? Walks me through your process." Tests whether critical thinking transfers to behavior when deadlines press and AI is in the loop.
