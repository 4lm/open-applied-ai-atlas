# 9.1.1 Routing, Identity, And Policy Distinctions

_Page Type: Concept Explainer | Maturity: Review-Ready_

Use this page to separate gateway control-plane responsibilities before the discussion collapses into "put a proxy in front of the model APIs." Gateway design becomes misleading when provider routing, caller identity, policy enforcement, quota ownership, and audit evidence are treated as one feature set instead of as distinct control questions.

## Gateway Control-Plane Map

| Control-plane element | What it is actually deciding | Where the real dependency sits | What fails when it is misclassified |
| --- | --- | --- | --- |
| Provider and model routing layer | which providers, model families, or regions a workload may call and under what fallback rules | provider-specific APIs, model semantics, routing policy syntax, and failover design | teams assume abstraction erased provider dependence even though prompts, feature flags, moderation hooks, or model behavior still bind the workload to one route family |
| Caller identity and tenant-attribution layer | which human, service, tenant, or workload identity is making the request and how policy attaches to it | IAM integration, token propagation, tenant mapping, and service-to-service trust design | spend, abuse review, and incident response stay anonymous because the gateway only sees one shared platform credential |
| Policy enforcement layer | which controls are applied centrally and which remain inside the application, runtime, or human-approval path | policy engine capability, exception handling, version control, and policy exportability | the gateway is called the control plane even though the decisive authorization, safety, or approval logic still lives elsewhere and is undocumented |
| Quota and budget governance layer | who owns limits on spend, throughput, burst behavior, and emergency shutdown | finance rules, platform ownership, customer-tier logic, and rate-limit override process | central limits become arbitrary or unsafe because they are disconnected from business ownership, workload criticality, or tenant fairness |
| Evidence and audit layer | which route, denial, override, and change events are retained and how they can be reconstructed later | logging design, redaction boundaries, export paths, and history retention | the platform looks governed until a dispute or incident arrives and no one can reconstruct which policy or route actually fired |
| Exception and direct-access lane | which traffic is intentionally allowed outside the gateway and under what expiry, approval, and review terms | break-glass governance, pilot policy, legacy integrations, and reconciliation discipline | teams believe the gateway standardized access while high-risk or high-volume traffic still bypasses it with no owner or sunset plan |

## Core Distinctions

| Distinction | Why it changes the gateway decision |
| --- | --- |
| Routing convenience vs. real portability | A gateway can centralize credentials and route logic while still leaving prompts, provider-specific features, and model behavior deeply tied to one supplier. |
| Identity federation vs. attributable usage | Single sign-on or shared service authentication is not enough if the gateway cannot tie requests to stable users, tenants, services, or approvals during audit and spend review. |
| Policy definition vs. policy enforcement | A catalog of desired rules is not the same as a reliably enforced control surface with versioning, rollback, and explicit exception handling. |
| Mediation layer vs. actual control boundary | Putting a gateway in the path does not mean the gateway owns secrets, approvals, retrieval policy, or tool authority; many critical controls may still belong elsewhere. |
| Central quotas vs. owned operating limits | Rate limits help only when somebody owns why the limit exists, who may override it, and what happens when a high-consequence workflow is throttled or denied. |
| Managed-gateway analytics vs. exportable evidence | Attractive dashboards are weak governance if route rules, denial logs, and policy history cannot be exported for audit, incident response, or provider exit. |
| Standard path vs. governed exception lane | A gateway standard is not real if direct provider access, unmanaged pilots, or emergency bypasses exist without an owner, expiry date, and review trigger. |
| Provider abstraction vs. provider behavior | One route surface can hide many different moderation, latency, region, support, and feature behaviors that still matter to architecture and governance. |

## What These Distinctions Change In Practice

- Start by naming the real problem. If the main pain is anonymous spend, weak tenant attribution, or inconsistent approvals, the issue is not only routing abstraction.
- Decide which policies belong in the gateway and which do not. Gateway policy is usually strongest for route eligibility, quota, coarse content or metadata checks, and evidence capture; application-specific business rules often need to stay closer to the workflow.
- Treat identity propagation as a first-class design task. A gateway without stable caller identity usually becomes a platform blind spot for abuse review, customer attribution, and internal chargeback.
- Make exceptions visible early. Direct provider access for pilots, latency-sensitive flows, or legacy integrations can be reasonable, but only if it is recorded as a controlled exception instead of hidden architecture drift.
- Ask what still depends on one provider after the gateway is added: model-specific prompts, tool contracts, safety features, region availability, analytics, or support access often remain the real portability limit.
- Require exportable route and policy history before standardization. If the organization cannot lift rules, logs, and change records out of the gateway product, the new control plane has simply moved the lock-in up a layer.

## Reviewer Checks

- Which decisions are actually centralized: provider choice, model-family eligibility, identity mapping, quota logic, policy enforcement, approval gates, or only credential hiding?
- Can the team explain how a denied, throttled, or misrouted request would be traced back to a user, service, tenant, route rule, and policy revision?
- Which controls still live outside the gateway in the application, runtime, security layer, or human-approval process, and are those boundaries documented?
- What direct-access or break-glass paths exist today, and who owns their expiry, review, and eventual closure?
- If the current gateway product disappeared, which parts of routing, identity, policy, and evidence would move cleanly and which would force redesign?

## Practical Reading Rule

Classify the gateway problem first, then use [9.1.2 Decision Boundaries And Adoption Heuristics](09-01-02-decision-boundaries-and-adoption-heuristics.md) to choose the default adoption lane. If the team still cannot say who owns route policy, how caller identity survives the hop, which controls are actually enforced centrally, and how exceptions stay reviewable, the gateway design is not ready for rollout review yet.

Back to [9.1 Gateway Foundations](09-01-00-gateway-foundations.md).
