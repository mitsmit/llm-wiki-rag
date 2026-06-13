"""Research-agent endpoints: streaming research runs, history of past
sessions, and pushing selected reading-list items into raw/ for the wiki's
INGEST workflow."""

from __future__ import annotations

import json
import queue
import re
import threading
from datetime import date
from typing import Iterator

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from ..research_bridge import dedup, fetch, parse, research_agent

router = APIRouter()


class ResearchRequest(BaseModel):
    query: str
    save: bool = True


class ReadingItem(BaseModel):
    title: str
    source: str | None = None
    authors: str | None = None
    date: str | None = None
    url: str | None = None
    type: str | None = None
    why_read_it: str | None = None


class SelectRequest(BaseModel):
    items: list[ReadingItem]
    query: str = "research"


def _ndjson(obj: dict) -> str:
    return json.dumps(obj) + "\n"


@router.post("/api/research")
def run_research(req: ResearchRequest) -> StreamingResponse:
    def gen() -> Iterator[str]:
        chunks: queue.Queue = queue.Queue()
        errors: list[str] = []

        def on_chunk(chunk: str) -> None:
            chunks.put(chunk)

        def run() -> None:
            try:
                research_agent.research(req.query, save=req.save, on_stream=on_chunk)
            except Exception as e:
                errors.append(str(e))
            finally:
                chunks.put(None)

        yield _ndjson({"type": "status", "data": "Expanding query and searching arXiv + web…"})

        thread = threading.Thread(target=run, daemon=True)
        thread.start()

        full_text = ""
        while True:
            chunk = chunks.get()
            if chunk is None:
                break
            full_text += chunk
            yield _ndjson({"type": "token", "data": chunk})

        if errors:
            yield _ndjson({"type": "error", "data": errors[0]})
            return

        yield _ndjson({"type": "items", "data": parse.parse_reading_list(full_text)})
        yield _ndjson({"type": "done"})

    return StreamingResponse(gen(), media_type="application/x-ndjson")


@router.get("/api/research/history")
def research_history() -> list[dict]:
    """Past research sessions (results/*.md), newest first."""
    files = sorted(research_agent.RESULTS_DIR.glob("*.md"), reverse=True)
    return [
        {"name": f.name, "label": f.stem[11:].replace("-", " ").title(), "date": f.stem[:10]}
        for f in files[:20]
    ]


@router.get("/api/research/result/{name}")
def research_result(name: str) -> dict:
    """Load a past result and its parsed reading-list items."""
    results_dir = research_agent.RESULTS_DIR.resolve()
    path = (results_dir / name).resolve()
    if path.parent != results_dir or path.suffix != ".md" or not path.is_file():
        raise HTTPException(status_code=404, detail="Result not found")
    content = path.read_text(encoding="utf-8")
    return {"name": name, "content": content, "items": parse.parse_reading_list(content)}


@router.post("/api/research/select")
def research_select(req: SelectRequest) -> dict:
    """Pull selected reading-list items into raw/: arXiv items as PDFs,
    everything else as a combined 'list of sources' file for INGEST."""
    added, skipped, non_arxiv = [], [], []
    for item in req.items:
        url = item.url or ""
        if fetch.is_arxiv_url(url):
            try:
                path = fetch.fetch_arxiv_pdf(url)
                added.append(f"raw/{path.name}")
            except Exception as e:
                skipped.append(f"{item.title} ({e})")
        else:
            non_arxiv.append(item)

    if non_arxiv:
        slug = re.sub(r"[^a-z0-9]+", "-", req.query.lower())[:40].strip("-")
        dest = dedup.WIKI_RAW / f"{date.today().isoformat()}-{slug}-selected.md"
        blocks = "\n\n".join(parse.render_item(item.model_dump()) for item in non_arxiv)
        dest.write_text(f"# Selected reading list\n\n{blocks}\n", encoding="utf-8")
        added.append(f"raw/{dest.name}")

    return {"added": added, "skipped": skipped}
