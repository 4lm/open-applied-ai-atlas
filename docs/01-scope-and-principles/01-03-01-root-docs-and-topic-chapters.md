# 1.3.1 Root Docs And Topic Chapters

_Page Type: Concept Explainer | Maturity: Review-Ready_

Use this page when a proposed addition sounds useful, but the team has not yet decided whether it is repository contract, mutable delivery tracking, or reusable applied-AI content. Placement is not a housekeeping detail. It changes who the audience is, how often the material should change, what kind of evidence it needs, and whether the atlas stays readable instead of turning topical pages into process notes or root guidance into a topic dump.

The key boundary is simple: root and `.delivery/` explain how the repository is run, maintained, and tracked; numbered chapter files explain applied organizational AI and ML itself. The hard part is spotting mixed material early enough that mission, editorial rules, and delivery state do not get copied into the wrong layer.

## Repository Placement Map

| If the material is mainly about... | Put it here | Why this is the right layer | Typical mistake to reject |
| --- | --- | --- | --- |
| public mission, chapter navigation, contribution entry points, or durable repository promises | repository root such as `README.md`, `CONTRIBUTING.md`, `EDITORIAL_RULES.md`, `AGENTS.md` | these files define how readers and contributors enter, understand, and maintain the atlas across many chapters | restating the same repository rules inside a topic page just because that chapter was recently edited |
| active tranche selection, open gaps, page-audit state, pass history, or operator control files | `.delivery/` and the delivery scripts that validate it | delivery state is mutable execution control, not public topical knowledge | burying live pass state inside chapter prose or using topical docs as a project board |
| taxonomy, use-case logic, governance patterns, sourcing trade-offs, architecture choices, standards, or implementation guidance | `docs/` in the numbered chapter that owns the topic | chapter content should remain reusable knowledge that survives changes in the delivery plan | pushing substantive topic guidance into root docs because the immediate trigger was an editing dispute |
| one-off scratch notes, private reminders, or temporary coordination text with no durable reader value | nowhere in the published repo unless intentionally retained for operators | weak temporary material raises noise quickly and creates fake completeness | keeping temporary scaffolding because it helped one pass land |

## What Each Layer Owns

| Layer | Owner question it answers | What belongs there | What does not belong there |
| --- | --- | --- | --- |
| Root guidance | "How does this repository work, and what durable contract should contributors follow?" | mission-led navigation, contribution workflow, editorial rules, changelog policy, durable agent instructions | chapter-deep explainers, product-style long topical surveys, or live gap-by-gap execution notes |
| `.delivery/` control layer | "What is the active improvement problem right now, and how is progress tracked?" | current PIP state, pass ledger, page audit, harness scripts, operator prompts, tranche status | evergreen topic content that readers should treat as atlas knowledge rather than current execution control |
| Numbered chapter system | "What should readers know to classify, compare, design, govern, source, or operate applied AI and ML systems?" | chapter-specific explanations, decision guides, worked examples, operational artifacts, reference sheets, glossary content | duplicate copies of root rules, contribution policy, or mutable delivery bookkeeping |

## Fast Boundary Tests

| Ask this first | If the answer is yes | Then the next move is |
| --- | --- | --- |
| Will this still be true if the current delivery tranche changes next week? | the content is durable | place it in root guidance or `docs/`, depending on whether it is repository contract or topical knowledge |
| Does the text tell contributors how to maintain the atlas rather than helping readers make an AI or ML decision? | it is repository process | keep it in root guidance or `.delivery/`, not in numbered chapter prose |
| Would a public reader benefit even if they never contribute to the repo? | it is probably chapter content or `README` navigation | write it in `docs/` or the root public entry surface instead of operator tracking files |
| Is the main value a live status signal, gap ID, pass history entry, or audit count? | it is delivery state | keep it in `.delivery/` and validate it with the harness instead of narrating it in chapter text |
| Is the proposal only needed because another file is weak, repetitive, or misplaced? | the placement problem is a symptom | strengthen or trim the owning page instead of adding another explanatory duplicate |

## Misplacement Signals

| Signal | What it usually means | Better placement or action |
| --- | --- | --- |
| A topic page starts explaining how contributors should update status boards, pass IDs, or harness scripts | delivery control leaked into public chapter content | move the process rule to root guidance or `.delivery/` and leave only the chapter-facing handoff |
| `README.md` or `CONTRIBUTING.md` starts carrying deep taxonomy, architecture, or standards explanations | root guidance is compensating for thin chapter content | move the substance into the owning numbered chapter and keep the root file navigational |
| `.delivery/STATUS.md` begins restating topical knowledge to justify a pass | execution tracking is doing the chapter's job | summarize the delivery delta briefly and move durable explanation back into `docs/` |
| A new file exists mainly to preserve outline symmetry, but it cannot name a durable reader decision | the repo is accumulating scaffold instead of knowledge | merge, defer, or remove it rather than adding thin prose |

## Reviewer Checks

- Is the intended audience a public reader, a contributor, or an operator tracking the active tranche?
- Will the material stay valid after the current PIP pass closes, or is it inherently mutable state?
- Does the proposed text explain applied AI and ML decisions, or only how this repository should organize and review that explanation?
- Has any root or `.delivery/` guidance been copied into `docs/` instead of linked?
- If the material is truly topical, which numbered chapter owns it so readers can find it again later?

## Practical Reading Rule

Keep chapter `1` focused on boundary-setting long enough to sort the material into the right layer. Once the placement is clear, move immediately to the owning root file, delivery artifact, or numbered chapter instead of leaving repository process and topical knowledge mixed together.

Back to [1.3 Repository Contract](01-03-00-repository-contract.md).
