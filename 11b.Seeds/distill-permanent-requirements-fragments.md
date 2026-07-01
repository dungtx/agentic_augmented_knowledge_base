# Fragments: what does the distill-permanent skill need?

> Concept: "What does the distill-permanent skill need?" — a question-driven exploration of its requirements, design constraints, and what it must do (and not do) to turn a seed into a permanent zettelkasten note in `11l.LtS/`.
> This is raw quarry material. Drift is expected and marked. concept-refine will filter.

---

The distill-permanent skill sits at the end of the pipeline: capture-fleeting → seed-inbox → distill-permanent. It's the gate where rough thinking becomes permanent knowledge. If capture is lossy by nature (miss a thought, it's gone), distill is the opposite problem: include the wrong thing or the wrong way, and the permanent record gets cluttered. The cost of a bad permanent note is higher than the cost of a missed capture, because you have to live with it and build on it.

---

Atomicity: a permanent note should contain one idea or concept. It can hold supporting material (examples, context, implications), but everything must centralize on that one idea. Not a cluster, not a tour of related thoughts — one gravitational center. If a seed contains multiple distinct ideas, it spawns multiple permanent notes, each atomic.

---

Summary-first: every permanent note opens with a summary at the top — the "what future-me needs to know in 10 seconds" version. The full note is for lookup; the summary is for scanning. The seed-inbox process already did the substantive rewrite, so distill-permanent doesn't re-rewrite the body. But it does extract or sharpen a summary from the seed, framed as "if I stumble on this note in 6 months, what's the one-paragraph version that tells me whether to read further?"

---

Mandatory linking: tags and an "up" link are non-negotiable. Tags situate the note in a controlled vocabulary. The "up" link points to a parent — an MOC, a domain overview, a broader concept this note is a piece of. This is what weaves the note into the graph. Without it, the note is an orphan; with it, the note is reachable.

---

Discoverability for agents: the permanent notes need to be findable by agents during conversations. When the user discusses a topic, the agent should be able to surface relevant permanent notes — by keyword match, by tag, by semantic adjacency. This means the summary, tags, and keywords in frontmatter are not just for human browsing; they're the retrieval surface for AI lookups. The frontmatter is a search index.

---

The agent as writing partner and editor: during distill-permanent, the agent doesn't just execute instructions — it actively suggests split points when it sees multiple ideas in a seed, and challenges the user's split decisions if it thinks they weaken atomicity. "This feels like two notes — the X part and the Y part. If we keep them combined, future-you searching for Y won't find it under X's summary. Split?" The agent is a meticulous editor who cares about the permanent record as much as the user does. Not adversarial, but willing to push back with reasoning.

---

Parent links (the "up" links): a permanent note can have multiple parents. Valid parents are:
- Domain MOCs (e.g. `[[../MOC|Presales MOC]]`)
- Concept MOCs that span domains (e.g. `[[Verification MOC]]`)
- Other permanent notes that sit above this one in scope — a "bigger idea" note that this note is a detail of
- NOT folders — the domain MOC covers that role; the folder is just organization, not semantics

The agent must propose parent links for each note. If the seed came from a domain and touches a cross-cutting concept, the agent should propose both the domain MOC and the concept MOC (creating the concept MOC if it doesn't exist yet). A note without at least one parent link is an orphan — invalid.

---

Retrieval happens at conversation time, not at distill time. The agent working with the user later (hours, days, months later) is the one that searches the vault. Distill-permanent's job is to make that retrieval fast and accurate — by writing strong summaries, precise tags, and good keywords in frontmatter. The permanent notes are the index; the agent at conversation time is the query engine. Question: what retrieval mechanism? Grep over keywords? Semantic search via embeddings? The agent reading candidate notes and judging relevance?

---

SQLite as a vector store — problems that can arise:

1. Embedding model dependency. You need a local model (e.g. all-MiniLM-L6-v2 via sentence-transformers, requiring Python) or an API call (needs network). The vault is local-first. Either way, distill-permanent now depends on something outside the vault.

2. The stale-index problem. If the agent embeds at distill time but you later edit the note in Obsidian, the stored vector is wrong. You need either a file-watcher daemon (complex, always-running), a git hook (only catches committed changes), or accepting stale vectors until a manual reindex. Manual reindex means retrieval silently degrades and you don't know when.

3. Pi/tool integration friction. Pi runs bash commands fine, but embedding is a Python invocation (`python embed.py`). Adds latency to every distill operation. A long-running watcher process is out of character for a CLI-based agent.

4. DB placement ambiguity. SQLite file in the vault? Syncs with everything else (bloat). In `.ai/`? Agent-only, not portable. Outside the vault? Not self-contained.

5. The real bottleneck is note quality, not retrieval technology. A good summary embeds well. A bad summary embeds badly. Embeddings amplify the note quality you already have — they don't compensate for weak writing. If the vault has 50 sparse notes, embeddings won't fix them; if it has 50 well-summarized notes, grep already finds them.

6. Scaling problem that doesn't exist yet. Option B (rg + agent reads + LLM judges relevance) works at 0–200 notes. Adding SQLite before retrieval actually breaks is solving a problem you haven't experienced. When grep starts missing notes that embeddings would catch, you'll know exactly what query patterns fail — and can design the embedding system to target those real failures.

---

Decision: hybrid approach. Start with Option B (grep + agent reads). But structure the permanent note frontmatter so adding embeddings later is painless — include a `summary` field tuned for both human scanning and vector quality, plus `keywords` and `tags` as grep targets. If embeddings get added later, the summary is already embedding-ready; just pipe it through a model and store the vector. No premature SQLite, just the right fields from day one.

---

Seed lifecycle after promotion: archive to `11b.Seeds/_processed/<slug>.md` with `status: distilled` and a `permanent_note` wikilink pointing to the new note(s). Mirrors the capture→seed pattern: the original survives, backlinked, traceable. Never delete the seed — the provenance chain (capture → seed → permanent) is the vault's intellectual history.

---

Permanent note frontmatter: only keep what's needed. The seed frontmatter carries fields that made sense for a rough draft (`seed_level`, etc.) — those die at the gate. What belongs on a permanent note? `status: permanent` replaces `status: seed`. `kind` probably stays (classifying idea vs lit-note is still useful for filtering). `captured_at` keeps the origin timestamp. `seeded_at` — provenance or clutter? `source` points to the archived seed. `tags` and `keywords` stay, mandatory. New: `summary` (the scan-line), `parents` (array of wikilinks to MOCs/parent notes), `distilled_at` (promotion timestamp).

---

Frontmatter decision: keep status, kind, source, tags, keywords, summary, parents. Drop captured_at, seeded_at, seed_level, distilled_at. Seven fields total — tight, each earns its place. `source` points to the archived seed (not the original capture — that chain is seed→capture, permanent→seed, traceable through the backlinks).

---

Placement: flat in `11l.LtS/` for now. No domain subfolders — the user will add them when categories emerge organically from real notes, not upfront taxonomy design. The folder is storage; the MOC is structure. The agent's job is MOC-level organization: decide which MOC(s) this note belongs to and ensure the links exist.

---

MOC updates are agent-handled, no approval required. The agent reads existing MOCs, finds where the new note fits, appends the wikilink under the right section. If no MOC exists for a concept the note introduces, the agent creates one. If the note fits an existing MOC but no existing section, the agent creates the section. MOC maintenance is part of the distill job, not a separate review step.

---

Three-phase distill flow (not "draft and present" like seed-inbox):

Phase 1 — Plan. Agent reads the seed, maps it: which distinct ideas, how many permanent notes, proposed summaries, parent MOC(s), tags, keywords. Presents the plan as a todo/outline for user approval. No note written yet. User can reshape the plan (merge, split differently, redirect).

Phase 2 — Interrogate. After the plan is approved and notes are drafted, the agent grills the user about gaps. Not one polite "anything missing?" — a persistent interview. "What's the counter-argument? What's the concrete example that proves this? What would someone who disagrees say? What adjacent idea should be here but isn't?" Follow-ups, pushback, not letting gaps slide. Continues until the user says "enough."

Phase 3 — Forward-link. Agent adds wikilinks to notes that don't exist yet but should — stubs, ghost links, future distillation targets. "You mentioned X but we didn't go deep — that's a future note: [[X]]." These are planted flags, not written notes. They show up as uncreated links in Obsidian's graph, visible and waiting.

---

Forward-links are inline wikilinks — normal `[[double bracket]]` links to nonexistent notes. Obsidian renders them as uncreated nodes (dim/different color) in the graph view. The graph becomes a visual map of "what to explore next" — the dim nodes are the frontier. No separate frontmatter field needed; the note body is the planting ground.

---

Ready-gate for seeds. If `seed_level: project`, the agent stops immediately — tells the user this seed is not for distillation (project seeds have a different workflow, not yet designed). For non-project seeds that still feel thin or fuzzy, the agent presents its best understanding of what the seed is trying to say, then asks the user what to do: distill anyway, leave it, or something else. The agent does not silently barrel through a half-baked seed.

---

Sibling links — existing permanent notes that cover adjacent ground. The agent should search `11l.LtS/` for related notes during the plan phase and surface them. These siblings should be embedded in the frontmatter (like parents) so they're discoverable by grep/approximation when the agent later discusses the topic — not just inline wikilinks buried in prose but structured metadata the retrieval layer can match against.

---

Siblings are a separate frontmatter field from parents. `parents` = "what larger context does this sit within?" (MOCs, broader notes). `siblings` = "what else covers nearby ground at the same level?" (adjacent permanent notes). Both are arrays of wikilinks. Both are grep targets for retrieval. Eight frontmatter fields total: status, kind, source, tags, keywords, summary, parents, siblings.

---

Tag handling: the agent refines the seed's tags against a controlled vocabulary — standardizing terms, dropping noise, picking precise labels. The seed's tags were best-guesses at seed time; permanent tags are curated. The agent also adds tags that feel correct but weren't in the seed, based on what the note actually covers once distilled. The controlled vocabulary itself is maintained in a central glossary/tag-index (to be created as part of the LtS infrastructure — presale-glosary.md is the existing model for this).

---

Loop behavior is topic-contiguous, not random-next-seed. After finishing one seed, the agent surfaces what's adjacent: "We identified sibling notes [[X]] and [[Y]] during distillation. Want to distill one of those next? Or there's a related seed in 11b.Seeds/ that touches the same topic." The loop stays in the current conceptual neighborhood rather than jumping to an unrelated seed. This builds out a topic area incrementally — distilling the map outward from the first note.

---

Naming: the permanent note gets a keyword-rich kebab-case slug (same pattern as seeds, up to ~6 words). After promotion, the archived seed in `11b.Seeds/_processed/` is renamed — its original keyword-slug is reclaimed for the permanent note. The keywords should grep-hit the permanent note, not the processed seed. The `source` backlink in the permanent note is updated to point to the renamed seed file.

---

Note body structure: the permanent note body is the seed body transplanted below the summary, with light editing for clarity and inline wikilinks added throughout. If one seed spawned multiple permanent notes (split case), each note gets only its relevant portion of the seed body — the agent extracts and places each idea's supporting material into the right note. The body carries inline links to siblings, parents, and forward-links (ghost notes). The summary lives above as a `summary` frontmatter field, not in the body itself — the body starts where the idea unfolds.

---

Filenames are pure keyword-slug — no date prefix. Permanent notes are timeless; a date prefix implies staleness. `verification-gates.md`, not `20260629-verification-gates.md`. Sortability comes from MOC organization and graph links, not chronological naming.

---

[drift] Previous agent (session 0006, 2026-06-30) also grilled distill-permanent. Locked decisions D18–D21 largely align with this session's fragments. Key differences and unresolved gaps to reconcile:

- D19 (their flow): Plan(all notes at once) → Draft+Interrogate(per-note sequential) → Forward-link. Our version: Plan → Interrogate → Forward-link without specifying per-note vs batch. Need to decide.
- G1 (kind field): they questioned whether `kind` carries enough signal for permanent notes (mostly idea/lit-note). We kept it. Revisit?
- G11: interaction with concept-refine pipeline. Can a seed go concept-refine → distill-permanent in one session? Does concept-refine output carry a "distill-ready" flag?
- G8: CDI worked-example as test case. The CDI seed should split into deal note (Presales) + verification note (AI).
- G2–G10: mostly align with our fragments but with finer-grained questions (MOC template, forward-link aggressiveness, sibling discovery mechanism, summary duplication).

---

Resolutions from this session vs. session 0006:

1. Interrogation is batch — grill about all notes in one pass, not per-note sequential. Plan → single interrogation covering every note → Forward-link.

2. Drop `kind` from frontmatter. Most permanent notes are `idea` or `lit-note` — two values that carry near-zero signal. Frontmatter: status, source, tags, keywords, summary, parents, siblings (7 fields).

3. concept-refine and distill-permanent are two different flows. concept-refine's output is effectively a permanent note — its refining process produces permanent-quality output directly. However, if distill-permanent (or the agent in general) encounters a concept-refine output that contradicts atomicity (multiple ideas bundled), it alerts the user — they can either split it or treat it as a deliberate exception.

Clarification — two pipelines, same destination:
- Path A: capture → seed-inbox → distill-permanent → `11l.LtS/` (permanent)
- Path B: capture → concept-mine (quarry/seed in `11b.Seeds/`) → concept-refine → `11l.LtS/` (permanent)

This means concept-refine needs updating — it writes directly to `11l.LtS/` with permanent frontmatter, not to `11b.Seeds/` as a seed. The concept-mine quarry serves as the "seed" for that pipeline. Both paths converge on the same permanent note format in LtS.

---

MOC maintenance: agent uses best guess for everything — section placement, new section creation, which MOCs to link. No approval gate for MOC changes. If a note fits multiple MOCs, the agent links both in `parents` and updates both MOC files. The user will sort out misfires later; the cost of a misplaced MOC link is low (move it), the cost of an approval step is high (friction).

---

Summary duplication: strip, don't duplicate. If the seed body contains summary-like content (e.g. a "Claim" blockquote from seed-inbox), the agent extracts it into the frontmatter `summary` field and removes it from the body. The body starts clean where the idea unfolds. No repeated text between frontmatter and body.

---

Forward-link aggressiveness: key concepts first — agent plants inline wikilinks for concepts that clearly deserve their own note (core dependencies, natural next-explorations). Then proposes up to 2 optional/additional links that are interesting but less certain — these go through a quick user gate: "Also worth planting [[X]] and [[Y]]?" The user can approve, reject, or rename them. The graph stays navigable, not cluttered with dim-node noise.

---

Sibling discovery: grep keywords + tags over all `11l.LtS/` frontmatter. Fast, exact-match driven, no summary-reading pass needed at discovery time. The agent uses the seed's keywords and tags as the query surface, surfaces frontmatter matches, and presents the best candidates as siblings.

---

Summary as embedding target: the `summary` field must be concrete, not abstract. "X is important" embeds poorly — no anchor. "X matters because when Y happens, Z breaks in three specific ways" embeds well — specific claims with concrete referents. The summary is a standalone unit of meaning: self-contained, no cross-references, keyword-rich without being stuffed. 3–5 sentences, future-proofed for vector search.

---

Loop discovery: both sources. The agent uses the `siblings` field of the just-written permanent note to surface existing notes worth exploring next (the map already knows its neighbors). Simultaneously, it greps `11b.Seeds/` for unprocessed seeds with keyword/tag overlap — same topic area, not yet distilled. Presents both as options: "Distill a sibling permanent note, or process this related seed?"

---

Interrogate protocol: a living list of standard questions + content-driven gap detection. The agent always runs through the standard questions, but also reads the draft and surfaces whatever gaps it sees — specific to the content, not just the template. The standard list is updatable over time (add questions that prove useful, drop ones that don't).

Initial standard questions:
- "What's the counter-argument to this?"
- "What's the simplest concrete example that proves this?"
- "What would someone who disagrees say — and what would you say back?"
- "What adjacent idea should be here but isn't?"
- "If this note is wrong, what would prove it wrong?"
- "What's the one sentence version?" (tests atomicity from the user's side)

---

Parent link validation: best guess, no gate. The agent proposes parent links based on its understanding of the note's domain and concept scope. If a note fits multiple MOCs, link both. If a concept MOC doesn't exist yet, create it. No approval needed — the user sorts out misfires later, same as MOC maintenance.
