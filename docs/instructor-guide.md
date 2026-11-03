# Instructor guide

Use the same small architecture case throughout. Students spend their attention on the new agentic AI mechanism instead of learning a new domain story in every lab. Each example has at most **20 main Python lines**, two main code blocks, one check, and one exercise. Allow **5–10 minutes**, plus first-run setup.

## Before teaching

Run the checks in the [README](../README.md), then open the notebooks in Colab. One setup cell installs `coursekit` from a pinned public GitHub revision. Protocol and framework lessons also install the relevant SDK. Supporting transport code is in that package.

The starting case has `team_size=3` and `independent_deploys=False`. The fictional policy chooses microservices only for a team of at least eight people that also needs independent deployments; otherwise it chooses a modular monolith. Explain that this is a teaching fixture. Ask students which real architecture concerns this rule omits.

Test one small live call with student-equivalent access. Defaults: FreeInference, `qwen3.6-35b`, and Colab Secret `FREEINFERENCE_API_KEY`. Service, model, and secret name are configurable. Verify current access and quotas; keep keys out of code and outputs.

## A short teaching rhythm

1. Predict the output for the shared case.
2. Run the example and its check.
3. Change one requirement or input.
4. Explain the new result and one consequence.
5. Compare with the earlier, simpler approach.

A 60–90 minute session can add paired practice, discussion, and optional live runs. Keep the introductory example small.

## One question per lab

| Lab | Ask |
| --- | --- |
| 00 | When is the Python rule sufficient, and why might the unguided model disagree? |
| 01 | Which prompt change helped, and which test case could reveal a mistake? |
| 02 | Which stored rule was retrieved, and what happens when no rule matches? |
| 03 | Which tool extracts information, and which tool changes state? |
| 04 | What action did the model choose, what did it observe, and why did it stop? |
| 05 | Which ADR instruction stays the same when the case changes? |
| 06 | What did the reviewer receive, and why did it accept or reject the proposal? |
| 07 | What is stored in graph state, and what does the check leave unassessed? |

## Evaluate useful behavior

Use a small rubric: **policy adherence**, **grounding in supplied facts**, and **one clear consequence**. A matching label is only the first check. For prompting, inspect the three cases and add a boundary or counterexample. For RAG, inspect the retrieved record. For tools and agent loops, inspect the action, observation, state change, and stop condition.

Practice replies and scores are scripted; they test the exercise’s plumbing, not an LLM. Run the same cases live before drawing conclusions about prompting. With a tiny test set, describe observed results rather than claiming general model accuracy.

For chain-of-thought-style prompting, teach explicit criterion checks and brief justifications. This is a teaching adaptation, not a reproduction of the original CoT method or access to private reasoning. ReAct-style loops make actions and observations visible after the tools lesson; the compact control-flow adaptation still needs allowed actions and a turn limit.

For a formative submission, request one changed input, its result, and two sentences explaining whether the policy was followed and what a real architect would still investigate. Reward a useful comparison, not extra code.

## Keep the implementation honest

The MCP lab builds its own small server and makes fixed client calls. The next lab adds model-selected actions. MCP’s save action changes an in-memory list only. A2A’s deterministic reviewer uses real local protocol routes and needs no live model. The skill example applies instructions directly. These boundaries let students distinguish data, actions, agent messages, reusable procedures, and orchestration.

Parallel workers, larger skill catalogs, production hosting, vector databases, and larger evaluation suites can follow once the tiny examples are clear. Continue with the linked learning resources.
