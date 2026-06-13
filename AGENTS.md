# Job Application Quality -- Agent Instructions

These instructions are canonical for all coding-agent CLIs working in this repository.

## Product Scope

This repository provides a reusable, local-first quality gate for job application packets.

It may:

- validate tenant profiles and role intake files
- check sponsorship, remote, ATS, and safety policy gates
- prepare application packet manifests
- QA generated artifacts
- draft recruiter emails without sending them
- assist browser-based form review while stopping before final submit
- record approved submission logs

It must not:

- Do not invent candidate facts, claims, credentials, dates, metrics, compensation, work authorization, or sponsorship status
- bypass CAPTCHA, paywalls, legal interstitials, or ATS restrictions
- send email or submit applications without explicit action-specific approval
- commit real tenant data, resumes, generated artifacts, secrets, or submission logs

## Canonical Skill

The Open Agent Skill entrypoint is:

```text
.agents/skills/job-application-quality/SKILL.md
```

CLI-specific wrappers should point to that file rather than copy its contents.

Current wrappers:

- `.claude/skills/job-application-quality/SKILL.md`
- `.qwen/skills/job-application-quality/SKILL.md`

Codex plugin compatibility is kept through:

- `skills/job-application-quality-gate/SKILL.md`

## Data Boundaries

Real users should keep private data in gitignored local directories:

- `tenants/`
- `outputs/`
- `generated/`
- `applications/`
- `packets/`
- `submissions/`

Only synthetic fixtures under `examples/` belong in git.

## Validation Before Release

Run all relevant checks before pushing a release:

```bash
python3 scripts/validate_tenant_profile.py examples/tenant/profile.valid.json
python3 scripts/validate_role_intake.py examples/role-intake.valid.json
python3 scripts/check_policy_gates.py examples/tenant/profile.valid.json examples/role-intake.valid.json
python3 scripts/validate_multi_cli_support.py
python3 scripts/prepare_application_packet.py examples/tenant/profile.valid.json examples/role-intake.valid.json /tmp/application-packet
python3 scripts/qa_artifacts.py /tmp/application-packet/manifest.json
python3 /Users/nextwebb/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
python3 /Users/nextwebb/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/job-application-quality-gate
```

Also verify the negative fixture still blocks:

```bash
if python3 scripts/check_policy_gates.py examples/tenant/profile.valid.json examples/role-intake.sponsorship-fail.json; then
  echo "Expected sponsorship failure"
  exit 1
fi
```

## Coding Rules

- Keep changes scoped to the plugin, skill, docs, scripts, schemas, examples, or CI.
- Prefer deterministic scripts for validation over model-only judgement.
- Keep examples synthetic.
- Keep the repo dependency-light unless a new dependency is clearly justified.
- Update `CHANGELOG.md` and plugin version for user-visible releases.
