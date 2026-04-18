# 12.1.2 Decision Boundaries And Escalation Heuristics

_Page Type: Decision Guide | Maturity: Review-Ready_

Use this page when a team knows system behavior must improve but has not yet earned the right to choose fine-tuning or retraining. The goal is to identify the dominant adaptation lane, keep the lighter options visible, and make sure cost, evaluation burden, data dependence, and lock-in rise only when the evidence justifies them.

## Decision Lanes

| Lane | Use it when the main question is... | Default posture |
| --- | --- | --- |
| Prompt-and-workflow lane | whether the failure is really underspecified instructions, weak structure, or missing review controls | tighten prompts, schemas, routing, approval steps, and task-specific evaluation before touching weights |
| Retrieval-first lane | whether the system is failing because facts change quickly, citations are weak, or source coverage is incomplete | improve retrieval coverage, freshness, provenance, and permission handling before any tuning step |
| Parameter-efficient tuning lane | whether a stable, repetitive task has hit a plateau after strong prompt and retrieval baselines | use narrow fine-tuning only with labeled data discipline, explicit rollback, and release-gate evaluation |
| Classical retraining lane | whether the issue is a predictive-model drift, feature-quality, or label-regime problem rather than an LLM behavior problem | run a governed retraining cycle with data review, holdout or backtest evidence, and updated monitoring thresholds |

## Practical Heuristics

- Start with the lightest reversible intervention that can plausibly close the failure mode.
- Do not fine-tune to solve freshness, permissions, or source-governance problems; those belong in retrieval and data-boundary work first.
- Require a prompt-only or prompt-plus-retrieval baseline before approving weight adaptation, otherwise the team cannot show that heavier change was necessary.
- Treat model-specific tuning formats, hosted training pipelines, and non-portable adapter choices as sourcing decisions, not only technical details.
- Raise the evidence bar when adaptation creates persistent state, uses sensitive internal data, or changes a release path that many teams depend on.
- For classical ML systems, assume retraining is incomplete unless the monitoring regime, drift thresholds, and business-loss assumptions are refreshed too.

## Escalate When

- the team cannot name the failure category it is trying to fix or the metric that proves improvement
- proposed training data has unclear provenance, licensing, consent, or retention posture
- the adaptation path would make rollback slower than the business can tolerate
- the system serves regulated, high-impact, or externally exposed decisions and the release gate has not been expanded accordingly
- a vendor-managed tuning workflow would materially change portability, sovereignty, or long-term operating cost
- prompt, retrieval, and workflow controls have not been tried seriously but the team is already treating weight changes as inevitable

## Adaptation Anti-Patterns

- escalating because stakeholders are impatient rather than because the lighter lane failed on evidence
- using fine-tuning to encode rapidly changing business facts that should stay in governed source systems
- comparing a tuned model only against a weak baseline instead of the best prompt, workflow, and retrieval version
- treating vendor-hosted tuning as lower-governance work simply because infrastructure details are abstracted away
- importing LLM adaptation language into a classical ML drift problem and skipping retraining discipline

## Chapter Handoffs

- [11. Knowledge Retrieval And Memory](../11-knowledge-retrieval-and-memory/11-00-00-knowledge-retrieval-and-memory.md) when the real problem is freshness, provenance, permissions, or memory scope.
- [13. Evaluation Testing And QA](../13-evaluation-testing-and-qa/13-00-00-evaluation-testing-and-qa.md) when adaptation cannot proceed without stronger baselines, regressions, and release gates.
- [14. Observability Logging And Monitoring](../14-observability-logging-and-monitoring/14-00-00-observability-logging-and-monitoring.md) when drift, rollback detection, or post-release monitoring becomes the dominant risk.
- [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md) when portability, supplier dependence, or hosting posture changes more than model quality alone.

## Practical Reading Rule

Escalate up the adaptation ladder only after the lower rung has been tested and documented. If the chosen path increases data dependence, release burden, or supplier lock-in, the evidence pack should become stronger, not thinner.

Back to [12.1 Adaptation Foundations](12-01-00-adaptation-foundations.md).
