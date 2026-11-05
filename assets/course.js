'use strict';
const labs = [
  {
    "id": "00",
    "file": "00_rules_and_llms",
    "title": "Rules, then LLM calls",
    "subtitle": "A Python rule on four projects, then a model's guesses",
    "topics": "rules llm prompt architecture monolith microservices baseline",
    "idea": "Write the policy as a function that explains its answer, then see where a model that never saw the policy disagrees.",
    "flow": "projects → decide() and ask() → to_label() → agreement count",
    "objectives": [
      "Write a rule that returns a decision and a reason.",
      "Turn free-text model replies into labels.",
      "Count how often a model agrees with the rule."
    ],
    "example": "Run the policy on four projects that cover every combination of the two facts, then ask a model about the same projects.",
    "exercise": "Add an 8-person project with independent deploys, then test the boundary by changing >= to >.",
    "checks": "Only the Payments platform gets microservices. The scripted model agrees on 2 of 4 projects and gets both mixed cases wrong.",
    "bridge": "A disagreement shows what the model is missing: the policy itself.",
    "track": "lecture-1"
  },
  {
    "id": "01",
    "file": "01_prompting_evaluation",
    "title": "Better prompts and small evaluations",
    "subtitle": "A guided prompt, a strict parser, and a five-case quality gate",
    "topics": "prompting cot criteria few shot json evaluation testing",
    "idea": "Give the model explicit criteria and a worked example, reject badly formatted replies, and score the prompt on labelled cases.",
    "flow": "policy + example + case → JSON → parse → pass / fail / invalid → gate",
    "objectives": [
      "Write a precise, structured prompt.",
      "Validate model output before trusting it.",
      "Score a prompt on a labelled test set."
    ],
    "example": "Build a four-part guided prompt, parse its JSON reply, and score it on five cases, including the boundary of exactly 8 people.",
    "exercise": "Fix the scripted mistake, then break the format with an unknown label and watch the quality gate stop the run.",
    "checks": "Four of five scripted replies pass (80%), which just meets the gate. Practice scores test the evaluation code, not model quality.",
    "bridge": "Use checkable criteria and brief justifications; more reasoning text does not prove a better design.",
    "track": "lecture-1"
  },
  {
    "id": "02",
    "file": "02_rag_systems",
    "title": "Retrieve architecture rules with RAG",
    "subtitle": "Retrieval-Augmented Generation · Embeddings, a vector database, and grounded answers",
    "topics": "rag retrieval embeddings vectors vector database chroma similarity rules source architecture context retrieval-augmented generation",
    "idea": "Turn policies into embedding vectors, store them in a vector database, retrieve by meaning, and check that the answer cites its evidence.",
    "flow": "question → embed → nearest policies in Chroma → distance threshold → grounded answer → citation check",
    "objectives": [
      "Explain embeddings and compare two with cosine similarity.",
      "Store and query vectors in a vector database.",
      "Abstain when no evidence is close, and check citations."
    ],
    "example": "Embed four policies with all-MiniLM-L6-v2, store them in Chroma, and retrieve R1 for a reworded question that word matching misses.",
    "exercise": "Add a cloud-region question, tighten and loosen the distance threshold, and break a citation.",
    "checks": "The reworded question retrieves R1, the billing question R2, and the lunch question nothing. Both answers are grounded.",
    "bridge": "The same steps scale up: a larger embedding model, a persistent vector database, and many more documents.",
    "track": "lecture-1",
    "pattern": "Retrieval-Augmented Generation"
  },
  {
    "id": "03",
    "file": "03_prompt_chaining",
    "title": "Chain the steps of a decision",
    "subtitle": "Single-Path Planning · Requirements, options, trade-offs, and a record, with a gate after each step",
    "topics": "prompt chaining workflow gate requirements options trade-offs adr patterns council single-path planning",
    "idea": "Split one decision into small prompts; each reply feeds the next prompt, and a gate in plain Python stops a bad reply before it spreads.",
    "flow": "brief → requirements → gate → options → gate → trade-offs → gate → decision record → gate",
    "objectives": [
      "Decompose a decision into a chain of prompts.",
      "Write a gate that checks one step's reply.",
      "Pass each step only what it needs."
    ],
    "example": "Chain four prompts for the Payments platform, whose squads want independent releases while one engineer runs operations.",
    "exercise": "Break the requirements list, drop a trade-off mark, and make the decision name an option that was never proposed.",
    "checks": "Every gate passes, and the record chooses microservices while naming the cost for the one operations engineer.",
    "bridge": "Gates check the shape of each step, not whether the decision is wise; Lab 06 adds architects who disagree.",
    "track": "lecture-2",
    "pattern": "Single-Path Planning"
  },
  {
    "id": "04",
    "file": "04_why_tools",
    "track": "lecture-2",
    "pattern": "One-Step Tool Agent",
    "title": "Tools: let the model read and change live data",
    "subtitle": "One-Step Tool Agent · A hotel search tool and a booking tool, step by step",
    "topics": "tools tool calling function calling hotel search booking read write confirmation live data one-step tool agent",
    "idea": "A model knows only its training and its prompt; tools let it read live data and change it, while our code checks every request.",
    "flow": "question → model guesses → search tool → tool descriptions → model picks a tool → checked call → answer from the result → write tool after confirmation",
    "objectives": [
      "Explain why a model needs tools for live data.",
      "Describe tools and check every tool request.",
      "Separate read tools from write tools that need confirmation."
    ],
    "example": "A hotel booking system: the model guesses whether Harbor View has a room, then searches the live data and books the Alfama Inn after the user confirms.",
    "exercise": "Close a hotel, request an unknown tool, send a wrong argument type, and add a cancel tool.",
    "checks": "The guess is wrong; the search finds the Alfama Inn; the booking waits for confirmation, then leaves 2 rooms.",
    "bridge": "Lab 05 lets the model call tools again and again, choosing each next step from what it has seen."
  },
  {
    "id": "05",
    "file": "05_react_agent",
    "title": "ReAct: choose a tool, then decide",
    "subtitle": "One-Step Tool Agent in a ReAct loop · A guarded ReAct loop with a history",
    "topics": "agent foundations patterns react action observation loop chaining routing one-step tool agent in a react loop",
    "idea": "The model chooses each action and sees every observation so far; our code owns the tools, the guards, and the turn limit.",
    "flow": "goal + history → action → tool → observation → … → finish → check",
    "objectives": [
      "Follow a model-selected sequence of actions.",
      "Explain each guard and the turn limit.",
      "Check the agent's final decision."
    ],
    "example": "The goal names “our wiki project”, so the agent must list the projects, read the right one, and then decide.",
    "exercise": "Make the agent finish too early, recover from a wrong project name, and change the goal.",
    "checks": "Three turns: list_projects, get_project, finish. The decision matches the policy after two tool calls.",
    "bridge": "The model chooses the steps, but code owns the tools, the guards, and the turn limit. Self-study Lab 10 serves tools through MCP.",
    "track": "lecture-2",
    "pattern": "One-Step Tool Agent in a ReAct loop"
  },
  {
    "id": "06",
    "file": "06_architecture_council",
    "title": "A council of architects: propose, challenge, agree",
    "subtitle": "Debate-Based Cooperation · Independent proposals on three model families, challenges, and a chair",
    "topics": "multi-agent council debate parallel proposals critique revision consensus voting dissent chair coordinator grounding model families patterns debate-based cooperation",
    "idea": "Three architects on three model families propose alone and in parallel; a chair challenges unsupported claims, counts grounded votes, keeps the dissent, and escalates a deadlock.",
    "flow": "shared sources → 3 proposals in parallel → challenge ungrounded claims → revise → grounded votes → decision + dissent | escalation",
    "objectives": [
      "Collect independent proposals in parallel.",
      "Turn disagreement into sourced claims.",
      "Apply a stopping rule, record dissent, and handle a deadlock."
    ],
    "example": "Two architects choose microservices and one the modular monolith; the claim without a source is challenged and revised before the vote.",
    "exercise": "Cause a deadlock, cite a made-up source, and compare one model family with three in live mode.",
    "checks": "Six messages over three rounds; microservices wins 2 to 1, and the Safeguard's dissent citing F3 is kept.",
    "bridge": "Live mode uses three model families, each with its own key: Qwen on FreeInference, DeepSeek, and Gemini.",
    "track": "lecture-3",
    "pattern": "Debate-Based Cooperation"
  },
  {
    "id": "07",
    "file": "07_human_feedback_memory",
    "title": "The human decides, the council learns",
    "subtitle": "Human in the Loop, Scratchpad and Archival Memory · Human review, short- and long-term memory, and a held-out evaluation",
    "topics": "human in the loop feedback memory vector database chroma lessons evaluation held-out learning patterns council human in the loop and archival memory short-term memory long-term memory scratchpad",
    "idea": "The human architect reviews each proposal and keeps the final say; the accepted decision and its reasons become a memory that later cases recall.",
    "flow": "proposal → human review → revise with feedback → accept → store lesson → recall for new cases → score before / after",
    "objectives": [
      "Keep a human's final authority in a bounded review loop.",
      "Store and recall lessons from past decisions.",
      "Measure improvement on held-out cases only."
    ],
    "example": "The human rejects microservices for its operating cost; the lesson later changes the Logistics tracker's decision but not the Search platform's.",
    "exercise": "Accept or reject every proposal, tighten the recall distance, and add a case where the lesson should not apply.",
    "checks": "The revision is accepted after two reviews. Held-out score: 1 of 2 without memory, 2 of 2 with it.",
    "bridge": "Similar text does not mean a lesson applies; the project needs 20 or more held-out scenarios and repeated live runs.",
    "track": "lecture-3",
    "pattern": "Human in the Loop and Archival Memory"
  },
  {
    "id": "08",
    "file": "08_council_evaluation",
    "title": "Does the council beat a single model?",
    "subtitle": "A baseline comparison with a calibrated LLM judge",
    "topics": "evaluation baseline experiment llm judge calibration human ratings grounding cost latency council patterns",
    "idea": "Compare the council with each of its models alone on the same scenarios, by correctness, grounding, a judged trade-off measure, and cost; trust the LLM judge only after it agrees with human ratings.",
    "flow": "recorded runs → correct / grounded / calls / seconds → LLM judge → agreement with human sample → council vs best single model",
    "objectives": [
      "Compare a system with the strongest baseline.",
      "Use an LLM judge with a narrow rubric.",
      "Calibrate the judge against human ratings."
    ],
    "example": "Four systems answer two held-out scenarios; the judge rates whether each answer names a cost of its option.",
    "exercise": "Raise the calibration threshold, make the council wrong once, and remove a run.",
    "checks": "The judge agrees with the human on 3 of 4 answers. The council ties DeepSeek on correctness and beats it on grounding, at 5 times the calls.",
    "bridge": "Two scenarios demonstrate the method; the project needs 20 or more, and an honest report even when the council does not win.",
    "track": "lecture-3"
  },
  {
    "id": "09",
    "file": "09_routing",
    "title": "Route each case: rule or council",
    "subtitle": "Routing · A model router, a dispatch table, a safe fallback, and the cost of each mistake",
    "topics": "routing router classifier dispatch handlers fallback cost few shot council patterns",
    "idea": "A router reads each case and picks a handler: plain code for routine cases, the council for contested ones. Code owns the routes and falls back to the council when a reply is unusable.",
    "flow": "case → router (model) → valid route? → HANDLERS[route] → rule (0 calls) | council (5 calls) → compare with human routes",
    "objectives": [
      "Route inputs with a model and a dispatch table.",
      "Fall back safely on an unusable reply.",
      "Count routing cost and weigh the two kinds of mistake."
    ],
    "example": "Six cases with a note the rule cannot read; the router sends the two cases with one operations engineer to the council.",
    "exercise": "Skip a needed debate, send an unusable route, change a note, and compare a router with and without worked examples.",
    "checks": "The router agrees with the human on 5 of 6 cases, skips no needed debate, and costs 21 calls against 30.",
    "bridge": "Live, worked examples kept the router from skipping debates; a router that wastes too many debates costs more than none.",
    "track": "self-study",
    "pattern": "Routing"
  },
  {
    "id": "10",
    "file": "10_tools_mcp",
    "title": "Architecture tools and our own MCP server",
    "subtitle": "Registry & Adapter · Read and write tools with validation and errors",
    "topics": "tools mcp server client extract action agent foundations registry & adapter",
    "idea": "A tool reads data or performs an allowed action; MCP publishes its name, description, and input schema to any client.",
    "flow": "list_tools → get_project → apply policy → save_decision → error results",
    "objectives": [
      "Build MCP tools with typed arguments.",
      "Discover tools and their schemas as a client.",
      "Handle tool errors without changing state."
    ],
    "example": "Serve get_project and save_decision through the real MCP SDK, run a fixed workflow over two projects, then send three bad calls.",
    "exercise": "Add a project, add a list_projects tool, and send an argument of the wrong type.",
    "checks": "Both decisions are saved. Each bad call returns is_error=True, and the saved state does not change.",
    "bridge": "In a council, one MCP server can give every architect the same tools and sources.",
    "track": "self-study",
    "pattern": "Registry & Adapter"
  },
  {
    "id": "11",
    "file": "11_agent_skills",
    "title": "A skill for a short architecture decision record",
    "subtitle": "Skill Library Evolution · Choose a skill from a catalog, then check its output",
    "topics": "skills skill.md adr architecture decision record reusable skill library evolution",
    "idea": "A skill packages a procedure with a name and a description; an agent chooses from the descriptions and loads only the chosen instructions.",
    "flow": "catalog of descriptions → choose skill → load instructions + case → ADR → checker",
    "objectives": [
      "Split a SKILL.md file into its header and body.",
      "Explain progressive disclosure.",
      "Check a skill's output format."
    ],
    "example": "Pick the ADR skill from a three-skill catalog, then write and check decision records for two projects.",
    "exercise": "Give an incident task, add a Risk line to an ADR, and write a fourth skill.",
    "checks": "The ADR skill is chosen. Both records have Context, Decision, and Consequence, with a policy-consistent decision.",
    "bridge": "Only the chosen skill's instructions enter the prompt, so the catalog can grow.",
    "track": "self-study",
    "pattern": "Skill Library Evolution"
  },
  {
    "id": "12",
    "file": "12_a2a_protocol",
    "title": "Delegate an architecture review with A2A",
    "subtitle": "Generator–Critic Loop · A tiny hotel-desk agent over A2A, then review and revision",
    "topics": "a2a agent card discovery message review architecture generator–critic loop agent card hotel desk",
    "idea": "A2A lets one agent discover another through its Agent Card and exchange messages; the reviewer's feedback can drive a revision.",
    "flow": "propose → A2A review → FAIL? revise with feedback → review again",
    "objectives": [
      "Discover a reviewer agent and read its reply.",
      "Use another agent's feedback to revise.",
      "Bound a multi-agent exchange."
    ],
    "example": "Our model proposes a decision for four projects. A reviewer agent rejects one proposal, and the revision passes.",
    "exercise": "Add a second mistake, then make a revision wrong too.",
    "checks": "All four projects pass, with one revision for the Internal wiki.",
    "bridge": "The reviewer is deterministic and runs over real local A2A routes; practice mode needs no API key.",
    "track": "self-study",
    "pattern": "Generator–Critic Loop"
  },
  {
    "id": "13",
    "file": "13_frameworks_langgraph",
    "title": "A framework for choosing and checking",
    "subtitle": "Generator–Critic Loop · A LangGraph loop with a conditional retry",
    "topics": "framework langgraph state nodes edges evaluate architecture generator–critic loop",
    "idea": "A framework makes the steps, the shared state, and the decision to retry explicit.",
    "flow": "START → choose → check → retry? → choose … → END",
    "objectives": [
      "Define graph state and nodes.",
      "Route with a conditional edge.",
      "Keep generation separate from validation."
    ],
    "example": "Run a choose-and-check graph on four projects. One project fails, gets feedback, and passes on its second attempt.",
    "exercise": "Use up the attempts, allow a third attempt, and add a fifth project.",
    "checks": "All four projects pass, the Internal wiki after two attempts, for five model calls in total.",
    "bridge": "Passing a policy check is useful evidence, but not architecture quality. Try Lab 06's council as a graph.",
    "track": "self-study",
    "pattern": "Generator–Critic Loop"
  },
  {
    "id": "14",
    "file": "14_framing_contract",
    "track": "self-study",
    "title": "Frame the debate and agree on a message contract",
    "subtitle": "Passive Goal Creator and a contract · Quality-attribute scenarios, a typed proposal, and swappable architects",
    "topics": "framing quality attribute scenarios iso 25010 message contract schema confidence swappable agents chair passive goal creator and a contract",
    "idea": "The chair frames a brief as measurable quality-attribute scenarios; every proposal must follow one contract, so any architect can be added or replaced.",
    "flow": "brief → chair frames 3 ISO 25010 scenarios → gate → proposals → contract check → votes and confidence",
    "objectives": [
      "Write measurable quality-attribute scenarios.",
      "Enforce a message contract with confidence and trade-offs.",
      "Add an architect without changing the council's code."
    ],
    "example": "A Booking service with a Monday spike and an audit requirement; four architects answer, and one is rejected for breaking the contract.",
    "exercise": "Fix the rejected reply, make votes and confidence disagree, add an architect, and break the frame.",
    "checks": "Three scenarios pass the gate; the Auditor is rejected; votes 2 to 1 and confidence 1.3 to 0.9 agree.",
    "bridge": "Self-reported confidence is information, not proof; Lab 15 learns whom to trust from outcomes.",
    "pattern": "Passive Goal Creator and a contract"
  },
  {
    "id": "15",
    "file": "15_learning_curve_trust",
    "track": "self-study",
    "title": "Learn from feedback: a learning curve and per-model trust",
    "subtitle": "Voting-Based Cooperation · A feedback/test split, trust-weighted votes, and a curve",
    "topics": "evaluation experiment feedback test split held-out learning curve per-model trust weighted vote council voting-based cooperation",
    "idea": "Learn from feedback cases only, weight each architect by how much better than chance it has been, and score the test cases after every round.",
    "flow": "benchmark → split once → feedback round → update trust → weighted vote on test cases → learning curve",
    "objectives": [
      "Keep feedback and test cases apart.",
      "Turn agreement with the human into vote weights.",
      "Read a learning curve, including where it stalls."
    ],
    "example": "Ten small cases and three recorded architects; plain majority gets 2 of 4 test cases, the trusted council 4 of 4 after five rounds.",
    "exercise": "Reorder the feedback, weight by raw trust, and remove the best architect's slip.",
    "checks": "The learning curve is [2, 2, 2, 2, 2, 4, 4], with two escalated ties at round 4.",
    "bridge": "A curve that falls as well as rises is still evidence; plan your project's experiment with it.",
    "pattern": "Voting-Based Cooperation"
  }
];

const tracks = [
  {
    "id": "lecture-1",
    "label": "Lecture 1 · 90 minutes",
    "title": "Ask, check, retrieve",
    "note": "A rule, a model, a test set, and retrieval: the building blocks of every later lab."
  },
  {
    "id": "lecture-2",
    "label": "Lecture 2 · 90 minutes",
    "title": "Chain, call tools, act",
    "note": "From a fixed chain of prompts, to tools that read and change live data, to an agent that chooses its own steps."
  },
  {
    "id": "lecture-3",
    "label": "Lecture 3 · 90 minutes",
    "title": "Debate, decide, measure",
    "note": "A council of architects debates, a human decides, short- and long-term memory keep the lessons, and an experiment tests the council."
  },
  {
    "id": "self-study",
    "label": "Self-study · at your own pace",
    "title": "Build your council further",
    "note": "Routing, protocols, skills, a framework, framing, and a learning experiment: what the project needs beyond the lectures. Each lab ends with a challenge for your council."
  }
];

const list = document.getElementById('lab-list');
const esc = text => String(text).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const config = window.COURSE_CONFIG || {};
const configured = typeof config.repo === 'string' && /^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})\/[A-Za-z0-9_.-]+$/.test(config.repo) && config.repo !== 'OWNER/REPO';
const ref = typeof config.ref === 'string' ? config.ref : 'main';
let completed = [];
try { const stored = JSON.parse(localStorage.getItem('agentic-ai-course-architecture-v2-progress') || '[]'); if (Array.isArray(stored)) completed = stored.filter(x => labs.some(l => l.id === x)); } catch (_) { /* Browser storage is optional. */ }

function updateProgress() {
  const count = labs.filter(l => completed.includes(l.id)).length;
  document.getElementById('progress-label').textContent = `${count} / ${labs.length} labs explored`;
  document.getElementById('course-progress').value = count;
  try { localStorage.setItem('agentic-ai-course-architecture-v2-progress', JSON.stringify(completed)); } catch (_) { /* Private browsing can disable storage. */ }
}
function notebookActions(lab) {
  const path = `notebooks/${lab.file}.ipynb`;
  const colab = configured ? `https://colab.research.google.com/github/${config.repo}/blob/${encodeURIComponent(ref)}/${path}` : null;
  const action = colab ? `<a class="button primary" href="${esc(colab)}" target="_blank" rel="noopener">Open in Colab <span aria-hidden="true">↗</span></a>` : `<a class="button secondary" href="#setup">Colab setup <span aria-hidden="true">↑</span></a>`;
  return `<div class="notebook-actions">${action}<a class="button secondary" href="${path}" download>Download notebook <span aria-hidden="true">↓</span></a></div>`;
}

const trackGroups = {};
tracks.forEach(track => {
  const group = document.createElement('section');
  group.className = 'track';
  group.setAttribute('aria-label', `${track.label}: ${track.title}`);
  group.innerHTML = `<div class="track-heading"><span class="tag">${esc(track.label)}</span><h3>${esc(track.title)}</h3><p>${esc(track.note)}</p></div>`;
  list.appendChild(group);
  trackGroups[track.id] = group;
});

labs.forEach((lab, i) => {
  const detail = document.createElement('details');
  detail.className = 'lab';
  detail.id = `lab-${lab.id}`;
  detail.dataset.search = `${lab.title} ${lab.subtitle} ${lab.topics}`.toLowerCase();
  detail.innerHTML = `<summary><span class="lab-number">${String(i).padStart(2, '0')}</span><div><h3>${esc(lab.title)}</h3><p>${esc(lab.subtitle)}</p></div><span class="lab-time">15–20 min</span><span class="expand-icon" aria-hidden="true">+</span></summary><div class="lab-body"><p class="lab-intro">${esc(lab.idea)}</p><pre class="lab-flow" aria-label="Control flow for ${esc(lab.title)}">${esc(lab.flow)}</pre><div class="lesson-grid"><div><h4>What you will learn</h4><ul>${lab.objectives.map(t => `<li>${esc(t)}</li>`).join('')}</ul></div><div><h4>Walk through an example</h4><p>${esc(lab.example)}</p></div><div><h4>Make it your own</h4><p>${esc(lab.exercise)}</p></div><div><h4>Expected output & check</h4><p>${esc(lab.checks)}</p></div></div><p class="lesson-takeaway"><strong>Takeaway.</strong> ${esc(lab.bridge)}</p><div class="lab-actions">${notebookActions(lab)}<label class="completion"><input type="checkbox" data-lab="${lab.id}" ${completed.includes(lab.id) ? 'checked' : ''}> I explored lab ${String(i).padStart(2, '0')}</label></div>${configured ? '' : '<p class="publish-note">Download this notebook and upload it to Colab, or configure the repository links.</p>'}</div>`;
  trackGroups[lab.track].appendChild(detail);
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
  list.querySelectorAll('.track').forEach(group => { group.hidden = !group.querySelector('.lab:not([hidden])'); });
  document.getElementById('filter-status').textContent = query ? `${visible} ${visible === 1 ? 'lab' : 'labs'} found` : `All ${labs.length} labs`;
});
function openLab(id) {
  const lab = labs.find(l => `lab-${l.id}` === id);
  if (!lab) return;
  const detail = document.getElementById(id);
  document.getElementById('lab-search').value = '';
  list.querySelectorAll('.lab, .track').forEach(item => { item.hidden = false; });
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
