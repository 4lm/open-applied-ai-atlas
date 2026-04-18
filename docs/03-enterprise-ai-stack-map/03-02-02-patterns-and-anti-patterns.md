# 3.2.2 Patterns And Anti-Patterns

_Page Type: Reference Sheet | Maturity: Review-Ready_

Use these patterns to test whether a proposal is using the stack map as a real design aid or only as explanatory decoration.

## Reusable Patterns

| Pattern | What good looks like |
| --- | --- |
| Boundary before model choice | The team identifies data, approval, and operating constraints before narrowing model options |
| Shared control layers named explicitly | Gateway, telemetry, policy, and evidence services are treated as stack layers, not optional extras |
| Stack map revisited on posture change | Managed-to-self-hosted, advisory-to-action, or single-team-to-platform changes reopen the map |
| Cross-cutting concerns visible by layer | Portability, sovereignty, privacy, and lock-in are attached to concrete layers rather than generic statements |

## Stack-Map Anti-Patterns

| Anti-pattern | Why it fails |
| --- | --- |
| Model-first architecture reasoning | The organization optimizes for capability while hiding workflow, data, or evidence risk |
| Tool catalog as stack map | Named products replace layer reasoning, so teams cannot explain responsibilities clearly |
| Shared dependency blindness | Different products appear independent while the same gateway, cloud, or support path dominates |
| Architecture shape mistaken for layer map | A reusable architecture is chosen before the team understands which layer is actually driving the decision |

## Review Prompt

| Ask during review... | Why it matters |
| --- | --- |
| Which layer carries the strongest unresolved risk? | Forces the team to name the real decision surface |
| Which controls are shared platform capabilities versus application-local behavior? | Prevents hidden coupling and duplicate control logic |
| What changes if the supplier or hosting posture changes? | Tests whether the stack map is portable or accidentally vendor-shaped |
| Which adjacent chapter now owns the hardest question? | Prevents the stack map from becoming a catch-all answer |

## Drift Signals

- teams discuss suppliers without naming gateway, telemetry, or approval layers
- self-hosting is proposed without a clear support, provenance, and observability plan
- product comparisons dominate before the data boundary and review lane are stable
- multiple teams claim autonomy while sharing one ungoverned control plane

Back to [3.2 Applying The Stack Map](03-02-00-applying-the-stack-map.md).
