# Install

Job Application Quality can be used three ways:

1. as a Codex plugin/app package
2. as a Claude plugin/skill package
3. as a plain local repository with scripts

## Codex

The Codex plugin manifest is:

```text
.codex-plugin/plugin.json
```

The Codex app companion manifest is:

```text
.app.json
```

For local development, open this repository in Codex and use the plugin marketplace entry from your personal marketplace if installed. The local plugin also has a Codex-compatible skill at:

```text
skills/job-application-quality-gate/SKILL.md
```

That skill delegates to the canonical Open Agent Skill:

```text
.agents/skills/job-application-quality/SKILL.md
```

## Claude

The Claude plugin metadata is:

```text
.claude-plugin/plugin.json
.claude-plugin/marketplace.json
```

The Claude skill wrapper is:

```text
.claude/skills/job-application-quality/SKILL.md
```

The wrapper points to the canonical Open Agent Skill so Claude and other CLIs share the same behavior.

## Manual Use

Clone the repo:

```bash
git clone https://github.com/nextwebb/job-application-quality.git
cd job-application-quality
```

Run the validation suite:

```bash
python3 scripts/validate_tenant_profile.py examples/tenant/profile.valid.json
python3 scripts/validate_role_intake.py examples/role-intake.valid.json
python3 scripts/check_policy_gates.py examples/tenant/profile.valid.json examples/role-intake.valid.json
python3 scripts/validate_multi_cli_support.py
python3 scripts/validate_package_metadata.py
```

Prepare a sample packet:

```bash
python3 scripts/prepare_application_packet.py \
  examples/tenant/profile.valid.json \
  examples/role-intake.valid.json \
  /tmp/application-packet

python3 scripts/qa_artifacts.py /tmp/application-packet/manifest.json
```
