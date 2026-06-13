"""Split document text into overlapping chunks for embedding."""

from __future__ import annotations


def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 200) -> list[str]:
    """Greedily pack paragraphs into chunks of roughly `chunk_size` characters.

    Each chunk (after the first) is prefixed with the trailing `overlap`
    characters of the previous chunk, so retrieved chunks carry a little
    surrounding context.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not paragraphs:
        return []

    chunks: list[str] = []
    current = ""

    for para in paragraphs:
        for piece in _split_long_paragraph(para, chunk_size):
            if current and len(current) + len(piece) + 2 > chunk_size:
                chunks.append(current)
                tail = current[-overlap:] if overlap else ""
                current = f"{tail}\n\n{piece}" if tail else piece
            else:
                current = f"{current}\n\n{piece}" if current else piece

    if current.strip():
        chunks.append(current)

    return chunks


def _split_long_paragraph(text: str, chunk_size: int) -> list[str]:
    """Split an overlong paragraph on whitespace boundaries near `chunk_size`."""
    if len(text) <= chunk_size:
        return [text]

    pieces = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end < len(text):
            split_at = text.rfind(" ", start, end)
            if split_at <= start:
                split_at = end
        else:
            split_at = len(text)
        pieces.append(text[start:split_at].strip())
        start = split_at

    return [p for p in pieces if p]
