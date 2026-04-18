# 9.1.1 Routing, Identity, And Policy Distinctions

This subsection isolates the most reusable distinctions in the chapter so later implementation and comparison material stays anchored to the right concepts.

This distinction layer matters because the chapter on model gateways and access control is only useful if readers can separate the recurring categories, responsibilities, or evidence types that would otherwise blur together. The atlas uses distinctions like this to keep comparison rigorous and to stop local shorthand from hiding governance, sourcing, or operational consequences.

## Why These Distinctions Matter

The practical question is not whether the labels are elegant. The practical question is whether the distinctions change how a team designs, reviews, buys, operates, or audits a system. In this chapter, that means checking whether the topic is being reasoned about in the right layer and with the right cross-cutting lenses still visible.

## Key Lenses

| Gateway lens | What it clarifies |
| --- | --- |
| Shared controls | Shows when central policy is worth the abstraction cost |
| Identity and attribution | Makes spend, misuse, and accountability visible |
| Provider abstraction | Highlights benefits and the new dependency it introduces |
| Policy portability | Tests whether central control can survive a future migration |

## What Matters Most

- A gateway becomes useful when model access is no longer a one-team concern
- Route abstraction does not erase provider-specific behavior
- Policies should be exportable and reviewable outside one ui
- Gateways can create new lock-in even while reducing direct provider lock-in

## What Reviewers Should Check

- Are the distinctions here still connected to the chapter's real decision surface rather than being treated as abstract categories?
- Is the proposal using these distinctions to expose trade-offs in control, evidence, ownership, or lock-in?
- Does the chapter language stay consistent with the atlas taxonomy instead of introducing new local categories without need?

## Practical Reading Rule

Use this file to sharpen the chapter, not to replace it. If a proposal still sounds plausible after the distinctions here are applied, it is usually ready to move into heuristics, scenarios, or reference material. If it falls apart, the distinction work has already paid for itself.

Back to [9.1 Gateway Foundations](09-01-00-gateway-foundations.md).
