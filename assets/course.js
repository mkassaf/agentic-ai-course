'use strict';
const labs = [
  {
    id: '00', file: '00_llm_basics', title: 'Your first LLM call', subtitle: 'Messages, prompts, responses, and the simplest useful baseline', topics: 'prompt llm api baseline tokens model',
    idea: 'An LLM call maps messages to a response. Your program decides what to send and what happens next. Begin with one call you can inspect before adding any autonomy.',
    flow: 'system instruction + user request\n              ↓\n         model call\n              ↓\n  text response + usage + latency',
    objectives: ['Explain the roles of the prompt, model, context, and response.', 'Make one live API call and inspect its trace.', 'Keep a single-call baseline to compare with later systems.'],
    example: 'Ask for an ingestion architecture for factory telemetry. Compare an open-ended question with a prompt that specifies on-premises deployment, a small operations team, and an explicit request for uncertainties. Look for information the model assumes rather than receives.',
    exercise: 'Change one requirement at a time. Write down which parts of the answer should change, then compare that expectation with the live response. Keep the original prompt and result.',
    checks: 'The scripted run makes no network calls. In live mode, one request returns text and a trace; unknown token usage remains unknown. A plausible recommendation is not proof that its assumptions are correct.',
    bridge: 'This call becomes the non-agentic baseline. Keep its scenario, evidence, and model identifier so the eventual comparison is fair.'
  },
  {
    id: '01', file: '01_structured_outputs', title: 'Turn text into a contract', subtitle: 'JSON, validation, and graceful handling of imperfect responses', topics: 'json schema structure validation contract errors',
    idea: 'A model response becomes useful software input only when your program checks its shape and meaning. Asking for JSON is an instruction; validation is a separate responsibility.',
    flow: 'request a proposal → parse JSON → validate fields\n                                 ↙           ↘\n                            accept        fail clearly',
    objectives: ['Separate valid JSON from a valid proposal.', 'Validate required fields, allowed values, and evidence references.', 'Handle malformed output without silently accepting it.'],
    example: 'Represent an architecture proposal as an option, rationale, evidence references, and confidence. Try responses with a missing field, an invented citation, or a confidence value outside the permitted range. Syntax alone catches none of the domain-level mistakes.',
    exercise: 'Add an explicit assumptions field and one new validation rule. Supply both a valid and an invalid example, then explain what your validator can and cannot establish.',
    checks: 'The normal example passes. Deliberately malformed or incomplete responses fail with a useful explanation. Confidence is a self-report from the model, not an empirical probability of correctness.',
    bridge: 'The project requires structured, swappable messages. A shared output contract lets architects and the chair communicate without brittle string matching.'
  },
  {
    id: '02', file: '02_grounding', title: 'Ground the answer in evidence', subtitle: 'A small retrieval pipeline you can inspect from end to end', topics: 'rag retrieval grounding citations evidence knowledge source',
    idea: 'Retrieval-augmented generation selects external context before asking the model to answer. Retrieval quality and answer quality are different things; inspect both.',
    flow: 'question → retrieve source snippets → build context\n                                          ↓\n                           answer + source identifiers\n                                          ↓\n                              check citation membership',
    objectives: ['Build a transparent lexical retriever over a tiny knowledge base.', 'Pass the same retrieved context to each compared model.', 'Check citation identifiers and recognize unsupported claims.'],
    example: 'Retrieve teaching snippets about operational burden and messaging options for an ingestion scenario. Keep source IDs with each snippet. A citation checker can confirm that an ID exists; a human still needs to check whether the source supports the claim.',
    exercise: 'Add one relevant and one distracting source, then change the retrieval limit. Ask an unanswerable question and design an abstention rule. Include a hostile instruction inside a source and explain why it is data rather than authority.',
    checks: 'Retrieved items retain stable source IDs. Invented source IDs are rejected. Empty or weak retrieval is visible. A matched citation does not guarantee entailment, freshness, or factual accuracy.',
    bridge: 'Every architect should receive a common evidence base with provenance. Later, compare lexical retrieval with embeddings or a knowledge graph only when you can evaluate the difference.'
  },
  {
    id: '03', file: '03_tool_use', title: 'Let the model choose an action', subtitle: 'Tools, observations, permissions, and a bounded agent loop', topics: 'tools agent loop actions observation allowlist budget safety',
    idea: 'A tool-using agent chooses its next action from the current state. The host program validates that choice, runs only permitted tools, and returns an observation. The model proposes an action; your code controls execution.',
    flow: 'state → choose {tool, arguments} → validate → execute\n  ↑                                            ↓\n  └──────────── observation ───────────────────┘\nstop: final answer OR call/step budget exhausted',
    objectives: ['Trace a model-selected action/observation loop.', 'Validate tool names and arguments before execution.', 'Stop cleanly when an agent repeats itself or reaches its limit.'],
    example: 'Give an architect a small evidence-search tool. The agent requests a lookup, receives a source-bearing observation, and returns a final recommendation. The exercise uses an explicit JSON action protocol so you can see the mechanism without a framework.',
    exercise: 'Add a read-only tool or change the search arguments. Then test an unknown tool, malformed arguments, and an agent that never chooses to finish. Explain why exposing arbitrary Python execution would change the risk.',
    checks: 'Only allowlisted tools execute. Denied actions raise a visible error before execution. The loop terminates within its declared budget and distinguishes a normal final answer from budget exhaustion.',
    bridge: 'Evidence lookup can be a tool in the council. MCP may later standardize that interface; it does not replace validation, permissions, or a termination rule.'
  },
  {
    id: '04', file: '04_workflows', title: 'Compose useful agentic patterns', subtitle: 'Prompt chaining, routing, and parallelization in plain Python', topics: 'patterns workflows chain routing parallelization orchestration',
    idea: 'In a workflow, code defines the main sequence of steps. Start with a predictable workflow when you know the process. Add dynamic decisions only where they serve a clear purpose.',
    flow: 'chaining:       extract → analyze → summarize\nrouting:        classify → select one handler\nparallelization: same input → independent analyses → combine',
    objectives: ['Recognize three common workflow patterns.', 'Keep each step’s input and output explicit.', 'Compare the additional calls and failure points with a single call.'],
    example: 'Chain a requirement extractor to an architecture summarizer. Route a request to the relevant analysis. Run independent quality-attribute reviews in parallel, then combine their outputs. Observe what the orchestrating Python code decides in each case.',
    exercise: 'Choose a pattern for two different requests and justify the choice. Add a failing branch and decide whether the workflow should stop, retry explicitly, or return a partial result. Measure calls rather than assuming parallel means cheaper.',
    checks: 'Chained steps use the preceding output. Routing selects a valid handler. Parallel analyses start from the same input, and results are associated with the correct branch. More calls do not automatically mean better quality.',
    bridge: 'These are building blocks for your council topology. Select and justify a pattern in an ADR instead of choosing a framework before defining the behavior.'
  },
  {
    id: '05', file: '05_reflection', title: 'Critique, revise, and stop', subtitle: 'An evaluator–optimizer loop with explicit acceptance checks', topics: 'reflection critique revision evaluator optimizer quality feedback',
    idea: 'Reflection adds a critique and a revision to a draft. It can surface omissions, but it can also reinforce a mistake. Improvement needs a criterion independent of the model’s claim that the revision is better.',
    flow: 'draft → critique against rubric → revise → check\n                                           ↓\n                             accept / stop at round limit',
    objectives: ['Define a concrete critique rubric.', 'Pass the draft and critique into a revision step.', 'Apply a stopping condition and retain the earlier version.'],
    example: 'Draft an architecture recommendation, critique missing assumptions and trade-offs, then revise. Check whether the revised output satisfies the contract and addresses the stated omissions. Compare the actual claims, not just the length of the answer.',
    exercise: 'Create a draft with one missing requirement and a draft with one false claim. Check whether the critic catches both. Set a maximum number of rounds and define what happens when the critique remains unresolved.',
    checks: 'The revision sees the draft and critique. The loop stops at its limit. A schema-valid revision can still be wrong. Record when a revision harms quality or leaves an objection unanswered.',
    bridge: 'This supplies the critique-and-revise stage of the architect debate. Require an argument and evidence for a changed position; agreement by itself is not success.'
  },
  {
    id: '06', file: '06_architect_council', title: 'Build a small architect council', subtitle: 'Independent proposals, structured debate, dissent, and a chair', topics: 'multi agent council debate consensus chair model families stances',
    idea: 'A council is an interaction protocol, not simply three consecutive calls. Preserve independence before the first debate round, make messages traceable, and decide how to handle persistent disagreement.',
    flow: 'same requirements + evidence\n       ↓           ↓           ↓\n   model A      model B      model C\n       └── independent proposals ──┘\n             ↓ critique + revise (bounded)\n             ↓ chair proposal + dissent\n             ↓ human decision',
    objectives: ['Separate independent proposal and shared debate phases.', 'Keep a common message contract and an attributable trace.', 'Record disagreement and distinguish a chair decision from consensus.'],
    example: 'Three peers examine the same ingestion scenario with pragmatist, guardian, and skeptic stances. They propose alone before viewing peers’ messages. A bounded exchange produces a chair recommendation while retaining the minority rationale.',
    exercise: 'Introduce a deadlock or add a peer. Check that the chair does not relabel a split vote as consensus. Configure three distinct approved model families for a live run and document the actual family behind each gateway alias.',
    checks: 'Initial prompts contain no peer proposals. Every message identifies its author and stage. Debate terminates. Dissent is preserved. Scripted peers or three stances on one model only test the protocol; they do not establish model diversity.',
    bridge: 'The lab is a small protocol scaffold. The assessed project still needs your architecture, real model diversity, evidence retrieval, live observability, ADRs, feedback mechanism, and evaluation.'
  },
  {
    id: '07', file: '07_feedback_evaluation', title: 'Test whether the system improves', subtitle: 'Baselines, feedback, held-out scenarios, cost, and honest conclusions', topics: 'evaluation benchmark feedback heldout baseline accuracy cost latency memory',
    idea: 'Treat “the council is better” and “feedback improves later decisions” as hypotheses. A tiny example teaches the evaluation pipeline; it cannot establish a general performance claim.',
    flow: 'scenarios → disjoint feedback / held-out split\nfeedback set → update memory or principles\nheld-out set → score before / score after\ncompare: each single model vs council\nreport: quality + citations + calls + latency + limits',
    objectives: ['Keep feedback examples out of held-out evaluation.', 'Compare the council with each constituent model used alone.', 'Report changes, costs, and uncertainty without promising improvement.'],
    example: 'Run the toy feedback and held-out sets through a scoring harness. Store feedback-derived principles and repeat the evaluation using the same held-out questions. Keep model versions, input context, and scoring rules fixed so you can explain the comparison.',
    exercise: 'Design an expert-reviewed benchmark of at least 20 project scenarios. Include cases with multiple defensible decisions and a rubric for trade-off coverage and evidence support. Add repeated runs and a context-matched single-model feedback ablation.',
    checks: 'Scenario IDs do not overlap between feedback and held-out sets. Held-out labels never enter prompts or memory. Baselines receive the same scenario and evidence. Unknown usage or cost is not reported as zero. A negative result remains a valid finding.',
    bridge: 'This prepares experiments A and B. Keep a final test set untouched while choosing your design; repeatedly inspecting the same held-out results can turn that set into development data.'
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
  detail.innerHTML = `<summary><span class="lab-number">${String(i).padStart(2, '0')}</span><div><h3>${esc(lab.title)}</h3><p>${esc(lab.subtitle)}</p></div><span class="lab-time">60–90 minutes</span><span class="expand-icon" aria-hidden="true">+</span></summary><div class="lab-body"><p class="lab-intro">${esc(lab.idea)}</p><pre class="lab-flow" aria-label="Control flow for ${esc(lab.title)}">${esc(lab.flow)}</pre><div class="lesson-grid"><div><h4>What you will learn</h4><ul>${lab.objectives.map(t => `<li>${esc(t)}</li>`).join('')}</ul></div><div><h4>Walk through an example</h4><p>${esc(lab.example)}</p></div><div><h4>Make it your own</h4><p>${esc(lab.exercise)}</p></div><div><h4>What to check</h4><p>${esc(lab.checks)}</p></div></div><p class="capstone-bridge"><strong>Project connection.</strong> ${esc(lab.bridge)}</p><div class="lab-actions">${notebookActions(lab)}<label class="completion"><input type="checkbox" data-lab="${lab.id}" ${completed.includes(lab.id) ? 'checked' : ''}> I explored lab ${String(i).padStart(2, '0')}</label></div>${configured ? '' : '<p class="publish-note">Before publication: download and upload this notebook to Colab. The TA can activate direct links with scripts/configure_repo.py.</p>'}</div>`;
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
