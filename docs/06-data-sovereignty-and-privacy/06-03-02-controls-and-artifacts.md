# 6.3.2 Controls And Artifacts

_Page Type: Operational Artifact | Maturity: Review-Ready_

Use this page to make privacy and sovereignty claims inspectable. A boundary posture is not real until the team can show how data enters, persists, is reviewed, and is removed.

## Readiness Checks

| Check | What must be true |
| --- | --- |
| Data-flow coverage | The team can describe prompts, outputs, logs, traces, memory, and support copies end to end |
| Retention logic | Each persistent state has an owner, purpose, and retention rule |
| Access-path clarity | Human support, engineering access, subprocessors, and telemetry routes are documented |
| Export and deletion evidence | The organization can explain how data leaves or is removed, not only that the contract says it can |
| Boundary-change review | New memory, retrieval, observability, or supplier features trigger reassessment |

## Minimum Artifact Set

- data-flow map with storage and transfer points
- retention schedule
- export and deletion evidence or tested procedure
- vendor data posture review
- support-access and subprocessors review
- boundary re-review trigger list

## Owner And Review Guidance

| Artifact | Primary owner | Revisit when... |
| --- | --- | --- |
| Data-flow map | System owner with architecture input | data path, storage, or provider changes |
| Retention schedule | Privacy or data owner | new traces, memory, or offline datasets are introduced |
| Vendor data posture review | Procurement or governance owner | contract, service tier, or supplier changes |
| Support-access review | Security or privacy owner | support model or subprocessor list changes |
| Export and deletion evidence | Service owner | renewal, migration planning, or regulator/customer inquiry |

## Release And Re-Review Prompts

- Which stored state would be hardest to enumerate and delete today?
- Which supplier claim about data handling is not technically demonstrated?
- What new telemetry, memory, or evaluation artifact was added since the last review?
- If the organization had to migrate providers in ninety days, which data states would be hardest to export or recreate?

Back to [6.3 Reference Points](06-03-00-reference-points.md).
