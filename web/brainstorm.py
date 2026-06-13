"""Brainstorming module: domain-expert personas that support, critique, and
refine a user's idea across a multi-round, multi-agent conversation.

Standalone — no wiki/RAG grounding, pure LLM reasoning about the idea and
the running transcript.
"""

from __future__ import annotations

import json
import os
import re
from typing import Iterator

from rag.generation import stream_chat
from rag.tracing import get_openai_client, observe, update_current_span

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
MAX_ROUNDS = 6

DOMAIN_SYSTEM_PROMPT = """\
You are a domain-classification assistant for a brainstorming tool. Given \
a user's idea or proposal, identify 2 or 3 distinct expert perspectives \
most useful for critiquing, supporting, and refining it. Pick perspectives \
that would meaningfully disagree or notice different things (technical \
feasibility, market/strategy, ethics/risk, user experience, etc.) — choose \
whichever 2-3 are MOST relevant to THIS idea, not a fixed template. Use 3 \
only if a third angle is clearly and distinctly important; otherwise use 2.

Respond with ONLY a JSON object, no markdown fences, no commentary:
{"personas": [{"name": "<persona title, e.g. 'Distributed Systems Engineer'>", "domain": "<short domain label>", "blurb": "<one sentence on this persona's lens>"}]}\
"""

EXPERT_SYSTEM_PROMPT_TEMPLATE = """\
You are {name}, an expert in {domain}. {blurb}

You're one of {n_personas} expert participants ({other_names}) in a \
multi-round brainstorming session about this idea, proposed by the user:

"{idea}"

Below is the transcript of the conversation so far, in order:

{transcript_block}

In your turn:
- Engage with the transcript directly — respond to the user's latest point \
and to anything the other expert(s) said in earlier rounds (agree, \
disagree, build on, or push back, naming them where useful).
- Hold your own ground. Don't converge with the other expert(s) just to \
reach harmony — if your domain's perspective leads you somewhere different \
than what they said, say so and explain why. Diverse, even conflicting, \
expert perspectives are the point; agreement between experts should be rare \
and earned, not the default.
- Support, critique, refine, or ask a clarifying question — whichever is \
most useful right now. Don't lock into one stance.
- Tone: polite and conversational, like a colleague talking it through — \
but don't soften real concerns. Be direct about weaknesses, risks, or \
flawed assumptions; critical feedback delivered respectfully is more useful \
than vague positivity.
- Be concise: respond in a single short paragraph (3-5 sentences max). \
Don't repeat points already made.
- Draw on your general domain knowledge only — you have no access to \
external documents.

Finish your reply with exactly one final line, on its own, with nothing \
after it:
VERDICT: AGREE
or
VERDICT: CONTINUE

Use AGREE only if, after this reply, you have no further objections, \
critiques, or questions about the idea as discussed so far. Otherwise use \
CONTINUE.\
"""

SYNTHESIS_SYSTEM_PROMPT = """\
You are a neutral facilitator summarizing a brainstorming session between a \
user and one or more domain-expert personas about the user's idea.

Given the idea and the full transcript below, produce a concise synthesis \
in markdown with exactly these three sections, each a short bullet list \
(omit a bullet point if there's nothing to say, but keep the heading):

## Agreements
## Objections
## Refinements

No preamble, no other sections, no closing remarks — just the three \
headings and their bullets.\
"""

VERDICT_RE = re.compile(
    r"\**VERDICT:?\**\s*[:\-]?\s*(AGREE|CONTINUE)\b\.?\**\s*$",
    re.IGNORECASE | re.MULTILINE,
)


def _slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


@observe(name="brainstorm_identify_domains", capture_input=False)
def identify_domains(idea: str, model: str = MODEL) -> list[dict]:
    """Identify 2-3 domain-expert personas relevant to `idea`.

    Returns a list of `{"id", "name", "domain", "blurb"}` dicts. `id` is
    derived server-side by slugifying `name`.
    """
    client = get_openai_client()
    response = client.chat.completions.create(
        model=model,
        max_tokens=512,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": DOMAIN_SYSTEM_PROMPT},
            {"role": "user", "content": idea},
        ],
    )
    raw = response.choices[0].message.content or "{}"
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    data = json.loads(raw)
    personas = data.get("personas", [])
    if len(personas) < 2:
        raise ValueError(f"Expected at least 2 personas, got {len(personas)}")
    personas = personas[:3]

    result = [
        {
            "id": _slugify(p["name"]),
            "name": p["name"],
            "domain": p["domain"],
            "blurb": p["blurb"],
        }
        for p in personas
    ]

    update_current_span(input={"idea": idea}, output=result)
    return result


def _render_transcript(transcript: list[dict]) -> str:
    if not transcript:
        return "(no turns yet — this is the opening round; respond to the idea above)"
    return "\n\n".join(f"**{t['speaker']}:**\n{t['text']}" for t in transcript)


@observe(name="brainstorm_expert_turn", capture_input=False)
def stream_expert_turn(
    persona: dict,
    idea: str,
    transcript: list[dict],
    personas: list[dict],
    model: str = MODEL,
) -> Iterator[str]:
    """Stream one persona's turn given the idea and full transcript so far."""
    other_names = ", ".join(p["name"] for p in personas if p["id"] != persona["id"])
    system_prompt = EXPERT_SYSTEM_PROMPT_TEMPLATE.format(
        name=persona["name"],
        domain=persona["domain"],
        blurb=persona["blurb"],
        idea=idea,
        n_personas=len(personas),
        other_names=other_names,
        transcript_block=_render_transcript(transcript),
    )

    parts: list[str] = []
    for delta in stream_chat(system_prompt, "Respond now.", [], model):
        parts.append(delta)
        yield delta

    update_current_span(
        input={"persona": persona["id"], "transcript_len": len(transcript)},
        output="".join(parts),
    )


def extract_verdict(full_text: str) -> tuple[str, str]:
    """Split a persona's reply into (display_text, verdict).

    `verdict` is "AGREE" or "CONTINUE". Fails open to "CONTINUE" if no
    verdict marker is found — a parsing miss must never silently end the
    conversation.
    """
    matches = list(VERDICT_RE.finditer(full_text))
    if not matches:
        return full_text.strip(), "CONTINUE"
    m = matches[-1]
    display = (full_text[: m.start()] + full_text[m.end():]).strip()
    return display, m.group(1).upper()


@observe(name="brainstorm_synthesis", capture_input=False)
def stream_synthesis(idea: str, transcript: list[dict], model: str = MODEL) -> Iterator[str]:
    """Stream a synthesized Agreements/Objections/Refinements verdict."""
    user_prompt = f"IDEA:\n{idea}\n\nTRANSCRIPT:\n\n{_render_transcript(transcript)}"

    parts: list[str] = []
    for delta in stream_chat(SYNTHESIS_SYSTEM_PROMPT, user_prompt, [], model):
        parts.append(delta)
        yield delta

    update_current_span(input={"idea": idea, "transcript_len": len(transcript)}, output="".join(parts))
