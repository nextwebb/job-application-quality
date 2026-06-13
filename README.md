# Job Application Quality

![Codex Plugin](https://img.shields.io/badge/Codex-Plugin-111111?style=flat)
![Skills](https://img.shields.io/badge/Skills-Enabled-2563eb?style=flat)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)
![Release](https://img.shields.io/github/v/release/nextwebb/job-application-quality?style=flat)
![CI](https://github.com/nextwebb/job-application-quality/actions/workflows/ci.yml/badge.svg)

AI can help with job applications. It can also quietly damage them.

One weak CV, one unsupported claim, one wrong sponsorship answer, or one accidental submit can cost a real opportunity. **Job Application Quality** is the reusable guardrail layer for agents that prepare CVs, cover letters, recruiter emails, and application packets.

It gives Codex/ChatGPT a practical workflow: use canonical facts, check the role, prepare a packet, QA the artifacts, log the decision, and stop before anything risky leaves the machine.

This is open source and multi-tenant by design.

---

## What Is This?

Job Application Quality is a local-first Codex/ChatGPT plugin and skill pack for building truthful, role-specific job application workflows.

Instead of asking an agent to "just apply," you give it a quality system:

- **Tenant profiles** for candidate facts, contact details, work authorization, policies, and reusable claims.
- **Role intake files** for job URL, ATS, location, remote policy, sponsorship status, and required skills.
- **Policy gates** that block unsafe applications before a CV or cover letter is used.
- **Application packet manifests** that record the exact inputs and artifacts used.
- **Artifact QA** for missing files, placeholders, empty outputs, and local-path leakage.
- **Submission logs** that preserve what was approved, when, and for which destination.

> Important: this is not a spray-and-pray automation tool. It is a quality gate. The plugin prepares, validates, and records application materials; it does not bypass CAPTCHA, invent experience, or remove the need for human judgment.

The intended user is any candidate, recruiter-assistant workflow, or job-search agent that needs reusable rules for application quality across multiple people without mixing their data.

## Features

| Feature | Description |
| --- | --- |
| **Codex Skill** | Adds a `job-application-quality-gate` skill for CV, cover letter, email, ATS, and browser-assisted application workflows. |
| **Open Agent Skill** | Adds a canonical `.agents/skills/job-application-quality/SKILL.md` router for multi-CLI use. |
| **Multi-Tenant Profiles** | Keeps every candidate in an isolated profile with canonical facts, policy settings, baseline artifacts, and approved claims. |
| **Role Intake Contract** | Normalizes job details into a small JSON file that can be checked before tailoring begins. |
| **Policy Gates** | Blocks unsupported ATS values, unavailable sponsorship, unknown sponsorship for relocation-sensitive roles, and unverified remote eligibility. |
| **Artifact Manifests** | Records profile hash, role hash, selected outputs, policy result, and approval status for traceability. |
| **Artifact QA** | Catches missing files, empty outputs, placeholders, and local path leakage before upload or email. |
| **Email Drafting** | Creates recruiter email drafts without sending them. |
| **Submission Logging** | Records destination, approval text, manifest hash, and outputs after explicit approval. |
| **CI Fixtures** | Ships with passing and failing examples so workflow behavior is testable from day one. |
| **Privacy Defaults** | Ignores real tenant data, generated artifacts, packets, logs, and local runtime files by default. |

## Quick Start

Clone the repo:

```bash
git clone https://github.com/nextwebb/job-application-quality.git
cd job-application-quality
```

Run the built-in checks:

```bash
python3 scripts/validate_tenant_profile.py examples/tenant/profile.valid.json
python3 scripts/validate_role_intake.py examples/role-intake.valid.json
python3 scripts/check_policy_gates.py examples/tenant/profile.valid.json examples/role-intake.valid.json
```

Prepare and QA a sample packet:

```bash
python3 scripts/prepare_application_packet.py \
  examples/tenant/profile.valid.json \
  examples/role-intake.valid.json \
  /tmp/application-packet

python3 scripts/qa_artifacts.py /tmp/application-packet/manifest.json
```

Confirm the sponsorship hard-fail fixture works:

```bash
if python3 scripts/check_policy_gates.py \
  examples/tenant/profile.valid.json \
  examples/role-intake.sponsorship-fail.json; then
  echo "Expected this role to fail"
  exit 1
else
  echo "Blocked as expected"
fi
```

## Use With Codex

Install or enable the plugin locally, then ask Codex:

```text
Use Job Application Quality to prepare an application packet for this role.

Tenant profile: /path/to/tenant/profile.json
Role intake: /path/to/role-intake.json
Output directory: /tmp/application-packet
```

Codex will follow the skill workflow:

1. Load the tenant profile and role intake.
2. Validate both files.
3. Check policy gates.
4. Select approved baseline artifacts.
5. Prepare a packet manifest.
6. Run artifact QA.
7. Present a pre-submit checklist.
8. Stop before email send, final ATS submit, CAPTCHA, identity upload, or legal attestation unless explicitly approved.

## Use With Other Agent CLIs

The canonical Open Agent Skill lives at:

```text
.agents/skills/job-application-quality/SKILL.md
```

Claude Code and Qwen wrappers point to that file:

```text
.claude/skills/job-application-quality/SKILL.md
.qwen/skills/job-application-quality/SKILL.md
```

The root `AGENTS.md` contains repository-wide rules for any coding-agent CLI. See [docs/MULTI_CLI.md](docs/MULTI_CLI.md).

## Core Commands

```bash
# Validate candidate profile structure
python3 scripts/validate_tenant_profile.py <profile.json>

# Validate role intake structure
python3 scripts/validate_role_intake.py <role-intake.json>

# Run policy gates
python3 scripts/check_policy_gates.py <profile.json> <role-intake.json>

# Prepare an application packet manifest
python3 scripts/prepare_application_packet.py <profile.json> <role-intake.json> <output-dir>

# QA packet artifacts
python3 scripts/qa_artifacts.py <manifest.json>

# Draft, but do not send, a recruiter email
python3 scripts/prepare_email_draft.py <profile.json> <role-intake.json> <manifest.json> <output.md>

# Record an approved submission event
python3 scripts/record_submission.py <manifest.json> <destination> <approval-text> <output-log.json>
```

## How It Works

```text
Tenant profile              Role intake
canonical facts             company, title, ATS, URL
claims, artifacts           remote, sponsorship, skills
       |                         |
       v                         v
  Profile validation       Role validation
       |                         |
       +-----------+-------------+
                   |
                   v
             Policy gates
     sponsorship, remote, ATS, safety
                   |
                   v
          Application packet
      selected artifacts + manifest
                   |
                   v
              Artifact QA
 placeholders, missing files, path leakage
                   |
                   v
          Approval checkpoint
      user decides whether to submit/send
                   |
                   v
            Submission log
```

## Data Model

The workflow has three primary contracts:

| File | Purpose |
| --- | --- |
| `tenant-profile.schema.json` | Candidate facts, contact details, work authorization, application policy, baseline artifacts, reusable claims, and forbidden claims. |
| `role-intake.schema.json` | Company, role title, URL, ATS, location, remote setting, sponsorship status, skills, and evidence notes. |
| `artifact-manifest.schema.json` | Generated packet metadata, input hashes, selected outputs, policy gate result, and approval state. |

See [docs/DATA_CONTRACT.md](docs/DATA_CONTRACT.md) for the detailed contract.

## Project Structure

```text
job-application-quality/
+-- .codex-plugin/
|   +-- plugin.json                         # Codex plugin manifest
+-- .agents/
|   +-- skills/job-application-quality/     # Canonical Open Agent Skill
+-- .claude/
|   +-- skills/job-application-quality/     # Claude wrapper
+-- .qwen/
|   +-- skills/job-application-quality/     # Qwen wrapper
+-- skills/
|   +-- job-application-quality-gate/
|       +-- SKILL.md                        # Codex plugin compatibility wrapper
|       +-- references/                     # Policy, browser, email, and artifact QA guidance
+-- scripts/
|   +-- validate_tenant_profile.py          # Tenant profile validator
|   +-- validate_role_intake.py             # Role intake validator
|   +-- check_policy_gates.py               # Sponsorship, remote, ATS, and safety gates
|   +-- prepare_application_packet.py       # Packet manifest builder
|   +-- qa_artifacts.py                     # Artifact QA checks
|   +-- prepare_email_draft.py              # Draft-only recruiter email helper
|   +-- record_submission.py                # Approved submission log helper
|   +-- validate_multi_cli_support.py       # Wrapper drift validator
+-- schemas/                                # JSON schema contracts
+-- examples/                               # Passing and failing fixtures
+-- evals/
|   +-- rubric.yaml                         # Quality rubric for agent review
+-- docs/                                   # Scope, architecture, gates, privacy, release process
+-- .github/workflows/ci.yml                # Validation workflow
```

## What It Will Block

The default examples and skill guidance are conservative. A workflow should stop when:

- Sponsorship is unavailable for a candidate who needs it.
- Sponsorship is unknown for relocation-sensitive local employment.
- Remote eligibility is unknown or does not appear to include the candidate location.
- The ATS is not allowed by the tenant policy.
- The form asks for passport, government ID, immigration documents, references, salary history, or long custom answers without review.
- A CV, cover letter, email, or form answer contains unsupported claims.
- A generated artifact has placeholders, missing files, duplicated sections, or obvious formatting failure.
- The agent is about to send an email or click final submit without explicit approval.

## Customizing For Your Workflow

Start from the examples:

```bash
cp examples/tenant/profile.valid.json tenants/alex/profile.json
cp examples/role-intake.valid.json roles/example-role.json
```

Then update:

- `tenant_id`, contact fields, work authorization, and application policy.
- `baseline_artifacts` to point to approved CVs, cover letters, or other packet files.
- `claims` with only verified candidate facts.
- `forbidden_claims` with credentials, skills, visa statuses, or metrics the agent must never use.
- `allowed_ats`, sponsorship policy, and remote policy for the candidate.

Real tenant data should stay local. The default `.gitignore` excludes `tenants/`, `generated/`, `packets/`, `submissions/`, and local environment files.

## Documentation

- [Product scope](docs/PRODUCT_SCOPE.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Data contracts](docs/DATA_CONTRACT.md)
- [Quality gates](docs/QUALITY_GATES.md)
- [Multi-CLI support](docs/MULTI_CLI.md)
- [Submission policy](docs/SUBMISSION_POLICY.md)
- [Security and privacy](docs/SECURITY_AND_PRIVACY.md)
- [Release process](docs/RELEASE_PROCESS.md)

## Tech Stack

- **Plugin runtime**: Codex plugin manifest, Open Agent Skill files, and CLI wrappers
- **Workflow scripts**: Python 3.11+, dependency-free standard library
- **Contracts**: JSON schemas and example fixtures
- **Quality checks**: Local scripts plus GitHub Actions CI
- **Data storage**: Local files owned by the user

## Disclaimer

Job Application Quality is a local, open-source workflow aid, not a hosted recruiting service.

By using it, you remain responsible for:

1. Reviewing all AI-generated content before submitting it.
2. Ensuring every claim in an application is true and supportable.
3. Following the Terms of Service of job boards, ATS platforms, email providers, and company websites.
4. Avoiding spam, duplicate applications, false attestations, and abusive automation.
5. Protecting candidate data, identity documents, credentials, and private communications.

No software can guarantee interviews, offers, visa outcomes, account safety, or recruiter responses. See [LEGAL_DISCLAIMER.md](LEGAL_DISCLAIMER.md) for details.

## Contributing

Contributions should make the workflow safer, more reusable, or easier to verify. Good changes include:

- Stronger validators.
- Better schema examples.
- More explicit policy gates.
- Improved artifact QA.
- Clearer skill instructions.
- Better documentation and release checks.

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. See [LICENSE](LICENSE).
