import { html, React } from "../html.js";
import { getSessionId, saveBrainstorm, startBrainstorm, streamQuery } from "../api.js";
import { renderMarkdown } from "../markdown.js";
import { IconSave, IconUsers } from "../icons.js";

const { useState } = React;

const MAX_ROUNDS = 6; // mirrors web/brainstorm.py's MAX_ROUNDS

function buildTranscript(rounds, personas) {
  const turns = [];
  for (const round of rounds) {
    turns.push({ speaker: "You", text: round.userText, verdict: null });
    for (const p of personas) {
      const agent = round.agents[p.id];
      if (agent) turns.push({ speaker: p.name, text: agent.text, verdict: agent.verdict });
    }
  }
  return turns;
}

export function BrainstormView() {
  const [idea, setIdea] = useState("");
  const [followUp, setFollowUp] = useState("");
  const [personas, setPersonas] = useState(null);
  const [rounds, setRounds] = useState([]);
  const [streaming, setStreaming] = useState({});
  const [phase, setPhase] = useState("idea"); // idea | discussing | concluding | concluded
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [banner, setBanner] = useState(null);
  const [verdict, setVerdict] = useState("");
  const [saveSlug, setSaveSlug] = useState("");
  const [saveStatus, setSaveStatus] = useState(null);

  async function runRound(userText, personasList, priorRounds) {
    setLoading(true);
    setStreaming({});
    setBanner(null);
    setError(null);

    const newRounds = [...priorRounds, { userText, agents: {} }];
    setRounds(newRounds);

    const transcript = [
      ...buildTranscript(priorRounds, personasList),
      { speaker: "You", text: userText, verdict: null },
    ];

    let agreedPersona = null;

    try {
      await streamQuery(
        "/api/brainstorm/turn",
        { idea, personas: personasList, transcript, session_id: getSessionId() },
        (evt) => {
          if (evt.type === "token") {
            setStreaming((prev) => ({ ...prev, [evt.agent_id]: (prev[evt.agent_id] || "") + evt.data }));
          } else if (evt.type === "agent_done") {
            if (evt.verdict === "AGREE") {
              const p = personasList.find((p) => p.id === evt.agent_id);
              if (p) agreedPersona = p.name;
            }
            setRounds((prev) => {
              const next = [...prev];
              const last = { ...next[next.length - 1] };
              last.agents = { ...last.agents, [evt.agent_id]: { text: evt.text, verdict: evt.verdict } };
              next[next.length - 1] = last;
              return next;
            });
          } else if (evt.type === "error") {
            setRounds((prev) => {
              const next = [...prev];
              const last = { ...next[next.length - 1] };
              last.agents = { ...last.agents, [evt.agent_id]: { text: `_Error: ${evt.data}_`, verdict: "CONTINUE" } };
              next[next.length - 1] = last;
              return next;
            });
          }
        }
      );
    } catch (err) {
      setError(String(err));
    } finally {
      setLoading(false);
      setPhase("discussing");
      if (agreedPersona) setBanner(agreedPersona);
    }
  }

  async function onStart(e) {
    e.preventDefault();
    const text = idea.trim();
    if (!text || loading) return;

    setLoading(true);
    setError(null);
    try {
      const result = await startBrainstorm(text, getSessionId());
      if (!result.personas) {
        setError(result.detail || "Could not identify expert personas for this idea.");
        setLoading(false);
        return;
      }
      setPersonas(result.personas);
      setPhase("discussing");
      await runRound(text, result.personas, []);
    } catch (err) {
      setError(String(err));
      setLoading(false);
    }
  }

  async function onFollowUp(e) {
    e.preventDefault();
    const text = followUp.trim();
    if (!text || loading) return;
    setFollowUp("");
    await runRound(text, personas, rounds);
  }

  async function onConclude() {
    setPhase("concluding");
    setVerdict("");
    setError(null);
    try {
      await streamQuery(
        "/api/brainstorm/conclude",
        { idea, transcript: buildTranscript(rounds, personas), session_id: getSessionId() },
        (evt) => {
          if (evt.type === "token") setVerdict((prev) => prev + evt.data);
          else if (evt.type === "error") setError(evt.data);
        }
      );
    } catch (err) {
      setError(String(err));
    } finally {
      setPhase("concluded");
    }
  }

  async function onSave() {
    const slug = saveSlug.trim();
    if (!slug || !verdict) return;
    setSaveStatus("Saving…");
    try {
      const result = await saveBrainstorm({
        slug,
        idea,
        personas,
        transcript: buildTranscript(rounds, personas),
        verdict,
      });
      setSaveStatus(result.path ? `Saved to ${result.path}` : `Error: ${JSON.stringify(result)}`);
    } catch (err) {
      setSaveStatus(`Error: ${err}`);
    }
  }

  return html`
    <div class="brainstorm-view">
      <div>
        <h1 class="icon-heading"><${IconUsers} size=${22} /> Brainstorm</h1>
        <p class="subtitle">
          Pitch an idea. 2-3 domain-expert agents will support, critique, refine, and
          question it across a multi-round discussion — wrap up whenever you're ready.
        </p>
      </div>

      ${phase === "idea" && html`
        <form class="brainstorm-form" onSubmit=${onStart}>
          <textarea
            value=${idea}
            onInput=${(e) => setIdea(e.target.value)}
            placeholder="Describe the idea or proposal you want to stress-test…"
            disabled=${loading}
          ></textarea>
          <button class="btn" type="submit" disabled=${loading}>
            ${loading ? "Assembling experts…" : "Start Brainstorm"}
          </button>
        </form>
      `}

      ${error && html`<div class="error">${error}</div>`}

      ${personas && html`
        <div class="brainstorm-rounds">
          ${rounds.map((round, i) => html`
            <div class="round-block" key=${i}>
              <div class="user-turn">${round.userText}</div>
              <div class="agent-pane-row" style=${{ "--n": personas.length }}>
                ${personas.map((p) => {
                  const agent = round.agents[p.id];
                  const isLast = i === rounds.length - 1;
                  const text = agent ? agent.text : (isLast ? (streaming[p.id] || "") : "");
                  return html`
                    <section class="pane agent-pane" key=${p.id}>
                      <header class="agent-pane-header">
                        <span class="agent-name">${p.name}</span>
                        <span class="agent-domain">${p.domain}</span>
                        ${agent && html`
                          <span class="verdict-badge verdict-${agent.verdict.toLowerCase()}">
                            ${agent.verdict === "AGREE" ? "Agrees" : "More to discuss"}
                          </span>
                        `}
                      </header>
                      <div class="answer" dangerouslySetInnerHTML=${{ __html: renderMarkdown(text) }}></div>
                    </section>
                  `;
                })}
              </div>
            </div>
          `)}
        </div>
      `}

      ${banner && phase === "discussing" && html`
        <div class="brainstorm-banner">
          <span><strong>${banner}</strong> has no further objections — wrap up and synthesize a verdict?</span>
          <button class="btn" onClick=${onConclude}>Wrap up</button>
          <button class="btn btn-secondary" onClick=${() => setBanner(null)}>Continue</button>
        </div>
      `}

      ${phase === "discussing" && html`
        <div>
          ${rounds.length >= MAX_ROUNDS && html`
            <p class="subtitle">You've reached ${rounds.length} rounds — consider wrapping up.</p>
          `}
          <form class="brainstorm-followup" onSubmit=${onFollowUp}>
            <input
              type="text"
              value=${followUp}
              onInput=${(e) => setFollowUp(e.target.value)}
              placeholder="Respond, refine, or push back…"
              disabled=${loading}
            />
            <button class="btn" type="submit" disabled=${loading || !followUp.trim()}>
              ${loading ? "Thinking…" : "Send"}
            </button>
            <button class="btn btn-secondary" type="button" disabled=${loading} onClick=${onConclude}>
              Wrap up
            </button>
          </form>
        </div>
      `}

      ${(phase === "concluding" || phase === "concluded") && html`
        <section class="pane brainstorm-verdict">
          <h2>Verdict</h2>
          ${phase === "concluding" && !verdict && html`<p class="subtitle">Synthesizing…</p>`}
          <div class="answer" dangerouslySetInnerHTML=${{ __html: renderMarkdown(verdict) }}></div>
          ${phase === "concluded" && verdict && html`
            <div class="save-row">
              <input
                type="text"
                placeholder="analysis-slug"
                value=${saveSlug}
                onInput=${(e) => setSaveSlug(e.target.value)}
              />
              <button class="btn btn-secondary" onClick=${onSave}><${IconSave} size=${16} /> Save</button>
              ${saveStatus && html`<span class="save-status">${saveStatus}</span>`}
            </div>
          `}
        </section>
      `}
    </div>
  `;
}
