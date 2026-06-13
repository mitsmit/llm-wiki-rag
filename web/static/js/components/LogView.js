import { html, React } from "../html.js";
import { getLog } from "../api.js";
import { renderMarkdown } from "../markdown.js";

const { useEffect, useState } = React;

export function LogView() {
  const [content, setContent] = useState(null);

  useEffect(() => {
    getLog().then((data) => setContent(data.content)).catch(() => setContent(""));
  }, []);

  return html`
    <div class="log-view">
      <h1>📋 Operation Log</h1>
      ${content === null && html`<p>Loading…</p>`}
      ${content !== null && html`
        <div class="markdown-body" dangerouslySetInnerHTML=${{ __html: renderMarkdown(content) }}></div>
      `}
    </div>
  `;
}
