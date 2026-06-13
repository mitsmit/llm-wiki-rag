import streamlit as st
import openai
import os
import re
from pathlib import Path
from dotenv import load_dotenv

from rag import (
    DEFAULT_INDEX_DIR,
    RAG_SYSTEM_PROMPT,
    RetrievedChunk,
    VectorStore,
    build_rag_context,
    rerank,
    retrieve_from_store,
)

# Load .env from project root (works whether launched from root or a subdirectory)
load_dotenv(Path(__file__).parent / ".env")

# ── Config ────────────────────────────────────────────────────────────────────

WIKI_ROOT  = Path(__file__).parent
WIKI_DIR   = WIKI_ROOT / "wiki"
MODEL      = os.getenv("OPENAI_MODEL", "gpt-4o")
RAW_DIR   = WIKI_ROOT / "raw"

st.set_page_config(
    page_title="LLM Wiki",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Helpers ───────────────────────────────────────────────────────────────────

@st.cache_data(ttl=30)
def load_all_pages() -> dict[str, str]:
    """Load every markdown page under wiki/ keyed by relative path."""
    pages = {}
    for f in WIKI_DIR.rglob("*.md"):
        key = str(f.relative_to(WIKI_ROOT))
        pages[key] = f.read_text(encoding="utf-8")
    return pages

@st.cache_data(ttl=30)
def load_index() -> str:
    p = WIKI_ROOT / "index.md"
    return p.read_text(encoding="utf-8") if p.exists() else ""

@st.cache_data(ttl=30)
def load_log_tail(n: int = 10) -> str:
    p = WIKI_ROOT / "log.md"
    if not p.exists():
        return ""
    lines = p.read_text(encoding="utf-8").splitlines()
    entries = [l for l in lines if l.startswith("## [")]
    return "\n".join(entries[-n:])

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

def wiki_stats(pages: dict) -> tuple[int, int]:
    sources   = sum(1 for c in pages.values() if page_type(c) == "source")
    total     = len(pages)
    return sources, total

@st.cache_resource
def load_rag_store() -> VectorStore:
    """Load the hybrid (embedding + BM25) RAG index once per server process."""
    store = VectorStore.load(DEFAULT_INDEX_DIR)
    store.ensure_bm25()
    return store

def build_context(pages: dict) -> str:
    """Build a single context block from all wiki pages for the query prompt."""
    parts = []
    for path, content in sorted(pages.items()):
        parts.append(f"=== FILE: {path} ===\n{content}\n")
    return "\n".join(parts)

# ── Sidebar ───────────────────────────────────────────────────────────────────

def render_sidebar(pages: dict):
    st.sidebar.title("📖 LLM Wiki")

    n_sources, n_pages = wiki_stats(pages)
    st.sidebar.markdown(
        f"<div style='font-size:0.85rem;color:gray'>{n_sources} sources · {n_pages} pages</div>",
        unsafe_allow_html=True,
    )
    st.sidebar.divider()

    # Group pages by type
    groups: dict[str, list[tuple[str, str]]] = {
        "source": [], "concept": [], "entity": [], "analysis": [], "other": []
    }
    for path, content in sorted(pages.items()):
        t = page_type(content)
        title = page_title(content, Path(path).stem.replace("-", " ").title())
        groups.get(t, groups["other"]).append((path, title))

    labels = {
        "source": "📄 Sources",
        "concept": "💡 Concepts",
        "entity": "🏢 Entities",
        "analysis": "🔬 Analyses",
        "other": "📝 Other",
    }

    # Overview shortcut
    overview_path = "wiki/overview.md"
    if overview_path in pages:
        if st.sidebar.button("🗺️ Overview", use_container_width=True):
            st.session_state.view = "browse"
            st.session_state.open_page = overview_path

    for group_key, group_label in labels.items():
        items = groups.get(group_key, [])
        if not items:
            continue
        st.sidebar.markdown(f"**{group_label}**")
        for path, title in items:
            if st.sidebar.button(title, key=f"nav_{path}", use_container_width=True):
                st.session_state.view = "browse"
                st.session_state.open_page = path

    st.sidebar.divider()
    col1, col2, col3 = st.sidebar.columns(3)
    if col1.button("🔍 Query", use_container_width=True):
        st.session_state.view = "query"
    if col2.button("🧪 RAG", use_container_width=True):
        st.session_state.view = "rag_query"
    if col3.button("📋 Log", use_container_width=True):
        st.session_state.view = "log"

# ── Query view ────────────────────────────────────────────────────────────────

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

def render_query_view(pages: dict):
    st.title("🔍 Query the Wiki")
    st.caption("Ask anything. The answer is synthesized from your wiki pages.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Render history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    query = st.chat_input("Ask a question about your wiki…")
    if not query:
        return

    # Show user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Build prompt
    context = build_context(pages)
    user_prompt = f"""WIKI CONTENTS:\n\n{context}\n\n---\n\nQUESTION: {query}"""

    # Stream response
    client = openai.OpenAI()
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        stream = client.chat.completions.create(
            model=MODEL,
            max_tokens=2048,
            stream=True,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *[{"role": m["role"], "content": m["content"]}
                  for m in st.session_state.messages[:-1]
                  if m["role"] == "assistant"],
                {"role": "user", "content": user_prompt},
            ],
        )
        for chunk in stream:
            text = chunk.choices[0].delta.content or ""
            full_response += text
            response_placeholder.markdown(full_response + "▌")
        response_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Offer to save as analysis
    with st.expander("💾 Save this answer as a wiki analysis page?"):
        slug = st.text_input("Filename slug (e.g. agi-timelines-comparison)", key="save_slug")
        if st.button("Save to wiki/analyses/", key="save_btn"):
            if slug:
                save_analysis(slug, query, full_response)
                st.success(f"Saved to wiki/analyses/{slug}.md")
                st.cache_data.clear()

def save_analysis(slug: str, query: str, answer: str):
    from datetime import date
    today = date.today().isoformat()
    path = WIKI_DIR / "analyses" / f"{slug}.md"
    content = f"""---
title: "{query[:80]}"
type: analysis
tags: []
sources: []
created: {today}
updated: {today}
---

## Query

{query}

## Answer

{answer}
"""
    path.write_text(content, encoding="utf-8")

    # Append to log
    log_path = WIKI_ROOT / "log.md"
    entry = f"\n## [{today}] query | {slug}\n\n- **Operation:** query\n- **Pages touched:** wiki/analyses/{slug}.md\n- **Notes:** Query: \"{query[:100]}\"\n"
    with open(log_path, "a") as f:
        f.write(entry)

    # Update index
    _append_to_index(f"- [{query[:60]}](wiki/analyses/{slug}.md) — query filed {today}", "## Analyses")

def _append_to_index(line: str, section: str):
    index_path = WIKI_ROOT / "index.md"
    content = index_path.read_text(encoding="utf-8")
    if line in content:
        return
    if section in content:
        content = content.replace(
            section,
            section + "\n" + line,
        )
    else:
        content += f"\n{section}\n{line}\n"
    index_path.write_text(content, encoding="utf-8")

# ── RAG query view ────────────────────────────────────────────────────────────

def render_rag_query_view():
    st.title("🧪 RAG Query (hybrid retrieval)")
    st.caption("Ask anything. The answer is synthesized from the top retrieved excerpts (wiki/ + raw/) via embedding + BM25 hybrid search.")

    if "rag_messages" not in st.session_state:
        st.session_state.rag_messages = []

    # Render history
    for msg in st.session_state.rag_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    query = st.chat_input("Ask a question (hybrid RAG)…", key="rag_chat_input")
    if not query:
        return

    # Show user message
    st.session_state.rag_messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Retrieve a wider candidate pool (hybrid: embeddings + BM25), then
    # cross-encoder rerank down to the final top-k for the prompt
    store = load_rag_store()
    candidates = retrieve_from_store(store, query, k=20)
    retrieved = rerank(query, candidates, top_n=8)
    context = build_rag_context(retrieved)
    user_prompt = f"""RETRIEVED EXCERPTS:\n\n{context}\n\n---\n\nQUESTION: {query}"""

    # Stream response
    client = openai.OpenAI()
    with st.chat_message("assistant"):
        if retrieved:
            with st.expander(f"📎 {len(retrieved)} retrieved excerpts"):
                for c in retrieved:
                    st.markdown(
                        f"- `{c.path}` — {c.title} "
                        f"(rerank {c.rerank_score:.3f}, hybrid {c.score:.3f})"
                    )

        response_placeholder = st.empty()
        full_response = ""
        stream = client.chat.completions.create(
            model=MODEL,
            max_tokens=2048,
            stream=True,
            messages=[
                {"role": "system", "content": RAG_SYSTEM_PROMPT},
                *[{"role": m["role"], "content": m["content"]}
                  for m in st.session_state.rag_messages[:-1]
                  if m["role"] == "assistant"],
                {"role": "user", "content": user_prompt},
            ],
        )
        for chunk in stream:
            text = chunk.choices[0].delta.content or ""
            full_response += text
            response_placeholder.markdown(full_response + "▌")
        response_placeholder.markdown(full_response)

    st.session_state.rag_messages.append({"role": "assistant", "content": full_response})

# ── Browse view ───────────────────────────────────────────────────────────────

def render_browse_view(pages: dict):
    path = st.session_state.get("open_page")
    if not path or path not in pages:
        st.title("Browse")
        st.info("Select a page from the sidebar.")
        return

    content = pages[path]
    title   = page_title(content, Path(path).stem.replace("-", " ").title())
    ptype   = page_type(content)

    type_badge = {
        "source": "📄 Source", "concept": "💡 Concept",
        "entity": "🏢 Entity", "analysis": "🔬 Analysis",
    }.get(ptype, "📝")

    st.title(title)
    st.caption(f"{type_badge}  ·  `{path}`")
    st.divider()
    st.markdown(strip_frontmatter(content))

# ── Log view ──────────────────────────────────────────────────────────────────

def render_log_view():
    st.title("📋 Operation Log")
    log_path = WIKI_ROOT / "log.md"
    if not log_path.exists():
        st.info("No log yet.")
        return
    st.markdown(log_path.read_text(encoding="utf-8"))

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if "view" not in st.session_state:
        st.session_state.view = "query"
    if "open_page" not in st.session_state:
        st.session_state.open_page = None

    pages = load_all_pages()
    render_sidebar(pages)

    view = st.session_state.view
    if view == "query":
        render_query_view(pages)
    elif view == "rag_query":
        render_rag_query_view()
    elif view == "browse":
        render_browse_view(pages)
    elif view == "log":
        render_log_view()

if __name__ == "__main__":
    main()
