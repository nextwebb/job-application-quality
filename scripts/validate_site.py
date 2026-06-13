#!/usr/bin/env python3
"""Validate the static GitHub Pages site without external dependencies."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

from common import fail


ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
INDEX = SITE / "index.html"
FORBIDDEN_MARKERS = (
    "X-Goog-Api-Key",
    "stitch.googleapis.com",
    "mcp_servers.stitch",
)


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.local_refs: list[str] = []
        self.anchor_refs: list[str] = []
        self.has_main = False
        self.has_h1 = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {name: value for name, value in attrs}
        element_id = data.get("id")
        if element_id:
            self.ids.add(element_id)
        if tag == "main":
            self.has_main = True
        if tag == "h1":
            self.has_h1 = True

        for attr in ("href", "src"):
            value = data.get(attr)
            if not value:
                continue
            if value.startswith("#"):
                self.anchor_refs.append(value[1:])
                continue
            parsed = urlparse(value)
            if parsed.scheme or value.startswith("mailto:"):
                continue
            if parsed.path:
                self.local_refs.append(parsed.path)


def validate() -> list[str]:
    errors: list[str] = []
    required = (
        "index.html",
        "styles.css",
        "script.js",
        ".nojekyll",
        "assets/icon.svg",
        "assets/logo.svg",
    )
    for relative in required:
        if not (SITE / relative).is_file():
            errors.append(f"missing site/{relative}")

    if not INDEX.is_file():
        return errors

    html = INDEX.read_text(encoding="utf-8")
    for marker in FORBIDDEN_MARKERS:
        if marker in html:
            errors.append(f"forbidden secret/config marker leaked into site: {marker}")

    parser = SiteParser()
    parser.feed(html)
    if not parser.has_main:
        errors.append("site/index.html missing <main>")
    if not parser.has_h1:
        errors.append("site/index.html missing <h1>")

    for anchor in parser.anchor_refs:
        if anchor and anchor not in parser.ids:
            errors.append(f"site/index.html links to missing anchor #{anchor}")

    for ref in parser.local_refs:
        if ref.startswith("/"):
            errors.append(f"site/index.html uses root-relative local reference: {ref}")
            continue
        if not (SITE / ref).is_file():
            errors.append(f"site/index.html links to missing local file: {ref}")

    return errors


def main() -> None:
    fail(validate())
    print("PASS site validation")


if __name__ == "__main__":
    main()
