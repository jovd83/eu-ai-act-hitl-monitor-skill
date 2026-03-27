#!/usr/bin/env python3
"""Repository-local validator for the bundled skill folder."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


MAX_SKILL_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_COMPATIBILITY_LENGTH = 500
ALLOWED_FRONTMATTER_KEYS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}


def _extract_frontmatter(content: str) -> dict:
    if not content.startswith("---"):
        raise ValueError("No YAML frontmatter found")

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        raise ValueError("Invalid frontmatter format")

    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML in frontmatter: {exc}") from exc

    if not isinstance(frontmatter, dict):
        raise ValueError("Frontmatter must be a YAML dictionary")
    return frontmatter


def validate_skill(skill_path: Path) -> tuple[bool, str]:
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    openai_yaml = skill_path / "agents" / "openai.yaml"
    if not openai_yaml.exists():
        return False, "agents/openai.yaml not found"

    references_dir = skill_path / "references"
    if not references_dir.exists() or not references_dir.is_dir():
        return False, "references directory not found"

    try:
        frontmatter = _extract_frontmatter(skill_md.read_text(encoding="utf-8"))
    except ValueError as exc:
        return False, str(exc)

    unexpected = set(frontmatter) - ALLOWED_FRONTMATTER_KEYS
    if unexpected:
        return False, f"Unexpected frontmatter keys: {', '.join(sorted(unexpected))}"

    for required_key in ("name", "description"):
        if required_key not in frontmatter:
            return False, f"Missing '{required_key}' in frontmatter"

    name = str(frontmatter["name"]).strip()
    if not re.fullmatch(r"[a-z0-9-]+", name):
        return False, f"Name '{name}' must be lowercase hyphen-case"
    if name.startswith("-") or name.endswith("-") or "--" in name:
        return False, f"Name '{name}' cannot start/end with '-' or contain '--'"
    if len(name) > MAX_SKILL_NAME_LENGTH:
        return False, f"Name is too long ({len(name)}). Maximum is {MAX_SKILL_NAME_LENGTH}"
    if name != skill_path.name:
        return False, f"Skill name '{name}' must match parent directory '{skill_path.name}'"

    description = str(frontmatter["description"]).strip()
    if not description:
        return False, "Description must not be empty"
    if len(description) > MAX_DESCRIPTION_LENGTH:
        return False, f"Description exceeds {MAX_DESCRIPTION_LENGTH} characters"

    license_value = frontmatter.get("license")
    if license_value is not None and (not isinstance(license_value, str) or not license_value.strip()):
        return False, "license must be a non-empty string when present"

    compatibility = frontmatter.get("compatibility")
    if compatibility is not None:
        if not isinstance(compatibility, str) or not compatibility.strip():
            return False, "compatibility must be a non-empty string when present"
        if len(compatibility) > MAX_COMPATIBILITY_LENGTH:
            return False, f"compatibility exceeds {MAX_COMPATIBILITY_LENGTH} characters"

    metadata = frontmatter.get("metadata")
    if metadata is not None:
        if not isinstance(metadata, dict):
            return False, "metadata must be a mapping when present"
        for key, value in metadata.items():
            if not isinstance(key, str) or not isinstance(value, str):
                return False, "metadata keys and values must be strings"

    allowed_tools = frontmatter.get("allowed-tools")
    if allowed_tools is not None and (not isinstance(allowed_tools, str) or not allowed_tools.strip()):
        return False, "allowed-tools must be a non-empty string when present"

    try:
        openai_config = yaml.safe_load(openai_yaml.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return False, f"Invalid YAML in agents/openai.yaml: {exc}"

    if not isinstance(openai_config, dict):
        return False, "agents/openai.yaml must contain a YAML dictionary"

    interface = openai_config.get("interface")
    if not isinstance(interface, dict):
        return False, "agents/openai.yaml must contain an interface mapping"

    for key in ("display_name", "short_description", "default_prompt"):
        value = interface.get(key)
        if not isinstance(value, str) or not value.strip():
            return False, f"agents/openai.yaml interface.{key} must be a non-empty string"

    if f"${name}" not in interface["default_prompt"]:
        return False, "agents/openai.yaml interface.default_prompt should reference the skill name"

    reference_files = list(references_dir.glob("*.md"))
    if not reference_files:
        return False, "references directory must contain at least one Markdown reference file"

    return True, "Skill is valid!"


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: validate_skill.py <skill_directory>")

    valid, message = validate_skill(Path(sys.argv[1]).resolve())
    print(message)
    raise SystemExit(0 if valid else 1)


if __name__ == "__main__":
    main()
