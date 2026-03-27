#!/usr/bin/env python3
"""Validate an interception policy JSON file against the repository JSON Schema."""

from __future__ import annotations

import sys
from pathlib import Path

from _validation import load_json, load_schema, validate_json_instance


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: validate_interception_policy.py <policy.json>")

    policy_path = Path(sys.argv[1]).resolve()
    schema_path = Path(__file__).resolve().parent.parent / "schemas" / "interception-policy.schema.json"

    policy = load_json(policy_path)
    schema = load_schema("interception-policy.schema.json")

    if not isinstance(policy, dict):
        raise SystemExit("[ERROR] Top-level JSON value must be an object.")

    validate_json_instance(policy, schema, label="Interception policy")

    print(f"[OK] Interception policy is valid: {policy_path}")
    print(f"[OK] Schema used: {schema_path}")


if __name__ == "__main__":
    main()
