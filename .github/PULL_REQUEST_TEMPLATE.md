## Summary

- 

## Type

- [ ] Bug fix
- [ ] Documentation
- [ ] Safety/policy gate
- [ ] Package/install metadata
- [ ] CLI wrapper
- [ ] Other

## Validation

- [ ] `python3 scripts/validate_tenant_profile.py examples/tenant/profile.valid.json`
- [ ] `python3 scripts/validate_role_intake.py examples/role-intake.valid.json`
- [ ] `python3 scripts/check_policy_gates.py examples/tenant/profile.valid.json examples/role-intake.valid.json`
- [ ] `python3 scripts/validate_multi_cli_support.py`
- [ ] `python3 scripts/validate_package_metadata.py`
- [ ] `python3 scripts/validate_site.py`
- [ ] Negative sponsorship fixture still fails

## Data Safety

- [ ] No real candidate data committed
- [ ] No secrets committed
- [ ] New user-owned paths are gitignored
- [ ] No unsafe auto-submit behavior added
