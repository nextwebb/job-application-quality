---
name: job-application-quality-gate
description: Codex compatibility wrapper for the canonical Job Application Quality Open Agent Skill.
license: MIT
---

# Job Application Quality Gate

This Codex plugin skill is a compatibility wrapper.

Before acting, read and follow the canonical Open Agent Skill:

```text
.agents/skills/job-application-quality/SKILL.md
```

Use this wrapper when Codex discovers plugin skills from `skills/`, but treat the `.agents` skill as the source of truth for mode routing, non-negotiables, context loading, preferred scripts, and pre-submit checks.

## Non-Negotiables

- Do not invent candidate experience, credentials, metrics, employers, dates, skills, publications, compensation, work authorization, location, sponsorship status, or availability.
- Use only canonical tenant facts, user-approved role facts, cited job posting facts, and approved baseline artifacts.
- Do not use chat memory as the source of truth when a tenant profile or artifact manifest exists.
- Do not send email, click final submit, solve a CAPTCHA, or accept legal attestations without explicit action-specific approval.
- If the CV/cover letter is weak, generic, factually risky, or missing a manifest, block the submission and report why.

## Standard Workflow

1. Load the tenant profile and role intake.
2. Validate both files with scripts.
3. Check sponsorship, remote, location, salary, credential, and false-attestation gates.
4. Select or prepare role-specific CV and cover letter artifacts from approved baselines.
5. Run artifact QA.
6. Write a manifest.
7. Present a pre-submit checklist.
8. Proceed to email/browser submission only after explicit approval.

## References

- Read `references/policies.md` when gate behavior or approval boundaries matter.
- Read `references/artifact-qa.md` before uploading or sending CVs, resumes, or cover letters.
- Read `references/browser-workflow.md` before browser-assisted application work.
- Read `references/email-workflow.md` before recruiter email work.

## Preferred Scripts

Use scripts rather than rewriting validators:

```bash
python3 scripts/validate_tenant_profile.py <profile.json>
python3 scripts/validate_role_intake.py <role-intake.json>
python3 scripts/check_policy_gates.py <profile.json> <role-intake.json>
python3 scripts/prepare_application_packet.py <profile.json> <role-intake.json> <output-dir>
python3 scripts/qa_artifacts.py <manifest.json>
python3 scripts/prepare_email_draft.py <profile.json> <role-intake.json> <manifest.json> <output.md>
python3 scripts/record_submission.py <manifest.json> <destination> <approval-text> <output-log.json>
```

## Pre-Submit Checklist

Before upload/send/submit:

- Company, title, URL, and ATS are verified.
- Artifacts match the manifest.
- No unsupported candidate claims are present.
- Sponsorship, remote, and location gates pass.
- Sensitive fields are not required or have explicit user review.
- Current user approval names the destination and action.
