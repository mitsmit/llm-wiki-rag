// Small local set of stroke-based SVG icons (24x24, currentColor), used in
// place of emoji throughout the UI. Each icon is `aria-hidden` — pair with a
// visible text label for accessibility.
import { html } from "./html.js";

function IconBase({ size = 18, children, ...rest }) {
  return html`
    <svg
      width=${size}
      height=${size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
      aria-hidden="true"
      focusable="false"
      ...${rest}
    >${children}</svg>
  `;
}

export function IconBookOpen(props) {
  return html`
    <${IconBase} ...${props}>
      <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" />
      <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" />
    </${IconBase}>
  `;
}

export function IconHome(props) {
  return html`
    <${IconBase} ...${props}>
      <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
      <polyline points="9 22 9 12 15 12 15 22" />
    </${IconBase}>
  `;
}

export function IconGitCompare(props) {
  return html`
    <${IconBase} ...${props}>
      <circle cx="18" cy="18" r="3" />
      <circle cx="6" cy="6" r="3" />
      <path d="M13 6h3a2 2 0 0 1 2 2v7" />
      <path d="M11 18H8a2 2 0 0 1-2-2V9" />
    </${IconBase}>
  `;
}

export function IconCompass(props) {
  return html`
    <${IconBase} ...${props}>
      <circle cx="12" cy="12" r="10" />
      <polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76" />
    </${IconBase}>
  `;
}

export function IconMap(props) {
  return html`
    <${IconBase} ...${props}>
      <path d="M9 3 4 6v15l5-3 6 3 5-3V3l-5 3-6-3Z" />
      <path d="M9 3v15" />
      <path d="M15 6v15" />
    </${IconBase}>
  `;
}

export function IconClipboardList(props) {
  return html`
    <${IconBase} ...${props}>
      <rect x="8" y="2" width="8" height="4" rx="1" />
      <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2" />
      <path d="M12 11h4" />
      <path d="M12 16h4" />
      <path d="M8 11h.01" />
      <path d="M8 16h.01" />
    </${IconBase}>
  `;
}

export function IconFileText(props) {
  return html`
    <${IconBase} ...${props}>
      <path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7z" />
      <path d="M14 2v4a2 2 0 0 0 2 2h4" />
      <path d="M10 9H8" />
      <path d="M16 13H8" />
      <path d="M16 17H8" />
    </${IconBase}>
  `;
}

export function IconLightbulb(props) {
  return html`
    <${IconBase} ...${props}>
      <path d="M12 2a6 6 0 0 0-4 10.5c.6.6 1 1.4 1 2.5h6c0-1.1.4-1.9 1-2.5A6 6 0 0 0 12 2Z" />
      <path d="M9 18h6" />
      <path d="M10 22h4" />
    </${IconBase}>
  `;
}

export function IconBuilding2(props) {
  return html`
    <${IconBase} ...${props}>
      <rect x="4" y="2" width="16" height="20" rx="1" />
      <path d="M9 22v-4h6v4" />
      <path d="M8 6h.01" />
      <path d="M16 6h.01" />
      <path d="M8 10h.01" />
      <path d="M16 10h.01" />
      <path d="M8 14h.01" />
      <path d="M16 14h.01" />
    </${IconBase}>
  `;
}

export function IconFlaskConical(props) {
  return html`
    <${IconBase} ...${props}>
      <path d="M10 2v6.292a7 7 0 1 0 4 0V2" />
      <path d="M5 15h14" />
      <path d="M8.5 2h7" />
    </${IconBase}>
  `;
}

export function IconFile(props) {
  return html`
    <${IconBase} ...${props}>
      <path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z" />
      <path d="M14 2v4a2 2 0 0 0 2 2h4" />
    </${IconBase}>
  `;
}

export function IconNewspaper(props) {
  return html`
    <${IconBase} ...${props}>
      <rect x="3" y="4" width="18" height="16" rx="2" />
      <path d="M7 8h10" />
      <path d="M7 12h10" />
      <path d="M7 16h6" />
    </${IconBase}>
  `;
}

export function IconRefreshCw(props) {
  return html`
    <${IconBase} ...${props}>
      <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8" />
      <path d="M21 3v5h-5" />
      <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16" />
      <path d="M8 16H3v5" />
    </${IconBase}>
  `;
}

export function IconPaperclip(props) {
  return html`
    <${IconBase} ...${props}>
      <rect x="6" y="3" width="8" height="14" rx="4" />
      <path d="M10 7v8a4 4 0 0 0 8 0V8" />
    </${IconBase}>
  `;
}

export function IconSave(props) {
  return html`
    <${IconBase} ...${props}>
      <path d="M15.2 3a2 2 0 0 1 1.4.6l3.8 3.8a2 2 0 0 1 .6 1.4V19a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z" />
      <path d="M17 21v-7a1 1 0 0 0-1-1H8a1 1 0 0 0-1 1v7" />
      <path d="M7 3v4a1 1 0 0 0 1 1h7a1 1 0 0 0 1-1V3.4" />
    </${IconBase}>
  `;
}

export function IconSearch(props) {
  return html`
    <${IconBase} ...${props}>
      <circle cx="11" cy="11" r="8" />
      <path d="m21 21-4.3-4.3" />
    </${IconBase}>
  `;
}

export function IconHistory(props) {
  return html`
    <${IconBase} ...${props}>
      <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
      <path d="M3 3v5h5" />
      <path d="M12 7v5l4 2" />
    </${IconBase}>
  `;
}

export function IconX(props) {
  return html`
    <${IconBase} ...${props}>
      <path d="M18 6 6 18" />
      <path d="m6 6 12 12" />
    </${IconBase}>
  `;
}

export function IconDownload(props) {
  return html`
    <${IconBase} ...${props}>
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
      <polyline points="7 10 12 15 17 10" />
      <line x1="12" y1="15" x2="12" y2="3" />
    </${IconBase}>
  `;
}

export function IconBarChart(props) {
  return html`
    <${IconBase} ...${props}>
      <path d="M3 3v18h18" />
      <path d="M18 17V9" />
      <path d="M13 17V5" />
      <path d="M8 17v-3" />
    </${IconBase}>
  `;
}

export function IconInbox(props) {
  return html`
    <${IconBase} ...${props}>
      <path d="M22 12h-6l-2 3h-4l-2-3H2" />
      <path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z" />
    </${IconBase}>
  `;
}

export function IconBookmark(props) {
  return html`
    <${IconBase} ...${props}>
      <path d="M19 21 12 16l-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z" />
    </${IconBase}>
  `;
}

export function IconUsers(props) {
  return html`
    <${IconBase} ...${props}>
      <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
      <circle cx="9" cy="7" r="4" />
      <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
      <path d="M16 3.13a4 4 0 0 1 0 7.75" />
    </${IconBase}>
  `;
}

export function IconAlertTriangle(props) {
  return html`
    <${IconBase} ...${props}>
      <path d="m21.73 18-8-14a2 2 0 0 0-3.46 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z" />
      <path d="M12 9v4" />
      <path d="M12 17h.01" />
    </${IconBase}>
  `;
}
