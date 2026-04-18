# 10.2.1 Worked Agentic Scenarios

_Page Type: Worked Example | Maturity: Review-Ready_

These scenarios focus on the operating choice, not the marketing label. In each case the question is whether the extra autonomy creates real value after controls are accounted for.

## Knowledge Assistant With Tools Disabled

| Field | Decision |
| --- | --- |
| Context | Analysts need synthesis and drafting help, but no side effects |
| Recommended pattern | Assistant, not agent |
| Why | The task is interpretive and reviewable without delegated action |
| Rejected alternative | Tool-using agent for “future flexibility” |
| Control implication | Retrieval, citations, and reviewer accountability matter more than execution controls |

## Durable Business Workflow

| Field | Decision |
| --- | --- |
| Context | A service process already has known steps, approvals, and owners |
| Recommended pattern | Workflow engine with bounded model steps |
| Why | The value comes from durable state and clear handoffs, not free-form planning |
| Rejected alternative | Planner-style agent deciding the process at run time |
| Control implication | Explicit retries, audit trails, and exception routing are easier to govern |

## Action-Capable Ticket Agent

| Field | Decision |
| --- | --- |
| Context | A team wants an agent to triage and resolve low-risk tickets |
| Recommended pattern | Bounded agent with approval matrix and rollback |
| Why | Some dynamic action choice creates value, but only inside a tightly defined surface |
| Rejected alternative | Broad tool access with no action classes |
| Control implication | Tool inventory, approval checkpoints, traces, and failure playbooks are mandatory |

## Browser Automation Pilot

| Field | Decision |
| --- | --- |
| Context | The team wants browser-capable execution across external systems |
| Recommended pattern | Pilot only, with sandboxing and narrow task scope |
| Why | Side effects expand quickly and failure investigation becomes harder |
| Rejected alternative | General browser autonomy in production-like environments |
| Control implication | Session isolation, action review, and incident rollback must exist before scale |

Back to [10.2 Operating Agentic Systems](10-02-00-operating-agentic-systems.md).
