# Instructor guide

The course introduces **general agentic AI** through small, understandable mechanisms. Use familiar examples and introduce one new building block at a time.

## Prepare once

Run the verification commands in the [README](../README.md). Open every notebook in Colab using a student-equivalent account. Run one live prompt with the intended API, then check the SDK setup cells in the MCP, A2A, and LangGraph labs. Package installation needs internet access even when the model examples run in practice mode.

The initial service is FreeInference at `https://freeinference.org/v1`, model `qwen3.6-35b`. Provide a credential privately and store it under Colab Secret `FREEINFERENCE_API_KEY`. `BASE_URL`, `MODEL`, and `SECRET_NAME` are configurable for another compatible service. Confirm current access, quotas, and model support; no particular free allowance is promised.

Use provider-side quota controls alongside the notebook’s call budget. Re-running a setup cell can reset an in-memory counter. Never place keys in code, screenshots, saved outputs, or the public repository.

## A simple class rhythm

| Minutes | Activity |
| --- | --- |
| 0–10 | Recall one previous idea and predict the new example’s output |
| 10–20 | Explain the concept and draw the short flow |
| 20–35 | Run and inspect the small worked example |
| 35–55 | Change one input or add one small behavior |
| 55–60 | Explain the result and one limitation |
| Optional extra 30 | Compare live outputs, discuss a failure, or try an extension |

Avoid beginning with all the shared runtime or server boilerplate. Keep it available in a collapsed cell, explain its purpose, and use the small main example to show the new concept. Students can inspect the implementation after they understand the flow.

## One teaching question per lab

| Lab | Ask students |
| --- | --- |
| 00 | Which part of your prompt changed the output, and which facts did you actually supply? |
| 01 | Was the wrong answer caused by retrieval or generation? |
| 02 | Who decides which actions may execute, and what stops the loop? |
| 03 | Which part of the process is fixed in code, and which part does the model choose? |
| 04 | What did MCP add beyond calling the Python function directly? |
| 05 | What does an Agent Card tell a client, and what does a message carry? |
| 06 | Which information belongs in a reusable skill, and which belongs in the current request? |
| 07 | What changed when the same steps became graph nodes? How did you check the result? |

## Small formative submissions

Ask for the modified notebook, one expected result, one relevant check, and a short explanation. A useful lightweight rubric is:

| Criterion | Suggested share |
| --- | --- |
| Student can explain the main control flow | 35% |
| The small modification works and has a meaningful check | 35% |
| Student identifies a limitation or failure case | 20% |
| Notebook is readable and reproducible | 10% |

Do not grade a particular wording from a live model. Distinguish deterministic protocol checks from subjective answer quality. Model comparisons should use the same input and evidence, and report the resource difference. A tiny classroom test set is an illustration of evaluation, not a claim about general performance.

## Keep the layers clear

- **MCP:** access to tools and context through a standard interface. Lab 04 uses the official SDK, discovery, and a tool call.
- **A2A:** capability discovery and messages between agent interfaces. Lab 05 uses the official SDK and a tiny greeting exchange.
- **Skills:** reusable procedural instructions and optional supporting resources. They do not themselves execute a tool or enforce a permission.
- **Frameworks:** state and orchestration abstractions. Lab 07 uses actual LangGraph while preserving a plain-Python comparison.

The protocol demos intentionally avoid live model calls so students can observe the interface without model variability. They do not cover production deployment or every protocol capability. Add those topics only after students can follow the small example.
