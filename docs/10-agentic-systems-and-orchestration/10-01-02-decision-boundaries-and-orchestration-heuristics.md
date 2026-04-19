# 10.1.2 Decision Boundaries And Orchestration Heuristics

_Page Type: Decision Guide | Maturity: Review-Ready_

Use this page after the execution posture is clear enough and the remaining question is which control lane fits by default. The goal is to stop teams from calling everything an "agent" and then skipping the harder review questions around typed actions, durable state, approvals, traces, and fallback.

## Decision Lanes

| Lane | Use it when the main question is... | Default orchestration posture |
| --- | --- | --- |
| Assistant-first lane | whether the task is still interpretation, drafting, synthesis, or recommendation and no external action is required | keep the system response-only, strengthen grounding and review expectations, and reject autonomy language that imports operating burden without real execution value |
| Workflow-first lane | whether the process steps, retries, approvals, and handoffs are already knowable even if some reasoning steps are fuzzy | keep sequence and state in workflow infrastructure, use models for bounded reasoning steps, and treat "agentic" behavior as a smell unless the workflow truly cannot be made explicit |
| Human-triggered tool lane | whether a user needs on-demand access to tools or data surfaces but should remain the decision point for every consequential call | expose only the minimum read, draft, or bounded-write actions, keep the invocation explicit, and require the UI and trace layer to show what the tool call will touch |
| Bounded-action lane | whether dynamic planning or tool choice adds real value, but only inside a named action surface with approval and rollback rules | type actions before framework choice, keep approvals and disablement outside the planner loop, and prove the agent can be interrupted without losing track of work or side effects |
| Delegated-execution lane | whether work must continue across queues, sessions, or cooperating agents after the initiating human moves on | assign queue ownership, stop conditions, retention limits, stale-task cleanup, and investigation traces before approving any background or multi-agent execution |

## Practical Heuristics

- Start with the lightest lane that satisfies the business need. Most proposals should fail into assistant-first or workflow-first until the team proves that dynamic action selection, not just missing process design, creates the value.
- Type actions before naming tools. "Can search tickets" and "can update tickets" are different operating decisions, and "can approve" or "can trigger external systems" are different again.
- Treat durable state as a first-class design boundary. If the work must survive session loss, retries, handoffs, deadlines, or staffing changes, the state owner cannot live only inside a model conversation.
- Separate tool access from business authority. An agent that can technically call an API should still be blocked from approvals, record mutation, or customer-impacting actions unless those actions were explicitly allowed and reviewed.
- Escalate quickly when browser or desktop control enters the design. User-interface automation crosses trust boundaries fast, hides implicit permissions, and usually raises the evidence burden beyond what early pilots can support.
- Use agentic orchestration to handle genuine uncertainty, not to avoid naming the workflow. If operators can already describe the sequence, exception paths, and ownership model, the right answer is usually better workflow design.
- Keep fallback proportionate to consequence. A drafting assistant may only need a human takeover path, while a ticket or case-handling agent needs disablement, replay, partial-work recovery, and a non-agent path for business continuity.
- Reopen adjacent chapters as soon as the lane changes. Gateway policy, retrieval scope, observability evidence, security posture, oversight ownership, and buy-vs-build dependence all change once autonomy expands.

## Escalate When

- the team still describes the system with broad labels such as "copilot," "assistant," or "agent" but cannot name the highest-consequence allowed action
- the design depends on memory, retries, queued work, or delegated follow-up, yet nobody owns the durable task state outside the chat session
- tool access is widening faster than the approval matrix, rollback plan, or trace model needed to investigate mistakes
- a workflow could be made explicit after one or two pilots, but the team is preserving open-ended autonomy because it sounds more advanced
- browser, desktop, or privileged business-system access is entering scope before session isolation, replay, and disablement are mature
- the proposal assumes human review is enough, but the reviewer will not see the full plan, retrieved context, tool calls, or intended side effects
- one framework or managed console is becoming the only place where task state, approval history, or incident evidence can be understood

## Orchestration Anti-Patterns

- using "agent" as a substitute for naming the allowed actions, workflow owner, or operational boundary
- granting broad tool access before splitting read, draft, bounded-write, privileged, and forbidden actions
- storing task progress only in prompts or chat memory when retries, queues, approvals, or partial completion must survive interruptions
- normalizing browser or desktop automation as a general solution before API-first options, typed actions, and replay-safe evidence are in place
- treating nominal human approval as sufficient even though the approver sees only the final answer rather than the execution trace
- expanding into multi-agent delegation because it looks modular while queue ownership, task expiry, and stale-work cleanup remain undefined
- calling the design portable or low lock-in even though one orchestration framework, vendor console, or hidden memory layer is now operationally mandatory

## Chapter Handoffs

- [9. Model Gateways And Access Control](../09-model-gateways-and-access-control/09-00-00-model-gateways-and-access-control.md) when tool eligibility, identity propagation, route policy, or exception governance are now the limiting control surface.
- [11. Knowledge Retrieval And Memory](../11-knowledge-retrieval-and-memory/11-00-00-knowledge-retrieval-and-memory.md) when memory retention, retrieval scope, provenance, or stale context risk matters more than the orchestration pattern itself.
- [14. Observability Logging And Monitoring](../14-observability-logging-and-monitoring/14-00-00-observability-logging-and-monitoring.md) when trace reconstruction, exportable telemetry, or investigation workflow is too weak for the proposed autonomy level.
- [15. Security And Abuse Resistance](../15-security-and-abuse-resistance/15-00-00-security-and-abuse-resistance.md) when privileged credentials, browser control, trust boundaries, or abuse containment dominate the review.
- [16. Human Oversight And Operating Model](../16-human-oversight-and-operating-model/16-00-00-human-oversight-and-operating-model.md) when approval rights, escalation ownership, staffing, or review burden become the real bottleneck.
- [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md) when managed-framework dependence, operator burden, or exit posture matters as much as the autonomy design itself.

## Practical Reading Rule

Choose the lightest orchestration lane that still fits the hardest action, state, and evidence requirement, then tighten it as soon as autonomy or consequence rises. If the team cannot explain which lane it is using, what the highest-consequence action is, where durable state lives, how a person intervenes, and what evidence survives an incident, the orchestration decision is still too weak.

Back to [10.1 Agentic Foundations](10-01-00-agentic-foundations.md).
