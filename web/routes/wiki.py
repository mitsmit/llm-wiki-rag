from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException

from ..wiki_data import (
    VAULT_ROOT,
    load_all_pages,
    page_excerpt,
    page_tags,
    page_title,
    page_tree,
    page_type,
    parse_log_activity,
    strip_frontmatter,
    wiki_stats,
)

router = APIRouter()


@router.get("/api/wiki/stats")
def stats() -> dict:
    pages = load_all_pages()
    sources, total = wiki_stats(pages)
    return {"sources": sources, "pages": total}


@router.get("/api/wiki/pages")
def pages_tree() -> dict:
    pages = load_all_pages()
    overview = "wiki/overview.md"
    return {
        "overview": overview if overview in pages else None,
        "groups": page_tree({k: v for k, v in pages.items() if k != overview}),
    }


@router.get("/api/wiki/page/{path:path}")
def page(path: str) -> dict:
    pages = load_all_pages()
    if path not in pages:
        raise HTTPException(status_code=404, detail=f"Page not found: {path}")
    content = pages[path]
    title = page_title(content, Path(path).stem.replace("-", " ").title())
    return {
        "path": path,
        "title": title,
        "type": page_type(content),
        "tags": page_tags(content),
        "excerpt": page_excerpt(content),
        "content": strip_frontmatter(content),
    }


@router.get("/api/wiki/log")
def log() -> dict:
    log_path = VAULT_ROOT / "log.md"
    content = log_path.read_text(encoding="utf-8") if log_path.exists() else ""
    return {"content": content}


@router.get("/api/wiki/activity")
def activity(limit: int = 5) -> list[dict]:
    return parse_log_activity(limit=limit)
