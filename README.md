# LLM Wiki

A personal knowledge wiki, written and maintained by an LLM agent (see
[CLAUDE.md](CLAUDE.md)), with a hybrid RAG search/chat interface and an
integrated research agent — all served by a single FastAPI app with a
plain-JS React frontend.

For module-by-module architecture, data flow, and design decisions, see
[DESIGN.md](DESIGN.md). This document is the setup and usage manual.

---

## 1. Prerequisites

- Python 3.10+
- An OpenAI API key — used for answer generation, the wiki query agent, and
  the research agent's query expansion/ranking. (Embeddings and reranking run
  **locally**, no API key or cost — see below.)
- Internet access on first run, to download two local models from Hugging
  Face (one-time, cached afterwards):
  - `BAAI/bge-base-en-v1.5` (embeddings, ~440 MB)
  - `cross-encoder/ms-marco-MiniLM-L-6-v2` (reranking, ~90 MB)

---

## 2. Setup

```bash
# from the repo root
python3 -m venv .venv
source .venv/bin/activate

pip install -r web/requirements.txt
```

`web/requirements.txt` pulls in `rag/requirements.txt` and
`research-agent/requirements.txt` as well, so this one command installs
everything needed by the wiki, RAG pipeline, and research agent.

Then create your `.env`:

```bash
cp .env.example .env
```

Edit `.env` and set `OPENAI_API_KEY`. Everything else is optional — see the
[environment variables reference](#5-environment-variables) below.

---

## 3. Running the app

From the repo root:

```bash
uvicorn web.server:app --reload --port 8000
```

Open **http://localhost:8000** in your browser.

On a fresh clone, `rag/.index/` doesn't exist yet (it's gitignored —
generated, not source). The server starts fine with an empty index, but
**Compare** (RAG) and the eval harness won't find anything until you build it:

1. Go to **Headlines** (the landing page).
2. Click **Reindex**.

This walks `wiki/` and `raw/`, chunks and embeds everything (downloading the
embedding model on first run if needed), and writes `rag/.index/`. Re-run it
any time wiki/raw content changes — it's incremental (only changed/new/removed
files are re-processed).

---

## 4. What each view does

| View | Route | What it's for |
|---|---|---|
| **Headlines** | `/` (`#/`) | Landing page — most recently ingested `wiki/sources/` pages, plus the **Reindex** button. |
| **Compare** | `#/compare` | Ask a question and see two answers side by side: a "wiki-dump" answer (every wiki page in context, no retrieval) vs. a hybrid-RAG answer (embeddings + BM25 + reranking, only the top excerpts in context). Useful for sanity-checking retrieval quality. Answers can be saved as `wiki/analyses/<slug>.md`. |
| **Discover** | `#/research` | The research agent. Enter a topic; it expands the query, searches arXiv + the web, dedupes against what's already in `raw/` and past runs, and ranks a top-10 reading list. Check items you want and click **Add selected to wiki (raw/)** — arXiv picks are downloaded as PDFs, everything else is written as a `<date>-<slug>-selected.md` "list of sources" file for the wiki agent's INGEST workflow. Past sessions are listed under **History**. |
| **Page view** | `#/page/<path>` | Renders any page under `wiki/` (sources, concepts, entities, analyses) from the sidebar. |
| **Log** | `#/log` | Raw view of `log.md`, the wiki agent's append-only operation log. |

If `LANGFUSE_PUBLIC_KEY`/`LANGFUSE_SECRET_KEY` are set, a **📊 Langfuse Traces**
link appears on Headlines, linking to the project's traces in Langfuse.

---

## 5. Environment variables

All read from `.env` at the repo root (via `python-dotenv`).

| Variable | Required | Default | Used for |
|---|---|---|---|
| `OPENAI_API_KEY` | **Yes** | — | All OpenAI calls: RAG/wiki answer generation, research agent query expansion + ranking, eval harness. |
| `OPENAI_MODEL` | No | `gpt-4o` | Generation model for Compare's wiki + RAG answers, the research agent, and the eval harness. |
| `EMBEDDING_MODEL` | No | `BAAI/bge-base-en-v1.5` | Local `sentence-transformers` model for embeddings. Runs on CPU, downloaded from Hugging Face on first use. **Not** an OpenAI model. |
| `LANGFUSE_PUBLIC_KEY` | No | unset | Enables Langfuse tracing. If unset (with `LANGFUSE_SECRET_KEY`), tracing is a complete no-op. |
| `LANGFUSE_SECRET_KEY` | No | unset | See above. |
| `LANGFUSE_HOST` | No | `https://cloud.langfuse.com` | Langfuse instance URL (only matters if the two keys above are set). |

Reranking (`cross-encoder/ms-marco-MiniLM-L-6-v2`) also runs locally but has
no env override — it's fixed in `rag/rerank.py`.

---

## 6. Adding content to the wiki

This repo's wiki content (`wiki/`, `raw/`, `index.md`, `log.md`) is maintained
by an LLM agent following the workflow in [CLAUDE.md](CLAUDE.md):

- Drop a new source file (or list of source links) into `raw/`, then ask the
  agent to ingest it.
- Use **Discover** to find and select new sources — selected items land in
  `raw/` ready for the same ingest step.
- Ask questions via **Compare**; useful answers can be filed as
  `wiki/analyses/*.md`.

---

## 7. Running the eval harness

The RAG pipeline has a retrieval + generation eval set
(`rag/eval/eval_set.jsonl`, a committed fixture):

```bash
python -m rag.eval.run_eval [--strict] [--model MODEL] [--judge-model MODEL]
```

Writes `rag/eval/results/latest.json` (per-item detail) and
`rag/eval/results/summary.md` (aggregate hit@k / MRR / citation validity /
groundedness / relevance). `--strict` exits non-zero if any aggregate falls
below the thresholds in `rag/eval/thresholds.py`.

To regenerate the eval set itself (rarely needed):

```bash
python -m rag.eval.generate_eval_set [--sample N] [--model MODEL]
```

---

## 8. Troubleshooting

- **First Compare/Discover request is slow** — the embedding and
  cross-encoder models are being downloaded and loaded into memory. Subsequent
  requests are fast.
- **Compare returns no excerpts** — you haven't built the index yet; click
  **Reindex** on Headlines (see [§3](#3-running-the-app)).
- **`OPENAI_API_KEY not found` / 401 errors** — check `.env` exists at the
  repo root (not inside `web/` or `rag/`) and has been filled in.
- **Discover search returns nothing** — `ddgs` (web search) occasionally
  rate-limits; arXiv results should still appear. Try a more specific query or
  retry after a short wait.

