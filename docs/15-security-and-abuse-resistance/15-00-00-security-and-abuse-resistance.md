# 15. Security And Abuse Resistance

This chapter is the front door for Security And Abuse Resistance. It maps threat surfaces, trust boundaries, and abuse resistance so AI-specific and conventional security controls can be combined coherently. The chapter is designed to help readers move from orientation into real decisions without losing the atlas priorities around openness, sovereignty, portability, privacy, compliance, and lock-in.

Security programs underperform when AI systems are treated as ordinary APIs or when new abuse paths are treated as purely model problems.

## Chapter Index

- 15.1 [Security Foundations](15-01-00-security-foundations.md)
- 15.1.1 [Threat Surfaces, Trust Boundaries, And Core Distinctions](15-01-01-threat-surfaces-trust-boundaries-and-core-distinctions.md)
- 15.1.2 [Decision Boundaries And Hardening Heuristics](15-01-02-decision-boundaries-and-hardening-heuristics.md)
- 15.2 [Operating Security And Abuse Resistance](15-02-00-operating-security-and-abuse-resistance.md)
- 15.2.1 [Worked Security Scenarios](15-02-01-worked-security-scenarios.md)
- 15.2.2 [Patterns And Anti-Patterns](15-02-02-patterns-and-anti-patterns.md)
- 15.3 [Reference Points](15-03-00-reference-points.md)
- 15.3.1 [Tools And Platforms](15-03-01-tools-and-platforms.md)
- 15.3.2 [Standards And Bodies](15-03-02-standards-and-bodies.md)
- 15.3.3 [Controls And Artifacts](15-03-03-controls-and-artifacts.md)

## Why This Chapter Exists

The atlas uses chapter front doors as real chapter maps, not as thin navigation stubs. This chapter therefore has to do more than list files. It should explain why the topic matters, show how the chapter is segmented, and help a reader choose the right depth before they disappear into detailed tables or worked examples.

That matters here because security and abuse resistance is rarely a self-contained question. Decisions in this chapter usually spill into adjacent chapters about governance, data boundaries, evidence, security, operations, or sourcing. The front door keeps those relationships visible before local optimization starts.

## Chapter Shape

```mermaid
flowchart LR
    C0["15.1 Security Foundations"]
    C1["15.2 Operating Security And Abuse Resistance"]
    C2["15.3 Reference Points"]
    C0 --> C1
    C1 --> C2
```

## What This Chapter Helps Decide

- what the main threat surfaces are
- where trust boundaries and control boundaries need to harden
- which security and abuse-resistance controls should block rollout
- which adjacent chapters should be read next because the issue is no longer only about security and abuse resistance

## How To Use This Chapter

Start with the first section when the language, scope, or boundary of the topic is still unstable. Move to the second section when the question becomes operational and the team needs practical sequencing, scenarios, or review logic. Use the third section after the conceptual and operating frame is clear enough that named tools, standards, controls, or reference artifacts will sharpen the decision rather than replace it.

If you are reviewing a proposal rather than designing one, use the chapter map to confirm which section the proposal really belongs in. That small check prevents detailed reference material from being mistaken for the whole argument.

## Adjacent Chapters

- Previous: [14. Observability Logging And Monitoring](../14-observability-logging-and-monitoring/14-00-00-observability-logging-and-monitoring.md)
- Next: [16. Human Oversight And Operating Model](../16-human-oversight-and-operating-model/16-00-00-human-oversight-and-operating-model.md)
- Repository guidance: [Contributing](../../CONTRIBUTING.md), [Editorial Rules](../../EDITORIAL_RULES.md)
