'use strict';
const labs = [
  {
    id: '00', file: '00_llms_prompting', title: 'LLMs and prompting', subtitle: 'Make one call, improve one prompt, check one response', topics: 'llm prompting messages json structure tokens api',
    idea: 'A model receives messages and generates a response. A clear task, useful context, and an output format make that response easier to use.',
    flow: 'task + context + output format → model → response',
    objectives: ['Make a small model call and read the response.', 'Compare a vague prompt with a clear one.'],
    example: 'Ask for a short reply to a customer asking about a late delivery. Then add a tone, a two-sentence limit, and a request not to invent a delivery date. Compare the two answers.',
    exercise: 'Change the tone from formal to friendly. Keep the task and length limit the same.',
    checks: 'Expect a short reply that addresses the request and avoids an invented date. If you request JSON, parse it and check the required field; readable text is not necessarily valid JSON.',
    bridge: 'Start with one useful call. Extra agent steps are worthwhile only when they solve a clear problem.'
  },
  {
    id: '01', file: '01_rag_systems', title: 'RAG systems', subtitle: 'Look up a small fact before asking the model to answer', topics: 'rag retrieval evidence citations grounding search context',
    idea: 'Retrieval-augmented generation gives the model relevant source text before it answers. You can build the basic mechanism with a few short documents.',
    flow: 'question → retrieve a source → model → answer + source ID',
    objectives: ['Retrieve a relevant snippet from a tiny collection.', 'Keep the source attached to the answer.'],
    example: 'Ask when the library closes. Retrieve the opening-hours note, include it in the prompt, and request an answer with the note’s source ID. Try a question the notes cannot answer.',
    exercise: 'Add a weekend-hours note and ask a weekend question.',
    checks: 'Expect an answer supported by the retrieved note and a real source ID. For missing information, expect an explicit “I don’t know.” A real citation ID alone does not prove the claim is supported.',
    bridge: 'Retrieval chooses the context; generation uses it. Inspect each step separately when an answer is wrong.'
  },
  {
    id: '02', file: '02_agent_foundations', title: 'Foundations of AI agents', subtitle: 'See a small action–observation loop and its stopping rule', topics: 'agent state actions observation tools loop termination budget',
    idea: 'An agent chooses a next action using its current state. Your program validates the action, supplies an observation, and decides when the loop must stop.',
    flow: 'choose action → check → run tool → observe → choose again\nstop at final answer or step limit',
    objectives: ['Distinguish one model call from an agent loop.', 'Add a step limit and an allowed-tool list.'],
    example: 'A tiny assistant looks up one fact before replying. Print its chosen action, the tool’s observation, and the final answer. This makes the loop visible without a framework.',
    exercise: 'Lower the step limit. Check what happens if the assistant cannot finish in time.',
    checks: 'Expect a short action/observation trace and a clear termination status. An unknown tool must fail before execution. Scripted practice checks this control flow rather than a model’s intelligence.',
    bridge: 'The model can suggest an action. The host program remains responsible for execution and limits.'
  },
  {
    id: '03', file: '03_tools_mcp', title: 'Tools and MCP', subtitle: 'Expose one small tool and call it through an MCP client', topics: 'tools mcp model context protocol client server sdk discovery',
    idea: 'A tool is a capability your program exposes. Model Context Protocol standardizes how an AI application connects to such capabilities and context.',
    flow: 'MCP client → discover tools → call lookup_note(topic) → note',
    objectives: ['Distinguish a Python tool from its protocol interface.', 'Discover and call a tool using the MCP SDK.'],
    example: 'Expose a read-only lookup_note tool. Discover its name and input schema through an MCP client, then ask it for a short note. Keep the lookup simple so the interface is the lesson.',
    exercise: 'Change the requested topic. Then omit the required argument and inspect the error result.',
    checks: 'Expect the matching note as the tool result. A call missing the required topic should return an error. Inspect the SDK result object as well as the text; a protocol does not supply permissions automatically.',
    bridge: 'MCP connects applications to tools and context. The agent loop still decides when to use them.'
  },
  {
    id: '04', file: '04_agentic_patterns', title: 'Agentic patterns', subtitle: 'Try chaining, routing, parallel work, and a revision step', topics: 'patterns workflow chain routing parallelization reflection evaluator optimizer',
    idea: 'Patterns are reusable ways to connect calls. Begin with a fixed workflow when you already know the steps; let the model choose only where that choice is useful.',
    flow: 'chain: extract → summarize\nroute: classify → choose handler\nparallel: independent checks → combine\nrevise: draft → critique → improve',
    objectives: ['Recognize the control flow of four small patterns.', 'Choose a pattern for a simple task.'],
    example: 'Process a short incoming message. Extract its topic, route it to a handler, or review it from two independent angles. Compare which calls each approach adds.',
    exercise: 'Add one category to the router and test a message from that category.',
    checks: 'Expect the message to reach the intended handler. Count the calls, keep branch results associated with their inputs, and bound revision attempts. More steps do not guarantee a better answer.',
    bridge: 'A pattern describes the arrangement of work. You can implement it in plain Python or in a framework.'
  },
  {
    id: '05', file: '05_a2a_protocol', title: 'A2A protocol', subtitle: 'Inspect an agent’s capability card and exchange a small message', topics: 'a2a agent2agent communication agent card message task sdk discovery',
    idea: 'A2A provides a common interface for agents to describe capabilities and communicate. Learn the message structure before attempting a large multi-agent system.',
    flow: 'discover Agent Card → send message → inspect response',
    objectives: ['Identify an Agent Card, a message, and a response.', 'Explain the different roles of A2A and MCP.'],
    example: 'Discover a small greeting assistant through its Agent Card, send Ada, and inspect the reply using the A2A SDK. Follow the identifiers and text parts through the exchange.',
    exercise: 'Change the greeting or advertised capability and verify the corresponding output.',
    checks: 'Expect a capability description and the reply “Hello, Ada!” associated with the request. This local SDK exchange uses the protocol routes; remote hosting and authentication are separate steps.',
    bridge: 'Use MCP for access to tools and context; use A2A when exposing an agent’s capabilities to another agent.'
  },
  {
    id: '06', file: '06_agent_skills', title: 'Agent skills', subtitle: 'Package a short, reusable procedure in a skill folder', topics: 'skills skill.md instructions metadata progressive disclosure reusable capabilities',
    idea: 'A skill packages task instructions and optional supporting resources. A SKILL.md file explains what the skill does and when it is useful.',
    flow: 'read name + description → select skill → load instructions → use',
    objectives: ['Create a small skill with name, description, and instructions.', 'Separate reusable procedure from the current task input.'],
    example: 'Write a note-summary skill that asks for three bullets and no invented facts. Inspect its metadata, load the instructions for a short note, and compare the result with the requested format.',
    exercise: 'Change the skill to produce a one-sentence summary. Keep the note itself outside the skill instructions.',
    checks: 'Expect a SKILL.md with the required metadata and clear steps. Check that the output follows the chosen format. Loading instructions does not itself enforce correctness or authorize every action described in a file.',
    bridge: 'Skills package procedural knowledge. Tools execute capabilities; frameworks organize the process. These pieces can work together.'
  },
  {
    id: '07', file: '07_frameworks_evaluation', title: 'Frameworks and evaluation', subtitle: 'Build a small LangGraph workflow and compare its behavior', topics: 'framework langgraph graph nodes state evaluation baseline test cases',
    idea: 'A framework provides building blocks for state and control flow. Map a small workflow to those blocks, then check whether the added structure serves your task.',
    flow: 'START → classify → respond → END\nsmall test set → compare with a simpler baseline',
    objectives: ['Identify state, nodes, and edges in an actual LangGraph example.', 'Run a small evaluation with a clear expected result.'],
    example: 'Build a short classify-and-reply graph for incoming messages. Follow the state from one node to the next. Compare the graph with a simple Python version using the same inputs.',
    exercise: 'Add one test case that the current system handles poorly. Change one thing and rerun the same checks.',
    checks: 'Expect the compiled graph to finish with the intended response field. Report passed cases and call counts. Keep unknown cost unknown; a tiny test set illustrates a method, not general model quality.',
    bridge: 'Choose a framework because its state and orchestration features help. Keep a simple baseline and observable tests.'
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
  detail.innerHTML = `<summary><span class="lab-number">${String(i).padStart(2, '0')}</span><div><h3>${esc(lab.title)}</h3><p>${esc(lab.subtitle)}</p></div><span class="lab-time">60–90 minutes</span><span class="expand-icon" aria-hidden="true">+</span></summary><div class="lab-body"><p class="lab-intro">${esc(lab.idea)}</p><pre class="lab-flow" aria-label="Control flow for ${esc(lab.title)}">${esc(lab.flow)}</pre><div class="lesson-grid"><div><h4>What you will learn</h4><ul>${lab.objectives.map(t => `<li>${esc(t)}</li>`).join('')}</ul></div><div><h4>Walk through an example</h4><p>${esc(lab.example)}</p></div><div><h4>Make it your own</h4><p>${esc(lab.exercise)}</p></div><div><h4>Expected output & check</h4><p>${esc(lab.checks)}</p></div></div><p class="lesson-takeaway"><strong>Takeaway.</strong> ${esc(lab.bridge)}</p><div class="lab-actions">${notebookActions(lab)}<label class="completion"><input type="checkbox" data-lab="${lab.id}" ${completed.includes(lab.id) ? 'checked' : ''}> I explored lab ${String(i).padStart(2, '0')}</label></div>${configured ? '' : '<p class="publish-note">Download this notebook and upload it to Colab, or configure the repository links.</p>'}</div>`;
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
