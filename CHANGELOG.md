# Changelog

## Unreleased

| Date | Change |
| --- | --- |
| 2026-04-18 | Hardened `scripts/ralph-codex.sh` so Ralph only stops when the final assistant reply contains the completion marker, preventing prompt echo or transcript echo from ending multi-pass runs early (`2026-04-18.p`). |
| 2026-04-18 | Rewrote `docs/11-knowledge-retrieval-and-memory/11-02-01-worked-retrieval-scenarios.md` into review-ready scenario tables covering live retrieval, bounded memory, graph-backed retrieval, and permission-sensitive access design (`2026-04-18.o`). |
| 2026-04-18 | Refactored `scripts/ralph-codex.sh` to stream Codex output directly to the console, replace per-iteration `iter-*.out` / `iter-*.err` artifacts with a recreated root `.ralph` timing ledger, and add ignore coverage for that generated file (`2026-04-18.n`). |
| 2026-04-18 | Added `.delivery/PROMPT.md` as the default Ralph prompt, clarified that Ralph already runs in explicit auto-allow mode, and expanded script help with profile and env-var examples (`2026-04-18.m`). |
| 2026-04-18 | Added `scripts/ralph-codex.sh` as a human-run external Codex loop, moved human guidance into `README.md` and script help, tightened the README overview, and set `MAX_ITERS` default to `100` as a safety stop (`2026-04-18.l`). |
| 2026-04-18 | Closed `G-12` by rewriting chapter `20` into a review-ready standards-selection and standards-combination system with stronger scenarios, pattern guidance, and an official-source-backed standards crosswalk (`2026-04-18.g`). |
| 2026-04-18 | Closed `G-11` by rewriting the remaining chapter `18` sourcing distinction, application, pattern, and reference-overview pages into review-ready decision surfaces (`2026-04-18.f`). |
| 2026-04-18 | Rewrote the stack-map and reference-architecture chapters into review-ready decision surfaces, merged the weak standalone chapter `19` pattern page, and closed `G-03` (`2026-04-18.e`). |
| 2026-04-18 | Hardened the taxonomy chapter's distinction, decision, scenario, and pattern surfaces into review-ready shared guidance and closed the taxonomy deepening gap (`2026-04-18.d`). |
| 2026-04-18 | Split delivery validation from delivery reporting by keeping `delivery-harness-check.sh` quiet and adding `delivery-harness-status.sh` for concise operator snapshots (`2026-04-18.c`). |
| 2026-04-18 | Refactored the delivery harness around `.delivery/STATUS.md`, a gap-linked page audit, and a lightweight harness consistency check (`2026-04-18.b`). |
| 2026-04-17 | Initial repository implementation for Open Applied AI Atlas, including root governance docs, taxonomy foundation, topic corpus, and cleanup discipline. |
