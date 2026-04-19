# 9.2.1 Worked Gateway Scenarios

_Page Type: Worked Example | Maturity: Draft_

Use these scenarios when the gateway decision needs to survive rollout pressure instead of staying at the level of abstract control-plane language. Each scenario shows the operating posture, evidence packet, and re-review trigger that should exist before the organization treats the gateway as a stable shared path.

## Multi-Team Provider Sprawl Cleanup

| Field | Decision |
| --- | --- |
| System | Several internal products already call different model providers with inconsistent credentials, uneven logging, and no shared route policy or spend ownership |
| Dominant operating failure | The platform adds a gateway for architectural neatness, but identity propagation, exception handling, and route ownership remain unclear so the new control plane hides the same disorder behind one endpoint |
| Gateway operating shape | Standardize first on caller identity, approved providers, route eligibility, and exportable request metadata; let provider-specific prompts and workflow logic stay local until the shared-control baseline is stable |
| Required evidence | route and provider register, caller-to-tenant attribution map, quota owner list, sample denial or throttle logs, direct-access exception register, and rollback path for route-policy mistakes |
| Release question | Can the organization explain who owns each shared route and which traffic still bypasses the gateway before it expands gateway usage to every team? |
| Re-review trigger | Reopen chapters `08`, `14`, `15`, and `18` when the gateway becomes the default path for regulated workloads, customer-facing systems, or managed-gateway analytics that teams cannot export |

## Low-Risk Single Application Exception

| Field | Decision |
| --- | --- |
| System | One bounded internal application uses a single provider, has modest traffic, and does not yet justify a shared gateway team or central route catalog |
| Dominant operating failure | The team adopts the platform gateway anyway, then inherits latency, policy, and dependency overhead that solves no real shared-control problem |
| Gateway operating shape | Keep provider access local to the application, but record the exception explicitly with named ownership, approved use boundary, and a trigger for revisiting gateway adoption when identity, tenant, or spend complexity grows |
| Required evidence | exception note, local credential and secret owner, logging location, rate-limit expectation, direct rollback method, and the threshold that would require migration into the gateway path |
| Release question | Is the organization preserving a proportionate direct-access path, or is it allowing unmanaged drift that will be expensive to reconcile later? |
| Re-review trigger | Reopen chapters `08`, `14`, and `16` when the service adds external users, privileged actions, multi-tenant behavior, or operating promises that need central attribution and intervention authority |

## Staged Route-Policy Migration

| Field | Decision |
| --- | --- |
| System | A team wants to move an existing production workload behind the gateway without forcing every request path, tenant, and model route through an immature policy layer on day one |
| Dominant operating failure | Migration starts with broad cutover instead of shadow traffic, route-by-route validation, and failure drills, so the first policy error or timeout becomes a service outage |
| Gateway operating shape | Migrate in phases: observe traffic first, move one route family at a time, compare latency and denial behavior side by side, and keep a tested bypass or rollback lane until the route policy proves stable |
| Required evidence | migration plan, shadow-traffic results, policy diff record, route-level rollback drill, denial escalation path, and sign-off from service owners affected by changed gateway behavior |
| Release question | If the gateway blocks or misroutes high-value traffic, can the team revert quickly without losing audit evidence or creating a second undocumented path? |
| Re-review trigger | Reopen chapters `08`, `14`, `15`, and `19` when failover logic changes, privileged tools are introduced, latency budgets tighten, or routing becomes dependent on gateway-only transformation features |

## Managed Gateway Exportability Review

| Field | Decision |
| --- | --- |
| System | The organization is close to standardizing on one managed gateway product for policy, provider routing, analytics, and spend control across many teams |
| Dominant operating failure | Convenience wins before anyone proves whether route definitions, policy history, denial logs, and exception records can be exported or recreated outside the vendor console |
| Gateway operating shape | Treat standardization as a dependency review: document which controls are product-specific, test evidence export, define a bypass posture, and keep policy logic understandable outside the gateway UI |
| Required evidence | route-export sample, log-export sample, policy reconstruction note, vendor-outage runbook, feature-dependence list, and named owner for provider-exit planning |
| Release question | If procurement, outage, or control failure forced the organization off this gateway, which controls would move cleanly and which would require redesign under pressure? |
| Re-review trigger | Reopen chapters `14`, `15`, `17`, and `18` when analytics retention changes, provider concentration rises, a managed control feature becomes mandatory for policy, or incident review depends on vendor-only history |

## Cross-Scenario Review Signals

- strong gateway operating review makes route ownership explicit: who approves routes, who owns exceptions, how caller identity survives the hop, and how evidence leaves the product
- the right gateway posture is proportional to shared-control burden: bounded single-app access can remain local, while multi-team routing and audit demands usually need a formal shared path
- phased migration is a control requirement, not project-management nicety: route cutover, shadow traffic, denial review, and rollback proof matter more than gateway launch announcements
- managed convenience is not portability: the more the organization relies on vendor-only policy syntax, analytics, or route history, the more urgently it needs export and bypass proof

## Reading Rule

Choose the scenario that matches the hardest operating constraint first, then ask whether the evidence packet, exception model, and rollback path are proportionate to that risk. If the team cannot show route ownership, identity attribution, exportable logs, and a governed bypass posture, the gateway rollout is not yet ready for standardization.

Back to [9.2 Operating Gateways And Controls](09-02-00-operating-gateways-and-controls.md).
