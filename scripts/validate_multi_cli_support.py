#!/usr/bin/env python3
"""Validate Open Agent Skill multi-CLI routing files."""

from __future__ import annotations

import re
from pathlib import Path

from common import fail


ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / ".agents" / "skills" / "job-application-quality" / "SKILL.md"
WRAPPER_TARGET = "../../../.agents/skills/job-application-quality/SKILL.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_frontmatter(content: str, label: str) -> list[str]:
    errors: list[str] = []
    if not content.startswith("---\n"):
        return [f"{label}: missing YAML frontmatter"]
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        return [f"{label}: malformed YAML frontmatter"]
    frontmatter = match.group(1)
    for key in ("name:", "description:", "license:"):
        if key not in frontmatter:
            errors.append(f"{label}: frontmatter missing {key}")
    return errors


def validate() -> list[str]:
    errors: list[str] = []

    if not CANONICAL.is_file():
        errors.append(f"missing canonical skill: {CANONICAL.relative_to(ROOT)}")
    else:
        content = read(CANONICAL)
        errors += validate_frontmatter(content, ".agents skill")
        for token in (
            "user-invocable: true",
            "argument-hint:",
            "## Mode Routing",
            "## Pre-Submit Checklist",
        ):
            if token not in content:
                errors.append(f".agents skill: missing {token}")

    for wrapper in (
        ROOT / ".claude" / "skills" / "job-application-quality" / "SKILL.md",
        ROOT / ".qwen" / "skills" / "job-application-quality" / "SKILL.md",
    ):
        if not wrapper.is_file():
            errors.append(f"missing wrapper: {wrapper.relative_to(ROOT)}")
            continue
        if read(wrapper).strip() != WRAPPER_TARGET:
            errors.append(f"{wrapper.relative_to(ROOT)} must contain only {WRAPPER_TARGET}")

    agents_md = ROOT / "AGENTS.md"
    if not agents_md.is_file():
        errors.append("missing AGENTS.md")
    else:
        agents_content = read(agents_md)
        for token in (
            ".agents/skills/job-application-quality/SKILL.md",
            "Do not invent",
            "Validation Before Release",
        ):
            if token not in agents_content:
                errors.append(f"AGENTS.md: missing {token}")

    claude_md = ROOT / "CLAUDE.md"
    if not claude_md.is_file():
        errors.append("missing CLAUDE.md")
    elif read(claude_md).strip() != "@AGENTS.md":
        errors.append("CLAUDE.md must import AGENTS.md with @AGENTS.md")

    codex_skill = ROOT / "skills" / "job-application-quality-gate" / "SKILL.md"
    if not codex_skill.is_file():
        errors.append("missing Codex plugin skill")
    else:
        codex_content = read(codex_skill)
        errors += validate_frontmatter(codex_content, "Codex plugin skill")
        if ".agents/skills/job-application-quality/SKILL.md" not in codex_content:
            errors.append("Codex plugin skill must reference the canonical Open Agent Skill")

    return errors


def main() -> None:
    fail(validate())
    print("PASS multi-CLI support")


if __name__ == "__main__":
    main()
