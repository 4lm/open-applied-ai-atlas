# 10.1.1 Autonomy, Tool Use, And Execution Distinctions

_Page Type: Concept Explainer | Maturity: Review-Ready_

Use this page to separate execution posture before a proposal gets flattened into "we need an agent." Agent review becomes sloppy when response-only assistants, workflow steps, human-triggered tool use, bounded action agents, and longer-running delegated execution are all treated as the same thing with different branding.

## Execution-Posture Map

| Execution posture | Where the real decision-making sits | What must be explicit | What fails when it is misclassified |
| --- | --- | --- | --- |
| Response-only assistant | the model helps interpret, summarize, draft, or explain, but no external action happens unless a person takes it | source grounding, review responsibility, and where the output can safely be used | teams add "agent" language to a drafting tool and import rollout controls they do not need while still ignoring quality, citation, or approval obligations |
| Workflow with model steps | the workflow owns the sequence, state, retries, and approvals while the model fills bounded reasoning steps inside that frame | the durable process boundary, step ownership, failure handling, and escalation route | teams blame model variability for problems that really come from missing workflow design, brittle handoffs, or weak exception paths |
| Human-triggered tool use | a user chooses when to call tools, but the system can now read or write beyond the prompt window | which tools are exposed, what data they touch, and whether outputs are advisory, draft, or directly applied | "tool use" gets mistaken for safe autonomy even though side effects and data exposure already widened materially |
| Bounded action agent | the system can plan and execute within a typed action surface, with approvals and rollback defined for higher-consequence steps | action classes, approval thresholds, trace coverage, disablement path, and environment separation | the team jumps from assistant demos to production action-taking without naming which actions are allowed, reversible, or forbidden |
| Long-running delegated or multi-agent execution | work continues across sessions, queues, or cooperating agents with memory, task state, and ownership outside one chat turn | task persistence, queue ownership, stop conditions, retention limits, and stale-work cleanup | "background autonomy" hides state growth, unowned queues, or recovery gaps that only appear after interruptions, incidents, or staffing changes |

## Core Distinctions

| Distinction | Why it changes the operating decision |
| --- | --- |
| Advice vs. action | A helpful answer becomes an operating decision once the system can change tickets, records, workflows, or external systems instead of merely recommending a next step. |
| Tool access vs. authority | Connecting a tool is not the same as approving every operation that tool can perform; least-privilege design depends on separating read, draft, bounded-write, and forbidden actions. |
| Session reasoning vs. durable workflow state | A model can plan inside one interaction, but retries, deadlines, approvals, and partial completion still need a workflow, queue, or case-management layer that survives the session. |
| Human initiation vs. delegated execution | A person pressing "run" on each step is materially different from a system that continues working, re-plans, or retries after the human has moved on. |
| Planning flexibility vs. process ownership | Dynamic plans help when the path is genuinely uncertain, but many teams use "agentic" language to cover for an unlabeled business process that should be explicit instead. |
| Interface automation vs. business-system integration | Browser or desktop control often feels fast to prototype, but stable APIs, typed actions, and workflow hooks are usually easier to govern, test, and roll back. |
| Trace visibility vs. chat transcript comfort | A readable conversation is not enough evidence once tools, approvals, memory, or external side effects matter; investigators need replayable traces across the full execution path. |

## What These Distinctions Change In Practice

- Start with the lightest execution posture that fits the business need. Many proposals described as "agents" are better served by a workflow with model steps or by a response-only assistant plus retrieval.
- Type actions before discussing framework choice. The real question is what the system may read, draft, execute, approve, or never touch, not whether it uses a planner loop or a vendor agent SDK.
- Treat tool boundaries as control boundaries. The jump from no tools to read-only tools, from read-only to bounded write, and from bounded write to privileged operations is a bigger operating change than a prompt tweak or model swap.
- Separate orchestration from persistence. If work needs retries, SLA timers, queue ownership, or handoff across people and systems, the durable state should live in workflow infrastructure rather than only in the model session.
- Assume browser and desktop automation are high-consequence surfaces. They cross trust boundaries quickly, make failure reconstruction harder, and often hide implicit permissions that would be obvious in API-first design.
- Keep adjacent chapters active instead of treating this chapter as self-contained. [9](../09-model-gateways-and-access-control/09-00-00-model-gateways-and-access-control.md), [11](../11-knowledge-retrieval-and-memory/11-00-00-knowledge-retrieval-and-memory.md), [14](../14-observability-logging-and-monitoring/14-00-00-observability-logging-and-monitoring.md), [15](../15-security-and-abuse-resistance/15-00-00-security-and-abuse-resistance.md), and [16](../16-human-oversight-and-operating-model/16-00-00-human-oversight-and-operating-model.md) usually decide whether a proposed autonomy level is actually governable.

## Reviewer Checks

- Which execution posture is actually being proposed: response-only assistance, workflow with model steps, human-triggered tool use, bounded action, or longer-running delegated execution?
- What is the first irreversible or externally visible action the system can take, and which approval or rollback rule covers it?
- Where does durable state live when the model session ends: nowhere, a workflow engine, a queue, a case record, or ad hoc memory attached to the agent?
- Which tool or interface boundary creates the real risk: data retrieval, record updates, browser control, privileged APIs, or hidden background retries?
- If the system fails mid-task, what evidence would let operators reconstruct the reasoning path, tool calls, approvals, and side effects without relying on screenshots or chat memory?
- Has the team chosen agentic execution because the work is truly uncertain, or because the underlying process and ownership model were never made explicit?

## Practical Reading Rule

Classify the execution posture first, then use [10.1.2 Decision Boundaries And Orchestration Heuristics](10-01-02-decision-boundaries-and-orchestration-heuristics.md) to choose the default control lane. If the team still cannot name the allowed actions, real tool boundary, durable state owner, and investigation path in one explanation, the agentic design is not ready for rollout or vendor comparison.

Back to [10.1 Agentic Foundations](10-01-00-agentic-foundations.md).
