# Curriculum

Eight beginner labs teach general agentic AI through one small software architecture question: **modular monolith or microservices?** Keep the case familiar while changing one mechanism at a time.

Each worked example takes **5–10 minutes**, plus first-run installation. There are at most **20 main Python lines**, two main code blocks, one check, and one small exercise. The whole notebook stays within **25 Python lines including setup**. Students need basic Python. Discussion and paired practice can extend a class to 60–90 minutes.

## The shared case

A three-person team has no independent deployment requirement. Our fictional course policy chooses microservices only when `team_size >= 8` **and** `independent_deploys` is true; otherwise it chooses a modular monolith.

This deliberately small policy makes comparisons easy. It is not a real-world architecture prescription: deployment boundaries, ownership, reliability, cost, and operational maturity need richer analysis.

## Eight steps

| Lab | New mechanism | Student comparison |
| --- | --- | --- |
| **00 · Rules and a first LLM call** | Python baseline, then one prompt | Does the model match the rule without being given it? |
| **01 · Better prompts and evaluation** | Explicit criteria, a worked example, JSON, three cases | Does a clearer prompt follow the supplied policy? |
| **02 · RAG for architecture rules** | Retrieve a policy record before generation | Which source supports the answer? |
| **03 · Tools and MCP** | Build a metrics reader and an in-memory save action | What is read, and what state changes? |
| **04 · Agent foundations and patterns** | Bounded ReAct-style action/observation loop | Who chooses the next step, and what stops the loop? |
| **05 · Reusable architecture skills** | Small ADR-writing SKILL.md | Which procedure can be reused for a new case? |
| **06 · A2A architecture review** | Discover and message a reviewer agent | What proposal crosses the agent interface? |
| **07 · Frameworks and a final check** | Two-node LangGraph choose-and-check workflow | Which node proposes, and which validates? |

## Four core areas

| Area | Labs |
| --- | --- |
| LLMs and Prompting · RAG Systems | 00–02 |
| Foundations of AI Agents · Agentic Patterns | 03–04 |
| Tools and MCP · A2A Protocol | 03 & 06 |
| Skills · Frameworks | 05 & 07 |

## Keep reasoning and evaluation observable

Prompt decomposition means checking explicit criteria and asking for a brief, verifiable justification. This is a teaching adaptation inspired by chain-of-thought prompting, not a reproduction of the original method or access to private model reasoning. ReAct-style action and observation comes after students have used tools. Its compact control-flow example illustrates the loop without implementing a full native function-calling agent.

Evaluate three things: adherence to the supplied policy, grounding in the case and retrieved evidence, and the clarity of one consequence or trade-off. The tiny automatic checks cover only part of that assessment. Scripted practice scores demonstrate the evaluation code; only live runs provide evidence about model behavior, and three cases cannot establish general quality.

The RAG retriever uses transparent keyword matching. MCP and A2A use their real SDKs locally; the save action changes only in-memory data. The ADR example loads instructions directly rather than implementing an automatic skill host. LangGraph runs an actual two-node workflow. Supporting transport code stays in the installable course package.

See the [instructor guide](instructor-guide.md) and [technical references](sources.md).
