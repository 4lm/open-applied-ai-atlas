# 21.2.1 Worked Research-To-Practice Scenarios

_Page Type: Worked Example | Maturity: Draft_

These scenarios show how outside knowledge becomes usable only after the team translates it into pilot scope, local evidence, ownership, and re-review triggers. The goal is not to reward whichever paper, benchmark, repository, or public guide is newest. The goal is to make the research-to-practice handoff inspectable before outside signals turn into production defaults.

## Benchmark-Led Model Shortlist Review

| Field | Decision |
| --- | --- |
| Context | A platform team is refreshing its model shortlist after a new public benchmark and several leaderboard summaries start circulating inside the company |
| External signal | Benchmark papers, leaderboard posts, and model-card summaries suggest a newer open-weight model may outperform the team's current managed default |
| Local question | Should the team treat the benchmark signal as enough to change the shortlist, or only as an input to bounded evaluation work? |
| Research-to-practice move | Use the public benchmark to define a local test packet, then compare task fit, hosting burden, licensing, and failure shape before the shortlist changes |
| Required evidence | benchmark-to-local-task mapping, representative internal evaluation set, runtime and cost note, license and support review, rollback plan, and named owner for refresh decisions |
| Release question | Can the team explain why the public benchmark is relevant to its actual tasks and constraints, or is the shortlist drifting because a leaderboard is easy to repeat? |
| Re-review trigger | Reopen chapters `07`, `08`, `13`, and `18` when shortlist changes imply new hosting posture, release criteria, or supplier dependence |

## Community Project Pilot With Production Pressure

| Field | Decision |
| --- | --- |
| Context | An engineering team wants to pilot an open-source orchestration or retrieval component that has strong community momentum but uneven maintainer capacity |
| External signal | Conference talks, GitHub activity, and community tutorials make the project look mature enough to standardize quickly |
| Local question | Is the project ready for a bounded pilot only, or mature enough to become part of a supported internal stack? |
| Research-to-practice move | Separate discovery value from production value by running a time-boxed pilot with maintainer, release, dependency, and exit checks before platform adoption |
| Required evidence | maintainer and release cadence review, dependency inventory, deployment path, issue-response snapshot, fallback option, and exit criteria for ending the pilot |
| Release question | If the project stalls or changes direction, does the team already know how it would replace, contain, or unwind the dependency? |
| Re-review trigger | Reopen chapters `10`, `11`, `14`, and `18` when the pilot adds agentic execution, persistent retrieval state, new telemetry obligations, or deeper build-vs-buy consequences |

## Public Safety Guidance Into Local Control Design

| Field | Decision |
| --- | --- |
| Context | A governance and security group is using public safety guidance, red-team playbooks, and community threat resources to tighten controls for a high-visibility assistant rollout |
| External signal | Public guidance from NIST, OWASP, MITRE, or similar bodies highlights prompt injection, unsafe tool use, and weak incident response as recurring failure modes |
| Local question | Which parts of that guidance should become mandatory controls now, and which parts remain orientation material until the local risk posture is clearer? |
| Research-to-practice move | Convert the public guidance into a chapter-specific control packet with named owners, test cases, and incident triggers instead of copying the guidance as policy text |
| Required evidence | threat-to-control mapping, test plan, abuse-case log, approval owner, incident escalation path, and one documented control exception process |
| Release question | Has the team translated the external guidance into verifiable checks and accountable ownership, or is it still citing respected sources without local operating proof? |
| Re-review trigger | Reopen chapters `04`, `13`, `15`, `16`, and `20` when consequence level, regulatory exposure, or human-approval design changes materially |

## Open Reference Stack Moving Toward Service Ownership

| Field | Decision |
| --- | --- |
| Context | A domain team wants to assemble an open reference stack from public repositories, tutorials, and example architectures rather than start with a managed end-to-end product |
| External signal | Community reference architectures make the stack look portable and open, but the operational burden is spread across many independently maintained parts |
| Local question | Is the reference stack a learning aid, a prototype baseline, or a credible candidate for production ownership? |
| Research-to-practice move | Treat the reference stack as a decomposition tool first, then prove which components can be owned, upgraded, monitored, and replaced under the team's actual staffing and control model |
| Required evidence | component ownership map, version and upgrade plan, security and provenance review, observability coverage, support boundary note, and integration test evidence |
| Release question | Can the team show who owns each layer once the stack is live, or is "open" being used to hide fragmented support and upgrade burden? |
| Re-review trigger | Reopen chapters `03`, `08`, `09`, `14`, `17`, and `19` when the stack becomes a shared platform, adds managed intermediaries, or starts constraining future sourcing choices |

## Cross-Scenario Review Signals

- outside knowledge becomes decision-grade only after it is translated into local evaluation sets, ownership, control outputs, and explicit rollback or exit conditions
- the dominant failure mode is prestige adoption: respected public artifacts are cited as if they settle fit, supportability, or compliance without local proof
- the highest-leverage re-review triggers are scope expansion, hidden supplier dependence, and steward or maintainer changes that quietly alter operational risk after the initial pilot

Back to [21.2 Applying Open Knowledge](21-02-00-applying-open-knowledge.md).
