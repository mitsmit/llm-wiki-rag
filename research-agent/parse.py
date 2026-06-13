"""Parse the research agent's markdown reading-list output (format defined
in CLAUDE.md's Output Format section) into structured items, so a selection
UI can render checkboxes and pass chosen urls straight to `fetch.fetch_to_raw`.
"""

from __future__ import annotations

import re

ITEM_RE = re.compile(
    r"^###\s*\d+\.\s*(?P<title>.+?)\s*\n(?P<body>(?:-\s*\*\*.+\n?)+)",
    re.MULTILINE,
)
FIELD_RE = re.compile(r"-\s*\*\*(?P<key>[^*]+?):\*\*\s*(?P<value>.+)")
LINK_RE = re.compile(r"\[([^\]]*)\]\((https?://[^\)\s]+)\)")

KEY_ALIASES = {
    "author(s)": "authors",
    "link": "url",
    "why read it": "why_read_it",
}


def parse_reading_list(markdown: str) -> list[dict]:
    """Extract each numbered reading-list item as a dict with (where present)
    title, source, authors, date, url, type, and why_read_it."""
    items = []
    for m in ITEM_RE.finditer(markdown):
        item = {"title": m.group("title").strip()}
        for fm in FIELD_RE.finditer(m.group("body")):
            key = KEY_ALIASES.get(fm.group("key").strip().lower(), fm.group("key").strip().lower())
            value = fm.group("value").strip()
            if key == "url":
                link_m = LINK_RE.search(value)
                value = link_m.group(2) if link_m else value
            item[key] = value
        items.append(item)
    return items


def render_item(item: dict) -> str:
    """Render a parsed item back into a CLAUDE.md-style reading-list block,
    for writing selected non-arXiv items into raw/ as a "list of sources"
    file the wiki agent can follow via their **Link:** urls."""
    lines = [f"### {item['title']}"]
    for key, label in (("source", "Source"), ("authors", "Author(s)"), ("date", "Date")):
        if item.get(key):
            lines.append(f"- **{label}:** {item[key]}")
    if item.get("url"):
        lines.append(f"- **Link:** [{item.get('source', 'link')}]({item['url']})")
    for key, label in (("type", "Type"), ("why_read_it", "Why read it")):
        if item.get(key):
            lines.append(f"- **{label}:** {item[key]}")
    return "\n".join(lines)


if __name__ == "__main__":
    import json
    import sys

    text = sys.stdin.read() if len(sys.argv) < 2 else open(sys.argv[1], encoding="utf-8").read()
    print(json.dumps(parse_reading_list(text), indent=2, ensure_ascii=False))
