# 8. Model Hosting And Inference

_Page Type: Chapter Index | Maturity: Review-Ready_

This chapter treats model hosting and inference as the point where model choice turns into runtime reality: where workloads execute, which party controls the serving path, what telemetry and support access exist, and how latency, cost, resilience, and exportability actually show up in operations.

The main decision is not only self-hosted versus managed. It is which runtime posture creates the right balance of portability, sovereignty, privacy, hardware dependence, support burden, and reviewability for the workload you are actually running.

## Chapter Index

- 8.1 [Hosting Foundations](08-01-00-hosting-foundations.md)
- 8.1.1 [Runtime Postures, Constraints, And Core Distinctions](08-01-01-runtime-postures-constraints-and-core-distinctions.md)
- 8.1.2 [Decision Boundaries And Deployment Heuristics](08-01-02-decision-boundaries-and-deployment-heuristics.md)
- 8.2 [Operating Hosting And Inference](08-02-00-operating-hosting-and-inference.md)
- 8.2.1 [Worked Hosting Scenarios](08-02-01-worked-hosting-scenarios.md)
- 8.2.2 [Patterns And Anti-Patterns](08-02-02-patterns-and-anti-patterns.md)
- 8.3 [Reference Points](08-03-00-reference-points.md)
- 8.3.1 [Tools And Platforms](08-03-01-tools-and-platforms.md)
- 8.3.2 [Reference Stack Solutions](08-03-02-reference-stack-solutions.md)

## How To Read This Chapter

- Start with [8.1 Hosting Foundations](08-01-00-hosting-foundations.md) when the team still needs stable language for managed inference, private hosting, self-hosted runtimes, hardware-specific optimization, and operational ownership.
- Move to [8.2 Operating Hosting And Inference](08-02-00-operating-hosting-and-inference.md) when the main question is rollout shape, operating burden, re-review triggers, or whether a hosting posture still holds up in live delivery.
- Use [8.3 Reference Points](08-03-00-reference-points.md) only after the control posture is clear enough that runtime and stack comparison will sharpen the decision instead of replacing it.

## What This Chapter Helps Decide

- whether model execution should stay inside a provider-managed surface, move into a dedicated managed deployment, or become an internally operated runtime
- where GPU ownership, scaling responsibility, telemetry, and support access should sit across product, platform, and vendor teams
- when portability, residency, or offline-operability needs justify higher operating burden instead of defaulting to managed convenience
- whether the real unresolved issue is model choice, gateway control, observability, security hardening, or sourcing rather than hosting alone

## Reading Boundaries

- Revisit [7. Model Ecosystem](../07-model-ecosystem/07-00-00-model-ecosystem.md) when the real issue is model class, openness posture, lifecycle fit, or whether the organization should standardize on one family at all.
- Revisit [6. Data Sovereignty And Privacy](../06-data-sovereignty-and-privacy/06-00-00-data-sovereignty-and-privacy.md) when transfer limits, retention rules, residency, or support-access restrictions shape the acceptable runtime posture.
- Revisit [9. Model Gateways And Access Control](../09-model-gateways-and-access-control/09-00-00-model-gateways-and-access-control.md) when routing, identity, spend control, policy enforcement, or provider abstraction matters more than raw hosting placement.
- Revisit [14. Observability Logging And Monitoring](../14-observability-logging-and-monitoring/14-00-00-observability-logging-and-monitoring.md) when the main gap is telemetry coverage, replayability, incident reconstruction, or exportable runtime evidence.
- Revisit [15. Security And Abuse Resistance](../15-security-and-abuse-resistance/15-00-00-security-and-abuse-resistance.md) when secrets handling, tenant isolation, model abuse containment, or runtime hardening are the dominant constraints.
- Revisit [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md) when managed-platform dependence, exit planning, or platform-team capacity determines what hosting posture is realistic.

## Adjacent Chapters

- Previous: [7. Model Ecosystem](../07-model-ecosystem/07-00-00-model-ecosystem.md)
- Next: [9. Model Gateways And Access Control](../09-model-gateways-and-access-control/09-00-00-model-gateways-and-access-control.md)
- Repository guidance: [Contributing](../../CONTRIBUTING.md), [Editorial Rules](../../EDITORIAL_RULES.md)
