# 6.1.1 Data Classes, Residency, And Control Distinctions

_Page Type: Concept Explainer | Maturity: Draft_

This page separates the main boundary concepts that are often discussed as if they were interchangeable. They are not. Privacy answers one set of questions; sovereignty, portability, and operational control answer others.

## Key Distinctions

| Distinction | Why it changes the decision |
| --- | --- |
| Source data vs derived traces | Prompts, outputs, logs, embeddings, evaluations, and memory can create new regulated or sensitive surfaces |
| Residency vs operational control | Region pinning does not prove who can access, support, copy, or override the system |
| Contract promise vs technical verifiability | A vendor claim matters less if deletion, export, and access behavior cannot be checked |
| Short-lived context vs long-lived memory | Persistent memory changes retention, deletion, and user-rights posture materially |
| Privacy compliance vs sovereignty posture | Lawful personal-data handling does not automatically deliver deployability, auditability, or exit control |

## What Changes In Practice

- Boundary reviews should include prompts, outputs, telemetry, support snapshots, and offline evaluation artifacts.
- Support and observability paths often matter as much as primary inference hosting.
- Data portability should be assessed before adoption, not only when a contract ends.
- Memory features should be treated as storage and lifecycle decisions, not only personalization features.

## Review Questions

- Which system traces persist beyond the user interaction?
- Which flows are technically enforced versus contractually asserted?
- Which boundary concern is dominant here: privacy rights, sovereignty, portability, or all three together?

## Handoffs

- Go to [4. Governance Risk Compliance](../04-governance-risk-compliance/04-00-00-governance-risk-compliance.md) when the main problem becomes review ownership, exception handling, or evidence design.
- Go to [17. Vendors Organizations And Market Structure](../17-vendors-organizations-and-market-structure/17-00-00-vendors-organizations-and-market-structure.md) and [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md) when the boundary answer is constrained by supplier concentration or sourcing posture.
- Go to [11. Knowledge Retrieval And Memory](../11-knowledge-retrieval-and-memory/11-00-00-knowledge-retrieval-and-memory.md) when persistent retrieval or memory design is the main technical driver.

Back to [6.1 Boundary Foundations](06-01-00-boundary-foundations.md).
