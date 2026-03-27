#!/usr/bin/env python3
"""Validate bundled positive and negative example fixtures."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PYTHON = sys.executable


POSITIVE_CASES = [
    ("interception policy", "scripts/validate_interception_policy.py", "examples/interception-policy.example.json"),
    ("generic handover packet", "scripts/validate_handover_packet.py", "examples/handover-packet.example.json"),
    ("generic review decision", "scripts/validate_review_decision.py", "examples/review-decision.example.json"),
    ("bug-fix handover packet", "scripts/validate_handover_packet.py", "examples/bug-fix-handover-packet.example.json"),
    ("bug-fix review decision", "scripts/validate_review_decision.py", "examples/bug-fix-review-decision.example.json"),
    (
        "feature handover packet",
        "scripts/validate_handover_packet.py",
        "examples/feature-implementation-handover-packet.example.json",
    ),
    (
        "feature review decision",
        "scripts/validate_review_decision.py",
        "examples/feature-implementation-review-decision.example.json",
    ),
]

NEGATIVE_CASES = [
    (
        "invalid handover missing review status",
        "scripts/validate_handover_packet.py",
        "examples/invalid/invalid-handover-missing-review-status.json",
    ),
    (
        "invalid handover bad trigger type",
        "scripts/validate_handover_packet.py",
        "examples/invalid/invalid-handover-bad-trigger-type.json",
    ),
    (
        "invalid handover pending state populated",
        "scripts/validate_handover_packet.py",
        "examples/invalid/invalid-handover-pending-review-fields-populated.json",
    ),
    (
        "invalid review bad timestamp",
        "scripts/validate_review_decision.py",
        "examples/invalid/invalid-review-bad-timestamp.json",
    ),
    (
        "invalid review submitted before start",
        "scripts/validate_review_decision.py",
        "examples/invalid/invalid-review-submitted-before-start.json",
    ),
    (
        "invalid review extra field",
        "scripts/validate_review_decision.py",
        "examples/invalid/invalid-review-extra-field.json",
    ),
    (
        "invalid policy missing human options",
        "scripts/validate_interception_policy.py",
        "examples/invalid/invalid-policy-missing-human-options.json",
    ),
]


def run_case(label: str, script: str, target: str, *, expect_success: bool) -> None:
    result = subprocess.run(
        [PYTHON, str(ROOT / script), str(ROOT / target)],
        capture_output=True,
        text=True,
        check=False,
    )
    if expect_success and result.returncode != 0:
        raise SystemExit(
            f"[ERROR] Expected {label} to pass.\n"
            f"Command: {script} {target}\n"
            f"Stdout:\n{result.stdout}\n"
            f"Stderr:\n{result.stderr}"
        )
    if not expect_success and result.returncode == 0:
        raise SystemExit(
            f"[ERROR] Expected {label} to fail.\n"
            f"Command: {script} {target}\n"
            f"Stdout:\n{result.stdout}\n"
            f"Stderr:\n{result.stderr}"
        )


def main() -> None:
    for label, script, target in POSITIVE_CASES:
        run_case(label, script, target, expect_success=True)
    for label, script, target in NEGATIVE_CASES:
        run_case(label, script, target, expect_success=False)

    print("[OK] All bundled example fixtures behaved as expected.")


if __name__ == "__main__":
    main()
