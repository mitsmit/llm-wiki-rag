"""
Research Agent
--------------
Takes a query, searches arXiv + web, returns top 10 curated reading list.
Can be used as a library (research(query)) or run as a CLI script.
"""

import os
import re
import json
import time
import requests
import xml.etree.ElementTree as ET
from datetime import date, datetime
from pathlib import Path
from dotenv import load_dotenv

import openai

from dedup import append_history, filter_known, load_known

# Load .env from project root (one level up from research-agent/)
load_dotenv(Path(__file__).parent.parent / ".env")

# ── Constants ─────────────────────────────────────────────────────────────────

ROOT   = Path(__file__).parent
SCHEMA = (ROOT / "CLAUDE.md").read_text()
RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

ARXIV_API  = "https://export.arxiv.org/api/query"
ARXIV_NS   = "{http://www.w3.org/2005/Atom}"
MODEL      = os.getenv("OPENAI_MODEL", "gpt-4o")

# ── Search functions ──────────────────────────────────────────────────────────

def search_arxiv(query: str, max_results: int = 15) -> list[dict]:
    """Query arXiv API and return structured results."""
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    try:
        resp = requests.get(ARXIV_API, params=params, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        return []

    root = ET.fromstring(resp.text)
    results = []
    for entry in root.findall(f"{ARXIV_NS}entry"):
        title   = entry.findtext(f"{ARXIV_NS}title", "").strip().replace("\n", " ")
        summary = entry.findtext(f"{ARXIV_NS}summary", "").strip().replace("\n", " ")[:400]
        published = entry.findtext(f"{ARXIV_NS}published", "")[:10]
        link    = entry.findtext(f"{ARXIV_NS}id", "").strip()
        authors = [a.findtext(f"{ARXIV_NS}name", "") for a in entry.findall(f"{ARXIV_NS}author")]
        results.append({
            "title":   title,
            "snippet": summary,
            "url":     link,
            "source":  "arXiv",
            "authors": ", ".join(authors[:3]) + (" et al." if len(authors) > 3 else ""),
            "date":    published,
            "type":    "Paper",
        })
    return results


def search_web(query: str, max_results: int = 25) -> list[dict]:
    """Search web using DuckDuckGo and return structured results."""
    try:
        try:
            from ddgs import DDGS
        except ImportError:
            from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            hits = list(ddgs.text(query, max_results=max_results))
        results = []
        for h in hits:
            results.append({
                "title":   h.get("title", ""),
                "snippet": h.get("body", "")[:400],
                "url":     h.get("href", ""),
                "source":  _extract_domain(h.get("href", "")),
                "authors": "",
                "date":    "",
                "type":    "Article",
            })
        return results
    except Exception:
        return []


def _extract_domain(url: str) -> str:
    m = re.search(r"https?://(?:www\.)?([^/]+)", url)
    return m.group(1) if m else url


# ── Core agent ────────────────────────────────────────────────────────────────

def research(query: str, save: bool = False, on_stream=None) -> str:
    """
    Run the research agent on a query.

    Args:
        query:     The research question or topic.
        save:      If True, saves the result to results/.
        on_stream: Optional callback(text_chunk) for streaming output.

    Returns:
        Markdown string with the top 10 reading list.
    """
    client = openai.OpenAI()

    # ── Step 1: Query expansion ────────────────────────────────────────────
    expansion_resp = client.chat.completions.create(
        model=MODEL,
        max_tokens=300,
        messages=[{
            "role": "user",
            "content": (
                f"You are a research librarian. Given the query below, produce 2–3 "
                f"search variants that cover different angles (technical, applied, critical). "
                f"Return ONLY a JSON array of strings, no explanation.\n\nQuery: {query}"
            ),
        }],
    )
    raw = expansion_resp.choices[0].message.content.strip()
    try:
        variants = json.loads(re.search(r"\[.*\]", raw, re.DOTALL).group())
    except Exception:
        variants = [query]

    all_variants = [query] + [v for v in variants if v != query]

    # ── Step 2: Search ─────────────────────────────────────────────────────
    arxiv_results, web_results = [], []

    for variant in all_variants[:2]:
        arxiv_results += search_arxiv(variant, max_results=10)
        time.sleep(0.5)

    for variant in all_variants[:2]:
        web_results += search_web(variant, max_results=15)
        time.sleep(0.5)

    # Deduplicate by URL
    seen_urls = set()
    all_results = []
    for r in arxiv_results + web_results:
        if r["url"] not in seen_urls:
            seen_urls.add(r["url"])
            all_results.append(r)

    # Drop candidates already ingested into the wiki or surfaced in a past run
    known = load_known()
    new_results, _already_seen = filter_known(all_results, known)
    # Fall back to the unfiltered pool if everything was already seen, so
    # there's still something to rank.
    all_results = new_results or all_results

    # ── Step 3: Rank and write top 10 ─────────────────────────────────────
    today = date.today().isoformat()

    results_block = json.dumps(all_results, indent=2, ensure_ascii=False)
    user_prompt = f"""
SCHEMA (your behavioral rules):
{SCHEMA}

---

TODAY: {today}

USER QUERY: {query}

SEARCH RESULTS ({len(all_results)} candidates from arXiv + web):
{results_block}

---

Using the schema rules above, select and rank the top 10 most valuable results for this query.
Write the full output document in the format specified in the schema's Output Format section.
Only use URLs that appear in the search results above — do not invent any.
""".strip()

    # Stream the response
    full_response = ""
    stream = client.chat.completions.create(
        model=MODEL,
        max_tokens=3000,
        stream=True,
        messages=[{"role": "user", "content": user_prompt}],
    )
    for chunk in stream:
        text = chunk.choices[0].delta.content or ""
        full_response += text
        if on_stream:
            on_stream(text)

    append_history(query, all_variants, all_results)

    # ── Step 4: Optionally save ────────────────────────────────────────────
    if save:
        slug = re.sub(r"[^a-z0-9]+", "-", query.lower())[:50].strip("-")
        path = RESULTS_DIR / f"{today}-{slug}.md"
        path.write_text(full_response, encoding="utf-8")

    return full_response


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Research query: ").strip()
    if not query:
        print("No query provided.")
        sys.exit(1)

    print(f"\nResearching: {query}\n{'─' * 60}\n")
    result = research(query, save=True, on_stream=lambda t: print(t, end="", flush=True))
    print(f"\n\n{'─' * 60}")
    print(f"Saved to results/")
