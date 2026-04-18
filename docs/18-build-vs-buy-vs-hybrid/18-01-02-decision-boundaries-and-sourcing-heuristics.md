# 18.1.2 Decision Boundaries And Sourcing Heuristics

_Page Type: Decision Guide | Maturity: Review-Ready_

Use this page to narrow the sourcing posture before comparing vendors or stack shapes. The goal is not to produce one universal answer for the chapter; it is to identify which decision lane dominates and which chapter must be pulled into the review before the sourcing choice hardens.

## Decision Lanes

| Lane | Use it when the main question is... | Typical sourcing bias |
| --- | --- | --- |
| Speed-first | how to deliver acceptable capability quickly with proportionate controls | buy commodity layers, keep scope narrow, preserve an exit path where it matters |
| Differentiation-first | which layer creates durable business leverage or domain advantage | build workflow, policy, or knowledge layers that create the differentiation |
| Sovereignty-first | how to keep locality, operator control, auditability, or jurisdictional exposure within bounds | self-host or compose the control-critical layers; buy only what can remain bounded |
| Shared-control | how to support many teams with common policies, budgets, and evidence standards | hybrid, with an internal or semi-portable gateway/control plane |
| Capability-transfer | how to use vendors or integrators now without making them permanent owners of the operating model | hybrid, with explicit transition milestones and retained internal control artifacts |

## Practical Heuristics

- Default to hybrid when the organization needs speed now but also expects control, portability, or multi-team reuse later.
- Build only when the team can name the strategic benefit and the operator who will carry the ongoing burden.
- Buy only when the control plane, data path, and evidence model remain acceptable after integration, not only at contract signature.
- Treat retrieval, policy, workflow logic, and telemetry as the layers most likely to decide real exit posture.
- Use managed capability for commodity interfaces unless jurisdiction, concentration, or runtime-control demands change the economics.
- Revisit the sourcing decision when a local tool becomes a shared service, when one provider becomes structurally dominant, or when the evidence burden rises.

## Escalate When

- the team cannot name a service owner for the internally built or composed layer
- the claimed exit path depends on undocumented data export, retraining, or policy recreation work
- a managed service changes privacy, sovereignty, procurement, or audit assumptions more than the delivery team admits
- an integrator or vendor is effectively being asked to own the long-term control plane
- the proposal assumes self-hosting without staffing for upgrades, incidents, security patches, and lifecycle management

## Sourcing Anti-Patterns

- one build-vs-buy answer for the whole stack
- hybrid presented as indecision instead of as a deliberate mixed-control posture
- buying speed and accidentally outsourcing the policy or evidence layer
- self-hosting as symbolism without a credible operating model
- treating supplier dissatisfaction as a sufficient reason to build

## Chapter Handoffs

- [3. Enterprise AI Stack Map](../03-enterprise-ai-stack-map/03-00-00-enterprise-ai-stack-map.md)
- [6. Data Sovereignty And Privacy](../06-data-sovereignty-and-privacy/06-00-00-data-sovereignty-and-privacy.md)
- [17. Vendors Organizations And Market Structure](../17-vendors-organizations-and-market-structure/17-00-00-vendors-organizations-and-market-structure.md)
- [19. Reference Architectures](../19-reference-architectures/19-00-00-reference-architectures.md)

Back to [18.1 Sourcing Foundations](18-01-00-sourcing-foundations.md).
