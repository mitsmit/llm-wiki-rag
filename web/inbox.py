"""Landing-page data: raw/ files dropped for ingestion but not yet processed.

A file counts as "pending" if its name never appears in log.md — log entries
reference ingested sources as `raw/<name>` (see CLAUDE.md's INGEST workflow),
so anything not mentioned hasn't been through INGEST yet.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = VAULT_ROOT / "raw"
LOG_PATH = VAULT_ROOT / "log.md"


def get_inbox_items() -> list[dict]:
    """Return raw/ files not yet referenced in log.md, newest first."""
    log_content = LOG_PATH.read_text(encoding="utf-8") if LOG_PATH.exists() else ""

    items = []
    for f in RAW_DIR.iterdir():
        if not f.is_file() or f.name.startswith("."):
            continue
        if f.name in log_content:
            continue
        items.append({
            "filename": f.name,
            "modified": f.stat().st_mtime,
        })

    items.sort(key=lambda item: item["modified"], reverse=True)
    for item in items:
        item["modified"] = datetime.fromtimestamp(item["modified"]).strftime("%Y-%m-%d")
    return items
