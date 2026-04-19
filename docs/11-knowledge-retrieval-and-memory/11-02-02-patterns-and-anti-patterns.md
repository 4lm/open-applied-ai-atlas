# 11.2.2 Patterns And Anti-Patterns

_Page Type: Reference Sheet | Maturity: Draft_

Use this page during design and renewal review to recognize healthy retrieval and memory shapes before convenience state hides provenance, permissions, deletion duties, or escalation into adaptation work.

## Reusable Retrieval Patterns

| Pattern | What good looks like | Fit signal | Review warning |
| --- | --- | --- | --- |
| Live retrieval from owned source of truth | Answers are assembled from current, owner-backed material at request time, with minimal long-lived state beyond indexing and trace data | source material changes regularly or policy accuracy matters more than conversational continuity | the team starts caching answer text or "helpful summaries" as if they were durable facts |
| Bounded memory with typed schema and expiry | Cross-session state is limited to a small set of approved fields such as preferences, workflow state, or user-authored notes, with retention and deletion rules attached | continuity matters, but most operational facts still belong in systems of record | free-form memory starts collecting sensitive facts, policy content, or account state because schema work looked slower |
| Hybrid retrieval with structured filters or graph edges | Semantic search is paired with metadata filters, canonical IDs, or relationship traversal so ownership, dependency, and escalation paths survive ingestion | the dominant questions depend on entities, permissions, or operational relationships rather than isolated fragments | the graph or metadata layer is added, but the team still cannot explain source hierarchy, fallback rules, or incomplete-edge handling |
| Permission-aware retrieval with revocation path | Access control is enforced in indexing and retrieval, and the team can revoke or re-index content when rights change | mixed-sensitivity corpora or role-specific answers are part of the design | permission checks happen only in the UI or after retrieval, so restricted content can still influence generation |
| Provenance-first answer assembly | Source identity, freshness, and citation behavior are treated as product behavior, not only observability detail | users must trust not just relevance, but why an answer appeared and whether it is current | citations are present, but nobody can explain source version, owner, or what happens when the source is withdrawn |

## Retrieval Anti-Patterns

| Anti-pattern | Why it fails | Early signal | Review action |
| --- | --- | --- | --- |
| Memory as a cache for changing facts | Convenience persistence turns fast-changing operational or policy content into stale state that looks authoritative | the proposal says memory will "reduce repeated lookups" for facts that already have systems of record | force the team to separate continuity state from factual state and justify every persisted field |
| Chunk-first indexing with no source hierarchy | Relevance may look good in demos while document authority, owner boundaries, and update logic disappear | ingestion treats every file as interchangeable chunks with no durable source model | require source classes, owner mapping, and refresh rules before wider rollout |
| Permissions added after retrieval | Front-end filtering cannot reliably undo leaked retrieval candidates, cached snippets, or embeddings built from restricted material | the team says access will be checked "before display" rather than in retrieval paths and indexes | reopen privacy and security review with chapter `06` and chapter `15` before shipping |
| Retrieval used to mask missing knowledge operations | Search quality becomes the scapegoat for bad source ownership, weak curation, or unresolved content duplication | the corpus is large, but nobody owns freshness, archive rules, or canonical copies | stop tuning retrieval until source governance and owner assignment are explicit |
| Fine-tuning to patch freshness or provenance failures | Training or fine-tuning adds cost and lock-in while leaving the real knowledge-state problem unresolved | adaptation is proposed because retrieval answers are inconsistent, uncited, or stale | pull chapter `12` back in and prove retrieval, source hygiene, and evaluation are insufficient first |

## Review Prompts

- Which pattern best matches the dominant knowledge shape: live retrieval, bounded memory, hybrid retrieval, or permission-sensitive retrieval?
- What evidence proves that source ownership, freshness, and revocation still hold after indexing, caching, and answer assembly?
- Which anti-pattern would most likely appear after the first successful rollout, not just in the initial design review?
- Which chapter must re-enter the decision before approval: `06`, `12`, `15`, or `16`?

## Drift Signals

- user convenience requests keep expanding the memory schema without new retention or deletion controls
- retrieval quality discussion dominates review while source ownership and update behavior remain vague
- the team can show citations, but not source version, owner, or revocation behavior
- permission-sensitive content is treated as a front-end filtering issue instead of an indexing and retrieval issue
- adaptation work is proposed before the team has proved that retrieval boundaries and source hygiene are already sound

Back to [11.2 Operating Retrieval And Memory](11-02-00-operating-retrieval-and-memory.md).
