# 17.1.1 Actor Types, Power, And Core Distinctions

_Page Type: Concept Explainer | Maturity: Review-Ready_

This page separates the main ecosystem roles that shape optionality across the AI stack. The distinction matters because the organization that sets prices, distribution rules, hardware availability, or support access is not always the one named on the interface your team uses.

## Key Distinctions

| Distinction | Why it changes the decision |
| --- | --- |
| Product vendor vs control-point actor | The visible product supplier may still depend on a hyperscaler, accelerator vendor, or model steward |
| Openness posture vs concentration posture | An option can be more open than an API-only service and still sit in a narrow support or hardware ecosystem |
| Foundation or community stewardship vs enterprise support maturity | Neutral governance can reduce control concentration, but it does not guarantee operational fit |
| Contract dependence vs skill dependence | The hardest thing to replace may be implementation knowledge, not software licensing |
| Supplier plurality vs real independence | Several branded options may still collapse onto one cloud, chip, or gateway control plane |

## What Changes In Practice

- Market analysis should include cloud, accelerator, gateway, hosting, and ecosystem-hub dependence.
- A portability review is incomplete if it looks only at API syntax and ignores talent, tooling, and policy coupling.
- Foundation-backed and open-source options still need maturity and support review; openness is not a free pass.
- Integrator-heavy delivery models can create strategic dependence even when the software stack is nominally portable.

## Review Questions

- Which actor would be hardest to replace in practice?
- Which "alternative" options still rely on the same hidden platform or hardware dependency?
- Is the dependency commercial, technical, operational, or skills-based?

## Handoffs

- Go to [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md) when market structure should change sourcing posture directly.
- Go to [19. Reference Architectures](../19-reference-architectures/19-00-00-reference-architectures.md) when the concentration question is really about architecture control points.
- Go to [4. Governance Risk Compliance](../04-governance-risk-compliance/04-00-00-governance-risk-compliance.md) when dependence or supplier opacity should trigger stronger approval or exception handling.

Back to [17.1 Market Foundations](17-01-00-market-foundations.md).
