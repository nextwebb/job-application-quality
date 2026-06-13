#!/usr/bin/env python3
"""Run conservative QA checks over an application packet manifest."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from common import load_json, write_json


PLACEHOLDERS = ["TODO", "TBD", "[company]", "[role]", "lorem ipsum"]
PRIVATE_PATH_MARKERS = ["/Users/", "\\Users\\", "/home/"]


def qa(manifest: dict) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
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

    text_blob = json.dumps(manifest)
    for token in PLACEHOLDERS:
        if token.lower() in text_blob.lower():
            errors.append(f"Placeholder found: {token}")

    status = "fail" if errors else ("warn" if warnings else "pass")
    return {"status": status, "errors": errors, "warnings": warnings}


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

