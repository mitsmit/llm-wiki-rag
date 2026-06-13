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


def strip_frontmatter(content: str) -> str:
    """Remove YAML frontmatter for cleaner display."""
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            return content[end + 3:].lstrip()
    return content


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
        groups.get(t, groups["other"]).append({"path": path, "title": title})
    return groups


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
