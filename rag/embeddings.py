"""Embed text chunks and queries using the OpenAI embeddings API."""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

from .tracing import get_openai_client

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
_BATCH_SIZE = 100

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = get_openai_client()
    return _client


def embed_texts(texts: list[str], model: str = EMBEDDING_MODEL) -> np.ndarray:
    """Embed a list of texts, returning an (N, dim) float32 array of
    L2-normalized vectors (so dot product == cosine similarity)."""
    if not texts:
        return np.empty((0, 0), dtype=np.float32)

    client = _get_client()
    vectors: list[list[float]] = []
    for i in range(0, len(texts), _BATCH_SIZE):
        batch = texts[i:i + _BATCH_SIZE]
        response = client.embeddings.create(model=model, input=batch)
        vectors.extend(item.embedding for item in response.data)

    arr = np.array(vectors, dtype=np.float32)
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return arr / norms


def embed_query(query: str, model: str = EMBEDDING_MODEL) -> np.ndarray:
    return embed_texts([query], model=model)[0]
