# 10.2.2 Patterns And Anti-Patterns

This subsection captures reusable good shapes and recurring failure shapes so the chapter remains useful during design review as well as implementation.

This file captures reusable ways to think about the topic. The point is not to add more categories. The point is to help readers recognize good and bad shapes quickly.

## Patterns To Reuse

- Assistants, workflows, and agents are not branding variants of the same thing
- The safest default is the simplest execution model that fits
- Tool access and approval design matter more than agent rhetoric

## Anti-Patterns To Avoid

- Using the chapter as only a taxonomy layer and never translating it into decisions.
- Keeping comparison tables without explanatory narrative around them.
- Letting local terminology drift away from the canonical chapter language.


## Decision Flow

```mermaid
flowchart TD
    A[Start with chapter question] --> B[Clarify constraints and scope]
    B --> C[Choose smallest viable pattern]
    C --> D[Check adjacent chapter dependencies]
    D --> E[Add review and rollback logic]
```

## Review Prompt

| During review ask... | Why |
| --- | --- |
| Are the chapter distinctions still visible in the proposal? | Prevents local shortcuts from flattening important trade-offs |
| Are openness, sovereignty, privacy, compliance, and lock-in visible where they matter? | Keeps the chapter aligned with the atlas mission |
| Has the team translated the pattern language into an actual design or control decision? | Prevents the section from remaining only descriptive |

Back to [10.2 Operating Agentic Systems](10-02-00-operating-agentic-systems.md).
