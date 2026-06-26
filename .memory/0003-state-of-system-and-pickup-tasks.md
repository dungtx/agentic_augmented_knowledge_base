# State of the System & Pickup Tasks (master handoff)

> **Purpose:** Read this first. Any new agent picking up the "knowledge base secretary" work starts here, knows what's built, what's stub, what's broken, and what to do next — without the user repeating themselves.
> **Date:** 2026-06-26 (end of grilling session 3)
> **User's standing instruction:** *"I want to be able to say 'let's continue building full AGENTS.md' and the agent will know what we built, the shortcomings, and as much info as possible so I don't repeat myself."*
> **Companion files (read in this order if you need depth):**
> 1. `0001-secretary-subagent-design-grilling-session.md` — full grilling session 1 record (intent, vault context, original Q-tree).
> 2. `0002-capture-fleeting-minimalist-requirements.md` — locked decisions D1–D15, B/C defaults, out-of-scope, remaining-grilling tree.
> 3. This file — current state + per-task pickup briefs.

---

## 1. What exists in the vault right now (ground truth)

### 1.1 Built and committed (working)

- **`AGENTS.md`** (vault root) — **STUB.** Secretary skeleton. Contains: 1-paragraph secretary persona ("lossy" capture bias), vault-layout lane definitions, dispatch rule (fragment → load `capture-fleeting`; ambiguity gate → one question, non-capture-answer = treat as normal request, do NOT capture), skills roadmap table. Explicit stub-note flag pointing at this `.memory/` for remaining work.
- **`.pi/skills/capture-fleeting/SKILL.md`** — **BUILT, TESTED.** Model-invoked (auto-invokable). 4-step workflow: confirm capture intent → jog clear (one-at-a-time questions, hints from `rg`-vault first then model knowledge, max 3) → write (`11a1.Inbox/YYYYMMDDHHmm-slug.md`, frontmatter `status/captured_at/tags/needs_review`, preview-then-write) → loop/end. Guardrail list of things it never does (promote/triage/tag/link/SRS/out-of-Inbox/.memory+`.ai`). Frontmatter valid: name `capture-fleeting`, desc 428 chars, `disable-model-invocation` absent.
- **`.memory/`** — **APPEND-LOG IN USE.** Files: `0001-…-grilling-session.md`, `0002-…-requirements.md`, this `0003-…` handoff. Convention: `NNNN-slug.md`, chronological. (A `facts.md` flat-summary file was *proposed* in `0001` but NOT built — see task T6.)
- **`.pi/settings.json`** — pre-existing subagent model overrides. Untouched.
- **`.gitignore`** — ignores `.atl/` (pi runtime), Obsidian `workspace.json` + plugin data + `.cache` (machine-local), `.DS_Store`, `Thumbs.db`.
- **`19z.Resources/`** — cloned external repos (skills-main, market-my-spec, codemyspec), committed snapshot-style. No submodules..flag: see §S1 shortcoming.
- **Existing vault content** committed: all of `11a.Capture/`, `11l.LtS/`, `19z.Resources/`. Example real capture note produced by skill: `11a.Capture/11a1.Inbox/202606261148-cedar-cdi-bid-preproposal.md` (Cedar/CDI deal — see §3 for why it matters).

### 1.2 NOT built (stubbed, planned, or pinned)

- **`distill-permanent` skill** — not built. Planned. (See task T2.)
- **`morning-review` skill** — not built. Planned. (See task T3.)
- **Full `AGENTS.md` vision** — stub only. (See task T1.)
- **`.ai/` directory** — does not exist. (See task T7.)
- **`.memory/facts.md`** — does not exist. (See task T6.)
- **SRS integration for `11a3.Someday/`** — pinned, not built. (See task T8.)
- **19y.Relics/ lane** — referenced in grilling as "supersession-only" but never created. (No action yet.)

### 1.3 Untracked (NOT created by this agent — DO NOT COMMIT)

Per user instruction 2026-06-26: these were created by another agent in a parallel session and are that agent's responsibility to commit:
- `11a.Capture/11a1.Inbox/202606261641-technical-interview-prep-playbook.md`
- `11a.Capture/11a1.Inbox/202606261725-mudah-emergency-bid-context.md`
- `11a.Capture/11a1.Inbox/202606261725-ai-engineer-candidate-rubric.md` (timestamp drift may exist; recheck at pickup time)
- `11l.LtS/11l07.Career/` (new permanent-note lane)

**Rule for any agent picking up:** if you see untracked files you didn't create, *ask the user before committing them*. Provenance discipline (W14).

### 1.4 Git state

- Remote: `git@github.com:dungtx/agentic_augmented_knowledge_base.git`, branch `main`, tracking `origin/main`.
- Author config saved in repo: `user.name=dante`, `user.email=dungtx3@vmogroup.com`.
- Last commit: `5a0b532` "Relabel Japanese Dailies as kind:task…".
- Commit style: scoped subject + body explaining decisions. All commits so far authored as `dante`.

---

## 2. Locked decisions (carry forward, do NOT re-grill)

| ID | Decision | Source |
|----|----------|--------|
| D1 | Architecture = `AGENTS.md` (always-on, vault root) + auto-invokable skills. | Q1 |
| D2 | Auto-invocation ENABLED (`disable-model-invocation` NOT set) on every skill. Manual `/skill:name` fallback always available. Defense-in-depth: aggressive descriptions + AGENTS.md restates dispatch + manual fallback, because pi docs say "models don't always auto-invoke." | Q1/2 |
| D3 | Dispatch strength = strong w/ **one-question confirmation gate**. Capture-biased ("lossy": false-pos = deletable, false-neg = lost idea). Non-capture answer = exit skill, treat as normal request, do NOT capture. | Q2 (refined 2026-06-26) |
| D4 | Capture destination = `11a1.Inbox/` (unified). No `11a0.Fleeting/` folder; "two pipelines" rigor deferred. | Q3 |
| D5 | No classification at capture time. Capture dumb+fast; triage & promotion are distill's job. | Q3 |
| D6 | Inbox horizon ≈ 24h (target, not hard delete). Slipping a day ≠ failure; chronic slipping = signal to run distill. Distill reports backlog age, never nukes. | Q3 |
| D7 | `11a2.Deferred/` = important-not-urgent. `11a3.Someday/` = nice-to-have idea resurfacing. Current items = first distill practice batch. | Q4a |
| D8 | Capture always → `11a1.Inbox/`. NEVER routes directly to Deferred/Someday. | Q4b |
| D9 | SRS = surfacing frequency ONLY, never priority taxonomy. Do NOT repurpose Anki buttons for urgency. | Q5 |
| D10 | Inbox is NOT an Anki deck. Capture skill is SRS-coupling-free. | Q5 |
| D11 | Someday + permanent knowledge are *candidates* for future SRS deck via `obsidian-spaced-repetition` plugin, folder-scoped to `11a3.Someday/`. Integrated in distill, not capture. | Q5 |
| D12 | SRS for permanent notes → PINNED for later. Preferred mechanism = AI retrieval (semantic search of LtS via `.ai/`+`.memory/`), NOT timer-based SRS. | Q5 |
| D13 | Three skills on roadmap: `capture-fleeting` (built), `distill-permanent` (planned), `morning-review` (planned). | Q6 |
| D14 | `morning-review` fires **consent-first**: only on trigger phrase OR explicit yes/no offer at session start. NEVER auto-hijacks. | Q6 |
| D15 | Minimalist capture skill = NO morning-review, NO SRS, NO retrieval. Only: listen → clarify one-at-a-time w/ hints → write Inbox note → ask "another or done?" → exit. | Q6 |
| D16 (new) | **Live mode** is the user's preferred capture variant — write directly without the question gate, batch clarification questions for the end. Currently NOT in the skill; user requested it be grilled as a possible branch. See task T4. | Observed 2026-06-26 |
| D17 (new) | Frontmatter gains an orthogonal **`kind:`** field for classification (`idea` \| `task` \| `routine` \| `lit-note`), separate from **`status:`** (`fleeting` \| `distilled` \| `discarded`). `status` = where in the fleeting lifecycle; `kind` = what category the item is. Don't conflate — orthogonal axes. Applied 2026-06-26: `capture-fleeting` skill now emits `kind: idea` by default; triage/distill may reassign. | Locked 2026-06-26 (Inbox cleanup) |

### 2.1 B/C defaults accepted (no vetoes)

B1 preview-then-write · B2 "another fragment, or done?" exit · B3 bundle if clearly one fragment, ask if ambiguous · B4 no `[[wikilinks]]` at capture (link at distill) · C1 frontmatter = `status`/`captured_at`/`tags`/`needs_review` **+ `kind` (D17, added 2026-06-26; default `idea`)** · C2 filename `YYYYMMDDHHmm-slug.md` · C3 max 3 clarifying questions/fragment · N6 timezone `+07:00`.

### 2.2 Skill-writing framework (use for ALL future skill work)

User invoked **`mp-writing-great-skills`** and it is the canonical guide for writing/tuning any `SKILL.md`. GLOSSARY at `~/.pi/agent/skills/mattpocock-skills/skills/productivity/writing-great-skills/GLOSSARY.md`. Key levers used so far: **model-invoked** (keep description), **leading words** (`fleeting`, `jog`, `lossy`), **steps-primary** with **checkable completion criteria** ("Done when…"), **co-location**, **single source of truth** guardrail list, avoid **no-ops**/**duplication**/**sediment**/**sprawl**/**premature-completion**.

---

## 3. Worked examples and seeds (worth knowing about)

### 3.1 The CDI note — first real capture-session via the skill

`11a.Capture/11a1.Inbox/202606261148-cedar-cdi-bid-preproposal.md` ( Cedar / codename **CDI** ). Key facts in it:

- Cedar = 3rd-party org building a **SaaS to track CO2 emissions**; phase 1 = oil + electricity usage metrics, expand later.
- AI-led delivery, phase 1.1 = quick AI-led prototype. AI engineer = **resource ask**.
- Customer cares: OCR, AI cost, reliability of data sourcing/parsing, data accuracy.
- Champion = CSTO on **6-mo probation, needs results in 3 mo**; unnamed (sales-owned); working style = review-via-collaboration; will join our hiring interviews for the AI engineer.
- Delivery: DevOps on customer side (CI/CD-experienced).
- Next step (user's): submit tentative cost for AI tooling + OCR. Budget open. User owns the AI+OCR cost lines.
- OCR is **multilingual** (VN start, SEA expansion) — handwriting variance flagged.
- Customer has **low AI knowledge** → open design question: **how does a human review AI-extracted data? Verification gates.**
- Relationship: worked with our company before, trust-but-measured. Competitors = sales-owned, out of user's scope.
- Stage = **pre-prep, future-reference**; user on waiting list, not active presales.

**Distill seed flagged for T2:** the CDI note is a candidate to split into **two** permanent notes: (a) the **deal** → `11l.LtS/11l06.Presales/` (deal-qualification lane); (b) **human-in-the-loop verification design for AI extraction** → `11l.LtS/11l05.AI/` (novel content, no existing note covers it). The user explicitly raised the verification-gates question — it's a real knowledge seed.

### 3.2 The Android lockout-gate note — merge-from-two example

`11a.Capture/11a1.Inbox/202606261200-android-lockout-gate-jp-output-practice.md`. Born 2026-06-26 from *merging* two old Inbox fragments (`Japanese writing app idea.md` + `Just start app idea.md`) which were always two faces of one idea. Demonstrates the dedup-not-supersession cleanup pattern (W15): originals deleted, no Relics entry. Content: Android lockout-gate app, MVP = JP daily output practice (1 sentence-to-say no-repeat + 1 sentence with new word/grammar), writing-only, bypass with escalating difficulty, future scope = reader/Anki/podcast hooks. Fleeting idea; not yet committed to build.

### 3.3 The Japanese Dailies task — relabel example

`11a.Capture/11a1.Inbox/Japanese Dailies.md` relabeled 2026-06-26 from a bare routine list to `kind: task, status: fleeting` — task = workshop the raw floor into a real worst-day/best-day routine, then promote via distill. First applied example of the D17 `kind:` field. Body preserved as raw sketch; workshop goal added.

Note was created in **hybrid mode**: gated clarifying questions for the first 3 fragments, then the user said "skip questions for now, treating this as a live note-taking first, ask questions afterward." That lived-mode invocation is the basis for D16 / task T4.

---

## 4. Bad-practice warnings issued (do NOT re-issue, do NOT regress)

W1–W13 from sessions 1–2 (see `0002 §10`): autodelivery-as-guaranteed · passive capture friction · classify-at-capture · Relics-as-junk-drawer · SRS-buttons-as-priority · SRS-on-Inbox · "I-was-busy" backlog-rot · morning-review auto-hijack.

**W14 (new 2026-06-26):** agents committing files they did not create. *Always ask the user before committing files you didn't write in this session* — provenance discipline (an untracked file may belong to a parallel agent session).

**W15 (new 2026-06-26, Inbox cleanup):** keeping two capture fragments as two notes when they were always two faces of one idea — duplicates calcify. Merge instead. Reserved `19y.Relics/` for *supersession* (X replaced by Y), NOT for *dedup* (these were always one idea) — distinguish the two. (Also: don't bolt a new value onto `status` to mean 'category'; orthogonal `kind:` field is the disciplined move.)

---

## 5. PICKUP TASKS — what any agent can do next, with briefs

Each task is self-contained: an agent told "do T2" (or "continue building full AGENTS.md" → T1) should have everything it needs below. **All tasks require the grilling skill (mp-grilling) interaction discipline: one question at a time, recommendation each go, flag bad practices inline, walk a branch before building.**

### T1 — Build the full `AGENTS.md` (probably what "let's continue building full AGENTS.md" means)

**Current state:** stub only — 1-paragraph persona, lane definitions, dispatch rule, roadmap table. ~30 lines.
**Goal:** replace the stub with a full secretary definition, *still tight* (AGENTS.md = always-on context, pays load every turn → prune per `writing-great-skills`).
**Must contain (grill these one at a time before writing):**
- Full vault vision in the user's own words — what this vault is FOR. (Currently a placeholder. The user is new to note-taking; the vision must be honest about that and not over-engineer.)
- Persona/voice of the secretary (terse? socratic? B2B-fluent since the user captures deals?).
- Refined dispatch rules for all three skills (capture built, distill + morning-review planned — rules can be written ahead of skill existence).
- `.memory/` policy block — see T6.
- `.ai/` index block — see T7. Likely imported via pi `@` mechanism (T9).
- Maybe: explicit "live mode" trigger word, if T4 lands it as a skill branch.
**Grilling questions to walk (in order):**
1. What is this vault FOR in your own words? (one sentence, then refine)
2. When you picture the secretary talking back to you, what's its voice? (terse/socratic/coach-like)
3. Should the secretary *proactively* point out backlog age ("you have 3 inbox notes > 24h") or stay silent until asked?
4. Should the secretary know your domain (Presales/AI/Linux) and use that vocabulary, or stay domain-agnostic?
**WARNING before writing:** resolve whether `AGENTS.md` should `@`-import `.ai/*` files (pi include mechanism — see T9). If yes, design the import structure with the user; if no, inline tight summaries. Do not bloat the always-on layer.

### T2 — Build the `distill-permanent` skill

**Current state:** not built. Most-valuable next skill (capture works, distill doesn't — pipeline ends at Inbox).
**Goal:** review a fleeting note → produce an atomic zettelkasten permanent note in `11l.LtS/`, with classification (task/fleeting/lit-note — see D5), tags, `[[wikilinks]]`, placed by domain (or `Kasten/` flat layer for ambiguous — to be decided in grilling).
**Grilling questions to walk (from `0002 §9`):**
- Q4 (fleeting lifecycle): after distillation, archive original to `11a0.Fleeting/_processed/` (if it exists) or hard-delete? **Recommended:** archive-supersede, never delete knowledge capture (bad practice: deleting a captured thought).
- Q5 (fleeting structure refactor?): should distill rewrite the *frontmatter* of the source fleeting note (set `status: distilled`, link to permanent note)? Recommended yes.
- Q7 (permanent-note placement): domain subfolder vs flat `Kasten/` layer for ambiguous ideas? Existing vault uses domain folders but classic zettelkasten says link-graph over folders. Flag as hybrid decision.
- Q8 (atomicity): one-idea-per-note vs topic-cluster? **Recommend ONE-idea-per-note (classic zettelkasten);** existing LtS notes are cluster-length — flag and ask if user wants to refactor or hybrid.
- Q9 (permanent note naming): `YYYYMMDDHHmm-slug.md` (consistent with capture) vs Luhmann-branch-ID vs title-with-space (existing `Customer Persona.md`)? **Recommend date-prefix slug.** Reject title-with-space (breaks shell/URLs).
- Q10 (linking convention): `[[free-title]]` vs `[[slug|alias]]`? **Recommend link by slug, alias for display** when slug is stiff.
- Q11 (MOC handling): root MOC only vs per-domain MOC + root index-of-MOCs? Existing: root `11l.LtS/MOC.md` (minimal) + Presales glossary working as a domain MOC. **Recommend per-domain MOC + root index.**
- Q-SRS-for-Someday: integrate `obsidian-spaced-repetition` folder-scoped to `11a3.Someday/` as part of distill, or separate? (D11.) Recommend: distill can tag a note as `srs-eligible` when promoting to Someday; plugin config is a follow-up task T8.
- Q-AI-retrieval-for-LtS: per D12, retrieval beats SRS for permanent notes. Design how `.ai/` indexes LtS for retrieval (semantic-ish `rg` over note titles + `[[links]]`). Couples with T7.
**Practice warnings to give inline:**
- Atomicity: one idea = one note. Clusters kill the link graph.
- Permanent notes are written in your own words, not copy-pasted — that's the *understanding test*.
- Titles should be *claims*, not topics ("OCR fails on mixed-script SEA handwriting" > "OCR notes").
**Test case ready:** the CDI note (`202606261148-cedar-cdi-bid-preproposal.md`) → two candidate outputs: deal note under Presales + verification-gates permanent note under `11l05.AI/`. Use it as the worked example during grilling.

### T3 — Build the `morning-review` skill

**Current state:** not built.
**Goal:** consent-first morning triage of Inbox; surfaces related Deferred/Someday items by topic. See D14.
**Grilling questions:**
- Triage-loop mechanics: one item at a time vs grouped by topic? Recommend grouped-by-topic (cross-lane surfacing is the value-add).
- Cross-lane surfacing: when reviewing an Inbox item, `rg` the vault for related Deferred/Someday items — show as a "related:" block. Recommendation yes (D14 says cross-lane surfacing is *core*, not enhancement).
- Consent-fire vocabulary: what trigger phrases fire morning-review? ("start my day", "morning", "triage inbox", `/skill:morning-review`). Also: should AGENTS.md ask an explicit yes/no "4 inbox items need triage, run morning-review?" at session start? Recommend yes-offer (NOT auto-fire).
- What counts as "morning"? Real time-of-day or any session-start? Recommend any session-start (user might work at night, agent shouldn't gate on clock).
**Practice warnings:**
- W7 auto-hijack rejected — consent only.
- Triage is decision-time, not capture-time; here classification *does* happen (vs D5 at capture).

### T4 — Grill "live mode" as a `capture-fleeting` branch

**Current state:** observed user behavior, not in skill.
**Goal:** allow `/skill:capture-fleeting live` OR a trigger word that puts the skill into write-now / batch-questions-at-end mode.
**Grilling questions:**
- Should live mode be a *branch* of `capture-fleeting` (per `writing-great-skills` branching) or a separate skill? Recommend branch (same leading word, same destination, just different question-timing) — disclose the live-mode rules behind a context pointer.
- Exit-signal for the question batch: "done" already works; questions get emitted *then*. Confirm.
- Should `needs_review: true` always be set in live mode (since clarification was deferred)? Recommend yes — same semantic as budget-exhausted.
- Should live mode be the *default* (user clearly prefers it) or opt-in? Recommend opt-in via explicit `live` arg/trigger (gated mode is safer default for new users; user is the only user and can default-live later if it stabilizes).

### T5 — The 15–20 note-taking concept walkthrough (user's original ask #4)

**Current state:** not delivered. User explicitly requested this at END of full grilling. List drafted in `0001 §7` (non-exhaustive).
**Goal:** conversational explanation of 15–20 concepts with integration suggestions into *this* vault.
**Draft list to refine (~17):** zettelkasten · fleeting/literature/permanent notes · atomicity · map of content (MOC) · index cards · link graph vs folder hierarchy · PARA vs Zettelkasten vs GTD · progressive summarization · evergreen notes (Andy Matuschak) · titles-as-claims · daily note log · tags vs links · "second brain" (Forte) · collector's fallacy · commonplace book · anti-library · **plus 2 observed from this user's journey**: verification-gates-for-AI-output (CDI seed) + SRS-for-surfacing-vs-retrieval-for-finding (D9/D12 — user invented this distinction, worth crystalizing).
**Practice warnings to weave in:** collector's fallacy (stop hoarding, start processing — presently a real risk in their `Deferred/`); "I was busy" backlog rot (already W12); title-with-space filenames break shell + URLs (Q9).
**Delivery format:** deliver conversationally in chat with the user. Also write a permanent reference note `11l.LtS/11l05.AI/note-taking-concepts.md` (or a new `11l00.KM/` lane?) so the lecture doesn't have to be re-delivered.

### T6 — Define and create `.memory/facts.md` (the flat summary)

**Current state:** `.memory/` is append-log only (this file is `0003-`). `0001` proposed a `facts.md` flat summary that any agent reads first. Not built.
**Goal:** create `facts.md` = a flat, rewritten-each-session summary of who the user is, what's built, what's pinned. The append-log stays as the timeline; `facts.md` is the *current snapshot*.
**Grilling questions:**
- Append-log + facts.md (two-file model) vs just the log (timeline only)? **Recommend both** — log = history, facts.md = "answer me now" snapshot for fast agent bootstrap.
- Who rewrites facts.md? Auto at session end, or on-demand? Recommend: on-demand (next agent that does a substantive task rewrites it to reflect new state) — explicit, not magical.

### T7 — Define and create `.ai/`

**Current state:** empty. User's stated vision: "agent-focused lessons learned or quick retrieval."
**Goal:** populate `.ai/` with cheat-sheets the agent reads on demand. Candidate files:
- `.ai/vault-conventions.md` (frontmatter schema, filename patterns, lane definitions — distilled from `0002`).
- `.ai/zettelkasten-cheatsheet.md` (the 15–20 concepts from T5, condensed).
- `.ai/skill-dispatch-map.md` (fire rules for each skill — mirrors AGENTS.md dispatch section).
- `.ai/retrieval-index.md` (per D12 — an index of LtS note titles + tags + 1-line summaries for AI retrieval; could be auto-generated).
**Grilling questions:**
- Which of these does AGENTS.md `@`-import (always-on) vs which sit dormant until an agent `read`s them? **Recommend: AGENTS.md imports `vault-conventions.md` + `skill-dispatch-map.md`; `zettelkasten-cheatsheet.md` + `retrieval-index.md` are read on-demand** (cheatsheet when distill runs; retrieval-index when user asks "anything on X").
- Auto-generate `retrieval-index.md` via a script, or hand-maintain? Recommend hand-maintain for now (script later) — quality > automation at this vault's size.

### T8 — Set up SRS for `11a3.Someday/`

**Current state:** pinned (D11). Plugin: `obsidian-spaced-repetition` (St3v3n-D). Not installed/configured.
**Goal:** folder-scoped SRS deck for Someday, with review-as-triage semantics (Good=longer interval, Easy=much longer, Again/Hard=resurface soon, Suspend=drop, "became a project"=move out of Someday + remove from SRS).
**Grilling questions:**
- Before enabling, distill the existing ~3 Someday items into proper note shapes (each needs: idea / why interesting / what acting-on-it looks like). That's a distill-skill job — *couple with T2*.
- Folder-scoped vs tag-scoped? **Recommend folder-scoped** (Johnny-decimal geography already encodes scope).
- How often does the user actually review? Honest cadence question — if they won't show up weekly, SRS is theatre.

### T9 — Verify pi `@`-import / AGENTS.md include mechanism

**Current state:** unknown. `0001` flagged this as an unresolved pi-mechanism question.
**Goal:** check whether pi supports `@path/to/file.md` or similar import in `AGENTS.md`, so always-on context can pull `.ai/*` files instead of inlining them.
**Action (no grilling needed — pure research):** read `docs/extensions.md` (at `/nix/store/w5a7pz01ds7aj3ldllmc0nyqfdnj852g-pi-0.79.1/lib/node_modules/@earendil-works/pi-coding-agent/docs/extensions.md`) and any `AGENTS.md`-specific docs. Verify the include syntax. Write the result into `.memory/` as a short note (`0004-pi-import-mechanism.md`) so no future agent re-researches it. This unblocks T1 + T7.

---

## 6. Suggested ordering if the user says "continue"

- **"continue building full AGENTS.md"** → T9 first (unblock), then T1.
- **"continue the grilling"** → T2 (distill — biggest value gap).
- **"add live mode to capture"** → T4 (small, frees friction).
- **"teach me note-taking"** → T5.
- **Just "continue" with no target** → recommend T9 → T1 → T2 → T4 → T5 → then T3 / T6 / T7 / T8 in any order. Reasoning: unblock (T9) → strengthen the brain (T1) → close the pipeline (T2) → small UX win (T4) → fulfill user's explicit deferred ask (T5). The rest are enhancements.

---

## 7. Interaction discipline any picking-up agent MUST follow

- **One question at a time.** Recommended answer each go. Flag bad practices inline. This is the `mp-grilling` skill — invocation stored in `~/.pi/agent/skills/mattpocock-skills/skills/productivity/grilling/SKILL.md`.
- **Use `mp-writing-great-skills`** when writing any `SKILL.md`. GLOSSARY at `…/writing-great-skills/GLOSSARY.md`.
- **Never commit files you didn't create in your own session** (W14).
- **Auto-invocation is probable, not guaranteed** (D2). When building a skill, write aggressive descriptions AND restate dispatch in AGENTS.md.
- **Capture is lossy** — bias toward capturing, never toward dropping. (D3.)
- **Two pipelines, not one** — GTD (tasks/links/someday) and zettelkasten (knowledge). Don't smush.
- **Don't classify at capture; classify at distill/triage.** (D5.)
- **Author git config already set**: `dante <dungtx3@vmogroup.com>`.

---

*End of grilling session 3. 9 pickup tasks (T1–T9), 1 new locked decision (D16), 1 new warning (W14), CDI worked example captured in §3. Repo at `a5856be`.*