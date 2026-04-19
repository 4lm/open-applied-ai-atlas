# Ralph Controller

`./scripts/ralph-codex.py` is the repository's human-run outer controller for long-running Codex work. It launches `codex app-server`, stores structured session state under `.codex/ralph-codex/`, starts in real Codex Plan Mode to build a broadened execution charter, runs an operator review loop before unattended execution begins, and resumes prior work only through explicit session commands.

This file is the canonical operator reference for Ralph. Other root docs should link here instead of duplicating its CLI surface or runtime defaults.

## CLI Surface

The public CLI is intentionally small:

1. `./scripts/ralph-codex.py`
   Prints help.
2. `./scripts/ralph-codex.py --message "Refactor the controller deeply"`
   Starts a new session from inline message text.
3. `./scripts/ralph-codex.py --file prompts/fix-tests.md`
   Starts a new session from a message file.
4. `./scripts/ralph-codex.py --file prompts/fix-tests.md --profile profiles/cautious.json`
   Starts a new session from a message file with a restricted custom profile.
5. `./scripts/ralph-codex.py --file prompts/fix-tests.md --profile profiles/dangerously-unrestricted.json`
   Starts a new session from a message file with full-access sandboxing.
6. `./scripts/ralph-codex.py --message "Refactor the controller deeply" --verbose`
   Starts a new verbose session with colored human-readable live status and event logging, plus compact structured terminal diagnostics and full wire diagnostics in `events.jsonl`.
7. `./scripts/ralph-codex.py --sessions 10`
   Lists the latest ten run-history rows.
8. `./scripts/ralph-codex.py --resume`
   Resumes the latest resumable session.
9. `./scripts/ralph-codex.py --resume 3`
   Resumes a specific resumable session by run-history index. A session id works too.

## Artifacts And State

- Example prompt and profile artifacts live under `prompts/` and `profiles/`, including `prompts/fix-tests.md`, `profiles/cautious.json`, and `profiles/dangerously-unrestricted.json`.
- Canonical schemas for Ralph artifacts live under `schemas/ralph-codex/`.
- The default profile is defined inline in `scripts/ralph-codex.py`.
- Each persisted JSON or JSONL artifact gets an adjacent copied schema file.
- Planning drafts are persisted in both `charter.json` (latest snapshot) and `charter-history.jsonl` (versioned draft history).
- Each run also writes a plain UTF-8 transcript under `sessions/<session-id>/logs/<run-id>.log`.

## Operational Defaults

- Ralph does not use turn inactivity timeouts. A live turn is allowed to stay silent while Codex reasons.
- Ralph always emits human-readable live status to `stdout` and event/error logging to `stderr` so an operator can follow along in the shell.
- Ralph mirrors the rendered terminal transcript and the raw app-server `stdin`, `stdout`, and `stderr` streams into the current run log under `sessions/<session-id>/logs/<run-id>.log`.
- Ralph formats live model output for humans instead of streaming raw schema JSON to the terminal during structured turns.
- Ralph planning runs in actual Plan Mode and explicitly forbids `update_plan`; plan revisions happen through repeated planning turns with controller feedback.
- When the initial planning charter requires operator review, Ralph prints that review block in full without console truncation in both normal and verbose mode, then offers an approve/change/abort loop instead of a one-shot `Y/n`.
- Operator-requested plan changes are fed back into another planning turn on the same thread until the operator approves the charter.
- If the planner needs material operator intent during planning, Ralph supports `request_user_input` and auto-selects the recommended option when answering those prompts.
- Ralph uses colored terminal layout automatically on interactive TTYs and falls back to plain text when output is redirected.
- Pressing `Ctrl+C` aborts the current run gracefully, clears the active controller run pointer, closes the app-server, and leaves the session resumable.
- After an abort, Ralph prints a one-line resume hint such as `./scripts/ralph-codex.py --resume <session-id>`.
- Ralph keeps `approvalPolicy` set to `never` in every access mode, so it does not ask for permissions during unattended execution after the initial plan approval.
- Ralph defaults to `thread_policy.access_mode: "restricted"`, which uses the `workspace-write` sandbox.
- `thread_policy.access_mode: "dangerously-unrestricted"` is an opt-in profile mode that uses `danger-full-access`.
- `max_iterations` uses `0` to mean unlimited. Non-zero values bound replanning loops, not wall-clock runtime.
- `execution.max_prompt_chars` defaults to `0`, which disables prompt-size caps unless a profile opts into one.
- Command activity from `commandExecution` items is passed through immediately, once per new state, in both normal and verbose mode. `WAIT` remains a thin elapsed-time heartbeat and does not replay already printed command lists.
- `events.jsonl` records semantic event changes and skips ghost duplicates where only the timestamp changed.
- Plan-review output includes a compact exec-log context reconstructed from semantic `commandExecution` notifications in `events.jsonl` for the reviewed planning turn.
- `events.jsonl` stays compact in normal mode and omits verbose wire bodies such as command `output`; `--verbose` enables those full diagnostics for the current run only while keeping console-rendered verbose payloads aggressively capped for readability. The plain-text run log is the full transcript artifact; `events.jsonl` remains the compact structured artifact.

## Verification

- When changing `scripts/ralph-codex.py`, `RALPH_CONTROLLER.md`, its schemas, or the related Ralph contract tests, run `python3 -m py_compile scripts/ralph-codex.py tests/test_ralph_codex.py tests/test_repo_contracts.py`.
- Then run `python3 -m unittest tests.test_repo_contracts tests.test_ralph_codex`.
