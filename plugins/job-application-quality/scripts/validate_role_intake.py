#!/usr/bin/env python3
"""Validate role intake structure."""

from __future__ import annotations

import sys
from pathlib import Path

from common import fail, load_json, require_keys


ALLOWED_ATS = {"ashby", "greenhouse", "lever", "workday", "other"}
SPONSORSHIP = {"available", "unavailable", "unknown", "not_required"}
REMOTE = {"global", "regional", "onsite", "hybrid", "unknown"}


def validate(role: dict) -> list[str]:
    errors: list[str] = []
    errors += require_keys(
        role,
        ["role_id", "company", "title", "job_url", "ats", "location", "remote", "sponsorship", "required_skills"],
        "role",
    )
    if role.get("ats") not in ALLOWED_ATS:
        errors.append(f"role.ats: unsupported value '{role.get('ats')}'")
    remote = role.get("remote", {})
    if not isinstance(remote, dict) or remote.get("status") not in REMOTE:
        errors.append("role.remote.status: missing or unsupported")
    sponsorship = role.get("sponsorship", {})
    if not isinstance(sponsorship, dict) or sponsorship.get("status") not in SPONSORSHIP:
        errors.append("role.sponsorship.status: missing or unsupported")
    if not isinstance(role.get("required_skills"), list):
        errors.append("role.required_skills: must be an array")
    return errors


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: validate_role_intake.py <role-intake.json>")
    path = Path(sys.argv[1])
    role = load_json(path)
    fail(validate(role))
    print(f"PASS role intake: {path}")


if __name__ == "__main__":
    main()

