# 16.3.2 Controls And Artifacts

_Page Type: Operational Artifact | Maturity: Draft_

Use this page when a team says a system has "human oversight" and a reviewer needs proof that the phrase maps to real owners, thresholds, approval rights, and intervention paths. The point is not to create bureaucracy. The point is to make accountability, escalation, and exception handling inspectable before scale, incident pressure, or vendor dependence turns vague oversight promises into operational drift.

## Minimum Oversight Control Pack

| Control or artifact | What it should make explicit | Typical owner | Review trigger |
| --- | --- | --- | --- |
| Decision-rights matrix | Which decisions are delegated, which require human approval, who can veto, and which roles only advise | Product, service, or risk owner | New workflow, autonomy increase, or policy change |
| Approval-threshold register | Which changes or actions are auto-allowed, peer-reviewed, manager-approved, or risk-approved, plus which actions are forbidden | Product plus governance owner | New tool, action class, or user-impact tier |
| Human-handoff design | Escalation triggers, queue owner, service-level expectation, fallback path, and user-visible messaging when automation stops | Operations or service owner | New customer journey, channel, or support model |
| Change-review cadence and gate | Which model, prompt, retrieval, policy, routing, or workflow changes require review before release and who signs off | Release owner plus accountable manager | Every production change or emergency exception |
| Exception and residual-risk log | Approved deviations, why they were accepted, who approved them, what expiry applies, and what review would close them | Risk, compliance, or designated approver | Exception request, audit, or recurring incident |
| Approver competency and access record | Who is allowed to approve or override, what training or context they need, and how access is rotated or removed | Team lead, HR enablement, or platform admin | New approver, reorg, or access review |
| Incident decision log | Who decided what during a failure, when humans intervened, what was paused, and what evidence supports the decision | Incident commander or service owner | Sev incident, rollback, or customer complaint |
| Portability and dependency note | Which parts of oversight depend on vendor-specific dashboards, moderation features, routing, or case management and how evidence would be exported if the supplier changes | Architecture, procurement, or platform owner | Vendor onboarding, renewal, or exit planning |

## Release-Ready Oversight Packet

Before launch or material change, reviewers should be able to inspect the following in one place:

- the current decision-rights matrix with named accountable owners for every irreversible or high-consequence action
- the approval-threshold register showing which changes are blocked, which need review, and who can authorize exceptions
- the human-handoff design with queue ownership, response expectation, and user-visible fallback behavior
- the current exception log, including open residual risks, expiry dates, and pending remediation
- evidence that named approvers and override holders were trained, briefed, and still have valid access
- the incident decision-log template or latest completed example showing how intervention decisions are captured
- the portability note for any vendor-managed oversight surface the team would rely on during incident review or audit

## Oversight Drill

Run at least one realistic review or tabletop before broad rollout.

| Drill question | Evidence reviewers should expect |
| --- | --- |
| Can the team name who may stop, continue, or override the system during a high-consequence event? | Decision-rights matrix, named roles, and current contact path |
| Can the team show which model, policy, or workflow changes can ship without human approval and which cannot? | Approval-threshold register and change gate record |
| Can a user-facing handoff happen predictably when confidence, policy, or operating conditions fall outside bounds? | Handoff trigger rules, queue owner, and fallback message or SOP |
| Can reviewers reconstruct why an exception was granted and whether it has expired? | Exception log, approver name, rationale, and expiry or remediation link |
| If the team lost access to a vendor console tomorrow, could it still recover the evidence needed for incident review? | Portability note, export path, and alternate evidence source |

## Failure Signs

- The team says a human is "in the loop," but cannot show which actions actually stop for human approval versus only generate a notification.
- The same person who benefits from faster automation also holds unchecked override authority with no second-level review.
- Escalation exists in principle, but nobody owns the queue, response expectation, or user communication path.
- Exception handling lives in chat threads or email instead of a durable register with expiry and remediation tracking.
- Critical oversight evidence only exists inside a vendor-specific dashboard or ticketing workflow with no export or continuity plan.

## Approval Prompt

If the team cannot show which artifact defines decision rights, which record proves exception approval, and which handoff path lets a human intervene before harm spreads, the oversight model is not yet ready.

Back to [16.3 Reference Points](16-03-00-reference-points.md).
