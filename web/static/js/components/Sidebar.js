import { html, React } from "../html.js";
import { getPages, getStats } from "../api.js";

const { useEffect, useState } = React;

const GROUP_LABELS = {
  source: "📄 Sources",
  concept: "💡 Concepts",
  entity: "🏢 Entities",
  analysis: "🔬 Analyses",
  other: "📝 Other",
};

export function Sidebar({ route }) {
  const [stats, setStats] = useState(null);
  const [pages, setPages] = useState(null);

  useEffect(() => {
    getStats().then(setStats).catch(() => {});
    getPages().then(setPages).catch(() => {});
  }, []);

  const isPage = (path) => route.name === "page" && route.path === path;

  return html`
    <nav class="sidebar">
      <h1 class="sidebar-title">📖 LLM Wiki</h1>
      ${stats && html`<div class="sidebar-stats">${stats.sources} sources · ${stats.pages} pages</div>`}

      <div class="sidebar-section">
        <a class="nav-item ${route.name === "headlines" ? "active" : ""}" href="#/">🏠 Headlines</a>
        <a class="nav-item ${route.name === "compare" ? "active" : ""}" href="#/compare">🔍↔🧪 Compare</a>
        <a class="nav-item ${route.name === "research" ? "active" : ""}" href="#/research">🔭 Discover</a>
        ${pages && pages.overview && html`
          <a class="nav-item ${isPage(pages.overview) ? "active" : ""}" href="#/page/${pages.overview}">🗺️ Overview</a>
        `}
        <a class="nav-item ${route.name === "log" ? "active" : ""}" href="#/log">📋 Log</a>
      </div>

      ${pages && Object.entries(GROUP_LABELS).map(([key, label]) => {
        const items = (pages.groups && pages.groups[key]) || [];
        if (items.length === 0) return null;
        return html`
          <div class="sidebar-section" key=${key}>
            <div class="sidebar-section-label">${label}</div>
            ${items.map((item) => html`
              <a class="nav-item nav-item-page ${isPage(item.path) ? "active" : ""}"
                 href="#/page/${item.path}" key=${item.path}>${item.title}</a>
            `)}
          </div>
        `;
      })}
    </nav>
  `;
}
