# AGENTS.md

## Purpose

This file is the entry-point and usage guide for coding agents working in Open Applied AI Atlas.

Start here before substantive planning, editing, or review work. Use this file to understand how change is driven in this repository, which guidance is durable, which guidance is delivery-specific, and when work is actually done.

Keep detailed editorial catalogs in the other root guidance files instead of duplicating them here.

## Core Delivery Model

Substantive change in this repository is driven through Product Improvement Plans.

- `.delivery/MISSION.md` is the unchangeable scope and value compass.
- `.delivery/PIP.md` is the current change engine and execution driver.
- One PIP can require many quality-improvement passes before the work is actually done.
- `AGENTS.md` tells coding agents how to use those documents together with the durable repository guidance.

Do not edit `.delivery/MISSION.md` or `.delivery/PIP.md`.

## Read Order For Coding Agents

Before substantive work, read these files in this order:

1. `AGENTS.md` for the agent workflow and completion contract.
2. `.delivery/MISSION.md` for immutable mission, scope, and value boundaries.
3. `.delivery/PIP.md` for the active improvement plan and execution target.
4. `README.md` for public mission, audience, and chapter navigation.
5. `CONTRIBUTING.md` for contribution workflow and anti-patterns.
6. `EDITORIAL_RULES.md` for canonical structure, metadata, and evidence rules.
7. `CONTENT_AUDIT_SUMMARY.md` for the current page-type, maturity, and quality-pass conventions.
8. `.delivery/page-audit.md` when the task touches page-level quality work, prioritization, merge/defer choices, or maturity-driven rewrites.

If the task is trivial and clearly non-substantive, use judgment. For any meaningful content, structure, or quality change, follow the full read order.

## Instruction Precedence

Use this precedence when guidance overlaps:

1. `AGENTS.md` for coding-agent operating workflow.
2. `.delivery/MISSION.md` for immutable scope and value boundaries.
3. `.delivery/PIP.md` for the active change objective, success criteria, and workstreams.
4. `README.md`, `CONTRIBUTING.md`, `EDITORIAL_RULES.md`, and `CONTENT_AUDIT_SUMMARY.md` for durable public guidance on mission, structure, evidence, page types, and maturity.
5. Local file context and adjacent documents for topic-specific fit and coherence.

If guidance appears to conflict, preserve the mission, follow the active PIP for change direction, and avoid creating a parallel policy layer in topical docs.

## Responsibility Boundaries

- `AGENTS.md` defines how coding agents should enter, interpret, and complete work in this repository.
- `.delivery/MISSION.md` defines the unchangeable mission, scope, audience, and value compass for the current delivery effort.
- `.delivery/PIP.md` defines the active improvement work that pushes changes forward.
- `README.md` explains the repository publicly.
- `CONTRIBUTING.md` defines contribution workflow and anti-patterns.
- `EDITORIAL_RULES.md` defines canonical structure, page metadata, and evidence rules.
- `CONTENT_AUDIT_SUMMARY.md` exposes the current public quality-pass signals.
- `.delivery/page-audit.md` is the detailed maintenance and prioritization inventory for page-level improvement work.

Do not create parallel copies of root or `.delivery` guidance inside topical chapter files unless that duplication is intentionally useful to readers.

## How Coding Agents Should Work

For substantive tasks, use this workflow:

1. Start from `AGENTS.md`, then read `.delivery/MISSION.md` and `.delivery/PIP.md`.
2. Identify the active PIP objective, workstream, and quality gap relevant to the task.
3. Check the root guidance and adjacent documents so the change fits the repository contract.
4. If the task touches page quality, use `CONTENT_AUDIT_SUMMARY.md` and `.delivery/page-audit.md` to choose the highest-leverage pass.
5. Make a concrete improvement pass that materially advances the PIP rather than just changing wording superficially.
6. Review the result for mission fit, taxonomy reuse, evidence posture, duplication, structure, links, numbering, and public readability.
7. Decide whether another pass is still needed under the same PIP.
8. Continue with further quality-improvement passes until the relevant PIP objective can honestly be considered done.

Do not treat a first pass as completion by default.

## PIP Pass Model

A Product Improvement Plan is the force that pushes change forward in this repository.

- A PIP may require repeated passes across the same file, chapter, or quality problem.
- A pass can rewrite, compress, deepen, merge, defer, reframe, or better evidence the material.
- Additional passes are expected when content is still thin, repetitive, structurally weak, weakly evidenced, poorly differentiated, or below the intended maturity.
- If a page or chapter still obviously needs another quality pass to satisfy the PIP, the work is not done.

Use repeated passes to increase real quality, not to create churn.

## Working Order

1. Confirm the change supports the mission and belongs in the current numbered chapter and section model.
2. Confirm which active PIP objective or workstream the task advances.
3. Keep repository-level guidance in root and `.delivery/`; keep topical depth inside `docs/`.
4. Strengthen numbered subchapter files before expanding a chapter front door such as `05-00-00-use-cases-and-application-landscapes.md`.
5. Reuse taxonomy, chapter language, and comparison conventions before introducing new labels or structures.
6. Reconcile numbering, links, titles, metadata, and adjacent-document coherence before finishing.
7. Remove duplication, stale scaffolding, and temporary artifacts at the end.

## Repository Boundaries

| Area | Allowed content | Not allowed |
| --- | --- | --- |
| Root | README, contributor guidance, editorial rules, changelog, audit summaries, and other repository-level docs | Topic deep dives and duplicate chapter content |
| `.delivery/` | Mission, Product Improvement Plans, page-audit inventories, and other delivery-control artifacts | Public topical deep dives copied from `docs/` |
| `docs/` | Numbered chapter indexes, section overviews, subchapter files, and other topical content | Root or `.delivery` process guidance copied into topic docs |
| `docs/02-taxonomy/` | Canonical taxonomy families, terminology anchors, comparison schema, and reuse rules | Competing taxonomy or ad hoc comparison systems elsewhere |

## Structure Contract

- Every chapter folder includes a chapter front door file named `CC-00-00-<chapter-slug>.md` so the chapter sorts correctly in file explorers.
- The chapter front door is a real outline of the chapter and should list the numbered subchapters.
- Section overview files use `CC-SS-00-<section-slug>.md`.
- Subchapter files use `CC-SS-TT-<subchapter-slug>.md`.
- The maximum depth is chapter plus two subchapter levels.
- Every file begins with a numbered H1 that matches its place in the outline.
- Chapter front doors and section overviews stay concise and navigational; they are not the place for most of the substance.
- When renaming or moving files, update numbering, links, backlinks, and adjacent references together.

## Authoring Model

The repository uses a mixed-format documentation style:

- prose for explanation and narrative framing
- bullets for distinctions, heuristics, steps, and anti-patterns
- Mermaid for diagrams and flow-style explanation when visuals help
- tables for inventories and comparison surfaces when side-by-side reading is genuinely useful

Do not force every section into a table. Do not add tiny tables where a short paragraph or bullet list would communicate better. Do not let pages feel like lightly customized template variants of one another.

## Page Quality And Evidence

- Every page in `docs/` must preserve the visible metadata line directly under the numbered H1 in the canonical form `_Page Type: ... | Maturity: ..._`.
- Preserve honest page-type and maturity signaling. Use the canonical lists and definitions from the root guidance docs instead of restating them ad hoc.
- Make the page's primary job obvious from its structure and wording.
- Reuse canonical terms from `docs/02-taxonomy/02-00-00-taxonomy.md` before introducing new labels.
- Reuse `docs/02-taxonomy/02-02-03-comparison-schema.md` for comparison-heavy pages instead of inventing ad hoc comparison criteria.
- Add `## Evidence Notes` when a page makes recommendations from comparison material, summarizes vendor, standards, or regulatory claims, or mixes direct facts with atlas synthesis or editorial judgment.
- Prefer primary sources for laws, regulations, standards, vendors, organizations, projects, and product claims. Use primary legal texts where possible.

## Durable Rules

- Preserve the broad applied-AI-and-ML mission; do not let generic GenAI framing displace forecasting, recommender systems, vision, speech, optimization, classical ML, or hybrid-system coverage.
- Keep the atlas useful across business, engineering, governance, privacy, security, sourcing, operations, and leadership roles.
- Keep governance, model, runtime, ecosystem, and sourcing concerns distinct unless a page is intentionally about their interaction.
- Keep public language neutral and avoid marketing voice.
- Link adjacent chapters coherently so readers can move through the stack.
- Prefer fewer stronger pages over many weak symmetric pages.
- Avoid generic intro paragraphs that could fit almost any chapter.
- Merge, defer, or avoid expanding thin standalone pages when they do not justify their slot after rewrite and metadata assignment.
- Keep `README.md` mission-led and one-page in spirit; chapter and file mechanics should remain secondary to scope, audience, landscape, and cross-cutting priorities.

## Do And Don't For Coding Agents

Do:

- treat `AGENTS.md` as the entry-point for substantive work
- treat `.delivery/MISSION.md` as the unchangeable scope and value compass
- treat `.delivery/PIP.md` as the active driver of change
- use `CONTENT_AUDIT_SUMMARY.md` and `.delivery/page-audit.md` to choose high-leverage quality passes where relevant
- prefer improving existing content and structure over adding parallel duplicates
- keep mission, taxonomy, evidence posture, and cleanup discipline visible through each pass

Do not:

- edit `.delivery/MISSION.md` or `.delivery/PIP.md`
- declare work done while a PIP-driven quality gap is still clearly open
- duplicate root or `.delivery` guidance into topical documents without a reader-facing reason
- preserve weak structural symmetry just because the outline suggests it
- add filler content to make a page look more complete than it is

## Completion Contract

Work is done only when:

- the result materially advances the active PIP objective
- the mission and scope remain intact
- duplication has not increased
- structure, numbering, links, and references are coherent
- taxonomy reuse and evidence posture still hold
- temporary scaffolding was removed unless intentionally retained
- the affected material no longer obviously needs another quality-improvement pass under the same PIP

## Cleanup Loop

1. Produce a pass that clearly advances the PIP.
2. Inspect for duplication, taxonomy drift, weak framing, broken links, stale scaffolding, and public-facing messiness.
3. Repair factual, structural, metadata, or evidence-posture problems.
4. Simplify wording, sectioning, and unnecessary table use.
5. Re-check adjacent-doc consistency, numbering, links, backlinks, and readability.
6. Confirm the page still uses the right metadata line, preserves taxonomy reuse, and adds `## Evidence Notes` where required.
7. Decide whether another pass is still needed for the same PIP.
8. Remove temporary artifacts that no longer belong.
