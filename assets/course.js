'use strict';
const labs = [
  {
    "id": "00",
    "file": "00_rules_and_llms",
    "title": "From rules to LLM calls",
    "subtitle": "A Python rule on four projects, then a model's guesses",
    "topics": "rules llm prompt architecture monolith microservices baseline",
    "idea": "Write the policy as a function that explains its answer, then see where a model that never saw the policy disagrees.",
    "objectives": [
      "Write a rule that returns a decision and a reason.",
      "Turn free-text model replies into labels.",
      "Count how often a model agrees with the rule."
    ],
    "example": "Run the policy on four projects that cover every combination of the two facts, then ask a model about the same projects.",
    "exercise": "Add an 8-person project with independent deploys, then test the boundary by changing >= to >.",
    "checks": "Only the Payments platform gets microservices. The scripted model agrees on 2 of 4 projects and gets both mixed cases wrong.",
    "bridge": "A disagreement shows what the model is missing: the policy itself.",
    "track": "lecture-1",
    "steps": 4,
    "patterns": [],
    "background": [
      "For decades, software made decisions with rules that people wrote by hand: if this, then that. The expert systems of the 1970s and 1980s stored hundreds of such rules, for example to suggest treatments for infections or to configure computer orders. Rules are exact, fast, and easy to audit. But every case must be foreseen, and someone must write and maintain every rule.",
      "Machine learning changed where a decision comes from: instead of writing the rule, we show a model many examples, and it learns the pattern. Large language models (LLMs) go further. Trained on a vast amount of text, they can answer questions that nobody wrote a rule for, in plain language. The price is that their answers are plausible, not guaranteed, and an LLM does not know your organisation's policy unless you tell it.",
      "This course keeps both. The rule is a reference that we can check a model against, and the model handles what a rule cannot express. Lab 00 puts them side by side on one question."
    ],
    "terms": [
      [
        "Rule-based system",
        "A program whose decisions come from rules that people wrote explicitly."
      ],
      [
        "Large language model (LLM)",
        "A model trained on large amounts of text that continues a prompt with likely text."
      ],
      [
        "Prompt",
        "The text we send to the model: the instructions, the facts, and the question."
      ],
      [
        "Baseline",
        "A simple reference result that a more advanced system must beat."
      ]
    ]
  },
  {
    "id": "01",
    "file": "01_prompting_evaluation",
    "title": "Prompting and small evaluations",
    "subtitle": "A guided prompt, a strict parser, and a five-case quality gate",
    "topics": "prompting cot criteria few shot json evaluation testing",
    "idea": "Give the model explicit criteria and a worked example, reject badly formatted replies, and score the prompt on labelled cases.",
    "objectives": [
      "Write a precise, structured prompt.",
      "Validate model output before trusting it.",
      "Score a prompt on a labelled test set."
    ],
    "example": "Build a four-part guided prompt, parse its JSON reply, and score it on five cases, including the boundary of exactly 8 people.",
    "exercise": "Fix the scripted mistake, then break the format with an unknown label and watch the quality gate stop the run.",
    "checks": "Four of five scripted replies pass (80%), which just meets the gate. Practice scores test the evaluation code, not model quality.",
    "bridge": "Use checkable criteria and brief justifications; more reasoning text does not prove a better design.",
    "track": "lecture-1",
    "steps": 4,
    "patterns": [],
    "background": [
      "Early work with LLMs was mostly trial and error: change the wording, read one answer, change it again. Two habits turned this into engineering. First, prompts became structured: clear instructions, the relevant policy, a worked example (few-shot prompting), and an exact output format. Second, the output became data: a parser turns a reply into a value that code can check, and a small labelled test set turns \"it looks right\" into a score.",
      "A model's answers vary, so one good answer proves little. A test set with edge cases, such as the boundary of exactly 8 people, shows where a prompt breaks, and a quality gate stops a change that makes things worse. Every later lab keeps this habit: never trust output that you have not checked."
    ],
    "terms": [
      [
        "Few-shot prompting",
        "Including one or more worked examples in the prompt, so the model sees what a good answer looks like."
      ],
      [
        "Structured output",
        "A reply in a fixed format, such as JSON, that code can parse."
      ],
      [
        "Evaluation set",
        "Labelled cases with known answers, used to score a prompt or a system."
      ],
      [
        "Quality gate",
        "A check that stops the run when the score falls below a threshold."
      ]
    ]
  },
  {
    "id": "02",
    "file": "02_rag_systems",
    "title": "RAG: ground answers in retrieved knowledge",
    "subtitle": "Embeddings, a vector database, and grounded answers",
    "topics": "rag retrieval embeddings vectors vector database chroma similarity rules source architecture context retrieval-augmented generation",
    "idea": "Turn policies into embedding vectors, store them in a vector database, retrieve by meaning, and check that the answer cites its evidence.",
    "objectives": [
      "Explain embeddings and compare two with cosine similarity.",
      "Store and query vectors in a vector database.",
      "Abstain when no evidence is close, and check citations."
    ],
    "example": "Embed four policies with all-MiniLM-L6-v2, store them in Chroma, and retrieve R1 for a reworded question that word matching misses.",
    "exercise": "Add a cloud-region question, tighten and loosen the distance threshold, and break a citation.",
    "checks": "The reworded question retrieves R1, the billing question R2, and the lunch question nothing. Both answers are grounded.",
    "bridge": "The same steps scale up: a larger embedding model, a persistent vector database, and many more documents.",
    "track": "lecture-1",
    "pattern": "Retrieval-Augmented Generation",
    "steps": 5,
    "patterns": [
      "Retrieval-Augmented Generation"
    ],
    "background": [
      "An LLM's knowledge is fixed when it is trained, and it never saw your private documents. Pasting every document into every prompt does not scale: a prompt has a size limit (the context window), long prompts cost more, and the model can miss the line that matters. Retrieval-augmented generation (RAG), described by Lewis and colleagues in 2020, splits the work: a retriever finds the few passages that matter, and the model answers from them.",
      "Modern retrieval uses embeddings: lists of numbers that capture meaning, so \"how many engineers\" can match \"8+ people\" without sharing a word. A vector database stores these vectors and finds the nearest ones quickly. RAG also adds new ways to fail, so we check them: a question that retrieves nothing relevant should not be answered, and an answer must cite only the sources it was given."
    ],
    "terms": [
      [
        "Context window",
        "The maximum amount of text a model can read in one call."
      ],
      [
        "Embedding",
        "A vector of numbers that represents the meaning of a text."
      ],
      [
        "Vector database",
        "A store that finds the vectors nearest to a query vector."
      ],
      [
        "Grounded answer",
        "An answer supported by, and citing, the retrieved sources."
      ]
    ]
  },
  {
    "id": "03",
    "file": "03_prompt_chaining",
    "title": "Prompt chaining with quality gates",
    "subtitle": "Requirements, options, trade-offs, and a record, with a gate after each step",
    "topics": "prompt chaining workflow gate requirements options trade-offs adr patterns council single-path planning",
    "idea": "Split one decision into small prompts; each reply feeds the next prompt, and a gate in plain Python stops a bad reply before it spreads.",
    "objectives": [
      "Decompose a decision into a chain of prompts.",
      "Write a gate that checks one step's reply.",
      "Pass each step only what it needs."
    ],
    "example": "Chain four prompts for the Payments platform, whose squads want independent releases while one engineer runs operations.",
    "exercise": "Break the requirements list, drop a trade-off mark, and make the decision name an option that was never proposed.",
    "checks": "Every gate passes, and the record chooses microservices while naming the cost for the one operations engineer.",
    "bridge": "Gates check the shape of each step, not whether the decision is wise; Lab 06 adds architects who disagree.",
    "track": "lecture-2",
    "pattern": "Single-Path Planning",
    "steps": 4,
    "patterns": [
      "Single-Path Planning"
    ],
    "background": [
      "A single prompt that asks for a whole decision hides its reasoning. When the answer is wrong, you cannot tell which part failed. Software engineers handle large problems by decomposition: split the work into steps with clear inputs and outputs. Prompt chaining does the same with an LLM: each prompt does one small job, and its output becomes the input of the next prompt.",
      "A chain is a workflow: our code fixes the steps, and the model only fills them in. That makes it predictable, cheap to debug, and easy to test, because a gate can check every intermediate result. Anthropic's guide \"Building effective agents\" recommends starting with simple workflows like this and adding autonomy only when it is needed. Labs 04 and 05 add that autonomy."
    ],
    "terms": [
      [
        "Workflow",
        "A sequence of steps fixed by code; the model does not choose what happens next."
      ],
      [
        "Decomposition",
        "Splitting a large task into smaller steps with clear inputs and outputs."
      ],
      [
        "Gate",
        "A plain-code check between two steps that stops a bad result from spreading."
      ],
      [
        "Decision record (ADR)",
        "A short note of an architecture decision: its context, the decision, and its consequence."
      ]
    ]
  },
  {
    "id": "04",
    "file": "04_why_tools",
    "track": "lecture-2",
    "pattern": "One-Step Tool Agent",
    "title": "Tool calling: let the model read and change live data",
    "subtitle": "A hotel search tool and a booking tool, step by step",
    "topics": "tools tool calling function calling hotel search booking read write confirmation live data one-step tool agent",
    "idea": "A model knows only its training and its prompt; tools let it read live data and change it, while our code checks every request.",
    "objectives": [
      "Explain why a model needs tools for live data.",
      "Describe tools and check every tool request.",
      "Separate read tools from write tools that need confirmation."
    ],
    "example": "A hotel booking system: the model guesses whether Harbor View has a room, then searches the live data and books the Alfama Inn after the user confirms.",
    "exercise": "Close a hotel, request an unknown tool, send a wrong argument type, and add a cancel tool.",
    "checks": "The guess is wrong; the search finds the Alfama Inn; the booking waits for confirmation, then leaves 2 rooms.",
    "bridge": "Lab 05 lets the model call tools again and again, choosing each next step from what it has seen.",
    "steps": 5,
    "patterns": [
      "One-Step Tool Agent"
    ],
    "background": [
      "A language model only produces text. To be useful in a real system, it must read current data and act: check a booking system, query a database, send a request. Tool use, also called function calling, gives it this ability in a controlled way. Most model APIs added it around 2023. The model writes a structured request that names a tool and its arguments, and the program decides whether to run it.",
      "This division of work is the key design idea. The model chooses; our code executes and stays responsible. So the program checks every request, returns errors that the model can read, and asks a person before any action that changes data. An LLM with tools is the \"augmented LLM\" that agents are built from."
    ],
    "terms": [
      [
        "Tool",
        "A function that the model may ask the program to run."
      ],
      [
        "Function calling",
        "A reply format in which the model names a tool and gives its arguments as JSON."
      ],
      [
        "Read and write tools",
        "A read tool only looks data up; a write tool changes data and needs more care."
      ],
      [
        "Confirmation",
        "A person's approval before a tool changes anything."
      ]
    ]
  },
  {
    "id": "05",
    "file": "05_react_agent",
    "title": "ReAct agents: reason, act, observe",
    "subtitle": "A guarded ReAct loop with a history",
    "topics": "agent foundations patterns react action observation loop chaining routing one-step tool agent in a react loop",
    "idea": "The model chooses each action and sees every observation so far; our code owns the tools, the guards, and the turn limit.",
    "objectives": [
      "Follow a model-selected sequence of actions.",
      "Explain each guard and the turn limit.",
      "Check the agent's final decision."
    ],
    "example": "The goal names “our wiki project”, so the agent must list the projects, read the right one, and then decide.",
    "exercise": "Make the agent finish too early, recover from a wrong project name, and change the goal.",
    "checks": "Three turns: list_projects, get_project, finish. The decision matches the policy after two tool calls.",
    "bridge": "The model chooses the steps, but code owns the tools, the guards, and the turn limit. Self-study Lab 11 serves tools through MCP.",
    "track": "lecture-2",
    "pattern": "One-Step Tool Agent in a ReAct loop",
    "steps": 4,
    "patterns": [
      "One-Step Tool Agent"
    ],
    "background": [
      "In Lab 04 the model chose one tool for one request. Many tasks need several steps, in an order that depends on what each step finds: look up the exact name, then read the facts, then decide. ReAct (Yao and colleagues, 2022) interleaves reasoning and acting: the model picks an action, the program runs it, and the result, the observation, goes back to the model for its next choice. This loop is what most people mean by an agent.",
      "Autonomy brings new risks: an agent can loop forever, act on a guess, or call something it should not. So the program keeps control of the loop: a turn limit, a fixed list of tools, and rules such as \"read the facts before you finish\". The agent decides what to do; the code decides what is allowed."
    ],
    "terms": [
      [
        "Agent",
        "A system in which a model chooses its next action in a loop, based on what it has observed."
      ],
      [
        "Observation",
        "The result of an action, fed back into the next prompt."
      ],
      [
        "History",
        "Every action and observation so far; the agent's view of the task."
      ],
      [
        "Guard",
        "A rule in code that the agent cannot override, such as a turn limit."
      ]
    ]
  },
  {
    "id": "06",
    "file": "06_multi_agent_debate",
    "title": "Multi-agent debate: propose, challenge, agree",
    "subtitle": "Independent proposals on three model families, challenges, and a chair",
    "topics": "multi-agent council debate parallel proposals critique revision consensus voting dissent chair coordinator grounding model families patterns debate-based cooperation",
    "idea": "Three architects on three model families propose alone and in parallel; a chair challenges unsupported claims, counts grounded votes, keeps the dissent, and escalates a deadlock.",
    "objectives": [
      "Collect independent proposals in parallel.",
      "Turn disagreement into sourced claims.",
      "Apply a stopping rule, record dissent, and handle a deadlock."
    ],
    "example": "Two architects choose microservices and one the modular monolith; the claim without a source is challenged and revised before the vote.",
    "exercise": "Cause a deadlock, cite a made-up source, and compare one model family with three in live mode.",
    "checks": "Six messages over three rounds; microservices wins 2 to 1, and the Safeguard's dissent citing F3 is kept.",
    "bridge": "Live mode uses three model families, each with its own key: Qwen on FreeInference, DeepSeek, and Gemini.",
    "track": "lecture-3",
    "pattern": "Debate-Based Cooperation",
    "steps": 5,
    "patterns": [
      "Debate-Based Cooperation",
      "Voting-Based Cooperation"
    ],
    "background": [
      "A single model has one set of blind spots and can be confidently wrong. People handle hard decisions with review boards and panels, and multi-agent systems borrow that idea. Research on multiagent debate (Du and colleagues, 2023) found that letting several model instances argue and revise their answers can improve factual accuracy and reasoning.",
      "Debate helps only when the views are independent and the rules are fair. Models tend to agree with what they have just read, a tendency called sycophancy, so the architects propose alone before they see each other's answers. Different model families make different mistakes. A chair with fixed rules demands sources, limits the rounds, counts the votes, keeps the dissent, and hands the decision to a person when there is no majority."
    ],
    "terms": [
      [
        "Multi-agent system",
        "Several model-driven agents with separate roles that work on one task."
      ],
      [
        "Independence",
        "Each agent answers without seeing the others first, so its view is its own."
      ],
      [
        "Grounding",
        "Supporting a claim with a source that everyone can check."
      ],
      [
        "Escalation",
        "Handing the decision to a person when the agents cannot agree."
      ]
    ]
  },
  {
    "id": "07",
    "file": "07_observe_trace_swap",
    "title": "Observability, tracing, and swappable agents",
    "subtitle": "A typed message, logs you can watch and search, a LangSmith trace, and an agent added in one line",
    "topics": "observability logging logs log file json lines traceability swappable message bus registry schema dataclass provenance langsmith tracing trace spans",
    "idea": "Log every message twice, as a live line and as a JSON record in a log file, make every message cite its basis, and find agents in a registry, so the council can be watched, traced, and changed.",
    "objectives": [
      "Define a typed, read-only message that cites its sources.",
      "Make a council observable with logs, a live stream and a JSON log file, and with a LangSmith trace.",
      "Trace a decision back to its evidence from the log file, and add an agent without changing the council's code."
    ],
    "example": "Two architects disagree and the chair logs an escalation warning; a rule-based agent joins with one line; council.log rebuilds the evidence trail, and LangSmith shows each run as a tree of timed steps.",
    "exercise": "Cite a missing source, count warnings from the log file, make the decision cite the dissent, and give one architect its own model.",
    "checks": "Run 1 logs an escalation warning at 1 vote of 2; run 2 decides microservices 2 of 3, and the trace of m6 from the log file reaches R1 and F1.",
    "bridge": "The logs make the council observable, the citations in them make it traceable, and the registry makes its agents swappable.",
    "track": "lecture-3",
    "steps": 5,
    "patterns": [
      "Shared Memory",
      "Registry & Adapter"
    ],
    "background": [
      "As soon as several agents work together, a new question appears: what is the system actually doing? With one model call you can read the reply. With a council, a decision comes out of many messages between many agents, and a wrong decision is hard to explain unless every step was recorded. Software engineering met the same problem with distributed systems, and answered it with observability: logs, metrics, and traces that let you see a running system from the outside.",
      "Three properties carry over to agents. A system is observable when you can watch it work while it runs. It is traceable when every output can be followed back to who produced it and what it was based on, which is also called provenance. It is swappable when a part can be added or replaced through a fixed interface, without rewriting the rest. Logs are the first tool for all of this: a live stream to watch, and a log file of structured records to search, count, and trace afterwards. A bus that logs every message, and a registry of agents, give all three properties. This is the event-driven design that many large systems use: components publish events, and anything interested subscribes. Tracing tools such as LangSmith add the execution view: each run as a tree of steps, with inputs, outputs, and timings."
    ],
    "terms": [
      [
        "Observability",
        "Seeing what a running system does from its outputs: logs, metrics, and traces."
      ],
      [
        "Trace",
        "A record of one run as a tree of steps, with each step's input, output, and timing; LangSmith shows traces of LLM applications."
      ],
      [
        "Log",
        "A time-stamped record of what happened; structured logs, such as JSON lines, can be searched and counted."
      ],
      [
        "Registry",
        "A lookup table of agents by name, so the system never hard-codes who takes part."
      ]
    ]
  },
  {
    "id": "08",
    "file": "08_human_feedback_memory",
    "title": "Human-in-the-loop and agent memory",
    "subtitle": "Human review, short- and long-term memory, and a held-out evaluation",
    "topics": "human in the loop feedback memory vector database chroma lessons evaluation held-out learning patterns council human in the loop and archival memory short-term memory long-term memory scratchpad",
    "idea": "The human architect reviews each proposal and keeps the final say; the accepted decision and its reasons become a memory that later cases recall.",
    "objectives": [
      "Keep a human's final authority in a bounded review loop.",
      "Store lessons with a human-approved scope, then retrieve applicable ones.",
      "Measure improvement on held-out cases only."
    ],
    "example": "The human rejects microservices for its operating cost; the lesson later changes the Logistics tracker's decision but not the Search platform's.",
    "exercise": "Accept or reject every proposal, tighten the recall distance, and add a case where the lesson should not apply.",
    "checks": "Practice: the revision is accepted; held-out scores are 1 of 2 before and 2 of 2 after memory. Live scores are measured, not guaranteed.",
    "bridge": "Similar text does not mean a lesson applies; the project needs 20 or more held-out scenarios and repeated live runs.",
    "track": "lecture-3",
    "pattern": "Human in the Loop and Archival Memory",
    "steps": 5,
    "patterns": [
      "Human in the Loop",
      "Scratchpad Memory",
      "Archival Memory"
    ],
    "background": [
      "Some decisions are too costly to automate fully, and someone must be accountable for them. Human-in-the-loop design places an approval point where the risk is high, and records the reasons. Those reasons are valuable: they hold knowledge that no written policy contains, such as \"one operations engineer cannot run a service per squad\".",
      "An LLM remembers nothing between calls; every call starts fresh. An agent's memory is therefore something the program builds. Short-term memory carries notes through one task, inside the prompt. Long-term memory keeps lessons across tasks, often in a vector database, and recalls them by similarity, as in the Generative Agents and Reflexion research. A similar case is not always a relevant one, so a lesson keeps its facts, reason, and human-approved scope. This lab filters by the operations-team size before adding a recalled lesson to the prompt, and measures the score change on cases that never gave feedback."
    ],
    "terms": [
      [
        "Human in the loop",
        "A design in which a person approves or corrects the system's decisions."
      ],
      [
        "Short-term memory",
        "Working notes for the current task, passed in the prompt."
      ],
      [
        "Long-term memory",
        "Lessons stored across tasks and recalled when a similar case appears."
      ],
      [
        "Held-out case",
        "A test case that was never used for feedback, so it measures learning, not memorisation."
      ]
    ]
  },
  {
    "id": "09",
    "file": "09_multi_agent_evaluation",
    "title": "Evaluation: a multi-agent system against a single model",
    "subtitle": "A baseline comparison with a calibrated LLM judge",
    "topics": "evaluation baseline experiment llm judge calibration human ratings grounding cost latency council patterns",
    "idea": "Compare the council with each of its models alone on the same scenarios, by correctness, grounding, a judged trade-off measure, and cost; trust the LLM judge only after it agrees with human ratings.",
    "objectives": [
      "Compare a system with the strongest baseline.",
      "Use an LLM judge with a narrow rubric.",
      "Calibrate the judge against human ratings."
    ],
    "example": "Four systems answer two held-out scenarios; the judge rates whether each answer names a cost of its option.",
    "exercise": "Raise the calibration threshold, make the council wrong once, and remove a run.",
    "checks": "The judge agrees with the human on 3 of 4 answers. The council ties DeepSeek on correctness and beats it on grounding, at 5 times the calls.",
    "bridge": "Two scenarios demonstrate the method; the project needs 20 or more, and an honest report even when the council does not win.",
    "track": "self-study",
    "steps": 5,
    "patterns": [],
    "background": [
      "A council is more complex than one model and makes several times as many calls, so it must earn its place. The honest test is a controlled comparison: run the council and each single model on the same scenarios, and measure several things, including cost and time, not only correctness.",
      "Some qualities, such as \"does the answer name a cost?\", need judgement. An LLM judge (Zheng and colleagues, 2023) uses a model to rate answers at scale, but judges have biases, for example towards longer answers or towards their own model family. So the judge is calibrated first: compared with a human's ratings on a sample, and trusted only if it agrees often enough."
    ],
    "terms": [
      [
        "Baseline",
        "The system to beat; here, the best single model."
      ],
      [
        "Metric",
        "A number that measures one quality, such as correct answers or model calls."
      ],
      [
        "LLM judge",
        "A model that rates other models' answers against a rubric."
      ],
      [
        "Calibration",
        "Checking the judge against human ratings before trusting it."
      ]
    ]
  },
  {
    "id": "10",
    "file": "10_routing",
    "title": "Routing: rules, models, and a safe fallback",
    "subtitle": "A model router, a dispatch table, a safe fallback, and the cost of each mistake",
    "topics": "routing router classifier dispatch handlers fallback cost few shot council patterns",
    "idea": "A router reads each case and picks a handler: plain code for routine cases, the council for contested ones. Code owns the routes and falls back to the council when a reply is unusable.",
    "objectives": [
      "Route inputs with a model and a dispatch table.",
      "Fall back safely on an unusable reply.",
      "Count routing cost and weigh the two kinds of mistake."
    ],
    "example": "Six cases with a note the rule cannot read; the router sends the two cases with one operations engineer to the council.",
    "exercise": "Skip a needed debate, send an unusable route, change a note, and compare a router with and without worked examples.",
    "checks": "The router agrees with the human on 5 of 6 cases, skips no needed debate, and costs 21 calls against 30.",
    "bridge": "Live, worked examples kept the router from skipping debates; a router that wastes too many debates costs more than none.",
    "track": "self-study",
    "pattern": "Routing",
    "steps": 4,
    "patterns": [
      "Routing"
    ],
    "background": [
      "Not every case deserves the most expensive treatment. Hospitals triage patients, and support desks route tickets. Routing applies the same idea to AI systems: a classifier, often a small model call, decides which handler fits each input, such as cheap rules for routine cases and a full council for contested ones.",
      "A router makes mistakes, and they do not cost the same. Sending a routine case to the council wastes calls; sending a contested case to the rule skips a debate that was needed. A good design falls back to the careful path when the router's answer is unusable, counts the router's own calls, and measures both kinds of mistake separately."
    ],
    "terms": [
      [
        "Router",
        "A component that picks the handler for each input."
      ],
      [
        "Dispatch table",
        "A mapping from each route to the function that handles it."
      ],
      [
        "Fallback",
        "The safe route taken when the router's answer cannot be used."
      ],
      [
        "Asymmetric errors",
        "Mistakes whose costs differ, so they are counted and weighed separately."
      ]
    ]
  },
  {
    "id": "11",
    "file": "11_tools_mcp",
    "title": "MCP: serve tools through a standard protocol",
    "subtitle": "Read and write tools with validation and errors",
    "topics": "tools mcp server client extract action agent foundations registry & adapter",
    "idea": "A tool reads data or performs an allowed action; MCP publishes its name, description, and input schema to any client.",
    "objectives": [
      "Build MCP tools with typed arguments.",
      "Discover tools and their schemas as a client.",
      "Handle tool errors without changing state."
    ],
    "example": "Serve get_project and save_decision through the real MCP SDK, run a fixed workflow over two projects, then send three bad calls.",
    "exercise": "Add a project, add a list_projects tool, and send an argument of the wrong type.",
    "checks": "Both decisions are saved. Each bad call returns is_error=True, and the saved state does not change.",
    "bridge": "In a council, one MCP server can give every architect the same tools and sources.",
    "track": "self-study",
    "pattern": "Registry & Adapter",
    "steps": 5,
    "patterns": [
      "Registry & Adapter"
    ],
    "background": [
      "In Lab 04 the tools lived inside our own program. As AI applications multiplied, every application wrote its own connection code for every tool and data source. The Model Context Protocol (MCP), released by Anthropic as an open standard in November 2024, gives this a common shape: a server publishes its tools with names, descriptions, and input schemas, and any MCP client can discover and call them.",
      "A protocol separates what a tool offers from who calls it. The tool checks its own input and reports errors as data, so every client sees the same behaviour. In a council, one MCP server can give every architect the same sources and the same tools."
    ],
    "terms": [
      [
        "MCP server",
        "A program that publishes tools, and other context, through the protocol."
      ],
      [
        "MCP client",
        "A program that discovers and calls a server's tools."
      ],
      [
        "Input schema",
        "A machine-readable description of a tool's arguments and their types."
      ],
      [
        "Discovery",
        "Asking a server what it offers, instead of hard-coding it."
      ]
    ]
  },
  {
    "id": "12",
    "file": "12_agent_skills",
    "title": "Agent skills: reusable instructions on demand",
    "subtitle": "Choose a skill from a catalog, then check its output",
    "topics": "skills skill.md adr architecture decision record reusable skill library evolution",
    "idea": "A skill packages a procedure with a name and a description; an agent chooses from the descriptions and loads only the chosen instructions.",
    "objectives": [
      "Split a SKILL.md file into its header and body.",
      "Explain progressive disclosure.",
      "Check a skill's output format and allow one bounded repair."
    ],
    "example": "Pick the ADR skill from a three-skill catalog, then write and check decision records for two projects.",
    "exercise": "Give an incident task, add a Risk line to an ADR, and write a fourth skill.",
    "checks": "The ADR skill is chosen. Both records have Context, Decision, and Consequence, with a policy-consistent decision.",
    "bridge": "Only the chosen skill's instructions enter the prompt, so the catalog can grow.",
    "track": "self-study",
    "pattern": "Skill Library Evolution",
    "steps": 5,
    "patterns": [
      "Skill Library Evolution"
    ],
    "background": [
      "Agents repeat procedures: write a decision record, summarise an incident, draft release notes. Copying these instructions into every prompt wastes context, and the copies drift apart. Agent Skills, an open format introduced by Anthropic in 2025, packages a procedure as a SKILL.md file with a name, a description, and the instructions.",
      "The key idea is progressive disclosure. The agent first sees only the short descriptions of all its skills, picks one, and only then loads its full instructions. A library of many skills costs little until one is needed. A skill's output is still model output, so the program keeps checking it."
    ],
    "terms": [
      [
        "Skill",
        "A packaged procedure: a name, a description, and instructions."
      ],
      [
        "Progressive disclosure",
        "Showing the model only short descriptions first, and the full instructions on demand."
      ],
      [
        "Catalog",
        "The list of skill names and descriptions that the model chooses from."
      ],
      [
        "Output checker",
        "Code that verifies that a skill's result has the promised shape."
      ]
    ]
  },
  {
    "id": "13",
    "file": "13_a2a_protocol",
    "title": "A2A: delegate work to another agent",
    "subtitle": "A tiny hotel-desk agent over A2A, then review and revision",
    "topics": "a2a agent card discovery message review architecture generator–critic loop agent card hotel desk",
    "idea": "A2A lets one agent discover another through its Agent Card and exchange messages; the reviewer's feedback can drive a revision.",
    "objectives": [
      "Discover a reviewer agent and read its reply.",
      "Use another agent's feedback to revise.",
      "Bound a multi-agent exchange."
    ],
    "example": "Our model proposes a decision for four projects. A reviewer agent rejects one proposal, and the revision passes.",
    "exercise": "Add a second mistake, then make a revision wrong too.",
    "checks": "All four projects pass, with one revision for the Internal wiki.",
    "bridge": "The reviewer is deterministic and runs over real local A2A routes; practice mode needs no API key.",
    "track": "self-study",
    "pattern": "Generator–Critic Loop",
    "steps": 4,
    "patterns": [
      "Generator–Critic Loop"
    ],
    "background": [
      "Tools are functions inside one program. Some capabilities are whole agents, built by other teams, in other languages, on other servers. The Agent2Agent (A2A) protocol, introduced by Google in April 2025 and now developed as an open project under the Linux Foundation, lets agents discover each other and exchange messages without sharing code.",
      "Each agent publishes an Agent Card with its name, description, skills, and address. A client reads the card, then sends messages. This makes a reviewer agent a real second opinion: it runs separately, with its own logic, and its feedback can drive a revision. In short, MCP connects an agent to tools, and A2A connects agents to each other."
    ],
    "terms": [
      [
        "Agent Card",
        "A public description of an agent: what it does and where to reach it."
      ],
      [
        "Message",
        "The unit of communication between two agents."
      ],
      [
        "Generator and critic",
        "One agent produces a draft; another reviews it against criteria."
      ],
      [
        "Interoperability",
        "Systems from different teams working together through a shared protocol."
      ]
    ]
  },
  {
    "id": "14",
    "file": "14_frameworks_langgraph",
    "title": "Agent frameworks: graphs with LangGraph",
    "subtitle": "A LangGraph loop with a conditional retry",
    "topics": "framework langgraph state nodes edges evaluate architecture generator–critic loop",
    "idea": "A framework makes the steps, the shared state, and the decision to retry explicit.",
    "objectives": [
      "Define graph state and nodes.",
      "Route with a conditional edge.",
      "Keep generation separate from validation."
    ],
    "example": "Run a choose-and-check graph on four projects. One project fails, gets feedback, and passes on its second attempt.",
    "exercise": "Use up the attempts, allow a third attempt, and add a fifth project.",
    "checks": "All four projects pass, the Internal wiki after two attempts, for five model calls in total.",
    "bridge": "Passing a policy check is useful evidence, but not architecture quality. Try Lab 06's council as a graph.",
    "track": "self-study",
    "pattern": "Generator–Critic Loop",
    "steps": 4,
    "patterns": [
      "Generator–Critic Loop"
    ],
    "background": [
      "After a few labs, the same parts keep appearing: shared state, steps, an order between them, and a decision to loop back. Frameworks name these parts and handle the plumbing. LangGraph, from the team behind LangChain, models a workflow as a graph: nodes are steps, edges set their order, and a conditional edge chooses the next node from the state.",
      "A framework does not make the model smarter. It makes the structure explicit: you can print the graph, test each node on its own, and see every retry. That pays off as a system grows. Building the loop in plain Python first shows what the framework does for you, and when you do not need one."
    ],
    "terms": [
      [
        "State",
        "The data that all steps of a workflow read and write."
      ],
      [
        "Node",
        "One step of the graph, written as a function of the state."
      ],
      [
        "Edge",
        "A connection that sets which node runs next."
      ],
      [
        "Conditional edge",
        "An edge that picks the next node from the state, which is how a graph loops."
      ]
    ]
  },
  {
    "id": "15",
    "file": "15_framing_contract",
    "track": "self-study",
    "title": "Problem framing and typed message contracts",
    "subtitle": "Quality-attribute scenarios, a typed proposal, and swappable architects",
    "topics": "framing quality attribute scenarios iso 25010 message contract schema confidence swappable agents chair passive goal creator and a contract",
    "idea": "The chair frames a brief as measurable quality-attribute scenarios; every proposal must follow one contract, so any architect can be added or replaced.",
    "objectives": [
      "Write measurable quality-attribute scenarios.",
      "Enforce a message contract with confidence and trade-offs.",
      "Add an architect without changing the council's code."
    ],
    "example": "A Booking service with a Monday spike and an audit requirement; four architects answer, and one is rejected for breaking the contract.",
    "exercise": "Fix the rejected reply, make votes and confidence disagree, add an architect, and break the frame.",
    "checks": "Three scenarios pass the gate; the Auditor is rejected; votes 2 to 1 and confidence 1.3 to 0.9 agree.",
    "bridge": "Self-reported confidence is information, not proof; Lab 16 learns whom to trust from outcomes.",
    "pattern": "Passive Goal Creator and a contract",
    "steps": 5,
    "patterns": [
      "Passive Goal Creator"
    ],
    "background": [
      "Architects often disagree less about the answer than about what matters. Software architecture practice handles this with quality-attribute scenarios, described by Bass, Clements, and Kazman: each names a quality, a stimulus, a response, and a measurable target. The ISO/IEC 25010 quality model gives a shared vocabulary, so \"security\" means the same thing to everyone.",
      "Agents need the same discipline in their messages. A message contract fixes what every proposal must contain, so the chair can check it with code and any architect can be replaced without changing the rest. It is the same idea as an API contract between services: agree on the interface, and the implementations can change freely."
    ],
    "terms": [
      [
        "Quality-attribute scenario",
        "A testable statement: a stimulus, the required response, and a measure."
      ],
      [
        "ISO/IEC 25010",
        "A standard model of software quality characteristics."
      ],
      [
        "Message contract",
        "The fields and rules that every message between agents must follow."
      ],
      [
        "Self-reported confidence",
        "A model's own estimate of how sure it is; information, not proof."
      ]
    ]
  },
  {
    "id": "16",
    "file": "16_learning_curve_trust",
    "track": "self-study",
    "title": "Learning from feedback: learning curves and trust weights",
    "subtitle": "A feedback/test split, trust-weighted votes, and a curve",
    "topics": "evaluation experiment feedback test split held-out learning curve per-model trust weighted vote council voting-based cooperation",
    "idea": "Learn from feedback cases only, weight each architect by how much better than chance it has been, and score the test cases after every round.",
    "objectives": [
      "Keep feedback and test cases apart.",
      "Turn agreement with the human into vote weights.",
      "Read a learning curve, including where it stalls."
    ],
    "example": "Ten small cases and three recorded architects; plain majority gets 2 of 4 test cases, the trusted council 4 of 4 after five rounds.",
    "exercise": "Reorder the feedback, weight by raw trust, and remove the best architect's slip.",
    "checks": "The learning curve is [2, 2, 2, 2, 2, 4, 4], with two escalated ties at round 4.",
    "bridge": "A curve that falls as well as rises is still evidence; plan your project's experiment with it.",
    "pattern": "Voting-Based Cooperation",
    "steps": 4,
    "patterns": [
      "Voting-Based Cooperation"
    ],
    "background": [
      "A system that learns from feedback must show that it improves on new cases, not that it remembers old ones. Machine learning answered this long ago with a train/test split: learn from one set, score on another, and never mix them. A learning curve plots the score as feedback grows, which shows how fast the system learns and where it stalls.",
      "Weighting voters by their record is an old idea too. The weighted majority algorithm (Littlestone and Warmuth, 1994) lowers an expert's weight each time it is wrong, so reliable experts come to dominate. Here, an architect that agrees with the human more often than chance gains influence, and one at chance level gets none."
    ],
    "terms": [
      [
        "Train/test split",
        "Separate cases for learning and for scoring."
      ],
      [
        "Learning curve",
        "The score plotted after each round of feedback."
      ],
      [
        "Weighted vote",
        "A vote in which each voter counts according to its weight."
      ],
      [
        "Trust",
        "Here, how often an architect has agreed with the human on the feedback cases."
      ]
    ]
  }
];

const patternGuide = [
  {"name": "Retrieval-Augmented Generation", "category": "Single-agent"},
  {"name": "Single-Path Planning", "category": "Single-agent"},
  {"name": "One-Step Tool Agent", "category": "Single-agent"},
  {"name": "Passive Goal Creator", "category": "Single-agent"},
  {"name": "Debate-Based Cooperation", "category": "Multi-agent"},
  {"name": "Voting-Based Cooperation", "category": "Multi-agent"},
  {"name": "Human in the Loop", "category": "Multi-agent"},
  {"name": "Generator–Critic Loop", "category": "Multi-agent"},
  {"name": "Registry & Adapter", "category": "Multi-agent"},
  {"name": "Skill Library Evolution", "category": "Multi-agent"},
  {"name": "Scratchpad Memory", "category": "Memory"},
  {"name": "Archival Memory", "category": "Memory"},
  {"name": "Shared Memory", "category": "Memory"},
  {"name": "Routing", "category": "Built from the guide", "note": "Combines Human in the Loop's risk classification with Registry & Adapter's dispatch."}
];

const tracks = [
  {
    "id": "lecture-1",
    "label": "Lecture 1 · 90 minutes",
    "title": "Ask, check, retrieve",
    "note": "A rule, a model, a test set, and retrieval: the building blocks of every later lab."
  },
  {
    "id": "lecture-2",
    "label": "Lecture 2 · 90 minutes",
    "title": "Chain, call tools, act",
    "note": "From a fixed chain of prompts, to tools that read and change live data, to an agent that chooses its own steps."
  },
  {
    "id": "lecture-3",
    "label": "Lecture 3 · 90 minutes",
    "title": "Debate, trace, decide",
    "note": "A council of architects debates through a message bus that you can watch and trace, a human decides, and short- and long-term memory keep the lessons."
  },
  {
    "id": "self-study",
    "label": "Self-study · at your own pace",
    "title": "Go deeper",
    "note": "An evaluation against single models, routing, protocols, skills, a framework, framing, and a learning experiment: what the project needs beyond the lectures. Each lab ends with a challenge for your council."
  }
];

const list = document.getElementById('lab-list');
const esc = text => String(text).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const config = window.COURSE_CONFIG || {};
const configured = typeof config.repo === 'string' && /^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})\/[A-Za-z0-9_.-]+$/.test(config.repo) && config.repo !== 'OWNER/REPO';
const ref = typeof config.ref === 'string' ? config.ref : 'main';
const STORAGE_KEY = 'agentic-ai-course-architecture-v3-progress';
const number = i => String(i).padStart(2, '0');
let completed = [];
try { const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); if (Array.isArray(stored)) completed = stored.filter(x => labs.some(l => l.id === x)); } catch (_) { /* Browser storage is optional. */ }

function updateProgress() {
  const count = labs.filter(l => completed.includes(l.id)).length;
  document.getElementById('progress-label').textContent = `${count} / ${labs.length} labs explored`;
  document.getElementById('course-progress').value = count;
  labs.forEach(lab => document.getElementById(`lab-${lab.id}`).classList.toggle('done', completed.includes(lab.id)));
  tracks.forEach(track => {
    const ids = labs.filter(l => l.track === track.id).map(l => l.id);
    const text = `${ids.filter(id => completed.includes(id)).length} of ${ids.length} explored`;
    document.querySelectorAll(`[data-track-progress="${track.id}"]`).forEach(el => { el.textContent = text; });
    document.querySelectorAll(`[data-track-short="${track.id}"]`).forEach(el => { el.textContent = `${ids.filter(id => completed.includes(id)).length} / ${ids.length} done`; });
  });
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(completed)); } catch (_) { /* Private browsing can disable storage. */ }
}
function notebookActions(lab) {
  const path = `notebooks/${lab.file}.ipynb`;
  const colab = configured ? `https://colab.research.google.com/github/${config.repo}/blob/${encodeURIComponent(ref)}/${path}` : null;
  const action = colab ? `<a class="button primary" href="${esc(colab)}" target="_blank" rel="noopener">Open in Colab <span aria-hidden="true">↗</span></a>` : `<a class="button secondary" href="#setup">Colab setup <span aria-hidden="true">↑</span></a>`;
  return `<div class="notebook-actions">${action}<a class="button secondary" href="${path}" download>Download notebook <span aria-hidden="true">↓</span></a></div>`;
}
const chips = names => names.map(name => `<span class="pattern-chip">${esc(name)}</span>`).join('');

// A bar of the four sections that stays in view while the lab list scrolls.
const jump = document.createElement('nav');
jump.className = 'track-jump';
jump.setAttribute('aria-label', 'Lectures and self-study');
jump.innerHTML = tracks.map(track => `<a href="#track-${track.id}"><strong>${esc(track.label.split(' · ')[0])}</strong><small data-track-short="${track.id}"></small></a>`).join('');
list.before(jump);

const trackGroups = {};
tracks.forEach(track => {
  const group = document.createElement('section');
  group.className = 'track';
  group.id = `track-${track.id}`;
  group.setAttribute('aria-label', `${track.label}: ${track.title}`);
  group.innerHTML = `<div class="track-heading"><div class="track-meta"><span class="tag">${esc(track.label)}</span><span class="track-progress" data-track-progress="${track.id}"></span></div><h3>${esc(track.title)}</h3><p>${esc(track.note)}</p></div>`;
  list.appendChild(group);
  trackGroups[track.id] = group;
});

labs.forEach((lab, i) => {
  const detail = document.createElement('details');
  detail.className = 'lab';
  detail.id = `lab-${lab.id}`;
  detail.dataset.search = `${lab.title} ${lab.subtitle} ${lab.topics} ${lab.patterns.join(' ')}`.toLowerCase();
  const prev = labs[i - 1], next = labs[i + 1];
  const pager = `<nav class="lab-pager" aria-label="Neighbouring labs">${prev ? `<a href="#lab-${prev.id}"><small>← Lab ${prev.id}</small>${esc(prev.title)}</a>` : '<span></span>'}${next ? `<a class="next" href="#lab-${next.id}"><small>Lab ${next.id} →</small>${esc(next.title)}</a>` : ''}</nav>`;
  detail.innerHTML = `<summary><span class="lab-number" aria-hidden="true"><span class="num">${number(i)}</span><span class="tick">✓</span></span><div><h3><span class="visually-hidden">Lab ${number(i)}: </span>${esc(lab.title)}</h3><p>${chips(lab.patterns)}<span class="lab-subtitle">${esc(lab.subtitle)}</span></p></div><span class="lab-time">${lab.steps} steps</span><span class="expand-icon" aria-hidden="true">+</span></summary>`
    + `<div class="lab-body"><div class="lab-lead"><p class="lab-intro">${esc(lab.idea)}</p>${notebookActions(lab)}</div>`
    + `<section class="lab-context" aria-label="The idea in context"><div><h4>The idea in context</h4>${lab.background.map(text => `<p>${esc(text)}</p>`).join('')}</div>`
    + `<aside class="key-terms"><h4>Key terms</h4><dl>${lab.terms.map(([term, meaning]) => `<dt>${esc(term)}</dt><dd>${esc(meaning)}</dd>`).join('')}</dl></aside></section>`
    + `<h4 class="diagram-heading">How the lab works</h4><figure class="lab-diagram" data-diagram="${lab.id}"></figure>`
    + `<div class="lesson-grid"><div><h4>What you will learn</h4><ul>${lab.objectives.map(t => `<li>${esc(t)}</li>`).join('')}</ul></div><div><h4>Walk through an example</h4><p>${esc(lab.example)}</p></div><div><h4>Make it your own</h4><p>${esc(lab.exercise)}</p></div><div><h4>Expected output &amp; check</h4><p>${esc(lab.checks)}</p></div></div>`
    + `<p class="lesson-takeaway"><strong>Takeaway.</strong> ${esc(lab.bridge)}</p>`
    + `<div class="lab-actions"><label class="completion"><input type="checkbox" data-lab="${lab.id}" ${completed.includes(lab.id) ? 'checked' : ''}> I explored lab ${number(i)}</label>${pager}</div>`
    + `${configured ? '' : '<p class="publish-note">Download this notebook and upload it to Colab, or configure the repository links.</p>'}</div>`;
  trackGroups[lab.track].appendChild(detail);
  detail.addEventListener('toggle', () => { if (detail.open) drawDiagram(detail); });
});

// The field guide's patterns, each linked to the labs that teach it.
const patternGrid = document.getElementById('pattern-grid');
if (patternGrid) {
  const categories = [...new Set(patternGuide.map(p => p.category))];
  patternGrid.innerHTML = categories.map(category => `<div class="pattern-column"><h3>${esc(category)}</h3><ul>${patternGuide.filter(p => p.category === category).map(p => {
    const where = labs.filter(l => l.patterns.includes(p.name)).map(l => `<a href="#lab-${l.id}">Lab ${l.id}</a>`).join(' ');
    return `<li><span class="pattern-name">${esc(p.name)}</span><span class="pattern-labs">${where}</span>${p.note ? `<small>${esc(p.note)}</small>` : ''}</li>`;
  }).join('')}</ul></div>`).join('');
}

function drawDiagram(detail) {
  const figure = detail.querySelector('.lab-diagram');
  if (figure && typeof renderDiagram === 'function') renderDiagram(figure, figure.dataset.diagram);
}
let resizeTimer;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => list.querySelectorAll('.lab[open]').forEach(drawDiagram), 150);
});

list.addEventListener('change', event => {
  if (!event.target.matches('input[data-lab]')) return;
  const id = event.target.dataset.lab;
  completed = event.target.checked ? [...new Set([...completed, id])] : completed.filter(x => x !== id);
  updateProgress();
});
document.getElementById('reset-progress').addEventListener('click', () => {
  completed = [];
  list.querySelectorAll('input[data-lab]').forEach(input => { input.checked = false; });
  updateProgress();
});
document.getElementById('lab-search').addEventListener('input', event => {
  const query = event.target.value.trim().toLowerCase();
  let visible = 0;
  list.querySelectorAll('.lab').forEach(lab => { lab.hidden = !lab.dataset.search.includes(query); if (!lab.hidden) visible += 1; });
  list.querySelectorAll('.track').forEach(group => { group.hidden = !group.querySelector('.lab:not([hidden])'); });
  document.getElementById('filter-status').textContent = query ? `${visible} ${visible === 1 ? 'lab' : 'labs'} found` : `All ${labs.length} labs`;
});
function clearSearch() {
  document.getElementById('lab-search').value = '';
  list.querySelectorAll('.lab, .track').forEach(item => { item.hidden = false; });
  document.getElementById('filter-status').textContent = `All ${labs.length} labs`;
}
function openLab(id) {
  const lab = labs.find(l => `lab-${l.id}` === id);
  if (!lab) return;
  const detail = document.getElementById(id);
  clearSearch();
  list.querySelectorAll('.lab[open]').forEach(other => { if (other !== detail) other.open = false; });
  detail.open = true;
  detail.scrollIntoView({block: 'start'});
}
if (configured) document.querySelectorAll('.repo-link').forEach(a => { a.href = `https://github.com/${config.repo}`; a.textContent = 'GitHub ↗'; });
function openHash() { openLab(window.location.hash.slice(1)); }
document.addEventListener('click', event => {
  const link = event.target.closest('a[href^="#lab-"]');
  if (link) openLab(link.getAttribute('href').slice(1));
  if (event.target.closest('a[href^="#track-"]')) clearSearch();
});
window.addEventListener('hashchange', openHash);
updateProgress();
if (location.hash.startsWith('#lab-')) openHash();
