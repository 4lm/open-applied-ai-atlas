# 11.3.2 Retrieval Readiness Checklist

_Page Type: Operational Artifact | Maturity: Review-Ready_

Use this checklist before calling a retrieval or memory layer production-ready. A retrieval demo is not enough if permissions, freshness, provenance, and deletion behavior are still unclear.

## Readiness Checks

| Check | What must be true |
| --- | --- |
| Source ownership | Every indexed source has a named owner and refresh expectation |
| Permission fidelity | Retrieval preserves source permissions and revocation behavior |
| Freshness design | The team can explain when content updates, expires, or is re-indexed |
| Provenance | Returned content can be traced back to a source and version state |
| Retention | Stored prompts, embeddings, and memory state have explicit retention logic |
| Deletion and revocation | The system can remove or invalidate content when policy or source state changes |
| Evaluation coverage | Relevance, permission leakage, and citation quality are tested separately |
| Incident response | The team can disable, re-index, or quarantine the knowledge layer quickly |

## Minimum Artifact Set

- source inventory with owners and data classes
- indexing and refresh policy
- permission model description
- relevance and leakage eval pack
- rollback or re-index playbook

## Release Gate Prompt

Do not release the knowledge layer until the team can answer all of these:

- What should be retrieved live instead of persisted?
- Which users should see different results from the same corpus?
- How will stale or revoked content be detected and corrected?
- What evidence would prove that the system is citing the wrong source or leaking a protected one?

Back to [11.3 Reference Points](11-03-00-reference-points.md).
