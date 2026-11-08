# Instructor guide

Use the same small architecture case throughout. Students spend their attention on the new agentic AI mechanism instead of learning a new domain story in every lab. Each lab has two to five numbered steps (one code cell each, at most **20 lines**), a check, and small exercises. Allow **15–20 minutes**, plus first-run setup.

## Before teaching

Run the checks in the [README](../README.md), then open the notebooks in Colab. One setup cell installs `coursekit` from a pinned public GitHub revision. The RAG and memory lessons install Chroma and download a small embedding model on first run; protocol and framework lessons install the relevant SDK. Supporting transport code is in that package.

The labs share four fictional projects, one for each combination of the two facts. Lab 00 starts with the Course portal: `team_size=3` and `independent_deploys=False`. The fictional policy chooses microservices only for a team of at least eight people that also needs independent deployments; otherwise it chooses a modular monolith. Explain that this is a teaching fixture. Ask students which real architecture concerns this rule omits.

For evaluation (Lab 09), MLflow tracks experiments locally. Lab 09 installs `mlflow` on first run and logs parameters and metrics to `file:///tmp/mlruns`. Students can open the UI with `mlflow ui --port 5000` and view the side-by-side comparison at `localhost:5000`. This is separate from LangSmith (Lab 07), which traces agent runs; MLflow logs experiment results. Test one run in the notebook before class to verify the install and UI work.

Test one small live call with student-equivalent access. Defaults: FreeInference, `qwen3.6-35b`, and Colab Secret `FREEINFERENCE_API_KEY`. Service, model, and secret name are configurable. Verify current access and quotas; keep keys out of code and outputs.

Gemini (`GEMINI_API_KEY`) and DeepSeek (`DEEPSEEK_API_KEY`) are built in as well: students set `PROVIDER` in the setup cell. The council lab (06) needs three model families in live mode, so it uses FreeInference (Qwen), DeepSeek, and Gemini together, and students need all three keys. FreeInference's free tier takes one request at a time (the course client queues the rest). Check each provider's pricing and quotas before class.

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
| 2 | 03 Prompt chaining · 04 Tools · 05 ReAct | Chain, call tools, act |
| 3 | 06 Multi-agent debate · 07 Observability and tracing · 08 Human-in-the-loop and memory | Debate, trace, decide |

A plan for each lecture:

| Minutes | Activity |
| --- | --- |
| 0–10 | Introduce the lecture's idea and the case. In Lecture 1, open Colab and save a copy first. |
| 10–30 | First lab: predict, run, check. |
| 30–50 | Second lab. |
| 50–75 | Third lab. In Lecture 1 it is one of the longest (02 has five steps). |
| 75–90 | Discussion of the lecture's question, one live-mode run if time allows, and the self-study pointer. |

Lecture 3 is the fullest: Labs 06, 07, and 08 have five steps each. Use this plan instead:

| Minutes | Activity |
| --- | --- |
| 0–5 | Introduce multi-agent debate and the Payments case. Students open Lab 08 in a second tab and run its setup cell now, so its packages install in the background; its Step 3 downloads an 80 MB embedding model, so warn them it takes a minute. |
| 5–30 | Lab 06 in practice mode. In class: *Try it* 1 and 3. |
| 30–55 | Lab 07. In class: *Try it* 1 and 2 (a broken message, then count from the logs). |
| 55–80 | Lab 08. In class: *Try it* 1 and 2. |
| 80–90 | Discussion: who said what, based on what, and who has the final word? Then the self-study pointer. |

Homework for Lecture 3: Lab 06 *Try it* 2, 4, and 5; Lab 07 *Try it* 3 to 7, including the LangSmith trace; Lab 08 *Try it* 3 to 5.

Keep the *Try it* exercises that need live mode, and the last one or two exercises of each lab, as homework. After Lecture 2, point students to self-study Labs 11 (MCP) and 13 (A2A); after Lecture 3, to Labs 09 (evaluation against single models), 10 (routing), 12 (skills), and 14 (LangGraph), and to Labs 15 (framing and the message contract), 16 (the learning curve), and 17 (the weighted decision matrix) before the project starts. The curriculum's *Project readiness* table maps every requirement of the brief to a lab. Each self-study lab ends with a challenge that applies it to the student's own council, which is a natural first project milestone.

## One question per lab

| Lab | Ask |
| --- | --- |
| 00 | Where does the model without the policy disagree with the rule, and why are those the mixed cases? |
| 01 | Which part of the guided prompt removes Lab 00's guesswork, and which test case could reveal a mistake? |
| 02 | Why do embeddings find R1 for the reworded question when word matching does not, and why does the lunch question get no answer? |
| 03 | What does each link of the chain receive, and what can a gate check that a single prompt hides? |
| 04 | Why did the model guess without a tool, what does `call_tool` check, and why must a write wait for the user? |
| 05 | Which actions did the model choose, what did it observe, and which guard would stop a bad run? |
| 06 | Why must the architects propose alone first, which claim was challenged, and why was the dissent kept? |
| 07 | What do the live log and `council.log` show, which sources does the decision rest on, and what changed in the code when the Rulebook joined? |
| 08 | Which reason did the human give, which new case recalled it, and why did the lesson apply to only one of them? |
| 09 | Which system is the baseline, where does the council win, at what cost, and why do we check the judge against a human? |
| 10 | Which case did the router send where, which mistake is costlier, and when does a router cost more than no router? |
| 11 | Which tool reads, which tool changes state, and why does a rejected call leave the state unchanged? |
| 12 | What did the model see when it chose a skill, and what did it see only afterwards? |
| 13 | What did the reviewer receive, and how did its feedback change the proposal? |
| 14 | What is stored in graph state, what decides between retrying and finishing, and what does the check leave unassessed? |
| 15 | Which scenario has a number you can check, and what does the contract let you change without touching the council's code? |
| 16 | Why must feedback and test cases stay apart, when does the curve rise, and why does a coin toss get no vote? |
| 17 | Which decision model hides its assumptions, and which single weight flips the winner when the scores do not change? |

## Evaluate useful behavior

Use a small rubric: **policy adherence**, **grounding in supplied facts**, and **one clear consequence**. A matching label is only the first check. For prompting, inspect the five cases and add a boundary or counterexample. For RAG, inspect the distances and the retrieved policies. For tools and agent loops, inspect the action, observation, state change, and stop condition.

Practice replies and scores are scripted; they test the exercise’s plumbing, not an LLM. Run the same cases live before drawing conclusions about prompting. With a small test set, describe observed results rather than claiming general model accuracy.

For chain-of-thought-style prompting, teach explicit criterion checks and brief justifications. This is a teaching adaptation, not a reproduction of the original CoT method or access to private reasoning. ReAct-style loops make actions and observations visible after the tools lesson; the compact control-flow adaptation still needs allowed actions and a turn limit.

For a formative submission, request one changed input, its result, and two sentences explaining whether the policy was followed and what a real architect would still investigate. Reward a useful comparison, not extra code.

## Keep the implementation honest

The self-study MCP lab builds its own small server and makes fixed client calls; Labs 04 and 05 have already shown model-selected tools. MCP’s save action changes an in-memory dictionary only. A2A’s reviewer is deterministic and uses real local protocol routes; the proposer is the course model, scripted in practice mode. The skills lab chooses from a small in-notebook catalog instead of a full skill host. The decision-model lab computes its weighted matrix entirely in plain code and uses the TypeSafe SDK only for the optional live scoring step, so the arithmetic holds with no model key. These boundaries let students distinguish data, actions, agent messages, reusable procedures, and orchestration.

The council labs keep the chair in plain code and replace Lab 06's council with one call in Lab 08, so each pattern stays visible. Larger skill catalogs, production hosting, persistent vector databases, and benchmarks of 20 or more scenarios can follow once these examples are clear. Continue with the linked learning resources.
