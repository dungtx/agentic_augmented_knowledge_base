# Rendering and validation

## Default: static validation (no tooling, no network)
`validate.py` parses every generated `.puml`, checks macro names against the
C4-PlantUML whitelist, checks arity, resolves every `Rel`/`BiRel` endpoint to a
defined alias, balances boundary braces, and verifies the coverage + cross-level
invariants. It needs only Python and catches the entire syntax-error class. Run it
after every build; it is the contract the skill guarantees.

## Viewing the diagrams (human)
- **PlantUML**: paste a `.puml` into https://www.plantuml.com/plantuml/uml/ (the
  server resolves the `!include` from GitHub), or use the VS Code *PlantUML*
  extension with `plantuml.server` set to the public server if there is no local
  Java. Offline: install Java + Graphviz and switch the include to
  `!include <C4/C4_Container>`.
- **Mermaid**: `.mmd` / fenced mermaid renders natively in GitHub and the VS Code
  markdown preview — no tooling.

## Opt-in: rasterize to an image (OFF by default)
Producing a PNG/SVG requires sending the diagram source to a renderer (a PlantUML
server or Kroki). That publishes internal architecture to a third party, so the
skill does NOT do it automatically. Only when the user explicitly asks:
```
# Example (only with user consent) — Kroki:
#   POST the .puml to https://kroki.io/plantuml/svg   (or run Kroki locally)
# or a local PlantUML jar:
#   java -jar plantuml.jar -tsvg docs/architecture/<sys>/container.puml
```
Prefer a locally-run renderer over a public server when images are required.

## "Test" vs "render"
Static validation is the *test* (correctness). Rasterizing is *rendering* (looks).
Layout problems (overlap, width) are only visible in a render — if a diagram is
valid but cramped, add `direction` hints in the IR or split a busy container.
