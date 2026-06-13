---
name: job-application-quality
description: Multi-CLI job application quality router for validated packets, policy gates, artifact QA, email drafts, and submission logs.
arguments: mode
user-invocable: true
argument-hint: "[packet | validate | gates | qa | email | browser | log | release]"
license: MIT
---

# Job Application Quality -- Router

This is the canonical Open Agent Skill entrypoint for Job Application Quality.

Use it from any agent CLI that understands repository skills. CLI-specific wrappers should point here instead of duplicating instructions.

## Non-Negotiables

- Do not invent candidate experience, credentials, metrics, employers, dates, skills, publications, compensation, work authorization, location, sponsorship status, or availability.
- Use only canonical tenant facts, user-approved role facts, cited job posting facts, and approved baseline artifacts.
- Do not use chat memory as the source of truth when a tenant profile or artifact manifest exists.
- Do not send email, click final submit, solve a CAPTCHA, upload identity documents, or accept legal attestations without explicit action-specific approval.
- If the CV, cover letter, email, form answer, or packet is weak, generic, factually risky, or missing a manifest, block the submission and explain why.

## Mode Routing

Determine the mode from `$mode`:

| Input | Mode |
| --- | --- |
| empty / no args | `discovery` |
| role URL or role details with tenant profile | `packet` |
| `packet` | `packet` |
| `validate` | `validate` |
| `gates` | `gates` |
| `qa` | `qa` |
| `email` | `email` |
| `browser` | `browser` |
| `log` | `log` |
| `release` | `release` |

If `$mode` is not a known command but includes a tenant profile path and role intake path, treat it as `packet`.

## Discovery Mode

Show this menu:

```text
Job Application Quality

Available commands:
  job-application-quality packet    Prepare application packet manifest and QA checklist
  job-application-quality validate  Validate tenant profile and role intake files
  job-application-quality gates     Run sponsorship, remote, ATS, and safety gates
  job-application-quality qa        QA an existing artifact manifest
  job-application-quality email     Draft a recruiter email without sending it
  job-application-quality browser   Assist with ATS/browser submission, stopping before final submit
  job-application-quality log       Record an approved submission event
  job-application-quality release   Validate plugin, skill, examples, and multi-CLI wrappers
```

## Context Loading

Always start from repository root when paths are relative.

For all modes, read:

- `AGENTS.md`
- `docs/SUBMISSION_POLICY.md`
- `docs/QUALITY_GATES.md`

For artifact, browser, and email work, also read the relevant reference:

- `skills/job-application-quality-gate/references/artifact-qa.md`
- `skills/job-application-quality-gate/references/browser-workflow.md`
- `skills/job-application-quality-gate/references/email-workflow.md`
- `skills/job-application-quality-gate/references/policies.md`

## Mode Instructions

### `packet`

1. Load the tenant profile and role intake.
2. Run validation and policy gates.
3. Prepare an application packet manifest.
4. Run artifact QA.
5. Present the manifest path, QA result, warnings, and pre-submit checklist.
6. Stop before browser submit or email send.

Preferred commands:

```bash
python3 scripts/validate_tenant_profile.py <profile.json>
python3 scripts/validate_role_intake.py <role-intake.json>
python3 scripts/check_policy_gates.py <profile.json> <role-intake.json>
python3 scripts/prepare_application_packet.py <profile.json> <role-intake.json> <output-dir>
python3 scripts/qa_artifacts.py <output-dir>/manifest.json
```

### `validate`

Run the tenant and role validators. Report exact failures and do not continue to packet generation if either validator fails.

### `gates`

Run `scripts/check_policy_gates.py`. Treat any non-zero exit as a hard block.

### `qa`

Run `scripts/qa_artifacts.py <manifest.json>`. A `fail` status blocks use of the packet. A `warn` status requires explicit review before upload or send.

### `email`

Draft only. Use `scripts/prepare_email_draft.py` and stop with the draft path. Do not send through Gmail, browser, CLI, or API from this mode.

### `browser`

Assist with reading forms, selecting safe answers from tenant facts, and checking the final review screen. Stop before CAPTCHA, legal attestation, file upload of sensitive documents, or final submit unless the user gives explicit action-specific approval.

### `log`

After a user-approved send or submit, run `scripts/record_submission.py` with the exact destination and approval text.

### `release`

Run the full local validation set before any release:

```bash
python3 scripts/validate_tenant_profile.py examples/tenant/profile.valid.json
python3 scripts/validate_role_intake.py examples/role-intake.valid.json
python3 scripts/check_policy_gates.py examples/tenant/profile.valid.json examples/role-intake.valid.json
python3 scripts/validate_multi_cli_support.py
python3 scripts/validate_package_metadata.py
python3 /Users/nextwebb/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
python3 /Users/nextwebb/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/job-application-quality-gate
```

## Pre-Submit Checklist

Before upload, send, or final submit:

- Company, title, URL, and ATS are verified.
- Artifacts match the manifest.
- No unsupported candidate claims are present.
- Sponsorship, remote, and location gates pass.
- Sensitive fields are not required or have explicit user review.
- Current user approval names the destination and action.
