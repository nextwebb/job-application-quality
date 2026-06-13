# Architecture

The plugin is organized around tenant isolation and deterministic gates.

```text
tenant profile + role intake
        |
        v
schema validation
        |
        v
policy gates
        |
        v
application packet
        |
        v
artifact QA + manifest
        |
        v
approval checklist
        |
        v
manual/browser/email action
```

## Main Components

- `skills/job-application-quality-gate/SKILL.md`: agent workflow and routing.
- `schemas/`: JSON schemas for reusable data contracts.
- `scripts/`: deterministic validators and packet builders.
- `examples/`: fake tenant and role fixtures.
- `docs/`: user-facing and maintainer-facing documentation.
- `evals/`: quality rubric and fixtures for future automated checks.

## Multi-Tenant Model

Each candidate should live in a separate tenant directory:

```text
tenants/<tenant_id>/
  profile.json
  applications/<role_id>/
    role-intake.json
    outputs/
    qa/
    manifests/
    logs/
```

Scripts accept explicit file paths and do not search across tenant directories. This keeps cross-tenant leakage out of the happy path.

