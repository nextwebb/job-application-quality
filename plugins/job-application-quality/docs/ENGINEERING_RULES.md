# Engineering Rules

These rules are project memory for future agents and contributors.

## Operating Principles

- Prefer deterministic scripts for checks that must be repeatable.
- Keep agent instructions as routing and policy, not hidden business logic.
- Do not add new dependencies unless the benefit is clear and documented.
- Keep the core local-first and file-based.
- Preserve tenant isolation; scripts should operate on explicit paths.
- Use synthetic fixtures in `examples/`.
- Keep real candidate data out of git.
- Treat sponsorship, work authorization, identity documents, salary history, and references as sensitive.

## Coding Rules

- Keep edits scoped to the requested behavior.
- Match existing style before adding abstractions.
- Add abstractions only when they remove real duplication or clarify safety boundaries.
- Prefer structured data contracts over ad hoc strings.
- Fail closed on policy gates.
- Emit clear errors for validation failures.
- Do not swallow missing-file or malformed-json errors when safety depends on them.
- Add or update validators when adding package metadata, wrappers, schemas, or safety gates.

## Verification

Before release, run:

```bash
python3 scripts/validate_tenant_profile.py examples/tenant/profile.valid.json
python3 scripts/validate_role_intake.py examples/role-intake.valid.json
python3 scripts/check_policy_gates.py examples/tenant/profile.valid.json examples/role-intake.valid.json
python3 scripts/validate_multi_cli_support.py
python3 scripts/validate_package_metadata.py
python3 scripts/prepare_application_packet.py examples/tenant/profile.valid.json examples/role-intake.valid.json /tmp/application-packet
python3 scripts/qa_artifacts.py /tmp/application-packet/manifest.json
```

Also verify the negative sponsorship fixture fails.
