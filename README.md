# Agentic AI, Step by Step

Prepared by **Mustafa Assaf**

**[Course website](https://mkassaf.github.io/agentic-ai-course/)** · **[GitHub repository](https://github.com/mkassaf/agentic-ai-course)**

Eighteen beginner labs in **general agentic AI**, connected by one small software architecture decision: **modular monolith or microservices?** Compare Python rules with a single prompt, improve and evaluate the prompt, retrieve a stored policy with embeddings and a vector database, then build an **architecture council** that debates, can be watched and traced, defers to a human architect, remembers, routes cases, and is evaluated against single models.

Nine core labs fit **three 90-minute lectures**, three labs each, and cover every pattern the council project needs. Nine **self-study** labs then cover what the project needs beyond the lectures: the council against single models, routing, MCP, Agent Skills, A2A, and LangGraph to connect and organize the council, quality-attribute framing with a message contract, a learning-curve experiment with per-model trust, and a decision-model lab that scores options with a weighted decision matrix and a System One model. Each self-study lab ends with a challenge for the student's own council. Each lab builds one worked example in short, numbered steps, checks the result, and ends with small exercises. Each lab opens with a pattern card that follows the [Architectural Patterns for Agentic AI](https://karthikv1392.github.io/agentic-patterns/) field guide: its name, context, problem, solution, trade-off, flow, and quality attributes.

The fictional course policy selects microservices only when `team_size >= 8` **and** `independent_deploys` is true; otherwise it selects a modular monolith. The starting case has a three-person team and no independent deployment requirement. This policy is a teaching fixture, not a general architecture recommendation.

The four core areas are:

- **LLMs and Prompting · RAG Systems**
- **Foundations of AI Agents · Agentic Patterns**
- **Tools and MCP · A2A Protocol**
- **Skills · Frameworks**

## Start learning

Open a notebook in **Google Colab**, save a copy to your Drive, and run the cells in order. A CPU runtime is sufficient. Allow **15–20 minutes for each lab**, plus first-run setup. In class, a 90-minute lecture runs three labs with a short introduction and discussion; see the [instructor guide](docs/instructor-guide.md) for the plan. Students should know basic Python functions, lists, dictionaries, loops, and JSON.

**Lecture 1 · Ask, check, retrieve (90 minutes)**

| Lab | Worked example | Colab | Notebook |
| --- | --- | --- | --- |
| 00 · From rules to LLM calls | Run a Python rule on four projects, then count how often a model agrees | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/00_rules_and_llms.ipynb) | [View](notebooks/00_rules_and_llms.ipynb) |
| 01 · Prompting and small evaluations | A guided prompt, a strict JSON parser, a five-case quality gate, and a live plain-vs-reasoning contrast | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/01_prompting_evaluation.ipynb) | [View](notebooks/01_prompting_evaluation.ipynb) |
| 02 · RAG: ground answers in retrieved knowledge | Embed policies, store them in a Chroma vector database, retrieve by meaning, and check citations | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/02_rag_systems.ipynb) | [View](notebooks/02_rag_systems.ipynb) |

**Lecture 2 · Chain, call tools, act (90 minutes)**

| Lab | Worked example | Colab | Notebook |
| --- | --- | --- | --- |
| 03 · Prompt chaining with quality gates | Requirements, options, trade-offs, and a decision record, with a gate after each step | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/03_prompt_chaining.ipynb) | [View](notebooks/03_prompt_chaining.ipynb) |
| 04 · Tool calling: let the model read and change live data | A hotel booking system: the model guesses without a tool, then searches live rooms and books one after the user confirms | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/04_why_tools.ipynb) | [View](notebooks/04_why_tools.ipynb) |
| 05 · ReAct agents: reason, act, observe | A guarded agent loop that finds a project, reads it, and decides | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/05_react_agent.ipynb) | [View](notebooks/05_react_agent.ipynb) |

**Lecture 3 · Debate, trace, decide (90 minutes)**

| Lab | Worked example | Colab | Notebook |
| --- | --- | --- | --- |
| 06 · Multi-agent debate: propose, challenge, agree | Three architects on three model families propose alone; a chair challenges, counts grounded votes, and keeps the dissent | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/06_multi_agent_debate.ipynb) | [View](notebooks/06_multi_agent_debate.ipynb) |
| 07 · Observability, tracing, and swappable agents | A bus that logs every message, live and to a JSON log file, an optional LangSmith trace, a trace from the decision back to its sources in that file, and a rule-based agent added in one line | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/07_observe_trace_swap.ipynb) | [View](notebooks/07_observe_trace_swap.ipynb) |
| 08 · Human-in-the-loop and agent memory | Human review and revision, a memory of past decisions, and a held-out before/after score | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/08_human_feedback_memory.ipynb) | [View](notebooks/08_human_feedback_memory.ipynb) |

**Self-study · Go deeper**

| Lab | Worked example | Colab | Notebook |
| --- | --- | --- | --- |
| 09 · Evaluation: a multi-agent system against a single model | Compare the council with its models alone; calibrate an LLM judge against human ratings | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/09_multi_agent_evaluation.ipynb) | [View](notebooks/09_multi_agent_evaluation.ipynb) |
| 10 · Routing: rules, models, and a safe fallback | A model router with worked examples, a dispatch table, a safe fallback, and the cost of each kind of mistake | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/10_routing.ipynb) | [View](notebooks/10_routing.ipynb) |
| 11 · MCP: serve tools through a standard protocol | Read and write tools with validation, discovery, and error results | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/11_tools_mcp.ipynb) | [View](notebooks/11_tools_mcp.ipynb) |
| 12 · Agent skills: reusable instructions on demand | Choose a skill from a catalog, write two ADRs, and check them | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/12_agent_skills.ipynb) | [View](notebooks/12_agent_skills.ipynb) |
| 13 · A2A: delegate work to another agent | Propose, have a reviewer agent check it over A2A, and revise | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/13_a2a_protocol.ipynb) | [View](notebooks/13_a2a_protocol.ipynb) |
| 14 · Agent frameworks: graphs with LangGraph | A LangGraph choose-and-check loop with a conditional retry | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/14_frameworks_langgraph.ipynb) | [View](notebooks/14_frameworks_langgraph.ipynb) |
| 15 · Problem framing and typed message contracts | Quality-attribute scenarios from ISO/IEC 25010, a proposal contract with confidence, and a fourth architect added in one line | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/15_framing_contract.ipynb) | [View](notebooks/15_framing_contract.ipynb) |
| 16 · Learning from feedback: learning curves and trust weights | A feedback/test split, trust-weighted votes, and a learning curve over feedback rounds | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/16_learning_curve_trust.ipynb) | [View](notebooks/16_learning_curve_trust.ipynb) |
| 17 · Decision models: a weighted decision matrix with a scoring model | Criteria weighted in code, option scores from a vote, an average, or a scoring model, and a weight that flips the winner | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/17_weighted_decision_jev.ipynb) | [View](notebooks/17_weighted_decision_jev.ipynb) |

Each notebook opens with what is new since the previous lab, then one setup cell that installs the reusable `coursekit` package from a pinned public GitHub revision. The RAG and memory labs (02 and 08) also install the Chroma vector database, and their first run downloads a small embedding model (about 80 MB). The MCP, A2A, LangGraph, and decision-model labs install their official SDKs (the decision-model lab installs the TypeSafe SDK for the live JEV step). Supporting transport code lives in the package, outside the notebooks. Each step is one code cell of at most 20 lines, and a lab has at most 75 lines of example code. You do not need a paid framework account.

## Use a live model

Start in `MODE="practice"` to inspect the scripted examples without a model API call. Practice tests Python behavior; its responses, scores, and speed are not evidence of model capability. Live evaluation checks the fictional policy on a few cases. Students must also inspect whether a reason is grounded in the supplied facts and explain one consequence; a correct label alone does not establish architecture quality.

For live model examples, add a Colab Secret named **`FREEINFERENCE_API_KEY`**, grant notebook access, and change the setup to:

```python
MODE = "live"
PROVIDER = "freeinference"  # or "gemini" or "deepseek"
ask = make_ask(mode=MODE, provider=PROVIDER)
```

| Provider | Default model | Colab Secret |
| --- | --- | --- |
| `freeinference` | `qwen3.6-35b` (Qwen) | `FREEINFERENCE_API_KEY` |
| `gemini` | `gemini-3.5-flash` (Gemini) | `GEMINI_API_KEY` |
| `deepseek` | `deepseek-flash` (DeepSeek) | `DEEPSEEK_API_KEY` |

`make_ask` also accepts `model`, `base_url`, and `secret_name` to override a provider's defaults or to use another compatible service. The MCP, learning-curve, and decision-model labs need no live model to run; in the A2A lab, a live model proposes and a deterministic agent reviews. The council lab (06) needs **three model families** in live mode, so it uses all three providers at once and needs all three keys. The decision-model lab (17) has an optional live step that asks TypeSafe's System One model **JEV** to score each option; it needs a `TYPESAFE_API_KEY` in Colab Secrets and installs the TypeSafe SDK. JEV can also be reached over OpenRouter as `typesafe/jev-1.13`, served through OpenRouter's decisions endpoint rather than chat completions. Lab 01's Step 5 is an optional live demo of **reasoning models** — it calls a plain `gpt-3.5-turbo-0613` and a reasoning `qwen/qwen3-235b-a22b-thinking-2507` directly on OpenRouter and needs `OPENROUTER_API_KEY` in Colab Secrets (see below). See [API setup](docs/api-setup.md).

The course model keys: `FREEINFERENCE_API_KEY` (default), `GEMINI_API_KEY`, and `DEEPSEEK_API_KEY` for the council, `TYPESAFE_API_KEY` for Lab 17's scoring step, and `OPENROUTER_API_KEY` for Lab 01's reasoning demo.

## Teaching guides

- [Curriculum and learning outcomes](docs/curriculum.md)
- [Instructor guide](docs/instructor-guide.md)
- [API setup and troubleshooting](docs/api-setup.md)
- [Technical references](docs/sources.md)

## More learning resources

- [Agentic AI Learning Lab](https://github.com/mkassaf/agentic-ai-learning-lab): a browser-based practice app with examples progressing from single prompts to tool use, reflection, and multi-agent workflows.
- [LangGraph Complete Guide](https://github.com/mkassaf/langgraph-complete-guide): Python examples covering chatbots, ReAct agents, supervisor patterns, and research workflows. Continue here after Lab 14.

## Run and verify locally

Python **3.11** is the reference environment. From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/build_notebooks.py
python -m unittest discover -s tests -v
python scripts/check_course.py
python scripts/execute_notebooks.py
python -m http.server 8000
```

Open [the local website](http://localhost:8000/). The notebook executor checks practice examples in fresh temporary directories. CI uses no model API keys and makes no paid model calls. Live-provider behavior requires a separate small smoke check with student-equivalent access.

## Maintain the course

The site is buildless HTML/CSS/JavaScript. Short lesson sources generate the notebooks; reusable helpers live in `coursekit/`. After changing a helper, publish that commit and put its SHA in `coursekit-ref.txt`, then regenerate the notebooks. Run the relevant checks after changing lessons or helpers.

For a fork, update public links with `python scripts/configure_repo.py OWNER/REPO --ref main`, then enable **GitHub Actions** as the Pages deployment source. The supplied workflow checks the course and publishes the static site. API credentials belong in private secrets, never in this repository.
