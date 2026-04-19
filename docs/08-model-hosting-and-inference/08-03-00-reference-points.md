# 8.3 Reference Points

_Page Type: Chapter Index | Maturity: Draft_

This section gathers the named runtimes, managed services, and reusable stack shapes that make hosting choices comparable. Use it when the runtime-control question is already clear and the remaining issue is which serving layer, provider posture, or stack composition best fits the workload's latency target, sovereignty boundary, hardware dependence, and exit plan.

## Included Reference Subsections

- 8.3.1 [Tools And Platforms](08-03-01-tools-and-platforms.md)
- 8.3.2 [Reference Stack Solutions](08-03-02-reference-stack-solutions.md)

## What To Look For Here

- which serving runtimes, managed endpoints, or hardware-aligned platforms fit the required control posture without hiding a bigger lock-in or support burden
- which reusable stack shapes keep model access, serving software, telemetry, and policy controls separable instead of collapsing them into one vendor choice
- where openness, sovereignty, portability, privacy, and hardware dependence still change the answer even after the team agrees on a hosting lane
- which unresolved questions should send the reader back to foundations, operating review, gateway control, observability, security, or sourcing rather than stretching the reference section beyond its role

## Reading Boundaries

- Start with [8.3.1 Tools And Platforms](08-03-01-tools-and-platforms.md) when the team needs to compare self-hosted runtimes, managed inference services, edge-oriented stacks, and hardware-specific platforms without confusing them as interchangeable layers.
- Use [8.3.2 Reference Stack Solutions](08-03-02-reference-stack-solutions.md) when the question is which end-to-end hosting shape belongs in the environment, including API-first, managed endpoint, cloud-estate, self-hosted, edge, or sovereign patterns.
- Revisit [8.1 Hosting Foundations](08-01-00-hosting-foundations.md) or [8.2 Operating Hosting And Inference](08-02-00-operating-hosting-and-inference.md) if the team still cannot name the required runtime posture, telemetry obligations, support-access limits, hardware assumptions, or re-review triggers before it compares references.
- Move to [7. Model Ecosystem](../07-model-ecosystem/07-00-00-model-ecosystem.md), [9. Model Gateways And Access Control](../09-model-gateways-and-access-control/09-00-00-model-gateways-and-access-control.md), [14. Observability Logging And Monitoring](../14-observability-logging-and-monitoring/14-00-00-observability-logging-and-monitoring.md), or [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md) when the binding issue is model-family fit, routing and policy, runtime evidence, or provider dependence rather than the hosting references themselves.

Back to [8. Model Hosting And Inference](08-00-00-model-hosting-and-inference.md).
