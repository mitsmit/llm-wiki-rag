import { html, React } from "../html.js";
import { getSessionId, saveAnalysis, streamQuery } from "../api.js";
import { renderMarkdown } from "../markdown.js";
import { LangfuseLink } from "./LangfuseLink.js";
import { IconBookOpen, IconFlaskConical, IconGitCompare, IconPaperclip, IconSave } from "../icons.js";

const { useState } = React;

export function ComparePanel() {
  const [question, setQuestion] = useState("");
  const [wikiAnswer, setWikiAnswer] = useState("");
  const [ragAnswer, setRagAnswer] = useState("");
  const [excerpts, setExcerpts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({ wiki: null, rag: null });
  const [saveSlug, setSaveSlug] = useState("");
  const [saveStatus, setSaveStatus] = useState(null);

  async function onSubmit(e) {
    e.preventDefault();
    const q = question.trim();
    if (!q || loading) return;

    setLoading(true);
    setWikiAnswer("");
    setRagAnswer("");
    setExcerpts([]);
    setErrors({ wiki: null, rag: null });
    setSaveStatus(null);

    const body = { question: q, session_id: getSessionId(), history: [] };

    const wikiPromise = streamQuery("/api/query/wiki", body, (evt) => {
      if (evt.type === "token") setWikiAnswer((prev) => prev + evt.data);
      else if (evt.type === "error") setErrors((prev) => ({ ...prev, wiki: evt.data }));
    }).catch((err) => setErrors((prev) => ({ ...prev, wiki: String(err) })));

    const ragPromise = streamQuery("/api/query/rag", body, (evt) => {
      if (evt.type === "excerpts") setExcerpts(evt.data);
      else if (evt.type === "token") setRagAnswer((prev) => prev + evt.data);
      else if (evt.type === "error") setErrors((prev) => ({ ...prev, rag: evt.data }));
    }).catch((err) => setErrors((prev) => ({ ...prev, rag: String(err) })));

    await Promise.all([wikiPromise, ragPromise]);
    setLoading(false);
  }

  async function onSave() {
    const slug = saveSlug.trim();
    if (!slug || !wikiAnswer) return;
    setSaveStatus("Saving…");
    try {
      const result = await saveAnalysis(slug, question, wikiAnswer);
      setSaveStatus(result.path ? `Saved to ${result.path}` : `Error: ${JSON.stringify(result)}`);
    } catch (err) {
      setSaveStatus(`Error: ${err}`);
    }
  }

  return html`
    <div class="compare-panel">
      <div class="compare-header">
        <div>
          <h1 class="icon-heading"><${IconGitCompare} size=${22} /> Knowledge Base</h1>
          <p class="subtitle">
            Ask one question, get two answers side by side: a full-wiki-context answer
            and a hybrid-RAG answer with retrieved excerpts.
          </p>
        </div>
        <${LangfuseLink} />
      </div>
      <form class="compare-form" onSubmit=${onSubmit}>
        <input
          type="text"
          value=${question}
          onInput=${(e) => setQuestion(e.target.value)}
          placeholder="Ask a question…"
          disabled=${loading}
        />
        <button class="btn" type="submit" disabled=${loading}>${loading ? "Asking…" : "Ask"}</button>
      </form>

      <div class="compare-panes">
        <section class="pane">
          <h2 class="icon-heading"><${IconBookOpen} size=${18} /> Wiki</h2>
          ${errors.wiki && html`<div class="error">${errors.wiki}</div>`}
          <div class="answer" dangerouslySetInnerHTML=${{ __html: renderMarkdown(wikiAnswer) }}></div>
          ${wikiAnswer && !loading && html`
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

        <section class="pane">
          <h2 class="icon-heading"><${IconFlaskConical} size=${18} /> RAG</h2>
          ${errors.rag && html`<div class="error">${errors.rag}</div>`}
          ${excerpts.length > 0 && html`
            <details class="excerpts">
              <summary><${IconPaperclip} size=${14} /> ${excerpts.length} retrieved excerpts</summary>
              <ul>
                ${excerpts.map((c, i) => html`
                  <li key=${i}>
                    <code>${c.path}</code> — ${c.title}
                    (rerank ${c.rerank_score != null ? c.rerank_score.toFixed(3) : "—"},
                     hybrid ${c.score != null ? c.score.toFixed(3) : "—"})
                  </li>
                `)}
              </ul>
            </details>
          `}
          <div class="answer" dangerouslySetInnerHTML=${{ __html: renderMarkdown(ragAnswer) }}></div>
        </section>
      </div>
    </div>
  `;
}
