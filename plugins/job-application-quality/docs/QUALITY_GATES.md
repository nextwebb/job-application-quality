# Quality Gates

## Hard Fail

- Unsupported candidate claim
- Invented metric
- Altered employment date
- Sponsorship or work authorization mismatch
- Remote/location mismatch
- Required false attestation
- Missing artifact manifest
- Failing QA report
- Send/submit action without explicit approval

## Warning

- Salary unknown
- Role fit below threshold
- Job posting older than configured freshness window
- Optional cover letter missing
- Evidence is truthful but weak

## Artifact QA

Artifacts should pass these checks:

- Correct candidate name
- Correct company and role
- No placeholders
- No private tenant path leakage
- No forbidden claims
- No incorrect location or links
- Required keywords represented naturally

## Truth And Evidence Checks

Artifact QA also compares generated text against the tenant profile and role intake:

- Claims in `forbidden_claims` must not appear in generated artifacts.
- Claims with `confidence: blocked` must not appear in generated artifacts.
- Required role skills should have support in canonical candidate claims.
- Required skills with no support are warnings unless they appear as unsupported claims.
- Supported required skills are reported as matches.

Example:

```text
Candidate facts:
- AWS Lambda
- Python
- no Kubernetes experience

Role requires:
- Kubernetes
- Terraform
- AWS

Generated CV says:
- "Built Kubernetes production clusters for high-availability deployments."

QA result:
- unsupported claim: Kubernetes production clusters
- missing Terraform evidence
- AWS match
- stop before submission
```
