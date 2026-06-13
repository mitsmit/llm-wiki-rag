import { html, React } from "../html.js";
import { getConfig } from "../api.js";
import { IconBarChart } from "../icons.js";

const { useEffect, useState } = React;

// Link to the Langfuse project's traces UI. Renders nothing if tracing
// isn't configured (no LANGFUSE_* keys in .env).
export function LangfuseLink() {
  const [url, setUrl] = useState(null);

  useEffect(() => {
    getConfig().then((cfg) => setUrl(cfg.langfuse_url)).catch(() => {});
  }, []);

  if (!url) return null;

  return html`
    <a class="btn btn-secondary" href=${url} target="_blank" rel="noopener noreferrer">
      <${IconBarChart} size=${16} /> Langfuse Traces
    </a>
  `;
}
