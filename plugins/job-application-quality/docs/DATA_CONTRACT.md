# Data Contract

## Tenant Profile

`profile.json` is the source of truth for candidate facts. It contains:

- Contact details
- Work authorization
- Application policy
- Canonical claims
- Baseline artifacts

Every reusable claim must have a stable `claim_id` and a confidence level.

## Role Intake

`role-intake.json` stores job-specific facts:

- Company
- Title
- Official URL
- ATS
- Location/remote facts
- Sponsorship evidence
- Required and preferred skills
- Required form questions

## Artifact Manifest

Every packet writes `manifest.json` with:

- Input hashes
- Output hashes
- Policy gate results
- QA status
- Approval status

If a manifest is missing, the packet is not ready for submission.

