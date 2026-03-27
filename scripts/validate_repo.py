#!/usr/bin/env python3
"""Run the full repository validation workflow."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PYTHON = sys.executable


def run(command: list[str], label: str) -> None:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise SystemExit(
            f"[ERROR] {label} failed.\n"
            f"Command: {' '.join(command)}\n"
            f"Stdout:\n{result.stdout}\n"
            f"Stderr:\n{result.stderr}"
        )
    print(f"[OK] {label}")


def main() -> None:
    run([PYTHON, "scripts/validate_skill.py", "eu-ai-act-hitl-oversight-skill"], "skill validation")
    run([PYTHON, "scripts/validate_versions.py"], "version validation")
    run([PYTHON, "scripts/validate_examples.py"], "example validation")
    run([PYTHON, "reference-implementations/python/handover_models.py"], "python reference validation")

    npm = shutil.which("npm")
    if npm:
        run([npm, "run", "typecheck"], "typescript typecheck")
    else:
        print("[WARN] npm not found; skipping TypeScript typecheck.")

    print("[OK] Repository validation completed successfully.")


if __name__ == "__main__":
    main()
