"""Wiki-dump content helpers for the web UI.

Mirrors the page-loading/prompt helpers that previously lived in the
Streamlit app's "Query the Wiki" view, plus a page_tree() grouping used by
the sidebar API.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterator

from rag.generation import stream_chat
from rag.tracing import observe, update_current_span

VAULT_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = VAULT_ROOT / "wiki"
LOG_PATH = VAULT_ROOT / "log.md"

LOG_ENTRY_RE = re.compile(r"^## \[(\d{4}-\d{2}-\d{2})\]\s+(\S+)\s*\|\s*(.+?)\s*$", re.MULTILINE)
LOG_NOTES_RE = re.compile(r"\*\*Notes:\*\*\s*(.+?)(?:\n-\s*\*\*|\n---|\Z)", re.DOTALL)

SYSTEM_PROMPT = """\
You are the query agent for a personal LLM Wiki. The wiki contains structured markdown pages \
covering sources, concepts, entities, and analyses. All wiki pages are provided below.

When answering a question:
1. Identify which pages are relevant (cite them by path).
2. Synthesize an accurate, well-structured answer using only information in the wiki.
3. If the wiki doesn't contain enough information, say so clearly and suggest what source \
   types would help.
4. Format your answer in clean markdown: use headings, bullet points, and tables where helpful.
5. End with a **Sources used** section listing the wiki pages you drew from.

Be direct and precise. Do not pad answers."""


def load_all_pages() -> dict[str, str]:
    """Load every markdown page under wiki/ keyed by vault-root-relative path."""
    pages = {}
    for f in WIKI_DIR.rglob("*.md"):
        key = str(f.relative_to(VAULT_ROOT))
        pages[key] = f.read_text(encoding="utf-8")
    return pages


def page_title(content: str, fallback: str) -> str:
    """Extract first # heading or frontmatter title from a page."""
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("title:"):
            return line.split(":", 1)[1].strip().strip('"')
        if line.startswith("# ") and not line.startswith("---"):
            return line[2:].strip()
    return fallback


def page_type(content: str) -> str:
    m = re.search(r"^type:\s*(\S+)", content, re.MULTILINE)
    return m.group(1) if m else "other"


def page_tags(content: str) -> list[str]:
    """Extract the frontmatter `tags: [a, b, c]` list, if present."""
    m = re.search(r"^tags:\s*\[(.*?)\]", content, re.MULTILINE)
    if not m:
        return []
    return [t.strip().strip("'\"") for t in m.group(1).split(",") if t.strip()]


def strip_frontmatter(content: str) -> str:
    """Remove YAML frontmatter for cleaner display."""
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            return content[end + 3:].lstrip()
    return content


EXCERPT_RE = re.compile(r"^#{1,6}[ \t]+[^\n]*\n+(.*?)(?:\n#{1,6}[ \t]|\Z)", re.DOTALL | re.MULTILINE)
WIKILINK_DISPLAY_RE = re.compile(r"\[\[[^\]|]*\|([^\]]+)\]\]")
WIKILINK_PLAIN_RE = re.compile(r"\[\[([^\]]+)\]\]")
MD_EMPHASIS_RE = re.compile(r"[*_`]{1,3}")


def page_excerpt(content: str, max_chars: int = 200) -> str:
    """First paragraph of body text following the page's first heading
    (Definition, Overview, Summary, etc.), plain-texted and truncated."""
    body = strip_frontmatter(content)
    m = EXCERPT_RE.search(body)
    text = m.group(1).strip() if m else body.strip()
    paragraph = text.split("\n\n", 1)[0].strip()
    paragraph = WIKILINK_DISPLAY_RE.sub(r"\1", paragraph)
    paragraph = WIKILINK_PLAIN_RE.sub(r"\1", paragraph)
    paragraph = MD_EMPHASIS_RE.sub("", paragraph)
    if len(paragraph) > max_chars:
        paragraph = paragraph[:max_chars].rsplit(" ", 1)[0] + "…"
    return paragraph


def wiki_stats(pages: dict[str, str]) -> tuple[int, int]:
    sources = sum(1 for c in pages.values() if page_type(c) == "source")
    return sources, len(pages)


def page_tree(pages: dict[str, str]) -> dict[str, list[dict[str, str]]]:
    """Group pages by type for the sidebar, each with its display title."""
    groups: dict[str, list[dict[str, str]]] = {
        "source": [], "concept": [], "entity": [], "analysis": [], "other": []
    }
    for path, content in sorted(pages.items()):
        t = page_type(content)
        title = page_title(content, Path(path).stem.replace("-", " ").title())
        groups.get(t, groups["other"]).append({
            "path": path,
            "title": title,
            "tags": page_tags(content),
        })
    return groups


def parse_log_activity(limit: int = 5) -> list[dict]:
    """Parse log.md entries into a compact activity feed, newest first."""
    content = LOG_PATH.read_text(encoding="utf-8") if LOG_PATH.exists() else ""

    matches = list(LOG_ENTRY_RE.finditer(content))
    entries = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        block = content[m.end():end]
        note_m = LOG_NOTES_RE.search(block)
        note = " ".join(note_m.group(1).split()) if note_m else ""
        if len(note) > 220:
            note = note[:220].rsplit(" ", 1)[0] + "…"
        entries.append({
            "date": m.group(1),
            "operation": m.group(2),
            "title": m.group(3),
            "note": note,
        })

    entries.sort(key=lambda e: e["date"], reverse=True)
    return entries[:limit]


def append_to_index(line: str, section: str) -> None:
    """Insert `line` after `section`'s header in index.md (deduped), or
    append a new section block if `section` isn't present."""
    index_path = VAULT_ROOT / "index.md"
    content = index_path.read_text(encoding="utf-8")
    if line in content:
        return
    if section in content:
        content = content.replace(section, section + "\n" + line)
    else:
        content += f"\n{section}\n{line}\n"
    index_path.write_text(content, encoding="utf-8")


def build_context(pages: dict[str, str]) -> str:
    """Build a single context block from all wiki pages for the query prompt."""
    parts = []
    for path, content in sorted(pages.items()):
        parts.append(f"=== FILE: {path} ===\n{content}\n")
    return "\n".join(parts)


@observe(name="wiki_answer_stream", capture_input=False)
def stream_wiki_answer(query: str, pages: dict[str, str], history: list[dict], model: str) -> Iterator[str]:
    """Streaming wiki-dump answer: yields text deltas, then records the full
    answer on the current span once exhausted."""
    context = build_context(pages)
    user_prompt = f"""WIKI CONTENTS:\n\n{context}\n\n---\n\nQUESTION: {query}"""

    parts: list[str] = []
    for delta in stream_chat(SYSTEM_PROMPT, user_prompt, history, model):
        parts.append(delta)
        yield delta

    update_current_span(input={"query": query}, output="".join(parts))
