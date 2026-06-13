import { html, React } from "../html.js";
import { getPage } from "../api.js";
import { renderMarkdown } from "../markdown.js";

const { useEffect, useState } = React;

const TYPE_BADGES = {
  source: "📄 Source",
  concept: "💡 Concept",
  entity: "🏢 Entity",
  analysis: "🔬 Analysis",
};

export function PageView({ path }) {
  const [page, setPage] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    setPage(null);
    setError(null);
    getPage(path)
      .then((data) => {
        if (data.detail) setError(data.detail);
        else setPage(data);
      })
      .catch((e) => setError(String(e)));
  }, [path]);

  if (error) return html`<div class="error">Error: ${error}</div>`;
  if (!page) return html`<p>Loading…</p>`;

  return html`
    <div class="page-view">
      <h1>${page.title}</h1>
      <div class="page-meta">${TYPE_BADGES[page.type] || "📝"} · <code>${page.path}</code></div>
      <hr />
      <div class="markdown-body" dangerouslySetInnerHTML=${{ __html: renderMarkdown(page.content) }}></div>
    </div>
  `;
}
