# 13.1.2 Decision Boundaries And Release Heuristics

_Page Type: Decision Guide | Maturity: Review-Ready_

Use this page when the evidence types are already clear and the remaining question is what release lane the change belongs in by default. The goal is to match proof depth to the highest-consequence failure so teams do not ship on benchmark optimism alone, over-test low-risk tweaks like full launches, or treat observability as a substitute for pre-release evidence.

## Decision Lanes

| Lane | Use it when the main question is... | Default release posture |
| --- | --- | --- |
| Baseline-capability lane | whether a model, component, or early prototype is capable enough to justify more investment at all | use benchmarks or small task sets to confirm obvious viability, but block any production release claim until system-level evidence exists |
| Regression-gate lane | whether a bounded prompt, model, route, policy, or retrieval change preserved behavior that previously worked | run representative replays against known tasks and known failure classes, compare against the current baseline, and log exceptions before rollout expands |
| Workflow-readiness lane | whether an end-to-end user journey with approvals, retrieval, tools, or business rules is safe enough to release | test the full path with scenario packs, reviewer notes, and failure-specific thresholds rather than model outputs alone |
| Abuse-and-boundary lane | whether hostile inputs, unsafe content, privilege edges, or untrusted retrieval can push the system outside its intended boundary | pair normal-path evidence with adversarial tests, policy-bypass probes, and explicit rollback criteria before launch |
| Live-rollout lane | whether the release is acceptable only if staged monitoring, operator review, and rollback hooks are already live | require pre-release evidence plus deployment guards, runtime alerts, human escalation paths, and mandatory re-evaluation triggers before traffic widens |

## Practical Heuristics

- Choose the lane by the worst plausible failure, not by the easiest existing metric. A small model swap behind a stable interface can still belong in the regression-gate or workflow-readiness lane if it changes retrieval, routing, or tool behavior.
- Treat end-to-end evidence as mandatory once the system touches retrieval, policy logic, approvals, or tools. Model-answer quality alone does not prove that the workflow behaves acceptably in context.
- Escalate from regression-gate to workflow-readiness as soon as a change affects business-critical tasks, user roles, or downstream actions. Reusing yesterday's replay set is not enough if the workflow shape has changed.
- Keep adversarial evidence in the main release packet when the system accepts open-ended input, cites retrieved content, or can trigger side effects. Abuse resistance is not a later hardening bonus.
- Use human review to resolve consequential judgment, not to hide weak test design. Reviewers need rubrics, sample selection rules, and a disagreement path before their notes count as release proof.
- Connect release evidence to runtime evidence. Prompt version, model route, policy version, release ID, and scenario pack should map cleanly into observability and rollback records so post-release incidents do not restart the investigation from zero.
- Define exception ownership before release, not after. Any accepted failure needs an owner, expiry, mitigation, and explicit re-run trigger.

## Escalate When

- a benchmark, leaderboard result, or isolated model demo is being treated as release approval for a system with retrieval, workflow logic, approvals, or tool use
- the team can replay happy-path prompts but cannot show tests for high-consequence tasks, edge cases, or known historical failures
- prompt, routing, retrieval, tool, policy, or model changes are being described as "small" even though they alter the user-visible path or authority boundary
- human reviewers disagree materially, but the rubric, tie-break rule, or escalation owner is still undefined
- monitoring is expected to discover failures that should have been scenario-tested or abuse-tested before launch
- an exception is being accepted without rollback conditions, expiry, or a named owner for the next re-evaluation

## Release Anti-Patterns

- calling a benchmark win "evaluation complete" even though the production workflow is still untested
- proving isolated model behavior while retrieval quality, policy gates, and tool contracts remain invisible
- reusing a regression suite that no longer reflects the tasks, roles, or integrations the release actually changes
- relying on broad human spot checks because the team never defined scenario coverage or measurable pass conditions
- widening rollout before observability, rollback, and exception handling are connected to the same release packet
- treating abuse testing as a security-only concern that can wait until after the feature is already exposed

## Chapter Handoffs

- [12. Training Fine-Tuning And Adaptation](../12-training-fine-tuning-and-adaptation/12-00-00-training-fine-tuning-and-adaptation.md) when the unresolved question is whether retrieval, prompt changes, tuning, or model replacement is the right adaptation path rather than how to prove the chosen change.
- [14. Observability Logging And Monitoring](../14-observability-logging-and-monitoring/14-00-00-observability-logging-and-monitoring.md) when the release lane is blocked on runtime reconstruction, alerting, telemetry scope, or rollback visibility.
- [15. Security And Abuse Resistance](../15-security-and-abuse-resistance/15-00-00-security-and-abuse-resistance.md) when abuse probes, trust boundaries, or side-effect containment drive more of the release burden than evaluation design alone.
- [16. Human Oversight And Operating Model](../16-human-oversight-and-operating-model/16-00-00-human-oversight-and-operating-model.md) when approval rights, reviewer authority, escalation ownership, or operator intervention remains unclear.
- [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md) when managed eval platforms, provider lock-in, or outsourcing of release evidence affects how review and auditability will work in practice.

## Practical Reading Rule

Pick the lightest release lane that still proves the highest-consequence failure mode, then tighten immediately when authority, workflow complexity, or external exposure increases. If the chosen lane cannot explain what was tested, who accepted the remaining exceptions, and what forces the next re-evaluation, the release gate is still too weak.

Back to [13.1 Evaluation Foundations](13-01-00-evaluation-foundations.md).
