# 3.2.1 Worked Stack Scenarios

_Page Type: Worked Example | Maturity: Draft_

These scenarios show how the stack map changes what a team reviews first, even when the visible application problem looks familiar.

## Internal Knowledge Assistant

| Field | Decision |
| --- | --- |
| Context | A team wants an internal retrieval-backed assistant for knowledge work across several business units |
| Recommended stack reading | Start with governance, data boundary, retrieval, gateway, evaluation, and observability before debating model swaps |
| Key control points | source permissions, gateway budget controls, response tracing, release eval pack, fallback workflow |
| Why | The main design risk is not model capability alone; it is whether shared knowledge access and evidence controls are coherent |
| Watch for | Treating the vector store or model provider as the whole architecture |
| Adjacent chapters | `06`, `09`, `11`, `13`, `19` |

## Regulated Workflow Automation

| Field | Decision |
| --- | --- |
| Context | A regulated enterprise wants an action-capable workflow for case preparation and escalation support |
| Recommended stack reading | Map approval ownership, workflow boundaries, model/runtime posture, logging, rollback, and human handoff before enabling actions |
| Key control points | approval lane, tool invocation rules, durable execution path, incident evidence, re-review trigger |
| Why | The decisive problem is alignment between governance, workflow control, and runtime behavior |
| Watch for | Building tool access before clarifying who approves action, who reviews incidents, and how rollbacks work |
| Adjacent chapters | `04`, `10`, `13`, `16`, `19` |

## Sovereign Private Deployment

| Field | Decision |
| --- | --- |
| Context | A public-sector or defense-style program wants strong locality, operator control, and exit posture |
| Recommended stack reading | Review data boundary, self-hosted runtime, policy enforcement, telemetry export, and support model as one control chain |
| Key control points | support access, model artifact provenance, local retrieval, update path, observability ownership |
| Why | Self-hosting changes multiple layers at once; it is not only a hosting decision |
| Watch for | Treating region selection or on-prem inference as proof that sovereignty concerns are solved |
| Adjacent chapters | `06`, `08`, `15`, `18`, `19` |

## Portfolio Rationalization

| Field | Decision |
| --- | --- |
| Context | A platform team inherits many AI pilots with duplicated gateways, eval tools, and observability choices |
| Recommended stack reading | Identify which layers should become shared platform services and which should remain application-local |
| Key control points | shared gateway, telemetry standard, approved model lanes, eval template, exception process |
| Why | Rationalization succeeds when the stack map separates real control layers from product politics |
| Watch for | Standardizing the wrong layer first and leaving identity, spend, or evidence fragmented |
| Adjacent chapters | `04`, `09`, `13`, `18`, `19` |

Back to [3.2 Applying The Stack Map](03-02-00-applying-the-stack-map.md).
