# 12.1.1 Adaptation Paths, Costs, And Core Distinctions

_Page Type: Concept Explainer | Maturity: Review-Ready_

Use this page to separate the main ways teams change system behavior: prompt and workflow adaptation, retrieval and knowledge adaptation, parameter-efficient tuning, broader fine-tuning, and classical retraining. Those paths are not interchangeable just because they all aim to improve output quality. They modify different system state, demand different evidence, and create different rollback and sourcing obligations.

## Adaptation-Path Map

| Adaptation path | What actually changes | Best fit | Main new burden | Common failure |
| --- | --- | --- | --- | --- |
| Prompt and workflow adaptation | instructions, schemas, routing, tool selection, approval steps, or other execution controls | the task is underspecified, unstable, or poorly decomposed even though the underlying model capability is likely sufficient | prompt versioning, eval baselines, reviewer consistency, and release discipline for configuration changes | treating weak task design as proof that model weights must change |
| Retrieval and knowledge adaptation | source coverage, chunking, metadata, ranking, citation behavior, freshness handling, or permission inheritance | answers depend on governed organizational facts that change faster than a tuning cycle should | source ownership, provenance, refresh cadence, access control, and deletion or revocation handling | encoding changing business facts into training data instead of fixing retrieval quality |
| Parameter-efficient tuning | narrow trainable deltas such as adapters or low-rank updates attached to a base model | a repetitive task has reached a clear prompt-plus-retrieval ceiling and needs stronger consistency, latency, or task fit | labeled data quality, baseline comparisons, model registry entries, and rollback for tuned variants | approving tuning because it feels more serious, not because lighter paths failed on evidence |
| Broader fine-tuning or post-training | a larger share of model behavior is updated through supervised or preference-based training | the organization truly needs deeper behavior change and can support the resulting lifecycle cost | higher compute demand, harder release gates, portability loss, and stronger supplier dependence if the method is platform-bound | treating a model-variant program as if it were a routine UX tweak |
| Classical model retraining | a predictive model is retrained on refreshed features, labels, or training windows | forecasting, ranking, classification, or anomaly-detection systems are degrading under drift or business-change pressure | data-window choice, label quality review, holdout or backtest evidence, and monitoring reset plans | importing LLM tuning language into a classical ML problem and skipping drift discipline |

## Core Distinctions

| Distinction | Why it changes the design |
| --- | --- |
| Behavior steering vs. knowledge access | If the model already knows how to do the task but lacks current facts, retrieval work is usually the right fix and tuning is not. |
| Configuration surface vs. trained artifact | Prompt, routing, and policy changes are usually easier to inspect and roll back than new model variants, checkpoints, or adapters. |
| Narrow task adaptation vs. broad behavior shift | Parameter-efficient tuning can solve a stable task without automatically justifying the governance burden of broader post-training. |
| Reversible release change vs. persistent estate change | Once adaptation creates new model artifacts, the organization needs ownership, registry, retirement, and rollback rules, not just experiment notes. |
| Adaptation method vs. sourcing posture | A managed tuning workflow changes portability, hosting dependence, and audit visibility even if the technical adaptation method looks familiar. |
| Generative adaptation vs. predictive retraining | LLM behavior work and classical ML drift work use different evidence, failure modes, and operating rhythms, so one vocabulary should not erase the other. |

## What These Distinctions Change In Practice

- Require the strongest credible prompt and retrieval baseline before approving any weight change.
- Treat changing organizational knowledge as a retrieval and source-governance problem unless the team can prove the real failure is behavioral rather than factual.
- Distinguish a narrow tuned variant from a broader post-training program because release burden, rollback friction, and supplier dependence rise sharply once model behavior changes more deeply.
- Treat hosted tuning and training as sourcing decisions as well as technical ones because data handling, exportability, regional control, and exit posture may change.
- For classical ML systems, refresh success metrics, drift thresholds, and monitoring plans when retraining is proposed; retraining is not complete when only the model weights changed.

## Reviewer Checks

- Can the team name which failure type it is addressing: task design, knowledge access, stable task fit, deeper model behavior, or predictive-model drift?
- What is the lightest path that could plausibly fix the problem, and what evidence shows that lighter path has been tried seriously?
- Which new persistent artifact will exist after the change: prompt version, retrieval index, adapter, tuned checkpoint, or retrained model?
- How will the team roll back the chosen adaptation path, and is that rollback speed proportionate to business risk?
- Does the proposal quietly change portability, sovereignty posture, or supplier dependence even if the stated goal is only quality improvement?

## Reading Rule

Use this page to classify the adaptation path before choosing it. Then move to [12.1.2 Decision Boundaries And Escalation Heuristics](12-01-02-decision-boundaries-and-escalation-heuristics.md) to decide which lane is proportionate. If the team still cannot say what state changes, what evidence is required, and what new operating burden appears, it has not earned a heavier adaptation choice yet.

Back to [12.1 Adaptation Foundations](12-01-00-adaptation-foundations.md).
