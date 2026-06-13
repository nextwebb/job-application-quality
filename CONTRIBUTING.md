# Contributing

Thanks for considering a contribution. This project is intentionally conservative: it protects candidate truthfulness, privacy, and human review.

Please open an issue before large behavior changes. Small documentation fixes, typo fixes, fixture fixes, and validator bug fixes can go straight to a pull request.

## Good Contributions

- Better validators for tenant profiles and role intake.
- More complete synthetic examples.
- Stronger artifact QA.
- Safer browser and email workflow guidance.
- Documentation that clarifies safety boundaries.
- Codex, Claude, or Open Agent Skill packaging improvements with validation.

## Not Accepted

- Features that invent candidate facts.
- Auto-submit flows without explicit review.
- CAPTCHA bypass or ToS-avoidance logic.
- Real candidate data in fixtures.
- Hidden network calls or telemetry.
- Hosted scraping or proxy infrastructure in the core package.
- New external dependencies without prior discussion.

## Pull Requests

- Keep changes focused.
- Add or update examples when contracts change.
- Run validation scripts before opening a PR.
- Update docs when behavior changes.
- Explain safety implications.
- Use the pull request template and include validation output where possible.

## Development Checks

```bash
python3 scripts/validate_tenant_profile.py examples/tenant/profile.valid.json
python3 scripts/validate_role_intake.py examples/role-intake.valid.json
python3 scripts/check_policy_gates.py examples/tenant/profile.valid.json examples/role-intake.valid.json
python3 scripts/validate_multi_cli_support.py
python3 scripts/validate_package_metadata.py
```

Confirm the sponsorship fixture fails:

```bash
if python3 scripts/check_policy_gates.py examples/tenant/profile.valid.json examples/role-intake.sponsorship-fail.json; then
  echo "Expected sponsorship failure"
  exit 1
fi
```

## Project Rules

Read [AGENTS.md](AGENTS.md), [DATA_CONTRACT.md](DATA_CONTRACT.md), [docs/ENGINEERING_RULES.md](docs/ENGINEERING_RULES.md), and [docs/DOCUMENTATION_RULES.md](docs/DOCUMENTATION_RULES.md) before changing core behavior.
