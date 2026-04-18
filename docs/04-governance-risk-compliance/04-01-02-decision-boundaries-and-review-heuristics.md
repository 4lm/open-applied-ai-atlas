# 4.1.2 Decision Boundaries And Review Heuristics

_Page Type: Decision Guide | Maturity: Review-Ready_

Use this page to decide which governance lane owns a question before the organization wastes time in the wrong forum.

## Decision Lanes

| Review lane | Use it when the main question is... |
| --- | --- |
| Legal and regulatory review | whether obligations under the EU AI Act, GDPR, the EU Data Act, sector rules, or contracts apply |
| Management-system governance | who owns the system, how review is repeated, and how exceptions are approved and expired |
| Control and evidence design | which artifacts, tests, records, and sign-offs must exist before release or re-review |
| Supplier and procurement review | whether vendor claims about hosting, telemetry, subcontractors, support access, or portability are acceptable |
| Operating oversight | how incidents, material changes, new failure modes, and threshold shifts trigger re-review |

## Practical Heuristics

- Escalate early when the system affects regulated workflows, rights-impacting decisions, sensitive data, or external users.
- Treat reusable platform patterns as governance-design work, not one-off project approvals.
- Require a named evidence package before release if the system can materially affect operations, customers, employees, or regulated outcomes.
- Move the question to chapter `6` when the argument is really about data classes, retention, or cross-border handling.
- Move the question to chapters `17` and `18` when the supposed governance issue is really supplier dependence or sourcing posture.
- Move the question to chapter `20` when the team is using one framework citation as a substitute for implementation design.

## Escalate When

- a supplier cannot clearly describe deployer or provider role, data flows, and subcontractor chain
- approval depends on undocumented exceptions or verbal sign-off
- post-launch changes are material, but nobody can name the required re-review lane
- policy claims are being used to compensate for missing tests, logs, or release evidence

## Common Failure Modes

- treating governance as a single gate instead of a set of distinct decision lanes
- discovering legal, privacy, or procurement constraints only after architecture and vendor lock-in
- letting one artifact pretend to be policy, risk record, and release evidence at the same time

## Chapter Handoffs

- [6. Data Sovereignty And Privacy](../06-data-sovereignty-and-privacy/06-00-00-data-sovereignty-and-privacy.md)
- [13. Evaluation Testing And QA](../13-evaluation-testing-and-qa/13-00-00-evaluation-testing-and-qa.md)
- [15. Security And Abuse Resistance](../15-security-and-abuse-resistance/15-00-00-security-and-abuse-resistance.md)
- [17. Vendors Organizations And Market Structure](../17-vendors-organizations-and-market-structure/17-00-00-vendors-organizations-and-market-structure.md)
- [20. Standards Frameworks And Bodies Of Knowledge](../20-standards-frameworks-and-bodies-of-knowledge/20-00-00-standards-frameworks-and-bodies-of-knowledge.md)

Back to [4.1 Governance Foundations](04-01-00-governance-foundations.md).
