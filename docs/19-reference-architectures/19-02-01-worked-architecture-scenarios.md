# 19.2.1 Worked Architecture Scenarios

_Page Type: Worked Example | Maturity: Draft_

These scenarios show how reference architectures should change with consequence, platform maturity, and control posture.

## SaaS-First Assistant

| Field | Decision |
| --- | --- |
| Context | A low-risk internal drafting service needs value quickly and has limited internal platform capacity |
| Recommended posture | Use a SaaS-first assistant pattern with basic telemetry, approved provider lane, and explicit fallback to existing workflows |
| Why | The organization benefits more from speed and constrained scope than from early platform investment |
| Watch for | Letting a temporary assistant pattern become the default for stronger-control use cases |
| Control implications | provider approval, usage logging, prompt/data boundary review, release gate for core tasks |
| Adjacent chapters | `03`, `06`, `18` |

## Gateway-Centric Enterprise Pattern

| Field | Decision |
| --- | --- |
| Context | Many teams now depend on shared model access, common budgets, and audit visibility |
| Recommended posture | Move to an enterprise gateway stack with shared auth, routing, trace standards, and evaluation templates |
| Why | Platform-level control becomes more important than local team speed once reuse and spend coordination grow |
| Watch for | Centralizing access without clear ownership of the gateway as a service |
| Control implications | service owner, policy-as-code, budget lanes, model approval process, shared observability |
| Adjacent chapters | `03`, `09`, `13`, `18` |

## Sovereign Private Stack

| Field | Decision |
| --- | --- |
| Context | A high-control environment needs strong locality, operator control, and explicit exit posture |
| Recommended posture | Use a sovereign private platform with self-hosted serving, local retrieval, policy enforcement, provenance, and auditable telemetry |
| Why | Sovereignty changes runtime, support, update, and evidence obligations together |
| Watch for | Underestimating staffing, lifecycle management, and support depth needed to keep the stack healthy |
| Control implications | support-access limits, signed artifacts, controlled updates, local observability, re-certification triggers |
| Adjacent chapters | `06`, `08`, `15`, `18` |

## Hybrid Predictive-Plus-Generative Stack

| Field | Decision |
| --- | --- |
| Context | A team combines forecasting or scoring with retrieval-backed explanation and human review |
| Recommended posture | Use a hybrid predictive-plus-generative stack rather than forcing a pure assistant or agent pattern |
| Why | The core business value still depends on classical ML or optimization components that need their own lifecycle controls |
| Watch for | Letting the language interface hide the predictive model, feature pipeline, or evaluation burden underneath |
| Control implications | ML lifecycle ownership, cross-method evaluation, retrieval provenance, workflow handoff rules |
| Adjacent chapters | `03`, `12`, `13`, `18` |

## Reusable Patterns Across Scenarios

| Pattern | What good looks like |
| --- | --- |
| Pattern family named first | The team can explain why this architecture family fits better than a lighter or heavier one |
| Control model matched to scale | Shared platforms, sovereign stacks, and mixed-method systems carry visibly different control obligations |
| Exit posture made explicit | The architecture preserves portability where the organization says portability matters most |

## Architecture Anti-Patterns

| Anti-pattern | Why it fails |
| --- | --- |
| Accidental platform | A thin pilot stack silently becomes the enterprise default without re-review |
| Control-free centralization | Shared infrastructure is introduced without service ownership, SLAs, or change governance |
| Self-hosting as symbolism | The organization accepts the heaviest operating burden without proving that control benefits justify it |
| One-pattern-for-everything | Low-risk assistance, action-taking workflows, and mixed predictive workloads are forced into the same stack family |

Back to [19.2 Applying Reference Architectures](19-02-00-applying-reference-architectures.md).
