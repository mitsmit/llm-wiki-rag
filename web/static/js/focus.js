// Client-side "diversity sensing" for the Desk landing page.
//
// Tracks which wiki pages (and their tags) the user has viewed recently and
// uses that to (a) populate "Recent reads" on Today with actual reading
// history, and (b) bias the "From the shelf" pick toward topics they
// *haven't* been looking at — a small nudge against echo-chamber drift.
// Everything lives in localStorage: no accounts, no backend involvement,
// and clearing storage simply resets the signal.

const KEY_VIEWS = "llm_wiki_recent_views";
const KEY_SHELF = "llm_wiki_shelf_recent";
const MAX_VIEWS = 20;
const MAX_SHELF = 3;
const DRIFT_THRESHOLD = 0.5;

// Navigational hubs, not "reading" — never recorded as a recent read or
// counted toward focus.
const EXCLUDED_PATHS = new Set(["wiki/overview.md"]);

function readJSON(key, fallback) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}

function writeJSON(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch {
    // localStorage unavailable (e.g. private browsing) - ignore
  }
}

// Record that the user viewed a page. Re-viewing a page moves it to the
// front of "recent reads" instead of duplicating it.
export function recordView(path, meta = {}) {
  if (!path || EXCLUDED_PATHS.has(path)) return;
  const views = readJSON(KEY_VIEWS, []).filter((v) => v.path !== path);
  views.push({
    path,
    title: meta.title || path,
    type: meta.type || "other",
    tags: meta.tags || [],
    excerpt: meta.excerpt || "",
    ts: Date.now(),
  });
  writeJSON(KEY_VIEWS, views.slice(-MAX_VIEWS));
}

// Most recently viewed pages, newest first.
export function getRecentReads(limit = 4) {
  return readJSON(KEY_VIEWS, []).slice(-limit).reverse();
}

// Build a tag -> frequency map from recently-viewed pages.
export function getFocusTagCounts() {
  const views = readJSON(KEY_VIEWS, []);
  const counts = {};
  for (const view of views) {
    for (const tag of view.tags || []) {
      counts[tag] = (counts[tag] || 0) + 1;
    }
  }
  return counts;
}

// Pick one candidate page, biased toward low overlap with the user's recent
// focus (i.e. "from the shelf, against the grain"). Avoids repeating recent
// reads or the last few shelf picks. Returns null if there are no candidates.
export function pickFromShelf(candidates, focusTagCounts) {
  if (!candidates || candidates.length === 0) return null;

  const recentShelf = readJSON(KEY_SHELF, []);
  const recentViewPaths = new Set(readJSON(KEY_VIEWS, []).map((v) => v.path));

  let pool = candidates.filter((c) => !recentShelf.includes(c.path) && !recentViewPaths.has(c.path));
  if (pool.length === 0) pool = candidates.filter((c) => !recentShelf.includes(c.path));
  if (pool.length === 0) pool = candidates;

  const scored = pool.map((item) => {
    const overlap = (item.tags || []).reduce((sum, t) => sum + (focusTagCounts[t] || 0), 0);
    return { item, overlap };
  });
  const minOverlap = Math.min(...scored.map((s) => s.overlap));
  const lowOverlap = scored.filter((s) => s.overlap <= minOverlap + 1);
  const pick = lowOverlap[Math.floor(Math.random() * lowOverlap.length)].item;

  writeJSON(KEY_SHELF, [pick.path, ...recentShelf].slice(0, MAX_SHELF));
  return pick;
}

// If one tag dominates recent focus, return {tag, share} so the UI can
// frame the shelf pick as a deliberate change of scene. Otherwise null.
export function getDriftNote(focusTagCounts) {
  const entries = Object.entries(focusTagCounts);
  const total = entries.reduce((sum, [, count]) => sum + count, 0);
  if (total === 0) return null;

  const [topTag, topCount] = entries.reduce((a, b) => (b[1] > a[1] ? b : a));
  const share = topCount / total;
  return share >= DRIFT_THRESHOLD ? { tag: topTag, share } : null;
}
