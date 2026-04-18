# 6.1.2 Decision Boundaries And Handling Heuristics

_Page Type: Decision Guide | Maturity: Draft_

This subsection explains how to separate privacy questions from sovereignty questions without pretending they can be solved independently.

## Decision Boundaries

- Treat the issue as **privacy-first** when the core concern is lawful basis, minimization, retention, deletion, access rights, or personal-data handling under GDPR or equivalent privacy obligations.
- Treat the issue as **sovereignty-first** when the core concern is who controls operation, support access, telemetry, key runtime services, or contractual override power.
- Treat the issue as **portability-first** when the risk is whether data, traces, memory state, or policy configuration can be exported, deleted, or migrated in a supplier change.
- Treat the issue as **combined privacy and sovereignty review** when personal data is processed through a managed service that also controls logging, support access, or cross-border operations.

## Practical Heuristics

- Do not accept region selection as proof of sovereignty; also inspect support pathways, telemetry routing, subcontractors, and contractually permitted access.
- Map the full data surface before judging the boundary posture: prompts, outputs, logs, traces, memory, evaluation artifacts, and support snapshots.
- Ask whether deletion and export are technically verifiable or only contractually promised.
- Use GDPR logic when the key question is personal-data rights and lawful handling; use EU Data Act logic when the key question is access, sharing, ecosystem control, or portability posture.
- When a supplier claims “no training on your data,” still inspect retention, observability, abuse-detection logging, and support-copy behavior.
- Route to chapter `18` when the cleanest boundary answer may require a different sourcing posture rather than a different contract clause.

## Escalate When

- The team cannot explain where logs, traces, memory, or evaluation artifacts are stored.
- A provider’s boundary posture depends on undocumented operational practices.
- Export, deletion, or support-access answers change depending on which sales or engineering contact is asked.
- Cross-border processing, customer-data reuse, or telemetry exceptions appear only in detailed terms or support policies.

## Common Failure Modes

- Treating privacy compliance as if it automatically delivers sovereignty.
- Treating contract language as equivalent to observable technical control.
- Ignoring the persistence created by monitoring, memory, or offline evaluation workflows.

Back to [6.1 Boundary Foundations](06-01-00-boundary-foundations.md).
