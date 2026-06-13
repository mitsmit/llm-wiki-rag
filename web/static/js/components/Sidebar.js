import { html, React } from "../html.js";
import { getPages, getStats } from "../api.js";
import {
  IconBookOpen,
  IconBuilding2,
  IconClipboardList,
  IconCompass,
  IconFile,
  IconFlaskConical,
  IconGitCompare,
  IconHome,
  IconLightbulb,
  IconMap,
  IconUsers,
} from "../icons.js";

const { useEffect, useState } = React;

const GROUP_LABELS = {
  concept: { icon: IconLightbulb, label: "Concepts" },
  entity: { icon: IconBuilding2, label: "Entities" },
  analysis: { icon: IconFlaskConical, label: "Analyses" },
  other: { icon: IconFile, label: "Other" },
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
      <div class="sidebar-top">
        <h1 class="sidebar-title"><${IconBookOpen} size=${20} /> LLM Wiki</h1>
        ${stats && html`<div class="sidebar-stats">${stats.sources} sources · ${stats.pages} pages</div>`}

        <a class="btn sidebar-discover ${route.name === "research" ? "active" : ""}" href="#/research">
          <${IconCompass} size=${18} /> Discover
        </a>

        <div class="sidebar-section">
          <a class="nav-item ${route.name === "home" ? "active" : ""}" href="#/"><${IconHome} size=${16} /> Today</a>
          <a class="nav-item ${route.name === "compare" ? "active" : ""}" href="#/compare"><${IconGitCompare} size=${16} /> Knowledge Base</a>
          <a class="nav-item ${route.name === "brainstorm" ? "active" : ""}" href="#/brainstorm"><${IconUsers} size=${16} /> Brainstorm</a>
          ${pages && pages.overview && html`
            <a class="nav-item ${isPage(pages.overview) ? "active" : ""}" href="#/page/${pages.overview}"><${IconMap} size=${16} /> Wiki Overview</a>
          `}
        </div>
      </div>

      <div class="sidebar-scroll">
        ${pages && Object.entries(GROUP_LABELS).map(([key, group]) => {
          const items = (pages.groups && pages.groups[key]) || [];
          if (items.length === 0) return null;
          return html`
            <div class="sidebar-section" key=${key}>
              <div class="sidebar-section-label"><${group.icon} size=${14} /> ${group.label}</div>
              ${items.map((item) => html`
                <a class="nav-item nav-item-page ${isPage(item.path) ? "active" : ""}"
                   href="#/page/${item.path}" key=${item.path}>${item.title}</a>
              `)}
            </div>
          `;
        })}
        <div class="sidebar-section">
          <a class="nav-item ${route.name === "log" ? "active" : ""}" href="#/log"><${IconClipboardList} size=${16} /> Log</a>
        </div>
      </div>
    </nav>
  `;
}
