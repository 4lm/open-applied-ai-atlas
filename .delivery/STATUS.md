# Delivery Status

This file is the internal execution board for the active Product Improvement Plan. Use it to understand what the current highest-leverage tranche is, which gaps remain open, which pass changed what, and what should happen next.

Operator note: `./scripts/delivery-harness-check.sh` validates delivery consistency. `./scripts/delivery-harness-status.sh` prints the current delivery snapshot. `./scripts/ralph-codex.sh` is a human-run external loop that launches fresh `codex exec` passes against `.delivery/PROMPT.md` by default; human usage examples live in `README.md` and `./scripts/ralph-codex.sh --help`.

## Current State

| Field | Value |
| --- | --- |
| Active PIP | Open Applied AI Atlas Product Improvement Plan |
| Current tranche | Knowledge retrieval and adaptation decision surfaces (`11`, `12`) in progress; retrieval fronts and the adaptation operating front are stronger, but adaptation chapter/reference fronts and retrieval/adaptation pattern surfaces remain thin |
| Last completed pass ID | `2026-04-18.u` |
| Current recommendation | `continue G-08` |

## Workstream Board

| Workstream | Status | Active gap IDs | Done when |
| --- | --- | --- | --- |
| `WS1` Reduce Boilerplate And Repetition | Active | `G-01`, `G-05`, `G-06`, `G-08`, `G-09`, `G-10`, `G-13` | chapter and section front doors are concise across the remaining weak clusters |
| `WS2` Increase Information Density And Asymmetry | Active | `G-01`, `G-05`, `G-06`, `G-07`, `G-08`, `G-09`, `G-10`, `G-13` | remaining thin pages are strengthened, merged, or explicitly deferred |
| `WS3` Add Decision-Grade Artifacts | Active | `G-05`, `G-06`, `G-07`, `G-08`, `G-09`, `G-10`, `G-13` | major open chapters each include usable decision aids, scenarios, or operational artifacts |
| `WS4` Separate Concept, Evidence, And Action | Active | `G-06`, `G-07`, `G-08`, `G-09`, `G-10`, `G-13` | page-type structure is obvious in the remaining weak chapters |
| `WS5` Visible Page Maturity Model | Done |  | all pages carry visible maturity labels and current tracking is aligned |
| `WS6` Citation And Evidence Discipline | Active | `G-06`, `G-09`, `G-13` | trust-critical comparison and standards pages show stronger primary-source grounding |
| `WS7` Comparison Schema Consistency | Active | `G-06`, `G-09`, `G-13` | comparison-heavy pages use stable reusable fields and evidence notes where needed |
| `WS8` Glossary / Terminology Ledger | Done |  | the terminology ledger remains the shared fast-reference anchor |
| `WS9` Strengthen High-Leverage Chapters First | Active | `G-05`, `G-06`, `G-07`, `G-08`, `G-09` | the highest-judgment chapters no longer read like scaffold material |
| `WS10` Prune, Merge, Or Defer Weak Pages | Active | `G-05`, `G-13` | weak standalone pages are resolved instead of lingering as symmetry placeholders |

## Gap Ledger

| Gap ID | Area | Workstream(s) | Gap type | Status | Leverage | Default next action | Page-audit scope | Closed by pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `G-01` | Scope and principles orientation surfaces (`01`) | `WS1`, `WS2`, `WS9` | `boilerplate` | Open | Medium | Rewrite front doors and reader-mode pages into stronger chapter-specific navigation | `01.*` |  |
| `G-02` | Taxonomy deepening and applied classification (`02`) | `WS2`, `WS4`, `WS6`, `WS7`, `WS9` | `thin_content` | Closed | High | Keep chapter `02` stable as the shared taxonomy and comparison spine for later chapter passes | `02.*` | `2026-04-18.d` |
| `G-03` | Stack-map and reference-architecture coherence (`03`, `19`) | `WS1`, `WS2`, `WS4`, `WS9`, `WS10` | `thin_content` | Closed | High | Keep chapters `03` and `19` stable as the stack-boundary and reference-architecture bridge for later passes | `03.*`, `19.*` | `2026-04-18.e` |
| `G-04` | Cross-cutting core chapters hardened (`04`, `06`, `17`) | `WS1`, `WS2`, `WS4`, `WS6`, `WS9` | `tracking_drift` | Closed | High | Keep these chapters stable as reference patterns for later passes | `04.*`, `06.*`, `17.*` | `2026-04-18.a` |
| `G-05` | Use-case portfolio density and asymmetry cleanup (`05`) | `WS1`, `WS2`, `WS3`, `WS9`, `WS10` | `thin_content` | Open | High | Deepen prioritization logic and resolve weak pattern/reference surfaces | `05.*` |  |
| `G-06` | Model, hosting, and gateway stack refinement (`07`, `08`, `09`) | `WS1`, `WS2`, `WS4`, `WS6`, `WS7`, `WS9` | `thin_content` | Open | High | Push runtime, hosting, and gateway foundations and reference pages to review-ready | `07.*`, `08.*`, `09.*` |  |
| `G-07` | Agentic operating surfaces completion (`10`) | `WS2`, `WS3`, `WS4`, `WS9` | `thin_content` | Open | High | Finish operating and reference surfaces so chapter `10` is consistent with its stronger decision pages | `10.*` |  |
| `G-08` | Knowledge retrieval and adaptation decision surfaces (`11`, `12`) | `WS1`, `WS2`, `WS3`, `WS4`, `WS9` | `thin_content` | Open | High | Finish the remaining adaptation section fronts and strengthen retrieval/adaptation pattern sheets | `11.*`, `12.*` |  |
| `G-09` | Assurance, observability, and security hardening (`13`, `14`, `15`) | `WS2`, `WS3`, `WS4`, `WS6`, `WS7`, `WS9` | `evidence_gap` | Open | High | Finish evaluation foundations and strengthen observability and security artifact/reference pages | `13.*`, `14.*`, `15.*` |  |
| `G-10` | Human oversight operating model completion (`16`) | `WS2`, `WS3`, `WS4`, `WS9` | `thin_content` | Open | Medium | Deepen oversight foundations, scenarios, and operational artifacts | `16.*` |  |
| `G-11` | Build-vs-buy follow-through and reference cleanup (`18`) | `WS1`, `WS2`, `WS3`, `WS7`, `WS9` | `thin_content` | Closed | High | Keep chapter `18` stable as a sourcing reference pattern for later passes | `18.*` | `2026-04-18.f` |
| `G-12` | Standards and bodies system completion (`20`) | `WS1`, `WS2`, `WS3`, `WS4`, `WS6`, `WS7`, `WS9`, `WS10` | `evidence_gap` | Closed | High | Keep chapter `20` stable as the standards-selection and standards-combination reference pattern for later passes | `20.*` | `2026-04-18.g` |
| `G-13` | Research and open-knowledge completion (`21`) | `WS1`, `WS2`, `WS3`, `WS4`, `WS6`, `WS7`, `WS10` | `thin_content` | Open | Medium | Deepen knowledge-source foundations and close weak reference surfaces | `21.*` |  |
| `G-14` | Delivery harness drift | `WS10` | `tracking_drift` | Closed | High | Maintain the single-board execution model and run harness checks after substantial passes | `.delivery`, `AGENTS.md`, `CONTENT_AUDIT_SUMMARY.md`, `CHANGELOG.md` | `2026-04-18.b` |

## Pass Log

### `2026-04-18.u`

- Date: `2026-04-18`
- Tranche: Adaptation operating section front (`12`)
- Goal: Rewrite the adaptation operating section overview into a concrete operating-review surface so chapter `12` no longer relies on scaffold prose between its stronger escalation and scenario pages
- Workstreams advanced: `WS1`, `WS2`, `WS4`, `WS9`
- Gap IDs moved: none
- Pages / chapter clusters touched: chapter `12`, plus page-audit, audit-summary, status, and changelog tracking
- Maturity moves: `12-02-00` promoted from `Outline` to `Review-Ready`
- Commit(s): `pending`
- Remaining gaps: `G-01`, `G-05`, `G-06`, `G-07`, `G-08`, `G-09`, `G-10`, `G-13`

### `2026-04-18.t`

- Date: `2026-04-18`
- Tranche: Retrieval operating section front (`11`)
- Goal: Rewrite the retrieval operating section overview into a concrete operating-review surface so chapter `11` no longer relies on scaffold prose between its stronger foundations and scenario pages
- Workstreams advanced: `WS1`, `WS2`, `WS4`, `WS9`
- Gap IDs moved: none
- Pages / chapter clusters touched: chapter `11`, plus page-audit, audit-summary, status, and changelog tracking
- Maturity moves: `11-02-00` promoted from `Outline` to `Review-Ready`
- Commit(s): `pending`
- Remaining gaps: `G-01`, `G-05`, `G-06`, `G-07`, `G-08`, `G-09`, `G-10`, `G-13`

### `2026-04-18.s`

- Date: `2026-04-18`
- Tranche: Retrieval foundations section front (`11`)
- Goal: Rewrite the retrieval foundations section overview into a concrete decision surface so chapter `11` starts from retrieval-versus-memory boundaries rather than scaffold prose
- Workstreams advanced: `WS1`, `WS2`, `WS4`, `WS9`
- Gap IDs moved: none
- Pages / chapter clusters touched: chapter `11`, plus page-audit, audit-summary, status, and changelog tracking
- Maturity moves: `11-01-00` promoted from `Outline` to `Review-Ready`
- Commit(s): `pending`
- Remaining gaps: `G-01`, `G-05`, `G-06`, `G-07`, `G-08`, `G-09`, `G-10`, `G-13`

### `2026-04-18.r`

- Date: `2026-04-18`
- Tranche: Adaptation foundation heuristics (`12`)
- Goal: Rewrite the adaptation decision-guide page into a concrete escalation surface so chapter `12` has usable lanes, triggers, and chapter handoffs before teams jump from prompts or retrieval into tuning or retraining
- Workstreams advanced: `WS2`, `WS3`, `WS4`, `WS9`
- Gap IDs moved: none
- Pages / chapter clusters touched: chapter `12`, plus page-audit, audit-summary, status, and changelog tracking
- Maturity moves: `12-01-02` promoted from `Draft` to `Review-Ready`
- Commit(s): `pending`
- Remaining gaps: `G-01`, `G-05`, `G-06`, `G-07`, `G-08`, `G-09`, `G-10`, `G-13`

### `2026-04-18.q`

- Date: `2026-04-18`
- Tranche: Adaptation worked scenarios (`12`)
- Goal: Rewrite the adaptation worked-example page into concrete escalation scenarios so chapter `12` has usable guidance for prompt-first stabilization, retrieval-before-training, justified fine-tuning, and classical retraining under drift
- Workstreams advanced: `WS2`, `WS3`, `WS4`, `WS9`
- Gap IDs moved: none
- Pages / chapter clusters touched: chapter `12`, plus page-audit, audit-summary, status, and changelog tracking
- Maturity moves: `12-02-01` promoted from `Outline` to `Review-Ready`
- Commit(s): `pending`
- Remaining gaps: `G-01`, `G-05`, `G-06`, `G-07`, `G-08`, `G-09`, `G-10`, `G-13`

### `2026-04-18.p`

- Date: `2026-04-18`
- Tranche: Ralph completion detection hardening
- Goal: Refactor `scripts/ralph-codex.sh` so Ralph only stops when the final assistant reply emits the completion marker, preventing prompt echo or transcript echo from ending a multi-pass PIP run early
- Workstreams advanced: `WS10`
- Gap IDs moved: none
- Pages / chapter clusters touched: root operator guidance, `.delivery`, audit summary, changelog, and `scripts/`
- Maturity moves: none
- Commit(s): `pending`
- Remaining gaps: `G-01`, `G-05`, `G-06`, `G-07`, `G-08`, `G-09`, `G-10`, `G-13`

### `2026-04-18.o`

- Date: `2026-04-18`
- Tranche: Knowledge retrieval worked scenarios (`11`)
- Goal: Rewrite the retrieval worked-example page into concrete decision-grade scenarios so chapter `11` has a usable operating reference for live retrieval, bounded memory, graph-backed retrieval, and permission-sensitive access design
- Workstreams advanced: `WS2`, `WS3`, `WS4`, `WS9`
- Gap IDs moved: none
- Pages / chapter clusters touched: chapter `11`, plus page-audit, audit-summary, status, and changelog tracking
- Maturity moves: `11-02-01` promoted from `Outline` to `Review-Ready`
- Commit(s): `pending`
- Remaining gaps: `G-01`, `G-05`, `G-06`, `G-07`, `G-08`, `G-09`, `G-10`, `G-13`

### `2026-04-18.n`

- Date: `2026-04-18`
- Tranche: Ralph console logging refactor
- Goal: Refactor `scripts/ralph-codex.sh` so Codex output stays on the console, replace per-iteration stdout/stderr files with a recreated root `.ralph` timing ledger, and add ignore coverage for the generated file
- Workstreams advanced: `WS10`
- Gap IDs moved: none
- Pages / chapter clusters touched: root operator guidance, `.delivery`, audit summary, changelog, root ignore rules, and `scripts/`
- Maturity moves: none
- Commit(s): `pending`
- Remaining gaps: `G-01`, `G-05`, `G-06`, `G-07`, `G-08`, `G-09`, `G-10`, `G-13`

### `2026-04-18.m`

- Date: `2026-04-18`
- Tranche: Ralph default prompt and full-auto clarification
- Goal: Add `.delivery/PROMPT.md`, make it the default Ralph prompt, document that Ralph already runs in explicit auto-allow mode, and expand help/examples for profiles and env-var options
- Workstreams advanced: `WS10`
- Gap IDs moved: none
- Pages / chapter clusters touched: root operator guidance, `.delivery`, audit summary, delivery status tracking, changelog, and `scripts/`
- Maturity moves: none
- Commit(s): `pending`
- Remaining gaps: `G-01`, `G-05`, `G-06`, `G-07`, `G-08`, `G-09`, `G-10`, `G-13`

### `2026-04-18.l`

- Date: `2026-04-18`
- Tranche: Ralph loop rollout
- Goal: Add `scripts/ralph-codex.sh` as a human-run external Codex loop, move human guidance into `README.md` and script help, tighten the README overview, and set `MAX_ITERS` default to `100` as a safety stop
- Workstreams advanced: `WS10`
- Gap IDs moved: none
- Pages / chapter clusters touched: root operator guidance, audit summary, delivery status tracking, changelog, and `scripts/`
- Maturity moves: none
- Commit(s): `pending`
- Remaining gaps: `G-01`, `G-05`, `G-06`, `G-07`, `G-08`, `G-09`, `G-10`, `G-13`

### `2026-04-18.g`

- Date: `2026-04-18`
- Tranche: Standards and bodies system completion (`20`)
- Goal: Rewrite chapter `20` into a review-ready standards-selection and standards-combination system with stronger scenarios, clearer page-type differentiation, and a standards crosswalk grounded in official sources
- Workstreams advanced: `WS1`, `WS2`, `WS3`, `WS4`, `WS6`, `WS7`, `WS9`, `WS10`
- Gap IDs moved: `G-12` `Open -> Closed`
- Pages / chapter clusters touched: chapter `20`, plus page-audit, audit-summary, status, and changelog tracking
- Maturity moves: all `20.*` pages promoted from `Outline` / `Draft` to `Review-Ready`
- Commit(s): `pending`
- Remaining gaps: `G-01`, `G-05`, `G-06`, `G-07`, `G-08`, `G-09`, `G-10`, `G-13`

### `2026-04-18.f`

- Date: `2026-04-18`
- Tranche: Build-vs-buy follow-through and reference cleanup (`18`)
- Goal: Harden the remaining sourcing distinction, operational, pattern, and reference-overview surfaces so chapter `18` reads as a review-ready sourcing chapter rather than a partial scaffold
- Workstreams advanced: `WS1`, `WS2`, `WS3`, `WS7`, `WS9`
- Gap IDs moved: `G-11` `Open -> Closed`
- Pages / chapter clusters touched: chapter `18`, plus page-audit, audit-summary, status, and changelog tracking
- Maturity moves: `18-01-01`, `18-01-02`, `18-02-00`, `18-02-02`, and `18-03-00` promoted from `Outline` / `Draft` to `Review-Ready`
- Commit(s): `pending`
- Remaining gaps: `G-01`, `G-05`, `G-06`, `G-07`, `G-08`, `G-09`, `G-10`, `G-12`, `G-13`

### `2026-04-18.e`

- Date: `2026-04-18`
- Tranche: Stack-map and reference-architecture coherence (`03`, `19`)
- Goal: Rewrite the stack-map and reference-architecture chapters into review-ready decision surfaces and resolve the weak chapter `19` standalone pattern page
- Workstreams advanced: `WS1`, `WS2`, `WS4`, `WS9`, `WS10`
- Gap IDs moved: `G-03` `Open -> Closed`
- Pages / chapter clusters touched: chapters `03` and `19`, plus page-audit, audit-summary, status, and changelog tracking
- Maturity moves: retained `03.*` and `19.*` front doors, foundations, and application pages promoted from `Outline` / `Draft` to `Review-Ready`; `19-02-02` removed after merge
- Commit(s): `pending`
- Remaining gaps: `G-01`, `G-05`, `G-06`, `G-07`, `G-08`, `G-09`, `G-10`, `G-11`, `G-12`, `G-13`

### `2026-04-18.d`

- Date: `2026-04-18`
- Tranche: Taxonomy deepening and applied classification (`02`)
- Goal: Harden the taxonomy chapter's distinction, decision, scenario, and pattern surfaces into a review-ready shared control surface
- Workstreams advanced: `WS2`, `WS4`, `WS6`, `WS7`, `WS9`
- Gap IDs moved: `G-02` `Open -> Closed`
- Pages / chapter clusters touched: chapter `02`, plus page-audit, audit-summary, status, and changelog tracking
- Maturity moves: `02-01-01`, `02-01-02`, `02-02-01`, and `02-02-02` promoted from `Outline` / `Draft` to `Review-Ready`
- Commit(s): `pending`
- Remaining gaps: `G-01`, `G-03`, `G-05`, `G-06`, `G-07`, `G-08`, `G-09`, `G-10`, `G-11`, `G-12`, `G-13`

### `2026-04-18.c`

- Date: `2026-04-18`
- Tranche: Delivery harness refinement
- Goal: Split delivery validation from delivery reporting and add explicit process policy for both scripts
- Workstreams advanced: `WS10`
- Gap IDs moved: none
- Pages / chapter clusters touched: `.delivery`, root agent guidance, delivery scripts, and public audit summary surfaces
- Maturity moves: none
- Commit(s): `pending`
- Remaining gaps: `G-01`, `G-02`, `G-03`, `G-05`, `G-06`, `G-07`, `G-08`, `G-09`, `G-10`, `G-11`, `G-12`, `G-13`

### `2026-04-18.b`

- Date: `2026-04-18`
- Tranche: Delivery harness refactor
- Goal: Replace the scattered mutable tracking model with one execution board, one page-state inventory, and one light consistency check
- Workstreams advanced: `WS10`
- Gap IDs moved: `G-14` `Open -> Closed`
- Pages / chapter clusters touched: `.delivery`, root delivery guidance, and public audit summary surfaces
- Maturity moves: none
- Commit(s): `pending`
- Remaining gaps: `G-01`, `G-02`, `G-03`, `G-05`, `G-06`, `G-07`, `G-08`, `G-09`, `G-10`, `G-11`, `G-12`, `G-13`

### `2026-04-18.a`

- Date: `2026-04-18`
- Tranche: Cross-cutting core (`04`, `06`, `17`)
- Goal: Strengthen governance, privacy/sovereignty, and market-structure chapters into review-ready anchor chapters
- Workstreams advanced: `WS1`, `WS2`, `WS3`, `WS4`, `WS6`, `WS9`
- Gap IDs moved: `G-04` `Open -> Closed`
- Pages / chapter clusters touched: chapters `04`, `06`, `17`, plus page-audit and audit-summary tracking
- Maturity moves: target chapter surfaces promoted from `Outline` / `Draft` to `Review-Ready`
- Commit(s): `15573dc`
- Remaining gaps: `G-01`, `G-02`, `G-03`, `G-05`, `G-06`, `G-07`, `G-08`, `G-09`, `G-10`, `G-11`, `G-12`, `G-13`, `G-14`

## Next Queue

1. `G-08` Knowledge retrieval and adaptation decision surfaces
2. `G-09` Assurance, observability, and security hardening
3. `G-05` Use-case portfolio density and asymmetry cleanup
4. `G-06` Model, hosting, and gateway stack refinement
5. `G-10` Human oversight operating model completion
6. `G-01` Scope and principles orientation surfaces
7. `G-13` Research and open-knowledge completion
