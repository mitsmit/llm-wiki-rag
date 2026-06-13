import { marked } from "https://esm.sh/marked@12";

// Obsidian-style [[wiki/concepts/x|Label]] or [[wiki/concepts/x]] -> SPA hash link.
const WIKILINK_RE = /\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g;

function wikilinksToMarkdown(text) {
  return text.replace(WIKILINK_RE, (_match, target, label) => {
    const display = label || target.split("/").pop();
    const path = target.endsWith(".md") ? target : `${target}.md`;
    return `[${display}](#/page/${path})`;
  });
}

export function renderMarkdown(text) {
  return marked.parse(wikilinksToMarkdown(text || ""));
}
