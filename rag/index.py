"""Build and incrementally update the local vector index over wiki/ and raw/."""

from __future__ import annotations

from pathlib import Path

from .chunking import chunk_text
from .embeddings import embed_texts
from .loaders import load_documents
from .store import VectorStore

VAULT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INDEX_DIR = Path(__file__).resolve().parent / ".index"
DEFAULT_ROOTS = ["wiki", "raw"]


def build_index(
    vault_root: Path = VAULT_ROOT,
    roots: list[str] = DEFAULT_ROOTS,
    index_dir: Path = DEFAULT_INDEX_DIR,
    chunk_size: int = 1200,
    overlap: int = 200,
) -> dict:
    """Build (or incrementally update) the local vector index.

    Documents whose content hash matches the last run are skipped, so
    re-running this after editing a handful of wiki pages only re-embeds
    those pages. Returns a summary dict of files added/updated/removed/unchanged.
    """
    store = VectorStore.load(index_dir)
    documents = load_documents(vault_root, roots)

    seen_paths = {doc.path for doc in documents}
    removed_paths = [path for path in store.manifest if path not in seen_paths]
    for path in removed_paths:
        store.remove_path(path)

    added, updated, unchanged = 0, 0, 0
    for doc in documents:
        existing = store.manifest.get(doc.path)
        if existing and existing["hash"] == doc.content_hash:
            unchanged += 1
            continue

        if existing:
            store.remove_path(doc.path)
            updated += 1
        else:
            added += 1

        pieces = chunk_text(doc.text, chunk_size=chunk_size, overlap=overlap)
        if not pieces:
            continue

        vectors = embed_texts(pieces)
        chunks = [
            {
                "path": doc.path,
                "title": doc.title,
                "doc_type": doc.doc_type,
                "tags": doc.tags,
                "chunk_index": i,
                "text": piece,
            }
            for i, piece in enumerate(pieces)
        ]
        store.add(chunks, vectors, doc.path, doc.content_hash)

    store.save(index_dir)

    return {
        "added": added,
        "updated": updated,
        "removed": len(removed_paths),
        "unchanged": unchanged,
        "total_files": len(store.manifest),
        "total_chunks": len(store.chunks),
    }
