"""Evaluation harness for the RAG pipeline.

Runs every question in rag/eval/eval_set.jsonl through the live hybrid
retrieval + rerank + generation pipeline and computes:

- Retrieval metrics: hit@3 / hit@5 / hit@8 and MRR (path-level, against
  each item's `expected_sources`)
- Citation validity: fraction of source paths cited in the generated answer
  that are actually among the retrieved chunks
- LLM-judge groundedness / relevance (1-5)

Usage:
    python -m rag.eval.run_eval [--strict] [--model MODEL] [--judge-model MODEL]

Writes rag/eval/results/latest.json (full per-item detail) and
rag/eval/results/summary.md (aggregate table). With --strict, exits 1 if any
aggregate metric falls below the threshold in thresholds.py.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

from openai import OpenAI

from .. import (
    DEFAULT_INDEX_DIR,
    VectorStore,
    build_index,
    generate_answer,
    rerank,
    retrieve_from_store,
)
from ..tracing import flush, observe, score_current, trace_attributes
from . import thresholds

EVAL_SET_PATH = Path(__file__).resolve().parent / "eval_set.jsonl"
RESULTS_DIR = Path(__file__).resolve().parent / "results"

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
DEFAULT_JUDGE_MODEL = "gpt-4o-mini"

RETRIEVE_K = 20
RERANK_TOP_N = 8
HIT_KS = (3, 5, 8)

# Matches source paths like wiki/concepts/rag.md or raw/some-paper.pdf,
# however they're punctuated in the answer (parens, backticks, plain text).
CITATION_RE = re.compile(r"\b(?:wiki|raw)/[\w\-./]+\.(?:md|pdf)\b")

JUDGE_PROMPT = """\
You are an evaluator for a retrieval-augmented generation (RAG) system. You will be \
given a question, a set of retrieved excerpts (each labeled with its source path), and \
the system's generated answer.

Rate the answer on two 1-5 scales:
- "groundedness": every factual claim in the answer is directly supported by the \
  retrieved excerpts (5 = fully grounded, no unsupported claims; 1 = mostly fabricated \
  or relies on outside knowledge not present in the excerpts).
- "relevance": the answer directly addresses the question (5 = fully addresses it; \
  1 = off-topic or a non-answer).

Respond as JSON: {"groundedness": <1-5>, "relevance": <1-5>, "notes": "<one-sentence explanation>"}"""


def _load_eval_set(path: Path = EVAL_SET_PATH) -> list[dict]:
    items = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def _retrieval_metrics(retrieved_paths: list[str], expected_sources: list[str]) -> dict:
    expected = set(expected_sources)
    metrics = {}
    for k in HIT_KS:
        metrics[f"hit@{k}"] = 1.0 if set(retrieved_paths[:k]) & expected else 0.0

    mrr = 0.0
    for rank, path in enumerate(retrieved_paths, start=1):
        if path in expected:
            mrr = 1.0 / rank
            break
    metrics["mrr"] = mrr
    return metrics


def _extract_cited_paths(answer: str) -> set[str]:
    return set(CITATION_RE.findall(answer))


def _citation_validity(answer: str, retrieved_paths: set[str]) -> tuple[float, bool]:
    cited = _extract_cited_paths(answer)
    if not cited:
        return 1.0, False
    valid = sum(1 for p in cited if p in retrieved_paths)
    return valid / len(cited), True


def _judge(client: OpenAI, question: str, retrieved, answer: str, model: str) -> dict:
    excerpts = "\n\n".join(f"[{c.path}] {c.text[:800]}" for c in retrieved)
    user_prompt = f"QUESTION:\n{question}\n\nRETRIEVED EXCERPTS:\n{excerpts}\n\nGENERATED ANSWER:\n{answer}"

    response = client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": JUDGE_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    try:
        data = json.loads(response.choices[0].message.content)
    except (json.JSONDecodeError, TypeError):
        data = {}

    return {
        "groundedness": float(data.get("groundedness", 0)),
        "relevance": float(data.get("relevance", 0)),
        "notes": data.get("notes", ""),
    }


def _aggregate(results: list[dict]) -> dict:
    if not results:
        return {}
    keys = [f"hit@{k}" for k in HIT_KS] + ["mrr", "citation_validity", "groundedness", "relevance"]
    n = len(results)
    return {key: sum(r[key] for r in results) / n for key in keys}


@observe(name="eval_item", capture_input=False, capture_output=False)
def _run_eval_item(item: dict, store: VectorStore, client: OpenAI, model: str, judge_model: str) -> dict:
    with trace_attributes(
        tags=["eval"],
        metadata={"eval_id": item["id"], "expected_sources": ", ".join(item["expected_sources"])},
    ):
        candidates = retrieve_from_store(store, item["question"], k=RETRIEVE_K)
        retrieved = rerank(item["question"], candidates, top_n=RERANK_TOP_N)
        retrieved_paths = [c.path for c in retrieved]

        retrieval_metrics = _retrieval_metrics(retrieved_paths, item["expected_sources"])

        answer = generate_answer(item["question"], retrieved, model)
        citation_validity, has_citations = _citation_validity(answer, set(retrieved_paths))
        judge = _judge(client, item["question"], retrieved, answer, judge_model)

        result = {
            "id": item["id"],
            "question": item["question"],
            "expected_sources": item["expected_sources"],
            "retrieved_paths": retrieved_paths,
            **retrieval_metrics,
            "citation_validity": citation_validity,
            "has_citations": has_citations,
            "groundedness": judge["groundedness"],
            "relevance": judge["relevance"],
            "judge_notes": judge["notes"],
            "answer": answer,
        }

        for k in HIT_KS:
            score_current(name=f"hit@{k}", value=result[f"hit@{k}"])
        score_current(name="mrr", value=result["mrr"])
        score_current(name="citation_validity", value=result["citation_validity"])
        score_current(name="groundedness", value=result["groundedness"])
        score_current(name="relevance", value=result["relevance"])

    return result


def run_eval(model: str = DEFAULT_MODEL, judge_model: str = DEFAULT_JUDGE_MODEL) -> dict:
    build_index()
    store = VectorStore.load(DEFAULT_INDEX_DIR)
    store.ensure_bm25()

    items = _load_eval_set()
    client = OpenAI()

    results = [_run_eval_item(item, store, client, model, judge_model) for item in items]
    return {"items": results, "aggregates": _aggregate(results)}


def _write_summary_md(report: dict, path: Path):
    agg = report["aggregates"]
    lines = [
        "# RAG Eval Summary",
        "",
        f"_{len(report['items'])} questions_",
        "",
        "| Metric | Value |",
        "|---|---|",
    ]
    for key, value in agg.items():
        lines.append(f"| {key} | {value:.3f} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _check_thresholds(agg: dict) -> list[str]:
    checks = {
        "hit@3": thresholds.MIN_HIT_AT_3,
        "hit@5": thresholds.MIN_HIT_AT_5,
        "hit@8": thresholds.MIN_HIT_AT_8,
        "mrr": thresholds.MIN_MRR,
        "citation_validity": thresholds.MIN_CITATION_VALIDITY,
        "groundedness": thresholds.MIN_GROUNDEDNESS,
        "relevance": thresholds.MIN_RELEVANCE,
    }
    failures = []
    for key, min_value in checks.items():
        value = agg.get(key, 0.0)
        if value < min_value:
            failures.append(f"{key} = {value:.3f} < {min_value}")
    return failures


def main():
    parser = argparse.ArgumentParser(description="Run the RAG evaluation harness.")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any aggregate metric is below its threshold.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Generation model.")
    parser.add_argument("--judge-model", default=DEFAULT_JUDGE_MODEL, help="LLM-judge model.")
    args = parser.parse_args()

    report = run_eval(model=args.model, judge_model=args.judge_model)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "latest.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    _write_summary_md(report, RESULTS_DIR / "summary.md")

    print((RESULTS_DIR / "summary.md").read_text(encoding="utf-8"))

    flush()

    if args.strict:
        failures = _check_thresholds(report["aggregates"])
        if failures:
            print("THRESHOLD FAILURES:")
            for f in failures:
                print(f"  - {f}")
            sys.exit(1)


if __name__ == "__main__":
    main()
