"""Generate an evaluation set of (question, expected_source) pairs from wiki/raw docs.

For each indexed document, an LLM writes one question answerable from that
document's text alone, plus a short reference answer. The document's path
becomes the ground-truth `expected_sources` entry for retrieval evaluation.

Not run by CI — `eval_set.jsonl` is a committed fixture. Regenerate by hand
when the wiki changes enough to warrant it:

    python -m rag.eval.generate_eval_set [--sample N] [--model MODEL]
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from openai import OpenAI

from ..index import DEFAULT_ROOTS, VAULT_ROOT
from ..loaders import load_documents

DEFAULT_MODEL = "gpt-4o-mini"
MIN_TEXT_LEN = 200
MAX_EXCERPT_CHARS = 4000

EVAL_SET_PATH = Path(__file__).resolve().parent / "eval_set.jsonl"

GENERATION_PROMPT = """\
You are creating an evaluation question for a retrieval-augmented generation (RAG) \
system that answers questions using a personal knowledge wiki.

Given the title and excerpt of a single document, write ONE specific question whose \
answer is fully contained in the excerpt, plus a concise reference answer (1-3 sentences).

Requirements:
- The question must be answerable using ONLY this excerpt — avoid vague questions that \
  could be answered from general knowledge without having read it.
- Avoid yes/no questions; prefer questions that require recalling a specific fact, \
  definition, number, name, or explanation from the text.
- The reference answer should be a short, factual summary drawn directly from the excerpt.

Respond as JSON: {"question": "...", "reference_answer": "..."}"""


def _generate_question(client: OpenAI, doc, model: str) -> dict | None:
    excerpt = doc.text[:MAX_EXCERPT_CHARS]
    user_prompt = f"Title: {doc.title}\n\nExcerpt:\n{excerpt}"

    response = client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": GENERATION_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    try:
        data = json.loads(response.choices[0].message.content)
    except (json.JSONDecodeError, TypeError):
        return None

    question = data.get("question")
    reference_answer = data.get("reference_answer")
    if not question or not reference_answer:
        return None
    return {"question": question, "reference_answer": reference_answer}


def generate_eval_set(sample: int | None = None, model: str = DEFAULT_MODEL, seed: int = 42) -> list[dict]:
    documents = [d for d in load_documents(VAULT_ROOT, DEFAULT_ROOTS) if len(d.text.strip()) >= MIN_TEXT_LEN]

    if sample is not None and sample < len(documents):
        rng = random.Random(seed)
        rng.shuffle(documents)
        documents = documents[:sample]

    documents = sorted(documents, key=lambda d: d.path)

    client = OpenAI()
    items = []
    for i, doc in enumerate(documents, start=1):
        result = _generate_question(client, doc, model)
        if result is None:
            continue
        items.append({
            "id": f"q{i:03d}",
            "question": result["question"],
            "expected_sources": [doc.path],
            "reference_answer": result["reference_answer"],
        })
    return items


def main():
    parser = argparse.ArgumentParser(description="Generate a RAG evaluation set from wiki/raw docs.")
    parser.add_argument("--sample", type=int, default=None, help="Generate from a random sample of N docs instead of all docs.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="LLM used to generate questions.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for --sample.")
    args = parser.parse_args()

    items = generate_eval_set(sample=args.sample, model=args.model, seed=args.seed)

    with open(EVAL_SET_PATH, "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item) + "\n")

    print(f"Wrote {len(items)} eval items to {EVAL_SET_PATH}")


if __name__ == "__main__":
    main()
