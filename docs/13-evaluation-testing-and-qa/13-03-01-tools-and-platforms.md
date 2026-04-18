# 13.3.1 Tools And Platforms

_Page Type: Comparison Page | Maturity: Review-Ready_

This file compares the main tooling used to test, benchmark, and gate AI systems. It spans regression harnesses, RAG and agent evaluators, benchmark suites, and managed evaluation platforms because release evidence is rarely credible if it relies on only one style of test.

## How To Use This File

- Read the tables as comparison surfaces, not as universal rankings.
- Separate regression tooling, public benchmarking, and production-linked evaluation platforms.
- Re-check `10`, `11`, `14`, and `15` before assuming a high eval score means the whole system is ready to ship.

## Evaluation Harnesses And Regression Tooling

These tools matter when teams need repeatable, CI-friendly evidence around prompts, retrieval systems, and agents.

| Name | Entity type | Stack role | Openness-policy tier | Open source posture | Hosting / control posture | Best-fit use cases | Main constraints / lock-in notes | Primary source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [OpenAI Evals](https://github.com/openai/evals) | Open-source project | Evaluation framework | Preferred | Fully open source | Self-hosted | Model and system eval experimentation | Requires local evaluation design and maintenance | [Repo](https://github.com/openai/evals) |
| [Inspect AI](https://inspect.aisi.org.uk/) | Open-source framework | LLM and agent evaluation framework | Preferred | Open source | Self-hosted | Structured model, tool-use, and agent evaluations with richer task and sandbox support | Requires deliberate eval design and local operating discipline | [Inspect](https://inspect.aisi.org.uk/) |
| [promptfoo](https://www.promptfoo.dev/) | Open-source project | Prompt and LLM testing | Preferred | Open source | Self-hosted or CI-integrated | CI-style evaluation and regression checks | Strongest for test harnesses, not full operating governance | [Docs](https://www.promptfoo.dev/docs/intro) |
| [DeepEval](https://docs.confident-ai.com/) | Framework | LLM evaluation | Acceptable | Open core / commercial ecosystem | Self-managed or managed | RAG and conversational eval workflows | More advanced workflows may depend on commercial layers | [Docs](https://docs.confident-ai.com/) |
| [Ragas](https://docs.ragas.io/) | Open-source project | RAG-focused evaluation | Preferred | Open source | Self-hosted | Retrieval-heavy app evaluation | Narrower than full system QA | [Docs](https://docs.ragas.io/) |
| [TruLens](https://www.trulens.org/) | Open-source project | Feedback and evaluation tooling | Preferred | Open source | Self-hosted | Trace-linked quality and feedback workflows | Requires internal instrumentation discipline | [TruLens](https://www.trulens.org/) |
| [Giskard](https://docs.giskard.ai/en/stable/) | Open-source platform | ML and LLM testing | Preferred | Open source / managed ecosystem | Self-hosted or managed | Broader model testing with both classical ML and LLM coverage | May require more setup than lighter prompt-only harnesses | [Docs](https://docs.giskard.ai/en/stable/) |
| [MLflow Evaluate](https://mlflow.org/docs/latest/llms/evaluate/index.html) | Open-source capability | Evaluation inside model lifecycle workflows | Preferred | Open source | Self-hosted or managed ecosystem | Teams already using MLflow for experiment and release governance | Best fit assumes MLflow-centered lifecycle operations | [Docs](https://mlflow.org/docs/latest/llms/evaluate/index.html) |
| [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) | Open-source project | Academic and standardized benchmark harness | Preferred | Open source | Self-hosted | Standardized model benchmark runs across common tasks | Public benchmark orientation does not replace domain QA | [Repo](https://github.com/EleutherAI/lm-evaluation-harness) |

## Managed Evaluation And Production-Linked Platforms

These platforms matter when teams want collaborative evaluation workflows, trace-linked debugging, or managed evaluation operations.

| Name | Entity type | Stack role | Openness-policy tier | Open source posture | Hosting / control posture | Best-fit use cases | Main constraints / lock-in notes | Primary source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [LangSmith Evaluation](https://docs.smith.langchain.com/evaluation) | Product docs | App and agent evaluation | Controlled Exception | Proprietary service | Managed | LangChain ecosystem evaluation and trace-linked QA | Strong ecosystem coupling | [Docs](https://docs.smith.langchain.com/evaluation) |
| [Arize Phoenix](https://phoenix.arize.com/) | Open-source project | Evaluation plus observability | Preferred | Open source | Self-hosted | Teams pairing tracing with evaluation | Blends observability and QA rather than replacing either | [Phoenix](https://phoenix.arize.com/) |
| [Weights & Biases Weave](https://wandb.ai/site/weave/) | Product / project | Trace-linked evaluation and experimentation | Acceptable | Open source / commercial ecosystem | Self-hosted or managed | Experiment-heavy and agent-heavy evaluation workflows | Rich features can pull teams toward a broader managed W&B estate | [W&B](https://wandb.ai/site/weave/) |
| [Braintrust](https://www.braintrust.dev/docs) | Evaluation platform | Collaborative evals and dataset management | Acceptable | Open source / commercial ecosystem | Self-hosted or managed | Eval-driven product teams needing datasets, scoring, and review workflows | Broader platform dependence grows as more workflow shifts into the product | [Docs](https://www.braintrust.dev/docs) |
| [Patronus AI](https://docs.patronus.ai/docs) | Evaluation and safety platform | Quality and risk evaluation for LLM systems | Controlled Exception | Proprietary platform | Managed | Organizations needing managed eval and policy workflows around LLM apps | Managed control-plane dependence is significant | [Docs](https://docs.patronus.ai/docs) |
| [Galileo](https://docs.galileo.ai/galileo) | Evaluation and observability platform | Offline evals, observability, and guardrail engineering | Controlled Exception | Proprietary platform | SaaS, VPC, or on-prem options | Teams connecting offline evals to live guardrails and failure analysis | Platform breadth increases dependence even when deployment options are flexible | [Docs](https://docs.galileo.ai/galileo) |

## Public Benchmarking And External Reference Programs

These resources matter for external comparison, procurement realism, and public model understanding, but they should not replace organization-specific release tests.

| Name | Entity type | Stack role | Openness-policy tier | Open source posture | Hosting / control posture | Best-fit use cases | Main constraints / lock-in notes | Primary source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [HELM](https://crfm.stanford.edu/helm/latest/) | Public benchmark suite | Standardized model and scenario evaluation | Not applicable | Open benchmark and academic resource | Public benchmark resource | Public benchmarking and comparative model understanding | Public benchmarks rarely replace domain-specific release tests | [HELM](https://crfm.stanford.edu/helm/latest/) |
| [MLCommons AILuminate](https://mlcommons.org/benchmarks/) | Benchmark program | Safety and public-comparison benchmark | Not applicable | Open benchmark ecosystem | Public benchmark resource | External safety reference and procurement context | Good external signal, not a substitute for organization-specific QA | [MLCommons](https://mlcommons.org/benchmarks/) |
| [OpenCompass](https://opencompass.org.cn/home) | Public benchmark platform | Benchmark aggregation and model comparison | Not applicable | Open benchmark ecosystem | Public benchmark resource | External model comparison across broad benchmark sets | Useful for ecosystem scanning, not direct release decisions | [OpenCompass](https://opencompass.org.cn/home) |

## Evidence Notes

- Product and project rows are anchored in official documentation and repository pages linked in the `Primary source` column.
- The portability, ecosystem-coupling, and governance commentary is atlas synthesis. It reflects how these tools behave inside broader release and evidence programs, not only their advertised feature sets.
- Public benchmarks belong in procurement context and external comparison work; they are not substitutes for release-specific evaluation packs.

## Reading Notes

- Re-check the main chapter if the comparison starts to feel more detailed than the underlying decision.
- Prefer adjacent chapter context over treating a single table row as a final answer.

Back to [13.3 Reference Points](13-03-00-reference-points.md).
