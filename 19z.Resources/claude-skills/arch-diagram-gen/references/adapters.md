# Adapters: getting from a source to a skeleton IR

Pick the richest source available. Every adapter emits a *skeleton* — the model
must enrich it (components, relations, datastores, externals, descriptions) before
running `build.py`. Skeletons never invent relations.

## 1. graphify graph (best, when graphify-out/ exists)
```
python scripts/derive_graphify.py <graph.json> [--product PREFIX] [--system NAME] [--top N]
```
- Groups nodes by service (first path segment of `source_file`) into containers.
- Seeds each container with its top-N highest-degree nodes as candidate components
  (refine these — degree is a hint, not a component boundary).
- `--product rfpilot_` marks only `rfpilot_*` services as owned; others become
  `owned:false` boundary references — useful in a federated multi-product repo.
- Does NOT detect datastores/externals or cross-service relations — add them by
  reading the graph (look for client/adapter/gateway nodes pointing outside).

## 2. repo scan (no graphify)
```
python scripts/derive_reposcan.py <repo_root> [--system NAME] [--max-depth 3]
```
- Detects containers by manifest (`package.json`, `go.mod`, `pyproject.toml`,
  `Dockerfile`, etc.) and lists docker-compose services as a hint.
- Components are empty — fill them by reading each container's entrypoints.

## 3. hand-written architecture.yaml (planned / greenfield systems)
```
python scripts/yaml_to_ir.py architecture.yaml > ir.json
```
- Copy `assets/architecture.example.yaml` and fill it in. The YAML mirrors the IR.
- If PyYAML is not installed, author the IR as JSON directly — identical shape.

## Enrichment checklist (all sources)
- [ ] Each owned container has real components (controllers / services /
      ports+adapters / stores), not just top-degree symbols.
- [ ] Datastores declared (DB, cache, file/blob store) under `datastores[]`.
- [ ] Externals declared (vendor APIs, other products/services) under `externals[]`.
      In a federated repo, other products are `externals` (or `owned:false`
      containers) — never fuse them in.
- [ ] Relations have a verb `label`, a `tech`, and the right `kind`
      (sync / async / bidirectional). Add `direction` only where it aids layout.
- [ ] IDs are unique and match `^[A-Za-z_][A-Za-z0-9_.]*$` (components may use dots).
