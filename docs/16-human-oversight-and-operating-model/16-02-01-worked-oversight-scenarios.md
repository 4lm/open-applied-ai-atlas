# 16.2.1 Worked Oversight Scenarios

_Page Type: Worked Example | Maturity: Review-Ready_

These scenarios turn oversight language into operating review. Each one shows the human decision rights, evidence, and re-review trigger that should already exist before a team claims people are meaningfully in control.

## Internal Assistant With Expert Escalation

| Field | Decision |
| --- | --- |
| System | Internal assistant for policy, HR, or support knowledge with a required handoff path for uncertain or sensitive cases |
| Oversight pressure | Teams treat escalation as a soft promise, but nobody owns the queue, response time, or final answer authority once confidence drops |
| Operating shape | The assistant may draft or route, but named human reviewers own exception decisions, sensitive interpretations, and final responses when policy ambiguity or user harm is plausible |
| Required evidence | Decision-rights matrix, handoff trigger rules, queue ownership, fallback message, training record for approvers, and one completed escalation example |
| Release question | Can the team prove who decides when the assistant stops, who answers next, and how users are protected from silent dead ends or vague "someone will review this" promises? |
| Re-review trigger | Reopen chapters `06`, `11`, and `14` when new sensitive data classes, retrieval sources, or support-access paths are introduced |

## Tool-Using Workflow With Bounded Human Approval

| Field | Decision |
| --- | --- |
| System | Workflow that drafts actions, calls tools, or prepares changes, but requires human approval before external effects occur |
| Oversight pressure | Approval becomes a rubber stamp because reviewers lack context, approvals are too frequent to inspect, or the workflow hides what would actually happen next |
| Operating shape | Allowed action classes are narrow, approval packets show the proposed action and evidence, override rights are named, and rollback ownership is clear before automation expands |
| Required evidence | Approval-threshold register, sample approval packet, denied-action examples, rollback drill, approver access record, and incident disablement path |
| Release question | Are humans approving a bounded action with enough evidence to say yes or no, or merely acknowledging that a system already decided? |
| Re-review trigger | Reopen chapters `10`, `14`, and `15` when new tools, background execution, or lower-friction approvals are proposed |

## High-Consequence Advisory Workflow

| Field | Decision |
| --- | --- |
| System | Advisory workflow in healthcare, finance, employment, benefits, or regulated case handling where the system recommends but a human remains accountable for the outcome |
| Oversight pressure | Teams downplay risk because the system is "only advisory," even though users or operators will predictably follow its recommendations under time pressure |
| Operating shape | The system can summarize, rank, or prefill, but human reviewers must confirm critical facts, record the final determination, and explain overrides or acceptance in durable case records |
| Required evidence | Review SOP, approval or sign-off record, competency requirements for reviewers, exception log, incident decision log, and user-facing disclosure of the human review point |
| Release question | Would an auditor or affected user be able to tell which judgment stayed human-owned and which system output merely informed it? |
| Re-review trigger | Reopen chapters `04`, `13`, and `20` when consequence level, regulatory classification, or audit obligations change materially |

## Central Platform With Federated Domain Teams

| Field | Decision |
| --- | --- |
| System | Organization-wide platform provides shared models, prompts, routing, and guardrails while domain teams own service outcomes and user relationships |
| Oversight pressure | The platform team gradually absorbs hidden approval power, or domain teams assume shared controls mean shared accountability |
| Operating shape | Central owners define control baselines and change gates, domain owners accept or reject local rollout, and cross-team review forums handle exceptions, incidents, and portfolio-wide changes |
| Required evidence | Layered decision-rights matrix, change-review cadence, domain sign-off record, exception register, vendor-dependence note, and one completed cross-team escalation example |
| Release question | Can the organization show where shared platform stewardship ends and where service-level accountability still sits with the domain owner? |
| Re-review trigger | Reopen chapters `09`, `17`, and `18` when gateway logic centralizes further, vendor dependence grows, or the platform begins forcing decisions that domain owners cannot inspect or contest |

## Cross-Scenario Review Signals

- real oversight is visible in named decision rights, bounded approvals, handoff ownership, and reconstructable records rather than in generic claims that a human is "in the loop"
- the strongest failure mode is authority drift: platform, vendor, or workflow convenience quietly changes who can approve, override, or stop the system without that shift being reviewed
- the most important re-review trigger is scope expansion, including new tools, broader data access, higher consequence use, or deeper managed-service dependence that changes who must stay accountable

Back to [16.2 Operating The Human Model](16-02-00-operating-the-human-model.md).
