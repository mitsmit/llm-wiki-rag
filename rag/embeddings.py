"""Embed text chunks and queries using a local sentence-transformers model."""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-base-en-v1.5")

# BGE models are trained with an instruction prefix on the query side only
# (passages are embedded as-is).
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

_model: SentenceTransformer | None = None


def _get_model(model_name: str = EMBEDDING_MODEL) -> SentenceTransformer:
    """Lazily load (and cache) the embedding model. The first call downloads
    the model from Hugging Face if not already cached."""
    global _model
    if _model is None:
        _model = SentenceTransformer(model_name)
    return _model


def embed_texts(texts: list[str], model: str = EMBEDDING_MODEL) -> np.ndarray:
    """Embed a list of passages, returning an (N, dim) float32 array of
    L2-normalized vectors (so dot product == cosine similarity)."""
    if not texts:
        return np.empty((0, 0), dtype=np.float32)

    vectors = _get_model(model).encode(texts, normalize_embeddings=True, convert_to_numpy=True)
    return vectors.astype(np.float32)


def embed_query(query: str, model: str = EMBEDDING_MODEL) -> np.ndarray:
    return embed_texts([QUERY_PREFIX + query], model=model)[0]
