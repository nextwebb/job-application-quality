#!/usr/bin/env python3
"""Validate Codex app and Claude plugin packaging metadata."""

from __future__ import annotations

from pathlib import Path

from common import fail, load_json


ROOT = Path(__file__).resolve().parent.parent


def require_file(path: Path, errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"missing {path.relative_to(ROOT)}")


def validate_codex_app(errors: list[str]) -> None:
    app_path = ROOT / ".app.json"
    require_file(app_path, errors)
    if not app_path.is_file():
        return
    payload = load_json(app_path)
    apps = payload.get("apps")
    if not isinstance(apps, dict) or "job-application-quality" not in apps:
        errors.append(".app.json must define apps.job-application-quality")
        return
    app = apps["job-application-quality"]
    if not isinstance(app, dict) or app.get("id") != "job-application-quality":
        errors.append(".app.json apps.job-application-quality.id must be job-application-quality")

    plugin = load_json(ROOT / ".codex-plugin" / "plugin.json")
    if plugin.get("apps") != "./.app.json":
        errors.append(".codex-plugin/plugin.json must reference ./.app.json in apps")


def validate_claude_plugin(errors: list[str]) -> None:
    plugin_path = ROOT / ".claude-plugin" / "plugin.json"
    marketplace_path = ROOT / ".claude-plugin" / "marketplace.json"
    require_file(plugin_path, errors)
    require_file(marketplace_path, errors)
    if not plugin_path.is_file() or not marketplace_path.is_file():
        return

    plugin = load_json(plugin_path)
    for key in ("name", "version", "description", "author", "skills", "permissions"):
        if key not in plugin:
            errors.append(f".claude-plugin/plugin.json missing {key}")
    if plugin.get("name") != "job-application-quality":
        errors.append(".claude-plugin/plugin.json name must be job-application-quality")
    if plugin.get("skills") is not True:
        errors.append(".claude-plugin/plugin.json skills must be true")
    permissions = plugin.get("permissions", {}).get("allow", [])
    if "Bash(python3:*)" not in permissions:
        errors.append(".claude-plugin/plugin.json must allow Bash(python3:*)")

    marketplace = load_json(marketplace_path)
    plugins = marketplace.get("plugins", [])
    if not isinstance(plugins, list) or not plugins:
        errors.append(".claude-plugin/marketplace.json must contain plugins")
        return
    entry = plugins[0]
    if entry.get("name") != "job-application-quality":
        errors.append(".claude-plugin/marketplace.json first plugin name must be job-application-quality")
    if entry.get("source") != "./":
        errors.append(".claude-plugin/marketplace.json source must be ./")


def validate_docs(errors: list[str]) -> None:
    for path in (
        "CODE_OF_CONDUCT.md",
        "CONTRIBUTING.md",
        "GOVERNANCE.md",
        "TRADEMARK.md",
        "DATA_CONTRACT.md",
        "docs/INSTALL.md",
        "docs/CODEX_APP.md",
        "docs/CLAUDE_PLUGIN.md",
        "docs/ENGINEERING_RULES.md",
        "docs/DOCUMENTATION_RULES.md",
        ".github/PULL_REQUEST_TEMPLATE.md",
    ):
        require_file(ROOT / path, errors)


def validate() -> list[str]:
    errors: list[str] = []
    validate_codex_app(errors)
    validate_claude_plugin(errors)
    validate_docs(errors)
    return errors


def main() -> None:
    fail(validate())
    print("PASS package metadata")


if __name__ == "__main__":
    main()
