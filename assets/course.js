'use strict';
const labs = [
  {
    "id": "00",
    "file": "00_llms_prompting",
    "title": "LLMs and prompting",
    "subtitle": "One call, one prompt edit",
    "topics": "llm prompt api messages",
    "idea": "A clear prompt tells the model what to do.",
    "flow": "prompt → response",
    "objectives": [
      "Make one model call.",
      "See how a prompt edit changes the reply."
    ],
    "example": "Ask for a short customer-support reply. Read the answer.",
    "exercise": "Change the tone from formal to friendly.",
    "checks": "Expect a short reply about the supplied request. Check that it does not invent a delivery date.",
    "bridge": "One useful call is the starting point."
  },
  {
    "id": "01",
    "file": "01_rag_systems",
    "title": "RAG systems",
    "subtitle": "Find an answer in two short notes",
    "topics": "rag retrieval sources context",
    "idea": "RAG retrieves relevant text before generating an answer.",
    "flow": "question → find note → answer",
    "objectives": [
      "Retrieve one relevant note.",
      "Use it as model context."
    ],
    "example": "Use two library notes. Ask when the library closes and pass the matching note to the model.",
    "exercise": "Change one opening time and ask again.",
    "checks": "Expect the answer to use the time in the selected note. Check its source ID.",
    "bridge": "Retrieval supplies the evidence."
  },
  {
    "id": "02",
    "file": "02_agent_foundations",
    "title": "Foundations of AI agents",
    "subtitle": "One lookup in a tiny agent loop",
    "topics": "agent loop action observation tool stop",
    "idea": "An agent chooses an action, observes its result, and decides what to do next.",
    "flow": "action → lookup → observation → answer",
    "objectives": [
      "Follow one action and observation.",
      "Recognize the stopping rule."
    ],
    "example": "Let a small assistant look up one fact, then reply.",
    "exercise": "Change the requested fact.",
    "checks": "Expect one lookup followed by an answer. The loop must stop within its limit.",
    "bridge": "The host program controls tool execution and limits."
  },
  {
    "id": "03",
    "file": "03_tools_mcp",
    "title": "Tools and MCP",
    "subtitle": "Call one lookup tool through MCP",
    "topics": "tool mcp client server protocol sdk",
    "idea": "MCP gives applications a standard interface to tools and context.",
    "flow": "MCP client → lookup tool → note",
    "objectives": [
      "Call a tool through an MCP client.",
      "Read the returned result."
    ],
    "example": "Ask the read-only lookup tool for one note. Supporting server code lives in the course package.",
    "exercise": "Request a different topic.",
    "checks": "Expect the matching note in the tool result. Check that the response contains it.",
    "bridge": "The tool’s interface is the new building block."
  },
  {
    "id": "04",
    "file": "04_agentic_patterns",
    "title": "Agentic patterns",
    "subtitle": "A tiny chain and a tiny router",
    "topics": "patterns chaining routing workflow",
    "idea": "Chaining connects steps; routing selects a path.",
    "flow": "chain: topic → reply\nroute: category → handler",
    "objectives": [
      "Pass one result to the next step.",
      "Route a message to a handler."
    ],
    "example": "Extract a message topic, then write a reply. In a second microexample, choose a handler from its category.",
    "exercise": "Change the message category.",
    "checks": "Expect the selected handler to match the category. Check that one output.",
    "bridge": "Parallelization, reflection, and orchestration are further reading."
  },
  {
    "id": "05",
    "file": "05_a2a_protocol",
    "title": "A2A protocol",
    "subtitle": "One Hello exchange",
    "topics": "a2a agent card message protocol sdk",
    "idea": "A2A gives agents a common interface for capability discovery and messages.",
    "flow": "discover greeter → send Ada → reply",
    "objectives": [
      "Find a greeting agent.",
      "Send one message."
    ],
    "example": "Send Ada to the small greeter through the A2A SDK. Read its reply.",
    "exercise": "Replace Ada with your name.",
    "checks": "Expect “Hello, Ada!” for the original input. Check that exact text.",
    "bridge": "The local exchange uses real A2A protocol routes."
  },
  {
    "id": "06",
    "file": "06_agent_skills",
    "title": "Agent skills",
    "subtitle": "Read and apply short skill instructions",
    "topics": "skills skill.md instructions reusable",
    "idea": "A skill stores reusable instructions for a task.",
    "flow": "read SKILL.md → apply to note → summary",
    "objectives": [
      "Read a short skill.",
      "Use its instructions with a new input."
    ],
    "example": "Read a note-summary SKILL.md and apply its short instructions to one note.",
    "exercise": "Change the requested summary length.",
    "checks": "Expect a summary in the requested format. Check that format.",
    "bridge": "Keep the reusable procedure separate from the current note."
  },
  {
    "id": "07",
    "file": "07_frameworks_evaluation",
    "title": "Frameworks",
    "subtitle": "A two-node LangGraph example",
    "topics": "framework langgraph nodes state edges",
    "idea": "A framework organizes a workflow using state, nodes, and edges.",
    "flow": "START → classify → reply → END",
    "objectives": [
      "Run an actual LangGraph workflow.",
      "Follow state through two nodes."
    ],
    "example": "A small graph classifies one message and writes a reply.",
    "exercise": "Change the input message.",
    "checks": "Expect the final state to contain a reply. Check that field.",
    "bridge": "The graph makes the sequence explicit."
  }
];

const list = document.getElementById('lab-list');
const esc = text => String(text).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const config = window.COURSE_CONFIG || {};
const configured = typeof config.repo === 'string' && /^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})\/[A-Za-z0-9_.-]+$/.test(config.repo) && config.repo !== 'OWNER/REPO';
const ref = typeof config.ref === 'string' ? config.ref : 'main';
let completed = [];
try { const stored = JSON.parse(localStorage.getItem('agentic-ai-course-progress') || '[]'); if (Array.isArray(stored)) completed = stored.filter(x => labs.some(l => l.id === x)); } catch (_) { /* Browser storage is optional. */ }

function updateProgress() {
  const count = labs.filter(l => completed.includes(l.id)).length;
  document.getElementById('progress-label').textContent = `${count} / ${labs.length} labs explored`;
  document.getElementById('course-progress').value = count;
  try { localStorage.setItem('agentic-ai-course-progress', JSON.stringify(completed)); } catch (_) { /* Private browsing can disable storage. */ }
}
function notebookActions(lab) {
  const path = `notebooks/${lab.file}.ipynb`;
  const colab = configured ? `https://colab.research.google.com/github/${config.repo}/blob/${encodeURIComponent(ref)}/${path}` : null;
  const action = colab ? `<a class="button primary" href="${esc(colab)}" target="_blank" rel="noopener">Open in Colab <span aria-hidden="true">↗</span></a>` : `<a class="button secondary" href="#setup">Colab setup <span aria-hidden="true">↑</span></a>`;
  return `<div class="notebook-actions">${action}<a class="button secondary" href="${path}" download>Download notebook <span aria-hidden="true">↓</span></a></div>`;
}

labs.forEach((lab, i) => {
  const detail = document.createElement('details');
  detail.className = 'lab';
  detail.id = `lab-${lab.id}`;
  detail.dataset.search = `${lab.title} ${lab.subtitle} ${lab.topics}`.toLowerCase();
  detail.innerHTML = `<summary><span class="lab-number">${String(i).padStart(2, '0')}</span><div><h3>${esc(lab.title)}</h3><p>${esc(lab.subtitle)}</p></div><span class="lab-time">5–10 min example</span><span class="expand-icon" aria-hidden="true">+</span></summary><div class="lab-body"><p class="lab-intro">${esc(lab.idea)}</p><pre class="lab-flow" aria-label="Control flow for ${esc(lab.title)}">${esc(lab.flow)}</pre><div class="lesson-grid"><div><h4>What you will learn</h4><ul>${lab.objectives.map(t => `<li>${esc(t)}</li>`).join('')}</ul></div><div><h4>Walk through an example</h4><p>${esc(lab.example)}</p></div><div><h4>Make it your own</h4><p>${esc(lab.exercise)}</p></div><div><h4>Expected output & check</h4><p>${esc(lab.checks)}</p></div></div><p class="lesson-takeaway"><strong>Takeaway.</strong> ${esc(lab.bridge)}</p><div class="lab-actions">${notebookActions(lab)}<label class="completion"><input type="checkbox" data-lab="${lab.id}" ${completed.includes(lab.id) ? 'checked' : ''}> I explored lab ${String(i).padStart(2, '0')}</label></div>${configured ? '' : '<p class="publish-note">Download this notebook and upload it to Colab, or configure the repository links.</p>'}</div>`;
  list.appendChild(detail);
});

list.addEventListener('change', event => {
  if (!event.target.matches('input[data-lab]')) return;
  const id = event.target.dataset.lab;
  completed = event.target.checked ? [...new Set([...completed, id])] : completed.filter(x => x !== id);
  updateProgress();
});
document.getElementById('reset-progress').addEventListener('click', () => {
  completed = [];
  list.querySelectorAll('input[data-lab]').forEach(input => { input.checked = false; });
  updateProgress();
});
document.getElementById('lab-search').addEventListener('input', event => {
  const query = event.target.value.trim().toLowerCase();
  let visible = 0;
  list.querySelectorAll('.lab').forEach(lab => { lab.hidden = !lab.dataset.search.includes(query); if (!lab.hidden) visible += 1; });
  document.getElementById('filter-status').textContent = query ? `${visible} ${visible === 1 ? 'lab' : 'labs'} found` : `All ${labs.length} labs`;
});
function openLab(id) {
  const lab = labs.find(l => `lab-${l.id}` === id);
  if (!lab) return;
  const detail = document.getElementById(id);
  document.getElementById('lab-search').value = '';
  list.querySelectorAll('.lab').forEach(item => { item.hidden = false; });
  document.getElementById('filter-status').textContent = `All ${labs.length} labs`;
  detail.open = true;
  detail.scrollIntoView({block:'start'});
}
if (configured) document.querySelectorAll('.repo-link').forEach(a => { a.href = `https://github.com/${config.repo}`; a.textContent = 'GitHub ↗'; });
function openHash() { openLab(window.location.hash.slice(1)); }
document.addEventListener('click', event => {
  const link = event.target.closest('a[href^="#lab-"]');
  if (link) openLab(link.getAttribute('href').slice(1));
});
window.addEventListener('hashchange', openHash);
updateProgress();
if (location.hash.startsWith('#lab-')) openHash();
