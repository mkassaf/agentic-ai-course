# Microservices lecture review map

Each Colab lab has two goals: build one agentic mechanism and revisit a concrete microservices or DDD decision from the supplied lectures. Its opening review provides context and questions; its code, checks, and exercises apply those ideas.

Slide numbers include each deck's title slide and appendices. The PowerPoint files remain class materials and are not redistributed here. The examples are small adaptations; illustrative scores, workloads, and timing fixtures are not empirical results.

| Lab / agentic mechanism | Microservices / DDD revision | Lecture slides |
| --- | --- | --- |
| 00 · From rules to LLM calls | Safe retries and idempotency; Bulkheads; API gateways and BFFs | Microservices & Their Patterns: 33, 35, 39 |
| 01 · Prompting and small evaluations | API gateway; Backend for frontend (BFF); Client-specific APIs | Microservices & Their Patterns: 33, 35 |
| 02 · RAG: ground answers in retrieved knowledge | Database per service; API composition vs CQRS; Idempotent consumers and transactional outbox | Microservices & Their Patterns: 24, 27, 28, 30; Microservices Lecture 2 - Condensed DDD: 52, 55 |
| 03 · Prompt chaining with quality gates | Event storming; Bounded contexts and ubiquitous language; Business capability vs technical-layer decomposition | Microservices Lecture 2 - Condensed DDD: 9, 10, 11, 17, 18, 21, 26, 32, 60, 70, 72, 73 |
| 04 · Tool calling: an agent with three tools | Database per service; Service-owned data; Published interface | Microservices & Their Patterns: 24, 27, 28, 30; Microservices Lecture 2 - Condensed DDD: 32 |
| 05 · ReAct agents: reason, act, observe | Cascading failure; Circuit breaker vs retry; Idempotency and graceful degradation | Microservices & Their Patterns: 38, 39, 40, 41 |
| 06 · Multi-agent debate: propose, challenge, agree | API composition versus CQRS; Eventual consistency and read-model cost | Microservices & Their Patterns: 27, 28, 30 |
| 07 · Observability, tracing, and swappable agents | Correlation IDs across service boundaries; Structured logs and immutable event facts | Microservices & Their Patterns: 46, 48; Microservices Lecture 2 - Condensed DDD: 30, 31 |
| 08 · Human-in-the-loop and agent memory | Idempotent reads versus non-idempotent charges; Bounded retries and deduplicated effects | Microservices & Their Patterns: 39, 41; Microservices Lecture 2 - Condensed DDD: 52, 55 |
| 09 · Evaluation: a multi-agent system against a single model | Choose data patterns from requirements; Measure label agreement, citation validity, and trade-offs | Microservices & Their Patterns: 25, 27, 28, 29, 30 |
| 10 · Routing: rules, models, and a safe fallback | Retry safety and fallback choices; Different costs of routing errors | Microservices & Their Patterns: 38, 39, 41; Microservices Lecture 2 - Condensed DDD: 52 |
| 11 · MCP: serve tools through a standard protocol | Database per service; API composition versus CQRS; Tool schema and validation | Microservices & Their Patterns: 24, 27, 28, 30; Microservices Lecture 2 - Condensed DDD: 32 |
| 12 · Agent skills: reusable instructions on demand | Saga compensation in reverse completion order; Read-only steps need no undo; No isolation and intermediate states; Skill discovery and bounded repair | Microservices & Their Patterns: 25, 26, 30; Microservices Lecture 2 - Condensed DDD: 54 |
| 13 · A2A: delegate work to another agent | Anti-corruption layer; Published internal contract; Agent Card discovery | Microservices Lecture 2 - Condensed DDD: 26, 27, 28, 31, 66, 74 |
| 14 · Agent frameworks: graphs with LangGraph | Additive event changes; Published contract; Bounded generator–critic repair | Microservices Lecture 2 - Condensed DDD: 13, 30, 31, 32 |
| 15 · Problem framing and typed message contracts | Dependency-specific resilience; Non-idempotent payment safety; Requirements versus assumed targets | Microservices & Their Patterns: 38, 39, 41; Microservices Lecture 2 - Condensed DDD: 13, 60 |
| 16 · Learning from feedback: learning curves and trust weights | Retry eligibility and idempotency; Correlated reviewer errors; Feedback/test separation | Microservices & Their Patterns: 39, 41; Microservices Lecture 2 - Condensed DDD: 51, 52, 55 |
| 17 · Decision models: a weighted decision matrix with a scoring model | task queues versus retained event logs; independent consumer groups and replay; partition key versus eventId; consumer parallelism is capped by partitions | Microservices Lecture 2 - Condensed DDD: 44, 47, 48, 49, 50, 51, 52, 92 |
