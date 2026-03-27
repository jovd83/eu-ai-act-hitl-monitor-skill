#!/usr/bin/env python3
"""Validate a review decision JSON file against the repository JSON Schema."""

from __future__ import annotations

import sys
from pathlib import Path

from _validation import (
    assert_iso_datetime,
    assert_iso_datetime_order,
    load_json,
    load_schema,
    validate_json_instance,
)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: validate_review_decision.py <decision.json>")

    decision_path = Path(sys.argv[1]).resolve()
    decision = load_json(decision_path)
    schema = load_schema("review-decision.schema.json")
    schema_path = Path(__file__).resolve().parent.parent / "schemas" / "review-decision.schema.json"

    if not isinstance(decision, dict):
        raise SystemExit("[ERROR] Top-level JSON value must be an object.")
    validate_json_instance(decision, schema, label="Review decision")

    assert_iso_datetime(decision.get("review_started_at"), "review_started_at")
    assert_iso_datetime(decision.get("review_submitted_at"), "review_submitted_at")
    assert_iso_datetime_order(
        decision.get("review_started_at"),
        decision.get("review_submitted_at"),
        start_name="review_started_at",
        end_name="review_submitted_at",
    )

    print(f"[OK] Review decision is valid: {decision_path}")
    print(f"[OK] Schema used: {schema_path}")


if __name__ == "__main__":
    main()
