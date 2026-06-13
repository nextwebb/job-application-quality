#!/usr/bin/env python3
"""Check role policy gates against tenant profile."""

from __future__ import annotations

import json
import sys

from common import load_json
from validate_role_intake import validate as validate_role
from validate_tenant_profile import validate as validate_profile


def check(profile: dict, role: dict) -> dict:
    errors = validate_profile(profile) + validate_role(role)
    warnings: list[str] = []
    policy = profile.get("application_policy", {})
    work_auth = profile.get("work_authorization", {})

    allowed_ats = set(policy.get("allowed_ats", []))
    if allowed_ats and role.get("ats") not in allowed_ats:
        errors.append(f"ATS '{role.get('ats')}' is not allowed by tenant policy")

    sponsorship_status = role.get("sponsorship", {}).get("status")
    if policy.get("skip_if_sponsorship_unavailable") and sponsorship_status == "unavailable":
        errors.append("Sponsorship is unavailable")
    if (
        policy.get("skip_if_sponsorship_unknown_for_relocation")
        and sponsorship_status == "unknown"
        and work_auth.get("requires_sponsorship_for_eu_uk_us")
    ):
        errors.append("Sponsorship is unknown for a role that may require work authorization support")

    remote = role.get("remote", {})
    if policy.get("skip_if_remote_country_unverified") and remote.get("status") == "unknown":
        errors.append("Remote eligibility is unknown")
    if remote.get("status") == "regional":
        regions = {r.lower() for r in remote.get("allowed_regions", [])}
        if not regions:
            errors.append("Regional remote role has no allowed regions")
        elif "global" not in regions and not any(r in regions for r in ["emea", "eu", "uk", "africa", "worldwide"]):
            warnings.append("Regional remote role may not include tenant location")

    result = {
        "status": "fail" if errors else "pass",
        "errors": errors,
        "warnings": warnings,
        "gates": {
            "ats": "pass" if not any("ATS" in e for e in errors) else "fail",
            "sponsorship": "pass" if not any("Sponsorship" in e for e in errors) else "fail",
            "remote": "pass" if not any("Remote" in e or "Regional" in e for e in errors) else "fail",
        },
    }
    return result


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: check_policy_gates.py <profile.json> <role-intake.json>")
    result = check(load_json(sys.argv[1]), load_json(sys.argv[2]))
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

