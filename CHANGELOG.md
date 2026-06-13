# Changelog

## Unreleased

### Added

- README site preview screenshot and `jobqa` dry-run GIF.
- Codex plugin taxonomy docs and validator coverage for avoiding standalone Codex App overclaims.

## 0.7.0 - 2026-06-13

### Added

- Static GitHub Pages site under `site/` for the JAQ project brief, PRD narrative, quality gates, CLI quick start, and unsupported-claim demo.
- GitHub Pages deployment workflow using `actions/deploy-pages`.
- `scripts/validate_site.py` to verify local site assets, anchors, and secret/config leakage.
- CI coverage and PR checklist coverage for site validation.

## 0.6.0 - 2026-06-13

### Added

- `jobqa` CLI with `demo`, `init`, `run`, `qa`, and `report` commands.
- `bin/jobqa` executable wrapper.
- `examples/basic/` simple passing workspace.
- CLI documentation.
- CI coverage for CLI demo, happy path, and failure path.

### Changed

- README quick start now leads with the `jobqa` CLI.

## 0.5.0 - 2026-06-13

### Added

- "Why this exists" README diagram that positions the project as a preflight QA layer.
- Runnable unsupported-claim demo under `examples/claim-demo/`.
- `scripts/run_claim_demo.py` for a one-command proof of unsupported claim blocking.
- Artifact QA truth/evidence checks for forbidden claims, missing required-skill evidence, and supported role matches.

### Changed

- README now uses the "Preflight checks for AI-generated job applications" positioning.
- CI now runs the unsupported-claim demo.

## 0.4.0 - 2026-06-13

### Added

- Custom repo marketplace metadata at `.agents/plugins/marketplace.json`.
- Install-surface assets under `assets/`.
- Default plugin-bundled `SessionStart` hook under `hooks/hooks.json`.
- Publishing documentation aligned with the official Codex plugin build guide.
- Validator coverage for marketplace metadata, hook config, assets, and richer manifest metadata.

### Changed

- Codex plugin manifest now includes richer publisher, repository, legal, asset, and install-surface metadata.
- CI now validates hook JSON and hook script output.

## 0.3.0 - 2026-06-13

### Added

- Optional app manifest companion metadata with plugin metadata wiring.
- Claude plugin metadata and marketplace descriptor.
- Install, Codex plugin metadata, and Claude plugin documentation.
- Root data contract, governance, code of conduct, trademark, contributors, and citation files.
- GitHub issue templates and pull request template.
- Engineering and documentation rules as project memory.
- Package metadata validator and CI coverage.

### Changed

- Plugin metadata now advertises Codex plugin companion metadata and Claude plugin packaging.
- Root `AGENTS.md` now includes global project memory for coding, engineering, and documentation rules.

## 0.2.0 - 2026-06-13

### Added

- Canonical `.agents/skills/job-application-quality/SKILL.md` Open Agent Skill router.
- Claude and Qwen wrapper skill files that point to the canonical skill.
- Root `AGENTS.md` instructions and `CLAUDE.md` import wrapper.
- Multi-CLI support documentation.
- `scripts/validate_multi_cli_support.py` and CI coverage for wrapper drift.

### Changed

- Codex plugin skill now acts as a compatibility wrapper that references the canonical Open Agent Skill.
- Plugin metadata now advertises Open Agent Skill and multi-CLI routing support.

## 0.1.0 - 2026-06-13

### Added

- Initial Codex plugin scaffold.
- Job Application Quality skill with canonical-fact workflow.
- Multi-tenant profile and role-intake schemas.
- Policy gate, artifact QA, manifest, packet, email draft, and submission log scripts.
- Example tenant profile and role intake fixtures.
- Release, privacy, and submission safety documentation.
- CI for scripts and schema fixtures.
