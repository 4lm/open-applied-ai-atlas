# 6.1.2 Decision Boundaries And Handling Heuristics

_Page Type: Decision Guide | Maturity: Draft_

Use this page to decide which boundary question actually dominates before choosing controls or providers.

## Decision Lanes

| Boundary lane | Use it when the main question is... |
| --- | --- |
| Privacy-first | lawful basis, minimization, retention, deletion, rights handling, or personal-data exposure |
| Sovereignty-first | who controls operation, support access, telemetry, key management, and deployability |
| Portability-first | whether data, traces, memory, or policy state can be exported, deleted, and migrated without vendor paralysis |
| Combined review | personal data is processed through a managed service that also controls logs, support, or cross-border operations |

## Practical Heuristics

- Do not accept region selection as proof of sovereignty; inspect support access, telemetry routing, subcontractors, and override rights.
- Map the full data surface before approving the posture: prompts, outputs, logs, traces, embeddings, memory, eval sets, and support artifacts.
- Treat "no training on your data" as only one claim among many; retention and support-copy behavior still matter.
- Ask whether export and deletion are technically demonstrable or only described in documentation.
- Route to chapter `18` when a different sourcing posture is cleaner than trying to contract around weak boundary control.
- Route to chapter `4` when the main issue becomes approval ownership, review triggers, or exception handling.

## Escalate When

- the team cannot explain where logs, traces, memory, or evaluation artifacts are stored
- export, deletion, or support-access answers differ across sales, docs, and engineering contacts
- telemetry or cross-border handling appears only in detailed service terms
- the same system claims strong privacy posture but has weak portability and opaque support operations

## Common Failure Modes

- treating privacy compliance as if it automatically solves sovereignty
- treating contract language as if it were equivalent to observable technical control
- ignoring persistence created by memory, monitoring, or offline evaluation workflows

## Chapter Handoffs

- [4. Governance Risk Compliance](../04-governance-risk-compliance/04-00-00-governance-risk-compliance.md)
- [11. Knowledge Retrieval And Memory](../11-knowledge-retrieval-and-memory/11-00-00-knowledge-retrieval-and-memory.md)
- [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md)
- [20. Standards Frameworks And Bodies Of Knowledge](../20-standards-frameworks-and-bodies-of-knowledge/20-00-00-standards-frameworks-and-bodies-of-knowledge.md)

Back to [6.1 Boundary Foundations](06-01-00-boundary-foundations.md).
