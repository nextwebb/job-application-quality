#!/usr/bin/env python3
"""Validate a tenant profile using dependency-free structural checks."""

from __future__ import annotations

import sys
from pathlib import Path

from common import fail, load_json, require_keys


def validate(profile: dict) -> list[str]:
    errors: list[str] = []
    errors += require_keys(
        profile,
        ["tenant_id", "candidate_name", "canonical_facts_version", "contact", "work_authorization", "application_policy", "claims"],
        "profile",
    )
    contact = profile.get("contact", {})
    if isinstance(contact, dict):
        errors += require_keys(contact, ["email", "current_location"], "contact")
    else:
        errors.append("contact: must be an object")
    claims = profile.get("claims", [])
    if not isinstance(claims, list):
        errors.append("claims: must be an array")
    else:
        seen: set[str] = set()
        for idx, claim in enumerate(claims):
            if not isinstance(claim, dict):
                errors.append(f"claims[{idx}]: must be an object")
                continue
            errors += require_keys(claim, ["claim_id", "text", "confidence"], f"claims[{idx}]")
            claim_id = claim.get("claim_id")
            if claim_id in seen:
                errors.append(f"claims[{idx}]: duplicate claim_id '{claim_id}'")
            seen.add(claim_id)
            if claim.get("confidence") == "blocked":
                errors.append(f"claims[{idx}]: blocked claim must not be reusable")
    return errors


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: validate_tenant_profile.py <profile.json>")
    path = Path(sys.argv[1])
    profile = load_json(path)
    fail(validate(profile))
    print(f"PASS tenant profile: {path}")


if __name__ == "__main__":
    main()

