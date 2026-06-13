"""Cross-encoder reranking for retrieved chunks.

Hybrid (embedding + BM25) search is good at recall but its scores aren't
directly comparable across chunks. A cross-encoder scores each (query, chunk)
pair jointly, giving a much sharper relevance signal for the final top-k.
"""

from __future__ import annotations

from dataclasses import replace

from sentence_transformers import CrossEncoder

from .retrieve import RetrievedChunk

DEFAULT_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

_model: CrossEncoder | None = None


def _get_model(model_name: str = DEFAULT_MODEL) -> CrossEncoder:
    """Lazily load (and cache) the cross-encoder model. The first call
    downloads the model (~90MB) from Hugging Face if not already cached."""
    global _model
    if _model is None:
        _model = CrossEncoder(model_name)
    return _model


def rerank(
    query: str, chunks: list[RetrievedChunk], top_n: int | None = None, model_name: str = DEFAULT_MODEL
) -> list[RetrievedChunk]:
    """Re-score `chunks` against `query` with a cross-encoder and return them
    sorted by `rerank_score` (descending), optionally truncated to `top_n`."""
    if not chunks:
        return []

    model = _get_model(model_name)
    scores = model.predict([(query, c.text) for c in chunks])

    reranked = sorted(
        (replace(c, rerank_score=float(s)) for c, s in zip(chunks, scores)),
        key=lambda c: c.rerank_score,
        reverse=True,
    )
    return reranked[:top_n] if top_n is not None else reranked
