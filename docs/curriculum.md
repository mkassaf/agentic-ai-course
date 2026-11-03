# Curriculum

Eight introductory labs teach general agentic AI through small, inspectable examples. Students should know basic Python. Allow **60–90 minutes per session**, or **8–12 contact hours** in total. Each worked example should take only a few minutes to read and run; the remaining time is for explanation, prediction, modification, and discussion.

## Four core areas

| Area | Labs | Central question |
| --- | --- | --- |
| LLMs and Prompting · RAG Systems | 00–01 | How do we ask clearly and supply useful evidence? |
| Foundations of AI Agents · Agentic Patterns | 02–03 | How do we control a sequence of model decisions? |
| Tools and MCP · A2A Protocol | 04–05 | How do capabilities and agents connect through standard interfaces? |
| Skills · Frameworks | 06–07 | How do we package procedures and organize a larger workflow? |

## Lab sequence

| Lab | Learn | Small example | Student check |
| --- | --- | --- | --- |
| **00 · LLMs and prompting** | Messages, clear task/context/format, few-shot prompting, structured output | Write a short customer-support reply | Change tone; check format and avoid invented facts |
| **01 · RAG systems** | Retrieval, context assembly, source IDs, missing information | Answer a library-hours question from a few notes | Add a note; test an unsupported question |
| **02 · Foundations of AI agents** | State, actions, observations, allowed tools, stopping | Let an assistant perform one lookup | Lower the step budget; reject an unknown action |
| **03 · Agentic patterns** | Chaining, routing, parallelization, critique/revision | Route a short message and compare small workflows | Add a category; count calls and inspect outputs |
| **04 · Tools and MCP** | Tools versus protocol, client/server discovery and invocation | Discover and call `lookup_note(topic)` through the MCP SDK | Inspect the input schema; reject a missing argument |
| **05 · A2A protocol** | Agent Card, capability discovery, messages and responses | Discover a greeting agent and send `Ada` | Expect `Hello, Ada!`; inspect identifiers and text parts |
| **06 · Agent skills** | SKILL.md metadata, reusable instructions, progressive loading | Package a short note-summary procedure | Change the output format without embedding the task input |
| **07 · Frameworks and evaluation** | State, nodes, edges, LangGraph, simple baselines | A classify-and-reply graph | Compare the graph with the same plain-Python steps |

## What students should be able to explain

By the end, students should distinguish a model call, workflow, and agent loop; trace a tool call; identify what retrieval contributes; and explain why the host program validates inputs and bounds execution. They should also distinguish **MCP** (tools/context), **A2A** (agent communication), **skills** (packaged procedural guidance), and **frameworks** (implementation and orchestration building blocks).

These are related layers, not interchangeable labels. A local SDK example teaches an interface; it does not teach production hosting, authorization, or every feature in the protocol. A skill supplies instructions; it does not guarantee correct execution. A framework organizes code; it does not establish that the resulting system is better.

## Keep the examples small

Introduce one familiar task at a time. Show the shortest useful call sequence first; leave server setup and shared helpers collapsed. Ask students to predict one result, run the example, change one input, and explain one limitation. Use optional extension tasks only after the main example is clear.

Practice mode uses visible scripted responses. It provides stable checks for control flow. Live mode sends the actual prompts to the selected API and may produce different answers or fail validation. Neither a passing toy example nor a plausible model response establishes general quality.

## Teaching pattern

1. Explain the idea in plain language.
2. Draw the short control flow.
3. Predict the expected result.
4. Run the worked example.
5. Make one small change and check it.
6. Explain when this building block is useful.

See the [instructor guide](instructor-guide.md) for a suggested class structure and [technical references](sources.md) for further reading.
