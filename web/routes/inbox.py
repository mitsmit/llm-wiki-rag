from __future__ import annotations

from fastapi import APIRouter

from ..inbox import get_inbox_items

router = APIRouter()


@router.get("/api/inbox")
def inbox() -> dict:
    items = get_inbox_items()
    return {"count": len(items), "items": items[:5]}
