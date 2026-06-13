#!/usr/bin/env python3
"""Provide lightweight developer context when the plugin starts."""

from __future__ import annotations

import json


CONTEXT = """Job Application Quality is local-first and human-in-the-loop.
Use AGENTS.md as project memory. Do not invent candidate facts. Use canonical tenant profiles, role intake files, policy gates, manifests, and artifact QA before upload, email, or submit. Stop before CAPTCHA, identity documents, legal attestations, email send, or final ATS submit unless the user gives explicit action-specific approval."""


def main() -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": CONTEXT,
        }
    }))


if __name__ == "__main__":
    main()
