"""Fetch full source content for a research candidate into raw/, ready for
the wiki's INGEST workflow.

Currently handles arXiv papers (PDF download). Web-article extraction is
not yet implemented — see ROADMAP.md item 3.
"""

from __future__ import annotations

import re
from pathlib import Path

import requests

from dedup import WIKI_RAW

ARXIV_ID_RE = re.compile(r"(\d{4}\.\d{4,5})(v\d+)?")
CONTENT_DISPOSITION_FILENAME_RE = re.compile(r'filename="([^"]+)"')


def is_arxiv_url(url: str) -> bool:
    return "arxiv.org" in url


def fetch_arxiv_pdf(url: str, raw_dir: Path = WIKI_RAW) -> Path:
    """Download an arXiv paper's PDF into `raw_dir`, named `<id>v<N>.pdf` to
    match existing wiki conventions. If any version of the paper is already
    in `raw_dir`, returns that path without making a request."""
    m = ARXIV_ID_RE.search(url)
    if not m:
        raise ValueError(f"Not an arXiv url: {url}")
    arxiv_id, version = m.group(1), m.group(2) or ""

    existing = sorted(raw_dir.glob(f"{arxiv_id}v*.pdf"))
    if existing:
        return existing[-1]

    resp = requests.get(f"https://arxiv.org/pdf/{arxiv_id}{version}", timeout=30)
    resp.raise_for_status()

    # arXiv reports the canonical `<id>v<N>.pdf` filename even when the
    # request url omits the version, so prefer that over our own guess.
    name_match = CONTENT_DISPOSITION_FILENAME_RE.search(resp.headers.get("content-disposition", ""))
    filename = name_match.group(1) if name_match else f"{arxiv_id}{version or 'v1'}.pdf"

    dest = raw_dir / filename
    dest.write_bytes(resp.content)
    return dest


def fetch_to_raw(url: str, raw_dir: Path = WIKI_RAW) -> Path:
    """Dispatch to the right fetcher based on the url. Raises
    NotImplementedError for non-arXiv urls until web-article extraction is
    added (see ROADMAP.md item 3)."""
    if is_arxiv_url(url):
        return fetch_arxiv_pdf(url, raw_dir)
    raise NotImplementedError(f"Web-article fetching not yet implemented: {url}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python fetch.py <url> [<url> ...]")
        raise SystemExit(1)

    for url in sys.argv[1:]:
        try:
            path = fetch_to_raw(url)
            print(f"{url} -> raw/{path.name}")
        except Exception as e:
            print(f"{url} -> ERROR: {e}")
