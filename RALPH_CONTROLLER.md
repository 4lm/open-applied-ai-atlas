# Ralph Controller

`./scripts/ralph-codex.py` is the repository's human-run outer controller for long-running Codex work. It launches `codex --search app-server` when research is required, stores structured session state under `.codex/ralph-codex/`, starts in real Codex Plan Mode to build a program board plus a bounded current tranche, runs an operator review loop before unattended execution begins, and resumes prior work only through explicit session commands.

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
- Profiles now carry per-phase model selection in `planning.model`, `evaluation.model`, and `execution.model`, plus `memory_policy`, `milestone_policy`, `worker_policy`, `evidence_policy`, `eval_policy`, and `loop_policy` blocks.
- Each persisted JSON or JSONL artifact gets an adjacent copied schema file.
- Planning drafts are persisted in both `charter.json` (latest snapshot) and `charter-history.jsonl` (versioned draft history), but the planning surface is now `program_board + active_milestone + current_tranche`.
- Planning outputs now include required `research`, `program_board`, `active_milestone`, and bounded `current_tranche` blocks.
- Execution outputs now include required `verification`, `touched_files`, `created_files`, `off_tranche_justifications`, `quality_claims`, `milestone_progress`, `acceptance_artifacts`, and `evidence_updates` fields.
- Ralph also runs a structured evaluation phase after each execution turn and records an `evaluation-result` event.
- Session state now persists program memory, research memory, execution memory, skill memory, evidence registry entries, checkpoint summaries, and worker manifests for long-running resumability.
- Each run also writes a plain UTF-8 terminal transcript under `sessions/<session-id>/logs/<run-id>.log`.

## Operational Defaults

- Ralph does not use turn inactivity timeouts. A live turn is allowed to stay silent while Codex reasons.
- Ralph always emits human-readable live status to `stdout` and event/error logging to `stderr` so an operator can follow along in the shell.
- Ralph mirrors only the user-facing terminal `stdin`, `stdout`, and `stderr` streams into the current run log under `sessions/<session-id>/logs/<run-id>.log`; raw app-server transport stays out of that file.
- Ralph formats live model output for humans instead of streaming raw schema JSON to the terminal during structured turns.
- Ralph planning runs in actual Plan Mode and explicitly forbids `update_plan`; plan revisions happen through repeated planning turns with controller feedback.
- Ralph treats live web research as mandatory. Planning and replanning must perform multi-step web search and record sources explicitly.
- Ralph raises planning and execution reasoning to `xhigh` by default.
- Ralph also runs an evaluator phase with its own model/instructions and uses that result to choose between `accept`, `repair_same_tranche`, and `replan`.
- Ralph enables the native search tool through `codex --search app-server` when `research_policy.mode` is `required`.
- Ralph uses a three-layer contract: a broad `program_board` for overall scope, one `active_milestone` for the current milestone, and a bounded `current_tranche` for the next execution turn.
- Ralph execution prompts send the tranche plus compact memory blocks, evidence registry slices, and milestone context rather than replaying the entire result history each turn.
- Ralph prefers same-tranche repair before broad replanning when the current tranche is still sound.
- Ralph rejects execution turns that exceed the tranche budget, spread repeated stock headings broadly, or create controller-serving meta artifacts such as ledgers or scoreboards unless the task explicitly asks for them.
- Ralph runs a post-iteration audit using an iteration-scoped repo baseline, model-reported touched files, milestone acceptance progress, repeated-heading heuristics, novelty plus milestone-completion scoring, and representative diff samples.
- Ralph records compact non-command tool activity relevant to research in `events.jsonl`.
- Ralph checks observed search activity against claimed planning research and execution verification before accepting those blocks as complete.
- Ralph uses milestone checkpoints and long-run memory state to keep super-long runs bounded and resumable.
- Ralph carries selective worker fan-out policy in profiles, but the main controller remains authoritative over planning, acceptance, and synthesis.
- When the initial planning charter requires operator review, Ralph prints that review block in full without console truncation in both normal and verbose mode, then offers an approve/change/abort loop instead of a one-shot `Y/n`.
- Operator-requested plan changes are fed back into another planning turn on the same thread until the operator approves the charter.
- If the planner needs material operator intent during planning, Ralph supports `request_user_input` and auto-selects the recommended option when answering those prompts.
- Ralph forces a progress checkpoint after repeated iterations, high file churn, or stagnating remaining-gap reports; the operator must continue or abort explicitly.
- Ralph uses colored terminal layout automatically on interactive TTYs and falls back to plain text when output is redirected.
- Pressing `Ctrl+C` aborts the current run gracefully, clears the active controller run pointer, closes the app-server, and leaves the session resumable.
- After an abort, Ralph prints a one-line resume hint such as `./scripts/ralph-codex.py --resume <session-id>`.
- Ralph keeps `approvalPolicy` set to `never` in every access mode, so it does not ask for permissions during unattended execution after the initial plan approval.
- Ralph defaults to `thread_policy.access_mode: "restricted"`, which uses the `workspace-write` sandbox.
- `thread_policy.access_mode: "dangerously-unrestricted"` is an opt-in profile mode that uses `danger-full-access`.
- Search enablement is independent of sandbox access mode. The default restricted mode still uses live web search.
- `max_iterations` uses `0` to mean unlimited. Non-zero values bound replanning loops, not wall-clock runtime.
- `execution.max_prompt_chars` is profile-controlled; the shipped profiles now use non-zero planning and execution prompt budgets.
- `research_policy`, `tranche_policy`, `quality_policy`, `memory_policy`, `milestone_policy`, `worker_policy`, `evidence_policy`, `eval_policy`, and `loop_policy` define the mandatory research contract, per-iteration tranche budget, long-run memory behavior, milestone acceptance checks, selective worker fan-out rules, evidence freshness, and prompt-compaction thresholds.
- Ralph uses semantic live badges such as `STARTING`, `PLANNING`, `WORKING`, `REVIEW`, `RESULT`, `DONE`, and `ABORTED` instead of generic `STATUS` and `WAIT`.
- Command activity from `commandExecution` items is rendered as one compact completed-command `TOOL` line rather than separate in-progress and completed lines.
- `events.jsonl` records semantic event changes and skips ghost duplicates where only the timestamp changed.
- Plan-review output includes a compact exec-log context reconstructed from semantic `commandExecution` notifications in `events.jsonl` for the reviewed planning turn.
- `events.jsonl` stays compact in normal mode and omits verbose wire bodies such as command `output`; `--verbose` enables those full diagnostics for the current run only while keeping them out of the operator console. The plain-text run log is the terminal transcript artifact; `events.jsonl` remains the structured debugging artifact.
## Verification

- When changing `scripts/ralph-codex.py`, `RALPH_CONTROLLER.md`, its schemas, or the related Ralph contract tests, run `python3 -m py_compile scripts/ralph-codex.py tests/test_ralph_codex.py tests/test_repo_contracts.py`.
- Then run `python3 -m unittest tests.test_repo_contracts tests.test_ralph_codex`.
