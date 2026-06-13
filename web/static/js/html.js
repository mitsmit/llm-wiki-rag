// Shared React + htm binding, imported by every component so they all share
// the same React instance (esm.sh caches modules by URL).
import React from "https://esm.sh/react@18";
import htm from "https://esm.sh/htm@3";

export { React };
export const html = htm.bind(React.createElement);
