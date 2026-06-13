# The Desk — landing page redesign

## Context

The landing view (`HeadlinesView.js`, route `""`/`"/"`) is currently a flat
reverse-chronological list of *all* `wiki/sources/*.md` pages — a filing
cabinet, not a workspace. The user's framing: the landing page should feel
like a study/reading room — surfacing what's relevant *right now* (recent
reads, open threads, pending items) in a small, calm, well-organized set of
zones, with a deliberate diversity mechanism so the room doesn't become an
echo chamber: it should sense when recent activity is narrowing toward one
topic and actively nudge toward something different. History stays
retrievable on demand (Sidebar nav / `#/log` already do this) — the landing
page shouldn't try to be the archive.

Investigation found real "on the desk" state that's currently invisible:
- `raw/` has ~9 files (PDFs from 2026-05-15 + earlier) never mentioned in
  `log.md` — i.e. dropped for ingestion but not yet processed.
- A Discover session ran today (2026-06-13, "World model against the
  generative model") with an unactioned reading list
  (`research-agent/results/2026-06-13-...md`).

These map directly onto "inbox tray" and "open notebook" — exactly the kind
of in-progress state a desk should surface.

---

## Concept → layout mapping

| Room element | Landing section | Data source |
|---|---|---|
| Open book on the desk | **Recent reads** (trimmed headlines, 4 items) | `GET /api/headlines?limit=4` (existing, has `tags`) |
| Notes pinned to the board | **Recent threads** (activity feed, 4 items) | NEW `GET /api/wiki/activity` |
| Inbox tray + open notebook | **Needs attention** (pending raw files + last Discover session) | NEW `GET /api/inbox` + existing `GET /api/research/history` |
| Pulled off the shelf, chosen *against* the grain | **From the shelf** (one resurfaced concept/entity/analysis, diversity-aware) | existing `GET /api/wiki/pages` (extended with `tags`), client-side focus tracker |

Only 4 zones, capped item counts, two of them (Needs attention / From the
shelf) intentionally small — this is what gives "minimum scrolling" and
avoids clutter. "Needs attention" disappears entirely if there's nothing
pending (no empty-state cards).

---

## 1. Backend additions

### `web/inbox.py` (new, mirrors `web/headlines.py` style)

```python
def get_inbox_items() -> list[dict]:
    """Files directly under raw/ not yet referenced anywhere in log.md
    (i.e. dropped for ingestion but not yet processed)."""
```
- List `raw/*` (skip dirs like `raw/assets/`, dotfiles).
- A file is "pending" if its filename is not a substring of `log.md`'s
  content (log entries already reference files as `` `raw/<name>` ``).
- Return `[{"filename": ..., "modified": "YYYY-MM-DD"}]`, sorted by mtime
  descending.

### `web/routes/inbox.py` (new)

```python
@router.get("/api/inbox")
def inbox() -> dict:
    items = get_inbox_items()
    return {"count": len(items), "items": items[:5]}
```
Register `app.include_router(inbox.router)` in `web/server.py`.

### `web/wiki_data.py` — add `parse_log_activity(limit=5)`

Regex-split `log.md` on `^## \[(\d{4}-\d{2}-\d{2})\]\s+(\S+)\s*\|\s*(.+)$`,
pull the first line of the `**Notes:**` bullet as a one-line summary, sort
by date descending (stable — preserves file order for same-date entries).
Return `[{"date", "operation", "title", "note"}]`.

### `web/wiki_data.py` — add `page_tags(content)`

Same pattern as the existing `page_type(content)`: regex-find the
frontmatter `tags: [...]` line, strip brackets/quotes, split on commas.
Returns `list[str]` (empty if absent).

### `web/routes/wiki.py` — extend existing endpoints

```python
@router.get("/api/wiki/activity")
def activity(limit: int = 5) -> list[dict]:
    return parse_log_activity(limit=limit)
```

- `page_tree()` (used by `/api/wiki/pages`): each item gains `"tags": page_tags(content)`.
- `page()` (used by `/api/wiki/page/{path}`): response gains
  `"tags": page_tags(content)`.

These two `tags` additions are the only data the diversity mechanism needs —
no new storage, no accounts.

---

## 2. Frontend API additions (`web/static/js/api.js`)

```js
export async function getActivity(limit = 5) {
  const res = await fetch(`/api/wiki/activity?limit=${limit}`);
  return res.json();
}
export async function getInbox() {
  const res = await fetch("/api/inbox");
  return res.json();
}
```
(`getHeadlines`, `getPages`, `getPage`, `getResearchHistory` already exist
and are reused as-is — `getPages`/`getPage` now also carry `tags`.)

---

## 3. Diversity sensing — focus tracker (`web/static/js/focus.js`, new)

A small local module, no backend involved — this is the concrete mechanism
behind "sense my interests over time and nudge toward diversity":

```js
const KEY_VIEWS = "llm_wiki_recent_views";   // rolling log of {path, tags, ts}
const KEY_SHELF = "llm_wiki_shelf_recent";   // last 3 shelf picks (avoid repeats)

export function recordView(path, tags) { /* append to KEY_VIEWS, cap at 20 */ }

export function getFocusTagCounts() {
  /* frequency map built from KEY_VIEWS entries (capped/rolling = "recent",
     not all-time) */
}

export function pickFromShelf(candidates, focusTagCounts) {
  /* score each candidate by *overlap* with focusTagCounts (lower = more
     diverse); weighted-random pick biased toward low-overlap candidates;
     exclude paths in KEY_SHELF; push the pick onto KEY_SHELF (cap at 3) */
}

export function getDriftNote(focusTagCounts) {
  /* if one tag accounts for >=50% of weighted recent focus, return
     {tag, share}; else null */
}
```

Wiring:
- `PageView.js` calls `recordView(page.path, page.tags)` once a page loads
  successfully — this is the "what have you been reading" signal.
- `DeskView.js` also seeds the counts with the tags from the 4 "Recent
  reads" headlines (so the signal isn't empty on a fresh browser/profile),
  then calls `pickFromShelf(candidates, focusTagCounts)` where `candidates`
  are all `concept`/`entity`/`analysis` pages from `getPages()` (excluding
  the overview page).
- If `getDriftNote()` returns non-null, the "From the shelf" card leads with
  *"Lots of **&lt;tag&gt;** lately — here's a change of scene:"*; otherwise it
  leads with *"Worth revisiting:"*. Either way the picked page (title + type
  badge, linking to `#/page/<path>`) follows.

This keeps the nudge legible (the user sees *why* something was surfaced)
and self-correcting (today's pick becomes tomorrow's `KEY_VIEWS`/`KEY_SHELF`
history), entirely client-side and reversible (clearing localStorage resets
it).

---

## 4. New icons (`web/static/js/icons.js`)

Two additions, same `IconBase` pattern as existing icons:
- `IconInbox` — Lucide-style inbox tray, for "Needs attention".
- `IconBookmark` — Lucide-style bookmark ribbon, for "From the shelf".

(`IconHistory`, `IconNewspaper`, `IconCompass`, `IconHome` already exist and
are reused for Recent threads / Recent reads / Discover-continuation /
header.)

---

## 5. New component `web/static/js/components/DeskView.js`

Replaces `HeadlinesView.js` (delete the old file once `DeskView.js` is
created and wired in). Keeps the Reindex button + `LangfuseLink` from the
current header (still useful utility actions), moved into a slim header
strip.

Structure:

```html
<div class="desk-view">
  <div class="desk-header">
    <div>
      <h1 class="icon-heading"><IconHome/> Today</h1>
      <p class="subtitle">…</p>
    </div>
    <div class="desk-actions"><LangfuseLink/><ReindexButton/></div>
  </div>

  <div class="desk-grid">
    <div class="desk-column">
      <!-- Recent reads: getHeadlines(4), same .headline-card markup as today -->
      <!-- Recent threads: getActivity(4), compact rows + "View full log →" -->
    </div>
    <div class="desk-column">
      <!-- Needs attention: getInbox() + getResearchHistory()[0], omitted if both empty -->
      <!-- From the shelf: getPages() + focus.js -> pickFromShelf(), one card -->
    </div>
  </div>
</div>
```

**Recent reads**: same `.headline-card` rendering as current
`HeadlinesView`, just `getHeadlines(4)` instead of `10`.

**Recent threads**: `getActivity(4)`, each row = date (muted, fixed-width) +
`.tag`-style operation badge + title + truncated note. Section ends with a
link to `#/log`.

**Needs attention**: render nothing if `inbox.count === 0` and no research
history. Otherwise an `.attention-card` containing:
- if `inbox.count > 0`: `<IconInbox/> N file(s) waiting in raw/` + up to 3
  filenames + "Run INGEST to add them to the wiki."
- if research history exists: "Last search: '&lt;label&gt;' (&lt;date&gt;)"
  linking to `#/research`.

**From the shelf**: as described in §3 — drift-aware lead line, then the
picked page's title/type badge (reuse `TYPE_BADGES` icon map from
`PageView.js`, factored into a tiny shared constant if convenient) linking
to `#/page/<path>`.

---

## 6. CSS additions (`web/static/css/styles.css`)

```css
.desk-header { display: flex; justify-content: space-between; align-items: flex-start; gap: var(--space-4); margin-bottom: var(--space-6); }
.desk-actions { display: flex; gap: var(--space-2); }
.desk-grid { display: grid; grid-template-columns: 1.6fr 1fr; gap: var(--space-6); align-items: start; }
.desk-column { display: flex; flex-direction: column; gap: var(--space-6); }

.desk-section-label { font-size: var(--text-sm); font-weight: var(--font-weight-semibold); color: var(--color-text-secondary); text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: var(--space-3); }

.attention-card { border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: var(--space-4); background: var(--color-surface); box-shadow: var(--shadow-sm); display: flex; flex-direction: column; gap: var(--space-3); }
.attention-list { margin: var(--space-1) 0 0; padding-left: var(--space-5); font-size: var(--text-sm); color: var(--color-text-secondary); }

.shelf-card { border: 1px dashed var(--color-border-strong); border-radius: var(--radius-md); padding: var(--space-4); background: var(--color-bg); }
.shelf-note { font-size: var(--text-sm); color: var(--color-text-secondary); font-style: italic; margin-bottom: var(--space-2); }

.activity-list { display: flex; flex-direction: column; gap: var(--space-3); }
.activity-item { display: flex; gap: var(--space-3); align-items: baseline; font-size: var(--text-sm); }
.activity-date { color: var(--color-text-muted); white-space: nowrap; min-width: 4.5rem; font-size: var(--text-xs); }
```

`@media (max-width: 900px)`: add `.desk-grid { grid-template-columns: 1fr; }`
to the existing stacking breakpoint.

The `.shelf-card`'s dashed border + `--color-bg` (vs `--color-surface`
elsewhere) is the one deliberate visual departure — a quiet signal that this
card is "different" (pulled from elsewhere, possibly against the grain of
recent activity) without introducing a new color. `.attention-card` reuses
existing surface/shadow tokens.

---

## 7. Routing / Sidebar updates

- `app.js`: rename route `"headlines"` → `"home"` (the name no longer fits);
  import `DeskView` instead of `HeadlinesView`; `parseRoute` maps `""`/`"/"`
  and unknown paths to `{name: "home"}`.
- `Sidebar.js`: nav item label "Headlines" → **"Today"**, active-check
  `route.name === "home"`, same `IconHome` icon and `href="#/"`.

---

## 8. Verification

- Server already running on `:8000` — confirm whether it's running with
  `--reload`; restart if needed so the new `/api/inbox` and
  `/api/wiki/activity` routes (and the extended `/api/wiki/pages` /
  `/api/wiki/page/{path}` responses) are picked up.
- `python3 -c` / urllib checks against `/api/inbox`, `/api/wiki/activity`,
  `/api/wiki/pages` (check `tags` present), `/api/wiki/page/<a-concept-page>`
  (check `tags` present) — confirm shapes and that the ~9 pending `raw/`
  files are detected.
- Re-read every new/modified file in full (no `node` available in this env,
  per prior session) to manually verify htm/JSX syntax.
- Ask the user to load `http://127.0.0.1:8000/#/` and confirm: the
  two-column desk layout, "Needs attention" and "From the shelf" cards, the
  900px stacking breakpoint, and — by visiting a few concept pages and
  reloading `#/` — that the "From the shelf" lead line changes from "Worth
  revisiting" to the drift-aware framing once one tag dominates recent
  views.
