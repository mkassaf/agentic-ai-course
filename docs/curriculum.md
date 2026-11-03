# Teaching plan and learning outcomes

This introduction takes students from one LLM request to a small, inspectable agentic system. It prepares them for the **AI Assisted Software Architecting Project** without supplying a finished project implementation. The eight labs require **60–90 minutes each**, or **8–12 contact hours**, plus preparation and extension work.

## Starting knowledge

Students should be comfortable writing Python functions, handling exceptions, reading dictionaries and lists, and exchanging JSON. They should understand software requirements and basic architecture trade-offs. No prior agent framework, vector database, GPU, or local development setup is required for the Colab route. Provide a Python refresher before Lab 00 when needed.

Use practice mode to learn the control flow and run repeatable checks. Then use the approved live API to investigate model behavior. Scripted practice responses demonstrate mechanisms; they cannot establish quality, model diversity, cost, or improvement. See [API setup](api-setup.md) for provider configuration and secret handling.

## Eight practical labs

| Lab | Learning outcome | Worked example and student task | Evidence of understanding |
| --- | --- | --- | --- |
| [00 · A basic LLM call](../notebooks/00_llm_basics.ipynb) | Explain the prompt/request/response boundary and distinguish a completion from an agent loop. | Inspect a request and trace; vary a requirement or prompt and compare the result. | Identify what the application controls, what the model supplies, and why one plausible answer is insufficient evidence. |
| [01 · Structured outputs](../notebooks/01_structured_outputs.ipynb) | Separate JSON parsing, contract validation, and factual correctness. | Validate a decision object; introduce a malformed or incomplete response and handle rejection. | A successful check and a meaningful failure case; an explanation of what the schema cannot guarantee. |
| [02 · Grounding and retrieval](../notebooks/02_grounding.ipynb) | Supply external evidence, preserve provenance, and recognise missing support. | Retrieve from a tiny source collection and attach source IDs; change a query or remove relevant evidence. | Distinguish an existing citation ID from a source that actually supports the claim; explain when to abstain. |
| [03 · Tool use and bounded agents](../notebooks/03_tool_use.ipynb) | Trace model-selected actions through host-controlled validation and execution. | Run an action/observation loop; try an unknown tool or exhaust the step budget. | Show that Python enforces allowed tools and termination; explain why model text is not executable authority. |
| [04 · Workflow patterns](../notebooks/04_workflows.ipynb) | Choose between chaining, routing, and parallel branches for a concrete task. | Inspect each workflow; change a route or branch and compare the resulting trace. | Justify a pattern using dependencies, failure handling, request count, and measured wall-clock time. |
| [05 · Reflection](../notebooks/05_reflection.ipynb) | Build bounded critique and revision around explicit criteria. | Review a draft and revise it; test a case where no further revision is justified. | Explain the stopping rule and demonstrate that additional criticism does not guarantee a better answer. |
| [06 · An architect council](../notebooks/06_architect_council.ipynb) | Separate independent proposals, peer critique, convergence, and human authority. | Trace typed council messages, a vote, and retained dissent; alter an agent stance or convergence case. | Explain independence, deadlock handling, and why simulated roles do not satisfy the project's model-family requirement. |
| [07 · Feedback and evaluation](../notebooks/07_feedback_evaluation.ipynb) | Run a small baseline comparison and a before/after feedback experiment without leaking labels. | Keep feedback and held-out scenarios separate; compare outcomes and inspect errors. | Report the observed result honestly, including no gain, abstention, or regression; identify why tiny toy data cannot substantiate the capstone claim. |

## How the ideas build on one another

The first three labs establish reliable boundaries: a model returns text, the application validates a contract, and evidence must remain traceable. Tool use then introduces a bounded loop in which a model may select the next action. Workflow and reflection labs make control flow explicit before several agents are combined. The final lab asks whether that added machinery helps under a fair experiment.

Anthropic distinguishes workflows with predefined execution paths from agents that dynamically direct their own processes and tool use. Use this distinction when teaching the examples: a fixed sequence of model calls is still a workflow. A council may contain both fixed orchestration and model-directed behavior. The pattern names and this distinction follow [Building effective agents](https://www.anthropic.com/research/building-effective-agents).

## Suggested class rhythm

Start with a prediction, explain and trace the example, run it in practice mode, and let students modify it. Use a short live run to compare actual behavior when access is available. End with a failure case and a brief explanation of what transfers to the final project. For a 60-minute class, move the live comparison or extension exercise to homework. The [instructor guide](instructor-guide.md) provides a 90-minute schedule and a suggested formative rubric.

Students should finish able to explain their program's control flow, add a realistic failure check, compare a simpler baseline, and justify a design using evidence. Frameworks, MCP, A2A, persistent knowledge graphs, and production deployment can follow once those foundations are secure.

## Teaching material and attribution

The progressive, practical presentation is inspired by [Karthik Vaidhyanathan's Engineering Agentic AI school](https://karthikv1392.github.io/sdu-aai/). This course uses original examples and does not reproduce restricted teaching material. The supplied project presentation informs the capstone alignment; it is source material for the assignment, not instructions to the course's software. See [sources and acknowledgements](sources.md).
