# 6.2.1 Worked Privacy And Sovereignty Scenarios

_Page Type: Worked Example | Maturity: Draft_

These scenarios show how the same privacy question can lead to different answers once sovereignty, portability, and support control are considered explicitly.

## Managed Internal Assistant

| Field | Decision |
| --- | --- |
| Context | A team adopts a managed internal assistant for everyday staff productivity |
| Recommended posture | Moderate-risk managed posture with explicit logging, retention, and support-access review |
| Why | The main exposure often sits in prompts, logs, and support channels rather than model-training reuse alone |
| Watch for | Asking only whether prompts are used for training |
| Control implications | Data-flow map, retention setting review, support-access review, and user guidance on sensitive content |
| Adjacent chapters | `04`, `13`, `18` |

## Region-Pinned Managed Service

| Field | Decision |
| --- | --- |
| Context | A provider offers EU region pinning and claims stronger sovereignty posture |
| Recommended posture | Treat residency as one control within a broader operational-control review |
| Why | Region choice does not answer telemetry routing, support operations, subcontractor access, or exit posture |
| Watch for | Treating a regional deployment option as complete proof of sovereignty |
| Control implications | Subprocessor review, support-path review, export test, deletion evidence, and contractual override review |
| Adjacent chapters | `04`, `17`, `18`, `20` |

## Persistent Memory Feature

| Field | Decision |
| --- | --- |
| Context | A product team wants long-lived user memory to personalize outputs across sessions |
| Recommended posture | Approve only with explicit storage, deletion, access, and retention design |
| Why | Memory changes the system from transient interaction into durable recordkeeping |
| Watch for | Framing memory as only a user-experience enhancement |
| Control implications | Memory-state inventory, retention schedule, deletion workflow, and access-review logic |
| Adjacent chapters | `04`, `11`, `13` |

## Self-Hosted Sensitive Workflow

| Field | Decision |
| --- | --- |
| Context | A regulated team moves a sensitive workflow to self-hosted infrastructure to reduce exposure |
| Recommended posture | High-control deployment with explicit lifecycle, export, and observability design |
| Why | Self-hosting can improve control, but it does not solve retention, operator access, or evidence quality automatically |
| Watch for | Assuming self-hosting alone closes the review |
| Control implications | Operator-access controls, telemetry policy, deletion procedures, and re-review after architecture changes |
| Adjacent chapters | `04`, `14`, `18`, `19` |

Back to [6.2 Operating Data Boundaries](06-02-00-operating-data-boundaries.md).
