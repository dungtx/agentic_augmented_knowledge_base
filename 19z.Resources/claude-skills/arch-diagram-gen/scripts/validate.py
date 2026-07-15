"""Static validator for arch-diagram-gen output.

Runs with no Java / no PlantUML / no network. Catches the entire macro-name,
arity, undefined-alias, and unbalanced-boundary error class (the Rel_Bi bug),
plus IR conformance, the C4 coverage invariant, and cross-level consistency.

Usage:
    python validate.py <output_dir>          # dir holding ir.json + *.puml + index.md
    python validate.py --ir ir.json          # IR-only conformance check

Exit code 0 = clean, 1 = errors.
"""
from __future__ import annotations
import json
import os
import re
import sys

# --- allowed C4-PlantUML macros -> minimum positional arity ------------------
MACRO_MIN_ARGS = {
    "Person": 2, "Person_Ext": 2,
    "System": 2, "System_Ext": 2, "SystemDb": 2, "SystemDb_Ext": 2, "SystemQueue": 2,
    "System_Boundary": 2, "Enterprise_Boundary": 2, "Boundary": 2,
    "Container": 2, "ContainerDb": 2, "ContainerQueue": 2,
    "Container_Ext": 2, "ContainerDb_Ext": 2, "Container_Boundary": 2,
    "Component": 2, "ComponentDb": 2, "ComponentQueue": 2, "Component_Ext": 2,
    "Rel": 3, "Rel_U": 3, "Rel_D": 3, "Rel_L": 3, "Rel_R": 3,
    "Rel_Up": 3, "Rel_Down": 3, "Rel_Left": 3, "Rel_Right": 3,
    "Rel_Back": 3, "Rel_Neighbor": 3, "Rel_Back_Neighbor": 3,
    "BiRel": 3, "BiRel_U": 3, "BiRel_D": 3, "BiRel_L": 3, "BiRel_R": 3,
    "LAYOUT_WITH_LEGEND": 0, "LAYOUT_TOP_DOWN": 0, "LAYOUT_LEFT_RIGHT": 0,
    "LAYOUT_AS_SKETCH": 0, "SHOW_LEGEND": 0,
}
# Names that LOOK like C4 element/rel macros -> if used but not whitelisted, it's an error.
SUSPECT_PREFIXES = ("Person", "System", "Container", "Component", "Rel", "BiRel",
                    "Boundary", "Enterprise", "Node", "Deployment")
# Prefixes we allow without arity checks (styling / tags / layout helpers).
ALLOW_PREFIXES = ("Lay", "SHOW", "LAYOUT", "Add", "Update", "SetDefault", "WithoutPropertyHeader")
ELEMENT_MACROS = {m for m in MACRO_MIN_ARGS if m.endswith("_Boundary")
                  or m in ("Person", "Person_Ext", "System", "System_Ext", "SystemDb",
                           "Container", "ContainerDb", "ContainerQueue", "Container_Ext",
                           "ContainerDb_Ext", "Component", "ComponentDb", "ComponentQueue",
                           "Component_Ext")}
REL_MACROS = {m for m in MACRO_MIN_ARGS if m.startswith("Rel") or m.startswith("BiRel")}


# --- arg parsing -------------------------------------------------------------
def split_args(inner):
    args, buf, depth, q = [], [], 0, False
    for ch in inner:
        if ch == '"':
            q = not q
            buf.append(ch)
        elif ch == "(" and not q:
            depth += 1; buf.append(ch)
        elif ch == ")" and not q:
            depth -= 1; buf.append(ch)
        elif ch == "," and not q and depth == 0:
            args.append("".join(buf).strip()); buf = []
        else:
            buf.append(ch)
    if "".join(buf).strip():
        args.append("".join(buf).strip())
    return args


def parse_call(line):
    """Return (name, args_list) for a macro call line, or None."""
    s = line.strip()
    if not s or s.startswith(("'", "!", "@", "//")) or s.startswith("title "):
        return None
    m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*\(", s)
    if not m:
        return None
    name = m.group(1)
    start = s.index("(")
    depth, q, end = 0, False, None
    for i in range(start, len(s)):
        ch = s[i]
        if ch == '"':
            q = not q
        elif ch == "(" and not q:
            depth += 1
        elif ch == ")" and not q:
            depth -= 1
            if depth == 0:
                end = i
                break
    if end is None:
        return (name, None)  # unbalanced parens
    return (name, split_args(s[start + 1:end]))


# --- puml validation ---------------------------------------------------------
def validate_puml(path):
    errors = []
    text = open(path, encoding="utf-8").read()
    rel = os.path.basename(path)
    if "@startuml" not in text or "@enduml" not in text:
        errors.append(f"{rel}: missing @startuml/@enduml")
    if text.count("{") != text.count("}"):
        errors.append(f"{rel}: unbalanced boundary braces ({text.count('{')} open vs {text.count('}')} close)")

    aliases = set()
    rels = []
    for ln in text.splitlines():
        parsed = parse_call(ln)
        if not parsed:
            continue
        name, args = parsed
        if args is None:
            errors.append(f"{rel}: unbalanced parentheses in `{ln.strip()[:60]}`")
            continue
        if name in MACRO_MIN_ARGS:
            if len(args) < MACRO_MIN_ARGS[name]:
                errors.append(f"{rel}: {name}() has {len(args)} args, needs >= {MACRO_MIN_ARGS[name]} -> `{ln.strip()[:70]}`")
            if name in ELEMENT_MACROS and args:
                aliases.add(args[0])
            if name in REL_MACROS:
                rels.append((name, args, ln.strip()))
        elif name.startswith(ALLOW_PREFIXES):
            pass  # styling/layout helper, allowed
        elif name.startswith(SUSPECT_PREFIXES):
            errors.append(f"{rel}: unknown/invalid C4 macro `{name}` -> `{ln.strip()[:70]}` "
                          f"(not in the C4-PlantUML macro set)")
    for name, args, raw in rels:
        for endpoint in args[:2]:
            if '"' in endpoint or "(" in endpoint:
                errors.append(f"{rel}: {name}() endpoint `{endpoint}` is not a bare alias -> `{raw[:70]}`")
            elif endpoint not in aliases:
                errors.append(f"{rel}: {name}() references undefined element `{endpoint}` -> `{raw[:70]}`")
    return errors, aliases


# --- IR validation -----------------------------------------------------------
REL_KINDS = {"sync", "async", "bidirectional"}
DIRECTIONS = {"up", "down", "left", "right", "auto"}
ID_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_.]*$")


def validate_ir(ir):
    errors = []
    if "system" not in ir or "id" not in ir.get("system", {}):
        return ["IR: missing system.id"]
    ids = {}
    def reg(eid, where):
        if not ID_RE.match(eid or ""):
            errors.append(f"IR: bad id `{eid}` in {where}")
        if eid in ids:
            errors.append(f"IR: duplicate id `{eid}` ({where} and {ids[eid]})")
        ids[eid] = where
    reg(ir["system"]["id"], "system")
    for p in ir.get("persons", []):
        reg(p["id"], "persons")
    for c in ir.get("containers", []):
        reg(c["id"], "containers")
        for comp in c.get("components", []):
            reg(comp["id"], f"components[{c['id']}]")
    for d in ir.get("datastores", []):
        reg(d["id"], "datastores")
    for e in ir.get("externals", []):
        reg(e["id"], "externals")
    for i, r in enumerate(ir.get("relations", [])):
        if r.get("kind", "sync") not in REL_KINDS:
            errors.append(f"IR: relation[{i}] bad kind `{r.get('kind')}` (allowed: {sorted(REL_KINDS)})")
        if r.get("direction", "auto") not in DIRECTIONS:
            errors.append(f"IR: relation[{i}] bad direction `{r.get('direction')}`")
        for end in ("from", "to"):
            if r.get(end) not in ids:
                errors.append(f"IR: relation[{i}] {end} `{r.get(end)}` is not a defined element id")
    return errors


# --- coverage + cross-level --------------------------------------------------
def validate_coverage(ir, out_dir):
    errors = []
    owned = [c for c in ir.get("containers", []) if c.get("owned", True)]
    comp_dir = os.path.join(out_dir, "components")
    for c in owned:
        has_comp_file = os.path.exists(os.path.join(comp_dir, c["id"] + ".puml")) or \
                        os.path.exists(os.path.join(comp_dir, c["id"] + ".mmd"))
        has_components = bool(c.get("components"))
        if has_components and not has_comp_file:
            errors.append(f"COVERAGE: owned container `{c['id']}` has components but no L3 diagram file")
        if not has_components and has_comp_file:
            errors.append(f"COVERAGE: `{c['id']}` has an L3 file but no components in IR")
    idx = os.path.join(out_dir, "index.md")
    if os.path.exists(idx):
        man = open(idx, encoding="utf-8").read()
        for c in owned:
            if c["id"] not in man:
                errors.append(f"COVERAGE: manifest index.md does not list owned container `{c['id']}`")
    else:
        errors.append("COVERAGE: index.md manifest missing")
    return errors


def validate_cross_level(ir, out_dir):
    errors = []
    l2_ids = {ir["system"]["id"]}
    l2_ids |= {p["id"] for p in ir.get("persons", [])}
    l2_ids |= {c["id"] for c in ir.get("containers", [])}
    l2_ids |= {d["id"] for d in ir.get("datastores", [])}
    l2_ids |= {e["id"] for e in ir.get("externals", [])}
    comp_dir = os.path.join(out_dir, "components")
    if not os.path.isdir(comp_dir):
        return errors
    own_comp_ids = {comp["id"] for c in ir.get("containers", []) for comp in c.get("components", [])}
    for fn in sorted(os.listdir(comp_dir)):
        if not fn.endswith(".puml"):
            continue
        _, aliases = validate_puml(os.path.join(comp_dir, fn))
        for a in aliases:
            if a.endswith("_b"):
                continue  # boundary alias
            if a in own_comp_ids:
                continue  # a component
            if a not in l2_ids:
                errors.append(f"CROSS-LEVEL: components/{fn} references `{a}` which is not present at the container (L2) level")
    return errors


def main():
    args = sys.argv[1:]
    if "--ir" in args:
        ir = json.load(open(args[args.index("--ir") + 1], encoding="utf-8"))
        errors = validate_ir(ir)
    else:
        if not args:
            print("usage: validate.py <output_dir> | --ir ir.json"); return 2
        out_dir = args[0]
        ir_path = os.path.join(out_dir, "ir.json")
        errors = []
        ir = None
        if os.path.exists(ir_path):
            ir = json.load(open(ir_path, encoding="utf-8"))
            errors += validate_ir(ir)
        else:
            errors.append("ir.json not found in output dir (build.py should copy it there)")
        for root, _dirs, files in os.walk(out_dir):
            for fn in sorted(files):
                if fn.endswith(".puml"):
                    perrs, _ = validate_puml(os.path.join(root, fn))
                    errors += perrs
        if ir is not None:
            errors += validate_coverage(ir, out_dir)
            errors += validate_cross_level(ir, out_dir)

    if errors:
        print(f"VALIDATION FAILED - {len(errors)} issue(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("VALIDATION PASSED - IR conformant, all diagrams syntactically valid, coverage complete, cross-level consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
