# 11.1.1 Knowledge State, Provenance, And Core Distinctions

_Page Type: Concept Explainer | Maturity: Draft_

This subsection isolates the most reusable distinctions in the chapter so later implementation and comparison material stays anchored to the right concepts.

This distinction layer matters because the chapter on knowledge retrieval and memory is only useful if readers can separate the recurring categories, responsibilities, or evidence types that would otherwise blur together. The atlas uses distinctions like this to keep comparison rigorous and to stop local shorthand from hiding governance, sourcing, or operational consequences.

## Why These Distinctions Matter

The practical question is not whether the labels are elegant. The practical question is whether the distinctions change how a team designs, reviews, buys, operates, or audits a system. In this chapter, that means checking whether the topic is being reasoned about in the right layer and with the right cross-cutting lenses still visible.

## Key Lenses

| Knowledge lens | What it clarifies |
| --- | --- |
| Retrieval versus memory | Prevents teams from using long-lived memory as a convenience substitute for search |
| Provenance | Makes traceability and answer justification visible |
| Permission inheritance | Tests whether AI abstractions preserve source access rules |
| Freshness and revocation | Connects knowledge quality to lifecycle and governance decisions |

## What Matters Most

- Retrieval, memory, and training solve different problems
- Provenance should be treated as product behavior, not only debug metadata
- Persistent memory creates deletion and access obligations
- Permission inheritance matters as much as retrieval relevance

## What Reviewers Should Check

- Are the distinctions here still connected to the chapter's real decision surface rather than being treated as abstract categories?
- Is the proposal using these distinctions to expose trade-offs in control, evidence, ownership, or lock-in?
- Does the chapter language stay consistent with the atlas taxonomy instead of introducing new local categories without need?

## Practical Reading Rule

Use this file to sharpen the chapter, not to replace it. If a proposal still sounds plausible after the distinctions here are applied, it is usually ready to move into heuristics, scenarios, or reference material. If it falls apart, the distinction work has already paid for itself.

Back to [11.1 Retrieval Foundations](11-01-00-retrieval-foundations.md).
