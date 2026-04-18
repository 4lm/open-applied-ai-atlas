# 4.1.2 Decision Boundaries And Review Heuristics

This subsection explains how to separate governance questions that look similar in meetings but belong to different review lanes in practice.

## Decision Boundaries

- Keep the question in **legal review** when the issue is whether the organization has obligations under the EU AI Act, GDPR, the EU Data Act, sector law, or contractual regulation-heavy regimes.
- Keep the question in **management-system governance** when the issue is accountability structure, policy ownership, review cadence, exceptions, or continual-improvement discipline.
- Keep the question in **control-evidence design** when the issue is what artifacts must exist before release or re-review: evaluations, risk records, privacy reviews, supplier assessments, approval logs, or monitoring evidence.
- Keep the question in **procurement or vendor review** when the risk depends on supplier claims about hosting, telemetry, access, support, portability, sublicensing, or downstream subcontractors.
- Keep the question in **operating oversight** when the system is already in use and the main issue is incident handling, threshold changes, material updates, escalation, or reclassification.

## Practical Heuristics

- Escalate to legal interpretation early if the system may be high-risk, rights-affecting, public-facing, or materially reliant on personal data.
- Anchor governance in a management-system or repeatable internal control model when multiple teams, suppliers, or product lines will reuse the same pattern.
- Require a named evidence package before release when the system affects regulated workflows, sensitive data, autonomous action, or externally visible outputs.
- Route questions to chapter `6` when the real dispute is about data boundary, residency, retention, or access posture rather than governance ownership alone.
- Route questions to chapters `17` and `18` when the control problem is really a sourcing or concentration problem hidden inside a governance discussion.
- Route questions to chapter `20` when the team is mixing up legal obligations, standards, and frameworks as if they were interchangeable.

## Escalate When

- A supplier cannot clearly describe its deployer/provider role, data-handling model, or subcontractor chain.
- The team is trying to compensate for missing evidence with policy language alone.
- A release decision depends on undocumented exceptions or informal verbal approvals.
- The system changes materially after initial approval and nobody can say which review lane owns the re-check.

## Common Failure Modes

- Treating governance as a single approval gate instead of a set of distinct decision lanes.
- Discovering legal or procurement constraints only after architecture and vendor commitment.
- Letting the same artifact try to serve as risk record, legal review, and release evidence without enough detail for any of those jobs.

Back to [4.1 Governance Foundations](04-01-00-governance-foundations.md).
