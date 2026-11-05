# Instructor guide

Use the same small architecture case throughout. Students spend their attention on the new agentic AI mechanism instead of learning a new domain story in every lab. Each lab has two to five numbered steps (one code cell each, at most **20 lines**), a check, and small exercises. Allow **15–20 minutes**, plus first-run setup.

## Before teaching

Run the checks in the [README](../README.md), then open the notebooks in Colab. One setup cell installs `coursekit` from a pinned public GitHub revision. The RAG and memory lessons install Chroma and download a small embedding model on first run; protocol and framework lessons install the relevant SDK. Supporting transport code is in that package.

The labs share four fictional projects, one for each combination of the two facts. Lab 00 starts with the Course portal: `team_size=3` and `independent_deploys=False`. The fictional policy chooses microservices only for a team of at least eight people that also needs independent deployments; otherwise it chooses a modular monolith. Explain that this is a teaching fixture. Ask students which real architecture concerns this rule omits.

Test one small live call with student-equivalent access. Defaults: FreeInference, `qwen3.6-35b`, and Colab Secret `FREEINFERENCE_API_KEY`. Service, model, and secret name are configurable. Verify current access and quotas; keep keys out of code and outputs.

Gemini (`GEMINI_API_KEY`) and DeepSeek (`DEEPSEEK_API_KEY`) are built in as well: students set `PROVIDER` in the setup cell. The council lab (05) needs three model families in live mode, so it uses FreeInference (Qwen), DeepSeek, and Gemini together, and students need all three keys. FreeInference's free tier takes one request at a time (the course client queues the rest). Check each provider's pricing and quotas before class.

## A short teaching rhythm

1. Predict the output for the shared case.
2. Run the example and its check.
3. Change one requirement or input.
4. Explain the new result and one consequence.
5. Compare with the earlier, simpler approach.

Every notebook has the same shape: **So far / New** (the one idea added since the previous lab), setup, two to five numbered steps, *What you should see*, *Try it*, and a *Takeaway*. Students can predict where to look in each lab.

Each step adds one piece of logic, so students can stop after any step and still have working code.

## Three 90-minute lectures

| Lecture | Labs | Theme |
| --- | --- | --- |
| 1 | 00 Rules and LLM calls · 01 Prompts and evaluation · 02 RAG | Ask, check, retrieve |
| 2 | 03 Prompt chaining · 04 ReAct with tools · 05 The council | Chain, act, debate |
| 3 | 06 Human and memory · 07 Routing · 08 Evaluating the council | Decide, learn, measure |

A plan for each lecture:

| Minutes | Activity |
| --- | --- |
| 0–10 | Introduce the lecture's idea and the case. In Lecture 1, open Colab and save a copy first; in Lecture 3, mention that Lab 06 downloads an 80 MB embedding model. |
| 10–30 | First lab: predict, run, check. |
| 30–50 | Second lab. |
| 50–75 | Third lab, the longest of the three (02, 05, and 08 each have five steps). |
| 75–90 | Discussion of the lecture's question, one live-mode run if time allows, and the self-study pointer. |

Keep the *Try it* exercises that need live mode, and the last one or two exercises of each lab, as homework. After Lecture 2, point students to self-study Labs 09 (MCP) and 11 (A2A); after Lecture 3, to Labs 10 (skills) and 12 (LangGraph), and to Labs 13 (framing and the message contract) and 14 (the learning curve) before the project starts. The curriculum's *Project readiness* table maps every requirement of the brief to a lab. Each self-study lab ends with a challenge that applies it to the student's own council, which is a natural first project milestone.

## One question per lab

| Lab | Ask |
| --- | --- |
| 00 | Where does the model without the policy disagree with the rule, and why are those the mixed cases? |
| 01 | Which part of the guided prompt removes Lab 00's guesswork, and which test case could reveal a mistake? |
| 02 | Why do embeddings find R1 for the reworded question when word matching does not, and why does the lunch question get no answer? |
| 03 | What does each link of the chain receive, and what can a gate check that a single prompt hides? |
| 04 | Which actions did the model choose, what did it observe, and which guard would stop a bad run? |
| 05 | Why must the architects propose alone first, which claim was challenged, and why was the dissent kept? |
| 06 | Which reason did the human give, which new case recalled it, and why did the lesson apply to only one of them? |
| 07 | Which case did the router send where, which mistake is costlier, and when does a router cost more than no router? |
| 08 | Which system is the baseline, where does the council win, at what cost, and why do we check the judge against a human? |
| 09 | Which tool reads, which tool changes state, and why does a rejected call leave the state unchanged? |
| 10 | What did the model see when it chose a skill, and what did it see only afterwards? |
| 11 | What did the reviewer receive, and how did its feedback change the proposal? |
| 12 | What is stored in graph state, what decides between retrying and finishing, and what does the check leave unassessed? |
| 13 | Which scenario has a number you can check, and what does the contract let you change without touching the council's code? |
| 14 | Why must feedback and test cases stay apart, when does the curve rise, and why does a coin toss get no vote? |

## Evaluate useful behavior

Use a small rubric: **policy adherence**, **grounding in supplied facts**, and **one clear consequence**. A matching label is only the first check. For prompting, inspect the five cases and add a boundary or counterexample. For RAG, inspect the distances and the retrieved policies. For tools and agent loops, inspect the action, observation, state change, and stop condition.

Practice replies and scores are scripted; they test the exercise’s plumbing, not an LLM. Run the same cases live before drawing conclusions about prompting. With a small test set, describe observed results rather than claiming general model accuracy.

For chain-of-thought-style prompting, teach explicit criterion checks and brief justifications. This is a teaching adaptation, not a reproduction of the original CoT method or access to private reasoning. ReAct-style loops make actions and observations visible after the tools lesson; the compact control-flow adaptation still needs allowed actions and a turn limit.

For a formative submission, request one changed input, its result, and two sentences explaining whether the policy was followed and what a real architect would still investigate. Reward a useful comparison, not extra code.

## Keep the implementation honest

The self-study MCP lab builds its own small server and makes fixed client calls; Lab 04 has already shown model-selected actions. MCP’s save action changes an in-memory dictionary only. A2A’s reviewer is deterministic and uses real local protocol routes; the proposer is the course model, scripted in practice mode. The skills lab chooses from a small in-notebook catalog instead of a full skill host. These boundaries let students distinguish data, actions, agent messages, reusable procedures, and orchestration.

The council labs keep the chair in plain code and replace Lab 05's council with one call in Lab 06, so each pattern stays visible. Larger skill catalogs, production hosting, persistent vector databases, and benchmarks of 20 or more scenarios can follow once these examples are clear. Continue with the linked learning resources.
