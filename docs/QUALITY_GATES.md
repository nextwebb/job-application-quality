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

