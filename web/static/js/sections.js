// Splits a frontmatter-stripped page body into top-level `## ` sections so
// PageView.js can pull specific sections (related concepts, challenges) out
// of the normal reading-order flow for prominent placement.

const HEADING_RE = /^## (.+)$/gm;

// heading=null marks any content before the first `## ` heading.
export function splitSections(markdown) {
  const text = markdown || "";
  const sections = [];
  let lastIndex = 0;
  let lastHeading = null;
  let match;

  while ((match = HEADING_RE.exec(text)) !== null) {
    const body = text.slice(lastIndex, match.index).trim();
    if (lastHeading !== null || body) {
      sections.push({ heading: lastHeading, body });
    }
    lastHeading = match[1].trim();
    lastIndex = match.index + match[0].length;
  }

  const body = text.slice(lastIndex).trim();
  if (lastHeading !== null || body) {
    sections.push({ heading: lastHeading, body });
  }

  return sections;
}

export function joinSections(sections) {
  return sections
    .map((s) => (s.heading ? `## ${s.heading}\n\n${s.body}` : s.body))
    .filter((s) => s.length > 0)
    .join("\n\n");
}

// Cross-reference list, e.g. "Related Concepts" / "Relationship to Other
// Concepts" / "Relationship to Other Wiki Concepts" — deliberately excludes
// substantive "Relationship to <Topic>" subsections.
export const RELATED_HEADING_RE = /^(Related Concepts|Relationship to Other (Wiki )?Concepts)$/i;

// "Key Challenges" / "Challenges".
export const CHALLENGES_HEADING_RE = /^(Key )?Challenges$/i;
