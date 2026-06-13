#!/usr/bin/env python3
"""Validate Codex and Claude plugin packaging metadata."""

from __future__ import annotations

from pathlib import Path

from common import fail, load_json


ROOT = Path(__file__).resolve().parent.parent
CODEX_PLUGIN_NAME = "job-application-quality"
CODEX_MARKETPLACE_SOURCE_PATH = "./plugins/job-application-quality"
CODEX_PLUGIN_PACKAGE_FILES = (
    ".codex-plugin/plugin.json",
    ".app.json",
    ".agents/skills/job-application-quality/SKILL.md",
    "skills/job-application-quality-gate/SKILL.md",
    "scripts/jobqa.py",
    "schemas/tenant-profile.schema.json",
    "examples/basic/candidate.json",
    "hooks/hooks.json",
    "assets/icon.svg",
)
PRIVATE_DATA_DIRS = ("tenants", "outputs", "generated", "applications", "packets", "submissions")


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
    for key in ("homepage", "repository", "license", "keywords"):
        if key not in plugin:
            errors.append(f".codex-plugin/plugin.json missing {key}")
    interface = plugin.get("interface", {})
    for key in ("websiteURL", "privacyPolicyURL", "termsOfServiceURL", "brandColor", "composerIcon", "logo"):
        if key not in interface:
            errors.append(f".codex-plugin/plugin.json interface missing {key}")
    for key in ("composerIcon", "logo"):
        raw_path = interface.get(key)
        if isinstance(raw_path, str) and raw_path.startswith("./"):
            require_file(ROOT / raw_path[2:], errors)


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


def validate_repo_marketplace(errors: list[str]) -> None:
    path = ROOT / ".agents" / "plugins" / "marketplace.json"
    require_file(path, errors)
    if not path.is_file():
        return
    payload = load_json(path)
    if payload.get("name") != "job-application-quality":
        errors.append(".agents/plugins/marketplace.json name must be job-application-quality")
    if payload.get("interface", {}).get("displayName") != "Job Application Quality":
        errors.append(".agents/plugins/marketplace.json interface.displayName mismatch")
    plugins = payload.get("plugins", [])
    if not isinstance(plugins, list) or len(plugins) != 1:
        errors.append(".agents/plugins/marketplace.json must contain exactly one plugin")
        return
    entry = plugins[0]
    if entry.get("name") != "job-application-quality":
        errors.append(".agents/plugins/marketplace.json plugin name mismatch")
    source = entry.get("source", {})
    if not isinstance(source, dict):
        errors.append(".agents/plugins/marketplace.json source must be an object")
        source = {}
    if source.get("source") != "local":
        errors.append(".agents/plugins/marketplace.json source.source must be local")
    if source.get("path") != CODEX_MARKETPLACE_SOURCE_PATH:
        errors.append(
            ".agents/plugins/marketplace.json source.path must be "
            f"{CODEX_MARKETPLACE_SOURCE_PATH}"
        )
    for unsupported_key in ("url", "ref"):
        if unsupported_key in source:
            errors.append(
                ".agents/plugins/marketplace.json source must not contain "
                f"{unsupported_key}"
            )
    raw_source_path = source.get("path")
    if isinstance(raw_source_path, str):
        if raw_source_path in ("", ".", "./"):
            errors.append(".agents/plugins/marketplace.json source.path must not be empty")
        raw_plugin_root = ROOT / raw_source_path
        if raw_plugin_root.is_symlink():
            errors.append(".agents/plugins/marketplace.json source.path must not be a symlink")
        if not raw_plugin_root.is_dir():
            errors.append(".agents/plugins/marketplace.json source.path must be a directory")
        for private_dir in PRIVATE_DATA_DIRS:
            if (raw_plugin_root / private_dir).exists():
                errors.append(
                    ".agents/plugins/marketplace.json source.path must not include "
                    f"private data directory '{private_dir}'"
                )
        for relative_path in CODEX_PLUGIN_PACKAGE_FILES:
            require_file(raw_plugin_root / relative_path, errors)
        plugin_root = raw_plugin_root.resolve()
        source_path_inside_repo = True
        try:
            plugin_root.relative_to(ROOT.resolve())
        except ValueError:
            source_path_inside_repo = False
            errors.append(".agents/plugins/marketplace.json source.path must stay inside repo")
        if source_path_inside_repo:
            plugin_manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
            require_file(plugin_manifest_path, errors)
            if plugin_manifest_path.is_file():
                plugin = load_json(plugin_manifest_path)
                if plugin.get("name") != CODEX_PLUGIN_NAME:
                    errors.append(
                        ".agents/plugins/marketplace.json source.path must resolve to "
                        f"{CODEX_PLUGIN_NAME} plugin"
                    )
    policy = entry.get("policy", {})
    if policy.get("installation") != "AVAILABLE":
        errors.append(".agents/plugins/marketplace.json policy.installation must be AVAILABLE")
    if policy.get("authentication") != "ON_INSTALL":
        errors.append(".agents/plugins/marketplace.json policy.authentication must be ON_INSTALL")
    if entry.get("category") != "Productivity":
        errors.append(".agents/plugins/marketplace.json category must be Productivity")


def validate_hooks(errors: list[str]) -> None:
    hooks_path = ROOT / "hooks" / "hooks.json"
    script_path = ROOT / "hooks" / "session_start_context.py"
    require_file(hooks_path, errors)
    require_file(script_path, errors)
    if not hooks_path.is_file():
        return
    payload = load_json(hooks_path)
    session_start = payload.get("hooks", {}).get("SessionStart")
    if not isinstance(session_start, list) or not session_start:
        errors.append("hooks/hooks.json must define hooks.SessionStart")
        return
    handler = session_start[0].get("hooks", [{}])[0]
    if handler.get("type") != "command":
        errors.append("hooks/hooks.json SessionStart handler must be a command hook")
    if "$PLUGIN_ROOT/hooks/session_start_context.py" not in handler.get("command", ""):
        errors.append("hooks/hooks.json must invoke session_start_context.py via PLUGIN_ROOT")


def validate_docs(errors: list[str]) -> None:
    for path in (
        "CODE_OF_CONDUCT.md",
        "CONTRIBUTING.md",
        "GOVERNANCE.md",
        "TRADEMARK.md",
        "DATA_CONTRACT.md",
        "docs/INSTALL.md",
        "docs/CLI.md",
        "docs/assets/jaq-site-preview.png",
        "docs/assets/jobqa-dry-run.gif",
        "docs/CODEX_PLUGIN.md",
        "docs/CODEX_APP.md",
        "docs/CLAUDE_PLUGIN.md",
        "docs/ENGINEERING_RULES.md",
        "docs/DOCUMENTATION_RULES.md",
        "docs/PUBLISHING.md",
        ".github/PULL_REQUEST_TEMPLATE.md",
        "bin/jobqa",
    ):
        require_file(ROOT / path, errors)


def validate_codex_taxonomy(errors: list[str]) -> None:
    """Keep public docs from marketing JAQ as a standalone Codex App."""
    checked_paths = (
        "README.md",
        "site/index.html",
        ".codex-plugin/plugin.json",
        "docs/INSTALL.md",
        "docs/PUBLISHING.md",
        "docs/ARCHITECTURE.md",
        "docs/RELEASE_PROCESS.md",
        "DATA_CONTRACT.md",
        "AGENTS.md",
    )
    forbidden = (
        "Codex App",
        "Codex app",
        "codex app",
        "Codex app/plugin",
        "Codex plugin/app",
        "Codex app package",
    )
    for relative_path in checked_paths:
        path = ROOT / relative_path
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in forbidden:
            if phrase in text:
                errors.append(
                    f"{relative_path} contains unsupported Codex taxonomy phrase: {phrase}"
                )


def validate_cli(errors: list[str]) -> None:
    cli_path = ROOT / "bin" / "jobqa"
    require_file(cli_path, errors)
    if cli_path.is_file() and not cli_path.stat().st_mode & 0o111:
        errors.append("bin/jobqa must be executable")
    require_file(ROOT / "scripts" / "jobqa.py", errors)
    require_file(ROOT / "examples" / "basic" / "candidate.json", errors)
    require_file(ROOT / "examples" / "basic" / "role.json", errors)
    require_file(ROOT / "examples" / "basic" / "artifacts" / "cv.txt", errors)


def validate_pages_site(errors: list[str]) -> None:
    for path in (
        ".github/workflows/pages.yml",
        "site/.nojekyll",
        "site/index.html",
        "site/styles.css",
        "site/script.js",
        "site/assets/icon.svg",
        "site/assets/logo.svg",
        "scripts/validate_site.py",
    ):
        require_file(ROOT / path, errors)


def validate() -> list[str]:
    errors: list[str] = []
    validate_codex_app(errors)
    validate_claude_plugin(errors)
    validate_repo_marketplace(errors)
    validate_hooks(errors)
    validate_docs(errors)
    validate_codex_taxonomy(errors)
    validate_cli(errors)
    validate_pages_site(errors)
    return errors


def main() -> None:
    fail(validate())
    print("PASS package metadata")


if __name__ == "__main__":
    main()
