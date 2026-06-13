#!/usr/bin/env python3
"""Check role policy gates against tenant profile."""

from __future__ import annotations

import json
import re
import sys

from common import load_json
from validate_role_intake import validate as validate_role
from validate_tenant_profile import validate as validate_profile


GLOBAL_REMOTE_REGIONS = {"global", "worldwide", "world", "anywhere"}

REGION_ALIASES = {
    "anywhere": "global",
    "emea": "emea",
    "eu": "eu",
    "eu only": "eu",
    "europe middle east africa": "emea",
    "europe middle east and africa": "emea",
    "european union": "eu",
    "global": "global",
    "remote worldwide": "worldwide",
    "uk": "uk",
    "united kingdom": "uk",
    "us": "us",
    "usa": "us",
    "united states": "us",
    "world": "worldwide",
    "worldwide": "worldwide",
}

LOCATION_NON_COUNTRIES = {
    "anywhere",
    "global",
    "hybrid",
    "onsite",
    "remote",
    "world",
    "worldwide",
}

EU_COUNTRIES = (
    "austria",
    "belgium",
    "bulgaria",
    "croatia",
    "cyprus",
    "czechia",
    "denmark",
    "estonia",
    "finland",
    "france",
    "germany",
    "greece",
    "hungary",
    "ireland",
    "italy",
    "latvia",
    "lithuania",
    "luxembourg",
    "malta",
    "netherlands",
    "poland",
    "portugal",
    "romania",
    "slovakia",
    "slovenia",
    "spain",
    "sweden",
)

AFRICA_COUNTRIES = (
    "algeria",
    "angola",
    "benin",
    "botswana",
    "burkina faso",
    "burundi",
    "cameroon",
    "cape verde",
    "central african republic",
    "chad",
    "comoros",
    "democratic republic of the congo",
    "djibouti",
    "egypt",
    "equatorial guinea",
    "eritrea",
    "eswatini",
    "ethiopia",
    "gabon",
    "gambia",
    "ghana",
    "guinea",
    "guinea bissau",
    "ivory coast",
    "kenya",
    "lesotho",
    "liberia",
    "libya",
    "madagascar",
    "malawi",
    "mali",
    "mauritania",
    "mauritius",
    "morocco",
    "mozambique",
    "namibia",
    "niger",
    "nigeria",
    "republic of the congo",
    "rwanda",
    "sao tome and principe",
    "senegal",
    "seychelles",
    "sierra leone",
    "somalia",
    "south africa",
    "south sudan",
    "sudan",
    "tanzania",
    "togo",
    "tunisia",
    "uganda",
    "zambia",
    "zimbabwe",
)

MIDDLE_EAST_COUNTRIES = (
    "bahrain",
    "iran",
    "iraq",
    "israel",
    "jordan",
    "kuwait",
    "lebanon",
    "oman",
    "palestine",
    "qatar",
    "saudi arabia",
    "syria",
    "turkey",
    "united arab emirates",
    "yemen",
)

NON_EU_EUROPE_COUNTRIES = (
    "albania",
    "andorra",
    "armenia",
    "azerbaijan",
    "belarus",
    "bosnia and herzegovina",
    "georgia",
    "iceland",
    "kosovo",
    "liechtenstein",
    "moldova",
    "monaco",
    "montenegro",
    "north macedonia",
    "norway",
    "russia",
    "san marino",
    "serbia",
    "switzerland",
    "ukraine",
    "vatican city",
)

COUNTRY_REGIONS = {country: {"eu", "europe", "emea"} for country in EU_COUNTRIES}
COUNTRY_REGIONS.update(
    {
        "united kingdom": {"uk", "europe", "emea"},
        "united states": {"us", "north america", "americas"},
    }
)
COUNTRY_REGIONS.update({country: {"africa", "emea"} for country in AFRICA_COUNTRIES})
COUNTRY_REGIONS.update({country: {"middle east", "emea"} for country in MIDDLE_EAST_COUNTRIES})
COUNTRY_REGIONS.update({country: {"europe", "emea"} for country in NON_EU_EUROPE_COUNTRIES})

COUNTRY_ALIASES = {country: country for country in COUNTRY_REGIONS}
COUNTRY_ALIASES.update(
    {
        "czech republic": "czechia",
        "gb": "united kingdom",
        "great britain": "united kingdom",
        "holland": "netherlands",
        "republic of congo": "republic of the congo",
        "ng": "nigeria",
        "republic of ireland": "ireland",
        "the netherlands": "netherlands",
        "u k": "united kingdom",
        "u s": "united states",
        "u s a": "united states",
        "uae": "united arab emirates",
        "uk": "united kingdom",
        "united states of america": "united states",
        "usa": "united states",
    }
)


def normalize_label(value: object) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", str(value).lower())).strip()


def normalize_region(value: object) -> str:
    label = normalize_label(value)
    if label.endswith(" only"):
        base_label = label.removesuffix(" only").strip()
        if base_label in REGION_ALIASES:
            return REGION_ALIASES[base_label]
    return REGION_ALIASES.get(label, label)


def candidate_country(profile: dict) -> str | None:
    location = profile.get("contact", {}).get("current_location")
    if not isinstance(location, str):
        return None

    labels = [normalize_label(part) for part in reversed(location.split(",")) if normalize_label(part)]
    labels.append(normalize_label(location))
    for label in labels:
        if label in COUNTRY_ALIASES:
            return COUNTRY_ALIASES[label]

    full_location = f" {normalize_label(location)} "
    for alias, country in sorted(COUNTRY_ALIASES.items(), key=lambda item: len(item[0]), reverse=True):
        if f" {alias} " in full_location:
            return country

    if labels and len(labels) > 1 and labels[0] not in LOCATION_NON_COUNTRIES:
        return labels[0]
    return None


def candidate_regions_for(country: str) -> set[str]:
    return COUNTRY_REGIONS.get(country, set()) | {country}


def add_remote_region_result(message: str, strict: bool, errors: list[str], warnings: list[str]) -> None:
    if strict:
        errors.append(message)
    else:
        warnings.append(message)


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
    strict_remote_country = bool(policy.get("skip_if_remote_country_unverified"))
    if strict_remote_country and remote.get("status") == "unknown":
        errors.append("Remote eligibility is unknown")
    if remote.get("status") == "regional":
        raw_regions = [str(r) for r in remote.get("allowed_regions", []) if str(r).strip()]
        regions = {normalize_region(r) for r in raw_regions}
        if not regions:
            errors.append("Regional remote role has no allowed regions")
        elif not (regions & GLOBAL_REMOTE_REGIONS):
            country = candidate_country(profile)
            if not country:
                add_remote_region_result(
                    "Remote eligibility cannot be verified because tenant country is unknown",
                    strict_remote_country,
                    errors,
                    warnings,
                )
            else:
                candidate_regions = candidate_regions_for(country)
                if not (regions & candidate_regions):
                    add_remote_region_result(
                        "Remote eligibility mismatch: "
                        f"tenant country '{country}' is not included in allowed regions {raw_regions}",
                        strict_remote_country,
                        errors,
                        warnings,
                    )

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
