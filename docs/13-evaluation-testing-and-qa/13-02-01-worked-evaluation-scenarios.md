# 13.2.1 Worked Evaluation Scenarios

_Page Type: Worked Example | Maturity: Draft_

These scenarios show what a credible evidence package looks like in practice. The point is not to name a tool, but to define what must be proven before release.

## Internal Assistant Release

| Field | Decision |
| --- | --- |
| System | Retrieval-backed internal assistant |
| Evidence mix | Gold set, citation review, permission-leakage checks, reviewer notes |
| Release question | Can the team widen rollout without turning fluent answers into over-trusted policy? |
| Gate logic | Do not launch broadly if citations fail or reviewer disagreement remains high |

## Model Swap Behind A Gateway

| Field | Decision |
| --- | --- |
| System | Existing application with a model-routing change |
| Evidence mix | System-level regression pack, routing comparison, prompt replay, exception log |
| Release question | Did the gateway change alter downstream behavior even without app-code changes? |
| Gate logic | Treat routing changes as release events, not invisible infrastructure tweaks |

## Action-Capable Workflow Agent

| Field | Decision |
| --- | --- |
| System | Bounded ticket or task-resolution agent |
| Evidence mix | Success metrics, approval-path tests, rollback tests, tool misuse scenarios |
| Release question | Can the agent act safely inside the approved action classes? |
| Gate logic | Output quality is insufficient if approval handling or rollback behavior fails |

## Predictive Service Refresh

| Field | Decision |
| --- | --- |
| System | Forecasting or scoring service refresh |
| Evidence mix | Drift review, recalibration checks, operator review, post-release monitoring hooks |
| Release question | Does the refreshed model improve decisions in context, not just offline metrics? |
| Gate logic | Statistical improvement alone is not enough when operational interpretation changes |

Back to [13.2 Operating Evaluation And QA](13-02-00-operating-evaluation-and-qa.md).
