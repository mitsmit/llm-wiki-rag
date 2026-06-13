"""Load source documents from wiki/ and raw/ for RAG indexing."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from pypdf import PdfReader


@dataclass
class Document:
    path: str             # path relative to the vault root, e.g. "wiki/concepts/rag.md"
    title: str
    doc_type: str         # "source" | "concept" | "entity" | "analysis" | "raw" | ...
    tags: list[str] = field(default_factory=list)
    text: str = ""
    content_hash: str = ""


def _hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load_markdown(path: Path, vault_root: Path, default_type: str) -> Document:
    raw_bytes = path.read_bytes()
    text = raw_bytes.decode("utf-8", errors="replace")

    title = path.stem
    doc_type = default_type
    tags: list[str] = []
    body = text

    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            frontmatter_raw = text[3:end].strip()
            body = text[end + 4:].lstrip("\n")
            try:
                meta = yaml.safe_load(frontmatter_raw) or {}
            except yaml.YAMLError:
                meta = {}
            title = meta.get("title", title) or title
            doc_type = meta.get("type", doc_type) or doc_type
            tags = list(meta.get("tags") or [])

    if title == path.stem:
        for line in body.splitlines():
            line = line.strip()
            if line.startswith("# "):
                title = line[2:].strip()
                break

    return Document(
        path=str(path.relative_to(vault_root)),
        title=title,
        doc_type=doc_type,
        tags=tags,
        text=body.strip(),
        content_hash=_hash_bytes(raw_bytes),
    )


def _load_pdf(path: Path, vault_root: Path) -> Document:
    raw_bytes = path.read_bytes()
    reader = PdfReader(path)
    pages = [(page.extract_text() or "").strip() for page in reader.pages]
    text = "\n\n".join(p for p in pages if p)

    return Document(
        path=str(path.relative_to(vault_root)),
        title=path.stem,
        doc_type="raw",
        tags=[],
        text=text,
        content_hash=_hash_bytes(raw_bytes),
    )


def load_documents(vault_root: Path, roots: list[str]) -> list[Document]:
    """Load every markdown and PDF document under the given root directories
    (paths relative to `vault_root`, e.g. ["wiki", "raw"])."""
    documents: list[Document] = []
    for root_name in roots:
        root = vault_root / root_name
        if not root.exists():
            continue
        default_type = "wiki" if root_name == "wiki" else "raw"
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            suffix = path.suffix.lower()
            if suffix == ".md":
                documents.append(_load_markdown(path, vault_root, default_type))
            elif suffix == ".pdf":
                documents.append(_load_pdf(path, vault_root))

    return [doc for doc in documents if doc.text.strip()]
