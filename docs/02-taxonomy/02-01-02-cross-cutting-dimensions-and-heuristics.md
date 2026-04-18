# 2.1.2 Cross-Cutting Dimensions And Heuristics

_Page Type: Decision Guide | Maturity: Outline_

This subsection defines the recurring dimensions that the atlas uses to compare unlike systems without flattening them into one generic score.

## Canonical Cross-Cutting Dimensions

- Openness: distinguishes open knowledge, open source, open weights, open artifacts, open tooling, and open governance rather than treating openness as a single binary.
- Sovereignty: captures where operational control really sits, including hosting control, telemetry exposure, support pathways, contractual dependency, and auditability.
- Portability: measures interface portability, exportability, migration burden, and the practical reversibility of a decision.
- Privacy: covers source data, prompts, outputs, logs, memory, traces, and retention behavior.
- Compliance exposure: captures whether the system creates obligations around law, sector regulation, procurement discipline, or management-system evidence.
- Vendor lock-in and exit posture: makes visible whether dependence sits with the model API, data location, orchestration layer, hardware stack, or operational knowledge.

## Heuristics For Use

- Apply the dimensions across broader applied AI and ML systems, including forecasting, recommender, vision, speech, optimization, and hybrid systems, not only chat or agentic stacks.
- Do not assume the same dimension matters equally in every chapter. Privacy may dominate one decision while portability or compliance exposure dominates another.
- Treat sovereignty and privacy as related but not identical. A system can be privacy-conscious in some respects while still leaving operational control elsewhere.
- Treat legal obligations, standards, and product posture as different entity classes even when they interact in one decision.

## Common Reader Mistakes

- Using openness language as a proxy for sovereignty or compliance.
- Treating vendor lock-in as only an API problem when it may also be a data, hardware, or control-plane problem.
- Assuming non-LLM systems do not need the same cross-cutting analysis.

Back to [2.1 Classification Foundations](02-01-00-classification-foundations.md).
