"""
Local hybrid RAG module for the llm-wiki vault.

Indexes markdown pages under wiki/ and source documents (markdown + PDF)
under raw/, embeds them with the OpenAI embeddings API, and stores the
result as a local numpy-backed vector index. Retrieval combines embedding
similarity with BM25 keyword search via reciprocal rank fusion.

One-off usage:

    from rag import build_index, retrieve

    build_index()                              # (re)index changed files under wiki/ and raw/
    for chunk in retrieve("how does RoPE work?", k=5):
        print(f"{chunk.score:.3f}  {chunk.path}  ({chunk.title})")
        print(chunk.text)

Long-lived process (e.g. a Streamlit app) — load the index once and reuse it:

    from rag import VectorStore, DEFAULT_INDEX_DIR, retrieve_from_store

    store = VectorStore.load(DEFAULT_INDEX_DIR)
    store.ensure_bm25()
    results = retrieve_from_store(store, "how does RoPE work?", k=5)

Re-running build_index() only re-embeds files whose content has changed
since the last run.

To sharpen the top results, rerank hybrid-search candidates with a
cross-encoder:

    from rag import rerank

    candidates = retrieve_from_store(store, query, k=20)
    top = rerank(query, candidates, top_n=8)
"""

from .generation import RAG_SYSTEM_PROMPT, build_rag_context, generate_answer
from .index import DEFAULT_INDEX_DIR, build_index
from .rerank import rerank
from .retrieve import RetrievedChunk, retrieve, retrieve_from_store
from .store import VectorStore

__all__ = [
    "build_index",
    "retrieve",
    "retrieve_from_store",
    "rerank",
    "RetrievedChunk",
    "VectorStore",
    "DEFAULT_INDEX_DIR",
    "RAG_SYSTEM_PROMPT",
    "build_rag_context",
    "generate_answer",
]
