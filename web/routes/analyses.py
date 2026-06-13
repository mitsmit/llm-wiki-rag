from __future__ import annotations

from datetime import date

from fastapi import APIRouter
from pydantic import BaseModel

from ..wiki_data import VAULT_ROOT, WIKI_DIR

router = APIRouter()


class AnalysisRequest(BaseModel):
    slug: str
    question: str
    answer: str


@router.post("/api/analyses")
def save_analysis(req: AnalysisRequest) -> dict:
    today = date.today().isoformat()
    path = WIKI_DIR / "analyses" / f"{req.slug}.md"
    content = f"""---
title: "{req.question[:80]}"
type: analysis
tags: []
sources: []
created: {today}
updated: {today}
---

## Query

{req.question}

## Answer

{req.answer}
"""
    path.write_text(content, encoding="utf-8")

    log_path = VAULT_ROOT / "log.md"
    entry = (
        f"\n## [{today}] query | {req.slug}\n\n"
        f"- **Operation:** query\n"
        f"- **Pages touched:** wiki/analyses/{req.slug}.md\n"
        f'- **Notes:** Query: "{req.question[:100]}"\n'
    )
    with open(log_path, "a") as f:
        f.write(entry)

    _append_to_index(f"- [{req.question[:60]}](wiki/analyses/{req.slug}.md) — query filed {today}", "## Analyses")

    return {"status": "ok", "path": f"wiki/analyses/{req.slug}.md"}


def _append_to_index(line: str, section: str) -> None:
    index_path = VAULT_ROOT / "index.md"
    content = index_path.read_text(encoding="utf-8")
    if line in content:
        return
    if section in content:
        content = content.replace(section, section + "\n" + line)
    else:
        content += f"\n{section}\n{line}\n"
    index_path.write_text(content, encoding="utf-8")
