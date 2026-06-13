# Documentation Rules

Documentation should make the workflow safer and easier to verify.

## Style

- Start with what the user can do and why it matters.
- Be direct about safety limits.
- Prefer short examples over abstract prose.
- Show commands that can be copied into a terminal.
- Keep generated examples synthetic.
- Do not imply that the tool guarantees interviews, offers, visas, or recruiter replies.
- Do not imply applications can be submitted without review.

## Required Docs For User-Visible Features

When changing behavior, update the relevant docs:

- `README.md` for public positioning and quick start.
- `CHANGELOG.md` for release-visible changes.
- `docs/INSTALL.md` for install/package changes.
- `docs/MULTI_CLI.md` for CLI routing changes.
- `docs/QUALITY_GATES.md` for policy gates.
- `docs/SUBMISSION_POLICY.md` for send/submit behavior.
- `DATA_CONTRACT.md` for user-owned vs system-owned file changes.

## Governance Docs

Community and legal docs should stay aligned:

- `CODE_OF_CONDUCT.md`
- `CONTRIBUTING.md`
- `GOVERNANCE.md`
- `SECURITY.md`
- `SUPPORT.md`
- `TRADEMARK.md`
- `LEGAL_DISCLAIMER.md`
