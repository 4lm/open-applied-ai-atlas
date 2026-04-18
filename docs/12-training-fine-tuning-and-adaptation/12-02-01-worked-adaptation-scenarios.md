# 12.2.1 Worked Adaptation Scenarios

_Page Type: Worked Example | Maturity: Review-Ready_

Use these scenarios to test whether the team has a prompt-and-workflow problem, a retrieval problem, a justified fine-tuning case, or a broader retraining obligation. Each scenario is framed around the escalation decision, the recommended posture, and the evidence outputs that should exist before rollout or re-release.

## Internal Drafting Copilot Under Style Pressure

| Field | Decision |
| --- | --- |
| Context | A legal and policy team wants an internal drafting copilot to produce consistent summaries, action lists, and response templates across recurring document types |
| Dominant question | Can prompt structure, schemas, and workflow controls stabilize output quality, or is model adaptation already justified? |
| Recommended posture | Prompt-first stabilization with structured inputs, output schema checks, approval workflow, and versioned prompt evaluation before any fine-tuning |
| Why | Many early failures come from underspecified tasks, weak exemplars, and missing review controls rather than a model that lacks the needed capability |
| Evidence and control outputs | prompt and template registry, task-specific eval set, reviewer rubric, fallback workflow, rollback path for prompt versions |
| Watch for | Treating style inconsistency as proof that weights must change, merging multiple tasks into one benchmark, or skipping comparisons against the best prompt-only baseline |
| Adjacent chapters | `10`, `13`, `16`, `18` |

## Knowledge Assistant With Fast-Changing Source Material

| Field | Decision |
| --- | --- |
| Context | A product and support organization wants better answers about features, release notes, and internal procedures that change weekly |
| Dominant question | Is the failure caused by missing task adaptation, or is the system trying to solve a freshness problem with weight changes? |
| Recommended posture | Improve retrieval coverage, source freshness, chunking, and citation behavior before any fine-tuning or retraining step |
| Why | When the underlying knowledge changes quickly, retrieval and provenance usually solve the real problem with lower cost, lower lock-in, and better rollback posture than tuned weights |
| Evidence and control outputs | source inventory, refresh cadence, grounding eval set, citation check, stale-content regression test, owner escalation path |
| Watch for | Fine-tuning on product knowledge that will soon change, indexing unofficial copies, or using training as a substitute for source governance |
| Adjacent chapters | `06`, `11`, `13`, `18` |

## Domain-Specific Triage With Stable Labels

| Field | Decision |
| --- | --- |
| Context | A high-volume operations team routes support tickets or claims into a stable label set and has accumulated reviewed examples showing repeatable prompt-only failure modes |
| Dominant question | Has the task become stable and repetitive enough that fine-tuning is now more reliable or cheaper than continually expanding prompt scaffolding? |
| Recommended posture | Parameter-efficient fine-tuning only after prompt and retrieval baselines plateau, the label scheme is stable, and the team can support disciplined evaluation and rollback |
| Why | Narrow weight adaptation can pay off when the task is repetitive, labels are durable, and latency or consistency requirements make prompt-only control increasingly fragile |
| Evidence and control outputs | baseline comparison pack, labeled train/validation split, data-provenance note, model registry entry, rollback checkpoint, release gate tied to error categories |
| Watch for | Training on unresolved reviewer disagreement, using fine-tuning to hide poor workflow design, or accepting a vendor-specific tuning path without acknowledging exit costs |
| Adjacent chapters | `07`, `09`, `13`, `18` |

## Predictive Operations Model Under Drift

| Field | Decision |
| --- | --- |
| Context | A forecasting or anomaly-detection system that once performed well is now degrading because customer behavior, seasonality, or operational conditions have shifted |
| Dominant question | Does the system need threshold tweaks and monitoring changes, or is this a governed retraining cycle with updated data and validation obligations? |
| Recommended posture | Classical ML retraining with feature and label review, shadow evaluation, staged rollout, and refreshed monitoring thresholds rather than LLM-style adaptation shortcuts |
| Why | Predictive-system drift is usually a data and model-fit problem that must be handled through retraining discipline, not by rephrasing prompts or bolting on generative patterns |
| Evidence and control outputs | drift report, training-window decision, label-quality check, backtest or holdout results, rollout gate, monitoring reset plan |
| Watch for | Treating retraining as routine batch work without checking label drift, policy changes, or business-cost shifts that changed what good performance means |
| Adjacent chapters | `05`, `13`, `14`, `16` |

## Reading Rule

Escalate only when the lighter path has been tested and documented. If the proposed adaptation increases persistent state, data dependence, supplier lock-in, or release burden, the evidence pack should become stronger, not thinner.

Back to [12.2 Operating Adaptation Work](12-02-00-operating-adaptation-work.md).
