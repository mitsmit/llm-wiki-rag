from __future__ import annotations

from fastapi import APIRouter

from rag.tracing import get_project_url

router = APIRouter()


@router.get("/api/config")
def get_config() -> dict:
    return {"langfuse_url": get_project_url()}
