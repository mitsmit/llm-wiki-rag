import { html, React } from "../html.js";
import { getResearchHistory, getResearchResult, selectResearchItems, streamQuery } from "../api.js";
import { renderMarkdown } from "../markdown.js";
import { IconCompass, IconDownload, IconHistory, IconSearch, IconX } from "../icons.js";

const { useEffect, useState } = React;

export function ResearchView() {
  const [query, setQuery] = useState("");
  const [save, setSave] = useState(true);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(null);
  const [answer, setAnswer] = useState("");
  const [items, setItems] = useState(null);
  const [selected, setSelected] = useState(new Set());
  const [error, setError] = useState(null);
  const [history, setHistory] = useState(null);
  const [activeName, setActiveName] = useState(null);
  const [addResult, setAddResult] = useState(null);
  const [adding, setAdding] = useState(false);

  useEffect(() => {
    refreshHistory();
  }, []);

  function refreshHistory() {
    getResearchHistory().then(setHistory).catch(() => setHistory([]));
  }

  function resetResult() {
    setAnswer("");
    setItems(null);
    setSelected(new Set());
    setError(null);
    setAddResult(null);
    setStatus(null);
  }

  async function onSubmit(e) {
    e.preventDefault();
    const q = query.trim();
    if (!q || loading) return;

    resetResult();
    setActiveName(null);
    setLoading(true);

    try {
      await streamQuery("/api/research", { query: q, save }, (evt) => {
        if (evt.type === "status") setStatus(evt.data);
        else if (evt.type === "token") {
          setStatus(null);
          setAnswer((prev) => prev + evt.data);
        } else if (evt.type === "items") setItems(evt.data);
        else if (evt.type === "error") setError(evt.data);
      });
    } catch (err) {
      setError(String(err));
    } finally {
      setLoading(false);
      setStatus(null);
      refreshHistory();
    }
  }

  async function onLoadHistory(item) {
    resetResult();
    setQuery(item.label);
    setActiveName(item.name);
    const result = await getResearchResult(item.name);
    setAnswer(result.content);
    setItems(result.items);
  }

  function toggleSelected(i) {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(i)) next.delete(i);
      else next.add(i);
      return next;
    });
  }

  async function onAddSelected() {
    const picks = items.filter((_, i) => selected.has(i));
    if (picks.length === 0) return;
    setAdding(true);
    setAddResult(null);
    try {
      const result = await selectResearchItems(picks, query.trim() || "research");
      setAddResult(result);
      setSelected(new Set());
    } catch (err) {
      setAddResult({ added: [], skipped: [String(err)] });
    } finally {
      setAdding(false);
    }
  }

  function onClear() {
    setQuery("");
    setActiveName(null);
    resetResult();
  }

  const hasResult = answer || activeName;

  return html`
    <div class="research-view">
      <div class="research-header">
        <h1 class="icon-heading"><${IconCompass} size=${22} /> Discover</h1>
        <p class="subtitle">
          Enter a topic. The agent expands your query, searches arXiv + web (skipping
          anything already in the wiki or shown before), and ranks the best reads.
          Tick the ones worth ingesting to add them to <code>raw/</code>.
        </p>
      </div>

      <form class="research-form" onSubmit=${onSubmit}>
        <input
          type="text"
          value=${query}
          onInput=${(e) => setQuery(e.target.value)}
          placeholder="e.g. 'alignment faking in large language models'"
          disabled=${loading}
        />
        <label class="save-checkbox">
          <input type="checkbox" checked=${save} onChange=${(e) => setSave(e.target.checked)} disabled=${loading} />
          Save
        </label>
        <button class="btn" type="submit" disabled=${loading}>
          ${loading ? "Researching…" : html`<${IconSearch} size=${16} /> Research`}
        </button>
      </form>

      ${history && history.length > 0 && html`
        <details class="research-history">
          <summary><${IconHistory} size=${14} /> Past sessions (${history.length})</summary>
          <ul>
            ${history.map((item) => html`
              <li key=${item.name}>
                <a href="#" onClick=${(e) => { e.preventDefault(); onLoadHistory(item); }}>${item.label}</a>
                <span class="research-history-date">${item.date}</span>
              </li>
            `)}
          </ul>
        </details>
      `}

      ${error && html`<div class="error">${error}</div>`}
      ${status && html`<p class="research-status">${status}</p>`}

      ${hasResult && html`
        <div class="research-result">
          ${activeName && html`<p class="page-meta"><${IconHistory} size=${14} /> results/${activeName}</p>`}
          <div class="answer" dangerouslySetInnerHTML=${{ __html: renderMarkdown(answer) }}></div>
          <div class="research-actions">
            <button class="btn btn-secondary" onClick=${onClear}><${IconX} size=${16} /> Clear</button>
          </div>
        </div>
      `}

      ${items && items.length > 0 && html`
        <div class="research-selection">
          <h2>Add to wiki</h2>
          <p class="subtitle">Select items to pull into <code>raw/</code> for ingestion.</p>
          ${items.map((item, i) => html`
            <label class="research-item" key=${i}>
              <input type="checkbox" checked=${selected.has(i)} onChange=${() => toggleSelected(i)} />
              <div>
                <div class="research-item-title">
                  <strong>${item.title}</strong>${item.source ? ` — ${item.source}` : ""}${item.date ? ` · ${item.date}` : ""}
                </div>
                ${item.why_read_it && html`<div class="research-item-why">${item.why_read_it}</div>`}
              </div>
            </label>
          `)}
          <button class="btn" disabled=${selected.size === 0 || adding} onClick=${onAddSelected}>
            ${adding ? "Adding…" : html`<${IconDownload} size=${16} /> Add selected to wiki (raw/)`}
          </button>
          ${addResult && html`
            <div class="research-add-result">
              ${addResult.added && addResult.added.length > 0 && html`
                <div class="research-add-ok">
                  Added to wiki:
                  <ul>${addResult.added.map((a) => html`<li key=${a}><code>${a}</code></li>`)}</ul>
                </div>
              `}
              ${addResult.skipped && addResult.skipped.length > 0 && html`
                <div class="research-add-skip">Could not fetch: ${addResult.skipped.join("; ")}</div>
              `}
            </div>
          `}
        </div>
      `}

      ${!loading && !hasResult && !error && html`
        <div class="research-empty">
          <p><strong>How it works:</strong></p>
          <ol>
            <li>Enter any research topic above</li>
            <li>The agent expands your query into search variants</li>
            <li>Searches arXiv (papers) + web (articles, blogs, news) in parallel, skipping
                anything already in the wiki or shown in a past run</li>
            <li>Ranks candidates and returns the best reads</li>
            <li>Tick the ones worth ingesting — arXiv picks are fetched as PDFs into
                <code>raw/</code>, others are written as a "selected reading list" for
                the wiki agent to follow</li>
          </ol>
          <p>Past sessions are listed above once you've run a search.</p>
        </div>
      `}
    </div>
  `;
}
