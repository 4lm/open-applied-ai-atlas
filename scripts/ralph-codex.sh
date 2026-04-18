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
  LOG_DIR          Iteration stdout/stderr directory. Default: repo-root .ralph
  MAX_ITERS        Stop after N iterations. Default: 100. Set 0 for unlimited
  SLEEP_SECS       Sleep between iterations. Default: 1
  COMPLETE_MARKER  Stdout marker that ends the loop. Default: <promise>COMPLETE</promise>
  USE_SEARCH       1 enables codex --search
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

  Different log directory:
    LOG_DIR=.ralph-review ./scripts/ralph-codex.sh

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
LOG_DIR="${LOG_DIR:-$ROOT_DIR/.ralph}"
MAX_ITERS="${MAX_ITERS:-100}"
SLEEP_SECS="${SLEEP_SECS:-1}"
COMPLETE_MARKER="${COMPLETE_MARKER:-<promise>COMPLETE</promise>}"
USE_SEARCH="${USE_SEARCH:-0}"
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

mkdir -p "$LOG_DIR"

iter=0

while :; do
  iter=$((iter + 1))

  out_file="$LOG_DIR/iter-$iter.out"
  err_file="$LOG_DIR/iter-$iter.err"

  echo "== Ralph iteration $iter =="

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

  if "$@" <"$PROMPT_FILE" >"$out_file" 2>"$err_file"; then
    :
  else
    echo "warning: codex exited non-zero on iteration $iter" >&2
  fi

  cat "$out_file"

  if grep -F "$COMPLETE_MARKER" "$out_file" >/dev/null 2>&1; then
    echo "Ralph finished on iteration $iter"
    exit 0
  fi

  if [ "$MAX_ITERS" -gt 0 ] && [ "$iter" -ge "$MAX_ITERS" ]; then
    echo "Reached MAX_ITERS=$MAX_ITERS without completion marker" >&2
    exit 2
  fi

  sleep "$SLEEP_SECS"
done
