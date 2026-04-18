# 4.3.2 Controls And Artifacts

_Page Type: Operational Artifact | Maturity: Review-Ready_

Use this page to make governance inspectable. A governance model is not operational until the organization can point to the artifacts, owners, and triggers that support approval, exception handling, and re-review.

## Readiness Checks

| Check | What must be true |
| --- | --- |
| System ownership | A named owner is accountable for the system after approval, not only during intake |
| Classification record | Risk, autonomy, user context, and regulated-use implications are documented |
| Control mapping | Policy statements are tied to concrete technical, process, or supplier controls |
| Release evidence | Evaluations, reviews, approvals, and exceptions are stored in a reviewable package |
| Exception handling | Deviations have owner, rationale, compensating controls, and expiry date |
| Re-review triggers | Material model, data, supplier, workflow, or incident changes reopen governance review |

## Minimum Artifact Set

- use-case classification record
- control mapping with owners
- approval log with reviewer roles
- exception register with expiry and compensating controls
- re-review trigger log
- linked evidence package for release or renewal

## Owner And Review Guidance

| Artifact | Primary owner | Revisit when... |
| --- | --- | --- |
| Classification record | Product or system owner | scope, autonomy, or user population changes |
| Control mapping | Governance owner with engineering and security input | controls or dependencies change |
| Approval log | Governance or program management | each formal approval or renewal |
| Exception register | Control owner plus approving authority | expiry nears or compensating controls weaken |
| Evidence package | Delivery owner plus QA and review functions | each release, reclassification, or significant incident |

## Release And Re-Review Prompts

- Which artifact would prove that this system stayed inside approved use boundaries?
- Which exception is still open, and why is it still justified?
- What changed since the last approval that should force re-review?
- If the supplier posture or data boundary changed tomorrow, which governance record would need immediate update?

Back to [4.3 Reference Points](04-03-00-reference-points.md).
