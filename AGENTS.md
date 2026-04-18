# AGENTS.md

## Purpose

This file defines the durable working rules for humans and coding agents contributing to Open Applied AI Atlas.

Use it as the top-level agent contract for mission guardrails, edit routing, evidence posture, and final cleanup. Keep detailed editorial catalogs in the other root guidance files instead of duplicating them here.

## Read First

Before substantive edits, read these root files in this order:

1. `README.md` for mission, audience, and chapter navigation.
2. `CONTRIBUTING.md` for contribution workflow and anti-patterns.
3. `EDITORIAL_RULES.md` for canonical structure, metadata, and evidence rules.
4. `CONTENT_AUDIT_SUMMARY.md` for the current page-type, maturity, and boilerplate-reduction conventions.
5. This file for the durable agent-specific contract.

If guidance overlaps, follow the newer root guidance and keep this file concise rather than turning it into a parallel policy manual.

## Repository Mission

Open Applied AI Atlas is a practical, taxonomy-driven, comparison-oriented, implementation-focused knowledge base for applying AI and ML in business, enterprise, public, nonprofit, and other organizational contexts of all sizes.

The atlas is not an LLM-only repository. Keep broader applied AI and ML visible, including retrieval, memory, forecasting, recommender systems, anomaly detection, optimization, computer vision, speech, classical ML, deep learning, generative AI, hybrid systems, governance, sourcing, architecture, assurance, and operations.

Treat AI systems as organizational systems rather than isolated model demos. Keep openness, sovereignty, portability, privacy, compliance, lock-in, and buy-vs-build visible when they materially shape the decision.

## Responsibility Boundaries

- `AGENTS.md` defines durable agent guardrails and the completion contract.
- `CONTRIBUTING.md` defines contribution workflow, source hierarchy, and contributor anti-patterns.
- `EDITORIAL_RULES.md` defines the canonical structure, page metadata, and evidence rules.
- `CONTENT_AUDIT_SUMMARY.md` explains the current quality pass, page-type system, maturity signals, and boilerplate-reduction posture.

Do not create parallel copies of root guidance inside topical chapter files unless that duplication is intentionally useful to readers.

## Working Order

1. Confirm the topic belongs in the current numbered chapter and section model before adding or moving content.
2. Keep repository-level guidance in root files and topical depth inside `docs/`.
3. Strengthen numbered subchapter files before expanding a chapter front door such as `05-00-00-use-cases-and-application-landscapes.md`.
4. Reuse taxonomy, chapter language, and comparison conventions before introducing new labels or structures.
5. Reconcile numbering, links, titles, metadata, and adjacent-document coherence before finishing.
6. Remove duplication, stale scaffolding, and temporary artifacts at the end.

## Repository Boundaries

| Area | Allowed content | Not allowed |
| --- | --- | --- |
| Root | README, contributor guidance, editorial rules, changelog, audit summaries, and other repository-level docs | Topic deep dives and duplicate chapter content |
| `docs/` | Numbered chapter indexes, section overviews, subchapter files, and other topical content | Root process guidance copied into topic docs |
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

## Quality Loop

1. Produce a first pass.
2. Inspect for duplication, taxonomy drift, weak framing, broken links, stale scaffolding, and public-facing messiness.
3. Repair factual, structural, metadata, or evidence-posture problems.
4. Simplify wording, sectioning, and unnecessary table use.
5. Re-check adjacent-doc consistency, numbering, links, backlinks, and readability.
6. Confirm the page still uses the right metadata line, preserves taxonomy reuse, and adds `## Evidence Notes` where required.
7. Remove temporary artifacts that no longer belong.
