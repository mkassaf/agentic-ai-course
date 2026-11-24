'use strict';
const labs = [
  {
    "id": "00",
    "file": "00_rules_and_llms",
    "title": "From rules to LLM calls",
    "subtitle": "Microservices quiz: rules versus LLM answers",
    "topics": "rules llm prompting microservices retry idempotency bulkhead api gateway bff sdk openai langchain framework deepseek harness",
    "idea": "Compare explicit rules and an LLM on the same microservices questions.",
    "objectives": [
      "Apply simple rules for retries, bulkheads, gateways, and BFFs.",
      "Make one LLM call, then compare SDK, LangChain, and optional DeepSeek Harness examples.",
      "Explain why agreement is useful to inspect but does not prove a design is correct."
    ],
    "example": "ShopEasy faces a slow dependency; ask the same question with a helper, SDK, LangChain, or an optional agent harness.",
    "exercise": "Change a failure from transient to permanent, and explain when a retry is safe.",
    "checks": "Compare the answer letters and examine any disagreement.",
    "bridge": "A timed-out payment might already have succeeded; server-supported idempotency makes a retry safer.",
    "track": "lecture-1",
    "steps": 4,
    "warmups": 1,
    "optional_examples": 3,
    "patterns": [],
    "background": [
      "A Python rule checks explicit facts; an LLM reads a natural-language question and returns a response. Both answers need to be reviewed in context.",
      "Retries need a transient failure, a safe operation, a limit, and backoff. Bulkheads isolate resources; gateways and BFFs serve different edge needs."
    ],
    "terms": [
      [
        "Idempotency",
        "Repeating an operation has the same intended effect as performing it once."
      ],
      [
        "Bulkhead",
        "A resource boundary that keeps one dependency from exhausting another’s capacity."
      ],
      [
        "API gateway",
        "An entry point that can route external requests and apply shared policies."
      ],
      [
        "Backend for frontend (BFF)",
        "A backend that adapts an API to a particular client’s needs."
      ],
      [
        "LLM prompt",
        "The instructions, facts, and question sent to a language model."
      ]
    ],
    "review": {
      "sources": [
        {
          "deck": "microservices",
          "slides": [
            33,
            35,
            39
          ]
        }
      ],
      "concepts": [
        "Safe retries and idempotency",
        "Bulkheads",
        "API gateways and BFFs"
      ],
      "questions": [
        "When is a retry safe, and why is a timed-out payment uncertain?",
        "How do bulkheads, API gateways, and BFFs address different problems?"
      ],
      "readings": [
        "Microservices & Their Patterns · slides 33, 35, 39"
      ]
    }
  },
  {
    "id": "01",
    "file": "01_prompting_evaluation",
    "title": "Prompting and small evaluations",
    "subtitle": "System and user prompts, sampling, memory, validation, and reasoning",
    "topics": "system user messages prompting memory validation json reasoning thinking chain of thought strawberry decimal architecture gateway bff generation settings sampling temperature top k top p max tokens",
    "idea": "Separate reusable system instructions from changing user questions, then check model answers.",
    "objectives": [
      "Distinguish system instructions from the user question and experiment with sampling settings.",
      "Pass a previous response into a follow-up and validate JSON.",
      "Compare an older model with guided prompts and DeepSeek thinking modes."
    ],
    "example": "Ask about API gateways and mobile BFFs, then test two small reasoning questions.",
    "exercise": "Change temperature or top-k, omit previous context, and inspect a wrong JSON decision.",
    "checks": "Check the reply format and decision; verify reasoning answers with Python.",
    "bridge": "Thinking mode can help but is not guaranteed to be correct; compare actual results.",
    "track": "lecture-1",
    "steps": 5,
    "warmups": 1,
    "patterns": [],
    "background": [
      "A system message guides the assistant; a user message requests a task. A follow-up can include a previous answer as temporary context.",
      "Parse and validate replies before using them. An older model and DeepSeek thinking modes can be compared on small, checkable examples."
    ],
    "terms": [
      [
        "System prompt",
        "Instructions that guide the assistant’s task and response."
      ],
      [
        "User prompt",
        "The specific question or request sent by the user."
      ],
      [
        "Temporary context",
        "Information, such as a previous answer, sent again in a later request."
      ],
      [
        "Validation",
        "Checking that a response has the expected format and meets a specific condition."
      ],
      [
        "Thinking mode",
        "A model setting that enables additional internal reasoning before the final answer."
      ]
    ],
    "review": {
      "sources": [
        {
          "deck": "microservices",
          "slides": [
            33,
            35
          ]
        }
      ],
      "concepts": [
        "API gateway",
        "Backend for frontend (BFF)",
        "Client-specific APIs"
      ],
      "questions": [
        "What shared needs can an API gateway address?",
        "Why might mobile and web clients benefit from different BFFs?"
      ],
      "readings": [
        "Microservices & Their Patterns · slides 33, 35"
      ]
    },
    "optional_examples": 3,
    "picture": {
      "src": "assets/images/sampling-settings.svg",
      "alt": "A worked sampling example: temperature changes four probabilities, top-k removes D, top-p removes C, then A and B are sampled at 62.25% and 37.75%.",
      "caption": "One illustrative next-token decision. The example uses temperature 2, top-k 3, and top-p 0.80."
    },
    "tool": {
      "src": "assets/tools/sampling.html",
      "label": "Open the interactive sampling simulator"
    }
  },
  {
    "id": "02",
    "file": "02_rag_systems",
    "title": "RAG: ground answers in retrieved knowledge",
    "subtitle": "From all policies to retrieved evidence",
    "topics": "rag retrieval embeddings vectors vector database chroma similarity rules source architecture context retrieval-augmented generation microservices DDD ShopEasy lecture revision Database per service API composition vs CQRS Idempotent consumers and transactional outbox",
    "idea": "Compare sending every microservices policy with retrieving only relevant policies.",
    "objectives": [
      "Organize policies into categories and compare full-context prompts with RAG.",
      "Inspect embeddings and ranked policies for several questions, including an unrelated one.",
      "Compare prompts, input-token usage, and citation validity; inspect factual support."
    ],
    "example": "Compare full-library and retrieved-policy answers about private service data and searchable order history.",
    "exercise": "Try more questions, change the number of retrieved policies, and inspect irrelevant matches.",
    "checks": "Inspect prompt sizes, reported input tokens, retrieved IDs and distances, and citation support.",
    "bridge": "Citing a valid source ID does not by itself prove factual support.",
    "track": "lecture-1",
    "pattern": "Retrieval-Augmented Generation",
    "steps": 5,
    "warmups": 1,
    "patterns": [
      "Retrieval-Augmented Generation"
    ],
    "background": [
      "Sending every policy increases prompt size as a library grows. RAG retrieves selected evidence; embeddings and nearest-neighbour scores do not guarantee relevance.",
      "Citing a valid source ID does not by itself prove factual support."
    ],
    "terms": [
      [
        "Context window",
        "The maximum amount of text a model can read in one call."
      ],
      [
        "Embedding",
        "A vector of numbers that represents the meaning of a text."
      ],
      [
        "Vector database",
        "A store that finds the vectors nearest to a query vector."
      ],
      [
        "Grounded answer",
        "An answer supported by, and citing, the retrieved sources."
      ]
    ],
    "review": {
      "sources": [
        {
          "deck": "microservices",
          "slides": [
            24,
            27,
            28,
            30
          ]
        },
        {
          "deck": "ddd",
          "slides": [
            52,
            55
          ]
        }
      ],
      "concepts": [
        "Database per service",
        "API composition vs CQRS",
        "Idempotent consumers and transactional outbox"
      ],
      "questions": [
        "Why is CQRS a better fit for searchable order history than a large in-memory API join?",
        "Does citing a valid source ID prove that the source supports an answer?"
      ],
      "readings": [
        "Microservices & Their Patterns · slides 24, 27, 28, 30",
        "Microservices Lecture 2 - Condensed DDD · slides 52, 55"
      ]
    }
  },
  {
    "id": "03",
    "file": "03_prompt_chaining",
    "title": "Prompt chaining with quality gates",
    "subtitle": "From a lunch idea to ShopEasy boundaries",
    "topics": "prompt chaining workflow gate requirements options trade-offs adr patterns council single-path planning microservices DDD ShopEasy lecture revision Event storming Bounded contexts and ubiquitous language Business capability vs technical-layer decomposition",
    "idea": "Pass one answer into the next prompt, first for a lunch idea and then for a boundary decision.",
    "objectives": [
      "Build a two-call prompt chain, then apply the same handoff to a boundary decision.",
      "Turn events and business responsibilities into candidate bounded contexts and a short ADR.",
      "Place Returns and Refunds; explain the language and invariants behind your boundary.",
      "Check each intermediate structure and manually inspect cohesion, coupling, and ownership."
    ],
    "example": "Suggest a lunch and list its ingredients; then group ShopEasy behaviour by business capability.",
    "exercise": "Place Returns and Refunds; explain the language and invariants behind your boundary.",
    "checks": "Check each intermediate structure and manually inspect cohesion, coupling, and ownership.",
    "bridge": "A bounded context is a model boundary; validate it before choosing deployment boundaries.",
    "track": "lecture-2",
    "pattern": "Single-Path Planning",
    "steps": 5,
    "patterns": [
      "Single-Path Planning"
    ],
    "background": [
      "A fixed prompt chain exposes intermediate results. Gates can catch a malformed handoff while leaving domain judgement for review.",
      "A bounded context is a model boundary; validate it before choosing deployment boundaries."
    ],
    "terms": [
      [
        "Workflow",
        "A sequence of steps fixed by code; the model does not choose what happens next."
      ],
      [
        "Decomposition",
        "Splitting a large task into smaller steps with clear inputs and outputs."
      ],
      [
        "Gate",
        "A plain-code check between two steps that stops a bad result from spreading."
      ],
      [
        "Decision record (ADR)",
        "A short note of an architecture decision: its context, the decision, and its consequence."
      ]
    ],
    "review": {
      "sources": [
        {
          "deck": "ddd",
          "slides": [
            9,
            10,
            11,
            17,
            18,
            21,
            26,
            32,
            60,
            70,
            72,
            73
          ]
        }
      ],
      "concepts": [
        "Event storming",
        "Bounded contexts and ubiquitous language",
        "Business capability vs technical-layer decomposition"
      ],
      "questions": [
        "Why can a technical-layer split create a distributed monolith?",
        "Why is a bounded context a service candidate rather than an automatic deployment decision?"
      ],
      "readings": [
        "Microservices Lecture 2 - Condensed DDD · slides 9, 10, 11, 17, 18, 21, 26, 32, 60, 70, 72, 73"
      ]
    }
  },
  {
    "id": "04",
    "file": "04_why_tools",
    "track": "lecture-2",
    "pattern": "One-Step Tool Agent",
    "title": "Tool calling: read and change an Order",
    "subtitle": "Tool calling through an Order aggregate",
    "topics": "tools tool calling function calling Order aggregate invariant read write confirmation live data one-step tool agent microservices DDD ShopEasy lecture revision Aggregate root Entity vs value object Consistency boundary and invariant",
    "idea": "Give the model checked tools to read and change an Order instead of guessing its state.",
    "objectives": [
      "Read current Order state and make a validated change through its public root.",
      "Try an invalid quantity and compare state before and after the rejected call.",
      "Validate tool names and arguments, require confirmation for writes, and check the invariant."
    ],
    "example": "A model requests an item change to an in-memory Order; the root checks the input and maintains the total.",
    "exercise": "Try an invalid quantity and compare state before and after the rejected call.",
    "checks": "Validate tool names and arguments, test the simulated confirmation flag, and check the invariant.",
    "bridge": "Tools perform actions; the model cannot bypass the aggregate root to edit totals.",
    "steps": 5,
    "warmups": 1,
    "patterns": [
      "One-Step Tool Agent"
    ],
    "background": [
      "Tool calling connects model-selected requests to ordinary code. The host validates requests and retains authority over state changes.",
      "Tools perform actions; the model cannot bypass the aggregate root to edit totals."
    ],
    "terms": [
      [
        "Tool",
        "A function that the model may ask the program to run."
      ],
      [
        "Function calling",
        "A reply format in which the model names a tool and gives its arguments as JSON."
      ],
      [
        "Read and write tools",
        "A read tool only looks data up; a write tool changes data and needs more care."
      ],
      [
        "Confirmation",
        "A person's approval before a tool changes anything."
      ]
    ],
    "review": {
      "sources": [
        {
          "deck": "ddd",
          "slides": [
            29,
            67,
            68,
            75,
            76,
            83
          ]
        }
      ],
      "concepts": [
        "Aggregate root",
        "Entity vs value object",
        "Consistency boundary and invariant"
      ],
      "questions": [
        "Why must outside code change an Order through the aggregate root rather than set its total?",
        "What distinguishes the identity of Order from the value of Money, and which details does this tiny model omit?"
      ],
      "readings": [
        "Microservices Lecture 2 - Condensed DDD · slides 29, 67, 68, 75, 76, 83"
      ]
    }
  },
  {
    "id": "05",
    "file": "05_react_agent",
    "title": "ReAct agents: reason, act, observe",
    "subtitle": "ReAct for checkout resilience",
    "topics": "agent foundations patterns react action observation loop chaining routing one-step tool agent in a react loop microservices DDD ShopEasy lecture revision Cascading failure Circuit breaker vs retry Idempotency and graceful degradation",
    "idea": "Observe a dependency before selecting a resilience policy.",
    "objectives": [
      "Inspect a service before choosing a resilience response, using a bounded action loop.",
      "Try finishing before a successful read, or inspect a non-idempotent payment call.",
      "Inspect action, observation, accumulated history, and the stopping guard."
    ],
    "example": "Read simulated Inventory latency and idempotency facts before recommending a circuit breaker or a safe retry.",
    "exercise": "Try finishing before a successful read, or inspect a non-idempotent payment call.",
    "checks": "Inspect action, observation, accumulated history, and the stopping guard.",
    "bridge": "An agent loop selects its next step from observations; it still needs a bound and allowed tools.",
    "track": "lecture-2",
    "pattern": "One-Step Tool Agent in a ReAct loop",
    "steps": 4,
    "warmups": 1,
    "patterns": [
      "One-Step Tool Agent"
    ],
    "background": [
      "ReAct-style control flow alternates model actions with tool observations. The example exposes those exchanges without deploying a checkout system.",
      "An agent loop selects its next step from observations; it still needs a bound and allowed tools."
    ],
    "terms": [
      [
        "Agent",
        "A system in which a model chooses its next action in a loop, based on what it has observed."
      ],
      [
        "Observation",
        "The result of an action, fed back into the next prompt."
      ],
      [
        "History",
        "Every action and observation so far; the agent's view of the task."
      ],
      [
        "Guard",
        "A rule in code that the agent cannot override, such as a turn limit."
      ]
    ],
    "review": {
      "sources": [
        {
          "deck": "microservices",
          "slides": [
            38,
            39,
            40,
            41
          ]
        }
      ],
      "concepts": [
        "Cascading failure",
        "Circuit breaker vs retry",
        "Idempotency and graceful degradation"
      ],
      "questions": [
        "Why can retries make a slow dependency worse?",
        "Why must the non-idempotent Payments charge not be blindly retried?"
      ],
      "readings": [
        "Microservices & Their Patterns · slides 38, 39, 40, 41"
      ]
    }
  },
  {
    "id": "06",
    "file": "06_multi_agent_debate",
    "title": "Multi-agent debate: propose, challenge, agree",
    "subtitle": "Multi-agent debate over CQRS and API composition",
    "topics": "multi-agent council debate independent proposals critique revision consensus voting dissent chair coordinator grounding model families patterns debate-based cooperation microservices DDD ShopEasy lecture revision API composition versus CQRS Eventual consistency and read-model cost",
    "idea": "Compare independent proposals and preserve disagreement on a design choice.",
    "objectives": [
      "Give peers the same source notes and ask them to defend a read-pattern choice.",
      "Remove a citation or change the query workload and inspect challenges and dissent.",
      "Check independent proposals, bounded revision, valid citations, a quorum, and escalation."
    ],
    "example": "Three architect roles on three providers compare ShopEasy support search with small order-by-ID lookups.",
    "exercise": "Remove a citation or change the query workload and inspect challenges and dissent.",
    "checks": "Check independent proposals, bounded revision, valid citations, a quorum, and escalation.",
    "bridge": "CQRS supports search but adds a read model and consistency lag; composition has different costs.",
    "track": "lecture-3",
    "pattern": "Debate-Based Cooperation",
    "steps": 5,
    "warmups": 1,
    "patterns": [
      "Debate-Based Cooperation",
      "Voting-Based Cooperation"
    ],
    "background": [
      "Independent proposals do not see one another. A coded chair limits discussion and aggregates proposals; agreement is not proof of correctness.",
      "CQRS supports search but adds a read model and consistency lag; composition has different costs."
    ],
    "terms": [
      [
        "Multi-agent system",
        "Several model-driven agents with separate roles that work on one task."
      ],
      [
        "Independence",
        "Each agent answers without seeing the others first, so its view is its own."
      ],
      [
        "Grounding",
        "Supporting a claim with a source that everyone can check."
      ],
      [
        "Escalation",
        "Handing the decision to a person when the agents cannot agree."
      ]
    ],
    "review": {
      "sources": [
        {
          "deck": "microservices",
          "slides": [
            27,
            28,
            30
          ]
        }
      ],
      "concepts": [
        "API composition versus CQRS",
        "Eventual consistency and read-model cost"
      ],
      "questions": [
        "Why is a customer-name search different from a lookup by order ID?",
        "Which cost of CQRS must the council record?"
      ],
      "readings": [
        "Microservices & Their Patterns · slides 27, 28, 30"
      ]
    }
  },
  {
    "id": "07",
    "file": "07_observe_trace_swap",
    "title": "Observability, tracing, and swappable agents",
    "subtitle": "Observable decisions and microservice correlation IDs",
    "topics": "observability logging logs log file json lines traceability swappable registry structured messages provenance langsmith tracing trace spans microservices DDD ShopEasy lecture revision Correlation IDs across service boundaries Structured logs and immutable event facts",
    "idea": "Keep structured logs so you can trace a decision and swap an agent.",
    "objectives": [
      "Log structured agent messages with correlation IDs and trace a decision to its inputs.",
      "Add an agent through the registry and follow its cited messages in the log.",
      "Inspect the live log, persisted records, and the decision evidence trail."
    ],
    "example": "Trace ShopEasy pattern recommendations back to the claims and evidence behind them.",
    "exercise": "Add an agent through the registry and follow its cited messages in the log.",
    "checks": "Inspect the live log, persisted records, and the decision evidence trail.",
    "bridge": "Agent-run traces and microservice request traces share correlation principles but are different systems.",
    "track": "lecture-3",
    "steps": 5,
    "warmups": 1,
    "patterns": [
      "Shared Memory",
      "Registry & Adapter"
    ],
    "background": [
      "Observability makes a workflow inspectable during and after a run. Each proposal is logged, and a registry lists reviewer settings.",
      "Agent-run traces and microservice request traces share correlation principles but are different systems."
    ],
    "terms": [
      [
        "Observability",
        "Seeing what a running system does from its outputs: logs, metrics, and traces."
      ],
      [
        "Trace",
        "A record of one run as a tree of steps, with each step's input, output, and timing; LangSmith shows traces of LLM applications."
      ],
      [
        "Log",
        "A time-stamped record of what happened; structured logs, such as JSON lines, can be searched and counted."
      ],
      [
        "Registry",
        "A lookup table of agents by name, so the system never hard-codes who takes part."
      ]
    ],
    "review": {
      "sources": [
        {
          "deck": "microservices",
          "slides": [
            46,
            48
          ]
        },
        {
          "deck": "ddd",
          "slides": [
            30,
            31
          ]
        }
      ],
      "concepts": [
        "Correlation IDs across service boundaries",
        "Structured logs and immutable event facts"
      ],
      "questions": [
        "What is the difference between a trace ID and a message ID?",
        "Why does an event or agent message need both identity and provenance?"
      ],
      "readings": [
        "Microservices & Their Patterns · slides 46, 48",
        "Microservices Lecture 2 - Condensed DDD · slides 30, 31"
      ]
    }
  },
  {
    "id": "08",
    "file": "08_human_feedback_memory",
    "title": "Human-in-the-loop and agent memory",
    "subtitle": "Human feedback and scoped memory for safe retries",
    "topics": "human in the loop feedback memory vector database chroma lessons evaluation held-out learning patterns council human in the loop and archival memory short-term memory long-term memory scratchpad microservices DDD ShopEasy lecture revision Idempotent reads versus non-idempotent charges Bounded retries and deduplicated effects",
    "idea": "Reuse human feedback only when it applies to the current operation.",
    "objectives": [
      "Store the reason for human feedback and retrieve it only for cases within its approved scope.",
      "Change idempotency or whether a failure is transient, and compare candidate memories with applicable ones.",
      "Report before/after held-out scores even when memory does not improve them."
    ],
    "example": "Simulated human feedback approves retry advice for an idempotent read; the lesson must not be reused blindly for a payment charge.",
    "exercise": "Change idempotency or whether a failure is transient, and compare candidate memories with applicable ones.",
    "checks": "Report before/after held-out scores even when memory does not improve them.",
    "bridge": "Similarity is not applicability. Check known scope conditions before inserting a lesson into a prompt.",
    "track": "lecture-3",
    "pattern": "Human in the Loop and Archival Memory",
    "steps": 5,
    "warmups": 1,
    "patterns": [
      "Human in the Loop",
      "Scratchpad Memory",
      "Archival Memory"
    ],
    "background": [
      "Human review can correct a proposal and supply a scoped lesson. This lab uses a scripted reviewer, and retrieval checks both relevance and applicability.",
      "Similarity is not applicability. Check known scope conditions before inserting a lesson into a prompt."
    ],
    "terms": [
      [
        "Human in the loop",
        "A design in which a person approves or corrects the system's decisions."
      ],
      [
        "Short-term memory",
        "Working notes for the current task, passed in the prompt."
      ],
      [
        "Long-term memory",
        "Lessons stored across tasks and recalled when a similar case appears."
      ],
      [
        "Held-out case",
        "A case not used for feedback, reserved to test whether the approach generalizes."
      ]
    ],
    "review": {
      "sources": [
        {
          "deck": "microservices",
          "slides": [
            39,
            41
          ]
        },
        {
          "deck": "ddd",
          "slides": [
            52,
            55
          ]
        }
      ],
      "concepts": [
        "Idempotent reads versus non-idempotent charges",
        "Bounded retries and deduplicated effects"
      ],
      "questions": [
        "Why must a timeout not automatically trigger another payment charge?",
        "Why does semantic similarity alone not establish that a stored lesson applies?"
      ],
      "readings": [
        "Microservices & Their Patterns · slides 39, 41",
        "Microservices Lecture 2 - Condensed DDD · slides 52, 55"
      ]
    }
  },
  {
    "id": "09",
    "file": "09_multi_agent_evaluation",
    "title": "Evaluation: a multi-agent system against a single model",
    "subtitle": "Evaluate pattern advice against single models",
    "topics": "evaluation baseline experiment llm judge calibration human ratings grounding cost latency council patterns microservices DDD ShopEasy lecture revision Choose data patterns from requirements Measure label agreement, citation validity, and trade-offs",
    "idea": "Compare council and single-model answers on the same cases.",
    "objectives": [
      "Compare systems on the same architecture cases and calibrate a narrow LLM judge.",
      "Change one answer and inspect correctness, valid citations, costs, and human/judge disagreement.",
      "The synthetic dataset demonstrates the measurement code; the model only judges the example answers."
    ],
    "example": "Score synthetic recommendations for customer support search and order-details lookups.",
    "exercise": "Change one answer and inspect correctness, valid citations, costs, and human/judge disagreement.",
    "checks": "The synthetic dataset demonstrates the measurement code; the model only judges the example answers.",
    "bridge": "Use actual run logs and repeated scenarios for the project experiment.",
    "track": "self-study",
    "steps": 5,
    "warmups": 1,
    "patterns": [],
    "background": [
      "Evaluation needs consistent inputs, labelled criteria, and honest provenance. Synthetic answers and timings teach the method without claiming measured model performance.",
      "Use actual run logs and repeated scenarios for the project experiment."
    ],
    "terms": [
      [
        "Baseline",
        "The system to beat; here, the best single model."
      ],
      [
        "Metric",
        "A number that measures one quality, such as correct answers or model calls."
      ],
      [
        "LLM judge",
        "A model that rates other models' answers against a rubric."
      ],
      [
        "Calibration",
        "Checking the judge against human ratings before trusting it."
      ]
    ],
    "review": {
      "sources": [
        {
          "deck": "microservices",
          "slides": [
            25,
            27,
            28,
            29,
            30
          ]
        }
      ],
      "concepts": [
        "Choose data patterns from requirements",
        "Measure label agreement, citation validity, and trade-offs"
      ],
      "questions": [
        "For a small order-details lookup by ID, why might a separate CQRS read model add unnecessary work?",
        "Which data pattern supports replaying a historical account balance?"
      ],
      "readings": [
        "Microservices & Their Patterns · slides 25, 27, 28, 29, 30"
      ]
    }
  },
  {
    "id": "10",
    "file": "10_routing",
    "title": "Routing: rules, models, and a safe fallback",
    "subtitle": "Route clear cases and escalate ambiguous ones",
    "topics": "routing router classifier dispatch handlers fallback cost few shot council patterns microservices DDD ShopEasy lecture revision Retry safety and fallback choices Different costs of routing errors",
    "idea": "Route clear cases to rules and uncertain cases to review.",
    "objectives": [
      "Dispatch simple pattern checks to rules and send contested architecture cases for review.",
      "Alter criticality or idempotency and compare skipped reviews with unnecessary ones.",
      "Compare routes with labelled examples and count routing overhead."
    ],
    "example": "Known safe retry conditions differ from uncertain checkout behaviour that needs a council or human.",
    "exercise": "Alter criticality or idempotency and compare skipped reviews with unnecessary ones.",
    "checks": "Compare routes with labelled examples and count routing overhead.",
    "bridge": "A router spends calls too; an uncertain reply should not silently skip review.",
    "track": "self-study",
    "pattern": "Routing",
    "steps": 4,
    "warmups": 1,
    "patterns": [
      "Routing"
    ],
    "background": [
      "Routing chooses which workflow handles a case. A dispatch table and conservative fallback keep selection separate from execution.",
      "A router spends calls too; an uncertain reply should not silently skip review."
    ],
    "terms": [
      [
        "Router",
        "A component that picks the handler for each input."
      ],
      [
        "Dispatch table",
        "A mapping from each route to the function that handles it."
      ],
      [
        "Fallback",
        "The safe route taken when the router's answer cannot be used."
      ],
      [
        "Asymmetric errors",
        "Mistakes whose costs differ, so they are counted and weighed separately."
      ]
    ],
    "review": {
      "sources": [
        {
          "deck": "microservices",
          "slides": [
            38,
            39,
            41
          ]
        },
        {
          "deck": "ddd",
          "slides": [
            52
          ]
        }
      ],
      "concepts": [
        "Retry safety and fallback choices",
        "Different costs of routing errors"
      ],
      "questions": [
        "Why is the Payments case more dangerous than a failed Pricing read?",
        "Why can routing cost as much as sending every case to review?"
      ],
      "readings": [
        "Microservices & Their Patterns · slides 38, 39, 41",
        "Microservices Lecture 2 - Condensed DDD · slides 52"
      ]
    }
  },
  {
    "id": "11",
    "file": "11_tools_mcp",
    "title": "MCP: serve tools through a standard protocol",
    "subtitle": "MCP tools respect service data ownership",
    "topics": "tools mcp server client extract action agent foundations registry & adapter microservices DDD ShopEasy lecture revision Database per service API composition versus CQRS Tool schema and validation",
    "idea": "Let agents discover approved Orders tools through MCP.",
    "objectives": [
      "Discover and call an Order-owned API through a real local MCP server.",
      "Send bad arguments and verify that a rejected write leaves state unchanged.",
      "Inspect tool descriptions, schemas, real SDK results, and error flags."
    ],
    "example": "Read exposed Order facts and save a validated read-pattern decision without reaching into another database.",
    "exercise": "Send bad arguments and verify that a rejected write leaves state unchanged.",
    "checks": "Inspect tool descriptions, schemas, real SDK results, and error flags.",
    "bridge": "Database per service means private ownership; public APIs and events expose selected facts.",
    "track": "self-study",
    "pattern": "Registry & Adapter",
    "steps": 5,
    "warmups": 1,
    "patterns": [
      "Registry & Adapter"
    ],
    "background": [
      "MCP standardizes tool discovery and calls. The lab runs its server locally in process; it does not deploy business microservices.",
      "Database per service means private ownership; public APIs and events expose selected facts."
    ],
    "terms": [
      [
        "MCP server",
        "A program that publishes tools, and other context, through the protocol."
      ],
      [
        "MCP client",
        "A program that discovers and calls a server's tools."
      ],
      [
        "Input schema",
        "A machine-readable description of a tool's arguments and their types."
      ],
      [
        "Discovery",
        "Asking a server what it offers, instead of hard-coding it."
      ]
    ],
    "review": {
      "sources": [
        {
          "deck": "microservices",
          "slides": [
            24,
            27,
            28,
            30
          ]
        },
        {
          "deck": "ddd",
          "slides": [
            32
          ]
        }
      ],
      "concepts": [
        "Database per service",
        "API composition versus CQRS",
        "Tool schema and validation"
      ],
      "questions": [
        "Why should reporting not read Orders tables directly?",
        "What requirement makes CQRS preferable to API composition?"
      ],
      "readings": [
        "Microservices & Their Patterns · slides 24, 27, 28, 30",
        "Microservices Lecture 2 - Condensed DDD · slides 32"
      ]
    }
  },
  {
    "id": "12",
    "file": "12_agent_skills",
    "title": "Agent skills: reusable instructions on demand",
    "subtitle": "Agent skills review Saga compensation",
    "topics": "skills skill.md adr architecture decision record reusable skill library evolution microservices DDD ShopEasy lecture revision Saga compensation in reverse completion order Read-only steps need no undo No isolation and intermediate states Skill discovery and bounded repair",
    "idea": "Load only the skill instructions relevant to a task.",
    "objectives": [
      "Choose a skill by its description.",
      "Validate compensation order, not just prose format.",
      "Inspect intermediate states and local transaction boundaries."
    ],
    "example": "For failed payment, release stock then reject the order; skip the read-only customer verification. Successful payment needs no compensation.",
    "exercise": "Reverse the compensation order or propose refunding a failed authorization and inspect the checker.",
    "checks": "The selected skill produces three-line ADRs with correctly ordered compensations or none, with at most one repair.",
    "bridge": "Each saga step is a local transaction. Compensation is a business action, not automatic isolation.",
    "track": "self-study",
    "pattern": "Skill Library Evolution",
    "steps": 5,
    "warmups": 1,
    "patterns": [
      "Skill Library Evolution"
    ],
    "background": [
      "Progressive disclosure shows skill descriptions first and loads instructions only when a task needs them. Host code validates the resulting proposal and bounds repairs.",
      "A saga coordinates local transactions. In this reduced ShopEasy case, failed payment releases reserved stock before rejecting the earlier order; the read-only customer check needs no undo. The code proposes a plan, without executing real transactions."
    ],
    "terms": [
      [
        "Skill",
        "A named reusable procedure selected by its description."
      ],
      [
        "Progressive disclosure",
        "Load full instructions only after selecting a skill."
      ],
      [
        "Saga compensation",
        "A business action that counteracts a completed local step."
      ]
    ],
    "review": {
      "sources": [
        {
          "deck": "microservices",
          "slides": [
            25,
            26,
            30
          ]
        },
        {
          "deck": "ddd",
          "slides": [
            54
          ]
        }
      ],
      "concepts": [
        "Saga compensation in reverse completion order",
        "Read-only steps need no undo",
        "No isolation and intermediate states",
        "Skill discovery and bounded repair"
      ],
      "questions": [
        "Why is a failed card authorization not a completed charge to refund?",
        "Which intermediate states can other services see before a saga finishes?"
      ],
      "readings": [
        "Microservices & Their Patterns · slides 25, 26, 30",
        "Microservices Lecture 2 - Condensed DDD · slides 54"
      ]
    }
  },
  {
    "id": "13",
    "file": "13_a2a_protocol",
    "title": "A2A: delegate work to another agent",
    "subtitle": "A2A and an anti-corruption layer",
    "topics": "a2a agent card discovery message review architecture generator–critic loop agent card payment adapter microservices DDD ShopEasy lecture revision Anti-corruption layer Published internal contract Agent Card discovery",
    "idea": "Discover a translation agent and protect the internal Payment model.",
    "objectives": [
      "Send a message to a discoverable local agent that translates a provider model at the boundary.",
      "Change a provider field or currency and inspect validation at the translation boundary.",
      "Inspect the Agent Card, real protocol exchange, internal output, and invalid-payload handling."
    ],
    "example": "Adapt a synthetic Stripe-style payment payload into the internal Payment and Money representation.",
    "exercise": "Change a provider field or currency and inspect validation at the translation boundary.",
    "checks": "Inspect the Agent Card, real protocol exchange, internal output, and invalid-payload handling.",
    "bridge": "A2A is an agent protocol; an anti-corruption layer protects the domain model. One does not imply the other.",
    "track": "self-study",
    "pattern": "Registry & Adapter",
    "steps": 3,
    "warmups": 1,
    "patterns": [
      "Registry & Adapter"
    ],
    "background": [
      "Delegation exchanges a task through an agent interface. This deterministic local agent demonstrates translation without a live payment service or model key.",
      "A2A is an agent protocol; an anti-corruption layer protects the domain model. One does not imply the other."
    ],
    "terms": [
      [
        "Anti-corruption layer",
        "Translation boundary that protects an internal domain model from a foreign one."
      ],
      [
        "Agent Card",
        "Discoverable description of an agent and its capabilities."
      ],
      [
        "Money value",
        "Amount and currency represented together in the internal model."
      ]
    ],
    "review": {
      "sources": [
        {
          "deck": "ddd",
          "slides": [
            26,
            27,
            28,
            31,
            66,
            74
          ]
        }
      ],
      "concepts": [
        "Anti-corruption layer",
        "Published internal contract",
        "Agent Card discovery"
      ],
      "questions": [
        "Why should Order not depend on the payment provider's field names?",
        "Which part is the A2A protocol, and which part is domain translation?"
      ],
      "readings": [
        "Microservices Lecture 2 - Condensed DDD · slides 26, 27, 28, 31, 66, 74"
      ]
    }
  },
  {
    "id": "14",
    "file": "14_frameworks_langgraph",
    "title": "Agent frameworks: graphs with LangGraph",
    "subtitle": "LangGraph checks event-contract compatibility",
    "topics": "framework langgraph state nodes edges evaluate architecture generator–critic loop microservices DDD ShopEasy lecture revision Additive event changes Published contract Bounded generator–critic repair",
    "idea": "Use a graph to make generation, checks, and bounded repair visible.",
    "objectives": [
      "Use nodes, state, and a bounded retry to validate an OrderPlaced contract.",
      "Remove a required old field and watch the compatibility feedback trigger a retry.",
      "Preserve existing field names and types and stop after the retry budget."
    ],
    "example": "Compare adding an optional field with renaming the total field that Payment still reads.",
    "exercise": "Remove a required old field and watch the compatibility feedback trigger a retry.",
    "checks": "Preserve existing field names and types and stop after the retry budget.",
    "bridge": "An additive event change protects consumers; a framework does not make a proposal compatible automatically.",
    "track": "self-study",
    "pattern": "Generator–Critic Loop",
    "steps": 4,
    "warmups": 1,
    "patterns": [
      "Generator–Critic Loop"
    ],
    "background": [
      "A graph names workflow steps and edges. A simple Python loop retries failed proposals using the check feedback.",
      "An additive event change protects consumers; a framework does not make a proposal compatible automatically."
    ],
    "terms": [
      [
        "State",
        "The data that all steps of a workflow read and write."
      ],
      [
        "Node",
        "One step of the graph, written as a function of the state."
      ],
      [
        "Edge",
        "A connection that sets which node runs next."
      ],
      [
        "Retry loop",
        "Python repeats the graph when its check fails, up to a fixed limit."
      ]
    ],
    "review": {
      "sources": [
        {
          "deck": "ddd",
          "slides": [
            13,
            30,
            31,
            32
          ]
        }
      ],
      "concepts": [
        "Additive event changes",
        "Published contract",
        "Bounded generator–critic repair"
      ],
      "questions": [
        "Why does renaming total break a consumer?",
        "Why should a new event field be optional for existing consumers?"
      ],
      "readings": [
        "Microservices Lecture 2 - Condensed DDD · slides 13, 30, 31, 32"
      ]
    }
  },
  {
    "id": "15",
    "file": "15_framing_contract",
    "track": "self-study",
    "title": "Problem framing and typed message contracts",
    "subtitle": "Frame checkout qualities and typed proposals",
    "topics": "framing quality attribute scenarios iso 25010 message contract schema confidence swappable agents chair passive goal creator and a contract microservices DDD ShopEasy lecture revision Dependency-specific resilience Non-idempotent payment safety Requirements versus assumed targets",
    "idea": "Turn a vague goal into measurable scenarios and comparable proposals.",
    "objectives": [
      "Turn a checkout brief into measurable scenarios and comparable architecture messages.",
      "Identify which targets are given facts and which are assumptions to confirm with a stakeholder.",
      "Check measurable scenarios, option labels, confidence, and trade-offs."
    ],
    "example": "Consider timeouts, payment safety, and graceful degradation for optional Recommendations.",
    "exercise": "Identify which targets are given facts and which are assumptions to confirm with a stakeholder.",
    "checks": "Check measurable scenarios, option labels, confidence, and trade-offs.",
    "bridge": "Timeouts, retries, breakers, bulkheads, and fallback solve different failure problems.",
    "pattern": "Passive Goal Creator and a contract",
    "steps": 5,
    "warmups": 1,
    "patterns": [
      "Passive Goal Creator"
    ],
    "background": [
      "Framing gives participants the same question and quality goals. A typed contract makes replies comparable but cannot establish that a proposed target is appropriate.",
      "Timeouts, retries, breakers, bulkheads, and fallback solve different failure problems."
    ],
    "terms": [
      [
        "Quality-attribute scenario",
        "A testable statement: a stimulus, the required response, and a measure."
      ],
      [
        "ISO/IEC 25010",
        "A standard model of software quality characteristics."
      ],
      [
        "Message contract",
        "The fields and rules that every message between agents must follow."
      ],
      [
        "Self-reported confidence",
        "A model's own estimate of how sure it is; information, not proof."
      ]
    ],
    "review": {
      "sources": [
        {
          "deck": "microservices",
          "slides": [
            38,
            39,
            41
          ]
        },
        {
          "deck": "ddd",
          "slides": [
            13,
            60
          ]
        }
      ],
      "concepts": [
        "Dependency-specific resilience",
        "Non-idempotent payment safety",
        "Requirements versus assumed targets"
      ],
      "questions": [
        "Why can the same timeout not fit every checkout dependency?",
        "Can a well-formed proposal still recommend an unsafe payment retry?"
      ],
      "readings": [
        "Microservices & Their Patterns · slides 38, 39, 41",
        "Microservices Lecture 2 - Condensed DDD · slides 13, 60"
      ]
    }
  },
  {
    "id": "16",
    "file": "16_learning_curve_trust",
    "track": "self-study",
    "title": "Learning from feedback: learning curves and trust weights",
    "subtitle": "Learn trust weights from retry decisions",
    "topics": "evaluation experiment feedback test split held-out learning curve per-model trust weighted vote council voting-based cooperation microservices DDD ShopEasy lecture revision Retry eligibility and idempotency Correlated reviewer errors Feedback/test separation",
    "idea": "Use separate feedback and test cases to inspect reviewer weights.",
    "objectives": [
      "Keep feedback cases separate from test cases while updating weights on pattern recommendations.",
      "Change the feedback order and inspect how a small sample affects the learning curve.",
      "Use synthetic fixtures to test aggregation; never train trust on held-out labels."
    ],
    "example": "Use idempotent reads and non-idempotent charges to demonstrate safe versus unsafe retry advice.",
    "exercise": "Change the feedback order and inspect how a small sample affects the learning curve.",
    "checks": "Use synthetic fixtures to test aggregation; never train trust on held-out labels.",
    "bridge": "Trust estimates on a tiny dataset are fragile; a rising demo curve is not evidence about real models.",
    "pattern": "Voting-Based Cooperation",
    "steps": 4,
    "warmups": 1,
    "patterns": [
      "Voting-Based Cooperation"
    ],
    "background": [
      "Feedback-weighted aggregation changes whom a council trusts. A fixed split and a visible curve make leakage and learning assumptions easier to inspect.",
      "Trust estimates on a tiny dataset are fragile; a rising demo curve is not evidence about real models."
    ],
    "terms": [
      [
        "Train/test split",
        "Separate cases for learning and for scoring."
      ],
      [
        "Learning curve",
        "The score plotted after each round of feedback."
      ],
      [
        "Weighted vote",
        "A vote in which each voter counts according to its weight."
      ],
      [
        "Trust",
        "Here, how often an architect has agreed with the human on the feedback cases."
      ]
    ],
    "review": {
      "sources": [
        {
          "deck": "microservices",
          "slides": [
            39,
            41
          ]
        },
        {
          "deck": "ddd",
          "slides": [
            51,
            52,
            55
          ]
        }
      ],
      "concepts": [
        "Retry eligibility and idempotency",
        "Correlated reviewer errors",
        "Feedback/test separation"
      ],
      "questions": [
        "Why is retrying a card charge different from retrying a price read?",
        "Why must test labels stay out of trust updates?"
      ],
      "readings": [
        "Microservices & Their Patterns · slides 39, 41",
        "Microservices Lecture 2 - Condensed DDD · slides 51, 52, 55"
      ]
    }
  },
  {
    "id": "17",
    "file": "17_weighted_decision_jev",
    "track": "self-study",
    "title": "Decision models: a weighted decision matrix with a scoring model",
    "subtitle": "Weighted decisions for task queues and event logs",
    "topics": "decision matrix criteria weights scoring model typesafe jev system one score rubric composite judgement trade-off reweight microservices DDD ShopEasy lecture revision task queues versus retained event logs independent consumer groups and replay partition key versus eventId consumer parallelism is capped by partitions",
    "idea": "Make priorities and hard requirements explicit in a decision matrix.",
    "objectives": [
      "Separate illustrative scores from priorities.",
      "Recall Kafka grouping, deduplication IDs, and per-group partition limits.",
      "Keep hard requirements outside the weighted average."
    ],
    "example": "Compare a simple task queue with a retained event log; distinguish an order key from eventId and compute consumer-group parallelism.",
    "exercise": "Make replay mandatory, change the Kafka key, or add a fifth consumer to four partitions.",
    "checks": "Check the weighted arithmetic, key roles, and consumer count; TypeSafe judgements can differ.",
    "bridge": "Preferences belong in weights; mandatory replay is an eligibility condition. Partition keys, event IDs, and consumer offsets solve different problems.",
    "steps": 5,
    "warmups": 1,
    "patterns": [],
    "background": [
      "A weighted matrix exposes the assumptions behind a choice. Code combines the scores; a scoring model supplies judgements rather than implementing broker guarantees.",
      "A task queue distributes deliveries among workers. A retained event log lets subscriber groups read and replay independently. Kafka groups are limited by partition count; eventId supports deduplication while a record key determines grouping under a stable partition mapping."
    ],
    "terms": [
      [
        "Decision model",
        "A repeatable procedure that turns judgements into a choice."
      ],
      [
        "Weighted decision matrix",
        "Option scores per criterion, each multiplied by the criterion's weight and summed."
      ],
      [
        "Weight",
        "How much one criterion counts toward the choice; the team's stated priority."
      ],
      [
        "System One model",
        "A model such as TypeSafe JEV that returns typed judgements and probabilities, not prose."
      ]
    ],
    "review": {
      "sources": [
        {
          "deck": "ddd",
          "slides": [
            44,
            47,
            48,
            49,
            50,
            51,
            52,
            92
          ]
        }
      ],
      "concepts": [
        "task queues versus retained event logs",
        "independent consumer groups and replay",
        "partition key versus eventId",
        "consumer parallelism is capped by partitions"
      ],
      "questions": [
        "Should competing workers process a task, or should each subscriber group read the same event?",
        "Why do orderId as the Kafka key and eventId for deduplication solve different problems?"
      ],
      "readings": [
        "Microservices Lecture 2 - Condensed DDD · slides 44, 47, 48, 49, 50, 51, 52, 92"
      ]
    }
  }
];

const patternGuide = [
  {"name": "Retrieval-Augmented Generation", "category": "Single-agent"},
  {"name": "Single-Path Planning", "category": "Single-agent"},
  {"name": "One-Step Tool Agent", "category": "Single-agent"},
  {"name": "Passive Goal Creator", "category": "Single-agent"},
  {"name": "Debate-Based Cooperation", "category": "Multi-agent"},
  {"name": "Voting-Based Cooperation", "category": "Multi-agent"},
  {"name": "Human in the Loop", "category": "Multi-agent"},
  {"name": "Generator–Critic Loop", "category": "Multi-agent"},
  {"name": "Registry & Adapter", "category": "Multi-agent"},
  {"name": "Skill Library Evolution", "category": "Multi-agent"},
  {"name": "Scratchpad Memory", "category": "Memory"},
  {"name": "Archival Memory", "category": "Memory"},
  {"name": "Shared Memory", "category": "Memory"},
  {"name": "Routing", "category": "Built from the guide", "note": "Combines Human in the Loop's risk classification with Registry & Adapter's dispatch."}
];

const tracks = [
  {
    "id": "lecture-1",
    "label": "Lecture 1 · 90 minutes",
    "title": "Ask, check, retrieve",
    "note": "A rule, a model, a test set, and retrieval: the building blocks of every later lab."
  },
  {
    "id": "lecture-2",
    "label": "Lecture 2 · 90 minutes",
    "title": "Chain, call tools, act",
    "note": "From a fixed chain of prompts, to tools that read and change an in-memory Order, to an agent that chooses its own steps."
  },
  {
    "id": "lecture-3",
    "label": "Lecture 3 · 90 minutes",
    "title": "Debate, trace, decide",
    "note": "A council debates, structured logs make decisions traceable, and simulated human feedback is stored for later use."
  },
  {
    "id": "self-study",
    "label": "Self-study · at your own pace",
    "title": "Go deeper",
    "note": "An evaluation against single models, routing, protocols, skills, a framework, framing, a learning experiment, and decision models: what the project needs beyond the lectures. Each lab ends with a challenge for your council."
  }
];

const list = document.getElementById('lab-list');
const esc = text => String(text).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const config = window.COURSE_CONFIG || {};
const configured = typeof config.repo === 'string' && /^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})\/[A-Za-z0-9_.-]+$/.test(config.repo) && config.repo !== 'OWNER/REPO';
const ref = typeof config.ref === 'string' ? config.ref : 'main';
const STORAGE_KEY = 'agentic-ai-course-microservices-slides-v1-progress';
const number = i => String(i).padStart(2, '0');
let completed = [];
try { const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); if (Array.isArray(stored)) completed = stored.filter(x => labs.some(l => l.id === x)); } catch (_) { /* Browser storage is optional. */ }

function updateProgress() {
  const count = labs.filter(l => completed.includes(l.id)).length;
  document.getElementById('progress-label').textContent = `${count} / ${labs.length} labs explored`;
  document.getElementById('course-progress').value = count;
  labs.forEach(lab => document.getElementById(`lab-${lab.id}`).classList.toggle('done', completed.includes(lab.id)));
  tracks.forEach(track => {
    const ids = labs.filter(l => l.track === track.id).map(l => l.id);
    const text = `${ids.filter(id => completed.includes(id)).length} of ${ids.length} explored`;
    document.querySelectorAll(`[data-track-progress="${track.id}"]`).forEach(el => { el.textContent = text; });
    document.querySelectorAll(`[data-track-short="${track.id}"]`).forEach(el => { el.textContent = `${ids.filter(id => completed.includes(id)).length} / ${ids.length} done`; });
  });
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(completed)); } catch (_) { /* Private browsing can disable storage. */ }
}
function notebookActions(lab) {
  const path = `notebooks/${lab.file}.ipynb`;
  const colab = configured ? `https://colab.research.google.com/github/${config.repo}/blob/${encodeURIComponent(ref)}/${path}` : null;
  const action = colab ? `<a class="button primary" href="${esc(colab)}" target="_blank" rel="noopener">Open in Colab <span aria-hidden="true">↗</span></a>` : `<a class="button secondary" href="#setup">Colab setup <span aria-hidden="true">↑</span></a>`;
  return `<div class="notebook-actions">${action}<a class="button secondary" href="${path}" download>Download notebook <span aria-hidden="true">↓</span></a></div>`;
}
const chips = names => names.map(name => `<span class="pattern-chip">${esc(name)}</span>`).join('');

// A bar of the four sections that stays in view while the lab list scrolls.
const jump = document.createElement('nav');
jump.className = 'track-jump';
jump.setAttribute('aria-label', 'Lectures and self-study');
jump.innerHTML = tracks.map(track => `<a href="#track-${track.id}"><strong>${esc(track.label.split(' · ')[0])}</strong><small data-track-short="${track.id}"></small></a>`).join('');
list.before(jump);

const trackGroups = {};
tracks.forEach(track => {
  const group = document.createElement('section');
  group.className = 'track';
  group.id = `track-${track.id}`;
  group.setAttribute('aria-label', `${track.label}: ${track.title}`);
  group.innerHTML = `<div class="track-heading"><div class="track-meta"><span class="tag">${esc(track.label)}</span><span class="track-progress" data-track-progress="${track.id}"></span></div><h3>${esc(track.title)}</h3><p>${esc(track.note)}</p></div>`;
  list.appendChild(group);
  trackGroups[track.id] = group;
});

labs.forEach((lab, i) => {
  const detail = document.createElement('details');
  detail.className = 'lab';
  detail.id = `lab-${lab.id}`;
  detail.dataset.search = `${lab.title} ${lab.subtitle} ${lab.topics} ${lab.patterns.join(' ')} ${(lab.review?.concepts || []).join(' ')}`.toLowerCase();
  const prev = labs[i - 1], next = labs[i + 1];
  const pager = `<nav class="lab-pager" aria-label="Neighbouring labs">${prev ? `<a href="#lab-${prev.id}"><small>← Lab ${prev.id}</small>${esc(prev.title)}</a>` : '<span></span>'}${next ? `<a class="next" href="#lab-${next.id}"><small>Lab ${next.id} →</small>${esc(next.title)}</a>` : ''}</nav>`;
  detail.innerHTML = `<summary><span class="lab-number" aria-hidden="true"><span class="num">${number(i)}</span><span class="tick">✓</span></span><div><h3><span class="visually-hidden">Lab ${number(i)}: </span>${esc(lab.title)}</h3><p>${chips(lab.patterns)}<span class="lab-subtitle">${esc(lab.subtitle)}</span></p></div><span class="lab-time">${lab.steps} core steps${lab.warmups ? `<br>+ ${lab.warmups} warm-up` : ""}${lab.optional_examples ? `<br>+ ${lab.optional_examples} optional examples` : ""}</span><span class="expand-icon" aria-hidden="true">+</span></summary>`
    + `<div class="lab-body"><div class="lab-lead"><p class="lab-intro">${esc(lab.idea)}</p>${notebookActions(lab)}</div>`
    + `<section class="lab-context" aria-label="The idea in context"><div><h4>The idea in context</h4>${lab.background.map(text => `<p>${esc(text)}</p>`).join('')}</div>`
    + `<aside class="key-terms"><h4>Key terms</h4><dl>${lab.terms.map(([term, meaning]) => `<dt>${esc(term)}</dt><dd>${esc(meaning)}</dd>`).join('')}</dl></aside></section>`
    + `<h4 class="diagram-heading">How the lab works</h4><figure class="lab-diagram" data-diagram="${lab.id}"></figure>`
    + `${lab.picture ? `<figure class="sampling-figure"><a href="${esc(lab.picture.src)}"><img src="${esc(lab.picture.src)}" alt="${esc(lab.picture.alt)}"></a><figcaption>${esc(lab.picture.caption)} Select the image to enlarge it.</figcaption></figure>` : ""}`
    + `${lab.tool ? `<p class="sampling-tool-link"><a class="text-link" href="${esc(lab.tool.src)}" target="_blank" rel="noopener">${esc(lab.tool.label)} ↗</a> · Adjust the settings and explore the resulting probabilities.</p>` : ""}`
    + `<div class="lesson-grid"><div><h4>What you will learn</h4><ul>${lab.objectives.map(t => `<li>${esc(t)}</li>`).join('')}</ul></div><div><h4>Walk through an example</h4><p>${esc(lab.example)}</p></div><div><h4>Make it your own</h4><p>${esc(lab.exercise)}</p></div><div><h4>Expected output &amp; check</h4><p>${esc(lab.checks)}</p></div></div>`
    + `<p class="lesson-takeaway"><strong>Takeaway.</strong> ${esc(lab.bridge)}</p>`
    + `<div class="lab-actions"><label class="completion"><input type="checkbox" data-lab="${lab.id}" ${completed.includes(lab.id) ? 'checked' : ''}> I explored lab ${number(i)}</label>${pager}</div>`
    + `${configured ? '' : '<p class="publish-note">Download this notebook and upload it to Colab, or configure the repository links.</p>'}</div>`;
  trackGroups[lab.track].appendChild(detail);
  detail.addEventListener('toggle', () => { if (detail.open) drawDiagram(detail); });
});

// The field guide's patterns, each linked to the labs that teach it.
const patternGrid = document.getElementById('pattern-grid');
if (patternGrid) {
  const categories = [...new Set(patternGuide.map(p => p.category))];
  patternGrid.innerHTML = categories.map(category => `<div class="pattern-column"><h3>${esc(category)}</h3><ul>${patternGuide.filter(p => p.category === category).map(p => {
    const where = labs.filter(l => l.patterns.includes(p.name)).map(l => `<a href="#lab-${l.id}">Lab ${l.id}</a>`).join(' ');
    return `<li><span class="pattern-name">${esc(p.name)}</span><span class="pattern-labs">${where}</span>${p.note ? `<small>${esc(p.note)}</small>` : ''}</li>`;
  }).join('')}</ul></div>`).join('');
}

function drawDiagram(detail) {
  const figure = detail.querySelector('.lab-diagram');
  if (figure && typeof renderDiagram === 'function') renderDiagram(figure, figure.dataset.diagram);
}
let resizeTimer;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => list.querySelectorAll('.lab[open]').forEach(drawDiagram), 150);
});

list.addEventListener('change', event => {
  if (!event.target.matches('input[data-lab]')) return;
  const id = event.target.dataset.lab;
  completed = event.target.checked ? [...new Set([...completed, id])] : completed.filter(x => x !== id);
  updateProgress();
});
document.getElementById('reset-progress').addEventListener('click', () => {
  completed = [];
  list.querySelectorAll('input[data-lab]').forEach(input => { input.checked = false; });
  updateProgress();
});
document.getElementById('lab-search').addEventListener('input', event => {
  const query = event.target.value.trim().toLowerCase();
  let visible = 0;
  list.querySelectorAll('.lab').forEach(lab => { lab.hidden = !lab.dataset.search.includes(query); if (!lab.hidden) visible += 1; });
  list.querySelectorAll('.track').forEach(group => { group.hidden = !group.querySelector('.lab:not([hidden])'); });
  document.getElementById('filter-status').textContent = query ? `${visible} ${visible === 1 ? 'lab' : 'labs'} found` : `All ${labs.length} labs`;
});
function clearSearch() {
  document.getElementById('lab-search').value = '';
  list.querySelectorAll('.lab, .track').forEach(item => { item.hidden = false; });
  document.getElementById('filter-status').textContent = `All ${labs.length} labs`;
}
function openLab(id) {
  const lab = labs.find(l => `lab-${l.id}` === id);
  if (!lab) return;
  const detail = document.getElementById(id);
  clearSearch();
  list.querySelectorAll('.lab[open]').forEach(other => { if (other !== detail) other.open = false; });
  detail.open = true;
  detail.scrollIntoView({block: 'start'});
}
if (configured) document.querySelectorAll('.repo-link').forEach(a => { a.href = `https://github.com/${config.repo}`; a.textContent = 'GitHub ↗'; });
function openHash() { openLab(window.location.hash.slice(1)); }
document.addEventListener('click', event => {
  const link = event.target.closest('a[href^="#lab-"]');
  if (link) openLab(link.getAttribute('href').slice(1));
  if (event.target.closest('a[href^="#track-"]')) clearSearch();
});
window.addEventListener('hashchange', openHash);
updateProgress();
if (location.hash.startsWith('#lab-')) openHash();
