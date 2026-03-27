#!/usr/bin/env python3
"""Shared validation helpers for repository-local contract validators."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parent.parent


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"[ERROR] File not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"[ERROR] Invalid JSON in {path}: {exc}")


def load_schema(schema_name: str) -> dict:
    schema = load_json(ROOT / "schemas" / schema_name)
    if not isinstance(schema, dict):
        raise SystemExit(f"[ERROR] Top-level schema value must be an object: {schema_name}")
    return schema


def parse_iso_datetime(value: object, field_name: str, *, allow_null: bool = False) -> datetime | None:
    if value is None and allow_null:
        return None
    if not isinstance(value, str):
        allowed = "string or null" if allow_null else "string"
        raise SystemExit(f"[ERROR] {field_name} must be a {allowed}.")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise SystemExit(f"[ERROR] {field_name} is not a valid ISO 8601 timestamp: {value}")


def assert_iso_datetime(value: object, field_name: str, *, allow_null: bool = False) -> None:
    parse_iso_datetime(value, field_name, allow_null=allow_null)


def assert_iso_datetime_order(start_value: object, end_value: object, *, start_name: str, end_name: str) -> None:
    start = parse_iso_datetime(start_value, start_name)
    end = parse_iso_datetime(end_value, end_name)
    if end < start:
        raise SystemExit(f"[ERROR] {end_name} must not be earlier than {start_name}.")


def validate_json_instance(instance: object, schema: dict, *, label: str) -> None:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(instance), key=lambda err: list(err.path))
    if errors:
        lines = [f"[ERROR] {label} failed schema validation:"]
        for error in errors:
            path = ".".join(str(item) for item in error.path) or "<root>"
            lines.append(f"  - {path}: {error.message}")
        raise SystemExit("\n".join(lines))
