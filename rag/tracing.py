"""Central Langfuse tracing wrapper for the RAG pipeline.

This is the only module that imports `langfuse`. Tracing is a no-op
everywhere unless LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY are set, so the
app and eval harness behave identically (and CI is unaffected) with or
without Langfuse configured.

Usage:
    from .tracing import get_openai_client, observe, score_current, trace_attributes, update_current_span, flush

    @observe(name="my_step")
    def do_thing(...): ...

    with trace_attributes(session_id=..., tags=["view:rag"]):
        ...
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Iterator

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

TRACING_ENABLED = bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))


if TRACING_ENABLED:
    from langfuse import get_client, observe, propagate_attributes
    from langfuse.openai import OpenAI as _TracedOpenAI

    _client = get_client()

    def get_openai_client() -> OpenAI:
        return _TracedOpenAI()

    @contextmanager
    def trace_attributes(**kwargs: Any) -> Iterator[None]:
        with propagate_attributes(**kwargs):
            yield

    def update_current_span(**kwargs: Any) -> None:
        _client.update_current_span(**kwargs)

    def score_current(name: str, value: float | str, comment: str | None = None) -> None:
        _client.score_current_trace(name=name, value=value, comment=comment)

    def flush() -> None:
        _client.flush()

    def get_project_url() -> str | None:
        """Return the Langfuse project's traces URL, or None if unavailable."""
        try:
            project_id = _client._get_project_id()
        except Exception:
            return None
        return f"{_client._base_url}/project/{project_id}" if project_id else None

else:
    def observe(func: Callable | None = None, **_kwargs: Any) -> Callable:
        """No-op stand-in for langfuse.observe. Supports both `@observe`
        and `@observe(name=..., ...)`."""
        if func is not None:
            return func

        def decorator(f: Callable) -> Callable:
            return f
        return decorator

    def get_openai_client() -> OpenAI:
        return OpenAI()

    @contextmanager
    def trace_attributes(**_kwargs: Any) -> Iterator[None]:
        yield

    def update_current_span(**_kwargs: Any) -> None:
        pass

    def score_current(name: str, value: float | str, comment: str | None = None) -> None:
        pass

    def flush() -> None:
        pass

    def get_project_url() -> str | None:
        return None
