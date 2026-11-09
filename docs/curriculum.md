# Curriculum

Seventeen beginner labs teach general agentic AI through one small software architecture question: **modular monolith or microservices?** Keep the case familiar while changing one mechanism at a time.

Each lab takes **15–20 minutes**, plus first-run installation. It has two to five numbered steps, each one code cell of at most **20 Python lines** (at most **75 example lines** per lab), a check, and small exercises. Students need basic Python. Nine core labs fit three 90-minute lectures, three labs each; nine self-study labs follow.

## The shared case

The labs reuse four fictional projects that cover every combination of the two facts: the Course portal (3 people, one shared release), the Payments platform (12 people, independent deploys), the Internal wiki (9 people, one shared release), and the Mobile backend (5 people, independent deploys). Our fictional course policy chooses microservices only when `team_size >= 8` **and** `independent_deploys` is true; otherwise it chooses a modular monolith.

This deliberately small policy makes comparisons easy. It is not a real-world architecture prescription: deployment boundaries, ownership, reliability, cost, and operational maturity need richer analysis.

## Three lectures and self-study

The core labs, 00–08, cover every pattern that the council project needs, so a student who attends the three lectures has seen all of them. The self-study labs, 09–17, cover what the project needs beyond the lectures. Lab 09 runs the project's first experiment, the council against single models, and Lab 10 adds routing. Labs 11–14 are the *implementation choices* that the brief leaves open: MCP for tools, Agent Skills for reusable procedures, A2A for agents that talk across processes, and LangGraph for orchestration. Labs 15–17 are three project steps that need more time than a lecture allows: framing the debate with quality-attribute scenarios and a message contract, measuring learning with a feedback/test split, a learning curve, and per-model trust, and scoring options with a weighted decision matrix that a System One model can fill in. Students take them at their own pace, and each ends with a challenge that applies it to their own council.

Each lab adds one mechanism to the previous one and says so at the top: **So far** recalls the last lab, **New** names the single addition. The same projects, the policy sentence, and names such as `projects`, `expected`, and `scripted` recur, so only the new idea needs attention. Each step adds one piece of logic and prints something to check.

**Lecture 1 · Ask, check, retrieve (90 minutes)**

| Lab | New mechanism | Student comparison |
| --- | --- | --- |
| **00 · From rules to LLM calls** | A Python rule with reasons, a reply normaliser, unguided model calls | Where does a model without the policy disagree with the rule? |
| **01 · Prompting and small evaluations** | Guided prompt, JSON parser, five labelled cases, quality gate, and a live plain-vs-reasoning contrast | Which cases does the guided prompt get right, which reply breaks the format, and why does a plain model miss the R's in strawberry? |
| **02 · RAG: ground answers in retrieved knowledge** | Embeddings, a Chroma vector database, a distance threshold, citation checks | Which evidence supports the answer, and when should the system abstain? |

**Lecture 2 · Chain, call tools, act (90 minutes)**

| Lab | New mechanism | Student comparison |
| --- | --- | --- |
| **03 · Prompt chaining with quality gates** | A chain of four prompts with a gate after each step | Which step's reply would you check first, and what does a gate not check? |
| **04 · Tool calling: let the model read and change live data** | A read tool and a write tool, tool descriptions, argument checks, confirmation before a change | What can the model know without a tool, and who decides that a tool may change data? |
| **05 · ReAct agents: reason, act, observe** | Guarded action/observation loop with a history | Who chooses the next step, and what stops the loop? |

**Lecture 3 · Debate, trace, decide (90 minutes)**

| Lab | New mechanism | Student comparison |
| --- | --- | --- |
| **06 · Multi-agent debate: propose, challenge, agree** | Independent parallel proposals on three model families, challenges, grounded votes, dissent, escalation | Which claim was challenged, which votes counted, and whose dissent was kept? |
| **07 · Observability, tracing, and swappable agents** | A typed message, logs (a live stream and a JSON log file), an optional LangSmith trace, a trace back to sources from the log, a registry of agents | What do the logs show, which messages did the decision rest on, and what changed when an agent joined? |
| **08 · Human-in-the-loop and agent memory** | Human review with bounded revision, a memory of past decisions, held-out evaluation | Which lesson did a new case recall, and did it apply? |

**Self-study · Go deeper**

| Lab | New mechanism | Student comparison |
| --- | --- | --- |
| **09 · Evaluation: a multi-agent system against a single model** | Baseline comparison, an LLM judge, calibration against human ratings | On which measures does the council win, at what cost, and can you trust the judge? |
| **10 · Routing: rules, models, and a safe fallback** | A model router with worked examples, a dispatch table, a safe fallback, routing cost | Which mistake would you rather make: a wasted debate or a skipped one? |
| **11 · MCP: serve tools through a standard protocol** | Read and write MCP tools with schemas and error results | What is read, what state changes, and what happens on a bad call? |
| **12 · Agent skills: reusable instructions on demand** | Skill catalog, progressive disclosure, ADR checker | Which skill fits the task, and what does its output promise? |
| **13 · A2A: delegate work to another agent** | Propose, review over A2A, revise on feedback | What crosses the agent interface, and how does feedback change the proposal? |
| **14 · Agent frameworks: graphs with LangGraph** | Choose-and-check graph with a conditional retry | Which node proposes, which validates, and what ends the loop? |
| **15 · Problem framing and typed message contracts** | ISO/IEC 25010 quality-attribute scenarios, a proposal contract with confidence, swappable architects | Which scenario has no number, and what does a contract make possible? |
| **16 · Learning from feedback: learning curves and trust weights** | Feedback/test split, trust-weighted votes, a learning curve | When does the curve rise, why can it fall, and why does a coin toss get no vote? |
| **17 · Decision models: a weighted decision matrix with a scoring model** | Criterion weights stated explicitly, option scores per criterion, a System One model filling in the scores | Which decision model hides its assumptions, and which weight flips the winner? |

## Four core areas

| Area | Labs |
| --- | --- |
| LLMs and Prompting · RAG Systems | 00–02 (Lecture 1) |
| Foundations of AI Agents · Agentic Patterns | 03–08 (Lectures 2 and 3); 09, 10, 15, 16, 17 (self-study) |
| Tools and MCP · A2A Protocol | 04 and 05 (tools, Lecture 2); 11 and 13 (self-study) |
| Skills · Frameworks | 12 and 14 (self-study) |

## Agentic patterns for the architecture council

Labs 03–10 build the course project's council one pattern at a time, in the order *chaining → independent proposals → critique → chair-controlled consensus → human feedback → memory*, then decide when the council is worth its cost (*routing*) and whether it beats a single model (*evaluation*). Retrieval and tools come from the earlier labs. The central idea: **form independent opinions, debate with evidence, reach a proposal, then learn from human feedback.** Pattern names, descriptions, and quality attributes follow the [Architectural Patterns for Agentic AI](https://karthikv1392.github.io/agentic-patterns/) field guide by Karthik Vaidhyanathan; each lab opens with a pattern card in the guide's format: context, problem, solution, use when, trade-off, flow, and quality attributes.

| Pattern | Field-guide pattern | Where students build it | Purpose in the project |
| --- | --- | --- | --- |
| Prompt chaining | Single-Path Planning (with a fixed plan) | 03: requirements → options → trade-offs → decision record, with gates | Break the decision process into clear, checkable steps |
| Independent parallel proposals | Parallel Fan-Out | 06: three architects answer alone, in parallel | Preserve different perspectives before the debate |
| Coordinator / chair | Debate-Based Cooperation (the judge) | 06: a chair with fixed rules runs the rounds | Manage the process while the architects stay peers |
| Critique and revision | Debate-Based Cooperation; Generator–Critic Loop | 06: an opponent challenges an unsourced claim; its author revises (self-study 13 and 14 add reviewer and checker feedback) | Make disagreement useful and evidence-based |
| Consensus and aggregation | Voting-Based Cooperation | 06: grounded votes, a two-thirds stopping rule, recorded dissent, escalation on deadlock | Produce a decision with a clear stopping rule and deadlock handling |
| Human-in-the-loop | Human in the Loop | 08: the human rejects microservices for its operating cost; the council revises until the human accepts | Use feedback and keep the human's final authority |
| Memory and feedback reuse | Archival Memory | 08: the accepted decision and its reasons are stored and recalled for later cases | Improve future decisions, not only the current one |
| Framing | Passive Goal Creator | 15: the chair turns the brief into measurable ISO/IEC 25010 quality-attribute scenarios | Give every architect the same scenarios to argue about |
| Message contract and swappable agents | Registry & Adapter | 15: every proposal names an option, a trade-off per scenario, a confidence, and a claim | Make proposals comparable and agents replaceable |
| Per-model trust | Voting-Based Cooperation (weighted scoring) | 16: votes weighted by each architect's record against the human | A learning lever that needs no prompt changes |
| Routing | Not in the guide: Human in the Loop's risk classification plus a dispatch | 10: a model router with worked examples, a dispatch table, and a fallback to the council | Spend a debate only on contested cases, and count what routing costs |
| Retrieval and grounding | Retrieval-Augmented Generation | 02: embeddings, a vector database, and citation checks; 06: claims must cite sources; 08: memory recall | Support arguments with traceable evidence |
| Tool use / ReAct | One-Step Tool Agent (in a loop); Registry & Adapter | 04 (a search and a booking tool), 05 (a ReAct loop); self-study 11 serves tools over MCP | Fetch evidence before deciding |
| Observable, traceable, swappable agents | Shared Memory; Registry & Adapter | 07: typed, read-only messages, a bus that logs each one live and to a JSON log file, an optional LangSmith trace of each run, a trace from the decision back to its sources in that file, and a registry where an agent joins in one line | Meet the brief's "must be" rules without rewrites |
| Structured messages and shared state | Shared Memory | 01 (JSON replies), 06 (a transcript of `round`, `speaker`, `kind` messages), 07 (a typed `Message` dataclass), self-study 14 (graph state) | Identify the speaker, proposal, critique, evidence, and round |
| Evaluation | Not a pattern: it measures the patterns' quality attributes | 01 (labelled checks), 08 (held-out cases before and after memory), 09 (council against the best single model, with an LLM judge calibrated against human ratings), 16 (a feedback/test split and a learning curve) | Compare approaches, measure improvement on unseen cases, and trust a judge only as far as it agrees with people |
| Decision model | Not a pattern: a technique that judges options | 17: criterion weights stated explicitly, per-option scores (by hand, a vote, or a System One model), a weighted total | Decide which option the project's priorities pick, and change a weight instead of re-arguing |
| MCP, A2A, skills, frameworks | Registry & Adapter; Generator–Critic Loop; Skill Library Evolution | Self-study 11, 13, 12, 14 | Ways to connect and organize the implementation |

*Orchestrator–workers*, where a central model splits a task into subtasks for specialist workers, has no lab of its own: the brief gives every architect the full mandate, and Lab 06's chair already coordinates the peers. Students can add a chair agent that frames the case or writes the final decision record.

The project requires **at least three model families**. Three personas on one model share one set of blind spots; in a live test with Qwen behind all three personas, the three architects agreed at once and cited the same sources. With Qwen, DeepSeek, and Gemini behind them, they split 2 to 1, and the chair kept Qwen's dissent about the single operations engineer.

## Project readiness: the brief, requirement by requirement

The labs never solve the project: they use a different question (modular monolith or microservices), different cases, and their own stances. Every requirement of the project brief is still practised somewhere.

| Brief requirement | Where students practise it |
| --- | --- |
| At least three architect agents, each on a different model family | 06 (Qwen, DeepSeek, and Gemini); 06's exercise compares one family with three |
| Same question and knowledge base for every architect | 02 (retrieval with citations), 06 (shared sources) |
| Same output contract: options, trade-offs, confidence | 03 (trade-off table), 15 (contract with confidence) |
| Distinct stances | 06 (example stances), 15 (add your own architect) |
| Frame: the chair sets the context and quality-attribute scenarios | 15 |
| Propose alone, then debate | 06 |
| Critique and revise, change one's mind only for an argument | 06 (sourced challenges); 13 and 14 (reviewer and checker feedback) |
| Converge by vote, score, or consensus | 06 (grounded votes), 15 (confidence), 16 (trust-weighted votes), 17 (weighted decision matrix) |
| Decide: a decision record with the dissent | 03 and 12 (decision records), 06 (recorded dissent); Lab 12's challenge adds the dissent to the record |
| Bounded rounds; deadlock goes to the chair or the human | 06, 08, 16 (ties escalate) |
| Structured, observable, traceable, and swappable communication | 07 (a typed message, live logs and a JSON log file, a trace to sources from the log, agents added through a registry), 06 (transcript), 15 (contract and a fourth architect), 13 (A2A messages) |
| Free choice of patterns and protocols | 03–10; 11 (MCP), 13 (A2A), 14 (LangGraph) |
| Knowledge with provenance: catalogs, ISO/IEC 25010, past decisions | 02 (vector store and citations), 08 (past decisions in memory), 15 (ISO/IEC 25010) |
| Short loop: human feedback in the next round | 08 |
| Long loop: memory, principles, per-model trust | 08 (memory of lessons), 16 (per-model trust) |
| Experiment A: council against each single model; accuracy, trade-off coverage, citations, cost, latency | 09 |
| Experiment B: feedback and test split, scores before and after, a learning curve, never test on feedback | 08 and 16 |
| LLM-as-judge only if calibrated against human ratings | 09 |
| ADRs that justify design choices | 03 and 12 |

Three design questions from the brief are left for class discussion rather than a lab: a knowledge graph next to the vector store, keeping knowledge fresh, and a live demo interface for the debate.

## Keep reasoning and evaluation observable

Prompt decomposition means checking explicit criteria and asking for a brief, verifiable justification. This is a teaching adaptation inspired by chain-of-thought prompting, not a reproduction of the original method or access to private model reasoning. ReAct-style action and observation comes after students have used tools. Its compact control-flow example illustrates the loop without implementing a full native function-calling agent.

Lab 01's Step 5 shows what *reasoning models* do with that same idea. A plain model reads short familiar words as single tokens and so tends to miss a letter count (the "R's in strawberry" task); a chain-of-thought prompt spells the word out and usually fixes it; a reasoning model writes that same letter-by-letter count for itself in a `reasoning` field before answering, at the cost of extra output tokens and latency. It runs live on OpenRouter and falls back to scripted answers without a key, so the reasoning differences are explained in the narrative even in practice mode.

Evaluate three things: adherence to the supplied policy, grounding in the case and retrieved evidence, and the clarity of one consequence or trade-off. The automatic checks cover only part of that assessment. Scripted practice scores demonstrate the evaluation code; only live runs provide evidence about model behavior, and five cases cannot establish general quality.

The RAG lab embeds policies with a small local model (`all-MiniLM-L6-v2`) and stores them in an in-memory Chroma vector database; a word-matching step shows what embeddings add. The memory lab reuses the same model and database for past decisions. The council's chair is plain code; Lab 08's `council` stands in for the full council with one model call to keep the lab short. MCP and A2A use their real SDKs locally; the save action changes only in-memory data. The skills lab chooses from a small in-notebook catalog rather than a full skill host. LangGraph runs an actual two-node graph with a conditional retry. The decision-model lab computes its matrix in plain code and uses the TypeSafe SDK only for the optional live scoring step, so the arithmetic works without a model key. Supporting transport code stays in the installable course package.

See the [instructor guide](instructor-guide.md) and [technical references](sources.md).
