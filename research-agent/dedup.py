"""Dedup + history tracking for the research agent.

Filters search candidates that are already in the wiki (PDFs in raw/, or
Link urls from research dumps previously sent to raw/) or that were already
surfaced to the user in a past research run (results/history.jsonl), so
ranking isn't spent re-recommending things the user has already seen.
"""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).parent
WIKI_RAW = ROOT.parent / "raw"
HISTORY_PATH = ROOT / "results" / "history.jsonl"

ARXIV_ID_RE = re.compile(r"(\d{4}\.\d{4,5})")
LINK_RE = re.compile(r"\*\*Link:\*\*\s*\[[^\]]*\]\((https?://[^\)\s]+)\)")


def normalize_url(url: str) -> str:
    """Collapse a url to a dedup key: arXiv links become `arxiv:<id>`
    (version-independent), everything else becomes `host/path`."""
    m = ARXIV_ID_RE.search(url)
    if m and "arxiv.org" in url:
        return f"arxiv:{m.group(1)}"
    parsed = urlparse(url)
    host = parsed.netloc.lower().removeprefix("www.")
    return f"{host}{parsed.path.rstrip('/')}"


def _ingested_arxiv_ids(raw_dir: Path) -> set[str]:
    ids = set()
    for pdf in raw_dir.glob("*.pdf"):
        m = ARXIV_ID_RE.search(pdf.stem)
        if m:
            ids.add(f"arxiv:{m.group(1)}")
    return ids


def _links_in_research_dumps(raw_dir: Path) -> set[str]:
    keys = set()
    for md in raw_dir.glob("*.md"):
        text = md.read_text(encoding="utf-8", errors="ignore")
        for url in LINK_RE.findall(text):
            keys.add(normalize_url(url))
    return keys


def _history_keys(history_path: Path) -> set[str]:
    if not history_path.exists():
        return set()
    keys = set()
    with open(history_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            for c in json.loads(line).get("candidates", []):
                keys.add(normalize_url(c["url"]))
    return keys


def load_known(raw_dir: Path = WIKI_RAW, history_path: Path = HISTORY_PATH) -> set[str]:
    """Dedup keys for everything already ingested or already surfaced to the
    user in a past research run."""
    return (
        _ingested_arxiv_ids(raw_dir)
        | _links_in_research_dumps(raw_dir)
        | _history_keys(history_path)
    )


def filter_known(results: list[dict], known: set[str]) -> tuple[list[dict], list[dict]]:
    """Split `results` into (new, already_known) using `known` dedup keys."""
    new, seen = [], []
    for r in results:
        (seen if normalize_url(r["url"]) in known else new).append(r)
    return new, seen


def append_history(
    query: str, variants: list[str], candidates: list[dict], history_path: Path = HISTORY_PATH
) -> None:
    """Record this run's query and candidate pool so future runs can dedupe
    against it, even if nothing from it gets ingested."""
    history_path.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "date": date.today().isoformat(),
        "query": query,
        "variants": variants,
        "candidates": [
            {"title": c["title"], "url": c["url"], "source": c["source"]} for c in candidates
        ],
    }
    with open(history_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
