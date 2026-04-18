# 5.2.1 Worked Use-Case Scenarios

This subsection turns the chapter into concrete organizational situations so the abstractions can be checked against real delivery contexts. The examples are comparative on purpose: the same tool category may appear in several rows, but the use-case family, control model, and sourcing posture still differ.

## Representative Scenarios

| Scenario | Primary family | Typical adjacent chapters | What to watch for |
| --- | --- | --- | --- |
| Enterprise chat assistant | Knowledge work assistance | 6, 11, 13 | Grounding, permission-aware retrieval, over-trust |
| Internal knowledge assistant | Organizational knowledge systems | 6, 11, 14 | Provenance, deletion, state sprawl |
| Coding assistant | Software and IT engineering | 13, 15, 18 | Local speed hiding downstream quality or lock-in cost |
| Coding agent | Agentic task execution | 10, 13, 15 | Tool permissions, rollback, approval design |
| Workflow agent | Agentic task execution | 10, 15, 16 | Execution bounds, traceability, escalation |
| Document processing | Business process automation | 4, 6, 13 | Confidence misuse, exception routing, evidence gaps |
| Forecasting service | Decision support | 3, 13, 14 | Drift, business interpretation, false precision |
| Recommendation system | Decision support | 3, 13, 17 | Feedback loops, concentration of influence, fairness |
| Anomaly detection | Decision support or operations and back office | 13, 14, 16 | Alert fatigue, threshold quality, ownership gaps |
| Computer vision inspection | Domain-specific intelligence | 6, 13, 16 | Dataset fit, false negatives, reviewer burden |
| Compliance assistant | Knowledge work assistance | 4, 6, 20 | Unsupported answers becoming policy decisions |
| QA/test generation | Software and IT engineering | 13, 15 | False confidence from low-value generated output |
| Enterprise search | Organizational knowledge systems | 6, 11 | Permission leakage, stale content, relevance drift |
| RAG system | Organizational knowledge systems | 6, 11, 13 | Retrieval quality treated as solved because generation looks fluent |
| Model evaluation pipeline | AI production systems | 13, 14 | Weak metric discipline and poor change visibility |
| Observability and monitoring system | AI production systems | 14, 16 | Under-scoping because it is framed as support tooling |

## Reading Notes

- The same organization may need several of these families at once; do not force them into one “AI platform” story too early.
- If a row affects rights, regulated outcomes, or action-taking execution, route it through governance and oversight chapters before broad rollout.
- If a row mainly exists to support other AI systems, do not treat it as secondary; those support systems often determine whether the portfolio is governable at all.

Back to [5.2 Applying Use-Case Portfolios](05-02-00-applying-use-case-portfolios.md).
