import { html, React } from "../html.js";
import { getHeadlines, reindex } from "../api.js";
import { LangfuseLink } from "./LangfuseLink.js";

const { useEffect, useState } = React;

export function HeadlinesView() {
  const [headlines, setHeadlines] = useState(null);
  const [reindexing, setReindexing] = useState(false);
  const [reindexResult, setReindexResult] = useState(null);

  useEffect(() => {
    getHeadlines(10).then(setHeadlines).catch(() => setHeadlines([]));
  }, []);

  async function onReindex() {
    setReindexing(true);
    setReindexResult(null);
    try {
      const result = await reindex();
      setReindexResult(result);
      if (result.status === "ok") {
        getHeadlines(10).then(setHeadlines).catch(() => {});
      }
    } catch (e) {
      setReindexResult({ status: "error", error: String(e) });
    } finally {
      setReindexing(false);
    }
  }

  return html`
    <div class="headlines-view">
      <div class="headlines-header">
        <div>
          <h1>📰 Latest Sources</h1>
          <p class="subtitle">
            Recently ingested documents. Start here, then head to
            <a href="#/compare">Compare</a> to research with the wiki and RAG side by side.
          </p>
        </div>
        <div class="headlines-actions">
          <${LangfuseLink} />
          <button class="btn" disabled=${reindexing} onClick=${onReindex}>
            ${reindexing ? "🔄 Reindexing…" : "🔄 Reindex"}
          </button>
        </div>
      </div>

      ${reindexResult && html`
        <div class="reindex-result">
          ${reindexResult.status === "ok"
            ? html`Reindex complete — ${reindexResult.sources} sources, ${reindexResult.pages} pages
                    (added ${reindexResult.added}, updated ${reindexResult.updated}, removed ${reindexResult.removed}).`
            : html`Reindex failed: ${reindexResult.error}`}
        </div>
      `}

      ${headlines === null && html`<p>Loading…</p>`}
      ${headlines && headlines.length === 0 && html`<p>No sources yet — add raw documents and run INGEST.</p>`}

      <div class="headline-list">
        ${headlines && headlines.map((item) => html`
          <article class="headline-card" key=${item.slug}>
            <div class="headline-meta">
              <span class="headline-date">${item.created}</span>
              ${item.tags.map((tag) => html`<span class="tag" key=${tag}>${tag}</span>`)}
            </div>
            <h2><a href="#/page/${item.page_path}">${item.title}</a></h2>
            <p class="headline-excerpt">${item.excerpt}</p>
          </article>
        `)}
      </div>
    </div>
  `;
}
