# Instructor guide

Teach one small mechanism at a time. Each lab’s main example has at most **20 visible Python lines**, two main code blocks, one check, and one exercise. Allow **5–10 minutes** to work through it, plus first-run setup.

## Before teaching

Run the checks in the [README](../README.md), then open the notebooks in Colab. The single setup cell installs `coursekit` from a pinned public GitHub revision. Protocol and framework lessons also install their relevant SDK. Supporting runtime/server code is in that package, outside the notebooks.

Test one small live call with student-equivalent access. The defaults use FreeInference, `qwen3.6-35b`, and Colab Secret `FREEINFERENCE_API_KEY`. The service, model, and secret name are configurable. Verify current access and quotas; keep keys out of code and outputs.

## A short teaching rhythm

1. Explain the idea in one sentence.
2. Predict the example’s output.
3. Run the short example and its one check.
4. Make the requested small change.
5. Ask the student to explain what changed.

A longer 60–90 minute class can include discussion, paired practice, and optional live runs. Avoid expanding the introductory notebook into a large project.

## One question per lab

| Lab | Ask |
| --- | --- |
| 00 | What changed when you edited the prompt? |
| 01 | Which note supplied the answer? |
| 02 | What happened after the lookup, and what stopped the loop? |
| 03 | What crossed the MCP tool interface? |
| 04 | How is a chain different from a router? |
| 05 | What message did the greeter receive and return? |
| 06 | Which instruction came from SKILL.md? |
| 07 | What did each of the two graph nodes do? |

For a small formative submission, ask for the changed example, its result, and two sentences explaining it. Check understanding rather than rewarding extra code.

## Further reading comes later

Parallelization, reflection, orchestration, full skill catalogs, production protocol hosting, and evaluation harnesses belong after the tiny examples are clear. The resource links provide places to continue. MCP and A2A examples use actual SDKs; their simple deterministic lookup/greeting behavior does not require a live model call.
