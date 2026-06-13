#!/usr/bin/env python3
"""Run conservative QA checks over an application packet manifest."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from common import load_json, write_json


PLACEHOLDERS = ["TODO", "TBD", "[company]", "[role]", "lorem ipsum"]
PRIVATE_PATH_MARKERS = ["/Users/", "\\Users\\", "/home/"]


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9+#.]+", " ", value.lower()).strip()


def read_text_artifact(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def resolve_input_path(manifest: dict, key: str) -> Path | None:
    raw_path = manifest.get("inputs", {}).get(key)
    if not raw_path:
        return None
    path = Path(raw_path)
    if path.exists():
        return path
    return None


def extract_claim_line(text: str, needle: str) -> str:
    normalized_needle = normalize(needle)
    for raw_line in re.split(r"[\n\r]+", text):
        line = raw_line.strip(" -\t")
        if normalized_needle and normalized_needle in normalize(line):
            return line
    return needle


def truth_checks(manifest: dict, artifact_texts: list[str]) -> dict:
    profile_path = resolve_input_path(manifest, "profile_path")
    role_path = resolve_input_path(manifest, "role_path")
    if profile_path is None or role_path is None:
        return {
            "unsupported_claims": [],
            "missing_evidence": [],
            "matches": [],
            "warnings": ["Profile or role input path unavailable; skipped truth/evidence checks"],
        }

    profile = load_json(profile_path)
    role = load_json(role_path)
    supported_claims = [
        claim.get("text", "")
        for claim in profile.get("claims", [])
        if claim.get("confidence") != "blocked"
    ]
    supported_text = normalize(" ".join(supported_claims))
    artifact_text = "\n".join(artifact_texts)
    artifact_normalized = normalize(artifact_text)

    unsupported: list[str] = []
    unsupported_terms: set[str] = set()
    forbidden_claims = list(profile.get("forbidden_claims", []))
    forbidden_claims.extend(
        claim.get("text", "")
        for claim in profile.get("claims", [])
        if claim.get("confidence") == "blocked"
    )
    for forbidden in forbidden_claims:
        normalized_forbidden = normalize(forbidden)
        if normalized_forbidden and normalized_forbidden in artifact_normalized:
            line = extract_claim_line(artifact_text, forbidden)
            if line not in unsupported:
                unsupported.append(line)
            unsupported_terms.add(normalized_forbidden)

    missing: list[str] = []
    matches: list[str] = []
    for skill in role.get("required_skills", []):
        normalized_skill = normalize(skill)
        if not normalized_skill:
            continue
        if normalized_skill in supported_text:
            matches.append(skill)
            continue
        if normalized_skill in artifact_normalized and any(
            normalized_skill in term or term in normalized_skill for term in unsupported_terms
        ):
            continue
        missing.append(skill)

    return {
        "unsupported_claims": unsupported,
        "missing_evidence": missing,
        "matches": matches,
        "warnings": [],
    }


def qa(manifest: dict) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    artifact_texts: list[str] = []
    outputs = manifest.get("outputs", [])
    if not outputs:
        errors.append("No output artifacts in manifest")

    for item in outputs:
        path = Path(item["path"])
        if not path.exists():
            errors.append(f"Missing artifact: {path}")
            continue
        if path.stat().st_size == 0:
            errors.append(f"Empty artifact: {path}")
        if any(marker in str(path) for marker in PRIVATE_PATH_MARKERS):
            warnings.append(f"Manifest contains absolute local path: {path}")
        text = read_text_artifact(path)
        if text:
            artifact_texts.append(text)

    text_blob = json.dumps(manifest)
    for token in PLACEHOLDERS:
        if token.lower() in text_blob.lower():
            errors.append(f"Placeholder found: {token}")

    claim_report = truth_checks(manifest, artifact_texts)
    for claim in claim_report["unsupported_claims"]:
        errors.append(f"Unsupported claim: {claim}")
    for skill in claim_report["missing_evidence"]:
        warnings.append(f"Missing evidence for required skill: {skill}")
    warnings.extend(claim_report["warnings"])

    status = "fail" if errors else ("warn" if warnings else "pass")
    return {
        "status": status,
        "errors": errors,
        "warnings": warnings,
        "claim_checks": claim_report,
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: qa_artifacts.py <manifest.json>")
    manifest_path = Path(sys.argv[1])
    manifest = load_json(manifest_path)
    report = qa(manifest)
    write_json(manifest_path.parent / "qa-report.json", report)
    print(json.dumps(report, indent=2, sort_keys=True))
    if report["status"] == "fail":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
