from __future__ import annotations

import json
import os
from typing import Iterator

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from rag import DEFAULT_INDEX_DIR, VectorStore, build_index, rerank, retrieve_from_store, stream_rag_answer
from rag.tracing import trace_attributes

from ..wiki_data import build_context, load_all_pages, stream_wiki_answer, wiki_stats

router = APIRouter()

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")


class ChatMessage(BaseModel):
    role: str
    content: str


class QueryRequest(BaseModel):
    question: str
    session_id: str
    history: list[ChatMessage] = []


def _ndjson(obj: dict) -> str:
    return json.dumps(obj) + "\n"


@router.post("/api/query/wiki")
def query_wiki(req: QueryRequest) -> StreamingResponse:
    history = [m.model_dump() for m in req.history]

    def gen() -> Iterator[str]:
        try:
            with trace_attributes(session_id=req.session_id, tags=["view:query"]):
                pages = load_all_pages()
                for delta in stream_wiki_answer(req.question, pages, history, MODEL):
                    yield _ndjson({"type": "token", "data": delta})
            yield _ndjson({"type": "done"})
        except Exception as e:
            yield _ndjson({"type": "error", "data": str(e)})

    return StreamingResponse(gen(), media_type="application/x-ndjson")


@router.post("/api/query/rag")
def query_rag(req: QueryRequest, request: Request) -> StreamingResponse:
    history = [m.model_dump() for m in req.history]
    store: VectorStore = request.app.state.rag_store

    def gen() -> Iterator[str]:
        try:
            with trace_attributes(session_id=req.session_id, tags=["view:rag"]):
                candidates = retrieve_from_store(store, req.question, k=20)
                retrieved = rerank(req.question, candidates, top_n=8)
                yield _ndjson({
                    "type": "excerpts",
                    "data": [
                        {
                            "path": c.path,
                            "title": c.title,
                            "score": round(c.score, 4),
                            "rerank_score": round(c.rerank_score, 4) if c.rerank_score is not None else None,
                        }
                        for c in retrieved
                    ],
                })
                for delta in stream_rag_answer(req.question, retrieved, history, MODEL):
                    yield _ndjson({"type": "token", "data": delta})
            yield _ndjson({"type": "done"})
        except Exception as e:
            yield _ndjson({"type": "error", "data": str(e)})

    return StreamingResponse(gen(), media_type="application/x-ndjson")


@router.post("/api/reindex")
def reindex(request: Request) -> dict:
    summary = build_index()
    store = VectorStore.load(DEFAULT_INDEX_DIR)
    store.ensure_bm25()
    request.app.state.rag_store = store

    pages = load_all_pages()
    sources, total = wiki_stats(pages)
    return {"status": "ok", "sources": sources, "pages": total, **summary}
