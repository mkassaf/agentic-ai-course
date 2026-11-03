# Learning resources and technical references

## More hands-on learning

- [Agentic AI Learning Lab](https://github.com/mkassaf/agentic-ai-learning-lab): a browser-based practice app with examples progressing from a single prompt to tools, reflection, and multi-agent workflows.
- [LangGraph Complete Guide](https://github.com/mkassaf/langgraph-complete-guide): Python examples for chatbots, ReAct agents, supervisor patterns, and research workflows; a follow-up to Lab 07.

Follow each repository's README for its own setup and run instructions.

## Technical references

These primary sources support the course concepts and interfaces. The notebooks keep the main examples small; use these pages for detail and further exercises.

| Topic | Reference | Use in the course |
| --- | --- | --- |
| Model API messages | [Chat Completions overview](https://developers.openai.com/api/reference/chat-completions/overview) and [request reference](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create) | Message input, response extraction, and the compatible transport |
| Initial model service | [FreeInference documentation](https://doc.freeinference.org/) | Base URL, current model access, service-specific behavior |
| RAG | [Lewis et al., Retrieval-Augmented Generation (2020)](https://arxiv.org/abs/2005.11401) | Retrieval supplies evidence before generation; the classroom retriever is deliberately small |
| Agent actions | [Yao et al., ReAct (2022)](https://arxiv.org/abs/2210.03629) | Actions and observations in a loop; the course does not expose private model reasoning |
| Workflows and patterns | [Anthropic, Building effective agents](https://www.anthropic.com/research/building-effective-agents) | Chaining, routing, parallelization, orchestration, and evaluator–optimizer patterns |
| MCP | [MCP introduction](https://modelcontextprotocol.io/docs/getting-started/intro) and [official Python SDK](https://github.com/modelcontextprotocol/python-sdk) | Tools/context interface, discovery, schemas, and calls |
| A2A | [A2A documentation](https://a2a-protocol.org/latest/) and [official Python SDK](https://github.com/a2aproject/a2a-python) | Agent Card, discovery, messages, and response handling |
| Agent Skills | [Overview](https://agentskills.io/home) and [specification](https://agentskills.io/specification) | Skill folders, SKILL.md metadata, instructions, and progressive loading |
| Frameworks | [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) | Graph state, nodes, edges, and orchestration |
| Notebook environment | [Google Colab FAQ](https://research.google.com/colaboratory/faq.html) | Runtime and notebook usage |

Protocol and framework APIs evolve. The repository pins the packages used for verification; when upgrading, regenerate and execute the notebooks against the updated dependencies. The local examples exercise a small part of each interface rather than claiming full protocol conformance or production readiness.
