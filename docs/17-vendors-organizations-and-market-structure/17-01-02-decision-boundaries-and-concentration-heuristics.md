# 17.1.2 Decision Boundaries And Concentration Heuristics

_Page Type: Decision Guide | Maturity: Review-Ready_

Use this page to decide when ecosystem concentration should materially change a technical or sourcing choice instead of being treated as background commentary.

## Decision Lanes

| Market-structure lane | Use it when the main question is... |
| --- | --- |
| Concentration risk | supposedly different options share the same cloud, hardware, or control-plane actor |
| Openness gap | an option is usable but still cannot be inspected, run, adapted, or migrated on acceptable terms |
| Sovereignty constraint | deployment, auditability, support control, or jurisdictional control is narrowed by the ecosystem structure |
| Exit-posture problem | switching cost depends more on data gravity, tooling, skills, or policy coupling than on the interface alone |

## Practical Heuristics

- Ask whether fallback suppliers are actually independent or just new wrappers around the same underlying platform.
- Discount apparent optionality when routing, telemetry, policy controls, or deployment artifacts are tied to one ecosystem.
- Treat open-weight or open-source access as incomplete if the viable operating path is still concentrated in one hardware or cloud estate.
- Increase scrutiny when one actor influences several layers at once: model path, hosting, gateway, observability, or marketplace.
- Route to chapter `18` when the answer should change what the organization builds, buys, or keeps portable.
- Route to chapter `19` when the concentration issue is really a control-point design question inside the architecture.

## Escalate When

- the fallback supplier still depends on the same hyperscaler, accelerator vendor, or hosted control plane
- exit would require rebuilding evaluation assets, policy controls, or operating knowledge from scratch
- procurement treats price competition as proof of strategic independence
- a delivery partner becomes the only party who knows how the system actually works

## Common Failure Modes

- confusing supplier plurality with real independence
- treating concentration as only a commercial issue instead of a sovereignty and evidence issue too
- focusing on software vendors while ignoring hardware, cloud, integrator, or ecosystem-hub dependence

## Chapter Handoffs

- [4. Governance Risk Compliance](../04-governance-risk-compliance/04-00-00-governance-risk-compliance.md)
- [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md)
- [19. Reference Architectures](../19-reference-architectures/19-00-00-reference-architectures.md)

Back to [17.1 Market Foundations](17-01-00-market-foundations.md).
