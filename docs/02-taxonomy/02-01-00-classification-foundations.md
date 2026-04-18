# 2.1 Classification Foundations

This section lays the conceptual foundation for Taxonomy. Within the chapter, it provides the canonical taxonomy that keeps tools, models, standards, vendors, controls, and use cases from collapsing into one mixed category, but the emphasis here is narrower: this section exists to establish a shared vocabulary, stable distinctions, and the minimum conceptual frame required before comparison or implementation makes sense.

## Section Map

- 2.1.1 [Entity Classes And Core Distinctions](02-01-01-entity-classes-and-core-distinctions.md)
- 2.1.2 [Cross-Cutting Dimensions And Heuristics](02-01-02-cross-cutting-dimensions-and-heuristics.md)

This deep dive expands the chapter beyond front-door orientation. Its job is to explain the distinctions that make the topic useful in implementation work rather than only in taxonomy or planning language.

## Why This Section Exists

This section exists to establish a shared vocabulary, stable distinctions, and the minimum conceptual frame required before comparison or implementation makes sense. It gives readers a stable place to answer the questions that are most likely to be confused inside taxonomy, which makes later comparison more reliable because it rests on a shared frame instead of local shorthand.

This section should also be read as part of the atlas mission rather than as a self-contained mini-essay. The point is to surface how classification foundations changes control, portability, sovereignty, privacy, compliance, and operating burden in real organizational systems.

## Section Shape

```mermaid
flowchart LR
    S0["2.1.1 Entity Classes And Core Distinctions"]
    S1["2.1.2 Cross-Cutting Dimensions And Heuristics"]
    S0 --> S1
```

## What To Look For Here

- the definitions and boundaries that should remain stable across the chapter
- the trade-offs or category errors that would distort later comparisons
- the chapter-specific lenses that should stay visible in reviews and designs
- where the section should hand the reader off to adjacent chapters instead of trying to answer everything locally

## Reading Guidance

Read this section first whenever the team is still arguing about terms, boundaries, or which problem family is actually in scope. When in doubt, ask whether the material here changes a real decision, review, or operating posture. If it does not, go back up one level and confirm that the right chapter or section is being used.

## Review Prompts

- Are the chapter terms being used consistently with the taxonomy in chapter 2?
- Would a new contributor understand what belongs in this chapter and what belongs elsewhere?
- Do the distinctions here change a real design or review decision later in the stack?

Back to [2. Taxonomy](02-00-00-taxonomy.md).
