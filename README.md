# Agentic AI, Step by Step

Prepared by **Mustafa Assaf**

[Course website](https://mkassaf.github.io/agentic-ai-course/) · [GitHub repository](https://github.com/mkassaf/agentic-ai-course)

Eighteen short Colab labs teach agentic systems while students revise **Microservices & Their Patterns** and **Microservices Lecture 2 - Condensed DDD**. Each lab provides the relevant context, asks two questions, applies the ideas in a small executable example, and ends with a change to try.

The examples use ShopEasy, the lectures' social app, and small checkout scenarios. They cover operational readiness, business boundaries, aggregates, private service data, CQRS, resilience, saga compensation, contracts, anti-corruption layers, and Kafka semantics. The old eight-person architecture rule and hotel-booking examples have been replaced. Scores, workloads, and scripted replies are explicitly teaching fixtures, not empirical results.

## Start in Colab

Save a copy of a notebook to your Drive and run cells in order with a CPU runtime. Students should know Python functions, dictionaries, lists, loops, and JSON. Allow roughly 15–20 minutes per lab, plus installation and discussion. Each core step has at most 25 Python lines; each lab has at most 100 example lines.

**Lecture 1 (00–02):** rules, prompting/evaluation, RAG. **Lecture 2 (03–05):** chaining, tools, ReAct. **Lecture 3 (06–08):** debate, observability, human feedback/memory. Labs 09–17 are self-study extensions.

| Lab | Microservices revision | Colab |
| --- | --- | --- |
| 00 · From rules to LLM calls | Independent deployment and scaling; Microservice premium; Operational prerequisites | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/00_rules_and_llms.ipynb) |
| 01 · Prompting and small evaluations | Operational prerequisites; At-least-once delivery and event identity; Criteria-based architecture decisions | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/01_prompting_evaluation.ipynb) |
| 02 · RAG: ground answers in retrieved knowledge | Database per service; API composition vs CQRS; Idempotent consumers and transactional outbox | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/02_rag_systems.ipynb) |
| 03 · Prompt chaining with quality gates | Event storming; Bounded contexts and ubiquitous language; Business capability vs technical-layer decomposition | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/03_prompt_chaining.ipynb) |
| 04 · Tool calling: let the model read and change live data | Aggregate root; Entity vs value object; Consistency boundary and invariant | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/04_why_tools.ipynb) |
| 05 · ReAct agents: reason, act, observe | Cascading failure; Circuit breaker vs retry; Idempotency and graceful degradation | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/05_react_agent.ipynb) |
| 06 · Multi-agent debate: propose, challenge, agree | API composition versus CQRS; Eventual consistency and read-model cost | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/06_multi_agent_debate.ipynb) |
| 07 · Observability, tracing, and swappable agents | Correlation IDs across service boundaries; Structured logs and immutable event facts | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/07_observe_trace_swap.ipynb) |
| 08 · Human-in-the-loop and agent memory | Idempotent reads versus non-idempotent charges; Bounded retries and deduplicated effects | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/08_human_feedback_memory.ipynb) |
| 09 · Evaluation: a multi-agent system against a single model | Choose data patterns from requirements; Measure label agreement, citation validity, and trade-offs | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/09_multi_agent_evaluation.ipynb) |
| 10 · Routing: rules, models, and a safe fallback | Retry safety and fallback choices; Different costs of routing errors | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/10_routing.ipynb) |
| 11 · MCP: serve tools through a standard protocol | Database per service; API composition versus CQRS; Tool schema and validation | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/11_tools_mcp.ipynb) |
| 12 · Agent skills: reusable instructions on demand | Saga compensation in reverse completion order; Read-only steps need no undo; No isolation and intermediate states; Skill discovery and bounded repair | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/12_agent_skills.ipynb) |
| 13 · A2A: delegate work to another agent | Anti-corruption layer; Published internal contract; Agent Card discovery | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/13_a2a_protocol.ipynb) |
| 14 · Agent frameworks: graphs with LangGraph | Additive event changes; Published contract; Bounded generator–critic repair | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/14_frameworks_langgraph.ipynb) |
| 15 · Problem framing and typed message contracts | Dependency-specific resilience; Non-idempotent payment safety; Requirements versus assumed targets | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/15_framing_contract.ipynb) |
| 16 · Learning from feedback: learning curves and trust weights | Retry eligibility and idempotency; Correlated reviewer errors; Feedback/test separation | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/16_learning_curve_trust.ipynb) |
| 17 · Decision models: a weighted decision matrix with a scoring model | task queues versus retained event logs; independent consumer groups and replay; partition key versus eventId; consumer parallelism is capped by partitions | [Run](https://colab.research.google.com/github/mkassaf/agentic-ai-course/blob/main/notebooks/17_weighted_decision_jev.ipynb) |

## Practice and live models

Start in `MODE="practice"`. Model replies are explicit scripted fixtures: practice validates the Python workflow, not model intelligence. The MCP and A2A labs use real local SDK protocol exchanges, without deploying business services. No Kafka broker, cloud account, or production payment provider is required.

For a live model, put `FREEINFERENCE_API_KEY` in Colab Secrets, grant access, and choose `MODE="live"`. The default is FreeInference `qwen3.6-35b`. The same `make_ask` interface supports university gateways and the Gemini and DeepSeek presets; see [API setup](docs/api-setup.md). Lab 06 requires all three providers in live mode. Lab 09 only runs its judge live; its comparison inputs are marked synthetic. Lab 17's optional scoring call uses a separate `TYPESAFE_API_KEY` and explicit live mode.

A passed format/citation check does not prove factual support or a good architecture. Read the result against the lecture, inspect the trade-off, and report negative results honestly. Do not infer a universal architecture rule from a tiny fixture.

## Teaching and revision guides

- [Curriculum](docs/curriculum.md)
- [Instructor guide](docs/instructor-guide.md)
- [API setup](docs/api-setup.md)
- [Technical references](docs/sources.md)

## More learning resources

- [Agentic AI Learning Lab](https://github.com/mkassaf/agentic-ai-learning-lab)
- [LangGraph Complete Guide](https://github.com/mkassaf/langgraph-complete-guide)

## Run and verify locally

Use Python 3.11 as the reference environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
node scripts/export_diagrams.js
python scripts/build_notebooks.py
python -m unittest discover -s tests -v
python scripts/check_course.py
python scripts/execute_notebooks.py
python -m http.server 8000
```

Practice execution uses fresh temporary directories and no model keys. Chroma downloads a small embedding model on first use. Optional MLflow tracking is an extra cell after Lab 09, with synthetic data labelled as such; it is not required for core execution.

## Maintain the course

Edit `lessons/*.json`, including each lesson's `review` metadata, and keep the site summaries in `assets/course.js` aligned. `scripts/build_notebooks.py` creates clean notebooks and the slide map. Source helpers are installed from the published revision in `coursekit-ref.txt`. Never put credentials in lesson sources, outputs, or Git.

For a fork, use `python scripts/configure_repo.py OWNER/REPO --ref main`, then enable GitHub Actions as the Pages source. The workflow verifies and publishes the static site.
