import { html, React } from "../html.js";
import { getSessionId, streamQuery } from "../api.js";
import { renderMarkdown } from "../markdown.js";
import { IconSearch } from "../icons.js";

const { useState } = React;

// Front-page wiki Q&A: streams the same full-wiki-context answer as
// ComparePanel's "Wiki" pane (`/api/query/wiki`), without the RAG pane,
// excerpts, or save controls — those stay in Compare.
//
// Split into a form (always full-width, fixed height, rendered above the
// Desk grid) and an answer block (rendered inside the left desk-column) so
// a growing answer only pushes "Recent reads"/"Recent threads" down, not
// the "Needs attention"/"From the shelf" column on the right.
export function useAskWiki() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function onSubmit(e) {
    e.preventDefault();
    const q = question.trim();
    if (!q || loading) return;

    setLoading(true);
    setAnswer("");
    setError(null);

    const body = { question: q, session_id: getSessionId(), history: [] };
    try {
      await streamQuery("/api/query/wiki", body, (evt) => {
        if (evt.type === "token") setAnswer((prev) => prev + evt.data);
        else if (evt.type === "error") setError(evt.data);
      });
    } catch (err) {
      setError(String(err));
    } finally {
      setLoading(false);
    }
  }

  return { question, setQuestion, answer, loading, error, onSubmit };
}

export function AskForm({ question, setQuestion, loading, onSubmit }) {
  return html`
    <form class="ask-form" onSubmit=${onSubmit}>
      <${IconSearch} size=${18} />
      <input
        type="text"
        value=${question}
        onInput=${(e) => setQuestion(e.target.value)}
        placeholder="Ask the wiki anything…"
        disabled=${loading}
      />
      <button class="btn" type="submit" disabled=${loading}>${loading ? "Asking…" : "Ask"}</button>
    </form>
  `;
}

export function AskAnswer({ answer, loading, error }) {
  if (!answer && !loading && !error) return null;
  return html`
    <div class="ask-result">
      ${error && html`<div class="error">${error}</div>`}
      ${loading && !answer && !error && html`<p class="subtitle">Thinking…</p>`}
      ${answer && html`<div class="answer ask-answer" dangerouslySetInnerHTML=${{ __html: renderMarkdown(answer) }}></div>`}
      ${answer && !loading && html`
        <p class="subtitle">Want RAG citations side-by-side, or to save this answer? <a href="#/compare">Open in Compare →</a></p>
      `}
    </div>
  `;
}
