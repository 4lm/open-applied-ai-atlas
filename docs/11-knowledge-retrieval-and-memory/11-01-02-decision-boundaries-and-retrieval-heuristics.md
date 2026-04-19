# 11.1.2 Decision Boundaries And Retrieval Heuristics

_Page Type: Decision Guide | Maturity: Draft_

Use this page when a team knows knowledge quality matters but has not yet proved what should be retrieved live, remembered across sessions, or kept out of persistent state altogether. The goal is to name the dominant retrieval lane before convenience, vendor defaults, or model-tuning pressure turn a knowledge-boundary problem into an architecture mistake.

## Decision Lanes

| Lane | Use it when the main question is... | Default posture |
| --- | --- | --- |
| Live-retrieval lane | whether answers must reflect current source-of-truth material rather than remembered prior output | retrieve at request time from owned sources, keep long-lived state minimal, and make freshness visible |
| Bounded-memory lane | whether continuity depends on carrying a small set of user or workflow state across sessions | persist only typed, approved memory fields with expiry, deletion, and revalidation rules |
| Relationship-aware lane | whether the answer depends on entities, source hierarchy, metadata filters, or graph edges rather than loose semantic similarity alone | combine semantic retrieval with structured filters, canonical IDs, or relationship traversal |
| Permission-sensitive lane | whether access rights, revocation, or mixed-sensitivity corpora dominate the risk posture | enforce permissions and revocation in ingestion and retrieval, with conservative fallbacks when access state is uncertain |

## Practical Heuristics

- Default to the least persistent state that can still satisfy the user need.
- Do not use memory as a cache for operational facts, policy text, entitlements, or other content that already has a governed source of truth.
- Treat provenance as product behavior: if the system cannot explain source, owner, version, or freshness, retrieval quality is not good enough yet.
- When relationships, permissions, or canonical IDs matter, assume plain chunk search is incomplete until structured signals or graph paths are designed explicitly.
- Enforce permissions before and during retrieval, not only in the user interface after candidate content has already been surfaced.
- Revisit the lane when teams start proposing fine-tuning or broader automation to fix stale, uncited, or access-unsafe answers; those are often unresolved retrieval-boundary failures first.

## Escalate When

- the team cannot name which state should be live, which state may persist, and which state should never be stored
- indexed sources do not have named owners, refresh expectations, or canonical-copy rules
- deletion, revocation, or subject-access requests would require manual guesswork across embeddings, caches, and memory fields
- permission-sensitive content is being flattened into one corpus without a retrieval-time access model
- the proposed design needs citations, auditability, or evidence review, but provenance is still treated as an optional UX flourish
- a memory schema keeps expanding because retrieval relevance is weak or source governance is poor

## Retrieval Anti-Patterns

- choosing memory because repeated retrieval feels expensive before checking whether the fact should persist at all
- treating every knowledge problem as vector search even when ownership, relationships, or filters carry most of the answer
- using retrieval to compensate for unmanaged source duplication, stale content, or unclear source authority
- checking permissions only after retrieval candidates or summaries have already been assembled
- escalating into adaptation work before proving that retrieval coverage, freshness, provenance, and permission handling are already sound

## Chapter Handoffs

- [6. Data Sovereignty And Privacy](../06-data-sovereignty-and-privacy/06-00-00-data-sovereignty-and-privacy.md) when retention, deletion, residency, or lawful-access posture becomes the main question.
- [10. Agentic Systems And Orchestration](../10-agentic-systems-and-orchestration/10-00-00-agentic-systems-and-orchestration.md) when retrieval choices are really workflow, tool-use, or delegation-boundary decisions.
- [12. Training Fine-Tuning And Adaptation](../12-training-fine-tuning-and-adaptation/12-00-00-training-fine-tuning-and-adaptation.md) when the team wants to change model behavior because retrieval, provenance, or freshness still looks weak.
- [15. Security And Abuse Resistance](../15-security-and-abuse-resistance/15-00-00-security-and-abuse-resistance.md) when leakage, access abuse, prompt injection through content, or revocation failure dominates the risk.
- [16. Human Oversight And Operating Model](../16-human-oversight-and-operating-model/16-00-00-human-oversight-and-operating-model.md) when reviewers, exception owners, or escalation paths for contested answers are still undefined.

## Practical Reading Rule

Choose the lane that minimizes persistent state first, then justify every extra memory field, index path, and access exception with a named owner and evidence plan. If the design starts solving convenience before provenance, permissions, or freshness, return to the top of the chapter and narrow the problem again.

Back to [11.1 Retrieval Foundations](11-01-00-retrieval-foundations.md).
