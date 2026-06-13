#!/usr/bin/env python3
"""Run the unsupported-claim demo and print a human-readable result."""

from __future__ import annotations

import shutil
from pathlib import Path

from common import load_json, write_json
from prepare_application_packet import prepare
from qa_artifacts import qa


ROOT = Path(__file__).resolve().parent.parent
PROFILE = ROOT / "examples" / "claim-demo" / "profile.json"
ROLE = ROOT / "examples" / "claim-demo" / "role-intake.json"
OUTPUT = Path("/tmp/job-application-quality-claim-demo")


def main() -> None:
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    manifest = prepare(PROFILE, ROLE, OUTPUT)
    report = qa(manifest)
    write_json(OUTPUT / "qa-report.json", report)

    role = load_json(ROLE)
    artifact_text = (OUTPUT / "generated-cv.txt").read_text(encoding="utf-8")
    bad_claim = "Built Kubernetes production clusters"

    print("Candidate says:")
    print("- AWS Lambda")
    print("- Python")
    print("- no Kubernetes experience")
    print()
    print("Job requires:")
    for skill in role["required_skills"]:
        print(f"- {skill}")
    print()
    print("AI-generated CV says:")
    for line in artifact_text.splitlines():
        if bad_claim in line:
            print(f'- "{line}"')
    print()
    print("QA result:")
    for claim in report["claim_checks"]["unsupported_claims"]:
        print(f'- ❌ unsupported claim: "{claim}"')
    for skill in report["claim_checks"]["missing_evidence"]:
        print(f"- ⚠️ missing {skill} evidence")
    for skill in report["claim_checks"]["matches"]:
        print(f"- ✅ {skill} match")
    if report["status"] == "fail":
        print("- ⛔ stop before submission")
    print()
    print(f"Manifest: {OUTPUT / 'manifest.json'}")
    print(f"QA report: {OUTPUT / 'qa-report.json'}")


if __name__ == "__main__":
    main()
