# 5.1.1 Task Classes, Autonomy, And Core Distinctions

This subsection ties system family to autonomy, control, and assurance expectations. It keeps worker assistance, decision support, and action-taking systems visibly separate so teams do not inherit the wrong operating model by accident.

## Key Lenses

| Use-case lens | What it clarifies |
| --- | --- |
| System family | Shows whether the dominant problem is prediction, ranking, generation, extraction, perception, or action |
| Autonomy level | Separates assistive systems from action-taking or workflow-driving systems |
| Governance pressure | Highlights where legal, quality, or human-oversight burden becomes sharper |
| Sovereignty and boundary sensitivity | Shows which systems are especially shaped by data location, operational control, or retention posture |

## Family Distinctions

| Family | Dominant task class | Typical autonomy posture | Strongest evidence need | Common failure mode |
| --- | --- | --- | --- | --- |
| Enterprise chat or knowledge assistant | Retrieval and response generation | Assistive | Grounded answer quality and access control | Fluent but unsupported output |
| Coding assistant | Suggestion and transformation | Assistive | Change quality and secure development fit | Local speed hiding downstream quality cost |
| Coding agent or workflow agent | Multi-step execution | Action-taking | Tool traceability, approval quality, rollback | Over-broad permissions or weak stop conditions |
| Document intelligence | Extraction and classification | Semi-automated | Precision/recall, exception routing, audit trail | Treating OCR or classification confidence as final truth |
| Forecasting or anomaly detection | Predictive scoring | Advisory | Backtesting, drift monitoring, business interpretation | Using a model output as a policy decision without review |
| Recommender or optimizer | Ranking and choice shaping | Advisory or partially automated | Objective fit, fairness, feedback-loop monitoring | Hidden policy bias becoming operational default |
| Vision or speech inspection | Perception and thresholding | Advisory or partially automated | Dataset quality, threshold design, reviewer agreement | Thresholds drifting away from real-world consequence |
| Evaluation or routing platform | Control and orchestration | Infrastructure-facing | Reliability, policy correctness, observability | Underinvesting because the system is treated as internal plumbing |

## What Matters Most

- Broader applied AI and ML families belong in the same atlas because organizations usually operate several at once.
- The same governance or privacy rule lands differently on a recommender, a document-intelligence workflow, and an agentic assistant.
- Non-LLM systems still need explicit treatment of sovereignty, compliance exposure, and build-vs-buy trade-offs.

Back to [5.1 Use-Case Foundations](05-01-00-use-case-foundations.md).
