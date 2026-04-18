# 18.2.1 Worked Build-Buy-Hybrid Scenarios

_Page Type: Worked Example | Maturity: Review-Ready_

These scenarios show how sourcing answers split by layer. Each case is intentionally hybrid enough to avoid the false comfort of one universal build-or-buy rule.

## Buy Model Access, Build Workflow Logic

| Field | Decision |
| --- | --- |
| Context | A team needs fast model capability but differentiates on domain workflow |
| Recommended sourcing | Buy model access, build workflow and policy logic |
| Why | Commodity model capability is not the strategic layer |
| Watch for | Overbuilding low-value infrastructure around commodity layers |

## Hybrid Retrieval Architecture

| Field | Decision |
| --- | --- |
| Context | The team accepts managed inference but wants tighter control over knowledge, permissions, and exit posture |
| Recommended sourcing | Buy inference, self-host or tightly control retrieval and permission layers |
| Why | Retrieval often carries the organization-specific data and governance burden |
| Watch for | Treating a model contract as if it settled the whole architecture |

## Self-Hosted Sovereign Posture

| Field | Decision |
| --- | --- |
| Context | A regulated organization values local control, auditability, and exit posture over raw speed |
| Recommended sourcing | Self-host or compose portable layers across serving, retrieval, and telemetry |
| Why | The strategic risk sits in dependence and jurisdictional exposure |
| Watch for | Underestimating support, staffing, and lifecycle burden |

## Integrator-Led Bootstrap With Transfer

| Field | Decision |
| --- | --- |
| Context | The organization needs a partner to accelerate delivery but wants long-term internal ownership |
| Recommended sourcing | Hybrid delivery with explicit capability-transfer milestones |
| Why | External speed is useful only if the organization avoids permanent dependency on one integrator |
| Watch for | Letting the partner become the irreplaceable control plane |

Back to [18.2 Applying Sourcing Choices](18-02-00-applying-sourcing-choices.md).
