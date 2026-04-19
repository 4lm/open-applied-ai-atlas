# 1.3.1 Root Docs And Topic Chapters

_Page Type: Concept Explainer | Maturity: Review-Ready_

Use this page when a proposed addition sounds useful, but the team has not yet decided whether it is repository contract, optional prompt/control context, or reusable applied-AI content. Placement is not a housekeeping detail. It changes who the audience is, how often the material should change, what kind of evidence it needs, and whether the atlas stays readable instead of turning topical pages into process notes or root guidance into a topic dump.

The key boundary is simple: root guidance explains the durable repository contract; optional prompt artifacts in `pips/` hold task-specific planning context when a task explicitly uses them; numbered chapter files explain applied organizational AI and ML itself. The hard part is spotting mixed material early enough that mission, contributor workflow, operator guidance, and temporary prompt context do not get copied into the wrong layer.

## Root Docs Map

Every root-level Markdown contract doc should appear in this map so the repository has one explicit inventory of durable root guidance.

| Root doc | Primary audience | What it owns |
| --- | --- | --- |
| [README.md](../../README.md) | public readers and new contributors | public atlas entry point, chapter navigation, and links into chapter-owned orientation pages |
| [MISSION.md](../../MISSION.md) | all readers and contributors | durable mission, audience, scope, and priorities |
| [CONTRIBUTING.md](../../CONTRIBUTING.md) | contributors | contribution workflow, evidence posture, and review expectations |
| [EDITORIAL_RULES.md](../../EDITORIAL_RULES.md) | contributors and editors | canonical numbering, page structure, page types, and maturity rules |
| [AGENTS.md](../../AGENTS.md) | coding agents and operators | durable operator rules and mission guardrails |
| [RALPH_CONTROLLER.md](../../RALPH_CONTROLLER.md) | Ralph operators | `./scripts/ralph-codex.py` usage, controller state model, and verification |
| [CHANGELOG.md](../../CHANGELOG.md) | contributors and reviewers | completion-only root ledger |
| [CONTRIBUTORS.md](../../CONTRIBUTORS.md) | public readers | public contributor list |

## Repository Placement Map

| If the material is mainly about... | Put it here | Why this is the right layer | Typical mistake to reject |
| --- | --- | --- | --- |
| public mission, chapter navigation, contribution entry points, operator instructions, or other durable repository promises | repository root such as `README.md`, `MISSION.md`, `CONTRIBUTING.md`, `EDITORIAL_RULES.md`, `AGENTS.md`, `RALPH_CONTROLLER.md`, `CHANGELOG.md`, and `CONTRIBUTORS.md` | these files define how readers, contributors, and operators enter, understand, and maintain the atlas across many chapters | restating the same repository rules inside a topic page just because that chapter was recently edited |
| explicitly referenced task prompts, optional plan artifacts, or temporary workstream framing | `pips/` | prompt artifacts belong in a separate control layer rather than in public topical pages | burying task-local prompt context inside chapter prose or using topical docs as a project board |
| taxonomy, use-case logic, governance patterns, sourcing trade-offs, architecture choices, standards, or implementation guidance | `docs/` in the numbered chapter that owns the topic | chapter content should remain reusable knowledge that survives changes in the current prompt or editing pass | pushing substantive topic guidance into root docs because the immediate trigger was an editing dispute |
| one-off scratch notes, private reminders, or temporary coordination text with no durable reader value | nowhere in the published repo unless intentionally retained for operators | weak temporary material raises noise quickly and creates fake completeness | keeping temporary scaffolding because it helped one pass land |

## What Each Layer Owns

| Layer | Owner question it answers | What belongs there | What does not belong there |
| --- | --- | --- | --- |
| Root guidance | "How does this repository work, and what durable contract should readers, contributors, and operators follow?" | public entry docs, mission, contribution workflow, editorial rules, operator references, changelog policy, and durable agent instructions | chapter-deep explainers, product-style long topical surveys, or task-local prompt state |
| `pips/` prompt layer | "Is there optional task-local prompt context that should stay out of durable root guidance and public topical docs?" | explicitly invoked PIPs, task-local plan artifacts, and prompt-level workstreams | durable mission scope, evergreen topic content, or default repo instructions |
| Numbered chapter system | "What should readers know to classify, compare, design, govern, source, or operate applied AI and ML systems?" | chapter-specific explanations, decision guides, worked examples, operational artifacts, reference sheets, glossary content | duplicate copies of root rules, contribution policy, or mutable execution bookkeeping |

## Fast Boundary Tests

| Ask this first | If the answer is yes | Then the next move is |
| --- | --- | --- |
| Will this still be true if the current task prompt changes next week? | the content is durable | place it in root guidance or `docs/`, depending on whether it is repository contract or topical knowledge |
| Does the text tell contributors how to maintain the atlas rather than helping readers make an AI or ML decision? | it is repository process | keep it in root guidance or an explicitly invoked prompt artifact, not in numbered chapter prose |
| Would a public reader benefit even if they never contribute to the repo? | it is probably chapter content or `README` navigation | write it in `docs/` or the root public entry surface instead of improvement-control files |
| Is the main value a task-local workstream, current prompt priority, or plan-specific instruction? | it is prompt state | keep it in `pips/` instead of narrating it in chapter text |
| Is the proposal only needed because another file is weak, repetitive, or misplaced? | the placement problem is a symptom | strengthen or trim the owning page instead of adding another explanatory duplicate |

## Misplacement Signals

| Signal | What it usually means | Better placement or action |
| --- | --- | --- |
| A topic page starts explaining how contributors should manage controller sessions, completion markers, or other runtime-only mechanics | outer execution control leaked into public chapter content | move the process rule to operator-facing root guidance and leave only the chapter-facing handoff |
| `README.md` or `CONTRIBUTING.md` starts carrying deep taxonomy, architecture, or standards explanations | root guidance is compensating for thin chapter content | move the substance into the owning numbered chapter and keep the root file navigational |
| `RALPH_CONTROLLER.md` starts carrying repo-wide contribution policy or PIP governance rules | the operator reference is absorbing repo contract material that belongs elsewhere | move the durable repo rule back to `MISSION.md`, `CONTRIBUTING.md`, `EDITORIAL_RULES.md`, or `AGENTS.md` and keep the controller doc tool-specific |
| A `pips/` file begins restating topical knowledge to justify a pass | improvement control is doing the chapter's job | summarize the plan delta briefly and move durable explanation back into `docs/` |
| A new file exists mainly to preserve outline symmetry, but it cannot name a durable reader decision | the repo is accumulating scaffold instead of knowledge | merge, defer, or remove it rather than adding thin prose |

## Reviewer Checks

- Is the intended audience a public reader, a contributor, or an operator steering a task-local prompt artifact?
- Will the material stay valid after the current prompt pass closes, or is it inherently mutable state?
- Does the proposed text explain applied AI and ML decisions, or only how this repository should organize and review that explanation?
- Has any root or `pips/` guidance been copied into `docs/` instead of linked?
- If the material is truly topical, which numbered chapter owns it so readers can find it again later?

## Practical Reading Rule

Keep chapter `1` focused on boundary-setting long enough to sort the material into the right layer. Once the placement is clear, move immediately to the owning root file, optional prompt artifact, or numbered chapter instead of leaving repository process and topical knowledge mixed together.

Back to [1.3 Repository Contract](01-03-00-repository-contract.md).
