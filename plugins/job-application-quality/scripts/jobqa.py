#!/usr/bin/env python3
"""Simple CLI front door for Job Application Quality."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any

from check_policy_gates import check
from common import load_json, write_json
from prepare_application_packet import prepare
from qa_artifacts import qa
from run_claim_demo import main as run_demo
from validate_role_intake import validate as validate_role
from validate_tenant_profile import validate as validate_profile


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIRNAME = "output"


def status_icon(status: str) -> str:
    if status == "pass":
        return "✅"
    if status == "warn":
        return "⚠️"
    return "⛔"


def default_profile() -> dict[str, Any]:
    return {
        "tenant_id": "my_candidate",
        "candidate_name": "Your Name",
        "canonical_facts_version": "v1",
        "contact": {
            "email": "you@example.com",
            "current_location": "City, Country",
            "linkedin": "https://www.linkedin.com/in/your-profile",
            "github": "https://github.com/your-handle",
        },
        "work_authorization": {
            "current_country": "authorized",
            "requires_sponsorship_for_eu_uk_us": True,
            "global_remote_contractor": True,
        },
        "application_policy": {
            "allowed_ats": ["ashby", "greenhouse", "lever"],
            "skip_if_sponsorship_unavailable": True,
            "skip_if_sponsorship_unknown_for_relocation": True,
            "skip_if_remote_country_unverified": True,
            "requires_explicit_submit_approval": True,
        },
        "baseline_artifacts": [
            {
                "artifact_id": "base_cv",
                "type": "cv",
                "path": "artifacts/cv.txt",
                "role_family": "backend",
            }
        ],
        "claims": [
            {
                "claim_id": "python_services",
                "text": "Built production Python services.",
                "confidence": "verified",
                "allowed_contexts": ["backend", "platform"],
            },
            {
                "claim_id": "aws_lambda",
                "text": "Built serverless APIs on AWS Lambda.",
                "confidence": "verified",
                "allowed_contexts": ["backend", "aws"],
            },
        ],
        "forbidden_claims": [
            "Kubernetes expert",
            "US citizen",
            "PhD",
        ],
    }


def default_role() -> dict[str, Any]:
    return {
        "role_id": "sample-backend-role",
        "company": "Example Company",
        "title": "Backend Engineer",
        "job_url": "https://jobs.ashbyhq.com/example/sample",
        "ats": "ashby",
        "source_timestamp": "2026-06-13T00:00:00Z",
        "location": "Remote",
        "remote": {
            "status": "global",
            "allowed_regions": ["global"],
        },
        "sponsorship": {
            "status": "not_required",
            "evidence": "Global remote contractor setup supported.",
        },
        "required_skills": ["Python", "AWS"],
        "preferred_skills": ["PostgreSQL"],
        "required_questions": [],
    }


def default_cv() -> str:
    return """Your Name
Backend Engineer

Summary
Built production Python services and serverless APIs on AWS Lambda.

Selected Experience
- Built production Python services.
- Built serverless APIs on AWS Lambda.
"""


def init_command(args: argparse.Namespace) -> int:
    target = Path(args.directory).expanduser()
    if target.exists() and any(target.iterdir()) and not args.force:
        raise SystemExit(f"{target} already exists and is not empty. Use --force to overwrite sample files.")

    (target / "artifacts").mkdir(parents=True, exist_ok=True)
    (target / DEFAULT_OUTPUT_DIRNAME).mkdir(parents=True, exist_ok=True)
    write_json(target / "candidate.json", default_profile())
    write_json(target / "role.json", default_role())
    (target / "artifacts" / "cv.txt").write_text(default_cv(), encoding="utf-8")
    print(f"Initialized jobqa workspace: {target}")
    print("Next: jobqa run " + str(target))
    return 0


def paths_for_workspace(workspace: Path) -> tuple[Path, Path, Path]:
    return (
        workspace / "candidate.json",
        workspace / "role.json",
        workspace / DEFAULT_OUTPUT_DIRNAME,
    )


def validate_inputs(profile_path: Path, role_path: Path) -> tuple[dict, dict]:
    profile = load_json(profile_path)
    role = load_json(role_path)
    errors = validate_profile(profile) + validate_role(role)
    if errors:
        raise SystemExit("\n".join(errors))
    return profile, role


def write_report(output_dir: Path, report: dict) -> None:
    write_json(output_dir / "qa-report.json", report)


def format_text(manifest: dict, report: dict) -> str:
    lines = [
        f"STATUS: {report['status'].upper()} {status_icon(report['status'])}",
        "",
        f"Role: {manifest.get('title')} at {manifest.get('company')}",
        f"Manifest: {Path(manifest.get('outputs', [{}])[0].get('path', '.')).parent / 'manifest.json'}",
    ]

    errors = report.get("errors", [])
    warnings = report.get("warnings", [])
    checks = report.get("claim_checks", {})

    if errors:
        lines.extend(["", "Blocking issues:"])
        lines.extend(f"- {error}" for error in errors)
    if warnings:
        lines.extend(["", "Warnings:"])
        lines.extend(f"- {warning}" for warning in warnings)
    if checks.get("matches"):
        lines.extend(["", "Matches:"])
        lines.extend(f"- {match}" for match in checks["matches"])

    lines.extend(["", "Next:"])
    if report["status"] == "fail":
        lines.append("- fix blocking issues before submission")
    elif report["status"] == "warn":
        lines.append("- review warnings before submission")
    else:
        lines.append("- review packet and approve manually before submission")
    return "\n".join(lines)


def format_markdown(manifest: dict, report: dict) -> str:
    lines = [
        f"# JobQA Report: {report['status'].upper()}",
        "",
        f"- **Role:** {manifest.get('title')} at {manifest.get('company')}",
        f"- **Job URL:** {manifest.get('job_url')}",
        f"- **Approval:** {manifest.get('approval', {}).get('status', 'unknown')}",
        "",
    ]
    sections = [
        ("Blocking Issues", report.get("errors", [])),
        ("Warnings", report.get("warnings", [])),
        ("Matches", report.get("claim_checks", {}).get("matches", [])),
    ]
    for title, items in sections:
        lines.append(f"## {title}")
        if items:
            lines.extend(f"- {item}" for item in items)
        else:
            lines.append("- None")
        lines.append("")
    lines.append("## Decision")
    if report["status"] == "fail":
        lines.append("- Stop before submission.")
    elif report["status"] == "warn":
        lines.append("- Review warnings before submission.")
    else:
        lines.append("- Packet passed QA; human approval is still required before submission.")
    return "\n".join(lines)


def print_report(manifest: dict, report: dict, output_format: str) -> None:
    if output_format == "json":
        print(json.dumps({"manifest": manifest, "qa_report": report}, indent=2, sort_keys=True))
    elif output_format == "markdown":
        print(format_markdown(manifest, report))
    else:
        print(format_text(manifest, report))


def run_workspace(workspace: Path, output_format: str) -> tuple[dict, dict]:
    profile_path, role_path, output_dir = paths_for_workspace(workspace)
    validate_inputs(profile_path, role_path)
    manifest = prepare(profile_path, role_path, output_dir)
    report = qa(manifest)
    write_report(output_dir, report)
    print_report(manifest, report, output_format)
    return manifest, report


def run_command(args: argparse.Namespace) -> int:
    _, report = run_workspace(Path(args.directory).expanduser(), args.format)
    return 1 if report["status"] == "fail" else 0


def qa_command(args: argparse.Namespace) -> int:
    manifest_path = Path(args.manifest).expanduser()
    manifest = load_json(manifest_path)
    report = qa(manifest)
    write_report(manifest_path.parent, report)
    print_report(manifest, report, args.format)
    return 1 if report["status"] == "fail" else 0


def report_command(args: argparse.Namespace) -> int:
    manifest_path = Path(args.manifest).expanduser()
    manifest = load_json(manifest_path)
    report_path = manifest_path.parent / "qa-report.json"
    report = load_json(report_path) if report_path.exists() else qa(manifest)
    print_report(manifest, report, args.format)
    return 0


def demo_command(args: argparse.Namespace) -> int:
    run_demo()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jobqa",
        description="Preflight checks for AI-generated job applications.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    demo = subparsers.add_parser("demo", help="Run the unsupported-claim demo")
    demo.set_defaults(func=demo_command)

    init = subparsers.add_parser("init", help="Create a simple jobqa workspace")
    init.add_argument("directory", help="Workspace directory to create")
    init.add_argument("--force", action="store_true", help="Overwrite sample files in an existing directory")
    init.set_defaults(func=init_command)

    run = subparsers.add_parser("run", help="Prepare, QA, and report on a workspace")
    run.add_argument("directory", help="Directory containing candidate.json, role.json, and artifacts/")
    run.add_argument("--format", choices=["text", "markdown", "json"], default="text")
    run.set_defaults(func=run_command)

    qa_parser = subparsers.add_parser("qa", help="Run QA for an existing manifest")
    qa_parser.add_argument("manifest", help="Path to manifest.json")
    qa_parser.add_argument("--format", choices=["text", "markdown", "json"], default="text")
    qa_parser.set_defaults(func=qa_command)

    report = subparsers.add_parser("report", help="Print a report for an existing manifest")
    report.add_argument("manifest", help="Path to manifest.json")
    report.add_argument("--format", choices=["text", "markdown", "json"], default="markdown")
    report.set_defaults(func=report_command)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
