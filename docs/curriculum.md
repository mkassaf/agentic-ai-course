# Curriculum

Eight beginner labs introduce general agentic AI through tiny examples. Each main example takes **5–10 minutes**, plus first-run package installation, and contains at most **20 visible Python lines** in at most **two main code blocks**. Each lab has one check and one exercise. Students need basic Python.

A class may spend 60–90 minutes on discussion and optional practice; that is not the time needed to read the short example.

## Four core areas

| Area | Labs |
| --- | --- |
| LLMs and Prompting · RAG Systems | 00–01 |
| Foundations of AI Agents · Agentic Patterns | 02 & 04 |
| Tools and MCP · A2A Protocol | 03 & 05 |
| Skills · Frameworks | 06–07 |

## Tiny examples

| Lab | Example | One small change |
| --- | --- | --- |
| **00 · LLMs and prompting** | One support-reply call | Edit the tone in the prompt |
| **01 · RAG systems** | A question answered from two short notes | Change an opening time |
| **02 · Foundations of AI agents** | One lookup in a bounded loop | Change the requested fact |
| **03 · Tools and MCP** | One lookup tool through MCP | Request another topic |
| **04 · Agentic patterns** | A chain and a router as microexamples | Change the message category |
| **05 · A2A protocol** | One Hello exchange | Replace Ada with your name |
| **06 · Agent skills** | Read and apply short SKILL.md instructions | Change the requested summary length |
| **07 · Frameworks** | An actual two-node LangGraph workflow | Change the input message |

## Keep the mechanism visible

Each notebook has one setup cell. It installs reusable course helpers from a pinned public GitHub revision, plus the relevant SDK for protocol/framework examples. Runtime, client, and server boilerplate lives in the package rather than inside the notebook.

Teach the short example first: predict its output, run it, check one result, then change one input. Keep parallelization, reflection, orchestration, larger skill catalogs, and evaluation harnesses as further reading. The introductory examples do not need them.

Students should be able to distinguish a model call, an agent loop, a tool interface, an agent message, skill instructions, and graph nodes. A check demonstrates one expected behavior; it does not establish general model quality.

See the [instructor guide](instructor-guide.md) and [technical references](sources.md).
