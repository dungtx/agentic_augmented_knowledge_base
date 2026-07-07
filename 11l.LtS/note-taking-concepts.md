---
status: permanent
source: "Generated from T5 concept walkthrough (2026-07-02). No seed — direct from model knowledge per user's original ask #4."
tags: [zettelkasten, note-taking, capture, distillation]
keywords: [note-taking-concepts, zettelkasten, atomic-notes, MOC, evergreen-notes]
summary: "A reference map of 16 note-taking concepts relevant to this vault's design. Covers zettelkasten fundamentals (fleeting/permanent notes, atomicity, titles-as-claims), organization (MOCs, link graph vs folders, tags vs links), comparative systems (PARA, GTD, second brain), practice heuristics (progressive summarization, evergreen notes, collector's fallacy, anti-library), and two vault-specific concepts: verification gates for AI output and SRS-for-surfacing vs retrieval-for-finding."
parents: ["[[MOC.md]]", "[[tag-glossary.md]]"]
siblings: []
---

# Note-taking concepts — the 15 that matter for this vault

A reference from the T5 walkthrough. Each entry is a 2–3 sentence definition + how it applies to _this_ vault.

## Foundation

### Zettelkasten

A slip-box method by Niklas Luhmann: one idea per note, notes linked together, structure emerges from links instead of pre-designed categories. The value is in the conversation between notes, not the filing system.

**This vault:** The pipeline (capture → seed → permanent) is zettelkasten-native. `11l.LtS/` is the slip-box. The flat-default + existing-subfolders-only rule enforces emergent organization.

### Fleeting, literature, and permanent notes

The three note types in zettelkasten: **fleeting** (raw capture, fast, lossy, ~24h shelf life), **literature** (your notes on someone else's ideas), **permanent** (one idea, in your words, linked into the graph).

**This vault:** Split across 5 lanes — Inbox captures, Deferred/Someday for parked items, Seeds for rough drafts, LtS for permanent notes. The `kind: lit-note` frontmatter covers literature notes.

### Atomicity

A permanent note holds exactly one idea. One gravitational center. If a note has two ideas, split it. The link graph connects them — a single note doesn't need to.

**This vault:** `distill-permanent` enforces this at the final gate. The CDI note was flagged for splitting (deal note + verification-gates note). The `summary` field is the atomicity test: can you summarize this note in 3 sentences around one idea?

### Titles as claims, not topics

"OCR fails on mixed-script SEA handwriting" beats "OCR notes." A claim-title tells future-you what the note argues. Topic-titles require opening the note to remember what it says.

**This vault:** Seed and permanent note slugs should encode the claim. The distill-permanent skill was designed to produce claim-titles during the final shaping pass.

## Organization

### Map of Content (MOC)

A note whose job is linking to other notes — a curated entry-point: "here's what I know about X, and here's where to find it." MOCs are notes themselves, so they can be linked, tagged, and evolved.

**This vault:** Root `MOC.md`, per-domain MOCs (e.g., `11l07.Career/MOC.md`), `presale-glosary.md` as a domain MOC, and the tag-glossary as a tag-level MOC.

### Link graph vs folder hierarchy

Folders impose one fixed taxonomy; links let a note belong in multiple contexts. Zettelkasten says: folders for coarse lanes (capture, seeds, permanent), links for meaning.

**This vault:** Johnny-decimal lanes for coarse organization, `[[wikilinks]]` for semantics. The rule "never create new `11l.LtS/` subfolders" protects against folder-creep.

### Tags vs links

Tags are retrieval hooks (grep `tag:interviews` → everything). Links are semantic connections (this note builds on that note). Tags are flat and global; links are directed and contextual.

**This vault:** Tag-glossary defines the controlled vocabulary (retrieval). `parents`/`siblings` frontmatter + inline wikilinks handle semantic linking. 2–6 tags per note for retrieval, parents/siblings for structure.

## Comparative systems

### PARA vs Zettelkasten vs GTD

Three systems, different purposes: **GTD** — task management (capture → clarify → organize → reflect → engage). **PARA** — folder-based life organization (Projects/Areas/Resources/Archive). **Zettelkasten** — knowledge development (ideas over time, not task-oriented).

**This vault:** A hybrid — GTD-style capture pipeline (Inbox → Deferred/Someday → Seeds) feeding a zettelkasten-style permanent layer (LtS). The two pipelines are kept separate (don't classify at capture; classification happens at triage/distill).

### Second brain (Tiago Forte)

Offload remembering to an external system. Your brain is for having ideas, not holding them. Capture everything, trust the system to resurface it when needed.

**This vault:** The core premise. "Capture is lossy" is the second-brain motto. The whole pipeline exists so you can dump thoughts and trust they'll surface.

## Practice heuristics

### Progressive summarization

Processing external content in layers: bold → highlight → executive summary. Each pass adds a layer, so you can read at the depth needed in the moment.

**This vault:** Currently less relevant (you're generating original content), but will matter when `web-research` (T10) pulls in external sources. Lit-notes (`kind: lit-note`) are where progressive summarization applies.

### Evergreen notes (Andy Matuschak)

Permanent notes you revisit and improve over time. Not "done and filed" — "good enough for now, will get better" as your understanding evolves.

**This vault:** Permanent notes in `11l.LtS/` are evergreen by design — timeless filenames (no date prefix), linked into an evolving graph. You can edit one later when you learn more.

### Collector's fallacy

Collecting more than you process. Saving a bookmark feels like learning but isn't. A full Inbox is a liability — each unprocessed item is a tiny open loop.

**This vault:** A live risk. Morning-review is the defense: regular triage prevents accumulation. The rule "chronic slipping = signal to run distill" is the collector's-fallacy alarm.

### Anti-library

Unread books are a research tool: they represent what you don't know, tagged and ready. The value isn't having read them — it's knowing they exist.

**This vault:** `11a3.Someday/` is an anti-library for ideas. Items parked there are "I know about this, I might explore it later." SRS-for-Someday (T8) makes sure they resurface.

### Daily note log

A chronological log — the "inbox of the day." Some use it as their primary capture surface.

**This vault:** You use timestamped individual capture files instead of a single daily log. The `YYYYMMDDHHmm` prefix serves the same chronological function.

## Vault-specific concepts

### Verification gates for AI output

When AI extracts data (OCR, parsing), how does a human verify it? What gates sit between "AI says X" and "we act on X"? Emerged from the CDI presales note.

**This vault:** A permanent-note candidate for `11l.LtS/11l05.AI/`. A good claim-title: "every AI extraction pipeline needs three verification gates."

### SRS-for-surfacing vs retrieval-for-finding

Two ways to get knowledge back: **SRS** surfaces ideas on a schedule (good for Someday items you want to encounter repeatedly). **Retrieval** (semantic search, grep) finds knowledge on demand (good for permanent notes you need in the moment).

**This vault:** Locked as D12 — SRS for `11a3.Someday/` (surfacing), retrieval for `11l.LtS/` (finding). SRS on permanent notes explicitly rejected. The `summary` frontmatter field doubles as the future retrieval embedding target.
