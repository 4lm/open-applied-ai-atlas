# 2.2.1 Worked Classification Scenarios

_Page Type: Worked Example | Maturity: Review-Ready_

These scenarios show how the taxonomy changes real review work. Each example is intentionally practical: the goal is not only to label the thing correctly, but to stop the wrong downstream comparison before it starts.

## Managed Model API For An Internal Assistant

| Field | Decision |
| --- | --- |
| Context | A team wants a fast internal assistant and plans to call a vendor-hosted model API directly from an application and retrieval layer |
| Common wrong shortcut | Treat the whole proposal as "which model should we use?" and compare only model capability rows |
| Correct classification | The runtime choice is a managed platform or service that exposes one or more models; if suppliers are being compared, the vendor must be named as a separate class |
| Better comparison shape | Use one comparison surface for managed services or platforms and, only if needed, a second surface for supplier posture and market dependence |
| Dimensions to apply | Openness posture, sovereignty, privacy, portability, compliance exposure, lock-in and exit posture |
| Downstream handoff | Chapters `07` and `08` for model and hosting questions, `09` for access-control posture, `11` if retrieval is involved, and `18` if dependence versus speed becomes the real decision |

## Open-Source Gateway In A Hybrid Estate

| Field | Decision |
| --- | --- |
| Context | An organization wants one routing and policy layer across multiple managed model providers and one self-hosted fallback path |
| Common wrong shortcut | Compare the gateway directly against model vendors or treat the gateway as the whole architecture |
| Correct classification | The gateway is a tool, framework, or project at the control-plane layer; the vendors behind routed endpoints remain separate entity classes |
| Better comparison shape | Compare gateways against gateway peers first, then compare the routed providers or hosting options in their own tables if those choices are still open |
| Dimensions to apply | Openness posture, portability, observability implications, security implications, and lock-in created by configuration, plugins, or policy logic |
| Downstream handoff | Chapters `03` and `09` for layer placement and gateway controls, `14` for telemetry, `17` for supplier dependence, and `18` for sourcing posture |

## Forecasting Platform In An Existing Data Estate

| Field | Decision |
| --- | --- |
| Context | A team with an established analytics estate is deciding between a managed forecasting platform, an existing ML workbench, and a more self-managed composition path |
| Common wrong shortcut | Treat the choice as if a classical-ML platform were the same class of decision as a frontier chat-model API |
| Correct classification | The primary comparison is between managed platform or service options and self-managed architecture patterns; individual algorithms or models are subordinate rows, not the entire decision |
| Better comparison shape | Compare managed platforms with peer managed platforms, and compare the self-managed architecture path as a pattern or reference-stack surface rather than as one more product row |
| Dimensions to apply | Portability, governance implications, data boundary implications, operational complexity, lock-in and exit posture, and fit by organization type |
| Downstream handoff | Chapters `03` and `05` for stack and use-case fit, `13` for evaluation requirements, `17` for supplier leverage, and `18` for build-buy-hybrid posture |

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
- If the scenario still feels ambiguous after naming the entity class, go back to [2.1.1 Entity Classes And Core Distinctions](02-01-01-entity-classes-and-core-distinctions.md).
- If the class is clear but the dimensions are not, use [2.1.2 Cross-Cutting Dimensions And Heuristics](02-01-02-cross-cutting-dimensions-and-heuristics.md) before touching a comparison table.

Back to [2.2 Applying The Taxonomy](02-02-00-applying-the-taxonomy.md).
