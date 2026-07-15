"""IR -> PlantUML-C4 / Mermaid renderer.

This module is the ONLY place diagram syntax is produced. The model never writes
.puml/.mmd by hand; it writes the typed IR and this renderer maps typed kinds to
correct macros (e.g. kind="bidirectional" -> BiRel). That inversion is what makes
syntax errors structurally impossible.

Public API (used by build.py):
    plantuml_context(ir) / plantuml_container(ir) / plantuml_component(ir, cid)
    mermaid_context(ir)  / mermaid_container(ir)  / mermaid_component(ir, cid)
    index_of(ir) -> helper dicts (element lookup, component->container map)
"""
from __future__ import annotations

C4_INCLUDE = "https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master"
DIR_SUFFIX = {"up": "_U", "down": "_D", "left": "_L", "right": "_R", "auto": ""}


# ---------------------------------------------------------------- IR indexing
def index_of(ir):
    """Return (elements, comp_parent) where elements maps id -> (category, obj)
    and comp_parent maps component id -> container id."""
    elements = {}
    comp_parent = {}
    sys = ir["system"]
    elements[sys["id"]] = ("system", sys)
    for p in ir.get("persons", []):
        elements[p["id"]] = ("person", p)
    for c in ir.get("containers", []):
        elements[c["id"]] = ("container", c)
        for comp in c.get("components", []):
            elements[comp["id"]] = ("component", comp)
            comp_parent[comp["id"]] = c["id"]
    for d in ir.get("datastores", []):
        elements[d["id"]] = ("datastore", d)
    for e in ir.get("externals", []):
        elements[e["id"]] = ("external", e)
    return elements, comp_parent


def owned_containers(ir):
    return [c for c in ir.get("containers", []) if c.get("owned", True)]


# ---------------------------------------------------------------- text helpers
def _esc(s):
    """Make a string safe inside a PlantUML/Mermaid quoted label."""
    if s is None:
        return ""
    return str(s).replace('"', "'").replace("\n", " ").strip()


def _desc(obj):
    bits = []
    if obj.get("tech"):
        bits.append(obj["tech"])
    if obj.get("description"):
        bits.append(obj["description"])
    return " - ".join(_esc(b) for b in bits)


# ---------------------------------------------------------------- relations
def _rel_macro(rel):
    base = "BiRel" if rel.get("kind") == "bidirectional" else "Rel"
    return base + DIR_SUFFIX.get(rel.get("direction", "auto"), "")


def _rel_label(rel):
    label = _esc(rel["label"])
    if rel.get("kind") == "async":
        label = (label + " [async]").strip()
    return label


def _emit_rel_puml(rel, src, dst):
    macro = _rel_macro(rel)
    label = _rel_label(rel)
    tech = _esc(rel.get("tech", ""))
    if tech:
        return f'{macro}({src}, {dst}, "{label}", "{tech}")'
    return f'{macro}({src}, {dst}, "{label}")'


def _map_to_container_level(eid, elements, comp_parent):
    """Map any element id to its container-diagram representative."""
    cat = elements.get(eid, (None,))[0]
    if cat == "component":
        return comp_parent[eid]
    return eid  # person/container/datastore/external/system unchanged


def _map_to_context_level(eid, elements):
    cat = elements.get(eid, (None,))[0]
    if cat in ("person", "external"):
        return eid
    return None  # collapse container/component/datastore/system into the system box


# ---------------------------------------------------------------- PlantUML
def _puml_header(name, title, include_file):
    return [
        f"@startuml {name}",
        f"!include {C4_INCLUDE}/{include_file}",
        "' Offline alternative: !include <C4/%s>" % include_file.replace(".puml", ""),
        "LAYOUT_WITH_LEGEND()",
        f"title {title}",
        "",
    ]


def plantuml_context(ir):
    elements, comp_parent = index_of(ir)
    sys = ir["system"]
    lines = _puml_header(f"{sys['id']}-context", f"System Context - {_esc(sys['name'])}", "C4_Context.puml")
    for p in ir.get("persons", []):
        macro = "Person_Ext" if p.get("external") else "Person"
        lines.append(f'{macro}({p["id"]}, "{_esc(p["name"])}", "{_desc(p)}")')
    lines.append(f'System({sys["id"]}, "{_esc(sys["name"])}", "{_esc(sys.get("description",""))}")')
    for e in ir.get("externals", []):
        lines.append(f'System_Ext({e["id"]}, "{_esc(e["name"])}", "{_desc(e)}")')
    lines.append("")
    seen = set()
    for rel in ir.get("relations", []):
        s = _map_to_context_level(rel["from"], elements)
        d = _map_to_context_level(rel["to"], elements)
        s = s if s is not None else sys["id"]
        d = d if d is not None else sys["id"]
        if s == d:
            continue
        key = (s, d, _rel_label(rel))
        if key in seen:
            continue
        seen.add(key)
        lines.append(_emit_rel_puml(rel, s, d))
    lines.append("@enduml")
    return "\n".join(lines) + "\n"


def _puml_container_box(c):
    return f'Container({c["id"]}, "{_esc(c["name"])}", "{_esc(c.get("tech",""))}", "{_esc(c.get("description",""))}")'


def plantuml_container(ir):
    elements, comp_parent = index_of(ir)
    sys = ir["system"]
    lines = _puml_header(f"{sys['id']}-container", f"Container Diagram - {_esc(sys['name'])}", "C4_Container.puml")
    for p in ir.get("persons", []):
        macro = "Person_Ext" if p.get("external") else "Person"
        lines.append(f'{macro}({p["id"]}, "{_esc(p["name"])}", "{_desc(p)}")')
    lines.append("")
    lines.append(f'System_Boundary({sys["id"]}_b, "{_esc(sys["name"])}") {{')
    for c in ir.get("containers", []):
        lines.append("    " + _puml_container_box(c))
    for d in ir.get("datastores", []):
        lines.append(f'    ContainerDb({d["id"]}, "{_esc(d["name"])}", "{_esc(d.get("tech",""))}", "{_esc(d.get("description",""))}")')
    lines.append("}")
    for e in ir.get("externals", []):
        lines.append(f'System_Ext({e["id"]}, "{_esc(e["name"])}", "{_desc(e)}")')
    lines.append("")
    seen = set()
    for rel in ir.get("relations", []):
        s = _map_to_container_level(rel["from"], elements, comp_parent)
        d = _map_to_container_level(rel["to"], elements, comp_parent)
        if s == d or s not in elements or d not in elements:
            continue
        if elements[s][0] == "system" or elements[d][0] == "system":
            continue
        key = (s, d, _rel_label(rel))
        if key in seen:
            continue
        seen.add(key)
        lines.append(_emit_rel_puml(rel, s, d))
    lines.append("@enduml")
    return "\n".join(lines) + "\n"


def plantuml_component(ir, container_id):
    elements, comp_parent = index_of(ir)
    sys = ir["system"]
    container = next(c for c in ir["containers"] if c["id"] == container_id)
    comp_ids = {comp["id"] for comp in container.get("components", [])}
    title = f"Component Diagram - {_esc(container['name'])}"
    lines = _puml_header(f"{sys['id']}-component-{container_id}", title, "C4_Component.puml")

    rels = []
    refs = set()
    for rel in ir.get("relations", []):
        f_in = rel["from"] in comp_ids
        t_in = rel["to"] in comp_ids
        if not (f_in or t_in):
            continue
        s = rel["from"] if f_in else _map_to_container_level(rel["from"], elements, comp_parent)
        d = rel["to"] if t_in else _map_to_container_level(rel["to"], elements, comp_parent)
        if s not in elements or d not in elements:
            continue
        if elements[s][0] == "system" or elements[d][0] == "system":
            continue
        if s == d:
            continue
        rels.append((rel, s, d))
        for end in (s, d):
            if end not in comp_ids:
                refs.add(end)

    lines.append(f'Container_Boundary({container_id}_b, "{_esc(container["name"])}") {{')
    for comp in container.get("components", []):
        macro = "ComponentDb" if comp.get("db") else "Component"
        lines.append(f'    {macro}({comp["id"]}, "{_esc(comp["name"])}", "{_esc(comp.get("tech",""))}", "{_esc(comp.get("description",""))}")')
    lines.append("}")

    for rid in sorted(refs):
        cat, obj = elements[rid]
        if cat == "person":
            m = "Person_Ext" if obj.get("external") else "Person"
            lines.append(f'{m}({rid}, "{_esc(obj["name"])}", "{_desc(obj)}")')
        elif cat == "container":
            lines.append(_puml_container_box(obj))
        elif cat == "datastore":
            lines.append(f'ContainerDb({rid}, "{_esc(obj["name"])}", "{_esc(obj.get("tech",""))}", "{_esc(obj.get("description",""))}")')
        elif cat == "external":
            lines.append(f'System_Ext({rid}, "{_esc(obj["name"])}", "{_desc(obj)}")')
    lines.append("")
    seen = set()
    for rel, s, d in rels:
        key = (s, d, _rel_label(rel))
        if key in seen:
            continue
        seen.add(key)
        lines.append(_emit_rel_puml(rel, s, d))
    lines.append("@enduml")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- Mermaid
_MERMAID_CLASSDEFS = [
    "classDef person fill:#08427b,color:#fff,stroke:#052e56;",
    "classDef system fill:#1168bd,color:#fff,stroke:#0b4884;",
    "classDef container fill:#1168bd,color:#fff,stroke:#0b4884;",
    "classDef db fill:#2e7d32,color:#fff,stroke:#1b5e20;",
    "classDef component fill:#85bbf0,color:#000,stroke:#5d82a8;",
    "classDef external fill:#6b6b6b,color:#fff,stroke:#4d4d4d;",
]


def _mid(eid):
    return eid.replace(".", "_").replace("-", "_")


def _mlabel(obj, kind_note=""):
    parts = [_esc(obj["name"])]
    sub = obj.get("tech") or kind_note
    if sub:
        parts.append(f"<br/>[{_esc(sub)}]")
    if obj.get("description"):
        parts.append(f"<br/>{_esc(obj['description'])}")
    return "".join(parts)


def _m_node(eid, obj, cls, kind_note=""):
    return f'{_mid(eid)}["{_mlabel(obj, kind_note)}"]:::{cls}'


def _m_edge(rel, s, d):
    label = _rel_label(rel)
    if rel.get("kind") == "bidirectional":
        arrow = f'<-->|"{label}"|'
    elif rel.get("kind") == "async":
        arrow = f'-.->|"{label}"|'
    else:
        arrow = f'-->|"{label}"|'
    return f"{_mid(s)} {arrow} {_mid(d)}"


def _mermaid_wrap(title, body_lines):
    out = [f"%% {title}", "flowchart TB"]
    out += ["    " + l for l in body_lines]
    out += ["    " + c for c in _MERMAID_CLASSDEFS]
    return "\n".join(out) + "\n"


def mermaid_context(ir):
    elements, comp_parent = index_of(ir)
    sys = ir["system"]
    body = []
    for p in ir.get("persons", []):
        body.append(_m_node(p["id"], p, "person", "person"))
    body.append(_m_node(sys["id"], sys, "system", "system"))
    for e in ir.get("externals", []):
        body.append(_m_node(e["id"], e, "external"))
    seen = set()
    for rel in ir.get("relations", []):
        s = _map_to_context_level(rel["from"], elements) or sys["id"]
        d = _map_to_context_level(rel["to"], elements) or sys["id"]
        if s == d:
            continue
        key = (s, d, _rel_label(rel))
        if key in seen:
            continue
        seen.add(key)
        body.append(_m_edge(rel, s, d))
    return _mermaid_wrap(f"System Context - {_esc(sys['name'])}", body)


def mermaid_container(ir):
    elements, comp_parent = index_of(ir)
    sys = ir["system"]
    body = []
    for p in ir.get("persons", []):
        body.append(_m_node(p["id"], p, "person", "person"))
    body.append(f'subgraph {_mid(sys["id"])}_b["{_esc(sys["name"])}"]')
    for c in ir.get("containers", []):
        body.append("    " + _m_node(c["id"], c, "container"))
    for d in ir.get("datastores", []):
        body.append("    " + _m_node(d["id"], d, "db"))
    body.append("end")
    for e in ir.get("externals", []):
        body.append(_m_node(e["id"], e, "external"))
    seen = set()
    for rel in ir.get("relations", []):
        s = _map_to_container_level(rel["from"], elements, comp_parent)
        d = _map_to_container_level(rel["to"], elements, comp_parent)
        if s == d or s not in elements or d not in elements:
            continue
        if elements[s][0] == "system" or elements[d][0] == "system":
            continue
        key = (s, d, _rel_label(rel))
        if key in seen:
            continue
        seen.add(key)
        body.append(_m_edge(rel, s, d))
    return _mermaid_wrap(f"Container Diagram - {_esc(sys['name'])}", body)


def mermaid_component(ir, container_id):
    elements, comp_parent = index_of(ir)
    sys = ir["system"]
    container = next(c for c in ir["containers"] if c["id"] == container_id)
    comp_ids = {comp["id"] for comp in container.get("components", [])}
    rels, refs = [], set()
    for rel in ir.get("relations", []):
        f_in, t_in = rel["from"] in comp_ids, rel["to"] in comp_ids
        if not (f_in or t_in):
            continue
        s = rel["from"] if f_in else _map_to_container_level(rel["from"], elements, comp_parent)
        d = rel["to"] if t_in else _map_to_container_level(rel["to"], elements, comp_parent)
        if s not in elements or d not in elements or s == d:
            continue
        if elements[s][0] == "system" or elements[d][0] == "system":
            continue
        rels.append((rel, s, d))
        for end in (s, d):
            if end not in comp_ids:
                refs.add(end)
    body = [f'subgraph {_mid(container_id)}_b["{_esc(container["name"])}"]']
    for comp in container.get("components", []):
        body.append("    " + _m_node(comp["id"], comp, "component"))
    body.append("end")
    clsmap = {"person": "person", "container": "container", "datastore": "db", "external": "external"}
    for rid in sorted(refs):
        cat, obj = elements[rid]
        body.append(_m_node(rid, obj, clsmap.get(cat, "external")))
    seen = set()
    for rel, s, d in rels:
        key = (s, d, _rel_label(rel))
        if key in seen:
            continue
        seen.add(key)
        body.append(_m_edge(rel, s, d))
    return _mermaid_wrap(f"Component Diagram - {_esc(container['name'])}", body)


if __name__ == "__main__":
    import json
    import sys as _sys
    ir = json.load(open(_sys.argv[1], encoding="utf-8"))
    which = _sys.argv[2] if len(_sys.argv) > 2 else "container"
    if which == "context":
        print(plantuml_context(ir))
    elif which == "container":
        print(plantuml_container(ir))
    else:
        print(plantuml_component(ir, which))
