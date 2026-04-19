# 13.3.3 Evaluation Plan And Release Gate Templates

_Page Type: Operational Artifact | Maturity: Draft_

This page provides reusable templates for teams that need evaluation and release evidence to be reviewable rather than ad hoc.

## Evaluation Plan Template

| Field | What to capture |
| --- | --- |
| System and release scope | Which workflow, model, retrieval layer, or feature is under review |
| Target users and contexts | Who uses it, in which situations, and with what consequence profile |
| Failure modes | The concrete errors that matter most for this release |
| Evidence mix | Automated tests, human review, adversarial tests, shadow traffic, or replay sets |
| Thresholds | What counts as acceptable for launch, rollback, or escalation |
| Data sources | Gold sets, replay sets, synthetic cases, or live samples |
| Owners | Who signs off on eval design, run results, and exceptions |
| Re-run triggers | Model change, prompt change, retrieval update, policy update, or incident |

## Release Gate Template

| Gate question | Required evidence |
| --- | --- |
| Did the system pass the defined regression pack? | Regression report with run date and owner |
| Were high-consequence failure modes tested directly? | Scenario pack results and reviewer notes |
| Are known exceptions documented and approved? | Exception log with owner and expiry |
| Are observability and rollback paths live? | Monitoring links and rollback plan |
| Did governance, privacy, or security review add blocking actions? | Review outcome with linked artifacts |

## Minimal Approval Record

- release identifier
- scope of change
- evidence package location
- approving roles
- open exceptions
- next mandatory re-evaluation trigger

Back to [13.3 Reference Points](13-03-00-reference-points.md).
