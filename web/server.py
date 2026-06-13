from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from rag import DEFAULT_INDEX_DIR, VectorStore
from rag.tracing import get_openai_client

VAULT_ROOT = Path(__file__).resolve().parent.parent
STATIC_DIR = Path(__file__).resolve().parent / "static"

load_dotenv(VAULT_ROOT / ".env")

from .routes import analyses, brainstorm, config, headlines, inbox, query, research, wiki  # noqa: E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    store = VectorStore.load(DEFAULT_INDEX_DIR)
    store.ensure_bm25()
    app.state.rag_store = store

    # Touch openai's lazily-imported `resources.chat` submodule once here,
    # single-threaded, so the Compare view's concurrent wiki+RAG requests
    # (both first-time `client.chat.completions` accesses, run in Starlette's
    # threadpool) don't race CPython's import lock and hit
    # "deadlock detected by _ModuleLock('openai.resources.chat')".
    get_openai_client().chat.completions

    yield


app = FastAPI(title="LLM Wiki", lifespan=lifespan)

app.include_router(headlines.router)
app.include_router(inbox.router)
app.include_router(wiki.router)
app.include_router(query.router)
app.include_router(analyses.router)
app.include_router(config.router)
app.include_router(research.router)
app.include_router(brainstorm.router)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")
