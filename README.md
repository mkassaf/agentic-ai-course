# From LLM Calls to Agentic Systems

Prepared by **Mustafa Assaf** · Teaching assistant

**[Course website](https://mkassaf.github.io/agentic-ai-course/)** · **[GitHub repository](https://github.com/mkassaf/agentic-ai-course)**

Eight introductory, hands-on labs for Python students preparing for the **AI Assisted Software Architecting Project**. Start with one model call and finish by testing a small council protocol and a feedback experiment. The configurable API client starts with **FreeInference / `qwen3.6-35b`**, using a key provided through Colab Secrets. Every notebook also has clearly labelled, scripted practice examples.

**Start here:** open [the course website](index.html), then [Lab 00](notebooks/00_llm_basics.ipynb). No GPU, framework account, or local installation is required for the Colab route.

## Learning path

Allow **60–90 minutes per lab**, plus preparation and extension exercises. Students should already know Python functions, lists, dictionaries, JSON, and basic exceptions. Students new to Python will need additional preparation.

| Lab | Topic | What you build | Notebook |
| --- | --- | --- | --- |
| 00 | A basic LLM call | A prompt, response, and observable request | [Open](notebooks/00_llm_basics.ipynb) |
| 01 | Structured outputs | A validated decision contract and rejection path | [Open](notebooks/01_structured_outputs.ipynb) |
| 02 | Grounding and retrieval | An evidence-backed answer with source IDs | [Open](notebooks/02_grounding.ipynb) |
| 03 | Tool use and bounded agents | A model-selected action/observation loop | [Open](notebooks/03_tool_use.ipynb) |
| 04 | Workflow patterns | Chaining, routing, and parallel branches | [Open](notebooks/04_workflows.ipynb) |
| 05 | Reflection | A bounded critique/revision workflow | [Open](notebooks/05_reflection.ipynb) |
| 06 | An architect council | Independent proposals, critique, vote, and dissent | [Open](notebooks/06_architect_council.ipynb) |
| 07 | Feedback and evaluation | Baselines, disjoint data, and a small experiment | [Open](notebooks/07_feedback_evaluation.ipynb) |

Each notebook contains an explanation, a worked example, executable checks, student tasks, and a connection to the project. The examples expose the underlying Python control flow before introducing frameworks. MCP, A2A, graph orchestration frameworks, and knowledge graphs are optional extensions.

## Run in Google Colab

Before this repository has been published, download a notebook and use **Colab → File → Upload notebook**. The notebooks are self-contained: they do not clone a repository, mount Drive, or fetch teaching datasets.

After publication, the course website generates a direct **Open in Colab** link for each notebook. Save your working copy in your own Drive. Use a CPU runtime and run cells from top to bottom. Shared notebooks include their saved outputs; clear outputs before submitting if they contain credentials or sensitive material. See [Google's Colab FAQ](https://research.google.com/colaboratory/faq.html).

Practice mode uses explicit fixtures to teach and test control flow. Its outputs, speed, and agreement are **not evidence about a model**. To run live, add the TA-provided key to Colab Secrets as `FREEINFERENCE_API_KEY`, grant notebook access, and change `MODE` to `"live"`. The initial settings are `BASE_URL="https://freeinference.org/v1"`, `MODEL="qwen3.6-35b"`, and `FAMILY="Qwen"`. Change these and `SECRET_NAME` to use another compatible service. See [API setup](docs/api-setup.md).

## For instructors

- [Teaching plan and learning outcomes](docs/curriculum.md)
- [Connection to the architect-council assignment](docs/project-bridge.md)
- [Instructor guide and assessment](docs/instructor-guide.md)
- [University API configuration](docs/api-setup.md)
- [Sources and acknowledgements](docs/sources.md)

The tiny lab council is a teaching example. The final project still requires at least three actual model families, a justified architecture, observable communication, human review, a credible knowledge base, and a substantially larger expert-reviewed benchmark. The course does not assume that councils beat individual models or that feedback always improves decisions.

## Publish on your GitHub

Publish **the contents of this folder** as the repository root. The existing enclosing workspace repository is separate.

1. Create or choose your course repository, then copy this folder's contents into it, including `.github/`.
2. Configure links: `python3 scripts/configure_repo.py YOUR-OWNER/YOUR-REPO --ref main`.
3. Commit and push to your chosen repository. Keep `main` as the default branch for the supplied workflows, or update their branch filters.
4. In **Settings → Pages → Build and deployment**, choose **GitHub Actions**.
5. Run the **Publish course** workflow if necessary. It checks the notebooks before deploying the static site.

The configuration command changes public link metadata only; it does not create a GitHub repository, upload files, or deploy. Colab links require the configured repository and branch to exist and be accessible to students. The Pages workflow configures links automatically using the repository where it runs. This follows [GitHub's custom Pages workflow guidance](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## Verify locally

Python **3.11** is the reference environment. Notebook examples use the standard library; the following dependencies are for verification and local Jupyter execution.

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

Open `http://localhost:8000/`. The executor runs every notebook in a fresh temporary directory in practice mode and does not save outputs into the published files. CI never receives or uses university API keys. Live gateway compatibility must be checked by the teaching team before class.

## Attribution

The public organisation of [Karthik Vaidhyanathan's Engineering Agentic AI school](https://karthikv1392.github.io/sdu-aai/) inspired this course's progressive structure. This repository contains original explanations and examples; participant-only slides and notebooks from that school are not included. Pattern terminology is grounded in [Anthropic's Building effective agents](https://www.anthropic.com/research/building-effective-agents). See [sources](docs/sources.md) for the remaining references and provenance.
