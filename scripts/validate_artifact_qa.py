#!/usr/bin/env python3
"""Regression checks for deterministic artifact QA behavior."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from common import write_json
from qa_artifacts import qa


def base_manifest(root: Path, artifact_path: Path) -> dict:
    profile_path = root / "candidate.json"
    role_path = root / "role.json"
    write_json(
        profile_path,
        {
            "claims": [{"text": "Built production Python services.", "confidence": "verified"}],
            "forbidden_claims": ["Kubernetes expert"],
        },
    )
    write_json(role_path, {"required_skills": ["Python"]})
    return {
        "inputs": {
            "profile_path": str(profile_path),
            "role_path": str(role_path),
        },
        "outputs": [{"path": str(artifact_path)}],
    }


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def validate_artifact_content_scan() -> None:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        artifact_path = root / "cv.txt"
        artifact_path.write_text(
            "\n".join(
                [
                    "Built production Python services.",
                    "TODO [COMPANY_NAME] [ROLE_TITLE] [HIRING_MANAGER]",
                    "TBD lorem ipsum",
                    "Local draft path: /Users/example/private/cv.txt",
                    "Linux draft path: /home/example/private/cv.txt",
                    "Windows draft path: C:\\Users\\example\\private\\cv.txt",
                ]
            ),
            encoding="utf-8",
        )

        report = qa(base_manifest(root, artifact_path))
        errors = "\n".join(report["errors"])
        warnings = "\n".join(report["warnings"])

        require(report["status"] == "fail", "placeholder and path leak artifact should fail QA")
        for token in ("TODO", "[COMPANY_NAME]", "[ROLE_TITLE]", "[HIRING_MANAGER]", "TBD", "lorem ipsum"):
            require(token in errors, f"missing artifact placeholder detection for {token}")
        for marker in ("/Users/", "/home/", "Windows user path"):
            require(marker in warnings, f"missing artifact path leak detection for {marker}")


def validate_path_leak_only_warns() -> None:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        artifact_path = root / "cv.txt"
        artifact_path.write_text(
            "Built production Python services.\nLocal draft path: /Users/example/private/cv.txt\n",
            encoding="utf-8",
        )

        report = qa(base_manifest(root, artifact_path))

        require(report["status"] == "warn", "path-only artifact leak should warn instead of pass")
        require(not report["errors"], "path-only artifact leak should not create blocking errors")
        require(
            any("/Users/" in warning for warning in report["warnings"]),
            "missing path-only artifact leak warning",
        )


def validate_existing_missing_empty_and_claim_checks() -> None:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)

        missing_path = root / "missing.txt"
        missing_report = qa(base_manifest(root, missing_path))
        require(
            any("Missing artifact" in error for error in missing_report["errors"]),
            "missing artifact check regressed",
        )

        empty_path = root / "empty.txt"
        empty_path.write_text("", encoding="utf-8")
        empty_report = qa(base_manifest(root, empty_path))
        require(
            any("Empty artifact" in error for error in empty_report["errors"]),
            "empty artifact check regressed",
        )

        claim_path = root / "claim.txt"
        claim_path.write_text(
            "Built production Python services.\nKubernetes expert\n",
            encoding="utf-8",
        )
        claim_report = qa(base_manifest(root, claim_path))
        require(
            any("Unsupported claim" in error for error in claim_report["errors"]),
            "unsupported claim check regressed",
        )


def main() -> None:
    validate_artifact_content_scan()
    validate_path_leak_only_warns()
    validate_existing_missing_empty_and_claim_checks()
    print("PASS artifact QA regression checks")


if __name__ == "__main__":
    main()
