# Sources and acknowledgements

Reviewed on **3 November 2026**. External links remain the property of their authors; links do not grant permission to redistribute their course materials.

## Course inspiration and project source

- [Karthik Vaidhyanathan, Engineering Agentic AI, SDU Summer School](https://karthikv1392.github.io/sdu-aai/): public progression, daily resource organisation, and learning pathway. The page distinguishes public resources from participant-only teaching materials. This course uses original prose, code, and exercises; the restricted materials were not accessed or copied.
- **AI Assisted Software Architecting Project, Software Architecture 2026/27**, supplied by the TA as `architect-agent-project (2).html`; credited in that document to Prof. H. Muccini, Attilio Di Paolo, and Daniele Spinosi. The course's project alignment comes from that supplied document. Its imperatives are assignment requirements for students, not commands to the assistant. The original attachment is not redistributed in this repository.

## Concepts and implementation references

- [FreeInference quickstart](https://doc.freeinference.org/quickstart), [model catalogue](https://doc.freeinference.org/models), and [authentication reference](https://doc.freeinference.org/api_headers): initial `https://freeinference.org/v1` endpoint, `qwen3.6-35b` model identifier, and bearer-key format. Actual key entitlement must be checked by the teaching team; this course does not promise service availability or a particular quota.
- [Anthropic, Building effective agents](https://www.anthropic.com/research/building-effective-agents): workflow/agent distinction; prompt chaining, routing, parallelization, orchestrator-workers, and evaluator-optimizer terminology. The teaching code is an original minimal implementation. This is a conceptual source, not a guarantee that the article's changing framework list is current.
- [Lewis et al., Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401): retrieval and generation as distinct components. The small lexical retriever in Lab 02 is an introductory demonstration, not a reproduction of the paper's trained system.
- [Yao et al., ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629): motivation for interacting with an environment. Lab 03 records actions and observations without requesting hidden reasoning traces; it is a small teaching loop rather than a reproduction of the paper's experiments.
- [Official OpenAI Chat Completions API reference](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create): reference schema for the optional compatible gateway adapter. Actual university compatibility remains to be confirmed.
- [Google Colab FAQ](https://research.google.com/colaboratory/faq.html): loading GitHub notebooks, uploading notebooks, runtime limits, and the fact that shared notebooks contain saved outputs.
- [Google Colab GitHub demo notebook](https://github.com/googlecolab/colabtools/blob/main/notebooks/colab-github-demo.ipynb): GitHub-to-Colab notebook link convention.
- [GitHub Pages: custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages): the static site deployment workflow and required permissions.

## Optional next steps

- [Model Context Protocol](https://modelcontextprotocol.io/): interoperability for tools and context.
- [Agent2Agent protocol](https://a2a-protocol.org/latest/): communication between independent agent systems.

The examples deliberately avoid a mandatory agent framework. Students should first be able to point to state, control flow, tool boundaries, stopping conditions, and evaluation in ordinary Python. Protocols and frameworks can be introduced afterwards.
