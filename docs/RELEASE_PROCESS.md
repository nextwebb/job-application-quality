# Release Process

Releases should be small, auditable, and safety-forward.

## Release Checklist

- [ ] Skill trigger text reviewed.
- [ ] Tenant isolation tests pass.
- [ ] Schema fixtures validate.
- [ ] No-invented-claims checks pass.
- [ ] Sponsorship and remote hard-fail tests pass.
- [ ] Codex app metadata validates.
- [ ] Repo marketplace metadata validates.
- [ ] Claude plugin metadata validates.
- [ ] Multi-CLI wrappers validate.
- [ ] Plugin hooks validate.
- [ ] Email send path remains approval-gated.
- [ ] Browser final-submit path remains approval-gated.
- [ ] Artifact manifest generated for every packet.
- [ ] Logs redact secrets and sensitive tokens.
- [ ] Docs updated for behavior or schema changes.
- [ ] No real personal data committed.

## Required Local Commands

```bash
python3 scripts/validate_tenant_profile.py examples/tenant/profile.valid.json
python3 scripts/validate_role_intake.py examples/role-intake.valid.json
python3 scripts/check_policy_gates.py examples/tenant/profile.valid.json examples/role-intake.valid.json
python3 scripts/validate_multi_cli_support.py
python3 scripts/validate_package_metadata.py
python3 scripts/prepare_application_packet.py examples/tenant/profile.valid.json examples/role-intake.valid.json /tmp/application-packet
python3 scripts/qa_artifacts.py /tmp/application-packet/manifest.json
python3 /Users/nextwebb/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
python3 /Users/nextwebb/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/job-application-quality-gate
```

## Release Notes Template

```md
## x.y.z - YYYY-MM-DD

### Why This Release Matters

Short user-facing explanation.

### Highlights

- Capability or workflow improvement.

### Safety / Privacy

- Gate, policy, or data-handling changes.

### Migration Notes

- Required config or schema updates.

### Fixes

- Bug fixes with practical impact.
```
