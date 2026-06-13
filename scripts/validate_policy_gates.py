#!/usr/bin/env python3
"""Run policy gate regression checks."""

from __future__ import annotations

import copy
from pathlib import Path

from check_policy_gates import check
from common import load_json


ROOT = Path(__file__).resolve().parent.parent
PROFILE = ROOT / "examples" / "tenant" / "profile.valid.json"
ROLE = ROOT / "examples" / "role-intake.valid.json"
EU_ONLY_ROLE = ROOT / "examples" / "role-intake.remote-eu-only.json"
WORLDWIDE_ROLE = ROOT / "examples" / "role-intake.remote-worldwide.json"


def expect_pass(label: str, profile: dict, role: dict) -> None:
    result = check(profile, role)
    if result["status"] != "pass":
        raise SystemExit(f"{label}: expected pass, got {result}")


def expect_fail(label: str, profile: dict, role: dict) -> None:
    result = check(profile, role)
    if result["status"] != "fail":
        raise SystemExit(f"{label}: expected fail, got {result}")


def role_with_regions(base_role: dict, regions: list[str]) -> dict:
    role = copy.deepcopy(base_role)
    role["remote"]["status"] = "regional"
    role["remote"]["allowed_regions"] = regions
    return role


def profile_with_location(base_profile: dict, location: str) -> dict:
    profile = copy.deepcopy(base_profile)
    profile["contact"]["current_location"] = location
    return profile


def main() -> None:
    profile = load_json(PROFILE)
    role = load_json(ROLE)

    expect_pass("Lagos profile matches EMEA acronym", profile, role)
    expect_pass(
        "Lagos profile matches spelled-out EMEA",
        profile,
        role_with_regions(role, ["Europe, Middle East and Africa"]),
    )
    expect_pass("Lagos profile matches worldwide remote", profile, load_json(WORLDWIDE_ROLE))
    expect_fail("Lagos profile fails EU-only remote", profile, load_json(EU_ONLY_ROLE))

    canada_profile = profile_with_location(profile, "Toronto, Canada")
    expect_pass(
        "Canada profile matches explicit Canada region",
        canada_profile,
        role_with_regions(role, ["Canada"]),
    )
    expect_fail(
        "Canada profile fails EU-only remote",
        canada_profile,
        role_with_regions(role, ["EU"]),
    )

    south_africa_profile = profile_with_location(profile, "Cape Town, South Africa")
    expect_pass(
        "South Africa profile matches EMEA regional remote",
        south_africa_profile,
        role_with_regions(role, ["EMEA"]),
    )

    united_states_profile = profile_with_location(profile, "Austin, United States")
    expect_pass(
        "United States profile matches US-only remote",
        united_states_profile,
        role_with_regions(role, ["US only"]),
    )

    united_kingdom_profile = profile_with_location(profile, "London, United Kingdom")
    expect_pass(
        "United Kingdom profile matches UK-only remote",
        united_kingdom_profile,
        role_with_regions(role, ["UK only"]),
    )


if __name__ == "__main__":
    main()
