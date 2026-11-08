'use strict';
// One diagram per lab, drawn as inline SVG by renderDiagram().
// A stage is a node, or an array of nodes that run side by side.
// A node: k = kind (data, code, model, check, gate, human), t = label, s = detail line,
//         in = label on the arrow that enters it, out = a side exit (for example a failure path).
// loops: arrows back from stage `from` to stage `to`, with a label.
const DIAGRAMS = {
  '00': {stages: [
    {k: 'data', t: '4 projects', s: 'every fact combination'},
    [{k: 'code', t: 'Apply the rule', s: 'decide()'}, {k: 'model', t: 'Ask a model', s: 'ask() + to_label()'}],
    {k: 'check', t: 'Compare', s: 'agreement count'}]},
  '01': {stages: [
    {k: 'data', t: 'Labelled case', s: '5 tests'},
    {k: 'code', t: 'Guided prompt', s: 'policy + example'},
    {k: 'model', t: 'Model', s: 'JSON reply'},
    {k: 'check', t: 'Parse', s: 'parse_reply()', out: 'bad format → invalid'},
    {k: 'check', t: 'Score', s: 'pass · fail · invalid'},
    {k: 'gate', t: '≥ 80%', out: 'below → stop'}]},
  '02': {stages: [
    {k: 'data', t: 'Question'},
    {k: 'code', t: 'Embed', s: 'MiniLM vectors'},
    {k: 'code', t: 'Nearest policies', s: 'Chroma'},
    {k: 'gate', t: 'close?', out: 'none → abstain'},
    {k: 'model', t: 'Grounded answer', s: 'cites [R1]'},
    {k: 'check', t: 'Citation check', s: 'cited ⊆ retrieved'}]},
  '03': {stages: [
    {k: 'data', t: 'Brief'},
    {k: 'model', t: 'Requirements', s: '3 labels'}, {k: 'gate', t: 'gate', out: 'fail → stop'},
    {k: 'model', t: 'Options', s: '2 or 3'}, {k: 'gate', t: 'gate'},
    {k: 'model', t: 'Trade-offs', s: '+ / − table'}, {k: 'gate', t: 'gate'},
    {k: 'model', t: 'Decision record', s: 'Context · Decision · Consequence'}, {k: 'gate', t: 'gate'}]},
  '04': {stages: [
    {k: 'data', t: 'Request'},
    {k: 'model', t: 'Pick a tool', s: '{"tool", "args"}'},
    {k: 'check', t: 'call_tool()', s: 'name · types', out: 'bad → error as data'},
    {k: 'human', t: 'User confirms', s: 'write tools only'},
    [{k: 'code', t: 'search_hotels()', s: 'reads live data'}, {k: 'code', t: 'book_room()', s: 'changes data'}],
    {k: 'model', t: 'Answer', s: 'from the result'}]},
  '05': {stages: [
    {k: 'data', t: 'Goal'},
    {k: 'model', t: 'Next action', s: 'JSON'},
    {k: 'check', t: 'Guards', s: 'known tool · facts read', out: 'finish → check decision'},
    {k: 'code', t: 'Run the tool', s: 'list / get_project'},
    {k: 'data', t: 'Observation', s: 'added to history'}],
    loops: [{from: 4, to: 1, t: 'repeat · at most 5 turns'}]},
  '06': {stages: [
    {k: 'data', t: 'Shared sources', s: 'R1 · F1–F3'},
    [{k: 'model', t: 'Minimalist', s: 'Qwen'}, {k: 'model', t: 'Safeguard', s: 'DeepSeek'}, {k: 'model', t: 'Modernizer', s: 'Gemini'}],
    {k: 'gate', t: 'grounded?'},
    {k: 'model', t: 'Challenge + revise', s: 'one round', in: 'no source'},
    {k: 'check', t: 'Chair counts', s: '⅔ of grounded votes'},
    [{k: 'data', t: 'Decision', s: '+ dissent kept'}, {k: 'human', t: 'Escalate', s: 'no majority'}]]},
  '07': {stages: [
    [{k: 'model', t: 'Minimalist', s: 'model agent'}, {k: 'model', t: 'Modernizer', s: 'model agent'}, {k: 'code', t: 'Rulebook', s: 'added in one line'}],
    {k: 'check', t: 'Schema check', s: 'typed Message', out: 'broken → rejected'},
    {k: 'code', t: 'Message bus', s: 'publish()'},
    [{k: 'data', t: 'Live log', s: 'time · level · line'}, {k: 'data', t: 'council.log', s: 'one JSON per line'}, {k: 'data', t: 'LangSmith', s: 'trace tree (optional)'}],
    {k: 'check', t: 'Chair', s: 'majority or escalate'},
    {k: 'data', t: 'Evidence trail', s: 'trace() from council.log'}]},
  '08': {stages: [
    {k: 'data', t: 'Council proposal', s: 'microservices 2–1'},
    {k: 'human', t: 'Human review', s: 'verdict + reason'},
    {k: 'model', t: 'Council revises', s: 'reads short-term notes', in: 'reject'},
    {k: 'code', t: 'Long-term memory', s: 'lesson in Chroma', in: 'accept'},
    {k: 'code', t: 'Recall', s: 'similar new cases'},
    {k: 'check', t: 'Held-out score', s: 'before vs after'}],
    loops: [{from: 2, to: 1, t: 'at most 2 reviews'}]},
  '09': {stages: [
    {k: 'data', t: 'Recorded runs', s: '4 systems × 2 cases'},
    {k: 'check', t: 'Correct · grounded', s: 'calls · seconds'},
    {k: 'model', t: 'LLM judge', s: 'names a cost?'},
    {k: 'human', t: 'Calibrate', s: 'agree with human ≥ 75%'},
    {k: 'check', t: 'Council vs best', s: 'wins, and at what cost'}]},
  '10': {stages: [
    {k: 'data', t: 'Case', s: 'facts + note'},
    {k: 'model', t: 'Router', s: 'route + reason'},
    {k: 'gate', t: 'valid?', out: 'no → council'},
    [{k: 'code', t: 'Rule', s: '0 calls'}, {k: 'model', t: 'Council', s: '5 calls'}],
    {k: 'check', t: 'Compare', s: 'vs human routes'}]},
  '11': {stages: [
    {k: 'code', t: 'MCP server', s: '2 registered tools'},
    {k: 'code', t: 'list_tools', s: 'names + schemas'},
    {k: 'code', t: 'get_project', s: 'read'},
    {k: 'code', t: 'Apply the policy', s: 'plain Python'},
    {k: 'code', t: 'save_decision', s: 'write', out: 'bad input → is_error'},
    {k: 'check', t: 'State check', s: 'rejected calls change nothing'}]},
  '12': {stages: [
    {k: 'data', t: 'Skill catalog', s: 'names + descriptions'},
    {k: 'model', t: 'Pick a skill', s: 'name only'},
    {k: 'code', t: 'Load instructions', s: 'SKILL.md body'},
    {k: 'model', t: 'Write the ADR', s: 'per case'},
    {k: 'check', t: 'Check the ADR', s: 'adr_problems()'}]},
  '13': {stages: [
    {k: 'data', t: 'Project'},
    {k: 'model', t: 'Propose', s: 'label only'},
    {k: 'code', t: 'Reviewer agent', s: 'over A2A: card + message'},
    {k: 'gate', t: 'PASS?'},
    {k: 'data', t: 'Accepted'}],
    loops: [{from: 3, to: 1, t: 'FAIL · one revision with feedback'}]},
  '14': {stages: [
    {k: 'data', t: 'START'},
    {k: 'model', t: 'choose', s: 'node'},
    {k: 'check', t: 'check', s: 'node'},
    {k: 'gate', t: 'route'},
    {k: 'data', t: 'END', in: 'done'}],
    loops: [{from: 3, to: 1, t: 'retry · at most 2 attempts'}]},
  '15': {stages: [
    {k: 'data', t: 'Brief', s: 'Booking service'},
    {k: 'model', t: 'Chair frames', s: '3 ISO 25010 scenarios'},
    {k: 'gate', t: 'has numbers?', out: 'no → stop'},
    {k: 'model', t: '4 architects', s: 'one contract'},
    {k: 'check', t: 'Contract check', s: 'option · marks · confidence', out: 'broken → rejected'},
    {k: 'check', t: 'Aggregate', s: 'votes vs confidence'}]},
  '16': {stages: [
    {k: 'data', t: 'Benchmark', s: '10 cases'},
    {k: 'code', t: 'Split once', s: '6 feedback · 4 test'},
    {k: 'human', t: 'Feedback case', s: 'one per round'},
    {k: 'code', t: 'Update trust', s: 'per architect'},
    {k: 'check', t: 'Weighted vote', s: 'test cases only'},
    {k: 'data', t: 'Learning curve'}],
    loops: [{from: 4, to: 2, t: 'next round'}]},
  '17': {stages: [
    {k: 'data', t: 'Two options', s: 'monolith · microservices'},
    [{k: 'code', t: 'Score criteria', s: '0–4 per option'}, {k: 'model', t: 'JEV scores', s: 'Score primitive'}],
    {k: 'code', t: 'Weights', s: 'the team’s priorities'},
    {k: 'code', t: 'Weighted total', s: 'Σ score × weight'},
    {k: 'data', t: 'Winner', s: 'higher total wins'}],
    loops: [{from: 1, to: 3, t: 'reweight, never re-judge'}]},
};

const DIAGRAM_KINDS = {
  data: 'Input or result', code: 'Plain Python', model: 'Model call', check: 'Check', gate: 'Decision point', human: 'Human',
};

const renderDiagram = (() => {
  const SVG = 'http://www.w3.org/2000/svg';
  const H = 58, GATE = 30, GAP = 30, VGAP = 10, CHAR = 6.7, SUBCHAR = 5.9;
  const esc = text => String(text).replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));

  function wrap(text, width, charWidth) {
    const max = Math.max(6, Math.floor(width / charWidth));
    const lines = [];
    String(text).split(' ').forEach(word => {
      const last = lines.length - 1;
      if (last >= 0 && (lines[last] + ' ' + word).length <= max) lines[last] += ' ' + word;
      else lines.push(word);
    });
    return lines;
  }

  function nodeSvg(n, x, y, w, h, side = false) {
    const cx = x + w / 2, cy = y + h / 2;
    if (n.k === 'gate') {
      const r = GATE / 2;
      const lx = side ? cx + r + 8 : cx, ly = side ? cy + 4 : cy + r + 12;
      const label = wrap(n.t, 90, 5.6).map((line, i) => `<tspan x="${lx}" dy="${i ? 11 : 0}">${esc(line)}</tspan>`).join('');
      return `<g class="dg-gate"><title>${esc(n.t)}</title><path d="M${cx} ${cy - r}L${cx + r} ${cy}L${cx} ${cy + r}L${cx - r} ${cy}Z"/>`
        + `<text class="dg-gate-label${side ? ' dg-start' : ''}" x="${lx}" y="${ly}">${label}</text></g>`;
    }
    const title = wrap(n.t, w - 16, CHAR), sub = n.s ? wrap(n.s, w - 14, SUBCHAR) : [];
    const lines = title.length + sub.length;
    let ty = cy - (lines - 1) * 7 + 4;
    const text = title.map(line => { const t = `<text class="dg-title" x="${cx}" y="${ty}">${esc(line)}</text>`; ty += 14; return t; }).join('')
      + sub.map(line => { const t = `<text class="dg-sub" x="${cx}" y="${ty}">${esc(line)}</text>`; ty += 13; return t; }).join('');
    const radius = n.k === 'data' ? h / 2 : 8;
    const badge = n.k === 'model' ? `<circle class="dg-dot" cx="${x + w - 9}" cy="${y + 9}" r="3"/>` : '';
    return `<g class="dg-${n.k}"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${Math.min(radius, 22)}"/>${badge}${text}</g>`;
  }

  // Measure how tall a node must be for its text at a given width.
  function nodeHeight(n, w) {
    if (n.k === 'gate') return GATE + 26;
    const lines = wrap(n.t, w - 16, CHAR).length + (n.s ? wrap(n.s, w - 14, SUBCHAR).length : 0);
    return Math.max(H, lines * 14 + 18);
  }

  function horizontal(spec, nodeW) {
    const stages = spec.stages.map(s => (Array.isArray(s) ? s : [s]));
    const widths = stages.map(group => (group[0].k === 'gate' ? GATE : nodeW));
    const gaps = stages.map(group => Math.max(GAP, ...group.map(n => (n.in ? n.in.length * 5.6 + 16 : 0))));
    const heights = stages.map((group, i) => group.map(n => nodeHeight(n, widths[i])));
    const groupH = heights.map(hs => hs.reduce((a, b) => a + b, 0) + (hs.length - 1) * VGAP);
    const band = Math.max(...groupH);
    const hasOut = stages.some(g => g.some(n => n.out));
    const top = hasOut ? 40 : 6, loopY = top + band + 22, height = top + band + (spec.loops ? 44 : 8);
    let x = 2;
    const boxes = stages.map((group, i) => {
      if (i) x += gaps[i];
      let y = group[0].k === 'gate' ? top + band / 2 - GATE / 2 : top + (band - groupH[i]) / 2;
      const items = group.map((n, j) => { const b = {n, x, y, w: widths[i], h: heights[i][j]}; y += b.h + VGAP; return b; });
      x += widths[i];
      return items;
    });
    const width = x + 2;
    const mid = b => (b.n.k === 'gate' ? b.y + GATE / 2 : b.y + b.h / 2);
    let edges = '';
    for (let i = 1; i < boxes.length; i++) {
      const mx = boxes[i][0].x - gaps[i] / 2;
      boxes[i - 1].forEach(a => boxes[i].forEach(b => {
        const ax = a.x + a.w + (a.n.k === 'gate' ? 0 : 0), ay = mid(a), bx = b.x - 2, by = mid(b);
        const d = Math.abs(ay - by) < 1 ? `M${ax} ${ay}H${bx}` : `M${ax} ${ay}H${mx}V${by}H${bx}`;
        edges += `<path class="dg-edge" d="${d}" marker-end="url(#ARROW)"/>`;
      }));
      boxes[i].forEach(b => { if (b.n.in) edges += `<text class="dg-edge-label" x="${b.x - gaps[i] / 2}" y="${mid(b) - 8}">${esc(b.n.in)}</text>`; });
    }
    boxes.flat().forEach(b => {
      if (!b.n.out) return;
      const cx = b.x + b.w / 2, y0 = b.n.k === 'gate' ? b.y : b.y;
      edges += `<path class="dg-edge dg-exit" d="M${cx} ${y0}V${top - 18}" marker-end="url(#ARROW)"/>`
        + `<text class="dg-exit-label" x="${cx}" y="${top - 24}">${esc(b.n.out)}</text>`;
    });
    (spec.loops || []).forEach(loop => {
      const from = boxes[loop.from], to = boxes[loop.to];
      const fx = from[0].x + from[0].w / 2, tx = to[0].x + to[0].w / 2;
      const fy = Math.max(...from.map(b => (b.n.k === 'gate' ? b.y + GATE : b.y + b.h)));
      const ty = Math.max(...to.map(b => b.y + b.h));
      edges += `<path class="dg-edge dg-loop" d="M${fx} ${fy}V${loopY}H${tx}V${ty + 2}" marker-end="url(#ARROW)"/>`
        + `<text class="dg-loop-label" x="${(fx + tx) / 2}" y="${loopY + 14}">${esc(loop.t)}</text>`;
    });
    const nodes = boxes.flat().map(b => nodeSvg(b.n, b.x, b.y, b.w, b.n.k === 'gate' ? GATE : b.h)).join('');
    return {width, height, body: edges + nodes};
  }

  function vertical(spec, width) {
    const stages = spec.stages.map(s => (Array.isArray(s) ? s : [s]));
    const hasOut = stages.some(g => g.some(n => n.out));
    const left = hasOut ? 86 : 4, right = spec.loops ? 34 : 4;
    const colW = Math.max(150, width - left - right);
    let y = 2;
    const boxes = stages.map((group, i) => {
      const gap = i ? Math.max(26, group.some(n => n.in) ? 30 : 0) : 0;
      y += gap;
      const w = group[0].k === 'gate' ? GATE : (colW - (group.length - 1) * 8) / group.length;
      const hs = group.map(n => (n.k === 'gate' ? GATE + 26 : nodeHeight(n, w)));
      const rowH = Math.max(...hs);
      const items = group.map((n, j) => ({n, x: group[0].k === 'gate' ? left + colW / 2 - GATE / 2 : left + j * (w + 8), y, w, h: n.k === 'gate' ? GATE : rowH}));
      y += group[0].k === 'gate' ? GATE : rowH;
      return items;
    });
    const height = y + 4;
    let edges = '';
    for (let i = 1; i < boxes.length; i++) {
      const prev = boxes[i - 1], next = boxes[i];
      const ay = Math.max(...prev.map(b => b.y + b.h)) , by = next[0].y - 2;
      const my = (ay + by) / 2;
      prev.forEach(a => next.forEach(b => {
        const ax = a.x + a.w / 2, bx = b.x + b.w / 2;
        const startY = a.n.k === 'gate' ? a.y + GATE : a.y + a.h;
        const d = Math.abs(ax - bx) < 1 ? `M${ax} ${startY}V${by}` : `M${ax} ${startY}V${my}H${bx}V${by}`;
        edges += `<path class="dg-edge" d="${d}" marker-end="url(#ARROW)"/>`;
      }));
      next.forEach(b => { if (b.n.in) edges += `<text class="dg-edge-label dg-start" x="${b.x + b.w / 2 + 8}" y="${b.y - 10}">${esc(b.n.in)}</text>`; });
    }
    boxes.flat().forEach(b => {
      if (!b.n.out) return;
      const cy = b.y + (b.n.k === 'gate' ? GATE / 2 : b.h / 2);
      edges += `<path class="dg-edge dg-exit" d="M${b.x} ${cy}H${left - 14}" marker-end="url(#ARROW)"/>`;
      wrap(b.n.out, left - 18, 5.6).forEach((line, i, all) => {
        edges += `<text class="dg-exit-label dg-end" x="${left - 18}" y="${cy - 6 - (all.length - 1 - i) * 11}">${esc(line)}</text>`;
      });
    });
    (spec.loops || []).forEach(loop => {
      const from = boxes[loop.from], to = boxes[loop.to];
      const fb = from[from.length - 1], tb = to[to.length - 1];
      const fx = fb.x + fb.w, fy = fb.y + fb.h / 2, tx = tb.x + tb.w + 2, ty = tb.y + tb.h / 2;
      const lx = left + colW + 16;
      edges += `<path class="dg-edge dg-loop" d="M${fx} ${fy}H${lx}V${ty}H${tx}" marker-end="url(#ARROW)"/>`
        + `<text class="dg-loop-label" transform="translate(${lx + 11} ${(fy + ty) / 2}) rotate(90)">${esc(loop.t)}</text>`;
    });
    const nodes = boxes.flat().map(b => nodeSvg(b.n, b.x, b.y, b.w, b.h, true)).join('');
    return {width, height, body: edges + nodes};
  }

  function describe(spec) {
    const name = n => (n.s ? `${n.t} (${n.s})` : n.t);
    const steps = spec.stages.map(s => (Array.isArray(s) ? s.map(name).join(' or ') : name(s)));
    const loops = (spec.loops || []).map(l => ` Then back to ${spec.stages[l.to].t || 'an earlier step'}: ${l.t}.`).join('');
    return `${steps.join(', then ')}.${loops}`;
  }

  // A self-contained SVG file for the notebooks: the wide layout, its legend, and the given styles.
  function standalone(id, css) {
    const spec = DIAGRAMS[id], layout = horizontal(spec, 118), pad = 18;
    const used = Object.keys(DIAGRAM_KINDS).filter(k => spec.stages.flat().some(n => n.k === k));
    let x = 0, legend = '';
    used.forEach(k => {
      const key = k === 'gate'
        ? `<g class="dg-gate"><path d="M${x + 7} 0L${x + 13} 6L${x + 7} 12L${x + 1} 6Z"/></g>`
        : `<g class="dg-${k}"><rect x="${x}" y="0" width="16" height="12" rx="${k === 'data' ? 6 : 3}"/></g>`;
      legend += `${key}<text class="dg-legend-text" x="${x + 22}" y="10">${esc(DIAGRAM_KINDS[k])}</text>`;
      x += 22 + DIAGRAM_KINDS[k].length * 6 + 22;
    });
    const width = Math.max(layout.width, x) + 2 * pad, height = layout.height + 2 * pad + 34;
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" class="dg" role="img" viewBox="0 0 ${width} ${height}" width="${width}" height="${height}">`
      + `<title>${esc(describe(spec))}</title><style>${css}</style>`
      + `<rect width="${width}" height="${height}" rx="12" fill="#f3f5f7"/>`
      + `<defs><marker id="arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L8 4L0 8Z"/></marker></defs>`
      + `<g transform="translate(${pad + (width - 2 * pad - layout.width) / 2} ${pad})">${layout.body.replaceAll('url(#ARROW)', 'url(#arrow)')}</g>`
      + `<g transform="translate(${pad} ${height - pad - 12})">${legend}</g></svg>\n`;
    return {svg, description: describe(spec)};
  }

  // Draw a lab's diagram into `figure`, horizontal when it fits, otherwise vertical.
  const render = function (figure, id) {
    const spec = DIAGRAMS[id];
    const available = figure.clientWidth;
    if (!spec || !available) return;
    const wide = horizontal(spec, 118);
    const layout = wide.width <= available ? wide : vertical(spec, Math.min(available, 460));
    const marker = `dg-arrow-${id}`;
    const used = Object.keys(DIAGRAM_KINDS).filter(k => spec.stages.flat().some(n => n.k === k));
    figure.innerHTML = `<svg class="dg" role="img" aria-label="${esc(describe(spec))}" viewBox="0 0 ${layout.width} ${layout.height}" width="${layout.width}" height="${layout.height}">`
      + `<defs><marker id="${marker}" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L8 4L0 8Z"/></marker></defs>`
      + layout.body.replaceAll('url(#ARROW)', `url(#${marker})`) + '</svg>'
      + `<figcaption class="dg-legend" aria-hidden="true">${used.map(k => `<span class="dg-key dg-key-${k}">${DIAGRAM_KINDS[k]}</span>`).join('')}</figcaption>`;
  };
  render.standalone = standalone;
  return render;
})();
if (typeof module !== 'undefined') module.exports = {DIAGRAMS, renderDiagram};
