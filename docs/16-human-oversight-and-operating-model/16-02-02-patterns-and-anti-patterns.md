# 16.2.2 Patterns And Anti-Patterns

_Page Type: Reference Sheet | Maturity: Draft_

Use this page during rollout review, exception handling, and operating-model changes to recognize healthy oversight shapes before a visible reviewer, a ticket queue, or a vendor dashboard gets mistaken for meaningful human control.

## Reusable Oversight Operating Patterns

| Pattern | What good looks like | Fit signal | Review warning |
| --- | --- | --- | --- |
| Typed action and decision-right ladder | Every meaningful action is classified as advisory, prepare-for-approval, approve-or-deny, execute-under-human-order, or forbidden, with the accountable owner and stop right named before rollout expands | the system drafts messages, proposes decisions, or prepares changes that can affect customers, entitlements, records, or regulated outcomes | reviewers can describe the user journey, but cannot say which actions remain human-owned or which role can halt the system |
| Approval packet with evidence and rollback context | Human reviewers see the proposed action, key evidence, uncertainty signal, expected side effects, and rollback path in one place so approval is a real decision rather than acknowledgement theater | the workflow asks humans to approve external actions, sensitive communications, or higher-consequence case handling | approvers see only a final recommendation, score, or button click with no context about what would happen next |
| Staffed escalation lane with explicit fallback experience | Sensitive, ambiguous, or policy-breaking cases move into a queue with named owners, service expectations, and user-visible fallback handling instead of vanishing into an abstract "human review" promise | the service claims humans will step in when confidence drops, policies conflict, or harm-sensitive cases appear | the design names escalation, but nobody owns queue health, response targets, or how users are supported while waiting |
| Shared-control governance with service-level accountability | Platform, product, risk, and operations teams each own a bounded part of the oversight surface, while one service owner still accepts outcome risk and can stop or narrow the service | the organization uses shared models, shared gateways, or centralized policy tooling across multiple teams | a central platform or vendor effectively controls approvals or policy without visible service-owner acceptance of the consequences |
| Portable oversight evidence and intervention drill | Decision logs, approval records, overrides, pauses, exceptions, and vendor-mediated actions can be reconstructed from one review packet, and the team has practiced pausing or degrading the service | incident response, audit, or regulator review may require proving who intervened, why, and with what authority | the organization depends on screenshots, memory, or one managed console to explain an oversight decision after the fact |
| Reviewer-load guardrails with redesign trigger | Approval volume, queue size, and override behavior are monitored so the organization can detect when human review has become throughput theater and must be narrowed or redesigned | the service is scaling to more users, more cases, or lower-friction approvals where reviewer burden can quietly outgrow competence | the team celebrates growth while approval times, bulk approvals, or operator fatigue show humans are no longer exercising real judgment |

## Oversight Operating Anti-Patterns

| Anti-pattern | Why it fails | Early signal | Review action |
| --- | --- | --- | --- |
| Human-in-the-loop theater | visible people create comfort, but real oversight is absent because nobody can prove which actions stop, who may intervene, or what evidence informs the decision | proposals keep repeating that a human will review outputs, yet no typed action ladder or stop-right record exists | reopen [16.1 Oversight Foundations](16-01-00-oversight-foundations.md) and require explicit decision rights before broader rollout |
| Rubber-stamp approval queue | approvals become ceremonial when reviewers lack time, competence, or evidence, so the workflow still behaves like automation while pretending otherwise | approval latency matters more in planning than reviewer judgment quality, and override reasons are rare or never recorded | narrow the action set, strengthen the approval packet, and reopen [13. Evaluation Testing And QA](../13-evaluation-testing-and-qa/13-00-00-evaluation-testing-and-qa.md) plus [16.3.2 Controls And Artifacts](16-03-02-controls-and-artifacts.md) |
| Escalation dead end | a human handoff exists only as a promise, so unresolved cases linger, users lose trust, and frontline staff improvise outside the designed path | support, operations, or domain experts are named informally, but queue ownership, response targets, and fallback messaging are missing | block rollout expansion until the handoff path is staffed, tested, and visible to users and operators |
| Hidden approval power in platform or vendor layers | shared tooling, moderation, routing, or case management quietly determines what can happen, but service owners cannot inspect or contest those decisions | teams rely on managed controls or centralized policy without being able to export evidence, challenge changes, or degrade safely | reopen [09. Model Gateways And Access Control](../09-model-gateways-and-access-control/09-00-00-model-gateways-and-access-control.md), [17. Vendors Organizations And Market Structure](../17-vendors-organizations-and-market-structure/17-00-00-vendors-organizations-and-market-structure.md), and [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md) |
| Reviewer-overload drift | the original oversight model was proportionate at pilot scale, but higher volume, broader scope, or faster SLAs turn human review into a bottleneck that can no longer challenge the system | reviewers start bulk-approving, skipping evidence, or working outside stated escalation rules just to keep up | redesign the workflow, narrow autonomy, or move back to a lower-consequence lane before the queue normalizes unsafe shortcuts |
| Exception register without expiry or learning | temporary approvals become permanent operating loopholes, so the organization keeps risky behavior alive without proving the original controls now work | exceptions accumulate, nobody closes them, and the same edge cases reappear without design changes | reopen [04. Governance Risk Compliance](../04-governance-risk-compliance/04-00-00-governance-risk-compliance.md) and require expiry, owner, remediation, and repeat-incident review before more scope is added |

## Review Prompts

- Which operating pattern carries the most oversight weight here: typed decision rights, evidence-rich approval packets, staffed escalation, shared-control governance, portable evidence, or reviewer-load guardrails?
- What artifact proves a human can still say no, pause the service, or force fallback before harm spreads: decision-rights matrix, approval packet, queue SOP, intervention drill, or exception register?
- Which anti-pattern is most likely once rollout pressure arrives: oversight theater, rubber-stamp approvals, dead-end escalation, hidden platform power, reviewer overload, or permanent exceptions?
- Which adjacent chapter must re-enter before approval: `04`, `09`, `13`, `14`, `17`, or `18`?

## Re-Review Triggers

- a new action class, tool, or workflow step can produce broader side effects without revisiting the decision-right ladder
- approval volume, reviewer staffing, or service-level expectations change enough that humans can no longer inspect the evidence in time
- escalation begins involving new domains, regulated cases, or sensitive user groups without updating the fallback path and queue ownership
- a shared platform or vendor now mediates approvals, intervention logic, or evidence retention in ways service owners cannot independently inspect
- incidents, complaints, or audits show missing decision logs, unclear override authority, or unresolved exceptions that were treated as normal operations

## Practical Reading Rule

Use these patterns after the role map and oversight lane are clear but before the organization treats the operating model as production-ready. If the team cannot show typed decision rights, evidence-rich approval, staffed escalation, bounded shared control, portable intervention evidence, and a way to detect reviewer overload, the oversight design is not finished.

Back to [16.2 Operating The Human Model](16-02-00-operating-the-human-model.md).
