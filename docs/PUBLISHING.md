# Publishing

This project follows the official Codex plugin packaging model.

## Package Checklist

- `.codex-plugin/plugin.json` exists and identifies the plugin.
- `skills/` contains Codex-compatible skill wrappers.
- `.agents/skills/` contains the canonical Open Agent Skill router.
- `.app.json` provides optional app manifest companion metadata for the Codex plugin.
- `hooks/hooks.json` contains optional lifecycle hooks.
- `assets/` contains install-surface assets.
- `.agents/plugins/marketplace.json` exposes the plugin as a custom repo marketplace path.
- `.claude-plugin/` exposes Claude plugin metadata.
- validators and CI cover the package metadata.

## Custom Repo Marketplace Path

The custom repo marketplace path lives at:

```text
.agents/plugins/marketplace.json
```

It points to the GitHub repository root because this plugin lives at the root of the repo.
This is repository-scoped marketplace metadata, not a curated marketplace listing.

Users can add it with:

```bash
codex plugin marketplace add nextwebb/job-application-quality --sparse .agents/plugins
```

Then restart Codex and install **Job Application Quality** from the plugin directory.

## Personal Marketplace During Development

For local development, the personal marketplace is:

```text
~/.agents/plugins/marketplace.json
```

The local install path should resolve to the working plugin directory. After metadata changes, update the plugin cachebuster:

```bash
python3 /Users/nextwebb/.codex/skills/.system/plugin-creator/scripts/update_plugin_cachebuster.py .
```

## Hooks

Codex can discover plugin-bundled hooks from:

```text
hooks/hooks.json
```

The hook in this repository is intentionally lightweight. It only adds startup context about candidate-truthfulness and approval gates. It does not inspect private data, send network requests, or enforce hidden behavior.

## MCP

No MCP server is bundled yet. Add `.mcp.json` only when the project has a real, documented MCP server with deterministic local behavior and validation.
