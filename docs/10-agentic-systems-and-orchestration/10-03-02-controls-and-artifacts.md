# 10.3.2 Controls And Artifacts

_Page Type: Operational Artifact | Maturity: Review-Ready_

This page turns the chapter into reusable operating material. Use it when an agent proposal has moved past concept discussion and the team needs a review packet that can survive release, incident response, and audit follow-up.

## Minimum Control Set

| Control | Why it exists | Owner |
| --- | --- | --- |
| Tool allowlist | Restricts the capability surface to explicitly reviewed actions | Platform or application owner |
| Approval matrix | Maps action classes to auto-approve, reviewer-approve, or forbid | Product plus risk owner |
| Budget and step caps | Limits runaway loops, cost growth, and over-delegation | Runtime owner |
| Trace collection | Preserves evidence for QA, incident review, and rollback analysis | Platform or observability owner |
| Rollback path | Defines how to stop, disable, or reverse the agent's effect | Service owner |

## Minimum Artifact Set

| Artifact | What it should contain |
| --- | --- |
| Tool inventory | Tool name, purpose, action class, data exposure, and owner |
| Approval matrix | Which actions need review, which are blocked, and who can approve exceptions |
| Failure playbook | Recovery path, disablement trigger, notification path, and evidence links |
| Pilot scope note | Allowed tasks, excluded tasks, environments, and time bounds |

## Review Prompts

- Which actions are reversible, and which require a stronger approval threshold?
- What evidence would show that the agent exceeded its intended scope?
- Which tool or environment creates the highest side-effect risk if the reasoning is wrong?

## Release Rule

Do not widen agent autonomy until the organization can name:

- the allowed action classes
- the approval path for irreversible actions
- the trace location for investigations
- the rollback path for failed or harmful execution

Back to [10.3 Reference Points](10-03-00-reference-points.md).
