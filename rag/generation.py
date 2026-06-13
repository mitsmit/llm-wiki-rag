"""Shared prompt/context-building logic for the RAG query view and the eval harness.

Keeping this in one place ensures the eval harness measures exactly what the
app would produce for a user.
"""

from __future__ import annotations

from typing import Iterator

from .retrieve import RetrievedChunk
from .tracing import get_openai_client, observe, update_current_span

RAG_SYSTEM_PROMPT = """\
You are the RAG query agent for a personal LLM Wiki. You are given the most relevant excerpts \
retrieved from the wiki (curated notes) and the raw source documents (papers, articles) \
that back it, each labeled with its source path, ranked by relevance to the question.

Every excerpt below is grounded in a specific source path — treat that path as its citation.

When answering a question:
1. Use only information found in the excerpts below. Do not rely on outside knowledge.
2. Every claim in your answer must be backed by at least one excerpt and cited inline by \
   its source path, e.g. (wiki/concepts/rag.md).
3. If a piece of information would be useful but no excerpt supports it, leave it out of \
   the answer rather than filling the gap from memory.
4. If the excerpts don't contain enough information to answer, say so clearly and suggest \
   what source types would help.
5. Format your answer in clean markdown: use headings, bullet points, and tables where helpful.
6. End with a **Sources used** section listing the exact source paths you cited.

Be direct and precise. Do not pad answers."""


def build_rag_context(chunks: list[RetrievedChunk]) -> str:
    """Build a context block from retrieved RAG chunks for the RAG query prompt."""
    if not chunks:
        return "(no relevant content found in the index)"
    parts = []
    for c in chunks:
        parts.append(f"=== {c.path} — {c.title} (relevance {c.score:.3f}) ===\n{c.text}\n")
    return "\n".join(parts)


@observe(name="generate_answer", capture_input=False)
def generate_answer(query: str, retrieved: list[RetrievedChunk], model: str) -> str:
    """Run the RAG generation step (non-streaming) and return the full answer text."""
    context = build_rag_context(retrieved)
    user_prompt = f"""RETRIEVED EXCERPTS:\n\n{context}\n\n---\n\nQUESTION: {query}"""

    client = get_openai_client()
    response = client.chat.completions.create(
        model=model,
        max_tokens=2048,
        messages=[
            {"role": "system", "content": RAG_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    answer = response.choices[0].message.content or ""
    update_current_span(
        input={"query": query, "retrieved_paths": [c.path for c in retrieved]},
    )
    return answer


def stream_chat(
    system_prompt: str,
    user_prompt: str,
    history: list[dict],
    model: str,
    client=None,
) -> Iterator[str]:
    """Stream a chat completion, yielding text deltas as they arrive.

    `history` is a list of `{"role": ..., "content": ...}` messages; only
    `assistant` turns are replayed (mirrors the Streamlit views' behavior of
    feeding back prior answers without re-sending prior prompts/contexts).
    """
    if client is None:
        client = get_openai_client()
    stream = client.chat.completions.create(
        model=model,
        max_tokens=2048,
        stream=True,
        messages=[
            {"role": "system", "content": system_prompt},
            *[{"role": m["role"], "content": m["content"]} for m in history if m["role"] == "assistant"],
            {"role": "user", "content": user_prompt},
        ],
    )
    for chunk in stream:
        text = chunk.choices[0].delta.content or ""
        if text:
            yield text


@observe(name="generate_answer_stream", capture_input=False)
def stream_rag_answer(
    query: str,
    retrieved: list[RetrievedChunk],
    history: list[dict],
    model: str,
) -> Iterator[str]:
    """Streaming counterpart to `generate_answer`: yields text deltas, then
    records the full answer on the current span once exhausted."""
    context = build_rag_context(retrieved)
    user_prompt = f"""RETRIEVED EXCERPTS:\n\n{context}\n\n---\n\nQUESTION: {query}"""

    parts: list[str] = []
    for delta in stream_chat(RAG_SYSTEM_PROMPT, user_prompt, history, model):
        parts.append(delta)
        yield delta

    update_current_span(
        input={"query": query, "retrieved_paths": [c.path for c in retrieved]},
        output="".join(parts),
    )
