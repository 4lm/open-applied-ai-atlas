# 9.1.2 Decision Boundaries And Adoption Heuristics

_Page Type: Decision Guide | Maturity: Draft_

Use this page when the gateway control-plane elements are already clear and the remaining question is what adoption lane fits by default. The goal is to match gateway scope to the real shared-control burden so teams do not standardize a proxy too early, skip identity and evidence work, or mistake managed mediation for complete policy ownership.

## Decision Lanes

| Lane | Use it when the main question is... | Default gateway posture |
| --- | --- | --- |
| Embedded-access lane | whether one bounded product or team can keep provider access local without creating shared-control drift yet | keep access in the application or platform layer, use shared client conventions, and revisit only when identity, quota, or provider-sprawl pressure becomes real |
| Identity-and-spend lane | whether the immediate problem is anonymous usage, shared credentials, weak tenant attribution, or missing budget ownership | prioritize stable caller identity, tenant mapping, request metadata, and quota ownership before adding sophisticated routing or multi-provider abstractions |
| Shared-policy lane | whether several teams, providers, or model families now need one place for route eligibility, coarse policy, quotas, and audit evidence | adopt a gateway as the standard path, with versioned route policy, reliable identity propagation, exportable logs, and an explicit exception process |
| High-consequence lane | whether regulated data, privileged actions, customer isolation, or sensitive support review makes centralized mediation necessary but insufficient on its own | use the gateway for eligibility, evidence, and coarse enforcement, while keeping application authorization, approval, and data-handling controls explicit outside the gateway |
| Dependency-governance lane | whether a managed gateway or vendor control plane is becoming a trust-critical dependency for routing, logging, policy, or provider access | require export tests, bypass runbooks, policy-recreation notes, and ownership of vendor-only features before the gateway becomes the organization's default path |

## Practical Heuristics

- Adopt a gateway for shared control, not for aesthetic architecture symmetry. One provider with many teams, tenants, or budgets can justify a gateway sooner than three providers used by one small bounded service.
- Fix attribution before clever routing. If the platform still cannot tie a request to a stable user, service, tenant, approval, or cost owner, abstraction has outrun governance.
- Centralize only the controls the gateway can really enforce. Route eligibility, quotas, coarse policy checks, and evidence capture fit well; business authorization, workflow-specific approvals, and domain rules often belong in the application or orchestration layer.
- Treat the exception lane as part of the design, not as an embarrassing afterthought. Direct provider access for pilots, incident response, latency-sensitive paths, or regional constraints is acceptable only when it has an owner, expiry, and reconciliation review.
- Demand exportable history before standardization. Route changes, denials, overrides, and policy revisions need to survive vendor outage, procurement conflict, and provider exit.
- Re-evaluate the gateway lane as soon as system authority, tenant mix, provider count, or regulated-data scope expands. Gateway posture that was proportionate for one internal assistant can become too weak for shared customer-facing workflows.

## Escalate When

- the team still relies on shared platform credentials or cannot trace one request cleanly through user identity, tenant, route, quota decision, and policy version
- the gateway is being asked to enforce business authorization or approval decisions that it cannot actually see or validate
- a managed gateway becomes the only place where routing logic, policy history, denial reasons, or audit evidence can be understood
- latency, residency, provider-feature, or reliability constraints are already pushing teams toward undeclared direct-access paths
- central quotas or route rules exist, but nobody can explain who owns the limit, who may override it, and what evidence remains after an exception
- gateway adoption is expanding faster than the export model, rollback plan, or break-glass process that would be needed during an incident or supplier dispute

## Gateway Adoption Anti-Patterns

- calling a gateway "portability" while prompts, safety dependencies, model semantics, and support processes remain tied to one provider
- hiding shared service credentials behind a gateway and treating that as attributable tenant identity
- centralizing policy names while the decisive business authorization and approval logic still lives invisibly in applications
- routing all traffic through a managed control plane before testing evidence export, bypass behavior, and policy reconstruction outside the vendor console
- declaring a gateway standard while permanent pilot, legacy, or executive-exception paths bypass it without review
- using the gateway to compensate for weak IAM, incomplete application controls, or missing operator ownership

## Chapter Handoffs

- [8. Model Hosting And Inference](../08-model-hosting-and-inference/08-00-00-model-hosting-and-inference.md) when the real blocker is runtime placement, latency budget, regional hosting, or capacity ownership rather than mediation policy.
- [10. Agentic Systems And Orchestration](../10-agentic-systems-and-orchestration/10-00-00-agentic-systems-and-orchestration.md) when tool authority, approval choreography, or multi-step execution is doing more decision work than provider routing.
- [14. Observability Logging And Monitoring](../14-observability-logging-and-monitoring/14-00-00-observability-logging-and-monitoring.md) when the missing control is reconstructable traces, exportable telemetry, or incident-review evidence rather than gateway adoption alone.
- [15. Security And Abuse Resistance](../15-security-and-abuse-resistance/15-00-00-security-and-abuse-resistance.md) when trust boundaries, secrets exposure, abuse containment, or break-glass hardening dominate the review.
- [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md) when managed-gateway dependence, exit posture, or supplier concentration matters as much as the technical gateway design.

## Practical Reading Rule

Choose the lightest gateway lane that still matches the highest shared-control burden, then tighten it as soon as identity, policy, evidence, or dependency risk rises. If the chosen lane cannot explain who owns route policy, how caller identity survives the hop, how exceptions are governed, and how evidence leaves the gateway product, the adoption posture is already underspecified.

Back to [9.1 Gateway Foundations](09-01-00-gateway-foundations.md).
