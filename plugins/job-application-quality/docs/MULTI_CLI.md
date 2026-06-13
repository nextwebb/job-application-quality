# Multi-CLI Support

Job Application Quality supports the Open Agent Skill layout introduced by the upstream Career-Ops multi-CLI pattern.

## Canonical Entry Point

The canonical skill lives at:

```text
.agents/skills/job-application-quality/SKILL.md
```

That file contains the mode router, safety rules, context-loading rules, and preferred scripts.

## Wrappers

CLI-specific files should be lightweight wrappers that point to the canonical skill:

| CLI family | File |
| --- | --- |
| Claude Code | `.claude/skills/job-application-quality/SKILL.md` |
| Qwen Code | `.qwen/skills/job-application-quality/SKILL.md` |
| Open Agent Skill compatible tools | `.agents/skills/job-application-quality/SKILL.md` |
| Codex plugin | `skills/job-application-quality-gate/SKILL.md` |

The Codex plugin skill remains a valid Codex skill file and delegates to the canonical Open Agent Skill instructions.

## Why This Shape

The goal is to keep one source of truth for behavior while still supporting tools with different discovery paths.

The repository should not grow separate command trees for Gemini, OpenCode, Claude, Qwen, Codex, and future CLIs. Add a wrapper only when a CLI requires a discovery-specific path; otherwise, point the tool at `.agents/skills/job-application-quality/SKILL.md`.

## Validation

Run:

```bash
python3 scripts/validate_multi_cli_support.py
```

The validator checks:

- canonical Open Agent Skill exists
- wrappers point to the canonical skill
- root `AGENTS.md` exists and references the canonical skill
- `CLAUDE.md` imports `AGENTS.md`
- Codex plugin compatibility skill remains valid enough to route to the canonical skill

