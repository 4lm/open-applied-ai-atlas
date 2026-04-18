# 5.1.2 Portfolio Boundaries And Prioritization Heuristics

This subsection helps teams reason about which system families deserve early investment, heavier review, or stricter governance.

## Prioritization Heuristics

- Start with the consequence of failure, not the trendiness of the technique.
- Escalate review when the system affects rights, regulated decisions, safety, or sensitive data handling.
- Treat customer-facing, employee-facing, and infrastructure-facing systems differently because the accountability and evidence burdens differ.
- Use sovereignty and portability as decision lenses when the system depends on external runtimes, managed control planes, or cross-border data flows.

## Family-Specific Pressure Points

| System family | Pressure points |
| --- | --- |
| Knowledge work assistance | grounding quality, permissioning, and user over-trust |
| Forecasting and anomaly detection | decision quality, monitoring drift, operational interpretation |
| Recommenders and optimization | fairness, feedback loops, hidden policy bias, concentration of influence |
| Document intelligence and retrieval | privacy, retention, provenance, deletion, access control |
| Agentic workflows and coding agents | autonomy, tool execution, approval design, rollback, auditability |
| Customer-facing AI | service quality, policy compliance, escalation, and incident handling |
| Vision and speech systems | dataset quality, threshold setting, human review, false-positive and false-negative consequences |

## Portfolio Triage Table

| Triage condition | Default response |
| --- | --- |
| High-consequence decisions or rights impact | Start with governance, evaluation, and human oversight constraints before tool choice |
| Sensitive data with unclear boundary ownership | Resolve residency, retention, and processor posture before prototyping |
| Strong vendor concentration or exit concern | Prefer architectures and tools with clearer portability and operating control |
| Large-scale workflow execution | Treat approval design and rollback as primary scope, not as later hardening work |
| Internal productivity use case with low autonomy | Bias toward the smallest assistive pattern that solves the real workflow |

Back to [5.1 Use-Case Foundations](05-01-00-use-case-foundations.md).
