# 8.2.2 Patterns And Anti-Patterns

_Page Type: Reference Sheet | Maturity: Draft_

Use this page during rollout, capacity review, and renewal planning to recognize healthy hosting operating shapes before labels such as "private," "dedicated," or "self-hosted" hide support access, upgrade dependence, untested fallback, or hardware lock-in.

## Reusable Hosting Operating Patterns

| Pattern | What good looks like | Fit signal | Review warning |
| --- | --- | --- | --- |
| Runtime ownership ledger before scale-up | Every deployment records runtime posture, model package, version owner, support-access path, patch window, telemetry location, and rollback owner so "who operates this" is answerable before production pressure arrives | a prototype is about to widen into business use or shared platform status | the team can name the model and region, but not who owns runtime changes, privileged access, or incident reconstruction |
| Capacity-tested rollout with explicit degraded mode | Throughput assumptions, queue behavior, timeout rules, cache behavior, and human or workflow fallback are tested under realistic load and tied to a release gate | latency, throughput, or availability promises are becoming contractual, customer-facing, or operationally critical | launch plans mention autoscaling or GPUs, but not admission control, degraded service behavior, or rollback proof |
| Managed isolation with exported evidence | Dedicated or cloud-estate hosting stays acceptable only when support access, version-change notice, logs, traces, and incident evidence can leave the managed platform and be reviewed elsewhere | the team needs better isolation or networking than a public API but does not want full serving operations | the proposal leans on private networking or tenant isolation while provider-side admin paths and evidence export remain vague |
| Self-hosted runtime with named operator burden | Serving software, image provenance, model packaging, accelerator dependence, patch cadence, on-call rotation, and restore drills are all assigned to named operators rather than implied by the phrase "self-hosted" | privacy, exit posture, packaging control, or predictable unit economics justify owning the serving stack directly | self-hosting is approved as a control win even though nobody owns GPU fleet operations, runtime hardening, or rollback |
| Offline or sovereign lifecycle discipline | Air-gapped or sovereign estates have a bounded model-ingest path, local telemetry and retention rules, validated update media, restore tests, and a support process that does not quietly depend on live vendor access | legal, security, or operational constraints require disconnected or tightly bounded runtime control | the estate is described as offline or sovereign, but updates, diagnostics, or emergency support still assume hidden external connectivity |

## Hosting Anti-Patterns

| Anti-pattern | Why it fails | Early signal | Review action |
| --- | --- | --- | --- |
| Region pinning presented as full control | Preferred geography can hide the fact that upgrades, support tooling, telemetry, and incident evidence still depend on the provider estate | reviewers hear "EU region" or "private VPC" more often than named admin, export, and rollback controls | reopen chapter `06`, chapter `14`, and chapter `18` before approving control-first claims |
| Self-hosting as branding, not an operating model | Running the stack internally creates new burden; if that burden is not staffed, the result is brittle infrastructure with worse evidence than the managed option | architecture diagrams show internal clusters, but patch cadence, capacity ownership, and on-call rotation are missing | block expansion until operator ownership, hardening work, and restore drills are explicit with chapter `15` handoff |
| Elasticity assumed instead of tested | Inference load, concurrency spikes, and model-size changes expose queue collapse or runaway spend when degraded behavior was never designed | plans cite autoscaling, but no one can show admission limits, timeout policy, or failure behavior under stress | require load evidence and fallback drills before widening production scope |
| Offline or sovereign labels with hidden remote dependencies | An estate cannot honestly be treated as disconnected or sovereign if updates, keys, admin channels, or diagnostics still rely on outside services | support runbooks reference vendor consoles, remote shells, or real-time external package pulls | reopen chapter `06`, chapter `19`, and chapter `20` and require a bounded lifecycle packet |
| Hardware and optimization lock-in discovered late | The model may be portable on paper while kernels, drivers, quantization formats, or accelerator contracts become the real exit barrier | migration conversations focus on weights and containers, but not accelerator family, serving runtime, or performance baseline | pull chapter `12` and chapter `18` back in before another rollout or procurement commitment |

## Review Prompts

- Which operating pattern best matches the current stage: explicit runtime ownership, capacity-tested rollout, managed isolation with exported evidence, self-hosted operator ownership, or offline lifecycle discipline?
- What evidence proves the chosen runtime can survive an outage, provider change, support event, or scaling surprise without discovering missing controls during the incident?
- Which anti-pattern is most likely after rollout pressure arrives: control theater through region labels, unstaffed self-hosting, untested elasticity, hidden remote dependence, or hardware lock-in?
- Which adjacent chapter must re-enter before approval: `06`, `12`, `14`, `15`, `18`, `19`, or `20`?

## Re-Review Triggers

- the workload widens from bounded experimentation into revenue, regulated, or safety-relevant use
- a new model family, quantization path, accelerator class, or serving runtime changes capacity or exit assumptions
- provider support access, private networking claims, or evidence export behavior changes enough that the original control posture no longer holds
- an offline or sovereign estate adds remote administration, live package pulls, or new telemetry transfer paths
- rollback, restore, or degraded-mode drills are older than the current runtime image, model package, or traffic shape

## Practical Reading Rule

Use these patterns after the runtime lane is broadly chosen but before the organization treats hosting as solved. If the team cannot show runtime ownership, tested degraded behavior, exportable evidence, bounded support access, and a believable exit from the current hardware or provider estate, the hosting operating design is not ready.

Back to [8.2 Operating Hosting And Inference](08-02-00-operating-hosting-and-inference.md).
