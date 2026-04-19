# 20.2.1 Worked Standards Scenarios

_Page Type: Worked Example | Maturity: Draft_

These scenarios show what a usable standards set looks like once the organization has to produce controls, evidence, and review outputs.

## EU-Facing Higher-Consequence Service

| Field | Decision |
| --- | --- |
| Context | A provider or deployer is preparing an EU-facing service with non-trivial rights, safety, or regulatory exposure |
| Dominant question | How should legal obligations and governance structure be combined without pretending one framework settles everything? |
| Recommended standards set | EU AI Act + GDPR + ISO/IEC 42001 + ISO/IEC 23894 |
| Why | The service needs legal interpretation, organization-wide governance structure, and a repeatable risk method |
| Evidence and control outputs | classification record, governance owner, control mapping, risk register, release gate, re-review trigger set |
| Watch for | Using AI Act or ISO language as assurance theater before the control map and evidence pack exist |
| Adjacent chapters | `04`, `06`, `13`, `16` |

## SME Managed-Assistant Rollout

| Field | Decision |
| --- | --- |
| Context | An SME wants a managed internal assistant for drafting and knowledge access without building a full enterprise program on day one |
| Dominant question | What is the lightest standards set that still produces credible governance and review? |
| Recommended standards set | NIST AI RMF + NIST AI RMF Playbook + chapter `04` governance lane |
| Why | The team needs public, accessible guidance that can be translated into proportionate local ownership and review practices |
| Evidence and control outputs | approved-use boundary, named owner, minimal eval pack, logging decision, exception path, supplier review note |
| Watch for | Copying a heavy certification narrative into a low-scale context while leaving real controls undefined |
| Adjacent chapters | `04`, `13`, `18` |

## Security Review For An Agentic Workflow

| Field | Decision |
| --- | --- |
| Context | A team is introducing an agentic workflow with tool access, multi-step execution, and sensitive downstream actions |
| Dominant question | Which standards and practice guides produce a real security and assurance review instead of generic trustworthy-AI language? |
| Recommended standards set | ISO/IEC 23894 or NIST AI RMF + OWASP GenAI + MITRE ATLAS + NIST SSDF |
| Why | The team needs both high-level risk framing and concrete adversarial, secure-development, and operational-control guidance |
| Evidence and control outputs | threat model, tool-permission review, security test plan, release criteria, incident escalation route, drift-monitoring plan |
| Watch for | Treating a public threat knowledge base as if it were a complete control program |
| Adjacent chapters | `10`, `13`, `14`, `15` |

## Portability And Supplier-Switch Review

| Field | Decision |
| --- | --- |
| Context | A platform team wants to reduce dependence on a managed provider and must justify what portability and provenance evidence should exist |
| Dominant question | Which standards and public anchors support a credible control and exit posture rather than a vague portability claim? |
| Recommended standards set | EU Data Act + NIST Privacy Framework or ISO/IEC 27701 + SPDX AI + C2PA |
| Why | The team needs an access-and-portability lens, a privacy/accountability lens, and machine-readable component or provenance visibility |
| Evidence and control outputs | export and retention rules, component inventory, provenance decision, supplier exit checklist, data-boundary review |
| Watch for | Claiming portability because the contract allows it while evidence, formats, and inventory remain proprietary or incomplete |
| Adjacent chapters | `06`, `14`, `18`, `21` |

Back to [20.2 Applying Standards And Frameworks](20-02-00-applying-standards-and-frameworks.md).
