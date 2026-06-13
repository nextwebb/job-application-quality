#!/usr/bin/env python3
"""Prepare an application packet manifest from tenant and role inputs."""

from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from check_policy_gates import check
from common import load_json, sha256_file, sha256_json, write_json


def choose_artifacts(profile: dict, role: dict) -> list[dict]:
    role_text = " ".join([role.get("title", ""), " ".join(role.get("required_skills", []))]).lower()
    artifacts = profile.get("baseline_artifacts", [])
    selected = []
    for artifact in artifacts:
        family = artifact.get("role_family", "").lower()
        if family and family in role_text:
            selected.append(artifact)
    if not selected:
        selected = [a for a in artifacts if a.get("type") in {"cv", "resume"}][:1]
    return selected


def prepare(profile_path: Path, role_path: Path, output_dir: Path) -> dict:
    profile = load_json(profile_path)
    role = load_json(role_path)
    gate_result = check(profile, role)
    if gate_result["status"] != "pass":
        raise SystemExit("Policy gates failed; packet not prepared")

    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = []
    for artifact in choose_artifacts(profile, role):
        source = Path(artifact["path"])
        if not source.is_absolute():
            source = profile_path.parent / source
        if not source.exists():
            continue
        dest = output_dir / source.name
        shutil.copy2(source, dest)
        outputs.append({
            "type": artifact["type"],
            "path": str(dest),
            "sha256": sha256_file(dest),
            "qa_status": "pending",
        })

    manifest = {
        "tenant_id": profile["tenant_id"],
        "role_id": role["role_id"],
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "profile_path": str(profile_path),
            "profile_sha256": sha256_json(profile),
            "role_path": str(role_path),
            "role_sha256": sha256_json(role),
        },
        "company": role["company"],
        "title": role["title"],
        "job_url": role["job_url"],
        "outputs": outputs,
        "policy_gates": gate_result,
        "approval": {"required": True, "status": "pending"},
    }
    write_json(output_dir / "manifest.json", manifest)
    return manifest


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("Usage: prepare_application_packet.py <profile.json> <role-intake.json> <output-dir>")
    manifest = prepare(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
    print(f"Packet ready: {Path(sys.argv[3]) / 'manifest.json'}")
    print(f"Outputs: {len(manifest['outputs'])}")


if __name__ == "__main__":
    main()

