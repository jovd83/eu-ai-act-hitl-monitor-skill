#!/usr/bin/env python3
"""Validate version consistency across repository markers."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_version(pattern: str, text: str, source: str) -> str:
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        raise SystemExit(f"[ERROR] Could not find version in {source}")
    return match.group(1)


def load_json(path: Path) -> dict:
    return json.loads(read_text(path))


def main() -> None:
    root_version = read_text(ROOT / "VERSION").strip()
    pyproject_version = extract_version(r'^version = "([^"]+)"$', read_text(ROOT / "pyproject.toml"), "pyproject.toml")
    package_version = load_json(ROOT / "package.json")["version"]
    package_lock_version = load_json(ROOT / "package-lock.json")["version"]

    if len({root_version, pyproject_version, package_version, package_lock_version}) != 1:
        raise SystemExit(
            "[ERROR] Repository/package versions do not match:\n"
            f"  VERSION={root_version}\n"
            f"  pyproject.toml={pyproject_version}\n"
            f"  package.json={package_version}\n"
            f"  package-lock.json={package_lock_version}"
        )

    schema_versions = {
        "handover-packet.schema.json": load_json(ROOT / "schemas" / "handover-packet.schema.json")["x-version"],
        "review-decision.schema.json": load_json(ROOT / "schemas" / "review-decision.schema.json")["x-version"],
        "interception-policy.schema.json": load_json(ROOT / "schemas" / "interception-policy.schema.json")["x-version"],
    }
    for schema_name, schema_version in schema_versions.items():
        if not re.fullmatch(r"\d+\.\d+\.\d+", schema_version):
            raise SystemExit(f"[ERROR] Invalid schema version in {schema_name}: {schema_version}")

    example_files = [
        ROOT / "examples" / "interception-policy.example.json",
        ROOT / "examples" / "handover-packet.example.json",
        ROOT / "examples" / "review-decision.example.json",
        ROOT / "examples" / "bug-fix-handover-packet.example.json",
        ROOT / "examples" / "bug-fix-review-decision.example.json",
        ROOT / "examples" / "feature-implementation-handover-packet.example.json",
        ROOT / "examples" / "feature-implementation-review-decision.example.json",
    ]
    example_versions = {}
    for path in example_files:
        payload = load_json(path)
        version = payload.get("example_version")
        if not version:
            raise SystemExit(f"[ERROR] Missing example_version in {path.name}")
        example_versions[path.name] = version

    distinct_example_versions = set(example_versions.values())
    if len(distinct_example_versions) != 1:
        lines = ["[ERROR] Example versions do not match:"]
        for name, version in example_versions.items():
            lines.append(f"  {name}={version}")
        raise SystemExit("\n".join(lines))

    print(f"[OK] Repository version is consistent: {root_version}")
    print(f"[OK] Schema versions: {schema_versions}")
    print(f"[OK] Example version: {distinct_example_versions.pop()}")


if __name__ == "__main__":
    main()
