#!/usr/bin/env python3
"""Validate a handover packet JSON file against the repository JSON Schema."""

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


def _validate_review_semantics(review: dict) -> None:
    status = review.get("status")
    reviewer_id = review.get("reviewer_id")
    review_started_at = review.get("review_started_at")
    review_submitted_at = review.get("review_submitted_at")
    review_duration_ms = review.get("review_duration_ms")
    decision_reason = review.get("decision_reason")
    modifications = review.get("modifications")

    if review_started_at is not None and review_submitted_at is not None:
        assert_iso_datetime_order(
            review_started_at,
            review_submitted_at,
            start_name="review.review_started_at",
            end_name="review.review_submitted_at",
        )

    if status == "pending":
        unexpected = {
            "reviewer_id": reviewer_id,
            "review_started_at": review_started_at,
            "review_submitted_at": review_submitted_at,
            "review_duration_ms": review_duration_ms,
            "decision_reason": decision_reason,
            "modifications": modifications,
        }
        for field_name, value in unexpected.items():
            if value is not None:
                raise SystemExit(f"[ERROR] review.{field_name} must be null while review.status is pending.")
        return

    required_non_null = {
        "reviewer_id": reviewer_id,
        "review_started_at": review_started_at,
        "review_submitted_at": review_submitted_at,
        "review_duration_ms": review_duration_ms,
        "decision_reason": decision_reason,
    }

    if status == "modify":
        required_non_null["modifications"] = modifications
    elif status in {"approve", "reject", "kill", "request_more_context"}:
        if modifications is not None:
            raise SystemExit("[ERROR] review.modifications must be null unless review.status is modify.")
    elif status == "timeout":
        timeout_required = {
            "review_submitted_at": review_submitted_at,
            "review_duration_ms": review_duration_ms,
            "decision_reason": decision_reason,
        }
        for field_name, value in timeout_required.items():
            if value is None:
                raise SystemExit(f"[ERROR] review.{field_name} must be present when review.status is timeout.")
        if modifications is not None:
            raise SystemExit("[ERROR] review.modifications must be null when review.status is timeout.")
        return

    for field_name, value in required_non_null.items():
        if value is None:
            raise SystemExit(f"[ERROR] review.{field_name} must be present when review.status is {status}.")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: validate_handover_packet.py <packet.json>")

    packet_path = Path(sys.argv[1]).resolve()
    packet = load_json(packet_path)
    schema = load_schema("handover-packet.schema.json")
    schema_path = Path(__file__).resolve().parent.parent / "schemas" / "handover-packet.schema.json"

    if not isinstance(packet, dict):
        raise SystemExit("[ERROR] Top-level JSON value must be an object.")

    validate_json_instance(packet, schema, label="Packet")

    assert_iso_datetime(packet.get("created_at"), "created_at")
    review_requirements = packet.get("review_requirements", {})
    if isinstance(review_requirements, dict):
        assert_iso_datetime(review_requirements.get("decision_deadline_at"), "review_requirements.decision_deadline_at")

    review = packet.get("review", {})
    if isinstance(review, dict):
        assert_iso_datetime(review.get("review_started_at"), "review.review_started_at", allow_null=True)
        assert_iso_datetime(review.get("review_submitted_at"), "review.review_submitted_at", allow_null=True)
        _validate_review_semantics(review)

    print(f"[OK] Packet is valid: {packet_path}")
    print(f"[OK] Schema used: {schema_path}")


if __name__ == "__main__":
    main()
