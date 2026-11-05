#!/usr/bin/env node
// Export each lab's diagram (assets/diagrams.js) as a standalone SVG file for the notebooks.
// The site draws the same diagrams in the browser; run this after changing a diagram.
'use strict';
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const {DIAGRAMS, renderDiagram} = require(path.join(root, 'assets', 'diagrams.js'));

// Reuse the site's diagram styles, with the colour variables resolved, so the files look the same.
const css = fs.readFileSync(path.join(root, 'assets', 'styles.css'), 'utf8');
const vars = Object.fromEntries([...css.match(/:root\{([^}]*)\}/)[1].matchAll(/--([\w-]+):([^;]+)/g)].map(m => [m[1], m[2]]));
const rules = (css.match(/\.dg[\w-]*(?:[ ,.][^{]*)?\{[^}]*\}/g) || [])
  .filter(rule => !/^\.dg-(legend|key)/.test(rule))
  .map(rule => rule.replace(/var\(--([\w-]+)\)/g, (_, name) => vars[name]));
const style = ['text{font-family:"Helvetica Neue",Arial,sans-serif}', ...rules,
  '.dg-legend-text{font-size:11px;fill:#5c5c5c}'].join('');

const out = path.join(root, 'assets', 'diagrams');
fs.mkdirSync(out, {recursive: true});
const descriptions = {};
for (const id of Object.keys(DIAGRAMS).sort()) {
  const {svg, description} = renderDiagram.standalone(id, style);
  fs.writeFileSync(path.join(out, `${id}.svg`), svg);
  descriptions[id] = description;
}
fs.writeFileSync(path.join(out, 'descriptions.json'), JSON.stringify(descriptions, null, 2) + '\n');
console.log(`Exported ${Object.keys(descriptions).length} diagrams to assets/diagrams/`);
