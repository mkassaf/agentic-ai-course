# Instructor guide

## Before the first class

Run the verification commands in the README. Then use a student-equivalent university account to test one ordinary call, one JSON response, and the configured output-token field. Confirm all three live council models are available, belong to different verified model families, and can be reached from a Colab CPU runtime. A different role prompt or deployment alias is not a different model family.

The initial model is FreeInference `qwen3.6-35b`. Provide its key through Colab Secrets named `FREEINFERENCE_API_KEY`; use `SECRET_NAME` to choose another secret. Endpoint and model settings remain configurable for other services. Give students the approved model IDs, family mapping, token parameter, key instructions, quotas, and support contact through your university channel. Keep credentials out of GitHub and notebook outputs. Use provider-side quota controls as well as the example's call budget: rerunning a cell creates a new client and can reset its in-memory counter.

Choose whether notebook exercises are formative or graded, agree with the professor on the final rubric, and publish the submission policy. The suggested marks below are teaching proposals; they do not change the assignment supplied by the professor.

## A repeatable 90-minute class

| Minutes | Activity | Instructor action |
| --- | --- | --- |
| 0–10 | Recall and prediction | Ask students to predict what will fail before running code. |
| 10–25 | Explain and trace | Draw the control flow, identify which decisions the model makes. |
| 25–45 | Worked example | Run practice first, then a short live run with the university API. |
| 45–70 | Student task | Students modify the example and add or exercise a failure case. |
| 70–85 | Compare and discuss | Inspect outputs and traces; compare quality with calls and latency. |
| 85–90 | Exit ticket | Ask for one limitation and one connection to the final project. |

For a 60-minute session, move the live comparison or extension exercise to homework. Eight 60–90 minute sessions provide 8–12 contact hours; extensive capstone development happens outside these labs.

## Suggested formative assessment

Each lab submission should include a modified notebook, one relevant successful test, one failure case, and a short explanation of the observed behavior. Prefer explanations and evidence over matching a particular model's prose.

| Criterion | Suggested share | Evidence |
| --- | --- | --- |
| Correct control flow and contracts | 35% | Inspectable code, bounded loops, validated messages. |
| Tests and failure handling | 25% | Checks that catch a realistic error, with a justified expected result. |
| Experimental reasoning | 25% | Fair comparison, trace, limitations, no unsupported improvement claim. |
| Explanation and project transfer | 15% | Student can explain decisions and what the capstone still needs. |

Suggested exit tickets: Lab 00—why is one completion not an autonomous agent? Lab 01—can valid JSON still be wrong? Lab 02—does a source ID prove a claim is supported? Lab 03—who executes the tool? Lab 04—what makes a workflow different from an agent? Lab 05—when should revision stop? Lab 06—why is a majority vote not human approval? Lab 07—why must feedback and test data be separate?

## Assess the project empirically

The assignment's claim that a council may improve decisions is a hypothesis. A well-designed experiment that finds no gain, regression, or an unjustified cost increase is useful evidence. Do not reward a fabricated positive result.

Measure agreement with expert decisions, trade-off coverage, evidence support, calls/token usage, cost where pricing is known, latency, and error/abstention rates. Architecture questions can have several defensible choices: use expert-reviewed acceptable alternatives and a rubric rather than a single answer string alone. The lab's tiny exact-match demonstration is only a way to learn experiment mechanics.

Use the same scenario, knowledge snapshot, and constraints for each model-alone baseline and the council. Compare the council to **each** single model and the best one. Also consider an additional-call or equal-budget baseline so that model coordination is not confused with merely spending more inference. Report the resource difference even when budgets cannot be equalized.

For feedback experiments, freeze a held-out set before developing feedback memory. Keep its labels away from prompts, retrieval, memory updates, and any judge used to give feedback. Compare before/after against that frozen set, then avoid repeatedly tuning on those test outcomes. Reserve a final untouched set when iterating. The project calls for 20+ expert-answered scenarios; the notebooks intentionally use only a few toy cases.

## Optional extensions

After students can explain the plain Python implementation, replace the loop with a graph orchestration framework, wrap a local tool with MCP, or compare an A2A interface with the in-process message schema. Ask students to state which interoperability problem each protocol solves. Neither protocol is a requirement of these introductory labs, and neither creates intelligent behavior by itself.

Useful follow-ups include a retrieval failure benchmark, disagreement analysis, persistent feedback memory with provenance, and a fairness analysis of the chair's tie-break rule. Add one dimension at a time and keep the original baseline.
