# Agentic AI, Step by Step

Prepared by **Mustafa Assaf**

**[Course website](https://mkassaf.github.io/agentic-ai-course/)** · **[GitHub repository](https://github.com/mkassaf/agentic-ai-course)**

Thirteen beginner labs in **general agentic AI**, connected by one small software architecture decision: **modular monolith or microservices?** Compare Python rules with a single prompt, improve and evaluate the prompt, retrieve a stored policy with embeddings and a vector database, then build an **architecture council** that debates, defers to a human architect, remembers, routes cases, and is evaluated against single models.

Nine core labs fit **three 90-minute lectures**, three labs each, and cover every pattern the council project needs. Four **self-study** labs then show the protocols, skills, and framework that students may use to connect and organize their council: MCP, Agent Skills, A2A, and LangGraph. Each self-study lab ends with a challenge for the student's own council. Each lab builds one worked example in short, numbered steps, checks the result, and ends with small exercises.

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
| 00 · Rules, then LLM calls | Run a Python rule on four projects, then count how often a model agrees | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/00_rules_and_llms.ipynb) | [View](notebooks/00_rules_and_llms.ipynb) |
| 01 · Better prompts and small evaluations | A guided prompt, a strict JSON parser, and a five-case quality gate | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/01_prompting_evaluation.ipynb) | [View](notebooks/01_prompting_evaluation.ipynb) |
| 02 · Retrieve architecture rules with RAG | Embed policies, store them in a Chroma vector database, retrieve by meaning, and check citations | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/02_rag_systems.ipynb) | [View](notebooks/02_rag_systems.ipynb) |

**Lecture 2 · Chain, act, debate (90 minutes)**

| Lab | Worked example | Colab | Notebook |
| --- | --- | --- | --- |
| 03 · Chain the steps of a decision | Requirements, options, trade-offs, and a decision record, with a gate after each step | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/03_prompt_chaining.ipynb) | [View](notebooks/03_prompt_chaining.ipynb) |
| 04 · ReAct: choose a tool, then decide | A guarded agent loop that finds a project, reads it, and decides | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/04_react_tools.ipynb) | [View](notebooks/04_react_tools.ipynb) |
| 05 · A council of architects: propose, challenge, agree | Three architects on three model families propose alone; a chair challenges, counts grounded votes, and keeps the dissent | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/05_architecture_council.ipynb) | [View](notebooks/05_architecture_council.ipynb) |

**Lecture 3 · Decide, learn, measure (90 minutes)**

| Lab | Worked example | Colab | Notebook |
| --- | --- | --- | --- |
| 06 · The human decides, the council learns | Human review and revision, a memory of past decisions, and a held-out before/after score | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/06_human_feedback_memory.ipynb) | [View](notebooks/06_human_feedback_memory.ipynb) |
| 07 · Route each case: rule or council | A model router with worked examples, a dispatch table, a safe fallback, and the cost of each kind of mistake | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/07_routing.ipynb) | [View](notebooks/07_routing.ipynb) |
| 08 · Does the council beat a single model? | Compare the council with its models alone; calibrate an LLM judge against human ratings | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/08_council_evaluation.ipynb) | [View](notebooks/08_council_evaluation.ipynb) |

**Self-study · Connect and organize your council**

| Lab | Worked example | Colab | Notebook |
| --- | --- | --- | --- |
| 09 · Architecture tools and our own MCP server | Read and write tools with validation, discovery, and error results | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/09_tools_mcp.ipynb) | [View](notebooks/09_tools_mcp.ipynb) |
| 10 · A skill for a short architecture decision record | Choose a skill from a catalog, write two ADRs, and check them | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/10_agent_skills.ipynb) | [View](notebooks/10_agent_skills.ipynb) |
| 11 · Delegate an architecture review with A2A | Propose, have a reviewer agent check it over A2A, and revise | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/11_a2a_protocol.ipynb) | [View](notebooks/11_a2a_protocol.ipynb) |
| 12 · A framework for choosing and checking | A LangGraph choose-and-check loop with a conditional retry | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/12_frameworks_langgraph.ipynb) | [View](notebooks/12_frameworks_langgraph.ipynb) |

Each notebook opens with what is new since the previous lab, then one setup cell that installs the reusable `coursekit` package from a pinned public GitHub revision. The RAG and memory labs (02 and 06) also install the Chroma vector database, and their first run downloads a small embedding model (about 80 MB). The MCP, A2A, and LangGraph labs install their official SDKs. Supporting transport code lives in the package, outside the notebooks. Each step is one code cell of at most 20 lines, and a lab has at most 75 lines of example code. You do not need a paid framework account.

## Use a live model

Start in `MODE="practice"` to inspect the scripted examples without a model API call. Practice tests Python behavior; its responses, scores, and speed are not evidence of model capability. Live evaluation checks the fictional policy on a few cases. Students must also inspect whether a reason is grounded in the supplied facts and explain one consequence; a correct label alone does not establish architecture quality.

For live model examples, add a Colab Secret named **`FREEINFERENCE_API_KEY`**, grant notebook access, and change the setup to:

```python
MODE = "live"
ask = make_ask(mode=MODE)
```

This uses FreeInference `qwen3.6-35b` by default. `make_ask` also accepts `base_url`, `model`, and `secret_name` for another compatible service. The MCP lab needs no live model; in the A2A lab, a live model proposes and a deterministic agent reviews. The council lab (05) needs **three model families** in live mode: FreeInference serves Qwen, so configure the other two architects with a second compatible service. See [API setup](docs/api-setup.md).

## Teaching guides

- [Curriculum and learning outcomes](docs/curriculum.md)
- [Instructor guide](docs/instructor-guide.md)
- [API setup and troubleshooting](docs/api-setup.md)
- [Technical references](docs/sources.md)

## More learning resources

- [Agentic AI Learning Lab](https://github.com/mkassaf/agentic-ai-learning-lab): a browser-based practice app with examples progressing from single prompts to tool use, reflection, and multi-agent workflows.
- [LangGraph Complete Guide](https://github.com/mkassaf/langgraph-complete-guide): Python examples covering chatbots, ReAct agents, supervisor patterns, and research workflows. Continue here after Lab 12.

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
