# Governance

## Overview

Job Application Quality is maintained as a local-first, human-in-the-loop safety layer for job application workflows.

The project favors a small-core governance model:

- deterministic validation before agent judgement
- user-owned local data
- no fake candidate claims
- no unsafe auto-submit behavior
- clear docs before broad automation

## Decision Making

| Area | Decision path |
| --- | --- |
| Safety policy, submission gates, data contracts | Maintainer decision after discussion |
| Bug fixes | Pull request with reproduction and validation |
| Documentation | Pull request with clear scope |
| New CLI wrappers | Pull request with validator coverage |
| New scripts | Issue first when behavior changes user safety or data boundaries |
| Hosted services, scraping infrastructure, or autonomous submission | Out of scope unless governance explicitly changes |

## Contributor Roles

### Participant

Anyone opening issues, asking questions, suggesting improvements, or reviewing docs.

### Contributor

Someone with merged pull requests or meaningful issue triage.

### Reviewer

A trusted contributor who understands the safety model, data contract, and validation suite well enough to review changes.

### Maintainer

A steward with merge and release authority.

## Values

- **Truth over conversion**: no application is worth unsupported claims.
- **Local-first**: private candidate data should stay under user control.
- **Human-in-the-loop**: agents prepare and check; humans approve sensitive actions.
- **Evidence-led changes**: risky behavior needs tests, fixtures, or documented rationale.
- **Small core**: reusable local workflow first, hosted infrastructure only as a separate explicit project.

## Release Authority

Releases should only be cut after:

- local validation passes
- GitHub CI passes
- changelog is updated
- version metadata is updated
- privacy/data-boundary changes are documented

See [docs/RELEASE_PROCESS.md](docs/RELEASE_PROCESS.md).
