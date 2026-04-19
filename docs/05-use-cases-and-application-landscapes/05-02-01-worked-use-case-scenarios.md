# 5.2.1 Worked Use-Case Scenarios

_Page Type: Worked Example | Maturity: Draft_

These scenarios show how the chapter changes a real portfolio decision. Each one is framed around the pattern that should be chosen first, not around the tool someone wants to buy.

## Startup Knowledge Assistant

| Field | Decision |
| --- | --- |
| Context | A small team wants faster answers from internal product and policy material |
| Best-fit pattern | Retrieval-backed assistant |
| Why this pattern fits | Content changes often and the team needs citations more than persistent memory |
| Rejected default | Long-lived memory or agentic tool use from day one |
| Control implications | Source ownership, permission-aware retrieval, and citation review matter early |
| Adjacent chapters | `06`, `11`, `13` |

## Regulated Enterprise Claims Review

| Field | Decision |
| --- | --- |
| Context | Analysts need drafting support for policy-heavy review work |
| Best-fit pattern | Assistant with retrieval and human approval |
| Why this pattern fits | The task is interpretive, but outputs can influence regulated decisions |
| Rejected default | Autonomous action-taking agent |
| Control implications | Governance review, evidence capture, and policy-source provenance are mandatory |
| Adjacent chapters | `04`, `06`, `13`, `20` |

## Operations Forecasting Service

| Field | Decision |
| --- | --- |
| Context | An operations team wants demand forecasts and exception explanations |
| Best-fit pattern | Classical ML or hybrid predictive stack |
| Why this pattern fits | The core value comes from prediction quality, not language generation alone |
| Rejected default | Chat-first assistant marketed as “predictive AI” |
| Control implications | Drift monitoring, model refresh policy, and operator interpretation matter more than conversational polish |
| Adjacent chapters | `03`, `13`, `14` |

## Document Intake And Routing

| Field | Decision |
| --- | --- |
| Context | A business process needs extraction, validation, and routing of incoming forms |
| Best-fit pattern | Document intelligence workflow |
| Why this pattern fits | Structured extraction and exception handling are the real bottlenecks |
| Rejected default | Generic conversational assistant over raw documents |
| Control implications | Confidence thresholds, reviewer queues, and audit trails are more important than fluent text output |
| Adjacent chapters | `04`, `06`, `13` |

## Reader Rule

- The same organization may need several patterns at once; do not force them into one “AI platform” story too early.
- If a scenario affects rights, regulated outcomes, or action-taking execution, route it through governance and oversight chapters before broad rollout.
- If the support system determines whether another AI system is governable, treat it as core infrastructure rather than a secondary add-on.

Back to [5.2 Applying Use-Case Portfolios](05-02-00-applying-use-case-portfolios.md).
