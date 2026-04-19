# 1.1.2 Audience, Roles, And Reader Modes

_Page Type: Concept Explainer | Maturity: Review-Ready_

Use this page to name who needs to align before a system review fragments into separate product, architecture, governance, sourcing, or operations conversations. The atlas is built for mixed teams, so reader alignment is not a courtesy step; it is how later chapters avoid solving different problems under the same project name.

## Reader Alignment Map

| Reader lane | What this reader is usually trying to settle first | What chapter `1` should help them clarify before they move on | Best next chapters once alignment exists |
| --- | --- | --- | --- |
| Product, project, and business roles | whether the use case is worth pursuing, who it affects, and how much workflow change it introduces | the organizational consequence, intended users, affected service or process, and which trade-offs cannot be treated as technical details later | [5. Use Cases And Application Landscapes](../05-use-cases-and-application-landscapes/05-00-00-use-cases-and-application-landscapes.md), [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md), [16. Human Oversight And Operating Model](../16-human-oversight-and-operating-model/16-00-00-human-oversight-and-operating-model.md) |
| Architecture and platform roles | where the system sits in the stack, what needs shared control, and how reversible the design should stay | the dominant system family, integration boundaries, dependency shape, and whether the team is solving a one-off feature or a reusable control surface | [2. Taxonomy](../02-taxonomy/02-00-00-taxonomy.md), [3. Enterprise AI Stack Map](../03-enterprise-ai-stack-map/03-00-00-enterprise-ai-stack-map.md), [7. Model Ecosystem](../07-model-ecosystem/07-00-00-model-ecosystem.md), [8. Model Hosting And Inference](../08-model-hosting-and-inference/08-00-00-model-hosting-and-inference.md), [9. Model Gateways And Access Control](../09-model-gateways-and-access-control/09-00-00-model-gateways-and-access-control.md) |
| ML, data, and build roles | what evidence, data, and adaptation work the system will demand in practice | whether the work is predictive, retrieval-heavy, generative, optimization-oriented, perception-based, or hybrid, and how much ongoing evaluation or retraining burden that implies | [5. Use Cases And Application Landscapes](../05-use-cases-and-application-landscapes/05-00-00-use-cases-and-application-landscapes.md), [11. Knowledge Retrieval And Memory](../11-knowledge-retrieval-and-memory/11-00-00-knowledge-retrieval-and-memory.md), [12. Training Fine-Tuning And Adaptation](../12-training-fine-tuning-and-adaptation/12-00-00-training-fine-tuning-and-adaptation.md), [13. Evaluation Testing And QA](../13-evaluation-testing-and-qa/13-00-00-evaluation-testing-and-qa.md) |
| Assurance, privacy, security, and GRC roles | what obligations, evidence, and review triggers appear once the system affects real users or data | the accountable owner, data boundary, harm surface, and whether the discussion is still exploratory or already making release-significant choices | [4. Governance Risk Compliance](../04-governance-risk-compliance/04-00-00-governance-risk-compliance.md), [6. Data Sovereignty And Privacy](../06-data-sovereignty-and-privacy/06-00-00-data-sovereignty-and-privacy.md), [13. Evaluation Testing And QA](../13-evaluation-testing-and-qa/13-00-00-evaluation-testing-and-qa.md), [15. Security And Abuse Resistance](../15-security-and-abuse-resistance/15-00-00-security-and-abuse-resistance.md), [20. Standards Frameworks And Bodies Of Knowledge](../20-standards-frameworks-and-bodies-of-knowledge/20-00-00-standards-frameworks-and-bodies-of-knowledge.md) |
| Operations, sourcing, and leadership roles | what level of control, staffing, supplier dependence, and operating burden the organization is actually willing to own | whether the problem demands shared internal capability, managed external service, or a hybrid posture with explicit exit and oversight expectations | [16. Human Oversight And Operating Model](../16-human-oversight-and-operating-model/16-00-00-human-oversight-and-operating-model.md), [17. Vendors Organizations And Market Structure](../17-vendors-organizations-and-market-structure/17-00-00-vendors-organizations-and-market-structure.md), [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md), [19. Reference Architectures](../19-reference-architectures/19-00-00-reference-architectures.md) |

## Core Distinctions

| Distinction | Why it changes the review |
| --- | --- |
| Job title vs. reader mode | The same person may read as a product owner in one meeting and as an incident approver or procurement reviewer in another. Useful chapter entry depends on the question being asked, not the badge alone. |
| Sponsor vs. accountable operator | A leader can fund the work without owning the runtime, exception handling, or evidence burden. If those owners are not named, downstream chapters will look more certain than the operating model really is. |
| Specialist depth vs. shared decision surface | Security, ML, or platform specialists may each need deep local detail later, but chapter `1` should first surface the questions they must answer together. |
| Orientation pass vs. implementation pass | Some readers only need to classify the problem and pull in the right chapters; others are already making architecture, procurement, or control decisions. Confusing those modes leads to premature tool debates or stale high-level prose. |
| Enterprise separation vs. small-team compression | Large organizations distribute ownership across many roles; smaller teams often combine product, architecture, operations, and privacy judgment in a few people. The atlas should still keep each concern visible even when one reader holds several roles. |

## Reader Modes And Expected Outputs

| Reader mode | Use it when | A useful pass should produce |
| --- | --- | --- |
| Orientation mode | the team still needs a shared description of the system family, affected workflow, and reader set before it can classify or govern the work | a named use-case family, a short list of relevant readers, and the next chapter set to read together |
| Design mode | architecture, data, gateway, retrieval, hosting, or sourcing choices are becoming concrete | explicit handoffs into stack, model, hosting, retrieval, or sourcing chapters with known control and dependency questions |
| Assurance mode | privacy, security, evaluation, legal, or policy concerns now shape whether the system can proceed | named review owners, control triggers, evidence needs, and the adjacent chapters that must participate before rollout |
| Leadership mode | the decision is mainly about investment level, operating posture, supplier dependence, and acceptable organizational risk | a clear statement of what the organization is willing to own itself, what it may delegate, and what exit or oversight conditions are non-negotiable |

## What This Changes In Practice

- Start by naming the live reader set, not the abstract audience list. Ask who is shaping scope, who owns runtime or workflow consequences, who must sign off, and who will live with the operating burden after launch.
- Use the smallest reader set that still covers the real decision. A low-risk internal productivity aid may only need product, platform, and privacy alignment, while a citizen-facing or regulated system may need governance, security, procurement, and oversight readers from the start.
- Treat role disagreements as useful signals. If product readers want speed, architecture readers want shared controls, and GRC readers want stronger evidence, the conflict is telling you which later chapters must stay in the loop.
- Reopen chapter `1` when the active readers change. A system that begins as a prototype for one team may need a different reading path once it becomes a shared service, procurement package, or public-facing workflow.
- Keep small-team reality visible without collapsing concerns. One person may cover several lanes, but the questions about ownership, portability, privacy, evidence, and exit still need distinct answers.

## Reviewer Checks

- Which readers are actually active in this decision right now, and which ones are missing but will later inherit risk, operations, or accountability?
- Is the team arguing from different reader modes, such as orientation versus approval, without naming that shift?
- Who sponsors the work, who operates it, and who owns exception handling, evaluation refresh, and exit posture?
- Has the discussion already moved into classification, stack, governance, privacy, oversight, or sourcing questions that another chapter should own next?
- If one reader holds multiple roles, are the distinct review concerns still visible or being collapsed into convenience language?

Use this page long enough to name the active readers, the mode they are reading in, and the handoff they need next. Then move to [1.2 Using The Atlas](01-02-00-using-the-atlas.md) for chapter sequencing, or jump directly into taxonomy, stack, governance, privacy, oversight, or sourcing chapters once reader alignment is no longer the blocker.

Back to [1.1 Mission And Scope](01-01-00-mission-and-scope.md).
