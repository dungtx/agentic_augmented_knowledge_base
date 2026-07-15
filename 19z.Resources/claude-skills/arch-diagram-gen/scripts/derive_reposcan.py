"""Adapter: generic repo scan -> skeleton IR (stdout).

Detects containers (deployable units) by manifest files anywhere in the tree:
package.json, go.mod, pyproject.toml/setup.py, pom.xml/build.gradle, Cargo.toml,
or a Dockerfile. Also parses docker-compose services. Components, datastores,
externals and relations are left for the model to enrich (SKILL.md step 2).

Usage:
    python derive_reposcan.py <repo_root> [--system NAME] [--max-depth 3]
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys

MANIFESTS = {
    "package.json": "Node/TS", "go.mod": "Go", "pyproject.toml": "Python",
    "setup.py": "Python", "pom.xml": "Java", "build.gradle": "JVM",
    "Cargo.toml": "Rust", "Dockerfile": "container",
}
SKIP_DIRS = {"node_modules", ".venv", "venv", "dist", "build", "lib", "libs",
             "__pycache__", ".git", "coverage", "vendor", "target", ".next"}


def sanitize(s):
    s = re.sub(r"[^A-Za-z0-9_]", "_", str(s))
    return s.strip("_") or "x"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--system", default="")
    ap.add_argument("--max-depth", type=int, default=3)
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    sysname = a.system or os.path.basename(root.rstrip("/\\"))

    found = {}  # container dir -> tech
    for cur, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        depth = cur[len(root):].count(os.sep)
        if depth > a.max_depth:
            dirs[:] = []
            continue
        for fn in files:
            if fn in MANIFESTS:
                rel = os.path.relpath(cur, root).replace("\\", "/")
                name = rel if rel != "." else os.path.basename(root)
                if name not in found or (found[name] == "container" and MANIFESTS[fn] != "container"):
                    found[name] = MANIFESTS[fn]

    containers = []
    for name in sorted(found):
        containers.append({
            "id": sanitize(name.split("/")[-1]),
            "name": name,
            "tech": found[name],
            "description": "",
            "owned": True,
            "components": [],
        })

    compose_services = []
    for cf in ("docker-compose.yml", "docker-compose.yaml",
               "docker-compose.dev.yml", "docker-compose.prod.yml"):
        p = os.path.join(root, cf)
        if os.path.exists(p):
            txt = open(p, encoding="utf-8", errors="ignore").read()
            m = re.search(r"^services:\s*$", txt, re.M)
            if m:
                block = txt[m.end():]
                for line in block.splitlines():
                    mm = re.match(r"^  ([A-Za-z0-9_.-]+):\s*$", line)
                    if mm:
                        compose_services.append(mm.group(1))

    ir = {
        "system": {"id": sanitize(sysname), "name": sysname, "description": ""},
        "persons": [],
        "containers": containers,
        "datastores": [],
        "externals": [],
        "relations": [],
    }
    print(json.dumps(ir, indent=2, ensure_ascii=False))
    sys.stderr.write(
        f"\n[derive_reposcan] {len(containers)} container(s) detected by manifest. "
        + (f"compose services seen: {', '.join(sorted(set(compose_services)))}. " if compose_services else "")
        + "ENRICH before building: add components per container, datastores, externals "
          "(DBs/vendor APIs), and relations. Then: build.py ir.json --out <dir>.\n")


if __name__ == "__main__":
    main()
