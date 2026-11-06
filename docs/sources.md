# Learning resources and technical references

## More hands-on learning

- [Agentic AI Learning Lab](https://github.com/mkassaf/agentic-ai-learning-lab): a browser-based practice app with examples progressing from a single prompt to tools, reflection, and multi-agent workflows.
- [LangGraph Complete Guide](https://github.com/mkassaf/langgraph-complete-guide): Python examples for chatbots, ReAct agents, supervisor patterns, and research workflows; a follow-up to Lab 14.

Follow each repository's README for its own setup and run instructions.

## Technical references

These primary sources support the course concepts and interfaces. The notebooks keep the main examples small; use these pages for detail and further exercises. Architecture labels and thresholds are fictional teaching fixtures, not recommendations derived from these sources.

| Topic | Reference | Use in the course |
| --- | --- | --- |
| Model API messages | [Chat Completions overview](https://developers.openai.com/api/reference/chat-completions/overview) and [request reference](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create) | Message input, response extraction, and the compatible transport |
| Initial model service | [FreeInference documentation](https://doc.freeinference.org/) | Base URL, current model access, service-specific behavior |
| Prompt decomposition | [Wei et al., Chain-of-Thought Prompting (2022)](https://arxiv.org/abs/2201.11903) | Background for decomposition; the classroom adaptation uses explicit criteria and brief justifications rather than reproducing the original CoT method |
| RAG | [Lewis et al., Retrieval-Augmented Generation (2020)](https://arxiv.org/abs/2005.11401) | Retrieval supplies evidence before generation; the classroom store holds four policies |
| Embeddings and vector search | [Reimers & Gurevych, Sentence-BERT (2019)](https://arxiv.org/abs/1908.10084), the [all-MiniLM-L6-v2 model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2), and [Chroma documentation](https://docs.trychroma.com/) | Sentence embeddings, cosine similarity, and an in-memory vector database |
| Agent actions | [Yao et al., ReAct (2022)](https://arxiv.org/abs/2210.03629) | Actions and observations in a loop; the course does not expose private model reasoning |
| Pattern names and descriptions | [Architectural Patterns for Agentic AI field guide](https://karthikv1392.github.io/agentic-patterns/) by Karthik Vaidhyanathan | The names, categories, flows, trade-offs, and quality attributes on each lab's pattern card |
| Workflows and patterns | [Anthropic, Building effective agents](https://www.anthropic.com/research/building-effective-agents) | Chaining (Lab 03), tools (Lab 04), parallelization and orchestration (Lab 06), routing (Lab 10), and evaluator–optimizer loops (Labs 13–14) |
| Multi-agent debate | [Du et al., Improving Factuality and Reasoning through Multiagent Debate (2023)](https://arxiv.org/abs/2305.14325) | Several models propose, read each other's answers, and converge; the council adds sources, a chair, and dissent |
| Independent opinions | [Sharma et al., Towards Understanding Sycophancy in Language Models (2023)](https://arxiv.org/abs/2310.13548) | Why architects propose alone before they read each other |
| Feedback and memory | [Shinn et al., Reflexion (2023)](https://arxiv.org/abs/2303.11366) and [Park et al., Generative Agents (2023)](https://arxiv.org/abs/2304.03442) | Verbal feedback stored as memory and retrieved for later tasks |
| LLM-as-a-judge | [Zheng et al., Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (2023)](https://arxiv.org/abs/2306.05685) | Model judges, their biases, and agreement with human ratings |
| Quality attributes | [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html) and Bass, Clements, and Kazman, *Software Architecture in Practice* (quality-attribute scenarios) | The shared vocabulary and the scenario form of Lab 15 |
| Observability and events | [Python logging HOWTO](https://docs.python.org/3/howto/logging.html), [LangSmith](https://smith.langchain.com/), [OpenTelemetry, Observability primer](https://opentelemetry.io/docs/concepts/observability-primer/) and [Fowler, What do you mean by "Event-Driven"?](https://martinfowler.com/articles/201701-event-driven.html) | Lab 07's logs, LangSmith trace, message bus, and evidence trail |
| Weighted voting | [Littlestone and Warmuth, The weighted majority algorithm (1994)](https://doi.org/10.1006/inco.1994.1009) | Background for Lab 16's trust-weighted votes |
| MCP | [MCP introduction](https://modelcontextprotocol.io/docs/getting-started/intro) and [official Python SDK](https://github.com/modelcontextprotocol/python-sdk) | Tools/context interface, discovery, schemas, and calls |
| A2A | [A2A documentation](https://a2a-protocol.org/latest/) and [official Python SDK](https://github.com/a2aproject/a2a-python) | Agent Card, discovery, messages, and response handling |
| Agent Skills | [Overview](https://agentskills.io/home) and [specification](https://agentskills.io/specification) | Skill folders, SKILL.md metadata, instructions, and progressive loading |
| Frameworks | [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) | Graph state, nodes, edges, and orchestration |
| Notebook environment | [Google Colab FAQ](https://research.google.com/colaboratory/faq.html) | Runtime and notebook usage |

Protocol and framework APIs evolve. The repository pins the packages used for verification; when upgrading, regenerate and execute the notebooks against the updated dependencies. The local examples exercise a small part of each interface rather than claiming full protocol conformance or production readiness.
