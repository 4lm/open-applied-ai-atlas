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
  PROMPT_FILE      Prompt/context file. Default: .delivery/PROMPT.md. Completion policy always comes from this script.
  RALPH_LOG_FILE   Single-run Ralph ledger. Default: repo-root .ralph
  RALPH_STATE_DIR  Runner state directory. Default: repo-root .codex/ralph-loop
  MAX_ITERS        Stop after N iterations. Default: 100. Set 0 for unlimited
  SLEEP_SECS       Sleep between iterations. Default: 1
  COMPLETE_MARKER  Completion promise string inside the final JSON response. Default: <promise>ralph-codex/__COMPLETE__</promise>
  USE_SEARCH       Default: 1, enables codex --search
  MODEL            Optional codex model override, e.g. gpt-5.4
  PROFILE          Optional user-level Codex profile override
  EXTRA_ARGS       Extra raw args appended before `exec -` as shell-split tokens
  HARD_COMPLETE_CMD  Optional shell gate for custom prompts. Default: unset
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

  Different Ralph state directory:
    RALPH_STATE_DIR=.codex/ralph-loop-review ./scripts/ralph-codex.sh

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

  Custom prompt with explicit hard gate:
    PROMPT_FILE=prompts/fix-tests.md HARD_COMPLETE_CMD='test -f /tmp/task.done' ./scripts/ralph-codex.sh

  Extra raw Codex args:
    EXTRA_ARGS='--color never' ./scripts/ralph-codex.sh

  Dangerous global bypass:
    USE_BYPASS=1 ./scripts/ralph-codex.sh

Worked examples for the default repo flow

1. Implement the current .delivery/PIP.md
   The tracked default prompt lives at .delivery/PROMPT.md. It reads AGENTS.md,
   .delivery/PIP.md, and .delivery/STATUS.md, chooses one correct increment
   per run, runs relevant checks, and prints <promise>ralph-codex/__COMPLETE__</promise> in
   the final assistant JSON only when the shell runner can verify that the
   whole delivery job is actually done.

   Run:
     ./scripts/ralph-codex.sh

2. Different use case, not implementing .delivery/PIP.md
   Create a task-specific prompt such as prompts/fix-tests.md that reads the
   real control files for that job, for example README.md, TEST_FAILURES.md,
   and TODO.md, then fixes one correct increment per run. Custom prompts do
   not auto-complete unless HARD_COMPLETE_CMD is set.

   Run:
     PROMPT_FILE=prompts/fix-tests.md ./scripts/ralph-codex.sh
EOF
}

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
DEFAULT_PROMPT_FILE="$ROOT_DIR/.delivery/PROMPT.md"
DEFAULT_RALPH_LOG_FILE="$ROOT_DIR/.ralph"
DEFAULT_RALPH_STATE_DIR="$ROOT_DIR/.codex/ralph-loop"
STATUS_FILE="$ROOT_DIR/.delivery/STATUS.md"
HARNESS_CHECK_SCRIPT="$ROOT_DIR/scripts/delivery-harness-check.sh"

timestamp_now() {
  date '+%Y-%m-%d %H:%M:%S %Z'
}

epoch_now() {
  date '+%s'
}

append_log() {
  printf '%s\n' "$1" >>"$RALPH_LOG_FILE"
}

append_history() {
  printf '%s\n' "$1" >>"$ITERATION_HISTORY_FILE"
}

finish_run() {
  run_end_ts=$(timestamp_now)
  run_end_epoch=$(epoch_now)
  run_duration=$((run_end_epoch - run_start_epoch))
  append_log "Ralph run ended: $run_end_ts"
  append_log "Ralph run duration_seconds: $run_duration"
}

abs_path() {
  dir=$(CDPATH= cd -- "$(dirname -- "$1")" && pwd)
  printf '%s/%s\n' "$dir" "$(basename -- "$1")"
}

write_completion_schema() {
  python3 - "$COMPLETE_MARKER" >"$COMPLETION_SCHEMA_FILE" <<'PY'
import json
import sys

marker = sys.argv[1]
schema = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "status",
        "summary",
        "evidence",
        "next_step",
        "completion_promise",
        "gate_reasoning",
    ],
    "properties": {
        "status": {
            "type": "string",
            "enum": ["IN_PROGRESS", "BLOCKED", "COMPLETE"],
        },
        "summary": {"type": "string", "minLength": 1},
        "evidence": {
            "type": "array",
            "minItems": 1,
            "items": {"type": "string", "minLength": 1},
        },
        "next_step": {"type": "string", "minLength": 1},
        "completion_promise": {"type": "string"},
        "gate_reasoning": {"type": "string", "minLength": 1},
    },
    "description": (
        "Ralph loop final response. Use completion_promise=%s only when "
        "status is COMPLETE and the shell runner can verify completion." % marker
    ),
}
json.dump(schema, sys.stdout, indent=2)
sys.stdout.write("\n")
PY
}

count_open_gaps() {
  awk -F'\\|' '
  /^\| `G-[0-9][0-9]` / {
    status=$6
    gsub(/^ +| +$/, "", status)
    if (status == "Open") count++
  }
  END {
    print count + 0
  }
  ' "$STATUS_FILE"
}

list_open_gaps() {
  awk -F'\\|' '
  /^\| `G-[0-9][0-9]` / {
    gap=$2
    status=$6
    gsub(/^ +| +$/, "", gap)
    gsub(/^ +| +$/, "", status)
    gsub(/`/, "", gap)
    if (status == "Open") print gap
  }
  ' "$STATUS_FILE"
}

current_recommendation() {
  awk -F'\\|' '
  /^\| Current recommendation / {
    value=$3
    gsub(/^ +| +$/, "", value)
    gsub(/`/, "", value)
    print value
    exit
  }
  ' "$STATUS_FILE"
}

render_open_gaps_summary() {
  gaps=$(list_open_gaps)
  if [ -n "$gaps" ]; then
    printf '%s\n' "$gaps" | paste -sd ', ' -
  else
    printf '%s\n' "none"
  fi
}

write_feedback_note() {
  reason=$1
  {
    printf '## Iteration %s feedback\n' "$iter"
    printf '%s\n' "- rejection reason: $reason"
    if [ "$RUN_MODE" = "delivery" ]; then
      printf '%s\n' "- open gaps: $CURRENT_OPEN_GAPS"
      printf '%s\n' "- current recommendation: $CURRENT_RECOMMENDATION"
    elif [ -n "$HARD_COMPLETE_CMD" ]; then
      printf '%s\n' "- hard completion command: \`$HARD_COMPLETE_CMD\`"
    else
      printf '%s\n' '- hard completion command: unset'
    fi
    printf '%s\n' '- rule: do not emit COMPLETE until the shell runner confirms the hard gates.'
    if [ -s "$GATE_RESULT_FILE" ]; then
      printf '%s\n' '- gate output:'
      sed 's/^/  /' "$GATE_RESULT_FILE"
    fi
    printf '\n'
  } >>"$AUTO_FEEDBACK_FILE"
}

build_effective_prompt() {
  CURRENT_RECOMMENDATION=$(current_recommendation)
  CURRENT_OPEN_GAPS=$(render_open_gaps_summary)

  {
    cat <<EOF
# Ralph Runner Control Preamble

This control preamble is injected by \`scripts/ralph-codex.sh\` and overrides
any conflicting completion or stopping rule in the context prompt below.

You are inside a hard-gated Ralph loop.

Output contract:
- Your final assistant message must be a single JSON object matching the provided output schema.
- Set "status" to one of: IN_PROGRESS, BLOCKED, COMPLETE.
- "summary" must be a short factual summary of this iteration.
- "evidence" must be a non-empty list of concrete repo facts, checks, or edits.
- "next_step" must name the next best increment.
- "completion_promise" must be "$COMPLETE_MARKER" only when status is COMPLETE.
- If status is not COMPLETE, set "completion_promise" to "".
- "gate_reasoning" must explain why the shell runner should or should not allow completion.

Hard completion rules enforced by the shell runner:
- This shell preamble overrides any conflicting completion rule in the context prompt.
- False negatives are acceptable. False positives are not.
- If completion is uncertain, return IN_PROGRESS or BLOCKED.
EOF

    if [ "$RUN_MODE" = "delivery" ]; then
      cat <<EOF
- This is the default delivery flow.
- Never emit COMPLETE while .delivery/STATUS.md still has any Open gaps.
- Current recommendation: $CURRENT_RECOMMENDATION
- Current open gaps: $CURRENT_OPEN_GAPS
- The shell runner will require $HARNESS_CHECK_SCRIPT to pass before it accepts COMPLETE.
EOF
      if [ -n "$HARD_COMPLETE_CMD" ]; then
        cat <<EOF
- An additional operator hard gate is configured and must also pass:
  $HARD_COMPLETE_CMD
EOF
      fi
    else
      cat <<EOF
- This is a custom prompt flow.
EOF
      if [ -n "$HARD_COMPLETE_CMD" ]; then
        cat <<EOF
- The shell runner will reject COMPLETE unless HARD_COMPLETE_CMD exits 0.
- HARD_COMPLETE_CMD: $HARD_COMPLETE_CMD
EOF
      else
        cat <<'EOF'
- HARD_COMPLETE_CMD is not set.
- The shell runner will reject COMPLETE unconditionally in this mode.
- Return IN_PROGRESS or BLOCKED instead of COMPLETE.
EOF
      fi
    fi

    cat <<'EOF'

If the shell runner previously rejected your completion claim, treat that
feedback as authoritative and continue the task instead of arguing with it.

## Runner Feedback
EOF

    if [ -s "$AUTO_FEEDBACK_FILE" ]; then
      cat "$AUTO_FEEDBACK_FILE"
    else
      printf '%s\n' '_No prior rejection feedback._'
    fi

    printf '\n## Context Prompt\n\n'
    cat "$PROMPT_FILE_ABS"
  } >"$EFFECTIVE_PROMPT_FILE"
}

load_model_response() {
  MODEL_STATUS="INVALID"
  MODEL_SUMMARY=""
  MODEL_NEXT_STEP=""
  MODEL_PROMISE=""
  MODEL_GATE_REASONING=""
  MODEL_PARSE_REASON=""
  MODEL_ATTEMPTED_COMPLETE="no"
  MODEL_PROMISE_MATCHED="no"

  if [ ! -s "$LAST_MESSAGE_FILE" ]; then
    MODEL_PARSE_REASON="missing final assistant message"
    return 1
  fi

  if ! jq -e '
    type == "object" and
    (.status | type == "string") and
    (.summary | type == "string" and length > 0) and
    (.evidence | type == "array" and length > 0 and all(.[]; type == "string" and length > 0)) and
    (.next_step | type == "string" and length > 0) and
    (.completion_promise | type == "string") and
    (.gate_reasoning | type == "string" and length > 0)
  ' "$LAST_MESSAGE_FILE" >/dev/null 2>&1; then
    MODEL_PARSE_REASON="final assistant message failed JSON/schema validation"
    return 1
  fi

  MODEL_STATUS=$(jq -r '.status' "$LAST_MESSAGE_FILE")
  MODEL_SUMMARY=$(jq -r '.summary' "$LAST_MESSAGE_FILE")
  MODEL_NEXT_STEP=$(jq -r '.next_step' "$LAST_MESSAGE_FILE")
  MODEL_PROMISE=$(jq -r '.completion_promise' "$LAST_MESSAGE_FILE")
  MODEL_GATE_REASONING=$(jq -r '.gate_reasoning' "$LAST_MESSAGE_FILE")
  if [ "$MODEL_STATUS" = "COMPLETE" ]; then
    MODEL_ATTEMPTED_COMPLETE="yes"
  fi
  if [ "$MODEL_PROMISE" = "$COMPLETE_MARKER" ]; then
    MODEL_PROMISE_MATCHED="yes"
  fi
  MODEL_PARSE_REASON=""
  return 0
}

run_operator_gate() {
  : >"$GATE_RESULT_FILE"
  if [ -n "$HARD_COMPLETE_CMD" ]; then
    if /bin/sh -c "$HARD_COMPLETE_CMD" >"$GATE_RESULT_FILE" 2>&1; then
      return 0
    fi
    return 1
  fi
  printf '%s\n' "HARD_COMPLETE_CMD is unset." >"$GATE_RESULT_FILE"
  return 1
}

evaluate_completion_gate() {
  COMPLETION_ACCEPTED="no"
  REJECTION_REASON=""

  if [ "$codex_status" -ne 0 ]; then
    REJECTION_REASON="codex exited non-zero"
    return 1
  fi

  if ! load_model_response; then
    REJECTION_REASON="$MODEL_PARSE_REASON"
    return 1
  fi

  if [ "$MODEL_STATUS" != "COMPLETE" ]; then
    return 1
  fi

  if [ "$MODEL_PROMISE" != "$COMPLETE_MARKER" ]; then
    REJECTION_REASON="model reported COMPLETE without the exact completion promise"
    return 1
  fi

  if [ "$RUN_MODE" = "delivery" ]; then
    CURRENT_OPEN_GAPS=$(render_open_gaps_summary)
    CURRENT_RECOMMENDATION=$(current_recommendation)
    if [ "$(count_open_gaps)" -gt 0 ]; then
      REJECTION_REASON="delivery gaps remain open"
      return 1
    fi
    case "$CURRENT_RECOMMENDATION" in
      continue\ *|advance\ *)
        REJECTION_REASON="delivery recommendation still indicates more work"
        return 1
        ;;
    esac
    if ! "$HARNESS_CHECK_SCRIPT" >"$GATE_RESULT_FILE" 2>&1; then
      REJECTION_REASON="delivery harness check failed"
      return 1
    fi
    if [ -n "$HARD_COMPLETE_CMD" ] && ! run_operator_gate; then
      REJECTION_REASON="operator hard completion command failed"
      return 1
    fi
  else
    if ! run_operator_gate; then
      if [ -n "$HARD_COMPLETE_CMD" ]; then
        REJECTION_REASON="custom hard completion command failed"
      else
        REJECTION_REASON="custom prompts do not auto-complete without HARD_COMPLETE_CMD"
      fi
      return 1
    fi
  fi

  COMPLETION_ACCEPTED="yes"
  return 0
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
PROMPT_FILE="${PROMPT_FILE:-$DEFAULT_PROMPT_FILE}"
RALPH_LOG_FILE="${RALPH_LOG_FILE:-$DEFAULT_RALPH_LOG_FILE}"
RALPH_STATE_DIR="${RALPH_STATE_DIR:-$DEFAULT_RALPH_STATE_DIR}"
MAX_ITERS="${MAX_ITERS:-100}"
SLEEP_SECS="${SLEEP_SECS:-1}"
COMPLETE_MARKER="${COMPLETE_MARKER:-<promise>ralph-codex/__COMPLETE__</promise>}"
USE_SEARCH="${USE_SEARCH:-1}"
MODEL="${MODEL:-}"
PROFILE="${PROFILE:-}"
EXTRA_ARGS="${EXTRA_ARGS:-}"
HARD_COMPLETE_CMD="${HARD_COMPLETE_CMD:-}"
USE_BYPASS="${USE_BYPASS:-0}"

if ! command -v "$CODEX_BIN" >/dev/null 2>&1; then
  echo "error: codex binary not found: $CODEX_BIN" >&2
  exit 127
fi

if [ ! -f "$PROMPT_FILE" ]; then
  echo "error: prompt file not found: $PROMPT_FILE" >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "error: jq is required for Ralph completion gating" >&2
  exit 127
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "error: python3 is required for Ralph schema generation" >&2
  exit 127
fi

PROMPT_FILE_ABS=$(abs_path "$PROMPT_FILE")
DEFAULT_PROMPT_FILE_ABS=$(abs_path "$DEFAULT_PROMPT_FILE")
if [ "$PROMPT_FILE_ABS" = "$DEFAULT_PROMPT_FILE_ABS" ]; then
  RUN_MODE="delivery"
else
  RUN_MODE="custom"
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

if [ -f "$RALPH_STATE_DIR" ]; then
  echo "error: RALPH_STATE_DIR points to a file: $RALPH_STATE_DIR" >&2
  exit 1
fi

mkdir -p "$RALPH_STATE_DIR"
EFFECTIVE_PROMPT_FILE="$RALPH_STATE_DIR/effective-prompt.md"
COMPLETION_SCHEMA_FILE="$RALPH_STATE_DIR/completion-schema.json"
LAST_MESSAGE_FILE="$RALPH_STATE_DIR/last-message.json"
AUTO_FEEDBACK_FILE="$RALPH_STATE_DIR/auto-feedback.md"
ITERATION_HISTORY_FILE="$RALPH_STATE_DIR/iteration-history.md"
GATE_RESULT_FILE="$RALPH_STATE_DIR/gate-result.txt"

write_completion_schema
: >"$AUTO_FEEDBACK_FILE"
: >"$ITERATION_HISTORY_FILE"
: >"$LAST_MESSAGE_FILE"
: >"$GATE_RESULT_FILE"

: >"$RALPH_LOG_FILE"
run_start_ts=$(timestamp_now)
run_start_epoch=$(epoch_now)
append_log "Ralph run started: $run_start_ts"
append_log "workdir: $WORKDIR"
append_log "prompt file: $PROMPT_FILE_ABS"
append_log "run mode: $RUN_MODE"
append_log "state dir: $RALPH_STATE_DIR"
append_log "completion marker: $COMPLETE_MARKER"
append_log "model: ${MODEL:-default}"
append_log "profile: ${PROFILE:-default}"
append_log "search enabled: $USE_SEARCH"
append_log "bypass enabled: $USE_BYPASS"
append_log "max iterations: $MAX_ITERS"
append_log "sleep seconds: $SLEEP_SECS"
append_log "completion detection: schema + jq + hard shell gates"
if [ -n "$HARD_COMPLETE_CMD" ]; then
  append_log "hard completion command: $HARD_COMPLETE_CMD"
else
  append_log "hard completion command: unset"
fi
append_log ""

iter=0

while :; do
  iter=$((iter + 1))
  iter_start_ts=$(timestamp_now)
  iter_start_epoch=$(epoch_now)
  iter_fifo=$(mktemp -u "${TMPDIR:-/tmp}/ralph-codex-fifo.XXXXXX")
  : >"$LAST_MESSAGE_FILE"
  : >"$GATE_RESULT_FILE"
  build_effective_prompt

  echo "== Ralph iteration $iter =="
  append_log "Iteration $iter"
  append_log "  start: $iter_start_ts"
  append_log "  effective_prompt: $EFFECTIVE_PROMPT_FILE"

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

  set -- "$@" exec --output-schema "$COMPLETION_SCHEMA_FILE" -o "$LAST_MESSAGE_FILE" -

  mkfifo "$iter_fifo"
  tee <"$iter_fifo" &
  tee_pid=$!

  if "$@" <"$EFFECTIVE_PROMPT_FILE" >"$iter_fifo" 2>&1; then
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
  append_log "  completion_check_source: jq + shell hard gates"

  if evaluate_completion_gate; then
    append_log "  model_status: $MODEL_STATUS"
    append_log "  completion_marker_seen: yes"
    append_log "  stop_reason: hard completion gates passed"
    append_log ""
    append_history "## Iteration $iter"
    append_history "- start: $iter_start_ts"
    append_history "- end: $iter_end_ts"
    append_history "- codex exit status: $codex_status"
    append_history "- model status: $MODEL_STATUS"
    append_history "- summary: $MODEL_SUMMARY"
    append_history "- next step: $MODEL_NEXT_STEP"
    append_history "- completion accepted: yes"
    append_history ""
    echo "Ralph finished on iteration $iter"
    finish_run
    exit 0
  fi

  if [ -n "${MODEL_STATUS:-}" ] && [ "$MODEL_STATUS" != "INVALID" ]; then
    append_log "  model_status: $MODEL_STATUS"
  fi

  if [ "${MODEL_ATTEMPTED_COMPLETE:-no}" = "yes" ] && [ "${MODEL_PROMISE_MATCHED:-no}" = "yes" ]; then
    append_log "  completion_marker_seen: yes"
  else
    append_log "  completion_marker_seen: no"
  fi

  if [ -n "${REJECTION_REASON:-}" ]; then
    append_log "  rejection_reason: $REJECTION_REASON"
    write_feedback_note "$REJECTION_REASON"
  else
    append_log "  rejection_reason: none"
  fi

  append_history "## Iteration $iter"
  append_history "- start: $iter_start_ts"
  append_history "- end: $iter_end_ts"
  append_history "- codex exit status: $codex_status"
  append_history "- model status: ${MODEL_STATUS:-INVALID}"
  if [ -n "${MODEL_SUMMARY:-}" ]; then
    append_history "- summary: $MODEL_SUMMARY"
  fi
  if [ -n "${MODEL_NEXT_STEP:-}" ]; then
    append_history "- next step: $MODEL_NEXT_STEP"
  fi
  append_history "- completion accepted: no"
  if [ -n "${REJECTION_REASON:-}" ]; then
    append_history "- rejection reason: $REJECTION_REASON"
  fi
  append_history ""

  if [ "$MAX_ITERS" -gt 0 ] && [ "$iter" -ge "$MAX_ITERS" ]; then
    append_log "  stop_reason: reached MAX_ITERS=$MAX_ITERS"
    append_log ""
    finish_run
    echo "Reached MAX_ITERS=$MAX_ITERS without verified completion" >&2
    exit 2
  fi

  append_log "  stop_reason: continue"
  append_log ""
  sleep "$SLEEP_SECS"
done
