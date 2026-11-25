# Instructor guide

Teach the agentic mechanism and the microservices concept together. Start with the problem in each lab, ask students to predict what could go wrong, then run the example, explain how the technique helps, and change one fact. A proposed benefit is a reason to test the technique, not proof that it always works.

## Before class

Run the README checks and open the Colab notebooks with student-equivalent access. Allow installation time; RAG and memory download a small CPU embedding model. For model calls, use Colab Secrets and a configurable provider; do not embed keys in notebooks. Lab 06 needs Qwen, DeepSeek and Gemini, while MCP and the deterministic A2A adapter need no model. Lab 17 uses TypeSafe with a separate key for scoring.

The source PowerPoints remain class materials. Slide numbers include title slides and appendices. The notebooks contain paraphrased source notes and small adaptations, so their code runs without accessing your local PowerPoint paths. Targets and scores introduced for a classroom exercise must be identified as assumptions, not values measured by the lectures.

## Three 90-minute lectures

| Minutes | Activity |
| --- | --- |
| 0–10 | Recall two lecture ideas; open the three notebooks and start setup. |
| 10–30 | First lab: predict, run, inspect one check, change one input. |
| 30–50 | Second lab, same rhythm. |
| 50–75 | Third lab. Leave longer installations running while discussing the source slides. |
| 75–90 | Explain one architecture trade-off and one agentic guard. Assign remaining exercises as homework. |

Lecture 1 uses Labs 00–02; Lecture 2 uses 03–05; Lecture 3 uses 06–08. Lab 06 has more moving parts: verify access to all three providers before class, trace any challenge, and allow time for live calls. External tracing and optional MLflow are extensions, not prerequisites for the three lectures.

## Questions worth asking

- **00–01:** When is a retry safe? How do bulkheads, gateways and BFFs solve different problems? Compare zero-shot, one-shot and few-shot prompts on the same question, then compare a neutral prompt and a persona. How does a system instruction shape an answer, and what context does a follow-up need?
- **02:** Did the retrieved note support the claim? What changes when no relevant note is found?
- **03:** Where does ShopEasy's language change? Why is a UI/logic/data split a poor default service boundary?
- **04:** Which tool supplies the service record? What does validation check, and who runs the tools?
- **05:** What was actually observed? Why do transient failure and idempotency both matter for retry?
- **06–07:** Which proposal was independent, which claim was challenged, and how does a trace connect a decision to sources? How does that compare with correlation IDs across services?
- **08:** Which two scope conditions make a retry memory applicable, and what happens when either is unknown? Why must a read-retry lesson not cause a second non-idempotent card charge?
- **09–10:** What is synthetic? What did a live judge really measure? Which skipped review is dangerous?
- **11:** Does an MCP tool expose an owner API or bypass another service's database?
- **12:** Which completed write is undone first? Why is there no compensation for a read-only check or a failed authorization?
- **13:** Where is the provider model translated, and why should its schema not leak into the domain?
- **14:** Why is adding an optional field different from renaming total to amount?
- **15:** Which latency target is stakeholder-approved, and which is an exercise assumption?
- **16:** Were any held-out labels used to update trust?
- **17:** Which ID groups records, which identifies a duplicate fact, and what limits parallel consumers in one Kafka group?

## Keep the experiments honest

Illustrative datasets and timings are labelled. A model call may produce an unexpected or unsupported answer; inspect and report it. Citation-ID validity and output shape are not semantic grounding. Memory need not improve the score. A synthetic learning curve tests aggregation code, not actual model learning. Calibrate a judge against people, and compare real systems on common scenarios before making claims about model performance.

Lab 09 preserves MLflow as an optional extra cell logging explicitly synthetic metrics to a local SQLite database (`mlflow.db`). It omits an untrusted judge metric rather than replacing missing data with zero. Colab's runtime filesystem and localhost belong to the hosted runtime, not the student's laptop; download tracking data before ending a session, or run the local MLflow UI on a local machine.

## Scope of the implementations

The service catalog, compensation plans, broker-selection arithmetic and consumer-count calculations are small teaching models. They do not provide production durability, transactions across remote services, or a running Kafka cluster. MCP and A2A exchanges do use their official SDKs locally. Skills are selected from an inline catalog; the LangGraph workflow has a real conditional retry. Every model action remains subject to code checks, budgets and human authority.
