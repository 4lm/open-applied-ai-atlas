# 21.1.1 Knowledge Source Classes And Core Distinctions

_Page Type: Concept Explainer | Maturity: Draft_

Use this page to classify what kind of public knowledge is actually in front of the team before a paper, benchmark, open-source repository, public guide, or community narrative starts carrying more authority than it earned. Chapter `21` only works if readers separate source classes, stewardship postures, and evidence claims before they start arguing about adoption.

## Knowledge-Source Map

| Source class | What it is good for | What it cannot settle on its own | What fails when it is misread |
| --- | --- | --- | --- |
| Primary research paper or preprint | Explaining a method, hypothesis, dataset, or experimental result in enough detail to understand what the authors claim they did | production fit, operational burden, sustained support, or release readiness for a specific organization | novelty and reputation get mistaken for implementation proof, so teams skip local evaluation and consequence review |
| Benchmark suite, leaderboard, or public evaluation result | Showing how systems perform on a defined task set under a named measurement method | whether the benchmark tasks match local work, whether the system is reliable in context, or whether the evidence is still current after setup changes | scores become shortlist policy even though the measurement surface is narrower than the real use case |
| Open-source project, model card, or implementation guide | Revealing concrete interfaces, dependencies, deployment assumptions, and reproducible starting points for hands-on learning | long-term supportability, secure operation, staffing capacity, or lifecycle ownership inside the organization | teams confuse inspectable code or docs with owned production posture and inherit unmanaged dependency risk |
| Public practice guidance, playbook, or nonprofit handbook | Turning recurring public lessons into review prompts, control ideas, and implementation questions that can sharpen local design | local approval logic, accountable owners, exception handling, or evidence that a control really works in the team's system | respected language gets copied into policy or audit packets without translation into local tests and owners |
| Community map, tutorial, conference narrative, or curated ecosystem summary | Accelerating discovery by showing what practitioners are noticing, combining, or debating across a fast-moving landscape | factual completeness, neutrality, maintenance quality, or durable authority over architecture and governance decisions | convenience and visibility overpower scrutiny, so stale or promotional material quietly defines the roadmap |
| Public artifact registry or preservation platform | Helping the team trace models, datasets, code, and related materials back to citable records, versions, and stewards | whether the artifact is trustworthy enough to mirror, fine-tune, redistribute, or depend on operationally | discoverability is confused with provenance assurance, licensing clarity, or safe operational reuse |

## Core Distinctions

| Distinction | Why it changes the review |
| --- | --- |
| Orientation signal vs. decision-grade evidence | Most public knowledge should first help the team ask better questions; only a smaller subset should influence shortlist, pilot, control, or release decisions. |
| Method claim vs. local outcome proof | A paper may show that an approach can work somewhere; it does not prove that the same approach will work under the team's data, users, runtime, and control constraints. |
| Measurement surface vs. real operating surface | Benchmarks and leaderboards measure a bounded task design, while organizations operate across latency, cost, abuse, failure recovery, staffing, and compliance conditions that the score often does not capture. |
| Inspectability vs. supportability | Open code, model cards, and public docs improve inspection and reproducibility, but they do not guarantee maintainer continuity, secure upgrades, or internal capacity to own the dependency. |
| Public guidance vs. local control design | External frameworks and playbooks can sharpen a control review, yet the organization still has to map them into named owners, tests, thresholds, and exception handling. |
| Community visibility vs. stewardship quality | A popular project or narrative may be easy to find and easy to repeat while still having weak maintenance, unclear governance, or uneven technical depth. |
| Discoverability vs. provenance trust | Being able to download or cite an artifact is different from being able to verify where it came from, what license governs it, and whether its history is intact enough for reuse. |
| Open posture vs. low lock-in | Public artifacts and open repositories can improve portability, but the operational path may still depend on a narrow maintainer set, one platform, or hidden integration labor. |

## What These Distinctions Change In Practice

- Classify the source before debating the recommendation. Ask whether the team is looking at a method claim, benchmark result, implementation artifact, public guidance resource, community narrative, or preservation record.
- Write down what the source is allowed to influence: orientation only, shortlist refresh, bounded pilot design, control review, or standards tracking. Anything broader needs stronger evidence and usually another chapter.
- Treat leaderboard movement and paper prestige as triggers for local testing, not as reasons to change production defaults on their own.
- Read open-source implementation detail together with maintenance posture, release cadence, dependency spread, and replacement cost.
- Convert public guidance into local review packets with owners, tests, and exception rules instead of copying external wording into policy prose.
- Reopen adjacent chapters as soon as the discussion becomes mainly about evaluation fit, hosting burden, security posture, sourcing dependence, or standards selection rather than source interpretation.

## Reviewer Checks

- Which source class is doing the persuasive work here, and has the team named that class explicitly?
- Is the source being used for orientation, pilot design, shortlist refresh, control updates, or release-significant evidence?
- What part of the claim depends on local context that the public source cannot supply on its own?
- If the source is open or public, what still needs verification around provenance, license, steward continuity, or operator burden?
- Are community visibility and public reputation being mistaken for neutral evidence or durable maintenance quality?
- Which adjacent chapter should own the next decision if the disagreement is now really about evaluation, runtime, security, sourcing, or standards?

## Practical Reading Rule

Classify the source, name what it is allowed to change, and keep the unresolved part of the problem visible. Then move to [21.1.2 Decision Boundaries And Research Heuristics](21-01-02-decision-boundaries-and-research-heuristics.md) for lane selection, or hand the question to the adjacent chapter that owns the real operating decision. If the team cannot tell the difference between method claims, measurement results, implementation artifacts, public guidance, and community narratives, it is not ready to treat outside knowledge as internal policy or platform input.

Back to [21.1 Knowledge Foundations](21-01-00-knowledge-foundations.md).
