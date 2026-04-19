# 15.2.1 Worked Security Scenarios

_Page Type: Worked Example | Maturity: Review-Ready_

These scenarios turn the chapter's threat and control language into concrete operating review. Each one shows what should already exist before rollout widens or an incident is treated as contained.

## Internal Assistant Exposed To Prompt Injection

| Field | Decision |
| --- | --- |
| System | Internal retrieval-backed assistant used for policy, support, or knowledge lookup |
| Dominant threat | Retrieved or pasted content tries to override instructions, exfiltrate secrets, or trigger unsafe tool use |
| Operating shape | Retrieval results are treated as untrusted input, tools are deny-by-default, and high-risk actions require human approval or a separate bounded workflow |
| Required evidence | Injection test pack, tool permission manifest, blocked-action examples, citation review, and escalation path for suspicious prompts or documents |
| Release question | Can the assistant stay useful while refusing context-sourced instructions that conflict with policy or privilege limits? |
| Re-review trigger | Reopen review with chapters `09`, `14`, and `16` when new tools, broader retrieval domains, or looser approval paths are proposed |

## Tool-Using Workflow With External Side Effects

| Field | Decision |
| --- | --- |
| System | Workflow agent that can create tickets, change records, messages, or low-risk operational actions |
| Dominant threat | Broad tool grants turn output mistakes, prompt attacks, or ambiguous instructions into real system changes |
| Operating shape | Capabilities are narrowed to approved action classes, preconditions are explicit, approvals are logged, and rollback is tested before automation expands |
| Required evidence | Tool inventory, approval-path tests, rollback drill, denied-action coverage, and named owners for emergency disablement |
| Release question | Is every allowed action bounded tightly enough that a failure remains reversible and reviewable? |
| Re-review trigger | Reopen chapters `10`, `14`, and `16` when the workflow gains new tools, background autonomy, or reduced approval latency |

## Persistent Memory With Sensitive Or Role-Scoped State

| Field | Decision |
| --- | --- |
| System | Assistant or agent with cross-session memory for preferences, workflow state, or user-authored notes |
| Dominant threat | Memory quietly accumulates sensitive facts, stale authority, or state that outlives the original permission context |
| Operating shape | Memory fields are typed and minimal, retention and deletion are explicit, role-sensitive content is excluded or separately governed, and memory writes are observable |
| Required evidence | Approved memory schema, retention schedule, deletion test, access-review output, and examples of rejected memory writes |
| Release question | Does persistence improve continuity without becoming an ungoverned store of sensitive or high-authority facts? |
| Re-review trigger | Reopen chapters `06`, `11`, and `14` when memory starts storing new sensitive attributes, policy content, or cross-border user state |

## Gateway-Centered Abuse Investigation

| Field | Decision |
| --- | --- |
| System | Multi-model deployment routed through a gateway with policy enforcement, logging, and provider controls |
| Dominant threat | Abuse or leakage signals are split across application logs, gateway traces, and provider events so investigators cannot reconstruct the real path |
| Operating shape | Gateway decisions, route identifiers, policy outcomes, and downstream provider calls are linked to application events and incident ownership |
| Required evidence | Correlated incident timeline example, route-policy audit log, export test for gateway telemetry, and playbook for disabling risky routes or models |
| Release question | Can the team reconstruct who asked what, which policy fired, which provider handled it, and what containment action followed? |
| Re-review trigger | Reopen chapters `09`, `14`, and `18` when route logic changes, provider regions expand, or telemetry export becomes vendor-dependent |

## Cross-Scenario Review Signals

- security review stays tied to the real system boundary: prompts, retrieval, tools, memory, routes, providers, and human approvals are all visible in one operating story
- every scenario names both preventive controls and reconstruction evidence; one without the other is not enough
- the strongest trigger for re-review is scope creep: new tools, broader memory, wider routing, or weaker approvals should reopen adjacent chapter decisions rather than be treated as minor tuning

Back to [15.2 Operating Security And Abuse Resistance](15-02-00-operating-security-and-abuse-resistance.md).
