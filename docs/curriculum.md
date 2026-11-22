# Curriculum

The course has two explicit outcomes for every lab: build an agentic mechanism and explain a related microservices/DDD decision from the supplied lectures. Every notebook provides context and two questions before the code.

## Three introductory lectures

| Lecture | Labs | Agentic mechanisms | Architecture revision |
| --- | --- | --- | --- |
| 1 · Ask, check, retrieve | 00–02 | Rule versus LLM, prompting, structured output, evaluation, RAG | Safe retries, bulkheads, gateways and BFFs; readiness and duplicate deliveries; private service data, CQRS and API composition |
| 2 · Chain, call tools, act | 03–05 | Prompt chains, validated tools, bounded ReAct | Business capabilities and bounded contexts; aggregate-root invariants; resilience and safe retries |
| 3 · Debate, trace, decide | 06–08 | Independent proposals, bounded debate, logging, swappable agents, human feedback, memory | Read-pattern trade-offs; correlation IDs; idempotent effects and scoped retry advice |

Nine self-study labs extend the same revision: evaluation (09), routing (10), MCP and owner APIs (11), skills and Saga compensation (12), A2A and anti-corruption layers (13), LangGraph and additive contracts (14), measurable checkout quality goals (15), feedback/test separation and retry judgements (16), and weighted queue/log decisions with optional typed model scoring (17).

## Keep examples small and checkable

Each lab has two to five core code steps, at most 25 lines each and 100 in total. The examples are deliberately reduced models; Python state changes stand in for services, and no Kafka, Kubernetes, or payment deployment is required. Official MCP, A2A, and LangGraph SDKs demonstrate the agentic interfaces themselves.

Lab 01's two-Boolean readiness screen is a classroom adaptation for cases whose stated goal is independent releases. `ops_ready` summarizes the four lecture prerequisites: CI/CD, monitoring, rapid provisioning, and teams owning operations. It is not a universal service-decomposition rule. The lectures also motivate independent scaling. Boundaries require business language, cohesion, consistency and change patterns, not a fixed team-size threshold.

## Learning outcomes

Students should be able to:

- Supply relevant domain evidence to an LLM, parse its output, and distinguish code checks from semantic correctness.
- Retrieve a lecture note and verify that it actually supports a claim, rather than merely accepting a source ID.
- Chain checkable steps and build a bounded action/observation loop with allowed tools and successful-read guards.
- Explain bounded contexts, aggregate roots, private data ownership, local saga transactions, and compensating actions using the executable examples.
- Contrast CQRS/composition, safe retry/no blind charge retry, additive/breaking events, and task queues/retained logs with an explicit cost.
- Coordinate independent peer proposals, keep dissent, escalate a deadlock, and retain human authority.
- Trace an agent decision, scope reused memories, separate feedback from held-out cases, and evaluate against a single-model baseline.

## Transfer to the architecture council project

The examples teach mechanisms, not a finished solution to the assignment. Students choose their own scenarios, knowledge base, stances, chair policy, evaluation rubric, and implementation. The live council still requires three model families; personas on one model do not satisfy that requirement.

Start the project by adapting one notebook with a changed scenario and a justified expected result. Build independent proposals, critiques, a stopping rule and dissent, human review, and feedback reuse. Compare actual logged council runs with each model alone on the same scenarios, then evaluate learning on cases never used for feedback. Synthetic demo timings and model-labelled fixtures are not project evidence.

## Assess both outcomes

Ask for one changed input, the observed action or answer, the relevant architecture concept, and a short explanation of the architecture trade-off. Reward a detected unsupported claim or a negative learning result. An exact output match alone does not establish sound architecture.
