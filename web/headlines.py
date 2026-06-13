"""Landing-page data: the most recently ingested wiki/sources/ pages.

Reads only `wiki/sources/*.md` frontmatter + the Summary section — exactly
what the CLAUDE.md INGEST workflow produces. A future scheduled ingestion
agent that drops new sources via that same workflow needs no changes here
for them to surface on the landing page.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

VAULT_ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = VAULT_ROOT / "wiki" / "sources"

SUMMARY_RE = re.compile(r"^##\s+Summary\s*\n+(.*?)(?:\n##|\Z)", re.DOTALL | re.MULTILINE)


def _parse_frontmatter(content: str) -> tuple[dict, str]:
    if not content.startswith("---"):
        return {}, content
    end = content.find("\n---", 3)
    if end == -1:
        return {}, content
    frontmatter = yaml.safe_load(content[3:end]) or {}
    body = content[end + 4:].lstrip("\n")
    return frontmatter, body


def _summary_excerpt(body: str, max_chars: int = 400) -> str:
    m = SUMMARY_RE.search(body)
    text = m.group(1).strip() if m else body.strip()
    paragraph = text.split("\n\n", 1)[0].strip()
    if len(paragraph) > max_chars:
        paragraph = paragraph[:max_chars].rsplit(" ", 1)[0] + "…"
    return paragraph


def get_headlines(limit: int = 10) -> list[dict]:
    """Return the `limit` most recently created wiki/sources/ pages, newest first."""
    items = []
    for f in SOURCES_DIR.glob("*.md"):
        content = f.read_text(encoding="utf-8")
        frontmatter, body = _parse_frontmatter(content)
        items.append({
            "slug": f.stem,
            "title": frontmatter.get("title", f.stem),
            "created": str(frontmatter.get("created", "")),
            "tags": frontmatter.get("tags") or [],
            "excerpt": _summary_excerpt(body),
            "page_path": f"wiki/sources/{f.name}",
        })
    items.sort(key=lambda item: item["created"], reverse=True)
    return items[:limit]
