# Contributing

Open Applied AI Atlas is a public documentation project. Good contributions improve explanation, implementation usefulness, and comparison clarity without weakening the repository mission: broad applied organizational AI and ML, explicit cross-role usefulness, and recurring focus on openness, sovereignty, portability, privacy, compliance, and lock-in.

## Contribution Workflow

1. Confirm the topic belongs in the current chapter and numbered section structure before adding or moving content.
2. Reuse canonical terms from [2. Taxonomy](docs/02-taxonomy/02-00-00-taxonomy.md) before introducing new labels.
3. Preserve the repository's broad applied-AI scope; do not narrow chapters implicitly to LLM-only framing unless the file is intentionally model-specific.
4. Prefer explanatory prose, bullets, diagrams & graphs (inline Mermaid format), and comparison tables only where side-by-side reading genuinely helps.
5. Keep chapter front doors concise and move substance into numbered subchapter files instead of overloading `CC-00-00-...md`.
6. Add or preserve the visible metadata line directly below the numbered H1: `_Page Type: … | Maturity: …_`.
7. Re-run adjacent links, numbering, and mission framing after structural edits so the chapter outline and reader purpose remain coherent.

## What Good Contributions Look Like

- they help business, engineering, governance, sourcing, or operations readers make a better decision
- they keep openness, sovereignty, portability, privacy, compliance, or lock-in visible where those concerns matter
- they improve a numbered chapter section without breaking the chapter outline
- they reuse taxonomy and chapter language consistently
- they leave the repository more navigable and more mission-faithful than before
- they make the page type obvious instead of relying on generic template prose
- they assign maturity honestly rather than implying polish the page has not earned

## Source Hierarchy

| Source type | How to use it |
| --- | --- |
| Primary sources | Preferred for named tools, standards, laws, regulations, organizations, and projects |
| High-quality public synthesis | Useful for context, not as the final authority |
| Vendor marketing | Treat as claims to verify, not as atlas voice |

## Page Types And Maturity

Use the canonical page-type and maturity definitions in [EDITORIAL_RULES.md](./EDITORIAL_RULES.md). In contribution work, the important discipline is to make the page type obvious and to assign maturity honestly.

## Prompt Artifacts

`pips/` is the optional prompt/control layer described in [1.3.1 Root Docs And Topic Chapters](docs/01-scope-and-principles/01-03-01-root-docs-and-topic-chapters.md). Use a `pips/PIP_*.md` file only for explicitly referenced task context that should stay out of durable root guidance and public atlas chapters.

- Every `pips/PIP_*.md` file must declare `pip-status: live`, `pip-status: archived`, or `pip-status: superseded` in frontmatter.
- `pip-status: superseded` requires `superseded_by`.
- `pip-status: archived` requires `retention_reason`.

## Evidence Notes

Add `## Evidence Notes` when a page:

- makes recommendations from a comparison table
- summarizes vendor, standards, or regulatory claims
- mixes direct facts with atlas synthesis or editorial judgment

Use that section to distinguish:

- primary-source-backed facts
- atlas synthesis
- explicit editorial judgment

## Repository Operations

- Read [RALPH_CONTROLLER.md](./RALPH_CONTROLLER.md) for the authoritative `./scripts/ralph-codex.py` operator reference and controller verification commands.
- Keep operator-facing Ralph details out of reader-facing atlas docs; link to the controller reference instead of duplicating its CLI surface.

## Anti-Patterns

- drifting toward LLM-only framing when a chapter is supposed to cover broader applied AI/ML
- expanding a chapter front door instead of creating or improving a numbered subchapter file
- breaking section numbers, backlinks, or adjacent chapter links
- creating comparison tables when a paragraph or bullet list would be clearer
- removing sovereignty, compliance, or lock-in language from chapters where those concerns materially shape decisions
- keeping a weak standalone page at a high maturity label
- reintroducing stock intro paragraphs that could fit almost any chapter
- burying PIP-only prompt context or frontmatter rules inside public chapter prose
- duplicating Ralph controller flag-by-flag usage across `README.md`, `CONTRIBUTING.md`, and other root docs instead of linking to the canonical reference
