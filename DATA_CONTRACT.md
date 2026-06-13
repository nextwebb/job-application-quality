# Data Contract

This document defines which files are system-owned and which files contain user-owned candidate data.

## User Layer

These files may contain personal data, generated application materials, private policies, or application history. They should not be committed.

| Path | Purpose |
| --- | --- |
| `tenants/<tenant_id>/profile.json` | Candidate profile, facts, work authorization, policies, and claims |
| `tenants/<tenant_id>/applications/` | Per-role application working data |
| `outputs/` | Generated local outputs |
| `generated/` | Generated CVs, cover letters, packets, and drafts |
| `applications/` | Local application state |
| `packets/` | Prepared packet manifests and artifacts |
| `submissions/` | Submission logs and approval records |
| `.env*` | Secrets and local environment configuration |

## System Layer

These files are safe to update through normal releases.

| Path | Purpose |
| --- | --- |
| `.codex-plugin/plugin.json` | Codex plugin metadata |
| `.app.json` | Optional app manifest companion metadata for Codex plugin discovery |
| `.agents/skills/job-application-quality/SKILL.md` | Canonical Open Agent Skill |
| `.claude/skills/job-application-quality/SKILL.md` | Claude wrapper skill |
| `.qwen/skills/job-application-quality/SKILL.md` | Qwen wrapper skill |
| `.claude-plugin/` | Claude plugin metadata |
| `skills/job-application-quality-gate/` | Codex plugin skill and references |
| `scripts/` | Deterministic validators and packet helpers |
| `schemas/` | JSON schema contracts |
| `docs/` | Project documentation |
| `examples/` | Synthetic fixtures |
| `evals/` | Rubric and future evaluation fixtures |
| `.github/` | GitHub automation and templates |

## Rules

- System updates must not overwrite user-layer files.
- Examples must stay synthetic.
- Private resumes, phone numbers, immigration documents, salary history, and application logs do not belong in git.
- Any new user-layer path must be added to `.gitignore` before release.
- Scripts must accept explicit paths and avoid cross-tenant discovery.
