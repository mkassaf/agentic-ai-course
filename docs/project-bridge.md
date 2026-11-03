# From the labs to the architect-council project

The supplied **AI Assisted Software Architecting Project** asks students to build a council of peer architects, test debate and feedback, and leave the final decision to a human architect. These labs teach the building blocks. The lab council and toy evaluation are starting points for understanding the protocol; students must design, implement, and evaluate their own project.

The mapping below interprets the supplied presentation. The professor's final assignment and assessment policy remain authoritative.

## Assignment requirements and preparation

| Project requirement | Preparation | What students must add for the project |
| --- | --- | --- |
| At least three architects using different model families | Labs 00, 01, 06 | Three actual, verified families behind swappable adapters; model IDs and family provenance. Three prompts, aliases, or scripted fixtures do not constitute model diversity. |
| Peer architects with a common mandate and distinct stances | Labs 01, 06 | Shared requirements, evidence access, and output contract; justified stances such as pragmatist, guardian, or skeptic. |
| Independent proposals before discussion | Labs 04, 06 | Ensure an initial proposal cannot see peers' initial answers; preserve the original proposals for inspection. |
| Bounded debate, convergence, and dissent | Labs 03, 05, 06 | A documented protocol and round limit, explicit consensus/tie-break rules, and a deadlock or escalation path. Do not label a chair's unilateral choice as unanimous agreement. |
| Structured, observable, traceable communication | Labs 01, 03, 06 | Validated message schemas and a live trace showing sender, recipient or audience, round, evidence, and revisions; failure handling for invalid messages. |
| Grounded arguments | Labs 02, 06 | A credible knowledge base with provenance and a versioned snapshot; check whether citations support claims. A retrieved passage or valid source ID alone is insufficient. |
| Human feedback for the current and future decisions | Labs 05, 07 | Distinguish revision within one decision from persistent changes that affect later decisions; preserve feedback provenance and avoid incorporating test labels. |
| Runnable baseline, evaluation, architecture documentation, ADRs, and live demo | Labs 00–07 | Reproducible setup, justified architecture and protocol choices, benchmark results, and a visible demonstration of agent communication. |

MCP, A2A, message buses, blackboards, and orchestration frameworks are possible design choices. The project presentation allows architectural freedom while requiring structured, observable, traceable, and swappable communication. Students should explain the need a chosen mechanism serves rather than add a protocol merely to name it.

## A safe progression of project milestones

1. **Make one baseline reproducible.** Freeze a small development scenario, its requirements, an evidence snapshot, an output contract, and logging. Run each intended council model individually.
2. **Make the protocol inspectable.** Implement independent proposals, critique and revision, a bounded convergence rule, retained dissent, and a human review point. Test malformed messages, missing evidence, provider failures, and deadlock.
3. **Add feedback deliberately.** First support feedback on the current proposal. Then choose and justify a persistent mechanism such as versioned principles, case memory, or model trust weights. This changes application behavior; it does not imply that model weights have been trained.
4. **Evaluate and defend the design.** Use expert-reviewed scenarios, comparable conditions, error analysis, and a cost/latency report. Justify the architecture in ADRs and show the actual communication trace in the demo.

The human remains responsible for the architectural decision. A council may produce a recommendation, request clarification, or escalate an unresolved conflict. A majority vote does not establish correctness or authorize an external action.

## Experiment A: council versus model-alone baselines

Run **each constituent model alone**, using the same scenario, requirements, output contract, and evidence snapshot as the council. The prescribed baseline has one prompt and no debate, roles, memory, or feedback. Compare the council with every single-model result and the best single model. Keep additional experiments clearly labelled: an equal-budget or additional-call baseline can help isolate the value of coordination from the value of spending more inference.

Measure expert-rated decision quality or agreement with acceptable decisions, trade-off coverage, evidence support, failures and abstentions, calls and tokens, cost where known, and wall-clock latency. Architecture often permits several defensible answers; a rubric and acceptable alternatives are more informative than a single technology-name string. Record unknown cost as unknown. Do not use practice-mode speed or scripted agreement as live-model evidence.

The hypothesis is that the council improves decisions enough to justify its complexity. A finding of no gain or worse results is a valid outcome when the experiment and analysis are sound.

## Experiment B: feedback and future decisions

The presentation calls for a benchmark of **20 or more scenarios with expert answers**, split into feedback and held-out test sets. The notebooks' handful of toy cases only demonstrate the mechanics and are insufficient for that benchmark. Twenty scenarios are a project minimum, not a guarantee of a precise estimate.

Freeze the split and evaluation rubric before developing feedback memory. Score the initial system on the held-out set, learn only from the feedback set, then score the resulting system on that same frozen held-out set. Keep held-out labels out of prompts, retrieval, memory, and feedback-generating judges. Near-duplicate scenarios across the split can also leak answers; inspect the split by scenario family.

Plot performance across feedback iterations, keep per-scenario results, and include uncertainty or variation across repeated live runs when feasible. Repeatedly tuning after viewing test results turns that set into development data; reserve another untouched set for the final report when iterating. Calibrate any LLM judge against human ratings before relying on it. Feedback can change preferences and retrieval without improving decision quality, so measure the intended outcome directly.

## What the lab scaffold does not establish

Passing notebook assertions shows that the illustrated control flow and deterministic checks work. It does not establish genuine model diversity, citation truth, expert-level architectural judgment, calibrated confidence, or generalisation after feedback. The final report must connect those claims to actual observations and disclose the limits of the experiment.

Use the [instructor guide](instructor-guide.md) for teaching and assessment suggestions, [API setup](api-setup.md) for live access, and [sources](sources.md) for provenance and further reading.
