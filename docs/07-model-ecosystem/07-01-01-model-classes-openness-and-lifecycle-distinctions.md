# 7.1.1 Model Classes, Openness, And Lifecycle Distinctions

_Page Type: Concept Explainer | Maturity: Draft_

This subsection isolates the most reusable distinctions in the chapter so later implementation and comparison material stays anchored to the right concepts.

This distinction layer matters because the chapter on model ecosystem is only useful if readers can separate the recurring categories, responsibilities, or evidence types that would otherwise blur together. The atlas uses distinctions like this to keep comparison rigorous and to stop local shorthand from hiding governance, sourcing, or operational consequences.

## Why These Distinctions Matter

The practical question is not whether the labels are elegant. The practical question is whether the distinctions change how a team designs, reviews, buys, operates, or audits a system. In this chapter, that means checking whether the topic is being reasoned about in the right layer and with the right cross-cutting lenses still visible.

## Key Lenses

| Comparison lens | Why it matters |
| --- | --- |
| Method fit | Prevents model choice from outrunning the actual problem class |
| Access posture | Shows whether API-only or self-hostable options are acceptable |
| Lifecycle burden | Surfaces version churn, benchmark opacity, and deprecation risk |
| Adaptation path | Connects model choice to retrieval, prompting, or training decisions |

## What Matters Most

- Method family matters before vendor branding
- Openness and deployment freedom should be explicit
- Retrieval and workflow often matter more than raw model breadth
- Version churn and deprecation are practical design concerns

## What Reviewers Should Check

- Are the distinctions here still connected to the chapter's real decision surface rather than being treated as abstract categories?
- Is the proposal using these distinctions to expose trade-offs in control, evidence, ownership, or lock-in?
- Does the chapter language stay consistent with the atlas taxonomy instead of introducing new local categories without need?

## Practical Reading Rule

Use this file to sharpen the chapter, not to replace it. If a proposal still sounds plausible after the distinctions here are applied, it is usually ready to move into heuristics, scenarios, or reference material. If it falls apart, the distinction work has already paid for itself.

Back to [7.1 Model Ecosystem Foundations](07-01-00-model-ecosystem-foundations.md).
