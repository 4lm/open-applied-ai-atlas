# 17.1.2 Decision Boundaries And Concentration Heuristics

This subsection explains when market structure should materially change a technical or sourcing decision instead of being treated as background context.

## Decision Boundaries

- Treat the issue as a **concentration problem** when multiple seemingly different options depend on the same cloud, hardware, model-distribution, or control-plane actor.
- Treat the issue as an **openness problem** when the organization can technically access a tool or model but still cannot inspect, run, adapt, or migrate it on acceptable terms.
- Treat the issue as a **sovereignty problem** when market choice constrains deployability, auditability, support control, or geographic-operational control.
- Treat the issue as an **exit-posture problem** when switching cost depends more on ecosystem coupling, data gravity, or control-plane policy than on API syntax alone.

## Practical Heuristics

- Ask whether two suppliers are actually distinct or whether they share the same hidden dependency on a hyperscaler, hardware estate, or dominant open-source steward.
- Discount apparent optionality when policy, logging, orchestration, or deployment artifacts are tied to one vendor ecosystem.
- Treat “open” posture as incomplete if the surrounding runtime, packaging, support, or hardware path is still highly concentrated.
- Increase scrutiny when a single actor controls both the model path and the gateway, observability, or deployment path.
- Route to chapter `18` when the concentration question should change a build-vs-buy posture, not only a market narrative.
- Route to chapter `3` or `19` when the concentration issue is really an architectural control-point issue.

## Escalate When

- The fallback supplier still depends on the same cloud, accelerator, or hosted control plane.
- Exit requires rebuilding operational knowledge, evaluation assets, or policy controls from scratch.
- The organization is implicitly accepting hardware or hyperscaler dependence without naming it as a strategic choice.
- Procurement is treating list-price competition as if it eliminated concentration risk.

## Common Failure Modes

- Confusing supplier plurality with real strategic independence.
- Treating concentration as purely commercial when it also shapes sovereignty, portability, and evidence quality.
- Ignoring integrator and talent dependence while focusing only on software vendors.

Back to [17.1 Market Foundations](17-01-00-market-foundations.md).
