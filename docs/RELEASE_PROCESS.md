# Release Process

Releases should be small, auditable, and safety-forward.

## Release Checklist

- [ ] Skill trigger text reviewed.
- [ ] Tenant isolation tests pass.
- [ ] Schema fixtures validate.
- [ ] No-invented-claims checks pass.
- [ ] Sponsorship and remote hard-fail tests pass.
- [ ] Email send path remains approval-gated.
- [ ] Browser final-submit path remains approval-gated.
- [ ] Artifact manifest generated for every packet.
- [ ] Logs redact secrets and sensitive tokens.
- [ ] Docs updated for behavior or schema changes.
- [ ] No real personal data committed.

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

