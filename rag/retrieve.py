"""Retrieve the most relevant wiki/raw chunks for a query.

Uses hybrid search: embedding (cosine similarity) results and BM25 keyword
results are each fetched, then fused with reciprocal rank fusion.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .embeddings import embed_query
from .index import DEFAULT_INDEX_DIR
from .store import VectorStore


@dataclass
class RetrievedChunk:
    text: str
    path: str
    title: str
    doc_type: str
    tags: list[str]
    chunk_index: int
    score: float
    rerank_score: float | None = None


def _to_retrieved_chunks(results: list[tuple[dict, float]]) -> list[RetrievedChunk]:
    """Convert raw (chunk, score) hits into RetrievedChunks, dropping any hit
    that lacks a source path or text — every returned chunk must be
    traceable to a citable wiki/raw document."""
    return [
        RetrievedChunk(
            text=chunk["text"],
            path=chunk["path"],
            title=chunk["title"],
            doc_type=chunk["doc_type"],
            tags=chunk["tags"],
            chunk_index=chunk["chunk_index"],
            score=score,
        )
        for chunk, score in results
        if chunk.get("path") and chunk.get("text")
    ]


def retrieve_from_store(store: VectorStore, query: str, k: int = 5, fetch_k: int = 20) -> list[RetrievedChunk]:
    """Hybrid retrieval against an already-loaded VectorStore.

    Useful for long-lived processes (e.g. a Streamlit app) that want to load
    the index once and reuse it across many queries.
    """
    if not store.chunks:
        return []
    query_vec = embed_query(query)
    return _to_retrieved_chunks(store.hybrid_search(query, query_vec, k=k, fetch_k=fetch_k))


def retrieve(query: str, k: int = 5, index_dir: Path = DEFAULT_INDEX_DIR, fetch_k: int = 20) -> list[RetrievedChunk]:
    """Return the top-k chunks most similar to `query` via hybrid search.

    Requires `build_index()` to have been run at least once. Loads the index
    fresh from disk each call; for repeated queries in a long-lived process,
    load a VectorStore once and use `retrieve_from_store` instead.
    """
    store = VectorStore.load(index_dir)
    return retrieve_from_store(store, query, k=k, fetch_k=fetch_k)
