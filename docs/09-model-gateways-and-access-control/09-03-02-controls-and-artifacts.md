# 9.3.2 Controls And Artifacts

_Page Type: Operational Artifact | Maturity: Draft_

Use this page when a team wants gateway policy to stay reviewable after rollout instead of living as hidden proxy config. A gateway is only a real control plane if reviewers can inspect route rules, caller identity, policy scope, exception handling, and export boundaries without reverse-engineering the running stack.

## Minimum Gateway Control Pack

| Control or artifact | What it should make explicit | Typical owner | Review trigger |
| --- | --- | --- | --- |
| Route and provider policy register | Approved providers, approved model families, blocked routes, fallback logic, and when direct-to-provider access is allowed | Platform or architecture owner | New provider, model class, or routing change |
| Identity and tenant-attribution map | Which user, service, tenant, or workload identities the gateway can see and how they map to policy decisions, quotas, and audit logs | Platform or IAM owner | New identity source, tenant model, or workload type |
| Policy decision catalog | Which controls are enforced at the gateway versus in the application, runtime, or human-approval lane | Platform, security, or governance owner | New policy type, approval rule, or exception |
| Quota, budget, and rate-limit profile | Spend caps, concurrency limits, burst rules, emergency kill switches, and owner for overrides | Platform or finance-facing service owner | New cost tier, customer segment, or service-level promise |
| Logging and evidence schema | Which request, response, route, policy, and denial events are retained, redacted, exportable, and linked to incident review | Observability, security, or privacy owner | New sink, retention change, or provider path |
| Exception and break-glass register | Temporary bypasses, direct-access cases, ungoverned legacy paths, approvers, expiry dates, and closure plan | Service owner plus risk or security owner | Incident, pilot launch, or urgent customer exception |
| Policy change and rollback record | Version history, approval path, rollout scope, rollback method, and proof that the previous safe state can be restored | Platform or release owner | Every production policy change |

## Minimum Review Packet

Before a gateway becomes the default path for teams, reviewers should be able to inspect the following in one place:

- the current route policy register, including blocked and exception routes
- the identity and tenant-attribution model for both human and service callers
- the policy decision catalog showing what the gateway enforces and what stays outside it
- the quota and emergency-control profile for spend, concurrency, and denial conditions
- the evidence schema for logs, route decisions, and denied requests, including redaction boundaries
- the exception register for direct provider access, unmanaged pilots, or legacy integrations
- the rollback record from at least one recent gateway-policy change or dry run

## Gateway Review Questions

| Review question | Evidence reviewers should expect |
| --- | --- |
| Can the team show which routes are allowed, blocked, or fallback-only for each workload class? | Route matrix, named owner, and last approved revision |
| Can the team explain how caller identity affects policy, quota, and audit attribution? | Identity map, policy links, and example decision traces |
| Can the team tell which controls live in the gateway and which depend on the application or runtime? | Policy decision catalog with explicit boundary notes |
| Can the team disable a harmful route or provider quickly without breaking unrelated traffic? | Emergency change path, rollback step, and tested ownership |
| Can the organization preserve policy evidence if it leaves the current gateway product? | Export note for route rules, logs, and policy history |

## Change Triggers That Require Re-Review

- adding a new provider, sovereign region, or managed gateway service
- widening access from one internal workload to many teams or external users
- moving policy enforcement from the application into the shared gateway
- introducing prompt, response, or retrieval inspection that changes privacy or observability posture
- allowing direct-access exceptions that bypass the main route policy
- depending on gateway-specific policy syntax or analytics that would complicate future exit

## Failure Signs

- The gateway is described as the control plane, but no one can point to a document that states which routes are actually approved.
- Identity is centralized for login, but quota, audit, and policy records still cannot be tied to a stable caller or tenant.
- Teams assume the gateway solved security or compliance even though critical approval, data-handling, or runtime controls still live elsewhere and are undocumented.
- Direct provider access exists for pilots or urgent launches, but there is no expiry date, owner, or reconciliation plan.
- Policy logic is embedded in one managed-gateway UI with no export path for rules, evidence, or change history.

## Approval Prompt

If the team cannot show which artifact records approved routes, identity-aware policy logic, exception handling, and rollback-ready change history, the gateway design is not yet ready to become the shared control plane.

Back to [9.3 Reference Points](09-03-00-reference-points.md).
