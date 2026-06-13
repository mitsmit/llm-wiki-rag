"""Brainstorming module endpoints: identify domain-expert personas for an
idea, run parallel multi-round persona turns, synthesize a verdict, and save
the session to brainstorming_output/."""

from __future__ import annotations

import json
import queue
import re
import threading
from datetime import date
from typing import Iterator

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from rag.tracing import trace_attributes

from ..brainstorm import MODEL, extract_verdict, identify_domains, stream_expert_turn, stream_synthesis
from ..wiki_data import VAULT_ROOT, append_to_index

router = APIRouter()


class PersonaModel(BaseModel):
    id: str
    name: str
    domain: str
    blurb: str


class TranscriptTurn(BaseModel):
    speaker: str
    text: str
    verdict: str | None = None


class StartRequest(BaseModel):
    idea: str
    session_id: str


class TurnRequest(BaseModel):
    idea: str
    personas: list[PersonaModel]
    transcript: list[TranscriptTurn]
    session_id: str


class ConcludeRequest(BaseModel):
    idea: str
    transcript: list[TranscriptTurn]
    session_id: str


class SaveRequest(BaseModel):
    slug: str
    idea: str
    personas: list[PersonaModel]
    transcript: list[TranscriptTurn]
    verdict: str


def _ndjson(obj: dict) -> str:
    return json.dumps(obj) + "\n"


@router.post("/api/brainstorm/start")
def start_brainstorm(req: StartRequest) -> dict:
    try:
        with trace_attributes(session_id=req.session_id, tags=["view:brainstorm"]):
            personas = identify_domains(req.idea, MODEL)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"personas": personas}


@router.post("/api/brainstorm/turn")
def brainstorm_turn(req: TurnRequest) -> StreamingResponse:
    transcript = [t.model_dump() for t in req.transcript]
    personas = [p.model_dump() for p in req.personas]

    def gen() -> Iterator[str]:
        events: queue.Queue = queue.Queue()
        lock = threading.Lock()
        remaining = {"n": len(personas)}

        def run_agent(persona: dict) -> None:
            parts: list[str] = []
            try:
                with trace_attributes(session_id=req.session_id, tags=["view:brainstorm", f"persona:{persona['id']}"]):
                    for delta in stream_expert_turn(persona, req.idea, transcript, personas, MODEL):
                        parts.append(delta)
                        events.put({"type": "token", "agent_id": persona["id"], "data": delta})
                display, verdict = extract_verdict("".join(parts))
                events.put({"type": "agent_done", "agent_id": persona["id"], "text": display, "verdict": verdict})
            except Exception as e:
                events.put({"type": "error", "agent_id": persona["id"], "data": str(e)})
            finally:
                with lock:
                    remaining["n"] -= 1
                    done = remaining["n"] == 0
                if done:
                    events.put(None)

        for p in personas:
            threading.Thread(target=run_agent, args=(p,), daemon=True).start()

        while True:
            evt = events.get()
            if evt is None:
                break
            yield _ndjson(evt)

        yield _ndjson({"type": "done"})

    return StreamingResponse(gen(), media_type="application/x-ndjson")


@router.post("/api/brainstorm/conclude")
def brainstorm_conclude(req: ConcludeRequest) -> StreamingResponse:
    transcript = [t.model_dump() for t in req.transcript]

    def gen() -> Iterator[str]:
        try:
            with trace_attributes(session_id=req.session_id, tags=["view:brainstorm"]):
                for delta in stream_synthesis(req.idea, transcript, MODEL):
                    yield _ndjson({"type": "token", "data": delta})
            yield _ndjson({"type": "done"})
        except Exception as e:
            yield _ndjson({"type": "error", "data": str(e)})

    return StreamingResponse(gen(), media_type="application/x-ndjson")


@router.post("/api/brainstorm/save")
def save_brainstorm(req: SaveRequest) -> dict:
    today = date.today().isoformat()
    output_dir = VAULT_ROOT / "brainstorming_output"
    output_dir.mkdir(exist_ok=True)
    path = output_dir / f"{req.slug}.md"

    tags = sorted({re.sub(r"[^a-z0-9]+", "-", p.domain.lower()).strip("-") for p in req.personas})
    tags_str = "[" + ", ".join(tags) + "]"

    persona_list = "\n".join(f"- **{p.name}** ({p.domain}) — {p.blurb}" for p in req.personas)

    transcript_md = "\n\n---\n\n".join(
        f"**{t.speaker}:**\n\n{t.text}" + (f"\n\n_Verdict: {t.verdict}_" if t.verdict else "")
        for t in req.transcript
    )

    content = f"""---
title: "Brainstorm: {req.idea[:80]}"
type: analysis
tags: {tags_str}
sources: []
created: {today}
updated: {today}
---

## Idea

{req.idea}

## Experts Consulted

{persona_list}

## Verdict

{req.verdict}

## Transcript

{transcript_md}
"""
    path.write_text(content, encoding="utf-8")

    log_path = VAULT_ROOT / "log.md"
    with open(log_path, "a") as f:
        f.write(
            f"\n## [{today}] brainstorm | {req.slug}\n\n"
            f"- **Operation:** brainstorm\n"
            f"- **Pages touched:** brainstorming_output/{req.slug}.md\n"
            f'- **Notes:** Brainstorm: "{req.idea[:100]}" — experts: '
            f"{', '.join(p.name for p in req.personas)}\n"
        )

    append_to_index(
        f"- [{req.idea[:60]}](brainstorming_output/{req.slug}.md) — brainstorm filed {today}",
        "## Brainstorms",
    )

    return {"status": "ok", "path": f"brainstorming_output/{req.slug}.md"}
