# 15.3.3 Controls And Artifacts

_Page Type: Operational Artifact | Maturity: Draft_

Use this page when the team needs reviewable security evidence instead of a generic statement that the system is "hardened." A useful security packet makes trust boundaries, abuse controls, release blockers, and incident-containment responsibilities explicit before a model, agent, or workflow reaches production.

## Minimum Security Control Pack

| Control or artifact | What it should make explicit | Typical owner | Review trigger |
| --- | --- | --- | --- |
| Trust-boundary register | User, model, retrieval, tool, third-party, and human-approval boundaries, plus which controls sit at each crossing | Security or architecture owner | New workflow, provider, or tool integration |
| Tool and action permission manifest | Which tools exist, which roles or policies can invoke them, what approvals are required, and which actions are blocked outright | Platform, product, or security owner | New tool, privilege change, or agent workflow update |
| Prompt, content, and data-handling rules | Which prompts, uploads, retrieved passages, and outputs are redacted, filtered, retained, or excluded from providers and logs | Privacy or security owner | New data source, logging sink, or provider route |
| Abuse-test and red-team pack | High-risk prompts, tool-abuse attempts, privilege escalation paths, exfiltration attempts, and expected safe outcomes | Security plus QA owner | Release candidate, major prompt change, or policy update |
| Model and dependency provenance record | Model source, signed artifacts, dependency versions, scanner results, and approval status for production use | Platform or supply-chain owner | Model swap, fine-tune refresh, or dependency upgrade |
| Secrets and credential exposure plan | Where credentials live, how they rotate, how access is scoped, and how prompt or tool paths prevent leakage | Platform or security owner | New secret, new runtime, or vendor change |
| Incident containment and recovery playbook | Kill switches, account disabling path, provider escalation contacts, evidence preservation steps, and rollback method | Service owner or incident commander | Sev incident, tabletop exercise, or architecture change |
| Egress, residency, and exception register | Which providers or destinations receive data, which regions apply, and what sovereign or contractual exceptions were approved | Privacy, procurement, or compliance owner | New region, new vendor, or contract renewal |

## Release-Blocking Review Packet

Before launch, reviewers should be able to inspect the following in one place:

- the current trust-boundary diagram or register, with named owners for each crossing
- the tool permission manifest showing allowed actions, blocked actions, and approval requirements
- the latest abuse-test results, including unresolved failures and explicit acceptance decisions
- evidence that model artifacts and critical dependencies were scanned, signed where required, and approved for use
- the data-handling record for prompts, uploads, retrieval content, and logs across every external provider or sink
- the incident containment playbook with live contacts, shutdown conditions, and recovery path
- the exception register for any unmanaged egress, vendor dependence, or residual high-risk behavior

## Containment Drill

Run at least one realistic drill before broad rollout.

| Drill question | Evidence reviewers should expect |
| --- | --- |
| Can the team disable a dangerous tool or agent path without redeploying the whole stack? | Kill-switch owner, action path, and tested rollback record |
| Can the team prove whether a harmful output came from the model, retrieval layer, tool invocation, or missing approval step? | Linked trace or audit path, change record, and decision log |
| Can the team show which data could have left the environment during an abuse attempt? | Egress register, provider path, and retention or deletion note |
| Can the team identify whether an attack used prompt injection, privilege drift, weak policy logic, or dependency compromise? | Threat mapping, abuse-test case, and incident classification rule |
| Can the team contain a compromised credential, model artifact, or external integration quickly enough for the service tier? | Rotation procedure, quarantine or rollback step, and accountable owner |

## Failure Signs

- A team can describe its guardrails, but cannot show which artifact records tool permissions, blocked actions, or approval thresholds.
- Security testing exists as an occasional red-team event rather than a reusable release gate with named owners and unresolved-failure handling.
- Model, adapter, or dependency changes can reach production without an integrity or provenance review step.
- Provider egress or logging exceptions exist, but no one can point to the document that approved them or states their expiry.
- Incident response depends on ad hoc chat messages because the containment playbook does not identify kill switches, contacts, or evidence-preservation steps.

## Approval Prompt

If the team cannot show which artifact would let a reviewer verify trust boundaries, inspect tool permissions, confirm abuse-test status, and contain a compromised runtime or provider path, the security design is not yet ready.

Back to [15.3 Reference Points](15-03-00-reference-points.md).
