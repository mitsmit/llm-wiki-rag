import { html, React } from "../html.js";
import { getActivity, getHeadlines, getInbox, getPages, getResearchHistory, reindex } from "../api.js";
import { getDriftNote, getFocusTagCounts, getRecentReads, pickFromShelf } from "../focus.js";
import { AskAnswer, AskForm, useAskWiki } from "./AskBox.js";
import { LangfuseLink } from "./LangfuseLink.js";
import { TYPE_BADGES } from "./PageView.js";
import {
  IconBookmark,
  IconCompass,
  IconFile,
  IconHistory,
  IconHome,
  IconInbox,
  IconNewspaper,
  IconRefreshCw,
} from "../icons.js";

const { useEffect, useState } = React;

const SHELF_TYPES = ["concept", "entity", "analysis"];

export function DeskView() {
  const [recentReads] = useState(() => getRecentReads(4));
  const [fallbackHeadlines, setFallbackHeadlines] = useState(null);
  const [activity, setActivity] = useState(null);
  const [inbox, setInbox] = useState(null);
  const [lastSearch, setLastSearch] = useState(null);
  const [shelf, setShelf] = useState(null);
  const [driftNote, setDriftNote] = useState(null);
  const [reindexing, setReindexing] = useState(false);
  const [reindexResult, setReindexResult] = useState(null);
  const ask = useAskWiki();

  function refreshShelf() {
    getPages().then((pages) => {
      const candidates = [];
      for (const type of SHELF_TYPES) {
        for (const item of (pages.groups && pages.groups[type]) || []) {
          candidates.push({ ...item, type });
        }
      }
      const focusCounts = getFocusTagCounts();
      setShelf(pickFromShelf(candidates, focusCounts));
      setDriftNote(getDriftNote(focusCounts));
    }).catch(() => {});
  }

  useEffect(() => {
    if (recentReads.length === 0) {
      getHeadlines(4).then(setFallbackHeadlines).catch(() => setFallbackHeadlines([]));
    }
    getActivity(4).then(setActivity).catch(() => setActivity([]));
    getInbox().then(setInbox).catch(() => setInbox({ count: 0, items: [] }));
    getResearchHistory().then((items) => setLastSearch(items[0] || null)).catch(() => setLastSearch(null));
    refreshShelf();
  }, []);

  async function onReindex() {
    setReindexing(true);
    setReindexResult(null);
    try {
      const result = await reindex();
      setReindexResult(result);
      if (result.status === "ok") {
        if (recentReads.length === 0) getHeadlines(4).then(setFallbackHeadlines).catch(() => {});
        refreshShelf();
      }
    } catch (e) {
      setReindexResult({ status: "error", error: String(e) });
    } finally {
      setReindexing(false);
    }
  }

  const needsAttention = (inbox && inbox.count > 0) || lastSearch;
  const shelfBadge = shelf ? (TYPE_BADGES[shelf.type] || { icon: IconFile, label: "Other" }) : null;

  return html`
    <div class="desk-view">
      <div class="desk-header">
        <div>
          <h1 class="icon-heading"><${IconHome} size=${22} /> Today</h1>
          <p class="subtitle">
            What's on your desk right now. Everything else lives in the sidebar.
          </p>
        </div>
        <div class="desk-actions">
          <${LangfuseLink} />
          <button class="btn" disabled=${reindexing} onClick=${onReindex}>
            <${IconRefreshCw} size=${16} class=${reindexing ? "icon-spin" : ""} />
            ${reindexing ? "Reindexing…" : "Reindex"}
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

      <${AskForm} ...${ask} />

      <div class="desk-grid">
        <div class="desk-column">
          <${AskAnswer} ...${ask} />

          <section>
            <h2 class="desk-section-label icon-heading"><${IconNewspaper} size=${14} /> Recent reads</h2>
            ${recentReads.length === 0 && fallbackHeadlines === null && html`<p>Loading…</p>`}
            ${recentReads.length === 0 && fallbackHeadlines && fallbackHeadlines.length === 0 && html`<p>No sources yet — add raw documents and run INGEST.</p>`}
            ${recentReads.length === 0 && fallbackHeadlines && fallbackHeadlines.length > 0 && html`
              <p class="subtitle">Nothing read yet — here's what's newest.</p>
            `}
            <div class="headline-list">
              ${recentReads.length > 0
                ? recentReads.map((item) => {
                    const badge = TYPE_BADGES[item.type] || { icon: IconFile, label: "Other" };
                    return html`
                      <article class="headline-card" key=${item.path}>
                        <div class="headline-meta">
                          <span class="icon-heading"><${badge.icon} size=${12} /> ${badge.label}</span>
                          <span class="headline-date">${new Date(item.ts).toLocaleDateString()}</span>
                          ${item.tags.map((tag) => html`<span class="tag" key=${tag}>${tag}</span>`)}
                        </div>
                        <h2><a href="#/page/${item.path}">${item.title}</a></h2>
                        ${item.excerpt && html`<p class="headline-excerpt">${item.excerpt}</p>`}
                      </article>
                    `;
                  })
                : fallbackHeadlines && fallbackHeadlines.map((item) => html`
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
          </section>

          <section>
            <h2 class="desk-section-label icon-heading"><${IconHistory} size=${14} /> Recent threads</h2>
            ${activity === null && html`<p>Loading…</p>`}
            <div class="activity-list">
              ${activity && activity.map((entry, i) => html`
                <div class="activity-item" key=${i}>
                  <span class="activity-date">${entry.date}</span>
                  <div class="activity-body">
                    <span class="tag">${entry.operation}</span>
                    <strong>${entry.title}</strong>
                    ${entry.note && ` — ${entry.note}`}
                  </div>
                </div>
              `)}
            </div>
            <p class="subtitle"><a href="#/log">View full log →</a></p>
          </section>
        </div>

        <div class="desk-column">
          ${needsAttention && html`
            <section>
              <h2 class="desk-section-label icon-heading"><${IconInbox} size=${14} /> Needs attention</h2>
              <div class="attention-card">
                ${inbox && inbox.count > 0 && html`
                  <div>
                    <span class="icon-heading">
                      <${IconInbox} size=${16} />
                      ${inbox.count} file${inbox.count === 1 ? "" : "s"} waiting in <code>raw/</code>
                    </span>
                    <ul class="attention-list">
                      ${inbox.items.slice(0, 3).map((item) => html`<li key=${item.filename}><code>${item.filename}</code></li>`)}
                      ${inbox.count > 3 && html`<li>+${inbox.count - 3} more</li>`}
                    </ul>
                    <p class="subtitle">Run INGEST to add ${inbox.count === 1 ? "it" : "them"} to the wiki.</p>
                  </div>
                `}
                ${lastSearch && html`
                  <div>
                    <span class="icon-heading"><${IconCompass} size=${16} /> Last search</span>
                    <p class="subtitle">
                      "${lastSearch.label}" (${lastSearch.date}) —
                      <a href="#/research">continue in Discover →</a>
                    </p>
                  </div>
                `}
              </div>
            </section>
          `}

          ${shelf && html`
            <section>
              <h2 class="desk-section-label icon-heading"><${IconBookmark} size=${14} /> From the shelf</h2>
              <div class="shelf-card">
                <p class="shelf-note">
                  ${driftNote
                    ? html`Lots of <strong>${driftNote.tag}</strong> lately — here's a change of scene:`
                    : "Worth revisiting:"}
                </p>
                <div class="page-meta"><${shelfBadge.icon} size=${14} /> ${shelfBadge.label}</div>
                <h3><a href="#/page/${shelf.path}">${shelf.title}</a></h3>
              </div>
            </section>
          `}
        </div>
      </div>
    </div>
  `;
}
