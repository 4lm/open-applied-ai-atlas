# 2.2.1 Worked Classification Scenarios

_Page Type: Worked Example | Maturity: Review-Ready_

These scenarios show how the taxonomy changes real review work. Each example is intentionally practical: the goal is not only to label the thing correctly, but to stop the wrong downstream comparison before it starts.

Use the scenarios to watch the first comparison surface change. If the entity class changes, the first table, the leading dimensions, and the next chapter should usually change with it.

## Managed Model API For An Internal Assistant

| Field | Decision |
| --- | --- |
| Context | A team wants a fast internal assistant and plans to call a vendor-hosted model API directly from an application and retrieval layer |
| Common wrong shortcut | Treat the whole proposal as "which model should we use?" and compare only model capability rows |
| Correct classification | The runtime choice is usually a managed service or API that exposes model access. If the proposal also bundles shared workflow tooling, policy enforcement, observability, and admin controls, it is a managed platform instead. If suppliers are being compared, the vendor must still be named as a separate class |
| Better comparison shape | Make the first table compare peer managed services or APIs when the decision is about bounded model access. Split out a separate platform comparison only if integrated control-plane coverage is part of the proposal, and keep supplier posture in its own surface if concentration or contract dependence still matters |
| Dimensions to apply | Control posture, support-path dependence, privacy, sovereignty, portability, and lock-in and exit posture |
| Downstream handoff | Chapters `07` and `08` for model and hosting questions, `09` for access-control posture, `11` if retrieval is involved, and `18` if dependence versus speed becomes the real decision |

## Open-Source Gateway In A Hybrid Estate

| Field | Decision |
| --- | --- |
| Context | An organization wants one routing and policy layer across multiple managed model providers and one self-hosted fallback path |
| Common wrong shortcut | Compare the gateway directly against model vendors or treat the gateway as the whole architecture |
| Correct classification | The gateway is a tool, framework, or project at the control-plane layer; the vendors behind routed endpoints remain separate entity classes |
| Better comparison shape | Make the first table compare gateways against gateway peers at the control-plane layer. Only after that should later tables compare routed providers, self-hosted fallback runtimes, or supplier posture if those choices are still open |
| Dimensions to apply | Openness posture, portability implications, observability implications, security implications, operational complexity, and lock-in created by configuration, plugins, or policy logic |
| Downstream handoff | Chapters `03` and `09` for layer placement and gateway controls, `14` for telemetry, `17` for supplier dependence, and `18` for sourcing posture |

## Forecasting Platform In An Existing Data Estate

| Field | Decision |
| --- | --- |
| Context | A team with an established analytics estate is deciding between a managed forecasting platform, an existing ML workbench, and a more self-managed composition path |
| Common wrong shortcut | Treat the choice as if a classical-ML platform were the same class of decision as a frontier chat-model API |
| Correct classification | If the offer is an integrated forecasting workbench with data preparation, training flow, scheduling, monitoring, and operator workflow, compare it as a managed platform. If it is a narrower hosted forecasting capability, compare it as a managed service or API. A self-managed composition path is an architecture pattern, not one more product row |
| Better comparison shape | Make the first table compare peer managed platforms or peer managed services at the same scope. Keep the self-managed path in a separate pattern or reference-stack surface. Compare individual forecasting models only after the operating lane is stable |
| Dimensions to apply | Portability implications, data boundary implications, governance implications, evaluation burden, operational complexity, and lock-in and exit posture |
| Downstream handoff | Chapters `03` and `05` for stack and use-case fit, `08` for runtime boundary, `13` for evaluation requirements, `17` for supplier leverage, and `18` for build-buy-hybrid posture |

## Vision Inspection On A Restricted Production Line

| Field | Decision |
| --- | --- |
| Context | A manufacturer is choosing between a vendor-managed vision inspection suite, a narrower hosted inference service, and a self-managed edge deployment path for quality control |
| Common wrong shortcut | Treat the choice as "which vision model has the best benchmark accuracy?" and compare models, cameras, and platforms in one table |
| Correct classification | A suite that bundles labeling, deployment, monitoring, and operator workflow is a managed platform. A narrower hosted inference endpoint is a managed service or API. An edge deployment path is an architecture choice, and camera hardware is another class again |
| Better comparison shape | Make the first table compare peer deployment lanes: managed platforms with similar workflow scope, managed inference services with similar boundaries, or edge patterns with similar control posture. Compare models inside the chosen lane, and compare hardware separately only if the sensor decision is still open |
| Dimensions to apply | Data boundary implications, sovereignty exposure, observability implications, operational complexity, security implications, and lock-in and exit posture |
| Downstream handoff | Chapters `03` and `05` for system fit, `08` for runtime boundary, `13` for evaluation thresholds, `15` for hardening, and `18` for sourcing posture |

## Regulated Workflow With Legal And Standards Anchors

| Field | Decision |
| --- | --- |
| Context | A regulated workflow, such as claims review or eligibility support, must be designed under legal obligations and internal assurance requirements |
| Common wrong shortcut | Put the EU AI Act, ISO/IEC 42001, and NIST AI RMF into the same table as products and ask which option is "best" |
| Correct classification | Laws and regulations, standards and frameworks, and internal control artifacts are separate reference classes; they are anchors that shape the design, not products being purchased as runtime components |
| Better comparison shape | Use one surface for legal and standards anchors, another for control artifacts, and keep product or platform comparison separate until the obligations are clear |
| Dimensions to apply | Compliance exposure, governance implications, evidence implications, privacy, and sourcing only after obligations and controls are clear |
| Downstream handoff | Chapters `04`, `06`, `13`, `16`, and `20` for governance lanes, data boundaries, evidence, oversight, and standards crosswalks |

## Cross-Scenario Reading Rule

- A taxonomy mistake usually appears before the architecture, sourcing, or compliance mistake it later causes.
- If the class change would alter the first table, keep that first surface narrow before adding supplier, standards, or architecture rows.
- If the scenario still feels ambiguous after naming the entity class, go back to [2.1.1 Entity Classes And Core Distinctions](02-01-01-entity-classes-and-core-distinctions.md).
- If the class is clear but the dimensions are not, use [2.1.2 Cross-Cutting Dimensions And Heuristics](02-01-02-cross-cutting-dimensions-and-heuristics.md) before touching a comparison table.
- Once the first surface is stable, use [2.2.3 Comparison Schema](02-02-03-comparison-schema.md) to decide the minimum fields and row depth.

Back to [2.2 Applying The Taxonomy](02-02-00-applying-the-taxonomy.md).
