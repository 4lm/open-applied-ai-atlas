# 10.2.2 Patterns And Anti-Patterns

_Page Type: Reference Sheet | Maturity: Draft_

Use this page during rollout, exception review, and autonomy expansion to recognize healthy agent operating shapes before a promising pilot turns into broad tool access, weak investigation traces, and unowned side effects.

## Reusable Agent Operating Patterns

| Pattern | What good looks like | Fit signal | Review warning |
| --- | --- | --- | --- |
| Action-class register before autonomy expansion | Every allowed action is typed as recommend, draft, execute, approve, or forbidden, with the approval path, rollback expectation, and owning team recorded before new tools are exposed | the pilot is about to move from content generation into ticket updates, workflow steps, or external system calls | teams can list tools, but not which action classes they enable or which actions are irreversible |
| Tool boundary plus environment separation | Read-only tools, sandboxed write tools, and privileged production actions are split across separate credentials, environments, or execution paths so one prompt path cannot silently cross trust boundaries | the same agent is being asked to support analysis, staging changes, and production actions | "one agent with all the tools" is being presented as simpler than maintaining explicit boundaries |
| Workflow-backed agent loop | The agent handles planning or interpretation, while durable state, retries, approvals, deadlines, and completion signals stay in a workflow or ticketing layer that survives model variability | the business process already has owners, SLAs, or audit expectations, but some dynamic routing or synthesis still adds value | reviewers hear about autonomy and reasoning quality, but not where state, retries, or human handoffs actually live |
| Trace-first execution with replayable evidence | Plan steps, tool calls, approvals, retrieved context, outputs, and disablement events are captured in one investigation path so incidents can be reconstructed without relying on chat transcripts alone | the system will touch regulated workflows, customer-facing operations, or privileged internal systems | the only evidence is chat history, vendor dashboards, or screenshots collected after the fact |
| Time-bounded pilot envelope with tested fallback | Scope, allowed environments, step limits, budget limits, human escalation, and kill-switch behavior are defined up front, with a known fallback workflow if the agent is disabled | a pilot is expanding beyond a demo into shared internal use or light production traffic | the team can explain the happy path, but not how work continues when the agent is paused, wrong, or unavailable |
| Named memory and delegation boundaries | Conversation memory, task state, queued work, and any multi-agent delegation are all bounded by explicit retention rules, ownership, and escalation paths so autonomy does not hide state growth | the team wants longer-lived tasks, background jobs, or cooperating agents to reduce operator effort | memory, delegation, or background execution is described as a product feature rather than as a control and ownership decision |

## Agent Operating Anti-Patterns

| Anti-pattern | Why it fails | Early signal | Review action |
| --- | --- | --- | --- |
| Agent label as a substitute for operating design | The team ships a vocabulary change, not a control model, so tool scope, approval logic, ownership, and fallback remain implicit | proposals emphasize planner quality or framework choice more than allowed actions, evidence, or rollback | send the review back to [10.1 Agentic Foundations](10-01-00-agentic-foundations.md) and require a named autonomy level plus a workflow comparison |
| Broad tool access before action typing | One generalized capability surface turns minor reasoning mistakes into production side effects because permissions were not split by consequence | credentials are issued before the review packet defines read-only, bounded-write, and forbidden action lanes | block rollout and reopen [9. Model Gateways And Access Control](../09-model-gateways-and-access-control/09-00-00-model-gateways-and-access-control.md), [15. Security And Abuse Resistance](../15-security-and-abuse-resistance/15-00-00-security-and-abuse-resistance.md), and [16. Human Oversight And Operating Model](../16-human-oversight-and-operating-model/16-00-00-human-oversight-and-operating-model.md) |
| Prompt-only state with no durable workflow anchor | Retries, approvals, deadlines, and partial progress disappear into chat history, making failures hard to resume, audit, or govern | the design cannot explain where pending work, handoffs, or retries live outside the model session | require a workflow or case-management boundary before more autonomy is approved |
| Browser or desktop autonomy normalized too early | Rich user-interface access magnifies side effects and trust-boundary crossings before the team can prove containment, evidence, or rollback | browser pilots start touching production consoles, finance systems, or personal data before sandboxing and replay are mature | narrow the scope, add session isolation and traceability, and reopen security and oversight review |
| Human review theater | A nominal approval step exists, but reviewers cannot see enough evidence, time, or context to make a real intervention decision | the approver sees only a final suggestion or button click with no trace of tool calls, retrieved context, or intended side effects | strengthen the review packet with [10.3.2 Controls And Artifacts](10-03-02-controls-and-artifacts.md) and chapter `13` release evidence before expansion |
| Delegation sprawl without ownership | Multi-agent or background-task patterns increase concurrency and hidden state while nobody owns queue health, escalation, or stale-task cleanup | teams talk about specialist sub-agents or autonomous retries, but cannot name queue owners, retention limits, or stop conditions | reopen chapter `11`, chapter `14`, and chapter `16` before approving longer-lived delegation |

## Review Prompts

- Which operating pattern best matches the current stage: typed action classes, split tool boundaries, workflow-backed autonomy, trace-first execution, a time-bounded pilot, or named memory and delegation boundaries?
- What evidence proves the agent can be interrupted, investigated, and de-scoped without losing work, hiding side effects, or breaking the underlying workflow?
- Which anti-pattern is most likely after rollout pressure arrives: agent-label theater, broad tool access, prompt-only state, premature browser autonomy, weak human review, or delegation sprawl?
- Which adjacent chapter must re-enter before approval: `09`, `11`, `13`, `14`, `15`, `16`, or `18`?

## Re-Review Triggers

- a new tool class, privileged credential, browser surface, or external system is added to the agent's action set
- the system moves from recommendation or drafting into direct execution, approval, or long-running delegated work
- memory retention, retrieval scope, or queued-task persistence changes enough that the original state boundary no longer holds
- incident review shows missing trace coverage, unclear rollback ownership, or unresolvable side effects
- the operating model starts depending on one managed framework or console for investigation, policy, or task recovery in a way that changes portability assumptions

## Practical Reading Rule

Use these patterns after the team already has a plausible agent use case but before it treats rollout as an implementation detail. If the proposal cannot show typed actions, separated tool boundaries, durable workflow anchors, reconstructable traces, bounded pilots, and owned delegation or memory rules, the agent operating design is not ready.

Back to [10.2 Operating Agentic Systems](10-02-00-operating-agentic-systems.md).
