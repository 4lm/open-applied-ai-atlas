# 20.1.2 Decision Boundaries And Combination Heuristics

_Page Type: Decision Guide | Maturity: Draft_

Use this page to choose a starting set. The right combination depends on the dominant question, not on which standard is most fashionable.

## Decision Lanes

| Lane | Use it when the main question is... |
| --- | --- |
| Legal applicability | which obligations, rights, prohibitions, or enforcement exposures apply |
| Governance system design | how accountability, policy structure, auditability, and continual improvement should work |
| Risk-program design | how to prioritize risks, control depth, and review intensity across use cases |
| Technical control selection | how to secure, monitor, document, or instrument the system in practice |
| Standards tracking and harmonization | which bodies, committees, or public programs should be watched as the landscape changes |

## Starting Combinations

| Situation | Starting set | Why this is the right starting set |
| --- | --- | --- |
| EU-facing service with meaningful consequence | EU AI Act + GDPR + ISO/IEC 42001 | obligations, privacy duties, and management-system structure all matter together |
| Organization needs a durable AI governance model | ISO/IEC 42001 + ISO/IEC 23894 or NIST AI RMF | combines governance discipline with a usable risk language |
| Team needs impact review beyond pure risk scoring | ISO/IEC 42001 + ISO/IEC 42005 + chapter `16` | adds stakeholder and oversight implications to the governance model |
| Security review for an AI-enabled application or agentic workflow | NIST AI RMF or ISO/IEC 23894 + OWASP GenAI + MITRE ATLAS + chapters `14` and `15` | combines governance framing with concrete security failure modes and operational controls |
| Portability, access, or ecosystem-control dispute | EU Data Act + chapter `06` + chapter `18` | the core question is switching and control posture, not only privacy or model quality |
| Standards-landscape monitoring for EU implementation | CEN-CENELEC AI work + ETSI AI + NIST AI Standards + chapter `21` | keeps tracking work separate from direct conformance claims |

## Practical Heuristics

- Start with the governing obligation, then add the management-system or technical anchor that makes it operational.
- Do not use a management-system standard as a substitute for system-specific evaluation, security, or oversight work.
- Do not treat public bodies or committees as if membership or awareness produces conformance.
- If the system crosses privacy, sourcing, or oversight boundaries, pull those chapters in explicitly instead of stretching chapter `20`.
- Prefer a small, named standards set with mapped outputs over a long list of respected references with no operational owner.

## Escalate When

- the team cannot say whether it is solving a legal, governance, risk, technical, or tracking problem
- certification or conformance language appears before a control mapping exists
- multiple standards are named, but nobody owns the crosswalk into release evidence, supplier review, or operating controls
- the standards dispute is really about data boundary, human oversight, evaluation coverage, or exit posture

## Chapter Handoffs

- [4. Governance Risk Compliance](../04-governance-risk-compliance/04-00-00-governance-risk-compliance.md)
- [6. Data Sovereignty And Privacy](../06-data-sovereignty-and-privacy/06-00-00-data-sovereignty-and-privacy.md)
- [13. Evaluation Testing And QA](../13-evaluation-testing-and-qa/13-00-00-evaluation-testing-and-qa.md)
- [15. Security And Abuse Resistance](../15-security-and-abuse-resistance/15-00-00-security-and-abuse-resistance.md)
- [16. Human Oversight And Operating Model](../16-human-oversight-and-operating-model/16-00-00-human-oversight-and-operating-model.md)
- [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md)

Back to [20.1 Standards Foundations](20-01-00-standards-foundations.md).
