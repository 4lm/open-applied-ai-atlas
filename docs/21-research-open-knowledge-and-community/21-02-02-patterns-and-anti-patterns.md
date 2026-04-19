# 21.2.2 Patterns And Anti-Patterns

_Page Type: Reference Sheet | Maturity: Review-Ready_

Use this page during pilot review, adoption pressure, and chapter handoffs to recognize healthy research-to-practice operating shapes before a paper, benchmark, repository, or public guide quietly becomes policy, platform standard, or sourcing commitment.

## Reusable Research-To-Practice Patterns

| Pattern | What good looks like | Fit signal | Review warning |
| --- | --- | --- | --- |
| Source packet before recommendation | The team keeps one review packet that names the source class, the claim being borrowed, what the source is allowed to influence, what local proof is still missing, and which adjacent chapter owns the next decision | a benchmark, paper, public guide, or community post is already shaping shortlist or roadmap discussion | reviewers can repeat the external claim, but cannot say whether it is orientation material, pilot input, control guidance, or release evidence |
| Benchmark-to-local-task bridge | Public evaluation results are translated into representative internal tasks, consequence-aware metrics, runtime constraints, and a clear shortlist decision rule before anything is standardized | the organization is refreshing model, retrieval, or workflow choices because benchmark movement looks significant | score gains are being treated as a sourcing or release decision without any mapping to local data, latency, cost, or failure tolerance |
| Time-boxed community-project pilot with exit path | Open repositories and reference stacks are piloted with named owners, maintainer checks, support boundaries, rollback criteria, and a clear decision date before they become shared dependencies | a project has strong community momentum and engineering teams want to adopt it quickly | the conversation is mostly about stars, demos, or conference visibility, while upgrade, staffing, and unwind plans remain vague |
| Public guidance translated into a local control packet | External practice resources become local review prompts, tests, approval owners, and exception paths instead of copied policy prose | NIST, OWASP, OECD, nonprofit playbooks, or incident writeups are being used to harden controls | respected public language is already showing up in governance material, but nobody has tied it to a test, release gate, or accountable owner |
| Provenance and license gate before artifact intake | External models, datasets, checkpoints, and demo assets are checked for origin, integrity, license terms, retention implications, and redistribution boundaries before they are mirrored, fine-tuned, or promoted internally | teams want to move quickly from "interesting public artifact" to internal reuse or distribution | the artifact is technically attractive, but provenance, permitted use, or update history still depends on informal assumptions |
| Horizon-scanning watchlist separated from roadmap | Trend monitoring stays in a named watchlist with review cadence, trigger criteria, and no implied delivery commitment until a stronger packet exists | leaders want visibility into fast-moving papers, projects, and standards without turning every signal into immediate execution work | a landscape tracker is quietly acting as a roadmap, even though none of the listed items has an owner, pilot scope, or evaluation plan |

## Research-To-Practice Anti-Patterns

| Anti-pattern | Why it fails | Early signal | Review action |
| --- | --- | --- | --- |
| Leaderboard-to-roadmap shortcut | Public measurement surfaces are narrower than real organizational operating conditions, so benchmark prestige cannot settle shortlist, release, or sourcing decisions on its own | roadmap slides cite benchmark gains, but no internal task mapping or runtime envelope exists | reopen [07. Model Ecosystem](../07-model-ecosystem/07-00-00-model-ecosystem.md), [08. Model Hosting And Inference](../08-model-hosting-and-inference/08-00-00-model-hosting-and-inference.md), and [13. Evaluation Testing And QA](../13-evaluation-testing-and-qa/13-00-00-evaluation-testing-and-qa.md) before the shortlist changes |
| Repository popularity as a support plan | Discoverability and community momentum help orientation, but they do not prove maintainer continuity, supportability, or low lock-in once the dependency becomes operational | teams talk about stars, forks, or tutorials more than release cadence, dependency spread, and replacement cost | freeze standardization and require a pilot packet plus [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md) handoff |
| Policy by public copy-paste | Public guidance sharpens local thinking, but copied language without tests, thresholds, owners, and exceptions creates compliance theater rather than operating control | audit or governance material quotes respected sources directly, yet nobody can show the linked control evidence | send the work back through chapters [04](../04-governance-risk-compliance/04-00-00-governance-risk-compliance.md), [15](../15-security-and-abuse-resistance/15-00-00-security-and-abuse-resistance.md), and [16](../16-human-oversight-and-operating-model/16-00-00-human-oversight-and-operating-model.md) for local control design |
| Open-by-label sourcing decision | Open repositories, open weights, or public documentation improve inspectability, but they do not by themselves guarantee sovereign operation, staffing capacity, or low vendor dependence | "it is open" is doing more argumentative work than ownership, hosting, portability, or support analysis | require the team to show the real support boundary and reopen chapters `06`, `08`, and `18` before approval |
| Artifact intake before provenance review | Technical curiosity outruns trust work, so the organization mirrors or adapts external artifacts without understanding origin, license, integrity, or redistribution limits | the artifact has already entered internal storage, testing, or sharing before the steward and license questions are settled | pause reuse and route the review through chapters `06`, `15`, and `20` before the artifact spreads further |
| Horizon-scanning drift presented as execution | A watchlist or community digest becomes a shadow roadmap, which creates hidden commitments without owners, evidence, or decision gates | leadership asks for "what the community is doing," and delivery teams start treating the list as approved direction | split the tracker from the roadmap and require explicit pilot, evaluation, or standards lanes before any item moves forward |

## Review Prompts

- Which pattern actually fits this moment: a source packet, a benchmark bridge, a bounded pilot, a translated control packet, a provenance gate, or a watchlist-only posture?
- What is the smallest local evidence packet that would justify the next move, and which chapter owns that evidence?
- Which anti-pattern is most likely under schedule pressure: leaderboard shortcut, popularity-as-support, policy copy-paste, open-by-label sourcing, premature artifact intake, or watchlist drift?
- Where are openness, sovereignty, privacy, compliance, portability, and lock-in visible in the current packet instead of being assumed from the public source itself?

## Re-Review Triggers

- a public result starts influencing a supported shortlist, deployment path, or procurement discussion rather than simple orientation
- a community project or reference stack moves from bounded pilot work into shared service ownership or mandatory internal use
- external guidance is cited in release, governance, or audit material without a refreshed local control packet
- an external model, dataset, or other artifact is mirrored, fine-tuned, redistributed, or attached to a longer retention path
- watchlist items begin accumulating implied roadmap weight without named owners, exit criteria, or chapter handoffs

## Practical Reading Rule

Use these patterns after the outside signal is understood but before the organization treats adoption as an implementation detail. If the team cannot show a source packet, a local evidence bridge, a bounded pilot or control translation path, and a real response to the dominant anti-pattern, the research-to-practice handoff is not ready.

Back to [21.2 Applying Open Knowledge](21-02-00-applying-open-knowledge.md).
