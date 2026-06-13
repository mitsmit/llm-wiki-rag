import { createRoot } from "https://esm.sh/react-dom@18/client";
import { html, React } from "./html.js";
import { Sidebar } from "./components/Sidebar.js";
import { DeskView } from "./components/DeskView.js";
import { ComparePanel } from "./components/ComparePanel.js";
import { PageView } from "./components/PageView.js";
import { LogView } from "./components/LogView.js";
import { ResearchView } from "./components/ResearchView.js";
import { BrainstormView } from "./components/BrainstormView.js";

const { useState, useEffect } = React;

function parseRoute(hash) {
  const path = hash.replace(/^#\/?/, "");
  if (path === "" || path === "/") return { name: "home" };
  if (path === "compare") return { name: "compare" };
  if (path === "research") return { name: "research" };
  if (path === "brainstorm") return { name: "brainstorm" };
  if (path === "log") return { name: "log" };
  if (path.startsWith("page/")) {
    return { name: "page", path: decodeURIComponent(path.slice("page/".length)) };
  }
  return { name: "home" };
}

function App() {
  const [route, setRoute] = useState(parseRoute(window.location.hash));

  useEffect(() => {
    const onHashChange = () => setRoute(parseRoute(window.location.hash));
    window.addEventListener("hashchange", onHashChange);
    return () => window.removeEventListener("hashchange", onHashChange);
  }, []);

  let main;
  if (route.name === "compare") main = html`<${ComparePanel} />`;
  else if (route.name === "research") main = html`<${ResearchView} />`;
  else if (route.name === "brainstorm") main = html`<${BrainstormView} />`;
  else if (route.name === "page") main = html`<${PageView} path=${route.path} />`;
  else if (route.name === "log") main = html`<${LogView} />`;
  else main = html`<${DeskView} />`;

  return html`
    <div class="layout">
      <${Sidebar} route=${route} />
      <main class="main">${main}</main>
    </div>
  `;
}

const root = createRoot(document.getElementById("root"));
root.render(html`<${App} />`);
