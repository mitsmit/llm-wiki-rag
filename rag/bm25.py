"""Minimal Okapi BM25 index for keyword-based retrieval over chunk text."""

from __future__ import annotations

import math
import re
from collections import Counter

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


class BM25Index:
    """Okapi BM25 over a fixed corpus of documents (chunk texts)."""

    def __init__(self, documents: list[str], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.doc_freqs: list[Counter] = []
        self.doc_lens: list[int] = []
        df: Counter = Counter()

        for doc in documents:
            freqs = Counter(tokenize(doc))
            self.doc_freqs.append(freqs)
            self.doc_lens.append(sum(freqs.values()))
            for term in freqs:
                df[term] += 1

        self.n_docs = len(documents)
        self.avg_doc_len = (sum(self.doc_lens) / self.n_docs) if self.n_docs else 0.0
        self.idf = {
            term: math.log(1 + (self.n_docs - freq + 0.5) / (freq + 0.5))
            for term, freq in df.items()
        }

    def top_k(self, query: str, k: int) -> list[tuple[int, float]]:
        """Return up to `k` (doc_index, score) pairs with score > 0, best first."""
        scores = [0.0] * self.n_docs

        for term in set(tokenize(query)):
            idf = self.idf.get(term)
            if not idf:
                continue
            for i, (freqs, doc_len) in enumerate(zip(self.doc_freqs, self.doc_lens)):
                f = freqs.get(term, 0)
                if f == 0:
                    continue
                denom = f + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_len)
                scores[i] += idf * (f * (self.k1 + 1)) / denom

        ranked = sorted(
            (i for i, s in enumerate(scores) if s > 0),
            key=lambda i: scores[i],
            reverse=True,
        )
        return [(i, scores[i]) for i in ranked[:k]]
