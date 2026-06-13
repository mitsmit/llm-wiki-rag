# Research Agent — Roadmap

Tracks known gaps and planned improvements for the research agent's path
toward a closed loop ("search → curate → select → fetch → ingest"). Each
item below is written to be filed as a GitHub issue as-is (title, context,
proposal, size).

_Last updated: 2026-06-13_

---

## Status

- ✅ **Dedup + history** ([dedup.py](dedup.py), wired into [agent.py](agent.py)) —
  filters candidates already ingested (`raw/*.pdf` arXiv IDs), already
  surfaced in past research dumps (`raw/*.md` `**Link:**` urls), or already
  shown in a past run (`results/history.jsonl`). Done 2026-06-13.
- ✅ **Fetcher, arXiv only** ([fetch.py](fetch.py)) — `fetch_to_raw(url)`
  downloads an arXiv paper's PDF into `raw/<id>v<N>.pdf` (skips if any
  version already present), via `python fetch.py <url> [<url> ...]` or as a
  library call. Web-article extraction still raises `NotImplementedError`
  (see item 3). Done 2026-06-13. Wired into the selection step via
  `POST /api/research/select`.
- ✅ **Reading-list parser** ([parse.py](parse.py)) — `parse_reading_list(markdown)`
  extracts each `### N. Title` item into `{title, source, authors, date,
  url, type, why_read_it}`; `render_item(item)` is the inverse, for writing
  selected non-arXiv items back into `raw/`. Verified against both existing
  `raw/*-research.md` dumps (7/7 and 10/10 items, including the file with
  skipped numbering). Done 2026-06-13.
- ✅ **Selection UI** ([ResearchView.js](../web/static/js/components/ResearchView.js)) —
  per-item checkboxes below each result; "Add selected to wiki (raw/)" calls
  `POST /api/research/select`, which fetches arXiv picks as PDFs via
  `fetch.fetch_arxiv_pdf` and writes non-arXiv picks as a
  `<date>-<slug>-selected.md` "list of sources" file. Originally prototyped
  in Streamlit (`app.py` `render_selection`), then ported to the main web
  app — see "Single-server web integration" below. Done 2026-06-13.
- ✅ **Single-server web integration** ([web/research_bridge.py](../web/research_bridge.py),
  [web/routes/research.py](../web/routes/research.py),
  [ResearchView.js](../web/static/js/components/ResearchView.js)) —
  research-agent's UI moved from a standalone Streamlit app (`app.py`, now
  removed) into a new **🔭 Discover** view in the main wiki app.
  `agent.research()`'s callback-based streaming is bridged to NDJSON via a
  thread+queue (`POST /api/research`, mirroring `/api/query/wiki`);
  `GET /api/research/history` and `GET /api/research/result/{name}` cover
  past sessions. One `uvicorn web.server:app` process now serves the wiki,
  RAG, and research agent. `research-agent/` was also un-gitignored (source
  only — `results/` stays local, see item 7) since `web/` now depends on it
  directly. Resolves item 6 below by removal. Done 2026-06-13.

---

## Known Gaps / Pain Points

### 1. History-based dedup never expires
- **Context:** `dedup.append_history()` records every candidate shown,
  forever. If a candidate is relevant to a *later, different* query but was
  part of an earlier unrelated run's pool, it's now permanently hidden —
  even if it was never ingested.
- **Proposal:** Add an expiry/cooldown (e.g. re-eligible after N days) or
  scope "seen" by query similarity rather than a single global set.
- **Size:** S

### 2. ~~No selection step~~ — done
- **Resolved 2026-06-13** by the Selection UI in Status above.

### 3. No full-text fetch for web articles
- **Context:** [fetch.py](fetch.py) now handles arXiv papers
  (`fetch_arxiv_pdf` → `raw/<id>v<N>.pdf`), covering the majority of past
  ingests. Web articles (`search_web` results) still raise
  `NotImplementedError` — their full text fetch into `raw/` continues to
  happen conversationally during INGEST.
- **Proposal:** Add `fetch_web_article(url) -> Path` using readability
  extraction (e.g. `trafilatura`, a new dependency) to write
  `raw/<slug>.md`. Wire both fetchers into `fetch_to_raw` dispatch (already
  in place) once selection (#2) provides the trigger.
- **Size:** S (remaining scope, down from M)

### 4. Research isn't informed by what the wiki is missing
- **Context:** The LINT workflow already produces "data gaps worth filling
  with a web search" (see `wiki/analyses/lint-2026-04-28.md`), but nothing
  feeds those into the research agent — searches are purely user-typed.
- **Proposal:** Allow LINT gap items to be queued as research-agent queries;
  surface results in a review inbox alongside ad-hoc searches.
- **Size:** M

### 5. No tests for research-agent modules
- **Context:** `agent.py` and `dedup.py` have no automated tests (dedup.py
  was only manually verified in this session). Regressions in normalization
  (e.g. arXiv id extraction, url collapsing) would be silent.
- **Proposal:** Add unit tests for `dedup.normalize_url`, `filter_known`,
  `append_history` against fixture `raw/`/`history.jsonl` data.
- **Size:** S

### 6. ~~`app.py` "Open Wiki" link likely stale~~ — done
- **Resolved 2026-06-13** — `app.py` (the standalone Streamlit app) was
  removed entirely; see "Single-server web integration" in Status above.
  The Discover view now lives inside the main app, so no cross-link is
  needed.

### 7. ~~`results/` grows unbounded and is git-committed~~ — done
- **Resolved 2026-06-13** — `research-agent/results/` (saved session
  markdowns + `history.jsonl`) is now gitignored as local/regenerable run
  state, consistent with `rag/.index/` and `rag/eval/results/`. Source
  modules (`agent.py`, `dedup.py`, `fetch.py`, `parse.py`) and
  `CLAUDE.md`/`ROADMAP.md` are tracked.

### 8. Silent search degradation
- **Context:** `search_web` catches all exceptions and returns `[]`
  silently (agent.py:92-93) if both `ddgs` and `duckduckgo_search` are
  unavailable or the search fails — the user gets a thinner result set with
  no indication why.
- **Proposal:** Surface a warning (via `on_stream` or the summary's "What's
  Missing" section) when a search source returns zero results/errors.
- **Size:** S

---

## Future Improvements

### A. ~~"Discover" tab in the main web app~~ — done
- **Resolved 2026-06-13** by "Single-server web integration" in Status above
  ([ResearchView.js](../web/static/js/components/ResearchView.js)).

### B. Scheduled research sweeps
- **Context:** Standing topics of interest could be searched periodically
  without manual triggering.
- **Proposal:** Use `/schedule` to run `research()` on a cadence for a
  configured list of topics, populating the review inbox (now available via
  the Discover view from A) rather than auto-ingesting.
- **Size:** M (A is done — this is now unblocked)

### C. Wiki-aware ranking
- **Context:** Ranking currently only sees the search candidates, not what's
  already in the wiki. `overview.md`'s "open threads" describe exactly the
  questions the wiki wants answered next.
- **Proposal:** Pass a summary of `overview.md`'s open threads into the
  ranking prompt so candidates that extend/contradict existing wiki threads
  are prioritized over generic "top 10 in X" results.
- **Size:** M

### D. Open-model swap for expansion + ranking
- **Context:** Carries over from the OpenAI-cost audit — query expansion and
  final ranking both run on `gpt-4o` per call. With dedup now shrinking the
  candidate pool (#1's fix would shrink it further over time), these are
  good low-stakes candidates for a cheaper/open model via an
  OpenAI-compatible endpoint.
- **Proposal:** Parameterize `MODEL`/`get_openai_client`-equivalent for the
  research agent separately from the live RAG generation model, and A/B
  query-expansion quality on an open model first.
- **Size:** M

### E. User-driven source requests
- **Context:** New sources currently enter the wiki via two paths: the wiki
  agent's INGEST workflow (human drops files/links into `raw/`) or Discover's
  agent-curated reading list (agent searches + ranks, human selects from the
  results of *that* search). There's no way for a user to browse a
  pre-existing list of candidate sources and pick from it, or to directly
  request that a specific source/topic be fetched and ingested without
  running a full Discover search first.
- **Proposal:** Two complementary additions to the Discover view:
  - A "suggested sources" list the user can browse and select from —
    candidates could come from LINT's "data gaps worth filling" output or a
    standing/curated catalog, reusing Discover's existing selection UI
    (checkboxes + `POST /api/research/select`).
  - A lightweight "request a source" input (paste a URL, or name a
    paper/topic) that fetches + stages that one item into `raw/` directly,
    without a full ranked top-10 search.
- **Size:** M
