# 17.2.2 Patterns And Anti-Patterns

_Page Type: Reference Sheet | Maturity: Draft_

Use these patterns to test whether an ecosystem choice preserves real optionality or only the appearance of it.

## Reusable Patterns

| Pattern | What good looks like |
| --- | --- |
| Concentration named by layer | The organization can say where dependence sits across model, cloud, hardware, gateway, and support layers |
| Optionality preserved where it matters most | Teams deliberately keep the highest-risk layer portable even if they buy speed elsewhere |
| Open posture reviewed with support reality | Openness is treated as an advantage, then tested against skills, maintenance, and operating maturity |
| Partner dependence time-boxed | Integrator or managed-service reliance includes capability transfer and exit planning from the start |

## Market-Structure Anti-Patterns

| Anti-pattern | Why it fails |
| --- | --- |
| Brand diversity illusion | Several vendors appear in the stack, but they all depend on the same underlying platform actor |
| Open means safe | Open code or open weights are treated as if they remove support, maturity, or hardware concentration risk |
| Price competition equals independence | Short-term commercial leverage is mistaken for long-term portability |
| Invisible services lock-in | The software looks replaceable, but the runbooks, policies, and operational knowledge are not |

## Review Prompt

| Ask during review... | Why it matters |
| --- | --- |
| Which dependency would be hardest to replace in practice? | Identifies the real control point early |
| Which alternatives share the same hidden platform or hardware path? | Prevents fake diversification |
| What capabilities leave with the supplier or partner if the relationship ends? | Makes skill and services dependence visible |
| Which layer must remain portable even if another layer is deliberately concentrated? | Forces explicit trade-off framing |

## Drift Signals

- fallback options all rely on the same hyperscaler or accelerator path
- procurement treats list-price competition as enough analysis
- teams discuss openness without discussing support and operating depth
- one partner accumulates the only usable deployment and troubleshooting knowledge

Back to [17.2 Applying Market Structure Analysis](17-02-00-applying-market-structure-analysis.md).
