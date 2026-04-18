# Content Audit Summary

This summary records the current public quality signals under the Product Improvement Plan.

The detailed per-page inventory lives in `.delivery/page-audit.md`. This public summary keeps the durable signals visible for contributors without turning the root of the repository into a spreadsheet dump.

Last delivery update: `2026-04-18.p` on `2026-04-18`.

## Current Counts

### By Page Type

- `Chapter Index`: 84
- `Comparison Page`: 27
- `Concept Explainer`: 26
- `Decision Guide`: 23
- `Glossary`: 1
- `Operational Artifact`: 10
- `Reference Sheet`: 20
- `Worked Example`: 21

### By Maturity

- `Outline`: 55
- `Draft`: 47
- `Review-Ready`: 109
- `Curated Reference`: 1

## What Changed

- Hardened `scripts/ralph-codex.sh` so Ralph only stops when the final assistant reply contains the completion marker, preventing prompt echo or transcript echo from ending multi-pass runs early.
- Promoted `docs/11-knowledge-retrieval-and-memory/11-02-01-worked-retrieval-scenarios.md` from `Outline` to `Review-Ready` by rewriting it as a set of retrieval-versus-memory decision scenarios with explicit evidence outputs and chapter handoffs.
- Refactored `scripts/ralph-codex.sh` so Codex output stays on the console, `.ralph` is recreated as a single per-run timing ledger, and the generated root `.ralph` file is ignored.
- Added `.delivery/PROMPT.md` as the default Ralph prompt, clarified that Ralph already runs in explicit auto-allow mode, and expanded script help with profile and env-var examples.
- Added `scripts/ralph-codex.sh` as a human-run external Codex loop, moved human guidance into `README.md` and script help, tightened the README overview, and set `MAX_ITERS` default to `100` as a safety stop.
- Added a visible page-type and maturity system to `docs/`.
- Reduced recurring chapter and section boilerplate.
- Added a terminology ledger and a canonical comparison schema in the taxonomy chapter.
- Hardened the taxonomy chapter's distinction, heuristic, scenario, and pattern surfaces into review-ready decision aids and closed `G-02`.
- Promoted the stack-map and reference-architecture chapters into review-ready decision surfaces and resolved the thin standalone chapter `19` pattern page.
- Closed `G-11` by hardening the remaining build-vs-buy sourcing distinctions, operational review surfaces, pattern sheet, and reference overview in chapter `18`.
- Closed `G-12` by rewriting chapter `20` into a review-ready standards-selection and standards-combination system with stronger scenarios and an official-source-backed standards crosswalk.
- Added first-wave decision and artifact pages in high-leverage chapters.
- Strengthened evidence posture on comparison-heavy and standards-heavy pages.
- Promoted the governance, privacy, and market-structure chapters through a concentrated cross-cutting pass.

## Canonical Page Types

- `Chapter Index`
- `Concept Explainer`
- `Comparison Page`
- `Decision Guide`
- `Worked Example`
- `Operational Artifact`
- `Reference Sheet`
- `Glossary`

## Canonical Maturity Levels

- `Outline`: structure exists but decision value is still limited.
- `Draft`: useful material exists, but the page is incomplete, uneven, or lightly evidenced.
- `Review-Ready`: substantial and coherent enough for editorial review.
- `Curated Reference`: stable, denser, and primary-source-anchored reference material.

## Main Boilerplate Families Reduced

- Repeated chapter-front-door justification prose.
- Repeated section-overview justification prose.
- Repeated worked-example introductions.
- Repeated “named comparison material” intros on reference pages.

## Highest-Priority Remaining Outline Pages

- `docs/01-scope-and-principles/01-02-00-using-the-atlas.md` (Chapter Index)
- `docs/01-scope-and-principles/01-03-00-repository-contract.md` (Chapter Index)
- `docs/07-model-ecosystem/07-00-00-model-ecosystem.md` (Chapter Index)
- `docs/08-model-hosting-and-inference/08-03-00-reference-points.md` (Chapter Index)
- `docs/11-knowledge-retrieval-and-memory/11-01-00-retrieval-foundations.md` (Chapter Index)
- `docs/12-training-fine-tuning-and-adaptation/12-03-00-reference-points.md` (Chapter Index)
- `docs/13-evaluation-testing-and-qa/13-01-00-evaluation-foundations.md` (Chapter Index)
- `docs/21-research-open-knowledge-and-community/21-00-00-research-open-knowledge-and-community.md` (Chapter Index)

## Reading Rule

Treat the maturity label as a navigation aid, not a claim that lower-maturity pages should be ignored. The atlas is explicit about where it is strong, where it is still developing, and which pages should anchor high-trust decisions first.
