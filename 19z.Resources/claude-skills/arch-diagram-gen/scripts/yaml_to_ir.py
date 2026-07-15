"""Adapter: hand-written architecture.yaml -> IR JSON (stdout).

The YAML mirrors the IR 1:1 (see assets/architecture.example.yaml), so this is
essentially a format conversion plus a light shape check. Use when there is no
graphify graph and a repo scan is too coarse — e.g. documenting a planned system.

Usage:
    python yaml_to_ir.py architecture.yaml > ir.json
"""
from __future__ import annotations
import json
import sys

try:
    import yaml  # PyYAML
except ImportError:
    sys.stderr.write(
        "PyYAML not installed. Either `pip install pyyaml`, or just write the IR as "
        "JSON directly (the YAML mirrors the IR 1:1) and skip this adapter.\n")
    sys.exit(2)


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("usage: yaml_to_ir.py architecture.yaml\n")
        sys.exit(2)
    with open(sys.argv[1], encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict) or "system" not in data or "containers" not in data:
        sys.stderr.write("YAML must have at least top-level `system` and `containers` keys.\n")
        sys.exit(1)
    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
