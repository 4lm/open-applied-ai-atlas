# 12.2.2 Patterns And Anti-Patterns

_Page Type: Reference Sheet | Maturity: Draft_

Use this page during design, release, and renewal review to recognize healthy adaptation shapes before teams turn prompt gaps, retrieval gaps, or unmanaged drift into unnecessary tuning programs.

## Reusable Adaptation Patterns

| Pattern | What good looks like | Fit signal | Review warning |
| --- | --- | --- | --- |
| Prompt-first stabilization with versioned controls | Task instructions, schemas, routing, approval steps, and prompt versions are treated as a managed release surface with evals and rollback before any weight change | failures are mostly style, formatting, task decomposition, or reviewer-consistency problems | the team cannot show the strongest prompt-only baseline, but is already planning fine-tuning |
| Retrieval-before-training for changing knowledge | Source coverage, freshness, provenance, and citation behavior are improved before adaptation work is approved | answers depend on product, policy, or operational knowledge that changes faster than a tuning cycle should | training data starts filling with copied knowledge articles or internal facts that already belong in governed source systems |
| Narrow tuning with explicit baseline, registry, and rollback | Parameter-efficient tuning is limited to a stable task, compared against strong prompt-plus-retrieval baselines, and released with rollback checkpoints and owner approval | the task is repetitive, labels are durable, and prompt or retrieval gains have plateaued | the tuning path is justified mainly by stakeholder impatience, with weak evidence on data quality or portability cost |
| Governed retraining cycle for predictive systems | Retraining is tied to drift diagnosis, feature and label review, holdout or backtest evidence, and refreshed monitoring thresholds | the system is a forecasting, ranking, anomaly-detection, or classification workflow under changing data conditions | the proposal borrows LLM fine-tuning language while skipping data-window, label-quality, or business-loss review |
| Managed adaptation with explicit sourcing guardrails | Vendor-hosted tuning or training is approved only with clear data-handling, portability, cost, and exit-position review | staffing or delivery constraints make managed adaptation realistic, but the organization still needs a defensible control posture | teams treat hosted training as low-governance simply because infrastructure detail is abstracted away |

## Adaptation Anti-Patterns

| Anti-pattern | Why it fails | Early signal | Review action |
| --- | --- | --- | --- |
| Tuning to solve freshness, permissions, or source hygiene | Weight changes add cost and lock-in while the real problem remains retrieval design, provenance, or access control | the issue statement mentions stale answers, missing citations, or role leakage more than model behavior | return the team to chapter `11` and require proof that retrieval and source governance are already sound |
| Escalation without the best lighter baseline | The team cannot prove heavier adaptation was necessary if prompt, workflow, and retrieval baselines were weak | evaluation compares the tuned system only against an early prompt draft or no retrieval variant at all | block approval until a credible lighter-path baseline exists |
| Adapter or model-variant sprawl with no release discipline | Local experiments turn into an ungoverned estate of checkpoints, adapters, and hidden behavior changes | multiple tuned variants exist, but owners cannot name the production baseline, rollback target, or retention rule | require model registry entries, release gates, and retirement rules before another variant ships |
| Retraining treated as routine batch maintenance | Drift, business-loss shifts, and label quality change over time, so blind retraining can refresh the wrong behavior | retraining cadence is described, but no one can show updated drift evidence or current success criteria | reopen evaluation and monitoring review with chapters `13` and `14` |
| Managed platform dependence hidden as implementation convenience | Hosted adaptation may solve speed problems while quietly changing portability, sovereignty posture, and long-term spend | the business case focuses on faster delivery, but not on model export, contract terms, or region and data handling constraints | pull chapter `18` into the decision and document exit posture before approval |

## Review Prompts

- Which adaptation pattern best fits the dominant failure mode: prompt stabilization, retrieval-first repair, narrow tuning, retraining, or managed adaptation with sourcing review?
- What evidence proves the lighter path was tried seriously before a heavier one was approved?
- Where do rollback, owner assignment, and retirement rules live for prompts, indexes, adapters, checkpoints, or retrained models?
- Which chapter must re-enter before release: `11`, `13`, `14`, `16`, or `18`?

## Re-Review Triggers

- a prompt-only system keeps accreting retrieval layers, memory, and tuning requests because nobody has named the primary failure type
- new tuning data arrives without clear provenance, labeling policy, consent posture, or retention rules
- evaluation results look better only on the team's preferred benchmark while business-critical regressions remain unmeasured
- rollback depends on ad hoc notebook state or vendor console history rather than a controlled release artifact
- a hosted adaptation workflow becomes harder to leave because export, regional deployment, or audit visibility were never checked up front

## Practical Reading Rule

Use these patterns after the adaptation lane is chosen but before the rollout is treated as safe. If the team cannot explain why a lighter path was insufficient, what new burden the heavier path creates, and how it will exit or roll back, the review is not finished.

Back to [12.2 Operating Adaptation Work](12-02-00-operating-adaptation-work.md).
