# 11.1.1 Knowledge State, Provenance, And Core Distinctions

_Page Type: Concept Explainer | Maturity: Draft_

Use this page to separate governed source content, retrieval structures, bounded memory, derived answer artifacts, and model-internal knowledge before teams decide what should persist. Retrieval work goes wrong when those states are treated as interchangeable just because they all influence the answer.

## Knowledge-State Map

| Knowledge state | What it holds | Why teams keep it | Main control obligation | Common failure |
| --- | --- | --- | --- | --- |
| Governed source of truth | policies, product docs, records, runbooks, contracts, or other owner-backed material | preserve the authoritative fact set the system should rely on | named owner, canonical-copy rule, permission model, refresh and archive policy | indexing unofficial copies and then treating them as equally authoritative |
| Retrieval structure | embeddings, chunk indexes, metadata filters, graph edges, or other derived lookup state | make source material discoverable at answer time | inherit source permissions, freshness, revocation, and source hierarchy into the retrieval layer | treating the index as a neutral technical cache with weaker governance than the source |
| Bounded memory state | user preferences, workflow state, approved summaries, or other typed continuity fields | reduce repeated user effort across sessions or tasks | schema limits, retention, deletion, revalidation, and access rules per field | storing changing facts, entitlements, or sensitive content in free-form memory because it feels convenient |
| Derived answer artifact | citations, summaries, extracted facts, intermediate notes, cached responses, or review outputs | speed up downstream work or preserve decision evidence | mark derivation path, expiry, owner, and revalidation expectations | reusing yesterday's answer artifact as if it were still the source of truth today |
| Model-internal knowledge | behavior learned from pretraining, fine-tuning, or retraining | encode stable task behavior or broad priors that are not retrieved live | prove that weight changes are justified, testable, and portable enough for the use case | using adaptation to encode fast-changing business facts that belong in governed sources instead |

## Core Distinctions

| Distinction | Why it changes the design |
| --- | --- |
| Retrieval vs. memory | Retrieval should fetch current governed content; memory should hold only the small continuity state worth persisting across requests. |
| Source authority vs. retrieval convenience | A high-scoring chunk is not automatically the canonical source; source hierarchy and owner responsibility still determine what should be trusted. |
| Provenance vs. citation veneer | A citation string is not enough if the system cannot explain source owner, source version, freshness, or why that source was selected. |
| Permission inheritance vs. front-end filtering | Access controls must survive ingestion, indexing, caching, and answer assembly, not just final display. |
| Freshness vs. relevance | A semantically relevant answer can still be operationally wrong if the source is stale, superseded, or revoked. |
| Relationship model vs. chunk similarity | Entity links, source hierarchy, and metadata filters often matter more than semantic closeness for engineering, legal, and operations questions. |

## What These Distinctions Change In Practice

- Treat retrieval structures as derived state, not as a second authoritative corpus.
- Require every persistent memory field to justify why it cannot be looked up live from a governed system instead.
- Preserve provenance through summaries, extracted facts, and reviewer notes so downstream users can still challenge the source basis.
- Assume deletion and revocation duties apply across indexes, caches, graph edges, and memory state, not only to the original document repository.
- Escalate into adaptation work only after retrieval coverage, freshness, permissions, and provenance already look sound.

## Reviewer Checks

- Can the team name which information lives in governed sources, retrieval structures, bounded memory, derived artifacts, and model behavior?
- Which state is authoritative for a disputed answer, and who owns keeping it current?
- If access is revoked or a source is withdrawn, which indexes, caches, summaries, or memory fields must be updated or deleted?
- Are citations pointing back to a canonical source and version, or only to the nearest retrieved fragment?
- Is the proposed design preserving operational relationships and source hierarchy, or flattening everything into interchangeable chunks?

## Reading Rule

Use this page to classify the knowledge state first. Then move to [11.1.2 Decision Boundaries And Retrieval Heuristics](11-01-02-decision-boundaries-and-retrieval-heuristics.md) to choose the default retrieval lane. If the design still cannot say what should be live, what may persist, and what should never be stored, the implementation is not ready for tooling choices yet.

Back to [11.1 Retrieval Foundations](11-01-00-retrieval-foundations.md).
