# Curriculum

Sixteen beginner labs teach general agentic AI through one small software architecture question: **modular monolith or microservices?** Keep the case familiar while changing one mechanism at a time.

Each lab takes **15–20 minutes**, plus first-run installation. It has two to five numbered steps, each one code cell of at most **20 Python lines** (at most **75 example lines** per lab), a check, and small exercises. Students need basic Python. Nine core labs fit three 90-minute lectures, three labs each; seven self-study labs follow.

## The shared case

The labs reuse four fictional projects that cover every combination of the two facts: the Course portal (3 people, one shared release), the Payments platform (12 people, independent deploys), the Internal wiki (9 people, one shared release), and the Mobile backend (5 people, independent deploys). Our fictional course policy chooses microservices only when `team_size >= 8` **and** `independent_deploys` is true; otherwise it chooses a modular monolith.

This deliberately small policy makes comparisons easy. It is not a real-world architecture prescription: deployment boundaries, ownership, reliability, cost, and operational maturity need richer analysis.

## Three lectures and self-study

The core labs, 00–08, cover every pattern that the council project needs, so a student who attends the three lectures has seen all of them. The self-study labs, 09–15, cover what the project needs beyond the lectures. Lab 09 adds routing. Labs 10–13 are the *implementation choices* that the brief leaves open: MCP for tools, Agent Skills for reusable procedures, A2A for agents that talk across processes, and LangGraph for orchestration. Labs 14–15 are two project steps that need more time than a lecture allows: framing the debate with quality-attribute scenarios and a message contract, and measuring learning with a feedback/test split, a learning curve, and per-model trust. Students take them at their own pace, and each ends with a challenge that applies it to their own council.

Each lab adds one mechanism to the previous one and says so at the top: **So far** recalls the last lab, **New** names the single addition. The same projects, the policy sentence, and names such as `projects`, `expected`, and `scripted` recur, so only the new idea needs attention. Each step adds one piece of logic and prints something to check.

**Lecture 1 · Ask, check, retrieve (90 minutes)**

| Lab | New mechanism | Student comparison |
| --- | --- | --- |
| **00 · Rules, then LLM calls** | A Python rule with reasons, a reply normaliser, unguided model calls | Where does a model without the policy disagree with the rule? |
| **01 · Better prompts and small evaluations** | Guided prompt, JSON parser, five labelled cases, quality gate | Which cases does the guided prompt get right, and which reply breaks the format? |
| **02 · Retrieve architecture rules with RAG** | Embeddings, a Chroma vector database, a distance threshold, citation checks | Which evidence supports the answer, and when should the system abstain? |

**Lecture 2 · Chain, call tools, act (90 minutes)**

| Lab | New mechanism | Student comparison |
| --- | --- | --- |
| **03 · Chain the steps of a decision** | A chain of four prompts with a gate after each step | Which step's reply would you check first, and what does a gate not check? |
| **04 · Tools: let the model read and change live data** | A read tool and a write tool, tool descriptions, argument checks, confirmation before a change | What can the model know without a tool, and who decides that a tool may change data? |
| **05 · ReAct: choose a tool, then decide** | Guarded action/observation loop with a history | Who chooses the next step, and what stops the loop? |

**Lecture 3 · Debate, decide, measure (90 minutes)**

| Lab | New mechanism | Student comparison |
| --- | --- | --- |
| **06 · A council of architects: propose, challenge, agree** | Independent parallel proposals on three model families, challenges, grounded votes, dissent, escalation | Which claim was challenged, which votes counted, and whose dissent was kept? |
| **07 · The human decides, the council learns** | Human review with bounded revision, a memory of past decisions, held-out evaluation | Which lesson did a new case recall, and did it apply? |
| **08 · Does the council beat a single model?** | Baseline comparison, an LLM judge, calibration against human ratings | On which measures does the council win, at what cost, and can you trust the judge? |

**Self-study · Build your council further**

| Lab | New mechanism | Student comparison |
| --- | --- | --- |
| **09 · Route each case: rule or council** | A model router with worked examples, a dispatch table, a safe fallback, routing cost | Which mistake would you rather make: a wasted debate or a skipped one? |
| **10 · Architecture tools and our own MCP server** | Read and write MCP tools with schemas and error results | What is read, what state changes, and what happens on a bad call? |
| **11 · A skill for a short architecture decision record** | Skill catalog, progressive disclosure, ADR checker | Which skill fits the task, and what does its output promise? |
| **12 · Delegate an architecture review with A2A** | Propose, review over A2A, revise on feedback | What crosses the agent interface, and how does feedback change the proposal? |
| **13 · A framework for choosing and checking** | Choose-and-check graph with a conditional retry | Which node proposes, which validates, and what ends the loop? |
| **14 · Frame the debate and agree on a message contract** | ISO/IEC 25010 quality-attribute scenarios, a proposal contract with confidence, swappable architects | Which scenario has no number, and what does a contract make possible? |
| **15 · Learn from feedback: a learning curve and per-model trust** | Feedback/test split, trust-weighted votes, a learning curve | When does the curve rise, why can it fall, and why does a coin toss get no vote? |

## Four core areas

| Area | Labs |
| --- | --- |
| LLMs and Prompting · RAG Systems | 00–02 (Lecture 1) |
| Foundations of AI Agents · Agentic Patterns | 03–08 (Lectures 2 and 3); 09, 14, 15 (self-study) |
| Tools and MCP · A2A Protocol | 04 and 05 (tools, Lecture 2); 10 and 12 (self-study) |
| Skills · Frameworks | 11 and 13 (self-study) |

## Agentic patterns for the architecture council

Labs 03–09 build the course project's council one pattern at a time, in the order *chaining → independent proposals → critique → chair-controlled consensus → human feedback → memory*, then decide when the council is worth its cost (*routing*) and whether it beats a single model (*evaluation*). Retrieval and tools come from the earlier labs. The central idea: **form independent opinions, debate with evidence, reach a proposal, then learn from human feedback.** Pattern names, descriptions, and quality attributes follow the [Architectural Patterns for Agentic AI](https://karthikv1392.github.io/agentic-patterns/) field guide by Karthik Vaidhyanathan; each lab opens with a pattern card in the guide's format: context, problem, solution, use when, trade-off, flow, and quality attributes.

| Pattern | Field-guide pattern | Where students build it | Purpose in the project |
| --- | --- | --- | --- |
| Prompt chaining | Single-Path Planning (with a fixed plan) | 03: requirements → options → trade-offs → decision record, with gates | Break the decision process into clear, checkable steps |
| Independent parallel proposals | Parallel Fan-Out | 06: three architects answer alone, in parallel | Preserve different perspectives before the debate |
| Coordinator / chair | Debate-Based Cooperation (the judge) | 06: a chair with fixed rules runs the rounds | Manage the process while the architects stay peers |
| Critique and revision | Debate-Based Cooperation; Generator–Critic Loop | 06: an opponent challenges an unsourced claim; its author revises (self-study 12 and 13 add reviewer and checker feedback) | Make disagreement useful and evidence-based |
| Consensus and aggregation | Voting-Based Cooperation | 06: grounded votes, a two-thirds stopping rule, recorded dissent, escalation on deadlock | Produce a decision with a clear stopping rule and deadlock handling |
| Human-in-the-loop | Human in the Loop | 07: the human rejects microservices for its operating cost; the council revises until the human accepts | Use feedback and keep the human's final authority |
| Memory and feedback reuse | Archival Memory | 07: the accepted decision and its reasons are stored and recalled for later cases | Improve future decisions, not only the current one |
| Framing | Passive Goal Creator | 14: the chair turns the brief into measurable ISO/IEC 25010 quality-attribute scenarios | Give every architect the same scenarios to argue about |
| Message contract and swappable agents | Registry & Adapter | 14: every proposal names an option, a trade-off per scenario, a confidence, and a claim | Make proposals comparable and agents replaceable |
| Per-model trust | Voting-Based Cooperation (weighted scoring) | 15: votes weighted by each architect's record against the human | A learning lever that needs no prompt changes |
| Routing | Not in the guide: Human in the Loop's risk classification plus a dispatch | 09: a model router with worked examples, a dispatch table, and a fallback to the council | Spend a debate only on contested cases, and count what routing costs |
| Retrieval and grounding | Retrieval-Augmented Generation | 02: embeddings, a vector database, and citation checks; 06: claims must cite sources; 07: memory recall | Support arguments with traceable evidence |
| Tool use / ReAct | One-Step Tool Agent (in a loop); Registry & Adapter | 04 (a search and a booking tool), 05 (a ReAct loop); self-study 10 serves tools over MCP | Fetch evidence before deciding |
| Structured messages and shared state | Shared Memory | 01 (JSON replies), 06 (a transcript of `round`, `speaker`, `kind` messages), self-study 13 (graph state) | Identify the speaker, proposal, critique, evidence, and round |
| Evaluation | Not a pattern: it measures the patterns' quality attributes | 01 (labelled checks), 07 (held-out cases before and after memory), 08 (council against the best single model, with an LLM judge calibrated against human ratings), 15 (a feedback/test split and a learning curve) | Compare approaches, measure improvement on unseen cases, and trust a judge only as far as it agrees with people |
| MCP, A2A, skills, frameworks | Registry & Adapter; Generator–Critic Loop; Skill Library Evolution | Self-study 10, 12, 11, 13 | Ways to connect and organize the implementation |

*Orchestrator–workers*, where a central model splits a task into subtasks for specialist workers, has no lab of its own: the brief gives every architect the full mandate, and Lab 06's chair already coordinates the peers. Students can add a chair agent that frames the case or writes the final decision record.

The project requires **at least three model families**. Three personas on one model share one set of blind spots; in a live test with Qwen behind all three personas, the three architects agreed at once and cited the same sources. With Qwen, DeepSeek, and Gemini behind them, they split 2 to 1, and the chair kept Qwen's dissent about the single operations engineer.

## Project readiness: the brief, requirement by requirement

The labs never solve the project: they use a different question (modular monolith or microservices), different cases, and their own stances. Every requirement of the project brief is still practised somewhere.

| Brief requirement | Where students practise it |
| --- | --- |
| At least three architect agents, each on a different model family | 06 (Qwen, DeepSeek, and Gemini); 06's exercise compares one family with three |
| Same question and knowledge base for every architect | 02 (retrieval with citations), 06 (shared sources) |
| Same output contract: options, trade-offs, confidence | 03 (trade-off table), 14 (contract with confidence) |
| Distinct stances | 06 (example stances), 14 (add your own architect) |
| Frame: the chair sets the context and quality-attribute scenarios | 14 |
| Propose alone, then debate | 06 |
| Critique and revise, change one's mind only for an argument | 06 (sourced challenges); 12 and 13 (reviewer and checker feedback) |
| Converge by vote, score, or consensus | 06 (grounded votes), 14 (confidence), 15 (trust-weighted votes) |
| Decide: a decision record with the dissent | 03 and 11 (decision records), 06 (recorded dissent); Lab 11's challenge adds the dissent to the record |
| Bounded rounds; deadlock goes to the chair or the human | 06, 07, 15 (ties escalate) |
| Structured, observable, traceable, and swappable communication | 06 (transcript), 14 (contract and a fourth architect), 12 (A2A messages) |
| Free choice of patterns and protocols | 03–09; 10 (MCP), 12 (A2A), 13 (LangGraph) |
| Knowledge with provenance: catalogs, ISO/IEC 25010, past decisions | 02 (vector store and citations), 07 (past decisions in memory), 14 (ISO/IEC 25010) |
| Short loop: human feedback in the next round | 07 |
| Long loop: memory, principles, per-model trust | 07 (memory of lessons), 15 (per-model trust) |
| Experiment A: council against each single model; accuracy, trade-off coverage, citations, cost, latency | 08 |
| Experiment B: feedback and test split, scores before and after, a learning curve, never test on feedback | 07 and 15 |
| LLM-as-judge only if calibrated against human ratings | 08 |
| ADRs that justify design choices | 03 and 11 |

Three design questions from the brief are left for class discussion rather than a lab: a knowledge graph next to the vector store, keeping knowledge fresh, and a live demo interface for the debate.

## Keep reasoning and evaluation observable

Prompt decomposition means checking explicit criteria and asking for a brief, verifiable justification. This is a teaching adaptation inspired by chain-of-thought prompting, not a reproduction of the original method or access to private model reasoning. ReAct-style action and observation comes after students have used tools. Its compact control-flow example illustrates the loop without implementing a full native function-calling agent.

Evaluate three things: adherence to the supplied policy, grounding in the case and retrieved evidence, and the clarity of one consequence or trade-off. The automatic checks cover only part of that assessment. Scripted practice scores demonstrate the evaluation code; only live runs provide evidence about model behavior, and five cases cannot establish general quality.

The RAG lab embeds policies with a small local model (`all-MiniLM-L6-v2`) and stores them in an in-memory Chroma vector database; a word-matching step shows what embeddings add. The memory lab reuses the same model and database for past decisions. The council's chair is plain code; Lab 07's `council` stands in for the full council with one model call to keep the lab short. MCP and A2A use their real SDKs locally; the save action changes only in-memory data. The skills lab chooses from a small in-notebook catalog rather than a full skill host. LangGraph runs an actual two-node graph with a conditional retry. Supporting transport code stays in the installable course package.

See the [instructor guide](instructor-guide.md) and [technical references](sources.md).
