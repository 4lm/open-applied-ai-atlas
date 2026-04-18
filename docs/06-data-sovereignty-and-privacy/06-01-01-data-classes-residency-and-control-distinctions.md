# 6.1.1 Data Classes, Residency, And Control Distinctions

This subsection isolates the most reusable distinctions in the chapter so later implementation and comparison material stays anchored to the right concepts.

This distinction layer matters because the chapter on data sovereignty and privacy is only useful if readers can separate the recurring categories, responsibilities, or evidence types that would otherwise blur together. The atlas uses distinctions like this to keep comparison rigorous and to stop local shorthand from hiding governance, sourcing, or operational consequences.

## Why These Distinctions Matter

The practical question is not whether the labels are elegant. The practical question is whether the distinctions change how a team designs, reviews, buys, operates, or audits a system. In this chapter, that means checking whether the topic is being reasoned about in the right layer and with the right cross-cutting lenses still visible.

## Key Lenses

| Boundary lens | What it makes visible |
| --- | --- |
| Data touchpoints | Shows that AI systems handle more than original source documents |
| Runtime and support paths | Reveals where managed services still retain effective control |
| Retention and reuse | Surfaces hidden persistence obligations |
| Exit posture | Connects privacy and sovereignty decisions to portability |

## What Matters Most

- The real boundary includes prompts, outputs, logs, memory, and evaluation traces
- Residency claims are weaker than operational control claims
- Memory and telemetry change privacy posture materially
- Export and deletion posture matter early, not only at exit time

## What Reviewers Should Check

- Are the distinctions here still connected to the chapter's real decision surface rather than being treated as abstract categories?
- Is the proposal using these distinctions to expose trade-offs in control, evidence, ownership, or lock-in?
- Does the chapter language stay consistent with the atlas taxonomy instead of introducing new local categories without need?

## Practical Reading Rule

Use this file to sharpen the chapter, not to replace it. If a proposal still sounds plausible after the distinctions here are applied, it is usually ready to move into heuristics, scenarios, or reference material. If it falls apart, the distinction work has already paid for itself.

Back to [6.1 Boundary Foundations](06-01-00-boundary-foundations.md).
