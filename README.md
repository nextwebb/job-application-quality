# Job Application Quality

Reusable Codex/ChatGPT plugin for quality-first job application packets.

It helps an agent prepare role-specific CVs, cover letters, recruiter emails, and application data without turning job search into a spray-and-pray machine. The core idea is simple: **canonical facts first, quality gates before upload, explicit approval before send or submit**.

## What It Does

- Keeps each candidate in an isolated tenant workspace.
- Loads only canonical, user-approved facts.
- Checks sponsorship, remote, location, salary, and false-attestation gates.
- Builds application packets from role facts and selected claim IDs.
- Runs artifact QA before any CV, cover letter, or email is used.
- Writes manifests and submission logs for traceability.
- Blocks weak, unsupported, or unsafe applications.

## What It Does Not Do

- It does not invent candidate claims, metrics, dates, employers, credentials, or work authorization.
- It does not bypass CAPTCHA, paywalls, legal interstitials, or ATS restrictions.
- It does not send email or submit applications without explicit approval.
- It does not commit real tenant data, resumes, or generated artifacts.

## Quick Start

```bash
git clone https://github.com/nextwebb/job-application-quality.git
cd job-application-quality

python3 scripts/validate_tenant_profile.py examples/tenant/profile.valid.json
python3 scripts/check_policy_gates.py examples/tenant/profile.valid.json examples/role-intake.valid.json
python3 scripts/prepare_application_packet.py examples/tenant/profile.valid.json examples/role-intake.valid.json /tmp/application-packet
python3 scripts/qa_artifacts.py /tmp/application-packet/manifest.json
```

## Codex Usage

Install the plugin locally, then ask:

```text
Use Job Application Quality to prepare an application packet for this role.
Tenant profile: /path/to/tenant/profile.json
Role intake: /path/to/role-intake.json
Baseline artifact directory: /path/to/generated
```

The skill will load the profile, validate policy gates, select the safest baseline CV/cover-letter variant, produce a manifest, and stop at a clear pre-submit checklist.

## Documentation

- [Product scope](docs/PRODUCT_SCOPE.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Data contracts](docs/DATA_CONTRACT.md)
- [Quality gates](docs/QUALITY_GATES.md)
- [Submission policy](docs/SUBMISSION_POLICY.md)
- [Release process](docs/RELEASE_PROCESS.md)
- [Security and privacy](docs/SECURITY_AND_PRIVACY.md)

## Release Philosophy

This project follows a local-first, human-in-the-loop approach. Releases should explain what changed, why it matters, migration notes, and the safety checks that passed. See [Release process](docs/RELEASE_PROCESS.md).

## License

MIT. See [LICENSE](LICENSE).

