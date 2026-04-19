# 12.1 Adaptation Foundations

_Page Type: Chapter Index | Maturity: Draft_

This section establishes the decision frame teams need before they argue about fine-tuning or retraining. Use it to separate prompt, retrieval, tuning, and classical retraining paths by failure type, data dependence, rollback friction, and sourcing consequences so heavier adaptation is justified rather than assumed.

## Section Map

- 12.1.1 [Adaptation Paths, Costs, And Core Distinctions](12-01-01-adaptation-paths-costs-and-core-distinctions.md)
- 12.1.2 [Decision Boundaries And Escalation Heuristics](12-01-02-decision-boundaries-and-escalation-heuristics.md)

## What This Section Helps Decide

- whether the dominant problem is weak task design, missing knowledge access, unstable model behavior, or classical-model drift
- which adaptation rung is the lightest plausible intervention and what evidence is required before escalation
- what new data, evaluation, rollback, portability, or lock-in burden appears once work moves from prompts into persistent state or weight changes
- when retrieval, evaluation, monitoring, or sourcing chapters should take over because adaptation is no longer the main question

## Reading Boundaries

- Start with [12.1.1 Adaptation Paths, Costs, And Core Distinctions](12-01-01-adaptation-paths-costs-and-core-distinctions.md) when the team needs stable boundaries between prompt optimization, retrieval design, parameter-efficient tuning, full fine-tuning, and classical retraining.
- Continue to [12.1.2 Decision Boundaries And Escalation Heuristics](12-01-02-decision-boundaries-and-escalation-heuristics.md) when the issue is choosing the default lane, naming escalation triggers, and documenting why lighter options were insufficient.
- Move to [12.2 Operating Adaptation Work](12-02-00-operating-adaptation-work.md) when a likely path is chosen and the question becomes rollout evidence, rollback, release gates, and re-review triggers.
- Revisit [11. Knowledge Retrieval And Memory](../11-knowledge-retrieval-and-memory/11-00-00-knowledge-retrieval-and-memory.md) when freshness, provenance, permissions, or memory scope matter more than model behavior.
- Revisit [13. Evaluation Testing And QA](../13-evaluation-testing-and-qa/13-00-00-evaluation-testing-and-qa.md), [14. Observability Logging And Monitoring](../14-observability-logging-and-monitoring/14-00-00-observability-logging-and-monitoring.md), or [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md) when the binding question is proof, post-release drift, or platform dependence rather than adaptation method alone.

Back to [12. Training Fine-Tuning And Adaptation](12-00-00-training-fine-tuning-and-adaptation.md).
