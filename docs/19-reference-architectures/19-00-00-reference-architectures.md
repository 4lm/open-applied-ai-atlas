# 19. Reference Architectures

This chapter is the front door for Reference Architectures. It turns the atlas into reusable architecture shapes so teams can compare reference patterns without pretending one stack fits every system. The chapter is designed to help readers move from orientation into real decisions without losing the atlas priorities around openness, sovereignty, portability, privacy, compliance, and lock-in.

Reference architectures become decorative if they are not connected back to constraints, trade-offs, and operating posture.

## Chapter Index

- 19.1 [Architecture Foundations](19-01-00-architecture-foundations.md)
- 19.1.1 [Architecture Shapes, Constraints, And Core Distinctions](19-01-01-architecture-shapes-constraints-and-core-distinctions.md)
- 19.1.2 [Decision Boundaries And Selection Heuristics](19-01-02-decision-boundaries-and-selection-heuristics.md)
- 19.2 [Applying Reference Architectures](19-02-00-applying-reference-architectures.md)
- 19.2.1 [Worked Architecture Scenarios](19-02-01-worked-architecture-scenarios.md)
- 19.2.2 [Patterns And Anti-Patterns](19-02-02-patterns-and-anti-patterns.md)
- 19.3 [Reference Points](19-03-00-reference-points.md)
- 19.3.1 [Tooling By Layer](19-03-01-tooling-by-layer.md)
- 19.3.2 [Reference Stack Solutions](19-03-02-reference-stack-solutions.md)

## Why This Chapter Exists

The atlas uses chapter front doors as real chapter maps, not as thin navigation stubs. This chapter therefore has to do more than list files. It should explain why the topic matters, show how the chapter is segmented, and help a reader choose the right depth before they disappear into detailed tables or worked examples.

That matters here because reference architectures is rarely a self-contained question. Decisions in this chapter usually spill into adjacent chapters about governance, data boundaries, evidence, security, operations, or sourcing. The front door keeps those relationships visible before local optimization starts.

## Chapter Shape

```mermaid
flowchart LR
    C0["19.1 Architecture Foundations"]
    C1["19.2 Applying Reference Architectures"]
    C2["19.3 Reference Points"]
    C0 --> C1
    C1 --> C2
```

## What This Chapter Helps Decide

- which reference architecture shape matches the use case
- which control and integration points are non-negotiable
- how to adapt a reference without losing the reason it exists
- which adjacent chapters should be read next because the issue is no longer only about reference architectures

## How To Use This Chapter

Start with the first section when the language, scope, or boundary of the topic is still unstable. Move to the second section when the question becomes operational and the team needs practical sequencing, scenarios, or review logic. Use the third section after the conceptual and operating frame is clear enough that named tools, standards, controls, or reference artifacts will sharpen the decision rather than replace it.

If you are reviewing a proposal rather than designing one, use the chapter map to confirm which section the proposal really belongs in. That small check prevents detailed reference material from being mistaken for the whole argument.

## Adjacent Chapters

- Previous: [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md)
- Next: [20. Standards Frameworks And Bodies Of Knowledge](../20-standards-frameworks-and-bodies-of-knowledge/20-00-00-standards-frameworks-and-bodies-of-knowledge.md)
- Repository guidance: [Contributing](../../CONTRIBUTING.md), [Editorial Rules](../../EDITORIAL_RULES.md)
