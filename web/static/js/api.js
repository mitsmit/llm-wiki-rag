export async function getHeadlines(limit = 10) {
  const res = await fetch(`/api/headlines?limit=${limit}`);
  return res.json();
}

export async function getConfig() {
  const res = await fetch("/api/config");
  return res.json();
}

export async function getStats() {
  const res = await fetch("/api/wiki/stats");
  return res.json();
}

export async function getPages() {
  const res = await fetch("/api/wiki/pages");
  return res.json();
}

export async function getPage(path) {
  const res = await fetch(`/api/wiki/page/${path}`);
  return res.json();
}

export async function getLog() {
  const res = await fetch("/api/wiki/log");
  return res.json();
}

export async function reindex() {
  const res = await fetch("/api/reindex", { method: "POST" });
  return res.json();
}

export async function saveAnalysis(slug, question, answer) {
  const res = await fetch("/api/analyses", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ slug, question, answer }),
  });
  return res.json();
}

export function getSessionId() {
  let id = localStorage.getItem("llm_wiki_session_id");
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem("llm_wiki_session_id", id);
  }
  return id;
}

// Streams NDJSON lines from a POST endpoint, calling onEvent(parsedLine) for each.
export async function streamQuery(endpoint, body, onEvent) {
  const res = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop();
    for (const line of lines) {
      if (line.trim()) onEvent(JSON.parse(line));
    }
  }
  if (buffer.trim()) onEvent(JSON.parse(buffer));
}
