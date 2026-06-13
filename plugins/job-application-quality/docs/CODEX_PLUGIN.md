# Codex Plugin

This repository is packaged for Codex as a plugin package with reusable skills through:

- `.codex-plugin/plugin.json`
- `.app.json` companion metadata
- `.agents/plugins/marketplace.json`
- `skills/job-application-quality-gate/SKILL.md`
- `hooks/hooks.json`
- `assets/`

## Contract

The Codex plugin package is local-first. It is not a standalone Codex App, hosted backend, MCP server, data collector, or autonomous application submitter.

The `.app.json` file is companion metadata only. It helps Codex discover the package as a reusable plugin surface; the actual workflow lives in deterministic scripts and skills.

The custom repo marketplace path can be added with:

```bash
codex marketplace add nextwebb/job-application-quality
```

This path is repository-scoped marketplace metadata, not a curated marketplace listing. Its plugin
entry uses Codex CLI's local source shape and resolves to `./plugins/job-application-quality`
inside the marketplace clone. That source path is a materialized plugin package, not a symlink to
the repo root.

## Validation

Run:

```bash
python3 /Users/nextwebb/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/job-application-quality
python3 scripts/validate_package_metadata.py
```

## Default Prompt

Use jobqa to run preflight QA on this application packet before submission.
