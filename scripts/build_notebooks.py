#!/usr/bin/env python3
"""Generate standalone, dependency-free notebooks from readable lesson sources."""
from pathlib import Path
import json
import sys
import textwrap
import ast

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = (ROOT / 'coursekit/runtime.py').read_text()
PATTERNS = (ROOT / 'coursekit/patterns.py').read_text().replace('from .runtime import parse_object\n', '')
PATTERN_NAMES = {
    '00_llm_basics': [],
    '01_structured_outputs': ['validate_proposal', 'proposal_prompt'],
    '02_grounding': ['retrieve', 'validate_proposal', 'proposal_prompt'],
    '03_tool_use': ['retrieve', 'bounded_tool_loop'],
    '04_workflows': [],
    '05_reflection': ['validate_proposal', 'proposal_prompt'],
    '06_architect_council': ['validate_proposal', 'proposal_prompt', 'run_council'],
    '07_feedback_evaluation': ['validate_proposal', 'proposal_prompt', 'run_council'],
}
FUNCTIONS = {node.name: ast.get_source_segment(PATTERNS, node) for node in ast.parse(PATTERNS).body if isinstance(node, ast.FunctionDef)}


def md(text):
    return {'cell_type': 'markdown', 'metadata': {}, 'source': textwrap.dedent(text).strip().splitlines(True)}


def code(text, hidden=False):
    return {'cell_type': 'code', 'execution_count': None, 'metadata': {'collapsed': True, 'jupyter': {'source_hidden': True}} if hidden else {}, 'outputs': [], 'source': textwrap.dedent(text).strip().splitlines(True)}


SETUP = '''
# Start with FreeInference; change these settings for any compatible gateway. Never paste a key here.
MODE = "practice"       # "live" makes real API calls and may use university quota.
BASE_URL = "https://freeinference.org/v1"  # API base, without /chat/completions
MODEL = "qwen3.6-35b"   # change to the exact identifier for another gateway/model
FAMILY = "Qwen"        # actual model family, verified by the teaching team
SECRET_NAME = "FREEINFERENCE_API_KEY"  # name of your Colab Secret, not the key itself
EXTRA_BODY = {}        # optional gateway-specific fields; cannot override contract/budgets
TOKEN_FIELD = "max_tokens"  # or "max_completion_tokens", according to the gateway

client = Client(mode=MODE, base_url=BASE_URL, model=MODEL, family=FAMILY,
                api_key=secret(SECRET_NAME) if MODE == "live" else "", token_field=TOKEN_FIELD, extra_body=EXTRA_BODY,
                max_calls=24, max_tokens=512, timeout=45)
print("Mode:", MODE, "| All practice outputs are scripted fixtures, not model reasoning.")
'''
COUNCIL_SETUP = '''
# Live councils use the configured gateway and the SAME secret, read once above.
# MODEL/FAMILY above configure the first peer; supply two OTHER actual families below.
# The primary client is used only to read the shared key; all calls below use peers.
COUNCIL_MODELS = [
    {"model": MODEL, "family": FAMILY},
    {"model": "", "family": ""},
    {"model": "", "family": ""},
]
peers = [Client(mode=MODE, base_url=BASE_URL,
                model=spec["model"], family=spec["family"] or f"practice-{i}",
                api_key=client._api_key, token_field=TOKEN_FIELD, extra_body=EXTRA_BODY,
                max_calls=24, max_tokens=700, timeout=45)
         for i, spec in enumerate(COUNCIL_MODELS)]
'''
COMMON_DOCS = '''
documents = [
    {"id": "D1", "text": "Synthetic course note: option A is the lightweight service. It minimizes operational work but has no durable replay in this exercise."},
    {"id": "D2", "text": "Synthetic course note: option B is the durable log. It supports replay and audit history but requires more operational effort in this exercise."},
]
scenario = "Choose A or B for event ingestion. A small operations team needs low maintenance; replay is desirable but not mandatory. State the trade-off."
'''
PROPOSALS = '''
fixtures = [
    {"option": "A", "rationale": "The small team prioritizes low maintenance.", "tradeoffs": ["No durable replay in this exercise."], "evidence": ["D1"], "confidence": 0.7},
    {"option": "A", "rationale": "Replay is desirable, not a hard constraint.", "tradeoffs": ["Future audit needs could require a change."], "evidence": ["D1", "D2"], "confidence": 0.6},
    {"option": "B", "rationale": "A durable history may reduce future migration risk.", "tradeoffs": ["The operations team must absorb additional effort."], "evidence": ["D2"], "confidence": 0.55},
]
'''


def notebook(slug, title, goals, concept, cells, bridge, challenge, readings, council=False):
    intro = f'''# {title}\n\n**Time:** 60–90 minutes · **Prerequisites:** basic Python; earlier labs in sequence.\n\n{goals}\n\n## The idea\n\n{concept}\n\n## Run this notebook\n\nUse **Runtime → Run all** in Google Colab (CPU runtime is enough), or run locally with Jupyter. No installation or repository clone is needed. The next collapsed cell is the complete shared runtime so this file can travel on its own.\n\nStart in `practice` mode: every response is an explicit, inspectable fixture. It tests Python control flow and failure handling; it is **not evidence of LLM capability**. For the initial live experiment, create a Colab Secret named `FREEINFERENCE_API_KEY`, enable notebook access to that secret, and change `MODE` to `live`. The defaults call `qwen3.6-35b` at `https://freeinference.org/v1`. To use a different compatible gateway, change `BASE_URL`, `MODEL`, `FAMILY` and `SECRET_NAME`; the secret name is configurable. Local Jupyter falls back to a hidden password prompt. Never save a key in a cell or output.\n\nThe client sends the same prompts to the configured OpenAI-compatible gateway, bounds calls/output/timeout, limits this notebook to two concurrent network calls, and never silently retries or switches keys. FreeInference requests disable streaming and ask to disable thinking; a model may ignore the thinking setting. The current model page lists the default Qwen model as non-thinking. Other gateways receive no provider-specific thinking field unless configured through `EXTRA_BODY`. A FreeInference cold-start placeholder stops the call with guidance to wait about 120 seconds and retry manually. The teaching team must verify gateway compatibility and available models first; no actual live service calls were made while building this scaffold. If your gateway uses another protocol, ask the TA for an adapter. Token usage is recorded only when reported, cost remains unknown, and practice has no real token usage.\n'''
    all_cells = [md(intro), code(RUNTIME, hidden=True), code(SETUP)]
    if PATTERN_NAMES[slug]:
        all_cells += [md('## Read the control flow\n\nThese small functions are the implementation used below. Read the checks and stopping rules before running the example; this is deliberately plain Python so you can change the orchestration.'), code('import re\nfrom collections import Counter\n\n' + '\n\n'.join(FUNCTIONS[name] for name in PATTERN_NAMES[slug]))]
    if council:
        all_cells += [code(COUNCIL_SETUP)]
    all_cells += cells
    all_cells += [md(f'''## Your experiment\n\n{challenge}\n\n## Bridge to the architect project\n\n{bridge}\n\n## Submit for this lab\n\nSave your modified notebook with secrets removed and include: (1) the change you made, (2) one successful and one failing example, (3) what the assertions establish, (4) an observation from a real model if university access is enabled, and (5) the call/token/latency trace. Explain any unknown metrics instead of inventing them.\n\n## Read further\n\n{readings}''')]
    data = {'nbformat': 4, 'nbformat_minor': 5, 'metadata': {'kernelspec': {'display_name':'Python 3','language':'python','name':'python3'}, 'language_info': {'name':'python','version':'3.11'}, 'colab': {'name': slug+'.ipynb', 'provenance': []}}, 'cells': all_cells}
    for i, cell in enumerate(data['cells']):
        cell['id'] = f'{slug[:20]}-{i:02d}'
    path = ROOT / 'notebooks' / (slug + '.ipynb')
    path.write_text(json.dumps(data, indent=1) + '\n')
    print(path.name)


notebook('00_llm_basics', 'Lab 00 · From a prompt to an LLM call',
'''By the end, you can identify the input, model, and output of a call; change a prompt deliberately; and separate a plausible answer from evidence.''',
'''An LLM generates a response from supplied context. A single call is not an autonomous agent. The application chooses when to call, what context to send, and how to handle failure. This course starts with observable behavior, not hidden reasoning traces.\n\n**Flow:** task → prompt + system instruction → model → text → human check.\n\n**Pacing:** 15 min concept/setup; 20 min worked example; 25 min experiment; 15 min discussion.''',
[
md('''## What goes into the LLM call\n\nA live call sends an HTTP POST to the API endpoint. `messages` contains the system instruction and task, `model` selects the configured model, and the token field bounds output length. The runtime adds the authorization header from Colab Secrets; it is deliberately absent from this printable example. This cell builds a payload only and makes no network call.'''),
code('''
example_payload = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": "Compare architecture alternatives; state uncertainty."},
        {"role": "user", "content": "What information is missing before choosing an event-ingestion design?"},
    ],
    TOKEN_FIELD: 128,
}
if urllib.parse.urlsplit(BASE_URL).hostname == "freeinference.org":
    example_payload.update({"stream": False, "thinking": {"type": "disabled"}})
print("POST", BASE_URL.rstrip("/") + "/chat/completions")
print(json.dumps(example_payload, indent=2))  # no key or authorization header
assert "Authorization" not in example_payload and "api_key" not in example_payload
'''),
md('''## A first call\n\nAsk for an architecture recommendation with two alternatives. The fixture is intentionally incomplete: it names a choice without measurements. Live output may differ. Do not treat model confidence as evidence.'''),
code('''
prompt = "A small team needs event ingestion. Compare a lightweight service and a durable event log in two sentences. Name one missing requirement."
answer = client.ask(prompt, system="Give a concise architecture comparison. State uncertainty.",
    practice="A lightweight service reduces operational effort; a durable log adds replay at extra complexity. Missing requirement: how long must events be retained?")
print(answer)
assert isinstance(answer, str) and answer.strip(), "An empty response is a failed call, not a recommendation."
'''),
md('''## Make one controlled prompt change\n\nAdd a hard requirement, keep the rest of the prompt fixed, and compare answers. This is a small qualitative experiment, not a reliability benchmark.'''),
code('''
constraint = "Hard requirement: events must be replayable for seven days."
constrained_answer = client.ask(prompt + " " + constraint,
    system="Give a concise architecture comparison. State uncertainty.",
    practice="The durable log better matches the explicit replay requirement in this exercise. We still need retention capacity and operations estimates.")
print(constrained_answer)
print(json.dumps(summarize_trace([client]), indent=2))
assert len(client.trace) == 2
assert all("api_key" not in row and "prompt" not in row for row in client.trace)
'''),
md('''**Expected observation:** the second fixture responds to the new constraint. With a live model, inspect whether it actually uses the requirement and whether it invents throughput numbers. A fluent answer alone does not establish correctness. `None` for token counts or cost means unknown; summed call latency is not an end-to-end benchmark.'''),
],
'''This becomes the **single-call baseline** in Experiment A. Save the exact prompt, model identifier, input context and output; the later council must be compared with each participating model alone.''',
'''Change `constraint` to require on-premise operation or a strict latency target. Before running, write which evidence you would need to justify a recommendation. Try a vague prompt and a specific prompt with the same model. Record a counterexample where an answer sounds certain but does not support its claim. Set a fresh practice `Client(max_calls=1)`, call it twice, and confirm the second call stops at the budget.''',
'''- [FreeInference quickstart](https://doc.freeinference.org/quickstart)\n- [FreeInference model catalog](https://doc.freeinference.org/models)\n- [OpenAI-compatible Chat Completions request/response schema](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create)\n- [Anthropic: Building effective agents](https://www.anthropic.com/research/building-effective-agents)''')

notebook('01_structured_outputs', 'Lab 01 · Turn text into a checked contract',
'''By the end, you can ask for JSON, validate a response before using it, and distinguish a schema-valid recommendation from a sound one.''',
'''Applications need contracts. A prompt that requests JSON does not guarantee valid JSON or truthful content. Parse, validate types and allowed values, check evidence references, and fail visibly. We use prompt-and-validate here for compatibility; this is not provider-enforced structured output.\n\n**Flow:** request a schema → parse JSON → validate → accept or stop.\n\n**Pacing:** 15 min contract design; 25 min example; 25 min failure injection; 10 min discussion.''',
[
code(COMMON_DOCS + PROPOSALS),
code('''
raw = client.ask(proposal_prompt(scenario, documents), practice=json.dumps(fixtures[0]))
proposal = validate_proposal(parse_object(raw), {d["id"] for d in documents})
print(json.dumps(proposal, indent=2))
assert proposal["option"] in {"A", "B", "abstain"}
'''),
md('''## Test inputs you should reject\n\nThese tests exercise the application boundary without spending university API quota. Evidence ID checking only proves that a referenced ID exists; you must still read the source and assess whether it supports the claim.'''),
code('''
invalid = ["not JSON", "[]",
    json.dumps(dict(fixtures[0], confidence=1.5)),
    json.dumps(dict(fixtures[0], confidence=True)),
    json.dumps(dict(fixtures[0], evidence=["MADE_UP_SOURCE"])),
    json.dumps(dict(fixtures[0], option="C")),
]
rejected = 0
for item in invalid:
    try:
        validate_proposal(parse_object(item), {"D1", "D2"})
    except (ValueError, TypeError):
        rejected += 1
assert rejected == len(invalid), "Invalid contracts must not enter the system."
print("Rejected", rejected, "invalid inputs.")
print(json.dumps(summarize_trace([client]), indent=2))
'''),
md('''**Expected observation:** a well-formed worked proposal passes; every malformed fixture fails. A live response may fail parsing: keep that failure as data, inspect its cause, and change the prompt or gateway configuration deliberately. Do not silently turn malformed output into a successful recommendation.'''),
],
'''Use typed proposal and critique messages so peers are swappable and every recommendation records an option, trade-offs, confidence and evidence. Validation is necessary for traceability, but it cannot certify architectural quality.''',
'''Extend the schema with a `missing_requirements` list and update both valid and invalid examples. Add an abstention case. Construct a proposal that passes every structural check yet misrepresents D1; explain why automated ID validation misses it. If you add a repair call, bound it to one attempt and record both attempts.''',
'''- [Function calling guide: validate application-side arguments](https://developers.openai.com/api/docs/guides/function-calling)\n- [JSON specification](https://www.rfc-editor.org/rfc/rfc8259)''')

notebook('02_grounding', 'Lab 02 · Retrieve evidence before answering',
'''By the end, you can implement a small retrieval baseline, attach source IDs to recommendations, and abstain when the retrieved context does not support an answer.''',
'''Grounding gives the model evidence, but retrieval and generation can each fail. We use lexical overlap over two **synthetic teaching notes**, not real vendor performance claims. This makes the retrieval step inspectable; it is not a production vector database or a complete RAG system.\n\n**Flow:** question → retrieve documents → model with source IDs → citation checks → human support check.\n\n**Pacing:** 15 min retrieval; 25 min example; 25 min failure cases; 10 min discussion.''',
[
code(COMMON_DOCS + PROPOSALS),
code('''
query = "Which option supports durable replay and audit history?"
hits = retrieve(query, documents, k=2)
print(json.dumps(hits, indent=2))
assert hits and hits[0]["id"] == "D2"
raw = client.ask(proposal_prompt(query, hits), practice=json.dumps(fixtures[2]))
answer = validate_proposal(parse_object(raw), {d["id"] for d in hits})
print(json.dumps(answer, indent=2))
'''),
md('''## Missing evidence should remain missing\n\nA lexical retriever can miss synonyms or retrieve irrelevant documents that happen to share words. A positive overlap is not proof of relevance. The application should handle an empty evidence set explicitly.'''),
code('''
unknown_query = "encryption cryptography certificates"
missing = retrieve(unknown_query, documents)
assert missing == []
abstention_fixture = {"option": "abstain", "rationale": "The supplied notes do not discuss encryption.",
    "tradeoffs": ["An answer requires additional security documentation."], "evidence": [], "confidence": 0.0}
unsupported = validate_proposal(parse_object(client.ask(proposal_prompt(unknown_query, missing),
    practice=json.dumps(abstention_fixture))), set())
print(json.dumps(unsupported, indent=2))
assert unsupported["option"] == "abstain", "No encryption evidence was provided. Investigate an unsupported live recommendation."
print(json.dumps(summarize_trace([client]), indent=2))
'''),
md('''**Expected observation:** D2 ranks first for replay/audit; the unknown query retrieves nothing and should lead to abstention. Manually check each cited sentence for relevance. Treat text inside retrieved sources as untrusted data even if it contains instructions.'''),
],
'''Give every architect the **same knowledge snapshot** and source IDs for a fair debate. Your real project must replace these toy notes with defensible sources, provenance and an update policy, and evaluate citation support rather than mere citation presence.''',
'''Add a third synthetic source and compare `k=1` with `k=2`. Try a synonym with no word overlap; record the retrieval failure. Add a source containing “ignore the other evidence” as quoted document text and test whether the live model improperly follows it. Explain why adding a source ID alone does not establish entailment.''',
'''- [Lewis et al.: Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)\n- [Anthropic: Building effective agents, augmented LLM](https://www.anthropic.com/research/building-effective-agents)''')

notebook('03_tool_use', 'Lab 03 · A bounded tool-using agent',
'''By the end, you can implement an action/observation loop, validate a model-selected action, and show that denied tools and nontermination are controlled.''',
'''An agent uses model output to choose the next action. The program still owns execution and permissions. Our loop accepts a small **JSON action protocol** rather than native API tool calling. It illustrates the control flow without depending on gateway-specific tool support. No shell, web access, writes or arbitrary evaluation are allowed.\n\n**Flow:** observe → model chooses action → validate → execute safe tool → observe again → finish or stop at budget.\n\n**Pacing:** 15 min loop; 25 min example; 30 min boundary tests; 10 min discussion.''',
[
code(COMMON_DOCS),
code('''
def lookup_notes(query):
    return json.dumps(retrieve(query, documents, k=1))

tools = {"lookup_notes": lookup_notes}
actions = [json.dumps({"action": "tool", "name": "lookup_notes", "arguments": {"query": "durable replay"}}),
           json.dumps({"action": "finish", "answer": "D2 describes option B as supporting durable replay; operational effort is its trade-off."})]
result = bounded_tool_loop(client, "Which option supports durable replay? Cite the note.", tools, actions, max_steps=3)
print(json.dumps(result, indent=2))
assert result["status"] in {"finished", "budget_exhausted"}
if MODE == "practice":
    assert result["status"] == "finished" and len(result["trace"]) == 1
'''),
md('''## A model cannot authorize its own tool\n\nThe application rejects unknown tools before execution, and a valid action can still be unhelpful. Keep the action trace: who requested what, what was returned, and when the loop stopped. We expose actions/observations, not private reasoning.'''),
code('''
for bad_action in [
    {"action": "tool", "name": "run_shell", "arguments": {"query": "anything"}},
    {"action": "tool", "name": "lookup_notes", "arguments": {"query": 123}},
]:
    try:
        bounded_tool_loop(Client(), "test", tools, [json.dumps(bad_action)])
    except ValueError:
        pass
    else:
        raise AssertionError("Unsafe action was accepted")
repeat = [actions[0]]
limited = bounded_tool_loop(Client(), "keep searching", tools, repeat, max_steps=2)
assert limited["status"] == "budget_exhausted" and len(limited["trace"]) == 2
print("Denied actions and the step limit behaved correctly.")
print(json.dumps(summarize_trace([client]), indent=2))
'''),
md('''**Expected observation:** the practice agent requests one lookup and then finishes. An endless sequence of lookups stops. Live models may select a different sequence or produce invalid JSON; both are useful findings. A finished answer still needs a source-support check.'''),
],
'''Use the same validated tool boundary for knowledge lookup in your council. MCP is an interoperability protocol you can investigate later; the core responsibility for validation, bounds and observability remains with your application.''',
'''Add a safe read-only `list_source_ids` tool with its own argument contract and tests. Try a fixture that returns `finish` immediately without evidence. Decide whether your application should accept it. Change `max_steps` and explain the cost/latency trade-off. Do not add unrestricted `eval`, filesystem writes or shell execution.''',
'''- [Yao et al.: ReAct](https://arxiv.org/abs/2210.03629)\n- [Model Context Protocol architecture](https://modelcontextprotocol.io/docs/learn/architecture)''')

notebook('04_workflows', 'Lab 04 · Chaining, routing and parallelization',
'''By the end, you can compose three common workflows, identify where control is fixed in code, and compare their latency and call count without assuming they improve quality.''',
'''A workflow follows a path defined by the application; a model-directed agent chooses its next action dynamically. Start with the least complex flow that solves the task. Chaining passes one result to the next step. Routing selects a branch. Parallelization runs independent analyses and then combines them.\n\n**Flow:** chain: extract → advise; router: classify → selected branch; parallel: independent checks → synthesis.\n\n**Pacing:** 15 min patterns; 30 min examples; 25 min experiment; 10 min comparison.''',
[
code(COMMON_DOCS),
md('''## 1. Chaining with an intermediate check'''),
code('''
requirements = parse_object(client.ask(scenario + '\\nReturn only {"hard_constraints": ["..."], "preferences": ["..."]}.',
    practice=json.dumps({"hard_constraints": [], "preferences": ["low maintenance", "replay desirable"]})))
assert set(requirements) == {"hard_constraints", "preferences"}
assert all(isinstance(v, list) and all(isinstance(x, str) for x in v) for v in requirements.values())
chain_answer = client.ask("Recommend A or B using only these requirements and notes: " + json.dumps([requirements, documents]),
    practice="A fits the low-maintenance preference; durable replay would favor B if it became mandatory.")
print(chain_answer)
'''),
md('''## 2. Routing with an allowed set of branches'''),
code('''
route = parse_object(client.ask(scenario + '\\nReturn only {"route":"operability"} or {"route":"reliability"}.',
    practice='{"route":"operability"}'))
if set(route) != {"route"} or route["route"] not in {"operability", "reliability"}:
    raise ValueError("Router selected an unknown branch")
branch_prompt = {"operability": "Identify the operational trade-off.", "reliability": "Identify the durability trade-off."}[route["route"]]
routed_answer = client.ask(branch_prompt + json.dumps(documents), practice="B adds operational effort for durable replay.")
print(route, routed_answer)
'''),
md('''## 3. Parallel independent reviews, then synthesis\n\nBoth reviews receive the original context and cannot see each other. Parallel completion order is not evidence order. Compare wall time with summed call latency: parallel work can overlap, and total token use can still increase.'''),
code('''
from concurrent.futures import ThreadPoolExecutor
started = time.perf_counter()
checks = ["Review operational effort.", "Review evidence gaps."]
fixtures_for_checks = ["A reduces effort but loses replay.", "No measurements establish the latency target."]
def review(item):
    question, fixture = item
    return client.ask(question + json.dumps(documents), practice=fixture)
with ThreadPoolExecutor(max_workers=2) as pool:
    reviews = list(pool.map(review, zip(checks, fixtures_for_checks)))
synthesis = client.ask("Combine these independent reviews, preserve uncertainty: " + json.dumps(reviews),
    practice="A is operationally simpler in the synthetic notes; evaluate latency separately and reconsider B if replay is mandatory.")
print(synthesis)
print("Parallel stage plus synthesis wall seconds:", round(time.perf_counter() - started, 4))
print(json.dumps(summarize_trace([client]), indent=2))
assert len(reviews) == 2 and all(isinstance(text, str) for text in reviews)
'''),
md('''**Expected observation:** all three workflows complete, but they spend different numbers of calls. A chain can propagate an extraction error; a router can choose the wrong valid branch; a synthesis can omit a minority concern. More calls are not automatically better.'''),
],
'''These patterns help you justify the council topology in an ADR. A deterministic pipeline, a bounded model-directed loop and a multi-agent debate have different failure modes. Name which behavior your architecture actually implements.''',
'''Run the same scenario through a single call and each workflow. Build a small comparison table: requirement coverage, supported citations, calls and observed latency. Add a routing counterexample. Remove the synthesis call and discuss what information is lost versus what quota is saved. Do not call the parallel reviews a debate unless they actually exchange and respond to messages.''',
'''- [Anthropic: Building effective agents, workflow patterns](https://www.anthropic.com/research/building-effective-agents)''')

notebook('05_reflection', 'Lab 05 · Critique and revise, with a stopping rule',
'''By the end, you can separate generation from critique, bound a revision loop, and test whether a change repairs a specific defect rather than merely sounding better.''',
'''An evaluator–optimizer loop asks for a draft, a critique, and a revision. It helps only when the critique identifies useful problems and the revision addresses them. A model can reinforce its own mistake. Here one round is an explicit stopping rule; structural checks are observable, while source support and architectural quality still require human review.\n\n**Flow:** draft → specific critique → one revision → validate → compare.\n\n**Pacing:** 15 min criteria; 25 min example; 25 min counterexamples; 10 min discussion.''',
[
code(COMMON_DOCS + PROPOSALS),
code('''
draft_fixture = dict(fixtures[0], evidence=["D9"])
draft = parse_object(client.ask(proposal_prompt(scenario, documents), practice=json.dumps(draft_fixture)))
try:
    validate_proposal(draft, {"D1", "D2"})
    initial_contract_valid = True
except ValueError:
    initial_contract_valid = False
critique = parse_object(client.ask("Identify specific problems in this draft using the notes. Return only {\\"issues\\":[\\"...\\"]}.\\n" + json.dumps({"draft": draft, "sources": documents}),
    practice=json.dumps({"issues": ["D9 does not exist in the source set; cite D1 for the operations claim and preserve the replay trade-off."]})))
if set(critique) != {"issues"} or not isinstance(critique["issues"], list) or not all(isinstance(x, str) for x in critique["issues"]):
    raise ValueError("Invalid critique contract")
revision = validate_proposal(parse_object(client.ask(proposal_prompt(scenario, documents) + '\\nDraft and critique: ' + json.dumps([draft, critique]) + '\\nRevise once; preserve the proposal schema.',
    practice=json.dumps(fixtures[0]))), {"D1", "D2"})
print(json.dumps({"initial_contract_valid": initial_contract_valid, "critique": critique, "revision": revision}, indent=2))
if MODE == "practice":
    assert not initial_contract_valid and revision["evidence"] == ["D1"]
assert len(client.trace) == 3, "One draft, one critique, one revision: the loop is bounded."
print(json.dumps(summarize_trace([client]), indent=2))
'''),
md('''**Expected observation:** the fixture repairs a nonexistent citation. That is a narrow, measurable improvement to the contract, not proof that the final choice is best. A live first draft may already be valid, or the revision may fail. Preserve both outputs and report the actual outcome.'''),
],
'''Peer architects should challenge a claim and then revise or defend it using evidence. Record why a position changed. The final project must compare outcomes before and after feedback; the existence of a critique message alone does not show learning.''',
'''Replace the bad citation with a valid but misleading citation. Write a human criterion for detecting the problem. Try a critique that wrongly pressures the model toward B; inspect whether revision becomes worse. Compare one versus two rounds using the same scenario and include total calls. Define an explicit condition that stops the loop and one that escalates to a human.''',
'''- [Anthropic: evaluator–optimizer workflow](https://www.anthropic.com/research/building-effective-agents)\n- [Shinn et al.: Reflexion](https://arxiv.org/abs/2303.11366)''')

notebook('06_architect_council', 'Lab 06 · A small architect council',
'''By the end, you can run isolated peer proposals, exchange critiques and revisions, preserve dissent, and distinguish a majority recommendation from a human decision.''',
'''The peers share an architect mandate, scenario, schema and knowledge snapshot. Their stances differ. In live mode they must also use **three university-verified model families**; three roles or temperatures of one model do not satisfy diversity. Family labels are administrative declarations, not proof: the TA must verify the gateway routing.\n\n**Flow:** independent proposals → shared critique → one revision round → chair policy → proposal + dissent → human decision.\n\nThe teaching chair is a deterministic controller with an explicit strict-majority rule, not an LLM chair agent. It always stops and escalates ties/abstention. The full student project must design and justify its chair agent and ADR-writing behavior.\n\n**Pacing:** 15 min protocol; 25 min execution; 30 min deadlock/dissent tests; 10 min interpretation.''',
[
code(COMMON_DOCS + PROPOSALS),
code('''
council = run_council(peers, scenario, documents, fixtures, rounds=1)
print(json.dumps(council, indent=2))
assert council["human_approval_required"] is True
assert len([h for h in council["history"] if h["phase"] == "independent"]) == 3
assert len([h for h in council["history"] if h["phase"] == "critique"]) == 3
assert len([h for h in council["history"] if h["phase"] == "revision"]) == 3
if MODE == "practice":
    assert council["decision"] == "A" and len(council["dissent"]) == 1
print(json.dumps(summarize_trace(peers), indent=2))
'''),
md('''## Deadlock and abstention are outcomes, not crashes\n\nUse separate practice clients to test the protocol at zero API cost. A tie must not be reported as consensus. Even unanimous model votes are not independent statistical samples and do not prove correctness.'''),
code('''
no_evidence = {"option": "abstain", "rationale": "The evidence is insufficient.",
    "tradeoffs": ["Ask a human to resolve the missing requirement."], "evidence": [], "confidence": 0.0}
tie = run_council([Client() for _ in range(3)], scenario, documents,
    [fixtures[0], fixtures[2], no_evidence], rounds=0)
assert tie["status"] == "escalate_to_human" and tie["decision"] is None
assert len(tie["dissent"]) == 3
print("Deadlock escalated; all three positions retained.")
'''),
md('''**Expected observation:** scripted peers propose A, A and B; after one round they retain their positions, so the chair emits a majority proposal with B recorded as dissent. Live outcomes may differ. The trace must show the exchange and stopping condition; agreement alone is not evidence of quality.'''),
],
'''This is a protocol learning scaffold, not the completed graded council. Students still need a real chair agent, robust message transport, swappable agents, defensible knowledge, feedback memory, baselines, 20+ expert-scored scenarios and a live observable demo.''',
'''Change one stance while keeping the architect mandate fixed. Add a fourth peer and create a 2–2 tie. Propose an alternative chair rule and record it in a short ADR. Compare the majority outcome with each model alone using exactly the same scenario and evidence. Identify dissent preserved by the trace but lost in a naive one-sentence summary.''',
'''- [Anthropic: orchestrator–workers and multi-agent trade-offs](https://www.anthropic.com/research/building-effective-agents)\n- Consult the original architect-council project handout supplied by your teaching team.''', council=True)

notebook('07_feedback_evaluation', 'Lab 07 · Evaluate a feedback loop honestly',
'''By the end, you can keep feedback and held-out scenarios separate, compare a council against every single-model baseline, and report small-sample limits, calls and latency.''',
'''Feedback can change the context used for later decisions without training model weights. This lab stores human-written **principles from feedback examples**, then evaluates before/after on disjoint toy scenarios. Both baselines and council receive identical scenario, source snapshot and feedback memory in each condition. No peer receives a held-out answer.\n\n**Flow:** split by scenario → evaluate before → derive memory from feedback only → evaluate after → compare with each model alone.\n\nWe use **four synthetic scenarios: two feedback and two held-out**. This is a wiring demonstration, not the project benchmark or evidence that councils improve quality. The practice fixtures deliberately encode the outcome so a score change only illustrates metric plumbing. For the graded project use 20+ expert-annotated scenarios, task-family-aware splits and a final untouched evaluation set.\n\n**Pacing:** 15 min protocol; 30 min experiment; 25 min interpretation; 10 min limitations.''',
[
code(COMMON_DOCS + PROPOSALS),
code('''
feedback = [
    {"id": "F1", "question": "For a two-person team, replay is optional. Choose A or B.",
     "human_feedback": "When replay is optional, favor lower operational effort unless another hard requirement rules it out."},
    {"id": "F2", "question": "A historical audit must reconstruct every event. Choose A or B.",
     "human_feedback": "Mandatory replay or audit reconstruction is a hard constraint; prioritize the durable option even when operations effort rises."},
]
heldout = [
    {"id": "T1", "question": "A prototype has one operator and no requirement to replay past events. Choose A or B.", "expert_option": "A"},
    {"id": "T2", "question": "Compliance requires reconstructing the event history after failures. Choose A or B.", "expert_option": "B"},
]
assert {x["id"] for x in feedback}.isdisjoint(x["id"] for x in heldout)
assert {x["question"] for x in feedback}.isdisjoint(x["question"] for x in heldout)
memory = "\\n".join(x["human_feedback"] for x in feedback)
assert all(x["question"] not in memory for x in heldout)
print("Feedback examples:", len(feedback), "| held-out examples:", len(heldout))
'''),
md('''## Measure each condition with the same context\n\nThe scored label is used only in the scoring code. Prompts contain the question and source notes, never `expert_option`. The fixture branch is deliberately scripted to make before/after easy to inspect; it cannot demonstrate learning. Council communication costs extra calls, which are measured instead of hidden. Baseline peers have no stance, debate or feedback loop of their own, but see the same supplied memory for a fair feedback-context comparison.'''),
code('''
def fixture_for(option):
    base = fixtures[0] if option == "A" else fixtures[2]
    return dict(base)

records = []
for condition, context_memory in [("before", ""), ("after", memory)]:
    for item in heldout:
        # Labels in this branch configure ONLY explicit practice fixtures; live ignores fixtures.
        scripted = [fixture_for(item["expert_option"] if condition == "after" else ("B" if i == 2 else "A")) for i in range(3)]
        for i, peer in enumerate(peers):
            start = len(peer.trace)
            started = time.perf_counter()
            prediction = validate_proposal(parse_object(peer.ask(
                proposal_prompt(item["question"], documents, context_memory),
                system="You are an architect. Make one evidence-based recommendation.",
                practice=json.dumps(scripted[i]))), {"D1", "D2"})
            records.append({"condition": condition, "scenario": item["id"], "method": f"single-{i}",
                "prediction": prediction["option"], "correct": prediction["option"] == item["expert_option"],
                "calls": len(peer.trace) - start, "latency_s": time.perf_counter() - started})
        start = sum(len(p.trace) for p in peers)
        started = time.perf_counter()
        result = run_council(peers, item["question"], documents, scripted, rounds=1, memory=context_memory)
        records.append({"condition": condition, "scenario": item["id"], "method": "council",
            "prediction": result["decision"], "correct": result["decision"] == item["expert_option"],
            "calls": sum(len(p.trace) for p in peers) - start, "latency_s": time.perf_counter() - started})

assert len(records) == 16
assert all(row["calls"] == (9 if row["method"] == "council" else 1) for row in records)
print(json.dumps(records, indent=2))
'''),
code('''
# Wilson interval is descriptive here: n=2 is far too small for a capability claim.
def wilson(successes, n, z=1.96):
    p = successes / n
    denominator = 1 + z*z/n
    center = (p + z*z/(2*n)) / denominator
    half = z * ((p*(1-p)/n + z*z/(4*n*n)) ** 0.5) / denominator
    return [round(max(0, center-half), 3), round(min(1, center+half), 3)]

summary = []
for condition in ["before", "after"]:
    for method in ["single-0", "single-1", "single-2", "council"]:
        rows = [r for r in records if r["condition"] == condition and r["method"] == method]
        correct = sum(r["correct"] for r in rows)
        summary.append({"condition": condition, "method": method, "correct": correct,
            "n": len(rows), "accuracy": correct / len(rows), "wilson_95_percent": wilson(correct, len(rows)),
            "calls": sum(r["calls"] for r in rows), "wall_latency_s": round(sum(r["latency_s"] for r in rows), 4)})
print(json.dumps(summary, indent=2))
print("API usage (unknown fields remain null):", json.dumps(summarize_trace(peers), indent=2))
if MODE == "practice":
    print("SCRIPTED DEMONSTRATION ONLY: the after fixtures encode the labels; these scores are not empirical findings.")
'''),
md('''**Expected observation:** the wiring yields one-call single-model baselines and a nine-call council for each scenario/condition. Practice “improvement” is intentionally authored into the fixtures. In live mode, record the actual outcome, including failures, abstentions and declines. A model response with invalid JSON stops the run visibly; do not drop it and score only successes.\n\n**Interpretation limits:** these labels encode a toy decision rule, not universal architecture truth. A 2/2 result has very wide uncertainty. Confidence intervals do not account for scenario dependence, repeated model sampling or expert disagreement. Reusing a held-out set to tune prompts leaks information: freeze prompts/memory rules before scoring, and reserve a fresh final test set for the capstone. Evaluate trade-off coverage and citation support with a human rubric as well as the simple choice-match metric.'''),
],
'''Build Experiment A (council vs each participating LLM alone, including best baseline) and Experiment B (before/after feedback on held-out scenarios) with expert labels, common knowledge/context and transparent cost/latency. Separate the effect of added feedback context from the effect of debate; a no-feedback single-call baseline is another useful, clearly labeled ablation. Calibrate any LLM judge against human ratings.''',
'''Add two new feedback cases and four new held-out cases without copying wording or scenario families across splits. Freeze the protocol before looking at results. Export `records` as JSON (never include keys), make a table of all baselines versus council, and state whether the council beats the best model. Add an abstention rate and a source-support human rating. If accuracy does not improve, report that result and investigate rather than changing labels.''',
'''- [HELM: holistic evaluation dimensions](https://crfm.stanford.edu/helm/)\n- [Anthropic: evaluation and complexity trade-offs](https://www.anthropic.com/research/building-effective-agents)''', council=True)
