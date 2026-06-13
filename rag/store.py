"""Local persistence and similarity search for embedded wiki/raw chunks."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .bm25 import BM25Index
from .tracing import observe, update_current_span

EMBEDDINGS_FILE = "embeddings.npy"
CHUNKS_FILE = "chunks.jsonl"
MANIFEST_FILE = "manifest.json"

RRF_K = 60  # standard reciprocal rank fusion constant


@dataclass
class VectorStore:
    chunks: list[dict] = field(default_factory=list)
    embeddings: np.ndarray = field(default_factory=lambda: np.empty((0, 0), dtype=np.float32))
    manifest: dict = field(default_factory=dict)  # path -> {"hash": ..., "chunk_count": ...}
    _bm25: BM25Index | None = field(default=None, repr=False, compare=False)

    @classmethod
    def load(cls, index_dir: Path) -> "VectorStore":
        chunks_path = index_dir / CHUNKS_FILE
        embeddings_path = index_dir / EMBEDDINGS_FILE
        manifest_path = index_dir / MANIFEST_FILE

        if not (chunks_path.exists() and embeddings_path.exists()):
            return cls()

        chunks = [
            json.loads(line)
            for line in chunks_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        embeddings = np.load(embeddings_path)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
        return cls(chunks=chunks, embeddings=embeddings, manifest=manifest)

    def save(self, index_dir: Path) -> None:
        index_dir.mkdir(parents=True, exist_ok=True)
        with open(index_dir / CHUNKS_FILE, "w", encoding="utf-8") as f:
            for chunk in self.chunks:
                f.write(json.dumps(chunk) + "\n")
        np.save(index_dir / EMBEDDINGS_FILE, self.embeddings)
        with open(index_dir / MANIFEST_FILE, "w", encoding="utf-8") as f:
            json.dump(self.manifest, f, indent=2)

    def remove_path(self, path: str) -> None:
        """Drop all chunks (and their embedding rows) belonging to `path`."""
        keep_idx = [i for i, c in enumerate(self.chunks) if c["path"] != path]
        if len(keep_idx) != len(self.chunks):
            self.chunks = [self.chunks[i] for i in keep_idx]
            self.embeddings = self.embeddings[keep_idx]
        self.manifest.pop(path, None)

    def add(self, chunks: list[dict], embeddings: np.ndarray, path: str, content_hash: str) -> None:
        self.chunks.extend(chunks)
        if self.embeddings.size == 0:
            self.embeddings = embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, embeddings])
        self.manifest[path] = {"hash": content_hash, "chunk_count": len(chunks)}

    def search(self, query_vec: np.ndarray, k: int = 5) -> list[tuple[dict, float]]:
        """Pure embedding (cosine similarity) search."""
        if self.embeddings.size == 0:
            return []
        scores = self.embeddings @ query_vec
        top_idx = np.argsort(-scores)[:k]
        return [(self.chunks[i], float(scores[i])) for i in top_idx]

    def ensure_bm25(self) -> BM25Index:
        """Lazily build (and cache) the BM25 index over chunk text."""
        if self._bm25 is None:
            self._bm25 = BM25Index([c["text"] for c in self.chunks])
        return self._bm25

    @observe(name="hybrid_search", capture_input=False, capture_output=False)
    def hybrid_search(
        self, query: str, query_vec: np.ndarray, k: int = 5, fetch_k: int = 20
    ) -> list[tuple[dict, float]]:
        """Combine embedding similarity and BM25 keyword search via reciprocal
        rank fusion (RRF), returning the top-k chunks by fused score."""
        if not self.chunks:
            return []

        embedding_ranked = [int(i) for i in np.argsort(-(self.embeddings @ query_vec))[:fetch_k]]
        bm25_ranked = [i for i, _ in self.ensure_bm25().top_k(query, fetch_k)]

        rrf_scores: dict[int, float] = {}
        for rank, idx in enumerate(embedding_ranked):
            rrf_scores[idx] = rrf_scores.get(idx, 0.0) + 1.0 / (RRF_K + rank + 1)
        for rank, idx in enumerate(bm25_ranked):
            rrf_scores[idx] = rrf_scores.get(idx, 0.0) + 1.0 / (RRF_K + rank + 1)

        ranked = sorted(rrf_scores.items(), key=lambda kv: kv[1], reverse=True)[:k]
        update_current_span(
            input={"query": query, "k": k, "fetch_k": fetch_k},
            output=[{"path": self.chunks[i]["path"], "rrf_score": round(score, 4)} for i, score in ranked],
        )
        return [(self.chunks[i], score) for i, score in ranked]
