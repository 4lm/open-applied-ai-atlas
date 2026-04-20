# Ralph Controller

`./scripts/ralph-codex.py` is the repository's human-run outer controller for long-running Codex work. It launches `codex --search app-server` when research is required, stores structured session state under `.codex/ralph-codex/`, starts in real Codex Plan Mode to build a program board plus a quality-first current tranche, runs an operator review loop before unattended execution begins, and resumes prior work only through explicit session commands.

This file is the canonical operator reference for Ralph. Other root docs should link here instead of duplicating its CLI surface or runtime defaults.

## CLI Surface

The public CLI is intentionally small:

1. `./scripts/ralph-codex.py`
   Prints help.
2. `./scripts/ralph-codex.py --message "Refactor the controller deeply"`
   Starts a new session from inline message text.
3. `./scripts/ralph-codex.py --file /tmp/task.md`
   Starts a new session from a message file.
4. `./scripts/ralph-codex.py --message "Refactor the controller deeply" --profile profiles/restricted.json`
   Starts a new session with the default restricted profile selected explicitly.
5. `./scripts/ralph-codex.py --message "Refactor the controller deeply" --profile profiles/dangerously-unrestricted.json`
   Starts a new session with full-access sandboxing.
6. `./scripts/ralph-codex.py --message "Refactor the controller deeply" --verbose`
   Starts a new verbose session with colored human-readable live status and event logging, plus compact structured terminal diagnostics and full wire diagnostics in `events.jsonl`.
7. `./scripts/ralph-codex.py --sessions 10`
   Lists the latest ten run-history rows.
8. `./scripts/ralph-codex.py --resume`
   Resumes the latest resumable session.
9. `./scripts/ralph-codex.py --resume 3`
   Resumes a specific resumable session by run-history index. A session id works too.

## Artifacts And State

- Shipped Ralph profiles live under `profiles/`, including `profiles/restricted.json` and `profiles/dangerously-unrestricted.json`.
- Canonical schemas for Ralph artifacts live under `schemas/ralph-codex/`.
- The default profile comes from `profiles/restricted.json`; omitting `--profile` loads that file directly.
- Profiles now carry per-phase model selection in `planning.model`, `evaluation.model`, and `execution.model`, plus `milestone_policy`, `worker_policy`, `evidence_policy`, `eval_policy`, and `loop_policy` blocks. `worker_policy.turn_timeout_secs` controls how long bounded auxiliary workers may run before they are disabled for the remainder of the session.
- Each persisted JSON or JSONL artifact gets an adjacent copied schema file.
- Planning drafts are persisted in both `charter.json` (latest snapshot) and `charter-history.jsonl` (versioned draft history), but the planning surface is now `program_board + active_milestone + current_tranche`.
- Planning outputs now include required `research`, `program_board`, `active_milestone`, and quality-first `current_tranche` blocks, and `research` now carries explicit `evidence_assessment` plus `live_search_assessment` instead of relying on a blind source-age cap or a fixed observed-search target.
- Execution outputs now include required `verification`, `touched_files`, `created_files`, `off_tranche_justifications`, `quality_claims`, `milestone_progress`, `acceptance_artifacts`, and `evidence_updates` fields, and `verification` now carries its own `evidence_assessment` plus `live_search_assessment`.
- Ralph also runs a structured evaluation phase after each execution turn and records an `evaluation-result` event.
- Session state now persists program memory, research memory, execution memory, skill memory, evidence registry entries, checkpoint summaries, and worker manifests for long-running resumability.
- Each run also writes a plain UTF-8 terminal transcript under `sessions/<session-id>/logs/<run-id>.log`, and that transcript is flushed continuously while the run is live.

## Operational Defaults

- Ralph does not use turn inactivity timeouts. A live turn is allowed to stay silent while Codex reasons.
- Ralph always emits human-readable live status to `stdout` and event/error logging to `stderr` so an operator can follow along in the shell.
- Ralph mirrors only the user-facing terminal `stdin`, `stdout`, and `stderr` streams into the current run log under `sessions/<session-id>/logs/<run-id>.log`; raw app-server transport stays out of that file.
- Ralph streams user-facing model text progressively to the terminal transcript during structured turns instead of buffering the full turn message in controller memory, and it still avoids dumping raw schema JSON to the operator console.
- Ralph planning runs in actual Plan Mode and explicitly forbids `update_plan`; plan revisions happen through repeated planning turns with controller feedback.
- Ralph treats live web research as dynamic quality posture, not a universal hard requirement. Planning and execution must use live web research when the task depends on unstable or external facts, and otherwise justify why zero live search was sufficient.
- Ralph raises planning and execution reasoning to `xhigh` by default.
- The shipped `restricted` profile is now tuned for long-running quality-first work after the initial plan approval, with stricter completion rules, escalation thresholds instead of repair-loop stop caps, and less frequent progress interruptions.
- The shipped `dangerously-unrestricted` profile keeps the same quality-first loop shape and mostly differs by sandbox access mode.
- Ralph also runs an evaluator phase with its own model/instructions and uses that result to choose between `accept`, `repair_same_tranche`, and `replan`.
- Ralph enables the native search tool through `codex --search app-server` when `research_policy.mode` is `required`.
- Ralph uses a three-layer contract: a broad `program_board` for overall scope, one `active_milestone` for the current milestone, and a quality-first `current_tranche` for the next execution turn.
- Ralph execution prompts send the tranche plus compact memory blocks, evidence registry slices, and milestone context rather than replaying the entire result history each turn.
- Ralph planning, execution, and evaluation prompts use quality-first prompt shaping: Ralph preserves the highest-signal context it can fit, drops lower-value or stale context first, and keeps searching for the best viable prompt before declaring prompt construction infeasible.
- Ralph prefers same-tranche repair before broad replanning when the current tranche is still sound.
- Ralph uses self-repair for malformed or unusable planning, execution, and evaluation outputs before failing a run, and the remaining loop policy values are escalation thresholds, not hard stop counters.
- Ralph rejects execution turns that spread repeated stock headings broadly or create controller-serving meta artifacts such as ledgers or scoreboards unless the task explicitly asks for them.
- Ralph runs a post-iteration audit using an iteration-scoped repo baseline, model-reported touched files, milestone acceptance progress, repeated-heading heuristics, novelty plus milestone-completion scoring, and representative diff samples.
- Ralph records compact non-command tool activity relevant to research in `events.jsonl`.
- Ralph checks observed live research activity against claimed planning research and execution verification before accepting those blocks as complete, but it does not use a fixed observed-search target. It validates sufficiency from `live_search_assessment`, the observed live activity, and the returned sources/findings together, and it only tolerates `observed_live_search_count=0` when the block explicitly declares a narrow light-search telemetry gap and still returns coherent external grounding.
- Ralph uses milestone checkpoints and long-run memory state to keep super-long runs bounded and resumable.
- Ralph now keeps execution memory, skill memory, checkpoint summaries, evidence registry entries, and worker manifests without profile-level retention caps; prompt shaping, not profile memory caps, controls prompt size.
- Ralph’s evidence contract is quality-first: relevance and quality are primary, freshness is assessed explicitly, and `evidence_policy` controls whether those assessments are required and whether evidence must be refreshed on replan.
- Ralph supports auxiliary worker fan-out for `research`, `read_only_repo`, and `evaluator_vote` roles only; shipped profiles do not advertise write-capable worker execution, and the main controller remains authoritative over planning, acceptance, and synthesis.
- Auxiliary worker output is validated through `schemas/ralph-codex/worker-summary-output-v0.1.0.schema.json`, auxiliary worker timeouts come from `worker_policy.turn_timeout_secs`, and repeated worker-role failures trip an in-memory circuit breaker for the rest of the run instead of breaking the controller.
- When the initial planning charter requires operator review, Ralph prints that review block in full without console truncation in both normal and verbose mode, then offers an approve/change/abort loop instead of a one-shot `Y/n`.
- Operator-requested plan changes are fed back into another planning turn on the same thread until the operator approves the charter.
- If the planner needs material operator intent during planning, Ralph supports `request_user_input` and auto-selects the recommended option when answering those prompts.
- Ralph still forces a progress checkpoint after milestone closure or stagnating remaining-gap reports, but shipped long-run profiles can switch post-seed checkpoints into record-only mode so unattended runs continue after the initial plan approval.
- Ralph uses colored terminal layout automatically on interactive TTYs and falls back to plain text when output is redirected.
- Pressing `Ctrl+C` aborts the current run gracefully, clears the active controller run pointer, closes the app-server, and leaves the session resumable.
- After an abort, Ralph prints a one-line resume hint such as `./scripts/ralph-codex.py --resume <session-id>`.
- Ralph keeps `approvalPolicy` set to `never` in every access mode, so it does not ask for permissions during unattended execution after the initial plan approval.
- Ralph defaults to `thread_policy.access_mode: "restricted"`, which uses the `workspace-write` sandbox.
- `thread_policy.access_mode: "dangerously-unrestricted"` is an opt-in profile mode that uses `danger-full-access`.
- Search enablement is independent of sandbox access mode. The default restricted mode still uses live web search.
- `max_iterations` uses `0` to mean unlimited and remains the only profile-visible hard whole-run fuse.
- `quality_policy.progress_checkpoint_mode` controls whether post-seed progress checkpoints require confirmation or are just recorded before automatic continuation.
- `quality_policy.stagnation_escalation_after_iterations` controls when repeated identical remaining-gap reports trigger a checkpoint-style escalation instead of silent continued looping.
- `loop_policy.same_tranche_escalation_after`, `replan_escalation_after`, `planning_repair_escalation_after`, `execution_repair_escalation_after`, and `evaluation_repair_escalation_after` are escalation thresholds, not stop counters.
- Ralph re-grounds from the original task on the first repair cycle, not via a profile knob.
- `eval_policy.acceptance_confidence_floor` gates acceptance quality only; it does not automatically force replanning.
- `research_policy`, `tranche_policy`, `quality_policy`, `milestone_policy`, `worker_policy`, `evidence_policy`, `eval_policy`, and `loop_policy` define the dynamic research contract, quality-first tranche shaping, milestone acceptance checks, selective worker fan-out rules, evidence-assessment requirements, acceptance confidence gating, and escalation behavior.
- Ralph uses semantic live badges such as `STARTING`, `PLANNING`, `WORKING`, `REVIEW`, `RESULT`, `DONE`, and `ABORTED` instead of generic `STATUS` and `WAIT`.
- Command activity from `commandExecution` items is rendered as one compact completed-command `TOOL` line rather than separate in-progress and completed lines.
- `events.jsonl` records semantic event changes and skips ghost duplicates where only the timestamp changed.
- Plan-review output includes a compact exec-log context reconstructed from semantic `commandExecution` notifications in `events.jsonl` for the reviewed planning turn.
- `events.jsonl` stays compact in normal mode and omits verbose wire bodies such as command `output`; `--verbose` enables those full diagnostics for the current run only while keeping them out of the operator console. The plain-text run log is the continuously flushed terminal transcript artifact; `events.jsonl` remains the structured debugging artifact.
## Verification

- When changing `scripts/ralph-codex.py`, `RALPH_CONTROLLER.md`, its schemas, or the related Ralph contract tests, run `python3 -m py_compile scripts/ralph-codex.py tests/test_ralph_codex.py tests/test_repo_contracts.py`.
- Then run `python3 -m unittest tests.test_repo_contracts tests.test_ralph_codex`.
