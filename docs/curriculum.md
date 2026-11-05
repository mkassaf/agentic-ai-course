# Curriculum

Thirteen beginner labs teach general agentic AI through one small software architecture question: **modular monolith or microservices?** Keep the case familiar while changing one mechanism at a time.

Each lab takes **15–20 minutes**, plus first-run installation. It has two to five numbered steps, each one code cell of at most **20 Python lines** (at most **75 example lines** per lab), a check, and small exercises. Students need basic Python. Nine core labs fit three 90-minute lectures, three labs each; four self-study labs follow.

## The shared case

The labs reuse four fictional projects that cover every combination of the two facts: the Course portal (3 people, one shared release), the Payments platform (12 people, independent deploys), the Internal wiki (9 people, one shared release), and the Mobile backend (5 people, independent deploys). Our fictional course policy chooses microservices only when `team_size >= 8` **and** `independent_deploys` is true; otherwise it chooses a modular monolith.

This deliberately small policy makes comparisons easy. It is not a real-world architecture prescription: deployment boundaries, ownership, reliability, cost, and operational maturity need richer analysis.

## Three lectures and self-study

The core labs, 00–08, cover every pattern that the council project needs, so a student who attends the three lectures has seen all of them. The self-study labs, 09–12, cover the *implementation choices* that the project brief leaves open: MCP for tools, Agent Skills for reusable procedures, A2A for agents that talk across processes, and LangGraph for orchestration. Students take them at their own pace, and each ends with a challenge that applies it to their own council.

Each lab adds one mechanism to the previous one and says so at the top: **So far** recalls the last lab, **New** names the single addition. The same projects, the policy sentence, and names such as `projects`, `expected`, and `scripted` recur, so only the new idea needs attention. Each step adds one piece of logic and prints something to check.

**Lecture 1 · Ask, check, retrieve (90 minutes)**

| Lab | New mechanism | Student comparison |
| --- | --- | --- |
| **00 · Rules, then LLM calls** | A Python rule with reasons, a reply normaliser, unguided model calls | Where does a model without the policy disagree with the rule? |
| **01 · Better prompts and small evaluations** | Guided prompt, JSON parser, five labelled cases, quality gate | Which cases does the guided prompt get right, and which reply breaks the format? |
| **02 · Retrieve architecture rules with RAG** | Embeddings, a Chroma vector database, a distance threshold, citation checks | Which evidence supports the answer, and when should the system abstain? |

**Lecture 2 · Chain, act, debate (90 minutes)**

| Lab | New mechanism | Student comparison |
| --- | --- | --- |
| **03 · Chain the steps of a decision** | A chain of four prompts with a gate after each step | Which step's reply would you check first, and what does a gate not check? |
| **04 · ReAct: choose a tool, then decide** | Guarded action/observation loop with a history | Who chooses the next step, and what stops the loop? |
| **05 · A council of architects: propose, challenge, agree** | Independent parallel proposals on three model families, challenges, grounded votes, dissent, escalation | Which claim was challenged, which votes counted, and whose dissent was kept? |

**Lecture 3 · Decide, learn, measure (90 minutes)**

| Lab | New mechanism | Student comparison |
| --- | --- | --- |
| **06 · The human decides, the council learns** | Human review with bounded revision, a memory of past decisions, held-out evaluation | Which lesson did a new case recall, and did it apply? |
| **07 · Route each case: rule or council** | A model router with worked examples, a dispatch table, a safe fallback, routing cost | Which mistake would you rather make: a wasted debate or a skipped one? |
| **08 · Does the council beat a single model?** | Baseline comparison, an LLM judge, calibration against human ratings | On which measures does the council win, at what cost, and can you trust the judge? |

**Self-study · Connect and organize your council**

| Lab | New mechanism | Student comparison |
| --- | --- | --- |
| **09 · Architecture tools and our own MCP server** | Read and write MCP tools with schemas and error results | What is read, what state changes, and what happens on a bad call? |
| **10 · A skill for a short architecture decision record** | Skill catalog, progressive disclosure, ADR checker | Which skill fits the task, and what does its output promise? |
| **11 · Delegate an architecture review with A2A** | Propose, review over A2A, revise on feedback | What crosses the agent interface, and how does feedback change the proposal? |
| **12 · A framework for choosing and checking** | Choose-and-check graph with a conditional retry | Which node proposes, which validates, and what ends the loop? |

## Four core areas

| Area | Labs |
| --- | --- |
| LLMs and Prompting · RAG Systems | 00–02 (Lecture 1) |
| Foundations of AI Agents · Agentic Patterns | 03–08 (Lectures 2 and 3) |
| Tools and MCP · A2A Protocol | 04 (tools, Lecture 2); 09 and 11 (self-study) |
| Skills · Frameworks | 10 and 12 (self-study) |

## Agentic patterns for the architecture council

Labs 03–08 build the course project's council one pattern at a time, in the order *chaining → independent proposals → critique → chair-controlled consensus → human feedback → memory*, then decide when the council is worth its cost (*routing*) and whether it beats a single model (*evaluation*). Retrieval and tools come from the earlier labs. The central idea: **form independent opinions, debate with evidence, reach a proposal, then learn from human feedback.**

| Pattern | Where students build it | Purpose in the project |
| --- | --- | --- |
| Prompt chaining | 03: requirements → options → trade-offs → decision record, with gates | Break the decision process into clear, checkable steps |
| Independent parallel proposals | 05: three architects answer alone, in parallel | Preserve different perspectives before the debate |
| Coordinator / chair | 05: a chair with fixed rules runs the rounds | Manage the process while the architects stay peers |
| Critique and revision | 05: an opponent challenges an unsourced claim; its author revises (self-study 11 and 12 add reviewer and checker feedback) | Make disagreement useful and evidence-based |
| Consensus and aggregation | 05: grounded votes, a two-thirds stopping rule, recorded dissent, escalation on deadlock | Produce a decision with a clear stopping rule and deadlock handling |
| Human-in-the-loop | 06: the human rejects microservices for its operating cost; the council revises until the human accepts | Use feedback and keep the human's final authority |
| Memory and feedback reuse | 06: the accepted decision and its reasons are stored and recalled for later cases | Improve future decisions, not only the current one |
| Routing | 07: a model router with worked examples, a dispatch table, and a fallback to the council | Spend a debate only on contested cases, and count what routing costs |
| Retrieval and grounding | 02: embeddings, a vector database, and citation checks; 05: claims must cite sources; 06: memory recall | Support arguments with traceable evidence |
| Tool use / ReAct | 04 (self-study 09 serves tools over MCP) | Fetch evidence before deciding |
| Structured messages and shared state | 01 (JSON replies), 05 (a transcript of `round`, `speaker`, `kind` messages), self-study 12 (graph state) | Identify the speaker, proposal, critique, evidence, and round |
| Evaluation | 01 (labelled checks), 06 (held-out cases before and after memory), 08 (council against the best single model, with an LLM judge calibrated against human ratings) | Compare approaches, measure improvement on unseen cases, and trust a judge only as far as it agrees with people |
| MCP, A2A, skills, frameworks | Self-study 09, 11, 10, 12 | Ways to connect and organize the implementation |

*Orchestrator–workers*, where a central model splits a task into subtasks for specialist workers, has no lab of its own: the brief gives every architect the full mandate, and Lab 05's chair already coordinates the peers. Students can add a chair agent that frames the case or writes the final decision record.

The project requires **at least three model families**. Three personas on one model share one set of blind spots; in a live test with Qwen behind all three personas, the three architects agreed at once and cited the same sources.

## Keep reasoning and evaluation observable

Prompt decomposition means checking explicit criteria and asking for a brief, verifiable justification. This is a teaching adaptation inspired by chain-of-thought prompting, not a reproduction of the original method or access to private model reasoning. ReAct-style action and observation comes after students have used tools. Its compact control-flow example illustrates the loop without implementing a full native function-calling agent.

Evaluate three things: adherence to the supplied policy, grounding in the case and retrieved evidence, and the clarity of one consequence or trade-off. The automatic checks cover only part of that assessment. Scripted practice scores demonstrate the evaluation code; only live runs provide evidence about model behavior, and five cases cannot establish general quality.

The RAG lab embeds policies with a small local model (`all-MiniLM-L6-v2`) and stores them in an in-memory Chroma vector database; a word-matching step shows what embeddings add. The memory lab reuses the same model and database for past decisions. The council's chair is plain code; Lab 06's `council` stands in for the full council with one model call to keep the lab short. MCP and A2A use their real SDKs locally; the save action changes only in-memory data. The skills lab chooses from a small in-notebook catalog rather than a full skill host. LangGraph runs an actual two-node graph with a conditional retry. Supporting transport code stays in the installable course package.

See the [instructor guide](instructor-guide.md) and [technical references](sources.md).
