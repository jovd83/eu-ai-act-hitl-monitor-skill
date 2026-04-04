#!/usr/bin/env python3
"""Validate all agent skill directories in the repository."""

from __future__ import annotations

from pathlib import Path

from validate_skill import validate_skill


ROOT = Path(__file__).resolve().parent.parent
SKILL_FILE = "SKILL.md"
SKIP_DIRS = {
    ".git",
    ".github",
    ".vscode",
    "docs",
    "evals",
    "examples",
    "node_modules",
    "reference-implementations",
    "schemas",
    "scripts",
}


def discover_skill_directories(root: Path) -> list[Path]:
    skill_dirs: list[Path] = []
    for path in root.iterdir():
        if not path.is_dir() or path.name in SKIP_DIRS:
            continue
        if (path / SKILL_FILE).is_file():
            skill_dirs.append(path)
    return sorted(skill_dirs)


def main() -> None:
    skill_dirs = discover_skill_directories(ROOT)
    if not skill_dirs:
        raise SystemExit("[ERROR] No skill directories with SKILL.md were found.")

    failures: list[str] = []
    for skill_dir in skill_dirs:
        valid, message = validate_skill(skill_dir)
        if valid:
            print(f"[OK] {skill_dir.name}: {message}")
            continue
        failures.append(f"[ERROR] {skill_dir.name}: {message}")

    if failures:
        raise SystemExit("\n".join(failures))

    print(f"[OK] Validated {len(skill_dirs)} agent skill director{'y' if len(skill_dirs) == 1 else 'ies'}.")


if __name__ == "__main__":
    main()
