# Codex App

This repository is packaged for Codex through:

- `.codex-plugin/plugin.json`
- `.app.json`
- `.agents/plugins/marketplace.json`
- `skills/job-application-quality-gate/SKILL.md`
- `hooks/hooks.json`
- `assets/`

## Contract

The Codex app/plugin package is local-first. It does not run a hosted backend, collect candidate data, or submit applications by itself.

The app metadata exists so Codex can discover the package as a reusable plugin surface. The actual workflow lives in deterministic scripts and skills.

The repo marketplace can be added with:

```bash
codex plugin marketplace add nextwebb/job-application-quality --sparse .agents/plugins
```

## Validation

Run:

```bash
python3 /Users/nextwebb/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
python3 scripts/validate_package_metadata.py
```

## Default Prompt

Use Job Application Quality to prepare a role-specific application packet with canonical facts, QA, and a submission checklist.
