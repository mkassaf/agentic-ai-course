# Agentic AI, Step by Step

Prepared by **Mustafa Assaf**

**[Course website](https://mkassaf.github.io/agentic-ai-course/)** · **[GitHub repository](https://github.com/mkassaf/agentic-ai-course)**

Eight beginner labs in **general agentic AI**. Start with a small LLM call, then explore RAG, agent loops, patterns, MCP, A2A, skills, and frameworks. Each lab uses one familiar task, short visible examples, an expected result, and a small exercise.

The four core areas are:

- **LLMs and Prompting · RAG Systems**
- **Foundations of AI Agents · Agentic Patterns**
- **Tools and MCP · A2A Protocol**
- **Skills · Frameworks**

## Start learning

Open a notebook in **Google Colab**, save a copy to your Drive, and run the cells in order. A CPU runtime is sufficient. Allow **60–90 minutes per lab**; the worked examples themselves are deliberately short. Students should know basic Python functions, lists, dictionaries, loops, and JSON.

| Lab | Small example | Colab | Notebook |
| --- | --- | --- | --- |
| 00 · LLMs and prompting | Improve a short support-reply prompt | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/00_llms_prompting.ipynb) | [View](notebooks/00_llms_prompting.ipynb) |
| 01 · RAG systems | Answer a library-hours question from notes | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/01_rag_systems.ipynb) | [View](notebooks/01_rag_systems.ipynb) |
| 02 · Foundations of AI agents | Follow one lookup in a bounded loop | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/02_agent_foundations.ipynb) | [View](notebooks/02_agent_foundations.ipynb) |
| 03 · Agentic patterns | Chain, route, parallelize, and revise small tasks | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/03_agentic_patterns.ipynb) | [View](notebooks/03_agentic_patterns.ipynb) |
| 04 · Tools and MCP | Discover and call a read-only note tool | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/04_tools_mcp.ipynb) | [View](notebooks/04_tools_mcp.ipynb) |
| 05 · A2A protocol | Discover a greeting agent and send a message | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/05_a2a_protocol.ipynb) | [View](notebooks/05_a2a_protocol.ipynb) |
| 06 · Agent skills | Package a note-summary procedure in SKILL.md | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/06_agent_skills.ipynb) | [View](notebooks/06_agent_skills.ipynb) |
| 07 · Frameworks and evaluation | Run a small LangGraph workflow and compare it | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/07_frameworks_evaluation.ipynb) | [View](notebooks/07_frameworks_evaluation.ipynb) |

The protocol and framework labs install their SDKs through notebook setup cells. Supporting code is collapsed so the main example stays readable. You do not need a paid framework account. MCP and A2A are core lessons with actual SDK examples, rather than simulated message dictionaries.

## Use a live model

Start in `MODE="practice"` to inspect the scripted examples without a model API call. Practice tests Python behavior; its responses and speed are not evidence of model capability.

For live model examples, add a Colab Secret named **`FREEINFERENCE_API_KEY`**, grant notebook access, and change `MODE` to `"live"`. The initial configuration is:

```python
BASE_URL = "https://freeinference.org/v1"
MODEL = "qwen3.6-35b"
SECRET_NAME = "FREEINFERENCE_API_KEY"  # secret name, never the key itself
```

The API adapter is provider-neutral: change the base URL, model, and secret name for another OpenAI-compatible Chat Completions service. Check current availability, quota, and compatibility before class. MCP/A2A demonstrations can teach the protocol without calling a live model. See [API setup](docs/api-setup.md).

## Teaching guides

- [Curriculum and learning outcomes](docs/curriculum.md)
- [Instructor guide](docs/instructor-guide.md)
- [API setup and troubleshooting](docs/api-setup.md)
- [Technical references](docs/sources.md)

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

The site is buildless HTML/CSS/JavaScript. Notebook sources and the generator keep the teaching examples reproducible. After changing a lesson, regenerate the notebooks and run the relevant checks.

For a fork, update public links with `python scripts/configure_repo.py OWNER/REPO --ref main`, then enable **GitHub Actions** as the Pages deployment source. The supplied workflow checks the course and publishes the static site. API credentials belong in private secrets, never in this repository.
