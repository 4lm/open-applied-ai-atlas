# 15.1.1 Threat Surfaces, Trust Boundaries, And Core Distinctions

_Page Type: Concept Explainer | Maturity: Draft_

This subsection isolates the most reusable distinctions in the chapter so later implementation and comparison material stays anchored to the right concepts.

This distinction layer matters because the chapter on security and abuse resistance is only useful if readers can separate the recurring categories, responsibilities, or evidence types that would otherwise blur together. The atlas uses distinctions like this to keep comparison rigorous and to stop local shorthand from hiding governance, sourcing, or operational consequences.

## Why These Distinctions Matter

The practical question is not whether the labels are elegant. The practical question is whether the distinctions change how a team designs, reviews, buys, operates, or audits a system. In this chapter, that means checking whether the topic is being reasoned about in the right layer and with the right cross-cutting lenses still visible.

## Key Lenses

| Security lens | Why it matters |
| --- | --- |
| Threat surface mapping | Keeps prompt, retrieval, tool, memory, and gateway risks distinct |
| Least privilege | Constrains how much damage a compromised or misled system can do |
| Containment | Makes sandboxing and approval patterns part of security design |
| Incident reconstruction | Connects abuse handling to observability and governance evidence |

## What Matters Most

- Ai security has to follow the actual architecture
- Prompt filtering alone is not a full security strategy
- Action-capable systems raise the control bar sharply
- Memory, retrieval, and gateway design are part of the threat model

## What Reviewers Should Check

- Are the distinctions here still connected to the chapter's real decision surface rather than being treated as abstract categories?
- Is the proposal using these distinctions to expose trade-offs in control, evidence, ownership, or lock-in?
- Does the chapter language stay consistent with the atlas taxonomy instead of introducing new local categories without need?

## Practical Reading Rule

Use this file to sharpen the chapter, not to replace it. If a proposal still sounds plausible after the distinctions here are applied, it is usually ready to move into heuristics, scenarios, or reference material. If it falls apart, the distinction work has already paid for itself.

Back to [15.1 Security Foundations](15-01-00-security-foundations.md).
