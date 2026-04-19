# 17.2.1 Worked Ecosystem Scenarios

_Page Type: Worked Example | Maturity: Draft_

These scenarios show how ecosystem analysis changes decisions that might otherwise look like routine product selection.

## Cloud-Estate Concentration

| Field | Decision |
| --- | --- |
| Context | A company uses several AI products that all run inside the same cloud estate |
| Recommended posture | Treat the cloud platform as the primary concentration point, not only the branded AI services |
| Why | Supplier plurality is weaker than it looks if the same cloud, identity, and policy layers dominate the estate |
| Watch for | Tracking only direct model-vendor risk while ignoring shared platform dependence |
| Control implications | Concentration register, exit review, and explicit decision on which layers must remain portable |
| Adjacent chapters | `04`, `18`, `19` |

## Open-Source Adoption With Thin Support

| Field | Decision |
| --- | --- |
| Context | A team adopts open tooling and open-weight models but relies on a very narrow internal and external skill pool |
| Recommended posture | Treat the posture as more portable than proprietary managed services, but still review skills and support concentration explicitly |
| Why | Open artifacts reduce one kind of lock-in while leaving operational dependence on scarce expertise or key maintainers |
| Watch for | Assuming open code automatically means low strategic dependence |
| Control implications | Capability-transfer plan, maintainer and support review, and fallback operating pattern |
| Adjacent chapters | `18`, `19`, `21` |

## Integrator-Heavy Delivery Program

| Field | Decision |
| --- | --- |
| Context | An external partner accelerates delivery and becomes the practical owner of architecture and operations knowledge |
| Recommended posture | Time-box partner dependence and require knowledge transfer as part of the delivery model |
| Why | Strategic dependence can sit with services and knowledge, not only with licensed software |
| Watch for | Letting one integrator become the irreplaceable control plane for the system |
| Control implications | Transition milestones, runbook ownership, internal shadowing, and approval before renewals |
| Adjacent chapters | `04`, `16`, `18` |

## Foundation-Led Ecosystem Choice

| Field | Decision |
| --- | --- |
| Context | A team prefers a foundation-backed or community-governed project to avoid single-vendor control |
| Recommended posture | Use the stewardship benefit, but still review support maturity, release cadence, and enterprise fit |
| Why | Neutral stewardship can widen optionality without removing all operational risk |
| Watch for | Treating foundation status as proof of production readiness |
| Control implications | Maturity review, support-path decision, and explicit criteria for when to adopt managed help around the project |
| Adjacent chapters | `18`, `19`, `21` |

Back to [17.2 Applying Market Structure Analysis](17-02-00-applying-market-structure-analysis.md).
