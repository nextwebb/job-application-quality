#!/usr/bin/env python3
"""Record a submission event after explicit user approval."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

from common import load_json, sha256_json, write_json


def main() -> None:
    if len(sys.argv) != 5:
        raise SystemExit("Usage: record_submission.py <manifest.json> <destination> <approval-text> <output-log.json>")
    manifest = load_json(sys.argv[1])
    approval_text = sys.argv[3]
    if len(approval_text.strip()) < 8:
        raise SystemExit("Approval text is too short")
    log = {
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "tenant_id": manifest["tenant_id"],
        "role_id": manifest["role_id"],
        "destination": sys.argv[2],
        "approval_text": approval_text,
        "manifest_sha256": sha256_json(manifest),
        "outputs": manifest.get("outputs", []),
    }
    write_json(Path(sys.argv[4]), log)
    print(f"Submission log written: {sys.argv[4]}")


if __name__ == "__main__":
    main()

