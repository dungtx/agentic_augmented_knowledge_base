---
name: arch-diagram-gen
description: >-
  Generate C4 architecture diagrams (Context / Container / Component) as PlantUML-C4 (default)
  or Mermaid for ANY codebase. Use this skill whenever the user wants an architecture diagram,
  a C4 diagram, a system/container/component diagram, a PlantUML or Mermaid diagram of how a
  system fits together, to "visualize the architecture", "diagram the services", "map the
  components", or to document a system's structure — even if they don't say "C4" explicitly.
  Works from a graphify knowledge graph, a raw repo scan, or a hand-written architecture.yaml.
  Guarantees zero diagram-syntax errors and gapless layer coverage by generating a typed
  intermediate representation and rendering/validating it deterministically.
---

# arch-diagram-gen

Generate **C4 model** architecture diagrams that are (a) **syntactically correct by construction** and
(b) **complete with no missing layers or containers**. These two guarantees are the whole point of the
skill — they exist because hand-writing PlantUML/Mermaid macros from memory produces wrong macro names
(e.g. `Rel_Bi` instead of the real `BiRel`), and because picking "interesting" parts to diagram silently
leaves gaps.

## The core idea: never hand-write diagram syntax

You (the model) do **not** write `.puml` or `.mmd` text directly. Instead you produce a **typed
intermediate representation (IR)** — a JSON object whose element/relationship kinds are closed enums.
Deterministic scripts then render the IR to PlantUML/Mermaid and validate it. Because the renderer owns
the macro mapping (e.g. `kind:"bidirectional"` → `BiRel`), a misspelled macro is *impossible to emit*.
Because coverage is computed from the IR, a missing container is *impossible to hide*.

If you ever feel the urge to type `Rel(`, `Container(`, `@startuml`, or `flowchart` by hand — stop. Put
that fact into the IR and let `render.py` produce the syntax.

## Workflow

```
source  --derive-->  IR (typed JSON)  --enrich-->  IR  --build-->  diagrams + manifest  --validate-->  ok/fail
```

1. **Pick the source** (best available). See `references/adapters.md`.
   - graphify graph: `python scripts/derive_graphify.py <graph.json> [--product NAME] > ir.json`
   - repo scan: `python scripts/derive_reposcan.py <repo_root> > ir.json`
   - hand-written: copy `assets/architecture.example.yaml`, fill it, `python scripts/yaml_to_ir.py file.yaml > ir.json`
   The adapter emits a **skeleton IR** — system, containers, datastores, externals, and a first pass at
   relations. It does NOT invent components reliably.

2. **Enrich the IR.** Read the skeleton and the source, then fill in:
   - `components` for each owned container (the internal building blocks — controllers, services,
     ports/adapters, stores). This is where your understanding of the code matters.
   - `relations` with real labels, `tech`, `kind` (sync/async/bidirectional), and `direction` hints.
   - descriptions. Keep them short — one line.
   Validate enums against `references/ir-schema.json`. Do not invent element kinds; the six are
   `person, system, container, container_db, component, external`.

3. **Build** (renders every required diagram + the coverage manifest):
   ```
   python scripts/build.py ir.json --out docs/architecture/<system> [--format plantuml|mermaid|both]
   ```
   This applies the **coverage law** (below) automatically and writes `index.md` (the manifest).

4. **Validate** (must pass before you hand anything over):
   ```
   python scripts/validate.py docs/architecture/<system>
   ```
   It checks IR conformance, macro/arity/alias/boundary correctness of every rendered file, the
   coverage invariant, and cross-level consistency. If it fails, fix the IR (not the `.puml`) and rebuild.

5. **Report only the manifest.** The user reviews `index.md` — denominator -> covered -> skipped(+reason).
   That table is the single review surface. Mention any validation warnings.

## The C4 coverage law (deterministic — do not curate by "interestingness")

Coverage is derived from the IR, never from judgment. For a system:

| Level | What it contains | How many diagrams |
|-------|------------------|-------------------|
| **L1 Context**   | the system as one box + all `persons` + all `externals` | exactly 1 |
| **L2 Container** | every `container` + every `container_db` + every `external` + `persons` | exactly 1 |
| **L3 Component** | the components of ONE container; other containers/datastores/externals appear only as referenced boundary boxes (never decomposed) | **exactly one per *owned* container** |

**L4 (code-level) diagrams are out of scope — never generate them.** This skill
stops at the component level. Do not produce class/function/sequence "code"
diagrams even if asked to "go deeper" than L3; deeper detail belongs in the code
itself, not in an architecture diagram.

Rules that make coverage gapless:
- A container is **owned** unless `owned: false`. Datastores and externals are **never** decomposed —
  they have no component diagram by definition.
- `count(L3 diagrams) == count(owned containers)`. The only allowed shortfall is an owned container with
  **zero components**, which `build.py` records in the manifest as `skipped: no components defined` — a
  visible, logged decision, not a silent gap. If a container genuinely has internal structure, give it
  components; don't let it be skipped.
- **Cross-level consistency**: any container/datastore/external referenced by an L3 component relation
  must exist at L2. The validator enforces this so a component can't depend on something the
  architecture doesn't declare.

## Output layout

`build.py` writes a hierarchy that mirrors the C4 levels (and nests under a product/system folder so
multiple systems coexist):

```
docs/architecture/<system>/
  context.puml                  # L1
  container.puml                # L2
  components/<container>.puml    # L3, one per owned container
  index.md                      # coverage manifest (the review surface)
```
With `--format mermaid` or `both`, parallel `.mmd` files are written alongside.

## Format choice

Default **PlantUML-C4** (highest C4 fidelity: real notation + legend). Pass `--format mermaid` when the
target renders natively without tooling (GitHub / VS Code markdown preview) — `render.py` emits
flowchart-with-subgraphs styled as C4 (more reliable layout than Mermaid's experimental `C4Container`).
`both` writes each. The IR is identical; only the render target changes.

## Rendering / "testing" a diagram

The validator is **static** — it needs no Java, no PlantUML, no network, and catches the entire
macro/arity/alias/boundary error class. That is the default safety net. Actually rasterizing to an image
(for layout review) is **opt-in** and may send diagram source to an external server, so it is OFF by
default — only do it if the user asks. See `references/rendering.md`.

## Reference files (read when needed)

- `references/ir-schema.json` — the typed IR contract (enums, required fields). Read before enriching.
- `references/c4-spec.md` — element/relationship kinds, the PlantUML & Mermaid macro mapping table, and
  the coverage law in detail. Read when you need to know how a kind renders or extend the renderer.
- `references/adapters.md` — how each source maps to the IR; how to choose.
- `references/rendering.md` — the opt-in external-render path and offline include note.

## Why this design (so you can extend it sensibly)

Two failure modes motivated every choice: improvised syntax (wrong macros) and improvised scope (missing
diagrams). The fix for both is the same — replace judgment with a typed artifact plus deterministic
checks. When you extend this skill, preserve that invariant: new capabilities should flow through the IR
and be validated by `validate.py`, never by trusting hand-written diagram text.
