# 9.2.2 Patterns And Anti-Patterns

_Page Type: Reference Sheet | Maturity: Draft_

Use this page during rollout, control review, and renewal planning to recognize healthy gateway operating shapes before a shared endpoint turns into an opaque proxy with weak ownership, thin evidence, and no clean exit path.

## Reusable Gateway Operating Patterns

| Pattern | What good looks like | Fit signal | Review warning |
| --- | --- | --- | --- |
| Identity-aware shared route register | Every approved route records provider, model family, caller classes, quota owner, denied-path behavior, and when direct access remains allowed outside the gateway | more than one team, provider, or workload class now depends on shared mediation | teams can name the gateway product, but cannot show which routes are actually approved or who owns them |
| Phased migration with observable bypass | Existing traffic is observed first, then migrated route by route with shadow checks, rollback drills, and an explicit fallback lane that does not erase audit history | a production workload is moving behind the gateway and downtime or hidden regressions would be expensive | the program plans a broad cutover because "it is only a proxy change" |
| Time-bounded exception handling | Direct provider access, urgent pilots, and incident bypasses stay visible in one exception register with approver, expiry, reconciliation plan, and the trigger for moving back into the governed path | one application or emergency path genuinely needs proportionate treatment outside the default shared route | exceptions accumulate as tribal knowledge, ticket comments, or permanent side doors |
| Exportable policy and evidence pack | Policy logic, denial events, route history, and usage evidence can be exported and reviewed outside one managed console so the control plane stays portable | the organization is considering managed gateway standardization or procurement concentration is rising | convenience features become mandatory before anyone tests whether policy or evidence can leave the vendor product |
| Split control between gateway and application | The team states clearly which controls the gateway owns versus which stay in application code, runtime placement, approval flow, or human oversight | response shaping, tool gating, residency, or approval decisions span multiple layers | reviewers speak as if the gateway solved security, compliance, or workflow approval by itself |

## Gateway Anti-Patterns

| Anti-pattern | Why it fails | Early signal | Review action |
| --- | --- | --- | --- |
| Standardizing the endpoint before standardizing ownership | A common URL can hide the same provider sprawl, credential drift, and route confusion that already existed | platform teams celebrate gateway adoption while route approval, identity propagation, and quota owners remain unclear | block wider rollout until the route register, owner map, and exception list exist |
| Identity lost at the mediation hop | Audit, spend, and policy controls weaken when the gateway cannot tie requests back to a stable user, service, or tenant | logs record gateway service accounts or generic application names instead of real callers | reopen IAM, observability, and oversight review with chapters `14` and `16` |
| Break-glass as the permanent operating model | Emergency bypass becomes an ungoverned shadow path that keeps the hardest traffic outside reviewable policy | "temporary" direct provider access has no expiry, no reconciliation work, and no named approver | require an exception register and a closure plan before approving more bypasses |
| Vendor-only control logic | Managed features may be useful, but policy, route history, and denial evidence become fragile if they only live in one product UI | no one can explain how to recreate critical controls during outage, contract failure, or exit planning | reopen sourcing review with chapter `18` and require export and bypass proof |
| Gateway rollout with no tested rollback | The first denial bug, latency spike, or route mismatch becomes an outage when rollback exists only as an assumption | migration planning mentions launch dates and route policies, but not route-level reversal drills | require rollback evidence, owner assignment, and failure drills before widening production scope |

## Review Prompts

- Which operating pattern best fits the current stage: identity-aware shared routing, phased migration, time-bounded exception handling, exportable managed control, or explicit split ownership across layers?
- What evidence proves the gateway preserves caller identity, route ownership, denial handling, and rollback rather than simply centralizing traffic?
- Which anti-pattern is most likely to appear after rollout pressure arrives: unmanaged exceptions, vendor-only logic, identity loss, or no-tested-rollback migration?
- Which adjacent chapter must re-enter before approval: `08`, `14`, `15`, `16`, or `18`?

## Re-Review Triggers

- a new provider, route family, tenant model, or privileged tool path is added behind the gateway
- managed gateway analytics, prompt inspection, or policy syntax become harder to export or reconstruct outside the product
- direct-access exceptions survive beyond their stated expiry or start carrying higher-risk traffic than the shared path
- latency, denial, or outage behavior changes enough that the old rollback proof no longer matches production reality
- reviewers can no longer explain which controls live in the gateway versus the application, runtime, or human approval layer

## Practical Reading Rule

Use these patterns after the gateway shape is broadly chosen but before the organization treats mediation as solved. If the team cannot show route ownership, identity-aware evidence, bounded exceptions, exportable control logic, and a tested rollback posture, the gateway operating design is not yet ready for standardization.

Back to [9.2 Operating Gateways And Controls](09-02-00-operating-gateways-and-controls.md).
