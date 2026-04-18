# 18.1.2 Decision Boundaries And Sourcing Heuristics

This subsection explains how to decide whether a layer should be built, bought, or run in a hybrid posture once speed, control, and operating realism are all considered together.

## Decision Boundaries

- Favor **buy** when the layer is non-differentiating, time-to-value dominates, and the organization can tolerate the resulting dependence.
- Favor **build** when the layer creates strategic leverage, the team can realistically operate it, and sovereignty, control, or portability demands are too strong for the managed alternatives.
- Favor **hybrid** when the stack contains a mix of commodity and strategic layers or when the organization needs faster delivery now without foreclosing a later migration path.
- Treat the question as **capability realism first** when the organization is attracted to control but lacks the people, process, or operational maturity to sustain it.

## Practical Heuristics

- Default to hybrid when governance, privacy, or sovereignty requirements are strong but the platform team is not ready to own every layer from day one.
- Do not build a layer only because the vendor is disliked; build it only when the organization can name the strategic benefit and operate the resulting burden.
- Do not buy a layer only because it is fast; inspect whether the control plane, data path, and exit posture remain acceptable after integration.
- Weigh openness and portability alongside cost. A cheaper managed option can still be strategically expensive if it blocks migration or auditability.
- Use buy-first for rapidly changing commodity interfaces unless the managed posture creates unacceptable compliance, sovereignty, or concentration constraints.
- Use build-first sparingly for layers tied directly to core differentiation, regulated boundary control, or non-negotiable evidence requirements.

## Escalate When

- The team cannot name who will operate the built or self-hosted layer after launch.
- Contract terms, export limits, or telemetry behavior undermine the claimed exit posture.
- A managed service would force unacceptable changes to privacy, sovereignty, or legal-review assumptions.
- The build case depends on heroic staffing assumptions or undocumented platform work.

## Common Failure Modes

- Arguing build vs buy as one decision for the whole stack instead of a layer-by-layer choice.
- Treating hybrid as indecision rather than as the normal posture for mixed constraints.
- Overvaluing short-term delivery speed while underpricing future migration and control costs.

Back to [18.1 Sourcing Foundations](18-01-00-sourcing-foundations.md).
