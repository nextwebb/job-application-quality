# Claude Plugin

This repository includes Claude plugin metadata inspired by the same packaging pattern used by Career-Ops.

## Files

```text
.claude-plugin/plugin.json
.claude-plugin/marketplace.json
.claude/skills/job-application-quality/SKILL.md
```

The `.claude/skills` wrapper points to:

```text
.agents/skills/job-application-quality/SKILL.md
```

## Permissions

The Claude plugin metadata allows local Python and Git commands:

```json
[
  "Bash(python3:*)",
  "Bash(git:*)"
]
```

It does not grant browser automation, email sending, web scraping, or network permissions by default.

## Usage

Open the repository in Claude Code and ask:

```text
Use job-application-quality to prepare a packet for this tenant profile and role intake.
```

Claude should load the canonical skill, validate the inputs, run policy gates, prepare a manifest, QA artifacts, and stop before send or final submit.
