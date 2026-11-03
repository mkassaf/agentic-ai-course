'use strict';
const labs = [
  {
    "id": "00",
    "file": "00_rules_and_llms",
    "title": "Rules, then one LLM call",
    "subtitle": "Compare Python rules with one prompt",
    "topics": "rules llm prompt architecture monolith microservices baseline",
    "idea": "Start with a rule you can inspect, then ask a model the same architecture question.",
    "flow": "case → Python rule / one prompt → compare",
    "objectives": [
      "Run a deterministic rule.",
      "Compare it with one model prediction."
    ],
    "example": "A three-person team has no independent deployment requirement. Compare a Python decision with a single architecture prompt.",
    "exercise": "Increase the team size and request independent deployments.",
    "checks": "The course policy selects a modular monolith for the original case. Compare the model’s label with that baseline.",
    "bridge": "A clear baseline gives later experiments something to compare."
  },
  {
    "id": "01",
    "file": "01_prompting_evaluation",
    "title": "Better prompts and small evaluations",
    "subtitle": "Explicit criteria, one example, three test cases",
    "topics": "prompting cot criteria few shot json evaluation testing",
    "idea": "Give the model explicit criteria and a small worked example, then check its output.",
    "flow": "policy + example + case → JSON → score",
    "objectives": [
      "Write a precise, structured prompt.",
      "Check policy adherence on three cases."
    ],
    "example": "Compare basic and guided prompts on three cases. Read the JSON decision and brief reason.",
    "exercise": "Add team_size=7 with independent deployment required and compare live.",
    "checks": "Read the three-case score and inspect failures. Practice scores only test the scripted example, not model quality.",
    "bridge": "Use checkable criteria and brief justifications; more reasoning text does not prove a better design."
  },
  {
    "id": "02",
    "file": "02_rag_systems",
    "title": "Retrieve architecture rules with RAG",
    "subtitle": "Retrieve a stored rule before answering",
    "topics": "rag retrieval rules source architecture context",
    "idea": "Store the policy as text, retrieve a matching rule, and use it as model context.",
    "flow": "question → retrieve policy → grounded answer",
    "objectives": [
      "Retrieve the relevant rule.",
      "Trace the answer back to its source."
    ],
    "example": "Find the deployment rule in a tiny rule collection, then answer the same architecture question.",
    "exercise": "Ask which deployment region to use; expect no matching rule.",
    "checks": "Check the retrieved rule and source. A missing rule should produce no match rather than unrelated evidence.",
    "bridge": "This transparent keyword retriever illustrates RAG; larger systems may use embeddings and ranking."
  },
  {
    "id": "03",
    "file": "03_tools_mcp",
    "title": "Architecture tools and our own MCP server",
    "subtitle": "Build a tiny metrics tool and save action",
    "topics": "tools mcp server client extract action agent foundations",
    "idea": "A tool reads data or performs an allowed action; MCP exposes its interface to a client.",
    "flow": "read_metrics → inspect → save_decision",
    "objectives": [
      "Build and call your own MCP tools.",
      "Distinguish a read from an action."
    ],
    "example": "Expose project metrics and save one architecture decision to an in-memory list through the real MCP SDK.",
    "exercise": "Add a service_name field to the metrics fixture and inspect it.",
    "checks": "Check the extracted metrics and saved value. The action changes only the notebook’s in-memory data.",
    "bridge": "These fixed client calls become model-chosen actions in the next lab."
  },
  {
    "id": "04",
    "file": "04_agentic_patterns",
    "title": "ReAct: choose a tool, then decide",
    "subtitle": "A bounded ReAct-style tool loop",
    "topics": "agent foundations patterns react action observation loop chaining routing",
    "idea": "An agent chooses an allowed action, reads the observation, and decides when to finish.",
    "flow": "choose action → read_metrics → observe → finish",
    "objectives": [
      "Follow model-selected actions.",
      "Explain the loop’s stopping limit."
    ],
    "example": "Let a tiny architecture assistant request the project metrics before returning a decision.",
    "exercise": "Change the team metrics and predict the next decision.",
    "checks": "Check the observation, final answer, and stop condition. Reaching the turn limit alone is not success.",
    "bridge": "ReAct-style action and observation follows tools and MCP; larger patterns are further practice."
  },
  {
    "id": "05",
    "file": "05_agent_skills",
    "title": "A skill for a short architecture decision record",
    "subtitle": "Write a three-part decision record",
    "topics": "skills skill.md adr architecture decision record reusable",
    "idea": "A skill packages a reusable procedure separately from the current project data.",
    "flow": "load ADR skill + case → decision record",
    "objectives": [
      "Read a small SKILL.md file.",
      "Apply it to a new architecture case."
    ],
    "example": "Use short instructions to write Context, Decision, and Consequence for the same case.",
    "exercise": "Add a Risk section to the skill, practice answer, and check.",
    "checks": "Check the three sections, policy-consistent choice, and a supported consequence.",
    "bridge": "This example loads instructions directly; a skill-aware host can select them when needed."
  },
  {
    "id": "06",
    "file": "06_a2a_protocol",
    "title": "Delegate an architecture review with A2A",
    "subtitle": "Send a proposal to a reviewer agent",
    "topics": "a2a agent card discovery message review architecture",
    "idea": "A2A lets one application discover an agent and send it a message.",
    "flow": "discover reviewer → send proposal → review",
    "objectives": [
      "Discover an architecture reviewer.",
      "Inspect its policy review response."
    ],
    "example": "Send the tiny case and a proposed decision through real A2A protocol routes using the course helper.",
    "exercise": "Propose microservices for the same small case; expect a failed review.",
    "checks": "Expect Architecture reviewer and a PASS review for modular monolith. A microservices proposal should produce FAIL.",
    "bridge": "The reviewer is deterministic; the protocol exchange needs no model API key."
  },
  {
    "id": "07",
    "file": "07_frameworks_evaluation",
    "title": "A framework for choosing and checking",
    "subtitle": "A two-node LangGraph choose-and-check workflow",
    "topics": "framework langgraph state nodes edges evaluate architecture",
    "idea": "A framework makes the sequence and shared state explicit.",
    "flow": "START → choose → check → END",
    "objectives": [
      "Run two real LangGraph nodes.",
      "Keep generation separate from validation."
    ],
    "example": "One node proposes the architecture; the next checks it against the course policy.",
    "exercise": "Change the case and inspect the final state.",
    "checks": "Inspect the decision and policy-check result. Then explain one consequence the automatic check does not assess.",
    "bridge": "Passing a policy check is useful evidence, but does not establish overall architecture quality."
  }
];

const list = document.getElementById('lab-list');
const esc = text => String(text).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const config = window.COURSE_CONFIG || {};
const configured = typeof config.repo === 'string' && /^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})\/[A-Za-z0-9_.-]+$/.test(config.repo) && config.repo !== 'OWNER/REPO';
const ref = typeof config.ref === 'string' ? config.ref : 'main';
let completed = [];
try { const stored = JSON.parse(localStorage.getItem('agentic-ai-course-architecture-v1-progress') || '[]'); if (Array.isArray(stored)) completed = stored.filter(x => labs.some(l => l.id === x)); } catch (_) { /* Browser storage is optional. */ }

function updateProgress() {
  const count = labs.filter(l => completed.includes(l.id)).length;
  document.getElementById('progress-label').textContent = `${count} / ${labs.length} labs explored`;
  document.getElementById('course-progress').value = count;
  try { localStorage.setItem('agentic-ai-course-architecture-v1-progress', JSON.stringify(completed)); } catch (_) { /* Private browsing can disable storage. */ }
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
