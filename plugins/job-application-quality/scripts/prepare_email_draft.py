#!/usr/bin/env python3
"""Prepare a recruiter email draft file. This script never sends email."""

from __future__ import annotations

import sys
from pathlib import Path

from common import load_json


def main() -> None:
    if len(sys.argv) != 5:
        raise SystemExit("Usage: prepare_email_draft.py <profile.json> <role-intake.json> <manifest.json> <output.md>")
    profile = load_json(sys.argv[1])
    role = load_json(sys.argv[2])
    manifest = load_json(sys.argv[3])
    output = Path(sys.argv[4])
    output.parent.mkdir(parents=True, exist_ok=True)
    body = f"""Subject: Application for {role['title']} at {role['company']}

Hi {role['company']} team,

I am interested in the {role['title']} role. I have attached the current application packet prepared from my verified profile and the role requirements.

Best,
{profile['candidate_name']}

---
Manifest: {manifest['role_id']}
Approval status: {manifest['approval']['status']}
"""
    output.write_text(body, encoding="utf-8")
    print(f"Draft written: {output}")


if __name__ == "__main__":
    main()

