# AGENTS.md

## Purpose

This file defines the durable working rules for humans and coding agents contributing to Open Applied AI Atlas.

The repository mission is to support applied organizational AI and ML across sectors, sizes, and roles with explicit attention to openness, sovereignty, portability, privacy, compliance, and vendor dependence. It is not an LLM-only knowledge base.

## Working Order

1. Read the root guidance docs and understand the numbered chapter model before editing.
2. Keep repository-level guidance at root and topical depth inside `docs/`.
3. Extend numbered subchapter files before expanding a chapter front door such as `05-00-00-use-cases-and-application-landscapes.md`.
4. Reconcile numbering, links, titles, and taxonomy reuse before finishing.
5. Remove duplication, broken links, and temporary scaffolding at the end.

## Repository Boundaries

| Area | Allowed content | Not allowed |
| --- | --- | --- |
| Root | README, contributor guidance, editorial rules, changelog, and other repository-level docs | Topic deep dives and duplicate chapter content |
| `docs/` | Numbered chapter indexes and numbered subchapter files | Root process guidance copied into topic docs |
| `docs/02-taxonomy/` | Canonical taxonomy families, openness-policy tiers, and reuse rules | Competing taxonomy definitions elsewhere |

## Chapter Structure Contract

- Every chapter folder includes a chapter front door file named `CC-00-00-<chapter-slug>.md` so the chapter sorts correctly in file explorers.
- The chapter front door is a real outline of the chapter and should list the numbered subchapters.
- Section overview files use `CC-SS-00-<section-slug>.md`.
- Subchapter files use `CC-SS-TT-<subchapter-slug>.md`.
- The maximum depth is chapter + two subchapter levels.
- Every file begins with a numbered H1 that matches its place in the outline.

## Authoring Model

The repository uses a mixed-format documentation style:

- prose for explanation and narrative framing
- bullets for distinctions, heuristics, steps, and anti-patterns
- Mermaid for diagrams and flow-style explanation when visuals help
- comparison tables where side-by-side reading is genuinely useful

Do not force every section into a table. Do not add tiny tables where a short paragraph or bullet list would communicate better. Do not reintroduce generic file-family names as the chapter contract.

## Durable Rules

- Reuse taxonomy before introducing new labels.
- Keep governance, model, runtime, ecosystem, and sourcing concerns distinct.
- Preserve the broad applied-AI-and-ML mission; do not let generic GenAI framing displace forecasting, recommender, vision, speech, optimization, classical ML, or hybrid-system coverage.
- Link adjacent chapters coherently so readers can move through the stack.
- Prefer official sources when naming tools, standards, organizations, or projects.
- Use primary legal texts for laws and regulations where possible, for example EUR-Lex for EU regulations, rather than third-party explainer sites.
- Keep public language neutral and avoid marketing voice.
- Update numbering and backlinks whenever a chapter file is renamed or moved.
- Keep `README.md` mission-led and one-page in spirit; chapter and file mechanics should remain secondary to scope, audience, landscape, and cross-cutting priorities.

## Ralph Wiggum Loop

1. Produce a first pass.
2. Inspect for dumbness, duplication, taxonomy drift, weak framing, broken links, and public-facing messiness.
3. Repair factual or structural problems.
4. Simplify wording, sectioning, and unnecessary table use.
5. Re-check adjacent-doc consistency, numbering, and readability.
6. Remove temporary artifacts that no longer belong.
