# 4.1.1 Policy, Ownership, And Control Mapping

_Page Type: Concept Explainer | Maturity: Review-Ready_

This page separates the recurring governance concepts that are easy to blur together in review meetings. The distinction work matters because teams often say "governance" when they actually mean policy writing, approval routing, control enforcement, or evidence collection.

## Key Distinctions

| Distinction | Why it changes the decision |
| --- | --- |
| Policy statement vs control | Policy defines what must be true; a control is how the organization makes it true in practice |
| Control owner vs reviewer | The owner keeps the control working; the reviewer checks whether it is adequate for the risk |
| Approval lane vs advice lane | Legal, privacy, security, and GRC input may be mandatory without each function being the final approver |
| Standard control vs compensating control | Exceptions can be approved, but only if the substitute control and expiry are explicit |
| Evidence artifact vs narrative justification | Audit, release, and incident decisions need inspectable records, not only persuasive prose |

## What Changes In Practice

- Governance is weak if policy exists without named owners, review triggers, and control evidence.
- A release decision should name both the approving role and the artifact set used to justify the decision.
- Exception handling must be time-bounded and tied to compensating controls rather than informal tolerance.
- The same issue may involve several reviewers, but only one lane should hold final accountability for the decision.

## Review Questions

- Which role owns the control after launch?
- Which artifact proves that the control was actually checked?
- Is the team asking governance to solve a runtime, privacy, or sourcing problem that belongs elsewhere?

## Handoffs

- Go to [6. Data Sovereignty And Privacy](../06-data-sovereignty-and-privacy/06-00-00-data-sovereignty-and-privacy.md) when the real dispute is about data handling, deletion, residency, or support access.
- Go to [17. Vendors Organizations And Market Structure](../17-vendors-organizations-and-market-structure/17-00-00-vendors-organizations-and-market-structure.md) and [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md) when supplier concentration or exit posture is the dominant constraint.
- Go to [20. Standards Frameworks And Bodies Of Knowledge](../20-standards-frameworks-and-bodies-of-knowledge/20-00-00-standards-frameworks-and-bodies-of-knowledge.md) when the team is mixing laws, standards, and frameworks as if they played the same role.

Back to [4.1 Governance Foundations](04-01-00-governance-foundations.md).
