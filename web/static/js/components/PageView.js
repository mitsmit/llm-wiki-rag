import { html, React } from "../html.js";
import { getPage } from "../api.js";
import { renderMarkdown } from "../markdown.js";
import { recordView } from "../focus.js";
import { splitSections, joinSections, RELATED_HEADING_RE, CHALLENGES_HEADING_RE } from "../sections.js";
import { IconAlertTriangle, IconBuilding2, IconFile, IconFileText, IconFlaskConical, IconLightbulb } from "../icons.js";

const { useEffect, useMemo, useState } = React;

export const TYPE_BADGES = {
  source: { icon: IconFileText, label: "Source" },
  concept: { icon: IconLightbulb, label: "Concept" },
  entity: { icon: IconBuilding2, label: "Entity" },
  analysis: { icon: IconFlaskConical, label: "Analysis" },
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
        else {
          setPage(data);
          recordView(data.path, { tags: data.tags, title: data.title, type: data.type, excerpt: data.excerpt });
        }
      })
      .catch((e) => setError(String(e)));
  }, [path]);

  // Pull the "Related Concepts" section out of the normal reading-order flow
  // into a sidebar visible from the top of the page. "Challenges" stays in
  // its original position but renders as a highlighted callout for prominence.
  const layout = useMemo(() => {
    if (!page) return null;
    const sections = splitSections(page.content);

    const relatedIdx = sections.findIndex((s) => RELATED_HEADING_RE.test(s.heading || ""));
    const related = relatedIdx >= 0 ? sections.splice(relatedIdx, 1)[0] : null;

    const challengeIdx = sections.findIndex((s) => CHALLENGES_HEADING_RE.test(s.heading || ""));
    const challenge = challengeIdx >= 0 ? sections[challengeIdx] : null;
    const before = challengeIdx >= 0 ? sections.slice(0, challengeIdx) : sections;
    const after = challengeIdx >= 0 ? sections.slice(challengeIdx + 1) : [];

    return {
      beforeHtml: renderMarkdown(joinSections(before)),
      afterHtml: renderMarkdown(joinSections(after)),
      related,
      relatedHtml: related ? renderMarkdown(related.body) : null,
      challenge,
      challengeHtml: challenge ? renderMarkdown(challenge.body) : null,
    };
  }, [page]);

  if (error) return html`<div class="error">Error: ${error}</div>`;
  if (!page) return html`<p>Loading…</p>`;

  const badge = TYPE_BADGES[page.type] || { icon: IconFile, label: "Other" };

  return html`
    <div class="page-view">
      <h1>${page.title}</h1>
      <div class="page-meta"><${badge.icon} size=${14} /> ${badge.label} · <code>${page.path}</code></div>
      <hr />
      <div class=${`page-layout${layout.related ? "" : " page-layout--full"}`}>
        <div class="page-main">
          <div class="markdown-body" dangerouslySetInnerHTML=${{ __html: layout.beforeHtml }}></div>
          ${layout.challenge && html`
            <div class="callout callout-challenges">
              <div class="callout-label icon-heading"><${IconAlertTriangle} size=${14} /> ${layout.challenge.heading}</div>
              <div class="markdown-body" dangerouslySetInnerHTML=${{ __html: layout.challengeHtml }}></div>
            </div>
          `}
          <div class="markdown-body" dangerouslySetInnerHTML=${{ __html: layout.afterHtml }}></div>
        </div>
        ${layout.related && html`
          <aside class="page-sidebar">
            <div class="sidebar-card">
              <div class="sidebar-card-label">${layout.related.heading}</div>
              <div class="markdown-body" dangerouslySetInnerHTML=${{ __html: layout.relatedHtml }}></div>
            </div>
          </aside>
        `}
      </div>
    </div>
  `;
}
