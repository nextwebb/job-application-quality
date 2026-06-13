# Changelog

## 0.3.0 - 2026-06-13

### Added

- Codex app companion manifest with plugin metadata wiring.
- Claude plugin metadata and marketplace descriptor.
- Install, Codex app, and Claude plugin documentation.
- Root data contract, governance, code of conduct, trademark, contributors, and citation files.
- GitHub issue templates and pull request template.
- Engineering and documentation rules as project memory.
- Package metadata validator and CI coverage.

### Changed

- Plugin metadata now advertises Codex app and Claude plugin packaging.
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
