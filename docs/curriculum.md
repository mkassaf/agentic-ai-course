# Curriculum

Eight beginner labs teach general agentic AI through one small software architecture question: **modular monolith or microservices?** Keep the case familiar while changing one mechanism at a time.

Each lab takes **15–20 minutes**, plus first-run installation. It has two to five numbered steps, each one code cell of at most **20 Python lines** (at most **60 example lines** per lab), a check, and small exercises. Students need basic Python. Discussion and paired practice can extend a class to 60–90 minutes.

## The shared case

The labs reuse four fictional projects that cover every combination of the two facts: the Course portal (3 people, one shared release), the Payments platform (12 people, independent deploys), the Internal wiki (9 people, one shared release), and the Mobile backend (5 people, independent deploys). Our fictional course policy chooses microservices only when `team_size >= 8` **and** `independent_deploys` is true; otherwise it chooses a modular monolith.

This deliberately small policy makes comparisons easy. It is not a real-world architecture prescription: deployment boundaries, ownership, reliability, cost, and operational maturity need richer analysis.

## Eight steps

Each lab adds one mechanism to the previous one and says so at the top: **So far** recalls the last lab, **New** names the single addition. The same projects, the policy sentence, and names such as `projects`, `expected`, and `scripted` recur, so only the new idea needs attention. Each step adds one piece of logic and prints something to check.

| Lab | New mechanism | Student comparison |
| --- | --- | --- |
| **00 · Rules, then LLM calls** | A Python rule with reasons, a reply normaliser, unguided model calls | Where does a model without the policy disagree with the rule? |
| **01 · Better prompts and small evaluations** | Guided prompt, JSON parser, five labelled cases, quality gate | Which cases does the guided prompt get right, and which reply breaks the format? |
| **02 · Retrieve architecture rules with RAG** | Score and rank stored policies, abstain, check citations | Which evidence supports the answer, and when should the system abstain? |
| **03 · Architecture tools and our own MCP server** | Read and write MCP tools with schemas and error results | What is read, what state changes, and what happens on a bad call? |
| **04 · ReAct: choose a tool, then decide** | Guarded action/observation loop with a history | Who chooses the next step, and what stops the loop? |
| **05 · A skill for a short architecture decision record** | Skill catalog, progressive disclosure, ADR checker | Which skill fits the task, and what does its output promise? |
| **06 · Delegate an architecture review with A2A** | Propose, review over A2A, revise on feedback | What crosses the agent interface, and how does feedback change the proposal? |
| **07 · A framework for choosing and checking** | Choose-and-check graph with a conditional retry | Which node proposes, which validates, and what ends the loop? |

## Four core areas

| Area | Labs |
| --- | --- |
| LLMs and Prompting · RAG Systems | 00–02 |
| Foundations of AI Agents · Agentic Patterns | 03–04 |
| Tools and MCP · A2A Protocol | 03 & 06 |
| Skills · Frameworks | 05 & 07 |

## Keep reasoning and evaluation observable

Prompt decomposition means checking explicit criteria and asking for a brief, verifiable justification. This is a teaching adaptation inspired by chain-of-thought prompting, not a reproduction of the original method or access to private model reasoning. ReAct-style action and observation comes after students have used tools. Its compact control-flow example illustrates the loop without implementing a full native function-calling agent.

Evaluate three things: adherence to the supplied policy, grounding in the case and retrieved evidence, and the clarity of one consequence or trade-off. The automatic checks cover only part of that assessment. Scripted practice scores demonstrate the evaluation code; only live runs provide evidence about model behavior, and five cases cannot establish general quality.

The RAG retriever uses transparent keyword matching. MCP and A2A use their real SDKs locally; the save action changes only in-memory data. The skills lab chooses from a small in-notebook catalog rather than a full skill host. LangGraph runs an actual two-node graph with a conditional retry. Supporting transport code stays in the installable course package.

See the [instructor guide](instructor-guide.md) and [technical references](sources.md).
