# AGENTS.md

Durable operator rules for coding-agent work in Open Applied AI Atlas.

## Focus

Work on how to inspect, improve, verify, and maintain the repository and the atlas.

## Read First

For substantive work, read in this order:

1. `AGENTS.md`
2. `MISSION.md`
3. `README.md`
4. `CONTRIBUTING.md`
5. `EDITORIAL_RULES.md`
6. adjacent chapter files and nearby root docs
7. explicitly referenced prompt artifacts

For trivial non-substantive tasks, use judgment. Otherwise inspect the repo before editing.

## Authority

When guidance overlaps, use this order:

1. `AGENTS.md`
2. `MISSION.md`
3. `README.md`, `CONTRIBUTING.md`, `EDITORIAL_RULES.md`
4. local file context and adjacent docs
5. explicitly referenced prompt artifacts

`MISSION.md` is authoritative and must not be edited. Prompt artifacts are optional context, not default policy.
Live PIPs become task context only when explicitly referenced.

## Repository Shape

- Root files carry mission, editorial, contribution, and operator guidance.
- `docs/` holds numbered atlas content.
- `pips/` holds optional prompt artifacts.
- Every `pips/PIP_*.md` file must declare `pip-status: live`, `pip-status: archived`, or `pip-status: superseded` in frontmatter.
- `pip-status: superseded` PIPs must also declare `superseded_by`; `pip-status: archived` PIPs must also declare `retention_reason`.
- Keep internal operator guidance separate from public atlas content.

## Operating Rules

For substantive changes:

1. Orient first: read root guidance and inspect adjacent files before editing.
2. Find the owning chapter, numbering, taxonomy, and backlinks before changing structure.
3. Prefer strengthening existing pages and paths over creating parallel duplicates.
4. When guidance, navigation, filenames, or links change, update the repo and atlas together.
5. Review for mission fit, cross-role usefulness, duplication, taxonomy reuse, evidence posture, numbering, links, and readability.
6. Make another pass if obvious same-pass cleanup remains.

## Durable Rules

- Preserve the broad applied-AI-and-ML mission; do not collapse the atlas into LLM-only framing.
- Keep the atlas useful across business, engineering, governance, privacy, security, sourcing, operations, and leadership roles.
- Keep governance, model, runtime, ecosystem, sourcing, and standards concerns distinct unless a page is explicitly about their interaction.
- Prefer fewer stronger pages over weak symmetry or parallel duplicates.
- Reuse canonical taxonomy and comparison conventions before introducing new labels.
- Keep chapter front doors concise and move substance into numbered subchapter files.
- Add `## Evidence Notes` when comparison, standards, regulatory, or recommendation-heavy material mixes sourced facts with atlas synthesis.
- Remove superseded scaffolding by default. Do not preserve obsolete wording, paths, structure, or compatibility layers unless explicitly required; update affected callers, docs, and tests in the same pass.

## Done When

Work is done only when it materially improves the repo or atlas, preserves mission and scope, avoids duplication, keeps numbering and links coherent, updates affected guidance and tests, removes temporary scaffolding, and leaves no obvious same-pass cleanup.
