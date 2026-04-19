# 1.1.4 Atlas Priorities: Openness, Sovereignty, Portability, Privacy, Compliance

_Page Type: Concept Explainer | Maturity: Draft_

These priorities are the atlas's recurring review lenses, not optional values statements. Use this page when a discussion about models, platforms, procurement, or delivery is drifting toward convenience, speed, or benchmark performance alone and the team needs to reopen the control, reversibility, and organizational-risk questions that actually shape the decision.

The five lenses are linked but not interchangeable. A stack can be open without being sovereign, portable without being privacy-safe, or compliant on paper while still creating heavy operational lock-in. The atlas keeps them visible together so later chapters do not mistake one favorable property for broad implementation safety.

## What Each Lens Changes

| Lens | Ask early | What it changes in practice | Common shortcut to reject |
| --- | --- | --- | --- |
| Openness | Which parts of the system are inspectable, reusable, and replaceable without private permission from one supplier? | Whether the team can verify claims, reuse knowledge, benefit from standards and community practice, and avoid treating one vendor roadmap as the only path forward | treating "open" as a synonym for low-risk, low-cost, or sovereign |
| Sovereignty | Who actually controls hosting location, operator access, support escalation, telemetry, and dependency on foreign legal or commercial control points? | Whether the organization can satisfy residency, sector, public-interest, or strategic-control requirements and still operate during contract, geopolitical, or provider changes | reducing sovereignty to region selection alone |
| Portability | How hard is it to move the workload, data, interfaces, evaluation assets, and operating procedures to another stack later? | Whether the current choice remains reversible when price, performance, policy, or supplier concentration changes | calling an API wrapper or export feature a complete exit strategy |
| Privacy | Which data classes, prompts, outputs, logs, traces, memory stores, and human review pathways expose personal, confidential, or sensitive information? | Whether the deployment needs stronger minimization, retention, access control, processor review, or human-handling constraints before rollout | discussing privacy only at source-dataset level while ignoring runtime traces and support access |
| Compliance | Which laws, regulations, contracts, sector rules, or assurance frameworks shape how the system must be designed, reviewed, documented, and operated? | Whether the team must add approval gates, evidence artifacts, testing discipline, incident handling, or supplier obligations before launch | treating compliance as a final legal sign-off instead of a design constraint |

## Why Lock-In Stays In Frame

The title lists five lenses, but lock-in remains the recurring consequence check across all of them.

- weak openness can create knowledge, tooling, or roadmap dependence
- weak sovereignty can create dependence on one jurisdiction, operator chain, or support path
- weak portability can turn switching cost into a strategic constraint
- weak privacy controls can make one vendor's handling model too risky to replace casually
- weak compliance design can bind the organization to whichever supplier can satisfy audit and evidence demands fastest

If a proposal sounds attractive only while its present vendor, hosting model, or workflow suite stays fixed, the atlas treats that as a real architectural and sourcing concern rather than a procurement footnote.

## How To Use These Lenses Together

### 1. Start With The Dominant Constraint

Name the first constraint that can invalidate the proposal outright:

- public-sector and regulated environments often start with sovereignty, privacy, or compliance
- internal platform decisions often start with portability and lock-in because one internal standard can shape many future use cases
- open-source-first or research-adjacent teams often start with openness, but they still need to test whether openness is enough to satisfy privacy, support, and operating-model needs

### 2. Check For False Comfort

A favorable answer on one lens does not close the others.

- An open-weight model can still create weak sovereignty if the managed control plane, support route, or evaluation tooling is external.
- A region-local hosted service can still create heavy lock-in if prompts, policies, orchestration logic, or approval workflows become provider-specific.
- A compliant procurement package can still be weak on portability if the evidence model only works inside one vendor suite.

### 3. Hand Off To The Owning Chapter

Use this page to reopen the right question, then move the work to the chapter that owns the detailed decision.

| If the unresolved question is mainly about... | Move to... |
| --- | --- |
| policy ownership, risk acceptance, or control design | [4. Governance Risk Compliance](../04-governance-risk-compliance/04-00-00-governance-risk-compliance.md) |
| data classes, residency, retention, or processor posture | [6. Data Sovereignty And Privacy](../06-data-sovereignty-and-privacy/06-00-00-data-sovereignty-and-privacy.md) |
| model, hosting, gateway, or runtime architecture trade-offs | chapters [7](../07-model-ecosystem/07-00-00-model-ecosystem.md) through [15](../15-security-and-abuse-resistance/15-00-00-security-and-abuse-resistance.md) |
| market concentration, supplier control, or ecosystem leverage | [17. Vendors Organizations And Market Structure](../17-vendors-organizations-and-market-structure/17-00-00-vendors-organizations-and-market-structure.md) |
| reversibility, sourcing posture, or exit-path design | [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md) |
| legal texts, standards, or framework combinations | [20. Standards Frameworks And Bodies Of Knowledge](../20-standards-frameworks-and-bodies-of-knowledge/20-00-00-standards-frameworks-and-bodies-of-knowledge.md) |

## Escalate When

- a proposal is being justified mainly by benchmark quality, user delight, or time-to-demo while reversibility and control posture remain vague
- a team uses "EU hosted", "private", "open", or "compliant" as a complete answer without naming the actual operator, data, evidence, and exit assumptions underneath
- procurement, architecture, and governance readers are each optimizing a different lens and nobody has named the trade-off explicitly
- an internal platform standard is about to spread across many use cases before the portability and support consequences are understood
- the system touches regulated decisions, sensitive records, or cross-border operations but the implementation plan still treats these lenses as downstream review items

## Reading Rule

Use these priorities to expose the constraint that most changes architecture, sourcing, and operating burden. If the discussion still sounds acceptable only because one favorable label is hiding the rest of the trade-off surface, the team is not ready to move past chapter `1`.

Back to [1.1 Mission And Scope](01-01-00-mission-and-scope.md).
