from __future__ import annotations

from fastapi import APIRouter

from ..headlines import get_headlines

router = APIRouter()


@router.get("/api/headlines")
def headlines(limit: int = 10) -> list[dict]:
    return get_headlines(limit=limit)
