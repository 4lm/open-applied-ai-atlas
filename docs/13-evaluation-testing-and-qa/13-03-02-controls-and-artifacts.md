# 13.3.2 Controls And Artifacts

This subsection holds the chapter's named comparison material. Read it as a reference layer, not as a substitute for the chapter's conceptual and implementation sections.

Controls and artifacts matter because evaluation testing and qa only becomes durable when somebody can review it, approve it, operate it, and revisit it after something changes. The atlas treats documents, logs, decision records, checklists, and control evidence as working tools rather than bureaucratic decoration.

## Why Artifacts Matter

A control that cannot be tied to an owner, a trigger, or a review moment is underspecified. An artifact that nobody reuses during release, incident response, or audit work is probably only nominally part of the operating model.

## Artifact Flow

```mermaid
flowchart LR
    A[Design decision] --> B[Required artifact]
    B --> C[Review and approval]
    C --> D[Release or deployment]
    D --> E[Incident or audit reuse]
```

This file translates the chapter into concrete controls, documents, and review artifacts teams usually need in practice.

## How To Use This File

- The goal is repeatable execution, not documentation for its own sake.
- Good artifacts should support review, release, and incident response.
- If a control cannot be tied to an owner or a trigger, it is probably underspecified.

## QA Artifacts

| Artifact | Purpose |
| --- | --- |
| Gold set | Stable reference behavior |
| Replay set | Realistic regression coverage |
| Scenario pack | Workflow and edge-case testing |
| Review rubric | Human evaluation consistency |

## QA Controls

| Control | Purpose |
| --- | --- |
| Release gate | Prevents untested changes from shipping |
| Regression suite | Protects against drift |
| Adversarial testing | Finds abuse and safety gaps |

## Reading Notes

- Re-check the main chapter if the comparison starts to feel more detailed than the underlying decision.
- Prefer adjacent chapter context over treating a single table row as a final answer.

## What Good Looks Like

- Each control or artifact has a clear owner and usage point.
- The same artifact can support design review, release discipline, and post-change accountability.
- The file makes it easier to ask whether the chapter's promises are actually visible in day-to-day work.

## Practical Reading Rule

Use this file after the concepts and scenarios are clear enough that the question becomes operational evidence. If the organization cannot name which artifacts it would inspect during review, the chapter is not yet implemented in practice.

Back to [13.3 Reference Points](13-03-00-reference-points.md).
