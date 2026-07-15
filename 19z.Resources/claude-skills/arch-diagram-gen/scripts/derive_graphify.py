"""Adapter: graphify graph.json -> skeleton IR (stdout).

Groups nodes by service (the first path segment of source_file) into containers,
and seeds each owned container with its highest-degree nodes as candidate
components. It does NOT invent relations or externals reliably — that's the
model's enrichment job (see SKILL.md step 2).

Usage:
    python derive_graphify.py <graph.json> [--product PREFIX] [--system NAME] [--top N]
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict


def top_dir(sf):
    sf = (sf or "").replace("\\", "/").lstrip("/")
    return sf.split("/")[0] if sf else ""


def sanitize(s):
    s = re.sub(r"[^A-Za-z0-9_]", "_", str(s))
    return s.strip("_") or "x"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("graph")
    ap.add_argument("--product", default="", help="only treat services with this dir prefix as owned")
    ap.add_argument("--system", default="", help="system id/name (default: product or 'system')")
    ap.add_argument("--top", type=int, default=6, help="candidate components per container")
    a = ap.parse_args()

    g = json.load(open(a.graph, encoding="utf-8"))
    nodes = {n["id"]: n for n in g["nodes"]}
    links = g.get("links", g.get("edges", []))

    degree = Counter()
    for e in links:
        degree[e.get("source")] += 1
        degree[e.get("target")] += 1

    by_service = defaultdict(list)
    for nid, n in nodes.items():
        svc = top_dir(n.get("source_file", ""))
        if svc:
            by_service[svc].append(nid)

    system_id = sanitize(a.system or a.product or "system")
    containers = []
    SKIP = re.compile(r"(package\.json|package-lock|tsconfig|requirements|nodemon|\.env|"
                      r"dockerfile|docker-compose|readme|__init__)", re.I)
    for svc in sorted(by_service):
        owned = True if not a.product else svc.startswith(a.product)
        ranked = sorted(by_service[svc], key=lambda x: -degree[x])
        comps = []
        seen = set()
        for nid in ranked:
            n = nodes[nid]
            sf = str(n.get("source_file", ""))
            label = n.get("label", nid)
            if SKIP.search(sf) or SKIP.search(label):
                continue
            cid = f"{sanitize(svc)}.{sanitize(label)[:30]}"
            if cid in seen:
                continue
            seen.add(cid)
            comps.append({"id": cid, "name": label,
                          "description": os.path.basename(sf)})
            if len(comps) >= a.top:
                break
        containers.append({"id": sanitize(svc), "name": svc, "tech": "",
                           "description": "", "owned": owned, "components": comps})

    ir = {
        "system": {"id": system_id, "name": a.system or a.product or "system",
                   "description": ""},
        "persons": [],
        "containers": containers,
        "datastores": [],
        "externals": [],
        "relations": [],
    }
    print(json.dumps(ir, indent=2, ensure_ascii=False))
    sys.stderr.write(
        f"\n[derive_graphify] skeleton: {len(containers)} containers "
        f"({sum(c['owned'] for c in containers)} owned). "
        "ENRICH before building: refine component lists, add datastores, externals, "
        "and relations (with kind/direction). Then: build.py ir.json --out <dir>.\n")


if __name__ == "__main__":
    main()
