# C4 spec: element/relationship kinds, macro mapping, coverage law

This is the type system the renderer enforces. The model never writes the macros
in the right-hand columns — it sets the IR `kind`/fields on the left, and
`render.py` produces the macro. `validate.py` rejects anything outside this set.

## Element kinds (IR -> PlantUML -> Mermaid class)

| IR location / flag         | PlantUML macro         | Mermaid class |
|----------------------------|------------------------|---------------|
| `persons[]`                | `Person`               | person        |
| `persons[].external:true`  | `Person_Ext`           | person        |
| `system` (context L1 box)  | `System`               | system        |
| `containers[]`             | `Container`            | container     |
| `datastores[]`             | `ContainerDb`          | db            |
| `externals[]`              | `System_Ext`           | external      |
| `components[]`             | `Component`            | component     |
| `components[].db:true`     | `ComponentDb`          | component     |
| system boundary            | `System_Boundary{ }`   | subgraph      |
| container boundary (L3)    | `Container_Boundary{ }`| subgraph      |

Only these six element kinds exist: `person, system, container, container_db,
component, external`. Do not invent others.

## Relationship kinds (IR -> macro)

`kind` selects the base macro; `direction` appends a suffix.

| kind             | base macro |
|------------------|------------|
| `sync` (default) | `Rel`      |
| `async`          | `Rel` (label gets a ` [async]` suffix; dashed arrow in Mermaid) |
| `bidirectional`  | `BiRel`    |

Direction suffix (PlantUML only): `up -> _U`, `down -> _D`, `left -> _L`,
`right -> _R`, `auto -> (none)`. So `{kind:"bidirectional", direction:"down"}`
renders `BiRel_D`. There is NO `Rel_Bi` / `Rel_Bidir` macro — that exact mistake
is why this skill exists. The valid bidirectional macros are `BiRel`, `BiRel_U`,
`BiRel_D`, `BiRel_L`, `BiRel_R`.

Mermaid arrows: sync `-->`, async `-.->`, bidirectional `<-->`, each with
`|"label"|`. Mermaid layout is automatic, so `direction` is ignored there.

## The coverage law (L1 / L2 / L3)

- **L1 Context** (1 diagram): the system as a single `System` box + all `persons`
  + all `externals`. Relations roll up: endpoints inside the system collapse to the
  system box; person/external endpoints stay; self-loops are dropped.
- **L2 Container** (1 diagram): all `containers` (owned or not) + all `datastores`
  inside the system boundary; `externals` + `persons` outside. Component-level
  relation endpoints roll up to their parent container.
- **L3 Component** (one per *owned* container that has components): the container's
  `components` inside a `Container_Boundary`; any other container/datastore/external
  a component talks to is drawn as a single boundary box (never expanded). A
  relation appears here iff at least one endpoint is a component of this container.

Denominator = count of owned containers. An owned container with zero components is
logged in `index.md` as `skipped: no components defined` (a visible decision), never
silently omitted. `validate.py` enforces `generated L3 files + logged skips ==
owned containers`, and that every boundary box referenced in an L3 exists at L2
(cross-level consistency).

## Why a renderer instead of hand-writing

Macro names, arity, and the `Rel`/`BiRel` direction matrix are easy to misremember
and impossible to spell-check by eye. Centralizing them here and in `render.py`
gives one audited mapping; `validate.py` is the backstop for any hand edit or drift.
