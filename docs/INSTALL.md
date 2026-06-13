# Install

Job Application Quality can be used three ways:

1. as a plain local repository with the `jobqa` CLI
2. as a Codex plugin package with reusable skills
3. as a Claude plugin/skill package

## Codex

The Codex plugin manifest is:

```text
.codex-plugin/plugin.json
```

The optional app manifest companion metadata is:

```text
.app.json
```

The custom repo marketplace path is:

```text
.agents/plugins/marketplace.json
```

Add the custom repo marketplace with Codex CLI 0.121.0+:

```bash
codex marketplace add nextwebb/job-application-quality
```

The marketplace entry uses `source: { "source": "local", "path":
"./plugins/job-application-quality" }`. That path is a repo-local plugin package path, so a sparse
checkout containing only `.agents/plugins` is not enough for installation.

Then restart Codex and install **Job Application Quality** from the plugin directory.

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

## Hooks

The plugin bundles a default startup hook:

```text
hooks/hooks.json
hooks/session_start_context.py
```

Codex requires hook review and trust before non-managed command hooks run.

## Manual Use

Clone the repo:

```bash
git clone https://github.com/nextwebb/job-application-quality.git
cd job-application-quality
```

Run the CLI:

```bash
./bin/jobqa demo
./bin/jobqa init /tmp/my-application
./bin/jobqa run /tmp/my-application
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
