# Agentic AI, Step by Step

Prepared by **Mustafa Assaf**

**[Course website](https://mkassaf.github.io/agentic-ai-course/)** · **[GitHub repository](https://github.com/mkassaf/agentic-ai-course)**

Eight beginner labs in **general agentic AI**. Start with a small LLM call, then explore RAG, agent loops, MCP, patterns, A2A, skills, and frameworks. Each lab has one tiny worked example, one check, and one small exercise.

The four core areas are:

- **LLMs and Prompting · RAG Systems**
- **Foundations of AI Agents · Agentic Patterns**
- **Tools and MCP · A2A Protocol**
- **Skills · Frameworks**

## Start learning

Open a notebook in **Google Colab**, save a copy to your Drive, and run the cells in order. A CPU runtime is sufficient. Allow **5–10 minutes for each worked example**, plus first-run setup. In class, use optional discussion and practice to fill a 60–90 minute session. Students should know basic Python functions, lists, dictionaries, loops, and JSON.

| Lab | Small example | Colab | Notebook |
| --- | --- | --- | --- |
| 00 · LLMs and prompting | Make one call and edit the prompt | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/00_llms_prompting.ipynb) | [View](notebooks/00_llms_prompting.ipynb) |
| 01 · RAG systems | Answer a question using two short notes | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/01_rag_systems.ipynb) | [View](notebooks/01_rag_systems.ipynb) |
| 02 · Foundations of AI agents | Follow one lookup in a bounded loop | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/02_agent_foundations.ipynb) | [View](notebooks/02_agent_foundations.ipynb) |
| 03 · Tools and MCP | Discover and call a read-only note tool | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/03_tools_mcp.ipynb) | [View](notebooks/03_tools_mcp.ipynb) |
| 04 · Agentic patterns | Try a tiny chain and router | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/04_agentic_patterns.ipynb) | [View](notebooks/04_agentic_patterns.ipynb) |
| 05 · A2A protocol | Discover a greeting agent and send a message | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/05_a2a_protocol.ipynb) | [View](notebooks/05_a2a_protocol.ipynb) |
| 06 · Agent skills | Read and apply short SKILL.md instructions | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/06_agent_skills.ipynb) | [View](notebooks/06_agent_skills.ipynb) |
| 07 · Frameworks | Run an actual two-node LangGraph workflow | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/07_frameworks_evaluation.ipynb) | [View](notebooks/07_frameworks_evaluation.ipynb) |

Each notebook starts with one setup cell that installs the reusable `coursekit` package from a pinned public GitHub revision. MCP, A2A, and LangGraph labs also install their relevant official SDK. Supporting runtime and server code lives in the package, outside the notebooks. The main example stays within 20 visible Python lines and two code blocks. You do not need a paid framework account.

## Use a live model

Start in `MODE="practice"` to inspect the scripted examples without a model API call. Practice tests Python behavior; its responses and speed are not evidence of model capability.

For live model examples, add a Colab Secret named **`FREEINFERENCE_API_KEY`**, grant notebook access, and change the setup to:

```python
MODE = "live"
ask = make_ask(mode=MODE)
```

This uses FreeInference `qwen3.6-35b` by default. `make_ask` also accepts `base_url`, `model`, and `secret_name` for another compatible service. MCP/A2A demonstrations need no live model. See [API setup](docs/api-setup.md).

## Teaching guides

- [Curriculum and learning outcomes](docs/curriculum.md)
- [Instructor guide](docs/instructor-guide.md)
- [API setup and troubleshooting](docs/api-setup.md)
- [Technical references](docs/sources.md)

## More learning resources

- [Agentic AI Learning Lab](https://github.com/mkassaf/agentic-ai-learning-lab): a browser-based practice app with examples progressing from single prompts to tool use, reflection, and multi-agent workflows.
- [LangGraph Complete Guide](https://github.com/mkassaf/langgraph-complete-guide): Python examples covering chatbots, ReAct agents, supervisor patterns, and research workflows. Continue here after Lab 07.

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
