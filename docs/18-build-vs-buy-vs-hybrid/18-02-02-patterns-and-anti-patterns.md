# 18.2.2 Patterns And Anti-Patterns

_Page Type: Reference Sheet | Maturity: Draft_

Use this page during design and renewal review to recognize good sourcing shapes before local politics or tool preferences flatten the decision.

## Reusable Sourcing Patterns

| Pattern | What good looks like | Fit signal | Review warning |
| --- | --- | --- | --- |
| Buy commodity capability, own workflow and policy | Managed model or platform access is paired with internally controlled workflow, approval, or policy logic | the organization differentiates in process design rather than in base model ownership | the bought layer starts absorbing workflow rules, approval logic, or tacit policy decisions |
| Managed now with explicit transfer path | A vendor or integrator accelerates delivery, but internal artifacts, telemetry, and runbooks are retained for later transition | the team can name capability-transfer milestones and retained evidence from day one | transfer is promised but no owner, date, or internal skill ramp exists |
| Self-host only the control-critical layers | The team keeps runtime, retrieval, or policy components local only where sovereignty, evidence, or cost control require it | one or two layers clearly dominate the control requirement | self-hosting expands outward because the organization cannot define the real boundary |
| Portable telemetry before deeper platform commitment | Evaluations, traces, and review evidence stay exportable even while the runtime is managed | multi-provider comparison, incident review, or future migration is likely | the telemetry stack becomes vendor-native only and portability becomes theoretical |
| Hybrid retrieval with managed inference | Sensitive knowledge and permission logic stay under stronger internal control while model access remains managed | internal content, provenance, and access rules matter more than owning model serving | the team treats the managed model contract as if it settled retrieval governance too |

## Sourcing Anti-Patterns

| Anti-pattern | Why it fails | Early signal | Review action |
| --- | --- | --- | --- |
| One sourcing answer for the whole stack | Different layers have different dependence, control, and operating burdens | the proposal says "we decided to build" or "we decided to buy" with no layer map | force a layer-by-layer sourcing breakdown |
| Integrator becomes the permanent control plane | Delivery speed is purchased at the cost of internal operating memory and exit posture | the partner owns the runbooks, gateway logic, and renewal decisions | require retained artifacts, owner assignment, and transfer milestones |
| Sovereignty theater | The team claims control while leaving core runtime, evidence, or support dependence unchanged | hosting is local but policy, telemetry, or update control remains external | verify which control actually moved and which did not |
| Premature self-hosting | The organization accepts the heaviest burden before proving a strong control or economics case | staffing, upgrades, and incident ownership are vague or aspirational | revisit whether hybrid or managed layers would meet the real need |
| Hidden lock-in in the gateway or telemetry layer | The team focuses on model portability while the control and evidence plane becomes sticky | migration looks easy on paper until tracing, policy, or eval history is considered | inspect data export, control policy portability, and evidence retention explicitly |

## Review Prompts

- Which pattern best describes the current proposal, and why is that pattern proportionate to the actual constraint?
- Which anti-pattern would be most likely to appear after the first successful rollout?
- What artifact proves that the organization could re-source the control-critical layer later if it had to?
- Which chapter should be pulled back in before the proposal is treated as settled: `06`, `09`, `16`, `17`, or `19`?

Back to [18.2 Applying Sourcing Choices](18-02-00-applying-sourcing-choices.md).
