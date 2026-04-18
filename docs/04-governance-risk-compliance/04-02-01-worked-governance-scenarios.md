# 4.2.1 Worked Governance Scenarios

_Page Type: Worked Example | Maturity: Review-Ready_

These scenarios show how governance should change across different consequence profiles. The point is not to make every system heavy; it is to make ownership, evidence, and escalation proportionate.

## Low-Risk Internal Assistant Review

| Field | Decision |
| --- | --- |
| Context | A team wants an internal drafting assistant for low-consequence knowledge work |
| Recommended posture | Lightweight governance with named owner, approved use boundaries, and release evidence proportional to the risk |
| Why | Internal use lowers exposure, but it does not remove ownership, logging, and exception needs |
| Watch for | Treating "internal only" as a reason to skip classification and evidence capture |
| Control implications | Acceptable-use policy, model/provider approval, basic eval pack, and incident escalation route |
| Adjacent chapters | `06`, `13`, `15` |

## Regulated Advisory Workflow

| Field | Decision |
| --- | --- |
| Context | Analysts use an AI-assisted workflow to support regulated case handling |
| Recommended posture | Formal governance lane with documented classification, legal input, release gate, and periodic re-review |
| Why | Advisory systems can still affect regulated outcomes even without taking final action automatically |
| Watch for | Assuming human review alone removes the need for evidence and recurring control checks |
| Control implications | Risk record, approval log, scenario-based evaluation, exception handling, and change-triggered re-review |
| Adjacent chapters | `06`, `13`, `16`, `20` |

## Vendor Exception Process

| Field | Decision |
| --- | --- |
| Context | A business unit wants a strategically useful managed service with weak portability and limited transparency |
| Recommended posture | Time-bounded exception with compensating controls, explicit owner, and exit review |
| Why | Some dependencies are worth accepting, but only if the risk is named rather than normalized by default |
| Watch for | Letting a one-off exception become a hidden platform standard |
| Control implications | Exception register, portability review, supplier due diligence, and review expiry date |
| Adjacent chapters | `06`, `17`, `18` |

## Post-Incident Governance Loop

| Field | Decision |
| --- | --- |
| Context | A live system causes a significant failure and the team proposes only a technical patch |
| Recommended posture | Incident plus governance re-review, including whether controls, thresholds, ownership, or release criteria need to change |
| Why | Repeated incidents often reveal governance design gaps, not only implementation bugs |
| Watch for | Closing the ticket without updating policy, evidence standards, or review triggers |
| Control implications | Incident record, root-cause review, revised control mapping, and mandatory re-approval before wider rollout |
| Adjacent chapters | `13`, `14`, `15`, `16` |

Back to [4.2 Operating The Governance Model](04-02-00-operating-the-governance-model.md).
