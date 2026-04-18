#!/bin/sh
set -eu

# Human-run outer loop for repeated Codex execution from a shell.
# Each iteration is a fresh Codex run against the same prompt file.
# Persistent state should live in repo files, not in this script's process state.
# This is not intended as a recursive driver from inside a live Codex session.

print_help() {
  cat <<'EOF'
Usage: ./scripts/ralph-codex.sh
       PROMPT_FILE=prompts/fix-tests.md ./scripts/ralph-codex.sh
       ./scripts/ralph-codex.sh -h | --help

Human-run outer loop for repeated fresh `codex exec -` runs.
Not intended for recursive use by Codex inside a live Codex session.
Default unattended mode is already auto-allow via `-a never -s danger-full-access`.
Codex `--full-auto` is not used here because it is weaker (`workspace-write` sandbox).

Environment:
  CODEX_BIN        Codex CLI binary to run. Default: codex
  WORKDIR          Repo or task working directory. Default: repo root
  PROMPT_FILE      Prompt file to feed to each run. Default: .delivery/PROMPT.md
  RALPH_LOG_FILE   Single-run Ralph ledger. Default: repo-root .ralph
  MAX_ITERS        Stop after N iterations. Default: 100. Set 0 for unlimited
  SLEEP_SECS       Sleep between iterations. Default: 1
  COMPLETE_MARKER  Output marker that ends the loop. Default: <promise>COMPLETE</promise>
  USE_SEARCH       Default: 1, enables codex --search
  MODEL            Optional codex model override, e.g. gpt-5.4
  PROFILE          Optional user-level Codex profile override
  EXTRA_ARGS       Extra raw args appended before `exec -` as shell-split tokens
  USE_BYPASS       1 uses --dangerously-bypass-approvals-and-sandbox

Profile example (~/.codex/config.toml):
  [profiles.ralph]
  model = "gpt-5.4"
  model_reasoning_effort = "high"

  Use:
    PROFILE=ralph ./scripts/ralph-codex.sh

Common examples:
  Default repo run:
    ./scripts/ralph-codex.sh

  Custom prompt file:
    PROMPT_FILE=prompts/fix-tests.md ./scripts/ralph-codex.sh

  Different working directory:
    WORKDIR=/path/to/repo ./scripts/ralph-codex.sh

  Different Ralph ledger file:
    RALPH_LOG_FILE=.ralph-review ./scripts/ralph-codex.sh

  Limit the run:
    MAX_ITERS=25 ./scripts/ralph-codex.sh

  Unlimited iterations:
    MAX_ITERS=0 ./scripts/ralph-codex.sh

  Search-enabled run:
    USE_SEARCH=1 ./scripts/ralph-codex.sh

  Model override:
    MODEL=gpt-5.4 ./scripts/ralph-codex.sh

  Custom completion marker:
    COMPLETE_MARKER='<promise>DONE</promise>' ./scripts/ralph-codex.sh

  Extra raw Codex args:
    EXTRA_ARGS='--color never' ./scripts/ralph-codex.sh

  Dangerous global bypass:
    USE_BYPASS=1 ./scripts/ralph-codex.sh

Worked examples for the default repo flow

1. Implement the current .delivery/PIP.md
   The tracked default prompt lives at .delivery/PROMPT.md. It reads AGENTS.md,
   .delivery/PIP.md, and .delivery/STATUS.md, chooses one correct increment
   per run, runs relevant checks, and prints <promise>COMPLETE</promise> only
   when the overall job is done.

   Run:
     ./scripts/ralph-codex.sh

2. Different use case, not implementing .delivery/PIP.md
   Create a task-specific prompt such as prompts/fix-tests.md that reads the
   real control files for that job, for example README.md, TEST_FAILURES.md,
   and TODO.md, then fixes one correct increment per run until complete.

   Run:
     PROMPT_FILE=prompts/fix-tests.md ./scripts/ralph-codex.sh
EOF
}

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
DEFAULT_RALPH_LOG_FILE="$ROOT_DIR/.ralph"

timestamp_now() {
  date '+%Y-%m-%d %H:%M:%S %Z'
}

epoch_now() {
  date '+%s'
}

append_log() {
  printf '%s\n' "$1" >>"$RALPH_LOG_FILE"
}

finish_run() {
  run_end_ts=$(timestamp_now)
  run_end_epoch=$(epoch_now)
  run_duration=$((run_end_epoch - run_start_epoch))
  append_log "Ralph run ended: $run_end_ts"
  append_log "Ralph run duration_seconds: $run_duration"
}

for arg in "$@"; do
  case "$arg" in
    -h|--help)
      print_help
      exit 0
      ;;
  esac
done

CODEX_BIN="${CODEX_BIN:-codex}"
WORKDIR="${WORKDIR:-$ROOT_DIR}"
PROMPT_FILE="${PROMPT_FILE:-$ROOT_DIR/.delivery/PROMPT.md}"
RALPH_LOG_FILE="${RALPH_LOG_FILE:-$DEFAULT_RALPH_LOG_FILE}"
MAX_ITERS="${MAX_ITERS:-100}"
SLEEP_SECS="${SLEEP_SECS:-1}"
COMPLETE_MARKER="${COMPLETE_MARKER:-<promise>COMPLETE</promise>}"
USE_SEARCH="${USE_SEARCH:-1}"
MODEL="${MODEL:-}"
PROFILE="${PROFILE:-}"
EXTRA_ARGS="${EXTRA_ARGS:-}"
USE_BYPASS="${USE_BYPASS:-0}"

if ! command -v "$CODEX_BIN" >/dev/null 2>&1; then
  echo "error: codex binary not found: $CODEX_BIN" >&2
  exit 127
fi

if [ ! -f "$PROMPT_FILE" ]; then
  echo "error: prompt file not found: $PROMPT_FILE" >&2
  exit 1
fi

RALPH_LOG_DIR=$(dirname -- "$RALPH_LOG_FILE")
mkdir -p "$RALPH_LOG_DIR"

if [ -d "$RALPH_LOG_FILE" ]; then
  if [ "$RALPH_LOG_FILE" = "$DEFAULT_RALPH_LOG_FILE" ]; then
    rm -rf "$RALPH_LOG_FILE"
  else
    echo "error: RALPH_LOG_FILE points to a directory: $RALPH_LOG_FILE" >&2
    exit 1
  fi
fi

: >"$RALPH_LOG_FILE"
run_start_ts=$(timestamp_now)
run_start_epoch=$(epoch_now)
append_log "Ralph run started: $run_start_ts"
append_log "workdir: $WORKDIR"
append_log "prompt file: $PROMPT_FILE"
append_log "completion marker: $COMPLETE_MARKER"
append_log "model: ${MODEL:-default}"
append_log "profile: ${PROFILE:-default}"
append_log "search enabled: $USE_SEARCH"
append_log "bypass enabled: $USE_BYPASS"
append_log "max iterations: $MAX_ITERS"
append_log "sleep seconds: $SLEEP_SECS"
append_log ""

iter=0

while :; do
  iter=$((iter + 1))
  iter_start_ts=$(timestamp_now)
  iter_start_epoch=$(epoch_now)
  iter_output=$(mktemp "${TMPDIR:-/tmp}/ralph-codex-output.XXXXXX")
  iter_fifo=$(mktemp -u "${TMPDIR:-/tmp}/ralph-codex-fifo.XXXXXX")

  echo "== Ralph iteration $iter =="
  append_log "Iteration $iter"
  append_log "  start: $iter_start_ts"

  set -- "$CODEX_BIN"

  if [ -n "$PROFILE" ]; then
    set -- "$@" --profile "$PROFILE"
  fi

  if [ -n "$MODEL" ]; then
    set -- "$@" --model "$MODEL"
  fi

  if [ "$USE_SEARCH" = "1" ]; then
    set -- "$@" --search
  fi

  set -- "$@" -C "$WORKDIR"

  if [ "$USE_BYPASS" = "1" ]; then
    set -- "$@" --dangerously-bypass-approvals-and-sandbox
  else
    set -- "$@" -a never -s danger-full-access
  fi

  if [ -n "$EXTRA_ARGS" ]; then
    # Intentionally allow shell-style splitting for operator-supplied extra args.
    # shellcheck disable=SC2086
    set -- "$@" $EXTRA_ARGS
  fi

  set -- "$@" exec -

  mkfifo "$iter_fifo"
  tee "$iter_output" <"$iter_fifo" &
  tee_pid=$!

  if "$@" <"$PROMPT_FILE" >"$iter_fifo" 2>&1; then
    codex_status=0
  else
    codex_status=$?
    echo "warning: codex exited non-zero on iteration $iter" >&2
  fi

  wait "$tee_pid"
  rm -f "$iter_fifo"

  iter_end_ts=$(timestamp_now)
  iter_end_epoch=$(epoch_now)
  iter_duration=$((iter_end_epoch - iter_start_epoch))
  append_log "  end: $iter_end_ts"
  append_log "  duration_seconds: $iter_duration"
  append_log "  exit_status: $codex_status"

  if grep -F "$COMPLETE_MARKER" "$iter_output" >/dev/null 2>&1; then
    append_log "  completion_marker_seen: yes"
    append_log "  stop_reason: completion marker"
    append_log ""
    echo "Ralph finished on iteration $iter"
    finish_run
    rm -f "$iter_output"
    exit 0
  fi

  append_log "  completion_marker_seen: no"

  if [ "$MAX_ITERS" -gt 0 ] && [ "$iter" -ge "$MAX_ITERS" ]; then
    append_log "  stop_reason: reached MAX_ITERS=$MAX_ITERS"
    append_log ""
    finish_run
    rm -f "$iter_output"
    echo "Reached MAX_ITERS=$MAX_ITERS without completion marker" >&2
    exit 2
  fi

  append_log "  stop_reason: continue"
  append_log ""
  rm -f "$iter_output"
  sleep "$SLEEP_SECS"
done
