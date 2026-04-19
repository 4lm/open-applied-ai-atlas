#!/usr/bin/env python3
"""Universal session-driven Ralph controller built on Codex app-server."""

from __future__ import annotations

import argparse
from collections import deque
import json
import queue
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent, wrap
from typing import Any, Callable, Optional


VERSION = "0.1.0"
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
SCHEMA_ROOT = REPO_ROOT / "schemas"
DEFAULT_PROFILE_PATH = REPO_ROOT / "profiles" / "restricted.json"
STATE_ROOT_NAME = ".codex/ralph-codex"
CODEx_BIN = "codex"
APP_SERVER_REQUEST_TIMEOUT_SECS = 30.0
STDERR_BUFFER_LINES = 50
TURN_IDLE_HEARTBEAT_SECS = 10.0
VERBOSE_CONSOLE_CHAR_LIMIT = 240
CONSOLE_WRAP_WIDTH = 88
MODEL_WORKSTREAM_PREVIEW_COUNT = 4
MODEL_GAP_PREVIEW_COUNT = 4
ABORT_EXIT_CODE = 130
ABORT_REASON = "aborted by operator"

PROFILE_SCHEMA_ID = "ralph-codex/profile"
PLANNING_OUTPUT_SCHEMA_ID = "ralph-codex/output/planning"
EXECUTION_OUTPUT_SCHEMA_ID = "ralph-codex/output/execution"
EVALUATION_OUTPUT_SCHEMA_ID = "ralph-codex/output/evaluation"
CONTROLLER_STATE_SCHEMA_ID = "ralph-codex/controller-state"
SESSION_SCHEMA_ID = "ralph-codex/session"
TASK_SCHEMA_ID = "ralph-codex/task"
SESSION_STATE_SCHEMA_ID = "ralph-codex/session-state"
CHARTER_SCHEMA_ID = "ralph-codex/charter"
CHARTER_HISTORY_LINE_SCHEMA_ID = "ralph-codex/charter-history-line"
COMPLETION_SCHEMA_ID = "ralph-codex/completion"
FINISHED_SCHEMA_ID = "ralph-codex/finished"
RUN_HISTORY_LINE_SCHEMA_ID = "ralph-codex/run-history-line"
EVENT_LOG_LINE_SCHEMA_ID = "ralph-codex/event-log-line"
TURN_LOG_LINE_SCHEMA_ID = "ralph-codex/turn-log-line"
SERVER_REQUEST_LOG_LINE_SCHEMA_ID = "ralph-codex/server-request-log-line"

WORKER_SUMMARY_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["role", "summary", "findings", "confidence"],
    "properties": {
        "role": {"type": "string", "enum": ["research", "read_only_repo", "evaluator_vote"]},
        "summary": {"type": "string", "minLength": 1},
        "findings": {
            "type": "array",
            "items": {"type": "string", "minLength": 1},
        },
        "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
        "sources": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["title", "url", "source_type", "used_for"],
                "properties": {
                    "title": {"type": "string", "minLength": 1},
                    "url": {"type": "string", "minLength": 1},
                    "source_type": {"type": "string", "enum": ["primary", "secondary"]},
                    "used_for": {"type": "string", "minLength": 1},
                },
            },
        },
    },
}

SCHEMA_FILES = {
    PROFILE_SCHEMA_ID: SCHEMA_ROOT / "ralph-codex" / "profile-v0.1.0.schema.json",
    PLANNING_OUTPUT_SCHEMA_ID: SCHEMA_ROOT / "ralph-codex" / "planning-output-v0.1.0.schema.json",
    EXECUTION_OUTPUT_SCHEMA_ID: SCHEMA_ROOT / "ralph-codex" / "execution-output-v0.1.0.schema.json",
    EVALUATION_OUTPUT_SCHEMA_ID: SCHEMA_ROOT / "ralph-codex" / "evaluation-output-v0.1.0.schema.json",
    CONTROLLER_STATE_SCHEMA_ID: SCHEMA_ROOT / "ralph-codex" / "controller-state-v0.1.0.schema.json",
    SESSION_SCHEMA_ID: SCHEMA_ROOT / "ralph-codex" / "session-v0.1.0.schema.json",
    TASK_SCHEMA_ID: SCHEMA_ROOT / "ralph-codex" / "task-v0.1.0.schema.json",
    SESSION_STATE_SCHEMA_ID: SCHEMA_ROOT / "ralph-codex" / "session-state-v0.1.0.schema.json",
    CHARTER_SCHEMA_ID: SCHEMA_ROOT / "ralph-codex" / "charter-v0.1.0.schema.json",
    CHARTER_HISTORY_LINE_SCHEMA_ID: SCHEMA_ROOT / "ralph-codex" / "charter-history-line-v0.1.0.schema.json",
    COMPLETION_SCHEMA_ID: SCHEMA_ROOT / "ralph-codex" / "completion-v0.1.0.schema.json",
    FINISHED_SCHEMA_ID: SCHEMA_ROOT / "ralph-codex" / "finished-v0.1.0.schema.json",
    RUN_HISTORY_LINE_SCHEMA_ID: SCHEMA_ROOT / "ralph-codex" / "run-history-line-v0.1.0.schema.json",
    EVENT_LOG_LINE_SCHEMA_ID: SCHEMA_ROOT / "ralph-codex" / "event-log-line-v0.1.0.schema.json",
    TURN_LOG_LINE_SCHEMA_ID: SCHEMA_ROOT / "ralph-codex" / "turn-log-line-v0.1.0.schema.json",
    SERVER_REQUEST_LOG_LINE_SCHEMA_ID: SCHEMA_ROOT / "ralph-codex" / "server-request-log-line-v0.1.0.schema.json",
}

SESSION_ID_RE = re.compile(r"^\d{8}T\d{9}Z_[0-9a-f]{12}$")
REASONING_LEVELS = {"low", "medium", "high", "xhigh"}
_DEFAULT_PROFILE_CACHE: dict[str, Any] | None = None

META_ARTIFACT_PATTERNS = (
    "ledger",
    "scoreboard",
    "parity-matrix",
    "structural-change",
)
REPEATED_HEADING_PATTERNS = (
    "## Internal Chapter Handoff Map",
    "## When This Chapter Must Reopen",
    "## Scenario-To-Chapter Handoff Matrix",
    "## Organization-Type Trade-Offs",
    "## Rejected Defaults",
    "## Verification Status In This Environment",
)

SANDBOX_BY_ACCESS_MODE = {
    "restricted": "workspace-write",
    "dangerously-unrestricted": "danger-full-access",
}


class RalphError(RuntimeError):
    """Raised when the Ralph controller cannot proceed safely."""


class UnsupportedPromptError(RalphError):
    """Raised when Codex asks a prompt Ralph cannot answer automatically."""


class PlanReviewAborted(KeyboardInterrupt):
    """Raised when the operator aborts during plan review."""


class ProgressReviewAborted(KeyboardInterrupt):
    """Raised when the operator aborts during a quality checkpoint."""


@dataclass
class Command:
    kind: str
    value: str | None = None
    profile_path: Path | None = None
    verbose: bool = False


@dataclass
class RuntimeConfig:
    workdir: Path
    state_root: Path


@dataclass
class ExecutionAudit:
    ok: bool
    feedback: str
    total_files_changed: int
    repeated_heading_file_count: int
    meta_artifact_files: list[str]
    requires_checkpoint: bool
    checkpoint_reason: str
    diff_samples: list[str]
    novelty_score: float = 0.0
    acceptance_progress_score: float = 0.0
    acceptance_criteria_met: list[str] | None = None
    acceptance_criteria_remaining: list[str] | None = None
    off_tranche_file_count: int = 0


@dataclass
class TurnOutputTracker:
    candidate_texts: list[str] = field(default_factory=list)
    seen_item_types: list[str] = field(default_factory=list)
    search_names: list[str] = field(default_factory=list)
    max_seen_item_types: int = 32

    def record_raw_item(self, item: dict[str, Any]) -> None:
        self._record_item_type(f"raw:{item.get('type', 'unknown')}")
        if item.get("type") == "message":
            if item.get("role") not in {"assistant", "model"}:
                return
            if item.get("phase") not in {None, "final_answer"}:
                return
            text = "".join(
                content.get("text", "")
                for content in item.get("content", [])
                if content.get("type") == "output_text"
            ).strip()
            if text:
                self.candidate_texts.append(text)
            return
        name = str(item.get("name", "")).strip()
        if str(item.get("type", "")).strip().lower() == "function_call" and "search" in name.lower():
            self.search_names.append(name)

    def record_thread_item(self, item: dict[str, Any]) -> None:
        item_type = str(item.get("type", "unknown")).strip()
        self._record_item_type(f"thread:{item_type}")
        text_value = item.get("text")
        text = text_value.strip() if isinstance(text_value, str) else ""
        if item_type in {"agentMessage", "plan"} and text:
            self.candidate_texts.append(text)
        if item_type != "commandExecution":
            return
        primary_action = str(item.get("primary_action", "")).strip().lower()
        if primary_action == "search":
            self.search_names.append(str(item.get("primary_target", "")).strip() or "search")

    def extract_final_output(self, schema: dict[str, Any]) -> dict[str, Any]:
        for text in reversed(self.candidate_texts):
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                validate_subset(schema, parsed)
                return parsed
        item_summary = ", ".join(self.seen_item_types[-10:]) if self.seen_item_types else "none"
        raise RalphError(
            "turn completed without a parseable final structured response "
            f"(seen items: {item_summary})"
        )

    def summarize_search_activity(self) -> dict[str, Any]:
        unique_names = sorted({name for name in self.search_names if name})
        return {"count": len(self.search_names), "names": unique_names}

    def _record_item_type(self, item_type: str) -> None:
        self.seen_item_types.append(item_type)
        overflow = len(self.seen_item_types) - self.max_seen_item_types
        if overflow > 0:
            del self.seen_item_types[:overflow]


class PlainTextRunLog:
    ANSI_ESCAPE_RE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")

    def __init__(
        self,
        path: Path,
        session_id: str,
        run_id: str,
        invocation_mode: str,
        verbose: bool,
    ):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._handle = self.path.open("w", encoding="utf-8", buffering=1)
        self._closed = False
        self._lock = threading.Lock()
        self._active_channel: str | None = None
        self._line_open = False
        header_lines = [
            "# Ralph Codex run log",
            f"session_id: {session_id}",
            f"run_id: {run_id}",
            f"invocation_mode: {invocation_mode}",
            f"verbose: {str(verbose).lower()}",
            f"started_at: {utc_timestamp()}",
            "",
        ]
        self._handle.write("\n".join(header_lines))
        self._handle.flush()

    def write_chunk(self, channel: str, text: str, *, strip_ansi: bool = False) -> None:
        if not text or self._closed:
            return
        rendered = self.ANSI_ESCAPE_RE.sub("", text) if strip_ansi else text
        with self._lock:
            if self._line_open and self._active_channel not in {None, channel}:
                self._handle.write("\n")
                self._handle.flush()
                self._line_open = False
                self._active_channel = None
            remaining = rendered
            while remaining:
                if not self._line_open:
                    self._handle.write(f"{utc_timestamp()} {channel} ")
                    self._active_channel = channel
                    self._line_open = True
                newline_index = remaining.find("\n")
                if newline_index < 0:
                    self._handle.write(remaining)
                    self._handle.flush()
                    break
                self._handle.write(remaining[: newline_index + 1])
                self._handle.flush()
                self._line_open = False
                self._active_channel = None
                remaining = remaining[newline_index + 1 :]

    def write_console_input(self, text: str) -> None:
        self.write_chunk("STDIN", text, strip_ansi=True)

    def write_console_output(self, stream_name: str, text: str) -> None:
        channel = "STDOUT" if stream_name == "stdout" else "STDERR"
        self.write_chunk(channel, text, strip_ansi=True)

    def close(self) -> None:
        with self._lock:
            if self._closed:
                return
            if self._line_open:
                self._handle.write("\n")
            self._handle.flush()
            self._handle.close()
            self._closed = True


class TerminalReporter:
    BADGE_WIDTH = 8

    def __init__(
        self,
        verbose: bool,
        stdout: Any = sys.stdout,
        stderr: Any = sys.stderr,
        session_log: PlainTextRunLog | None = None,
    ):
        self.verbose = verbose
        self.stdout = stdout
        self.stderr = stderr
        self.session_log = session_log
        self._stdout_at_line_start = True
        self._stderr_at_line_start = True
        self._stdout_color = self._supports_color(stdout)
        self._stderr_color = self._supports_color(stderr)
        self._model_stream_active = False
        self._model_stream_at_line_start = True

    def status(self, message: str, badge: str = "STARTING", tone: str = "status") -> None:
        self._emit_record("stdout", badge, message, tone=tone)

    def wait(
        self,
        phase_name: str,
        elapsed_seconds: int,
        command_rows: list[dict[str, Any]] | None = None,
        badge: str = "WORKING",
    ) -> None:
        title = f"{phase_name} running for {elapsed_seconds}s"
        self._emit_record("stdout", badge, title, tone="wait")

    def event(self, message: str, tone: str = "event") -> None:
        badge = {"error": "ERROR", "warn": "WARNING"}.get(tone, "NOTICE")
        self._emit_record("stderr", badge, message, tone=tone)

    def tool(self, detail: str, stream_name: str = "stdout") -> None:
        self._emit_record(stream_name, "TOOL", detail, tone="tool")

    def prompt(self, message: str) -> None:
        self._emit_record("stderr", "REVIEW", message, tone="prompt")

    def approval_prompt(self, message: str) -> None:
        self._emit_record("stdout", "REVIEW", message, tone="prompt")

    def command_trace_context(self, trace_rows: list[dict[str, Any]]) -> None:
        if not trace_rows:
            return
        lines = self._render_command_trace_lines(trace_rows)
        self._emit_block("stdout", "REVIEW", "exec log context", lines, tone="tool")

    def review_diff(self, title: str, detail_lines: list[str]) -> None:
        if not detail_lines:
            return
        self._emit_block("stdout", "REVIEW", title, detail_lines, tone="tool")

    def model_result(self, phase_name: str, payload: dict[str, Any], full: bool = False) -> None:
        lines = self._render_full_model_payload_lines(payload) if full else self._render_model_payload_lines(payload)
        title = f"{phase_name} result"
        self._emit_block("stdout", "RESULT", title, lines, tone="model")

    def model_text(self, phase_name: str, text: str) -> None:
        cleaned = " ".join(text.split())
        if not cleaned:
            return
        self._emit_block(
            "stdout",
            "RESULT",
            f"{phase_name} message",
            self._wrap_detail(cleaned, width=CONSOLE_WRAP_WIDTH - 4),
            tone="model",
        )

    def stream_model_text(self, phase_name: str, text: str) -> bool:
        if not text:
            return False
        if not self._model_stream_active:
            self._emit_block("stdout", "RESULT", f"{phase_name} message", [], tone="model")
            self._model_stream_active = True
            self._model_stream_at_line_start = True
        indent = f"{' ' * 9} {' ' * self.BADGE_WIDTH} "
        for chunk in text.splitlines(keepends=True):
            if self._model_stream_at_line_start:
                self._write("stdout", indent)
            self._write("stdout", chunk)
            self._model_stream_at_line_start = chunk.endswith("\n")
        if not text.endswith(("\n", "\r")) and self._model_stream_at_line_start:
            self._write("stdout", indent)
            self._model_stream_at_line_start = False
        return True

    def finish_model_text_stream(self) -> None:
        if not self._model_stream_active:
            return
        if not self._model_stream_at_line_start:
            self._write("stdout", "\n")
        self._model_stream_active = False
        self._model_stream_at_line_start = True

    def verbose_trace(self, event_type: str, payload: dict[str, Any]) -> None:
        return

    def finish_stdout_line(self) -> None:
        self.finish_model_text_stream()
        if not self._stdout_at_line_start:
            self._write("stdout", "\n")

    def console_input(self, text: str) -> None:
        if self.session_log is not None:
            self.session_log.write_console_input(text)

    @staticmethod
    def stringify(value: Any) -> str:
        if isinstance(value, str):
            return value
        try:
            return json.dumps(value, sort_keys=True)
        except TypeError:
            return str(value)

    @staticmethod
    def cap_console_text(text: str, limit: int = VERBOSE_CONSOLE_CHAR_LIMIT) -> str:
        if len(text) <= limit:
            return text
        marker = "... (truncated for console)"
        return text[: max(0, limit - len(marker))] + marker

    def _emit_record(self, stream_name: str, label: str, message: str, tone: str) -> None:
        self._prepare_line(stream_name)
        timestamp = self._style(stream_name, utc_now().strftime("%H:%M:%SZ"), "meta")
        badge = self._style(stream_name, label.upper().ljust(self.BADGE_WIDTH), tone)
        wrapped = self._wrap_detail(message)
        if not wrapped:
            wrapped = [""]
        first, *rest = wrapped
        self._write(stream_name, f"{timestamp} {badge} {first}\n")
        for line in rest:
            self._write(stream_name, f"{' ' * 9} {' ' * self.BADGE_WIDTH} {line}\n")

    def _emit_block(
        self,
        stream_name: str,
        label: str,
        title: str,
        detail_lines: list[str],
        tone: str,
    ) -> None:
        self._prepare_line(stream_name)
        timestamp = self._style(stream_name, utc_now().strftime("%H:%M:%SZ"), "meta")
        badge = self._style(stream_name, label.upper().ljust(self.BADGE_WIDTH), tone)
        header = self._style(stream_name, title, "title")
        self._write(stream_name, f"{timestamp} {badge} {header}\n")
        for line in detail_lines:
            self._write(stream_name, f"{' ' * 9} {' ' * self.BADGE_WIDTH} {line}\n")

    def _prepare_line(self, stream_name: str) -> None:
        if stream_name == "stdout":
            self.finish_stdout_line()
        elif not self._stderr_at_line_start:
            self._write("stderr", "\n")

    def _write(self, stream_name: str, text: str) -> None:
        stream = self.stdout if stream_name == "stdout" else self.stderr
        stream.write(text)
        stream.flush()
        if self.session_log is not None:
            self.session_log.write_console_output(stream_name, text)
        if stream_name == "stdout":
            self._stdout_at_line_start = text.endswith("\n")
        else:
            self._stderr_at_line_start = text.endswith("\n")

    def _style(self, stream_name: str, text: str, tone: str) -> str:
        if not self._colors_enabled(stream_name):
            return text
        color_by_tone = {
            "meta": "\033[2m",
            "status": "\033[36m",
            "wait": "\033[34m",
            "event": "\033[35m",
            "tool": "\033[33m",
            "prompt": "\033[95m",
            "model": "\033[32m",
            "trace": "\033[2m",
            "error": "\033[31m",
            "warn": "\033[33m",
            "title": "\033[1m",
            "key": "\033[36m",
            "value": "\033[32m",
        }
        color = color_by_tone.get(tone)
        if not color:
            return text
        return f"{color}{text}\033[0m"

    def _colors_enabled(self, stream_name: str) -> bool:
        return self._stdout_color if stream_name == "stdout" else self._stderr_color

    @staticmethod
    def _supports_color(stream: Any) -> bool:
        isatty = getattr(stream, "isatty", None)
        if not callable(isatty):
            return False
        try:
            return bool(isatty())
        except Exception:
            return False

    def _wrap_detail(self, text: str, width: int = CONSOLE_WRAP_WIDTH) -> list[str]:
        normalized = " ".join(text.split())
        if not normalized:
            return []
        return wrap(normalized, width=width) or [normalized]

    def _format_kv(self, stream_name: str, key: str, value: str) -> str:
        return f"{self._style(stream_name, key + ':', 'key')} {self._style(stream_name, value, 'value')}"

    def _render_model_payload_lines(self, payload: dict[str, Any]) -> list[str]:
        lines: list[str] = []
        scalar_keys = ("status", "summary", "next_step", "gate_reasoning", "broadening_rationale")
        for key in scalar_keys:
            if isinstance(payload.get(key), str) and payload[key].strip():
                value = self.cap_console_text(" ".join(payload[key].split()))
                lines.extend(self._wrap_detail(self._format_kv("stdout", key, value), width=CONSOLE_WRAP_WIDTH - 4))
        program_board = payload.get("program_board")
        if not isinstance(program_board, dict) and isinstance(payload.get("charter"), dict):
            program_board = legacy_program_board_from_charter(payload.get("charter"))
        if isinstance(program_board, dict):
            milestones = program_board.get("milestones") or []
            workstreams = [
                workstream
                for milestone in milestones
                for workstream in milestone.get("workstreams") or []
            ]
            success_criteria = program_board.get("success_criteria") or []
            if success_criteria:
                lines.append(self._format_kv("stdout", "success", f"{len(success_criteria)} criteria"))
            if milestones:
                lines.append(self._format_kv("stdout", "milestones", f"{len(milestones)} planned"))
            if workstreams:
                lines.append(self._format_kv("stdout", "workstreams", f"{len(workstreams)} planned"))
                for workstream in workstreams[:MODEL_WORKSTREAM_PREVIEW_COUNT]:
                    identifier = workstream.get("id", "?")
                    title = self.cap_console_text(" ".join(str(workstream.get("title", "")).split()), limit=72)
                    lines.extend(self._wrap_detail(f"- {identifier}: {title}", width=CONSOLE_WRAP_WIDTH - 6))
                remaining = len(workstreams) - MODEL_WORKSTREAM_PREVIEW_COUNT
                if remaining > 0:
                    lines.append(f"- +{remaining} more")
        active_milestone = payload.get("active_milestone")
        if isinstance(active_milestone, dict) and active_milestone.get("milestone_id"):
            lines.append(
                self._format_kv("stdout", "active_milestone", str(active_milestone.get("milestone_id", "")).strip())
            )
        updates = payload.get("workstream_updates")
        if isinstance(updates, list) and updates:
            lines.append(self._format_kv("stdout", "updates", f"{len(updates)} workstreams"))
            for update in updates[:MODEL_WORKSTREAM_PREVIEW_COUNT]:
                identifier = update.get("id", "?")
                status = update.get("status", "?")
                lines.append(f"- {identifier}: {status}")
        milestone_progress = payload.get("milestone_progress")
        if isinstance(milestone_progress, dict):
            criteria_met = milestone_progress.get("criteria_met") or []
            criteria_remaining = milestone_progress.get("criteria_remaining") or []
            lines.append(
                self._format_kv(
                    "stdout",
                    "milestone_progress",
                    f"met={len(criteria_met)} remaining={len(criteria_remaining)}",
                )
            )
        gaps = payload.get("remaining_gaps")
        if isinstance(gaps, list):
            lines.append(self._format_kv("stdout", "remaining_gaps", str(len(gaps))))
            for gap in gaps[:MODEL_GAP_PREVIEW_COUNT]:
                lines.extend(self._wrap_detail(f"- {self.cap_console_text(' '.join(str(gap).split()), limit=72)}", width=CONSOLE_WRAP_WIDTH - 6))
            remaining = len(gaps) - MODEL_GAP_PREVIEW_COUNT
            if remaining > 0:
                lines.append(f"- +{remaining} more")
        validation = payload.get("validation_completed")
        if isinstance(validation, list) and validation:
            lines.append(self._format_kv("stdout", "validation", ", ".join(map(str, validation[:4]))))
        return lines or [self._format_kv("stdout", "status", "no structured details")]

    def _render_full_model_payload_lines(self, payload: dict[str, Any]) -> list[str]:
        lines: list[str] = []
        scalar_keys = ("status", "summary", "next_step", "gate_reasoning", "broadening_rationale")
        for key in scalar_keys:
            if isinstance(payload.get(key), str) and payload[key].strip():
                lines.extend(
                    self._wrap_detail(
                        self._format_kv("stdout", key, " ".join(payload[key].split())),
                        width=CONSOLE_WRAP_WIDTH - 4,
                    )
                )
        program_board = payload.get("program_board")
        if not isinstance(program_board, dict) and isinstance(payload.get("charter"), dict):
            program_board = legacy_program_board_from_charter(payload.get("charter"))
        if isinstance(program_board, dict):
            goal = program_board.get("goal")
            if isinstance(goal, str) and goal.strip():
                lines.extend(
                    self._wrap_detail(
                        self._format_kv("stdout", "goal", " ".join(goal.split())),
                        width=CONSOLE_WRAP_WIDTH - 4,
                    )
                )
            lines.extend(self._render_list_section("success", program_board.get("success_criteria") or []))
            lines.extend(
                self._render_list_section(
                    "milestones",
                    [
                        f"{milestone.get('id', '?')}: {milestone.get('title', '')}"
                        for milestone in program_board.get("milestones") or []
                    ],
                )
            )
            workstreams = [
                workstream
                for milestone in program_board.get("milestones") or []
                for workstream in milestone.get("workstreams") or []
            ]
            lines.extend(self._render_workstream_section(workstreams))
            lines.extend(self._render_list_section("validation_categories", program_board.get("validation_categories") or []))
            lines.extend(self._render_list_section("deferrals", program_board.get("explicit_deferrals") or []))
        active_milestone = payload.get("active_milestone")
        if isinstance(active_milestone, dict):
            lines.extend(
                self._wrap_detail(
                    self._format_kv("stdout", "active_milestone", str(active_milestone.get("milestone_id", ""))),
                    width=CONSOLE_WRAP_WIDTH - 4,
                )
            )
        updates = payload.get("workstream_updates")
        if isinstance(updates, list) and updates:
            lines.append(self._format_kv("stdout", "updates", f"{len(updates)} workstreams"))
            for update in updates:
                identifier = update.get("id", "?")
                status = update.get("status", "?")
                evidence_count = len(update.get("evidence") or [])
                detail = f"- {identifier}: {status}"
                if evidence_count:
                    detail += f" | evidence={evidence_count}"
                lines.extend(self._wrap_detail(detail, width=CONSOLE_WRAP_WIDTH - 6))
        milestone_progress = payload.get("milestone_progress")
        if isinstance(milestone_progress, dict):
            lines.extend(self._render_list_section("criteria_met", milestone_progress.get("criteria_met") or []))
            lines.extend(self._render_list_section("criteria_remaining", milestone_progress.get("criteria_remaining") or []))
        lines.extend(self._render_list_section("remaining_gaps", payload.get("remaining_gaps") or []))
        lines.extend(self._render_list_section("validation_completed", payload.get("validation_completed") or []))
        lines.extend(self._render_list_section("evidence", payload.get("evidence") or []))
        return lines or [self._format_kv("stdout", "status", "no structured details")]

    def _render_list_section(self, key: str, values: list[Any]) -> list[str]:
        rendered_values = [" ".join(str(value).split()) for value in values if str(value).strip()]
        if not rendered_values:
            return []
        lines = [self._format_kv("stdout", key, f"{len(rendered_values)} item(s)")]
        for value in rendered_values:
            lines.extend(self._wrap_detail(f"- {value}", width=CONSOLE_WRAP_WIDTH - 6))
        return lines

    def _render_workstream_section(self, workstreams: list[dict[str, Any]]) -> list[str]:
        if not workstreams:
            return []
        lines = [self._format_kv("stdout", "workstreams", f"{len(workstreams)} planned")]
        for workstream in workstreams:
            identifier = workstream.get("id", "?")
            title = " ".join(str(workstream.get("title", "")).split()) or "(untitled)"
            lines.extend(self._wrap_detail(f"- {identifier}: {title}", width=CONSOLE_WRAP_WIDTH - 6))
            if isinstance(workstream.get("goal"), str) and workstream["goal"].strip():
                lines.extend(
                    self._wrap_detail(
                        f"  goal: {' '.join(workstream['goal'].split())}",
                        width=CONSOLE_WRAP_WIDTH - 6,
                    )
                )
            adjacent = [str(value).strip() for value in workstream.get("required_adjacent_surfaces") or [] if str(value).strip()]
            if adjacent:
                lines.extend(self._wrap_detail(f"  adjacent: {', '.join(adjacent)}", width=CONSOLE_WRAP_WIDTH - 6))
            validation = [str(value).strip() for value in workstream.get("validation") or [] if str(value).strip()]
            if validation:
                lines.extend(self._wrap_detail(f"  validation: {', '.join(validation)}", width=CONSOLE_WRAP_WIDTH - 6))
            status = workstream.get("status")
            if isinstance(status, str) and status.strip():
                lines.extend(self._wrap_detail(f"  status: {status}", width=CONSOLE_WRAP_WIDTH - 6))
        return lines

    def _render_command_trace_lines(self, trace_rows: list[dict[str, Any]]) -> list[str]:
        lines = [self._format_kv("stdout", "commands", f"{len(trace_rows)} completed")]
        for row in trace_rows:
            lines.extend(self._wrap_detail(f"- {self.render_command_summary(row)}", width=CONSOLE_WRAP_WIDTH - 6))
        return lines

    def render_command_summary(self, row: dict[str, Any], *, include_pid: bool = False) -> str:
        action = " ".join(str(row.get("action", "exec")).split()) or "exec"
        target = " ".join(str(row.get("target", "")).split())
        if not target:
            target = truncate_label(" ".join(str(row.get("command", "")).split()), limit=120)
        if not target:
            target = "command"
        detail_parts = [f"{action} {target}".strip()]
        exit_code = row.get("exit_code")
        if isinstance(exit_code, int) and exit_code != 0:
            detail_parts.append(f"exit={exit_code}")
        output_chars = row.get("output_chars")
        if isinstance(output_chars, int):
            detail_parts.append(f"output={output_chars} chars")
        duration_ms = row.get("duration_ms")
        if isinstance(duration_ms, int) and duration_ms > 0:
            detail_parts.append(f"duration={duration_ms}ms")
        process_id = row.get("process_id")
        if include_pid and process_id:
            detail_parts.append(f"pid={process_id}")
        return " | ".join(detail_parts)

    def _render_trace_lines(self, payload: dict[str, Any]) -> list[str]:
        lines: list[str] = []
        for key in sorted(payload.keys()):
            rendered = self._summarize_value(payload[key])
            lines.extend(
                self._wrap_detail(
                    self._format_kv("stderr", key, self.cap_console_text(rendered)),
                    width=CONSOLE_WRAP_WIDTH - 4,
                )
            )
        return lines or [self._format_kv("stderr", "detail", "empty payload")]

    def _summarize_value(self, value: Any) -> str:
        if isinstance(value, (str, int, float, bool)) or value is None:
            return str(value)
        if isinstance(value, list):
            preview = ", ".join(self.cap_console_text(self.stringify(item), limit=48) for item in value[:3])
            suffix = "" if len(value) <= 3 else f", +{len(value) - 3} more"
            return f"[{preview}{suffix}]"
        if isinstance(value, dict):
            preview = []
            for key in sorted(value.keys())[:4]:
                preview.append(f"{key}={self.cap_console_text(self.stringify(value[key]), limit=40)}")
            suffix = "" if len(value) <= 4 else f", +{len(value) - 4} more"
            return "{" + ", ".join(preview) + suffix + "}"
        return self.stringify(value)


@dataclass
class SessionContext:
    session_id: str
    session_dir: Path
    session: dict[str, Any]
    task: dict[str, Any]
    profile: dict[str, Any]
    state: dict[str, Any]
    charter_record: dict[str, Any] | None
    completion_record: dict[str, Any]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def utc_timestamp() -> str:
    return utc_now().isoformat(timespec="milliseconds").replace("+00:00", "Z")


def stamped_id(value: datetime | None = None, uid: str | None = None) -> str:
    moment = value or utc_now()
    token = uid or secrets.token_hex(6)
    return moment.strftime("%Y%m%dT%H%M%S") + f"{moment.microsecond // 1000:03d}Z_{token}"


def new_session_id(value: datetime | None = None, uid: str | None = None) -> str:
    return stamped_id(value, uid)


def new_run_id(value: datetime | None = None, uid: str | None = None) -> str:
    return stamped_id(value, uid)


def deep_copy_json(value: Any) -> Any:
    return json.loads(json.dumps(value))


def merge_missing_keys(value: Any, defaults: Any) -> Any:
    if isinstance(defaults, dict):
        result = deep_copy_json(value) if isinstance(value, dict) else {}
        for key, default_value in defaults.items():
            if key not in result:
                result[key] = deep_copy_json(default_value)
            else:
                result[key] = merge_missing_keys(result[key], default_value)
        return result
    if isinstance(defaults, list):
        return deep_copy_json(value) if isinstance(value, list) else deep_copy_json(defaults)
    if value in {None, ""}:
        return deep_copy_json(defaults)
    return value


def semver(value: str) -> bool:
    return bool(re.match(r"^\d+\.\d+\.\d+$", value))


def default_research_payload() -> dict[str, Any]:
    return {
        "status": "blocked",
        "search_strategy": "Compatibility fallback for legacy Ralph session output.",
        "findings": ["Legacy planning output did not record mandatory web research."],
        "sources": [
            {
                "title": "Legacy session artifact",
                "url": "local://legacy-session",
                "source_type": "secondary",
                "used_for": "Compatibility fallback",
            }
        ],
        "open_questions": ["Refresh research under the current Ralph contract before executing again."],
    }


def default_tranche_payload(charter: dict[str, Any] | None = None) -> dict[str, Any]:
    workstreams = (charter or {}).get("workstreams") or []
    active_ids = [entry.get("id", "") for entry in workstreams if entry.get("status") == "planned"][:5]
    if not active_ids:
        active_ids = [entry.get("id", "") for entry in workstreams[:1] if entry.get("id")]
    surfaces: list[str] = []
    for entry in workstreams:
        if entry.get("id") not in active_ids:
            continue
        for surface in entry.get("required_adjacent_surfaces") or []:
            if surface and surface not in surfaces:
                surfaces.append(surface)
        if len(surfaces) >= 5:
            break
    if not surfaces:
        surfaces = ["docs/"]
    validation = []
    for entry in workstreams:
        if entry.get("id") not in active_ids:
            continue
        for item in entry.get("validation") or []:
            if item and item not in validation:
                validation.append(item)
    if not validation:
        validation = ["review the tranche result against the current charter"]
    return {
        "batch_id": "legacy-tranche",
        "milestone_id": "legacy-milestone",
        "workstream_ids": active_ids or ["legacy-workstream"],
        "target_files": surfaces,
        "intended_outcome": "Refresh the legacy charter under the current bounded-tranche contract.",
        "validation": validation,
    }


def default_verification_payload() -> dict[str, Any]:
    return {
        "status": "not_needed",
        "scope": "Legacy execution output did not include the mandatory verification block.",
        "findings": ["Refresh verification under the current Ralph contract before claiming completion."],
        "sources": [],
    }


def default_quality_claims_payload() -> dict[str, Any]:
    return {
        "tranche_followed": False,
        "user_facing_outcome": "Legacy execution output did not record tranche adherence.",
        "avoided_meta_artifacts": False,
        "repeated_heading_risk": "unknown",
    }


def default_program_memory_payload(started_at: str = "") -> dict[str, Any]:
    return {
        "goal": "",
        "milestones": [],
        "active_milestone_id": "",
        "updated_at": started_at,
    }


def default_research_memory_payload(started_at: str = "") -> dict[str, Any]:
    return {
        "search_strategy": "",
        "open_questions": [],
        "last_refreshed_at": started_at,
    }


def default_session_state_payload(session_id: str = "", started_at: str = "") -> dict[str, Any]:
    return {
        "session_id": session_id,
        "thread_id": "",
        "current_turn_id": "",
        "model": "",
        "phase": "planning",
        "status": "active",
        "iteration": 0,
        "same_tranche_repair_count": 0,
        "consecutive_replans": 0,
        "consecutive_low_novelty_iterations": 0,
        "seed_confirmed": False,
        "charter_version": 0,
        "active_milestone_id": "",
        "milestone_iteration_count": 0,
        "pending_feedback": "",
        "completion_rejections": [],
        "iteration_repo_baseline": [],
        "iteration_repo_after": [],
        "program_memory": default_program_memory_payload(started_at),
        "research_memory": default_research_memory_payload(started_at),
        "execution_memory": [],
        "skill_memory": [],
        "evidence_registry": [],
        "checkpoint_summaries": [],
        "worker_manifests": [],
        "started_at": started_at,
        "updated_at": started_at,
    }


def legacy_program_board_from_charter(charter: dict[str, Any] | None) -> dict[str, Any]:
    workstreams = (charter or {}).get("workstreams") or []
    return {
        "goal": (charter or {}).get("goal", ""),
        "milestones": [
            {
                "id": "legacy-milestone",
                "title": "Legacy milestone",
                "objective": (charter or {}).get("goal", "Refresh the legacy plan."),
                "acceptance_criteria": (charter or {}).get("success_criteria", []) or ["Refresh the milestone plan."],
                "dependencies": [],
                "evidence_requirements": (charter or {}).get("validation_categories", []),
                "status": "active",
                "workstreams": workstreams or [
                    {
                        "id": "legacy-workstream",
                        "title": "Legacy workstream",
                        "goal": "Refresh the legacy workstream plan.",
                        "required_adjacent_surfaces": ["docs/"],
                        "validation": ["Refresh the tranche plan."],
                        "status": "planned",
                    }
                ],
            }
        ],
        "success_criteria": (charter or {}).get("success_criteria", []) or ["Refresh the legacy plan."],
        "validation_categories": (charter or {}).get("validation_categories", []) or ["review"],
        "explicit_deferrals": (charter or {}).get("explicit_deferrals", []),
    }


def default_active_milestone_payload(program_board: dict[str, Any] | None = None) -> dict[str, Any]:
    milestones = (program_board or {}).get("milestones") or []
    milestone = milestones[0] if milestones else {}
    target_files: list[str] = []
    for workstream in milestone.get("workstreams") or []:
        for surface in workstream.get("required_adjacent_surfaces") or []:
            if surface and surface not in target_files:
                target_files.append(surface)
    validation: list[str] = []
    for workstream in milestone.get("workstreams") or []:
        for item in workstream.get("validation") or []:
            if item and item not in validation:
                validation.append(item)
    return {
        "milestone_id": milestone.get("id", "legacy-milestone"),
        "rationale": milestone.get("objective", "Refresh the active milestone plan."),
        "success_checkpoint": ((milestone.get("acceptance_criteria") or ["Refresh the milestone plan."])[0]),
        "evidence_focus": milestone.get("evidence_requirements", []),
        "target_files": target_files or ["docs/"],
        "validation": validation or ["Review the milestone outcome."],
    }


def charter_from_program_board(program_board: dict[str, Any] | None) -> dict[str, Any]:
    board = program_board or {}
    workstreams = [
        workstream
        for milestone in board.get("milestones", [])
        for workstream in milestone.get("workstreams", [])
    ]
    return {
        "goal": board.get("goal", ""),
        "success_criteria": board.get("success_criteria", []),
        "validation_categories": board.get("validation_categories", []),
        "explicit_deferrals": board.get("explicit_deferrals", []),
        "workstreams": workstreams,
    }


def read_json_object(path: Path, label: str) -> dict[str, Any]:
    if not path.exists():
        raise RalphError(f"{label} not found: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RalphError(f"{label} is not valid JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise RalphError(f"{label} must be a JSON object: {path}")
    return payload


def default_profile_baseline() -> dict[str, Any]:
    global _DEFAULT_PROFILE_CACHE
    if _DEFAULT_PROFILE_CACHE is None:
        payload = read_json_object(DEFAULT_PROFILE_PATH, "default profile")
        payload["schema_id"] = PROFILE_SCHEMA_ID
        payload["schema_version"] = VERSION
        legacy_model = str(payload.get("model", "")).strip()
        for section_name, default_mode, output_schema_id in (
            ("planning", "plan", PLANNING_OUTPUT_SCHEMA_ID),
            ("evaluation", "default", EVALUATION_OUTPUT_SCHEMA_ID),
            ("execution", "default", EXECUTION_OUTPUT_SCHEMA_ID),
        ):
            section = payload.setdefault(section_name, {})
            if legacy_model and not section.get("model"):
                section["model"] = legacy_model
            section.setdefault("mode", default_mode)
            section.setdefault("output_schema_id", output_schema_id)
        payload.setdefault(
            "loop_policy",
            {
                "same_tranche_retry_limit": 2,
                "max_consecutive_replans": 3,
                "planning_max_prompt_chars": 0,
                "execution_max_prompt_chars": payload.get("execution", {}).get("max_prompt_chars", 0),
                "compact_history_after_chars": 12000,
                "require_iteration_repo_baseline": True,
                "max_consecutive_low_novelty_iterations": 2,
            },
        )
        memory_policy = payload.setdefault("memory_policy", {})
        memory_policy.setdefault("max_execution_memory_entries", 8)
        memory_policy.setdefault("max_skill_memory_entries", 8)
        memory_policy.setdefault("max_checkpoint_summaries", 8)
        memory_policy.setdefault("max_evidence_registry_entries", 32)
        memory_policy.setdefault("max_worker_manifests", 8)
        quality_policy = payload.setdefault("quality_policy", {})
        quality_policy.setdefault("progress_checkpoint_mode", "require_confirmation")
        _DEFAULT_PROFILE_CACHE = deep_copy_json(payload)
    return deep_copy_json(_DEFAULT_PROFILE_CACHE)


def normalize_payload_for_schema(schema_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    normalized = deep_copy_json(payload)
    if schema_id == PROFILE_SCHEMA_ID:
        legacy_model = str(normalized.get("model", "")).strip()
        missing_phase_models = {
            section_name: not (
                isinstance(normalized.get(section_name), dict)
                and str(normalized.get(section_name, {}).get("model", "")).strip()
            )
            for section_name in ("planning", "evaluation", "execution")
        }
        baseline = default_profile_baseline()
        normalized = merge_missing_keys(normalized, baseline)
        if legacy_model:
            for section_name in ("planning", "evaluation", "execution"):
                section = normalized.get(section_name)
                if isinstance(section, dict) and missing_phase_models.get(section_name):
                    section["model"] = legacy_model
        loop_policy = normalized.get("loop_policy")
        if isinstance(loop_policy, dict):
            if not isinstance(loop_policy.get("execution_max_prompt_chars"), int):
                loop_policy["execution_max_prompt_chars"] = normalized.get("execution", {}).get("max_prompt_chars", 0)
        worker_policy = normalized.get("worker_policy")
        if isinstance(worker_policy, dict):
            allowed_roles = worker_policy.get("allowed_roles")
            if isinstance(allowed_roles, list):
                worker_policy["allowed_roles"] = [
                    role
                    for role in allowed_roles
                    if role in {"research", "read_only_repo", "evaluator_vote"}
                ] or ["research"]
        normalized["schema_id"] = PROFILE_SCHEMA_ID
        normalized["schema_version"] = baseline["schema_version"]
        return normalized
    if schema_id == SESSION_STATE_SCHEMA_ID:
        session_id = str(normalized.get("session_id", "")).strip()
        started_at = str(normalized.get("started_at", "")).strip()
        normalized = merge_missing_keys(normalized, default_session_state_payload(session_id, started_at))
        execution_memory = normalized.get("execution_memory")
        if isinstance(execution_memory, list):
            for entry in execution_memory:
                if not isinstance(entry, dict):
                    continue
                if "acceptance_progress_score" not in entry and "closure_score" in entry:
                    entry["acceptance_progress_score"] = entry.get("closure_score")
                entry.pop("closure_score", None)
        normalized["schema_id"] = SESSION_STATE_SCHEMA_ID
        normalized["schema_version"] = VERSION
        return normalized
    if schema_id == CHARTER_SCHEMA_ID:
        planning_result = normalized.get("planning_result")
        if isinstance(planning_result, dict):
            planning_result.setdefault("research", default_research_payload())
            if "program_board" not in planning_result and isinstance(planning_result.get("charter"), dict):
                planning_result["program_board"] = legacy_program_board_from_charter(planning_result.get("charter"))
            planning_result.setdefault("active_milestone", default_active_milestone_payload(planning_result.get("program_board")))
            planning_result.setdefault(
                "current_tranche",
                default_tranche_payload(
                    planning_result.get("charter")
                    or {
                        "workstreams": [
                            workstream
                            for milestone in (planning_result.get("program_board") or {}).get("milestones", [])
                            for workstream in milestone.get("workstreams", [])
                        ]
                    }
                ),
            )
        return normalized
    if schema_id == CHARTER_HISTORY_LINE_SCHEMA_ID:
        planning_result = normalized.get("planning_result")
        if isinstance(planning_result, dict):
            planning_result.setdefault("research", default_research_payload())
            if "program_board" not in planning_result and isinstance(planning_result.get("charter"), dict):
                planning_result["program_board"] = legacy_program_board_from_charter(planning_result.get("charter"))
            planning_result.setdefault("active_milestone", default_active_milestone_payload(planning_result.get("program_board")))
            planning_result.setdefault(
                "current_tranche",
                default_tranche_payload(
                    planning_result.get("charter")
                    or {
                        "workstreams": [
                            workstream
                            for milestone in (planning_result.get("program_board") or {}).get("milestones", [])
                            for workstream in milestone.get("workstreams", [])
                        ]
                    }
                ),
            )
        return normalized
    if schema_id == COMPLETION_SCHEMA_ID:
        last_result = normalized.get("last_result")
        if isinstance(last_result, dict) and last_result:
            last_result.setdefault("verification", default_verification_payload())
            last_result.setdefault("touched_files", ["legacy-output"])
            last_result.setdefault("created_files", [])
            last_result.setdefault("off_tranche_justifications", [])
            last_result.setdefault("quality_claims", default_quality_claims_payload())
            last_result.setdefault(
                "milestone_progress",
                {
                    "milestone_id": "legacy-milestone",
                    "criteria_met": [],
                    "criteria_remaining": ["Refresh the milestone progress block."],
                    "novelty_notes": ["Legacy output did not record novelty assessment."],
                    "completion_notes": ["Refresh the milestone completion assessment."],
                },
            )
            milestone_progress = last_result.get("milestone_progress")
            if isinstance(milestone_progress, dict):
                if "completion_notes" not in milestone_progress and "closure_notes" in milestone_progress:
                    milestone_progress["completion_notes"] = milestone_progress.get("closure_notes")
                milestone_progress.pop("closure_notes", None)
            last_result.setdefault("acceptance_artifacts", [])
            last_result.setdefault("evidence_updates", [])
            last_result.setdefault("next_tranche_recommendation", last_result.get("next_step", "Refresh the tranche plan."))
        return normalized
    return normalized


def adjacent_schema_path(path: Path) -> Path:
    return path.with_name(f"{path.name}.schema.json")


def truncate_label(text: str, limit: int = 48) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3] + "..."


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ralph-codex",
        description="Universal, session-driven Ralph controller for Codex.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose trace output and persist full wire diagnostics in events.jsonl.",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-m", "--message", help="Start a new session from inline message text.")
    group.add_argument("-f", "--file", help="Start a new session from a message file.")
    group.add_argument(
        "-s",
        "--sessions",
        nargs="?",
        const="",
        metavar="COUNT",
        help="List run history rows from sessions.log.jsonl. Optionally limit to the latest COUNT rows.",
    )
    group.add_argument(
        "-r",
        "--resume",
        nargs="?",
        const="",
        metavar="SESSION",
        help="Resume the latest resumable session, or the listed session id/index.",
    )
    parser.add_argument(
        "-p",
        "--profile",
        help="Use a custom JSON profile. Only valid with --message or --file.",
    )
    return parser


def parse_command(argv: list[str]) -> tuple[argparse.ArgumentParser, Command]:
    parser = build_parser()
    if not argv:
        return parser, Command(kind="help")
    namespace = parser.parse_args(argv)
    if namespace.profile and namespace.message is None and namespace.file is None:
        parser.error("--profile can only be used with --message or --file")
    if namespace.message is not None:
        return parser, Command(
            kind="message",
            value=namespace.message,
            profile_path=path_or_none(namespace.profile),
            verbose=namespace.verbose,
        )
    if namespace.file is not None:
        return parser, Command(
            kind="file",
            value=namespace.file,
            profile_path=path_or_none(namespace.profile),
            verbose=namespace.verbose,
        )
    if namespace.sessions is not None:
        limit = parse_positive_integer(parser, namespace.sessions, "--sessions") if namespace.sessions else None
        return parser, Command(kind="sessions", value=str(limit) if limit is not None else None, verbose=namespace.verbose)
    if namespace.resume is not None:
        return parser, Command(kind="resume", value=namespace.resume or None, verbose=namespace.verbose)
    return parser, Command(kind="help", verbose=namespace.verbose)


def path_or_none(value: str | None) -> Path | None:
    if not value:
        return None
    return Path(value).expanduser().resolve()


def parse_positive_integer(parser: argparse.ArgumentParser, value: str, flag_name: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        parser.error(f"{flag_name} expects a positive integer count")
        raise AssertionError("unreachable") from exc
    if parsed < 1:
        parser.error(f"{flag_name} expects a positive integer count")
    return parsed


def validate_subset(schema: dict[str, Any], payload: Any, path: str = "$") -> None:
    expected_type = schema.get("type")
    if expected_type == "object":
        if not isinstance(payload, dict):
            raise RalphError(f"{path} must be an object")
        required = schema.get("required", [])
        for key in required:
            if key not in payload:
                raise RalphError(f"{path}.{key} is required")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in payload:
                if key not in properties:
                    raise RalphError(f"{path}.{key} is not allowed")
        for key, value in payload.items():
            if key in properties:
                validate_subset(properties[key], value, f"{path}.{key}")
        return
    if expected_type == "array":
        if not isinstance(payload, list):
            raise RalphError(f"{path} must be an array")
        min_items = schema.get("minItems")
        if min_items is not None and len(payload) < min_items:
            raise RalphError(f"{path} must contain at least {min_items} items")
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(payload):
                validate_subset(item_schema, item, f"{path}[{index}]")
        return
    if expected_type == "string":
        if not isinstance(payload, str):
            raise RalphError(f"{path} must be a string")
        min_length = schema.get("minLength")
        if min_length is not None and len(payload) < min_length:
            raise RalphError(f"{path} must be at least {min_length} chars")
        pattern = schema.get("pattern")
        if pattern and not re.match(pattern, payload):
            raise RalphError(f"{path} does not match {pattern}")
        if "enum" in schema and payload not in schema["enum"]:
            raise RalphError(f"{path} must be one of {schema['enum']}")
        return
    if expected_type == "integer":
        if not isinstance(payload, int) or isinstance(payload, bool):
            raise RalphError(f"{path} must be an integer")
        minimum = schema.get("minimum")
        if minimum is not None and payload < minimum:
            raise RalphError(f"{path} must be >= {minimum}")
        if "enum" in schema and payload not in schema["enum"]:
            raise RalphError(f"{path} must be one of {schema['enum']}")
        return
    if expected_type == "boolean":
        if not isinstance(payload, bool):
            raise RalphError(f"{path} must be a boolean")
        return
    if expected_type == "number":
        if not isinstance(payload, (int, float)) or isinstance(payload, bool):
            raise RalphError(f"{path} must be a number")
        minimum = schema.get("minimum")
        if minimum is not None and payload < minimum:
            raise RalphError(f"{path} must be >= {minimum}")
        return
    if expected_type == "null":
        if payload is not None:
            raise RalphError(f"{path} must be null")
        return
    if "enum" in schema and payload not in schema["enum"]:
        raise RalphError(f"{path} must be one of {schema['enum']}")


class SchemaCatalog:
    def __init__(self, schema_files: dict[str, Path]):
        self.schema_files = schema_files
        self._cache: dict[str, dict[str, Any]] = {}

    def load(self, schema_id: str) -> dict[str, Any]:
        if schema_id not in self._cache:
            path = self.schema_files[schema_id]
            schema = json.loads(path.read_text(encoding="utf-8"))
            if schema.get("schema_id") != schema_id:
                raise RalphError(f"schema id mismatch in {path}")
            if not semver(schema.get("schema_version", "")):
                raise RalphError(f"invalid schema version in {path}")
            self._cache[schema_id] = schema
        return self._cache[schema_id]

    def validate(self, schema_id: str, payload: dict[str, Any]) -> None:
        validate_subset(self.load(schema_id), payload)

    def model_schema(self, schema_id: str) -> dict[str, Any]:
        schema = deep_copy_json(self.load(schema_id))
        schema.pop("schema_id", None)
        schema.pop("schema_version", None)
        return schema

    def copy_adjacent(self, schema_id: str, artifact_path: Path) -> None:
        adjacent_path = adjacent_schema_path(artifact_path)
        content = json.dumps(self.load(schema_id), indent=2) + "\n"
        if adjacent_path.exists() and adjacent_path.read_text(encoding="utf-8") == content:
            return
        adjacent_path.write_text(content, encoding="utf-8")


def load_profile(schema_catalog: SchemaCatalog, path: Path | None) -> dict[str, Any]:
    profile_path = DEFAULT_PROFILE_PATH if path is None else path
    label = "default profile" if path is None else "profile"
    profile = read_json_object(profile_path, label)
    profile = normalize_payload_for_schema(PROFILE_SCHEMA_ID, profile)
    schema_catalog.validate(PROFILE_SCHEMA_ID, profile)
    return profile


class SessionStore:
    def __init__(self, root: Path, schema_catalog: SchemaCatalog):
        self.root = root
        self.sessions_dir = self.root / "sessions"
        self.controller_state_path = self.root / "controller-state.json"
        self.sessions_log_path = self.root / "sessions.log.jsonl"
        self.schema_catalog = schema_catalog
        self._event_fingerprint_cache: dict[str, str | None] = {}
        self.root.mkdir(parents=True, exist_ok=True)
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.ensure_top_level_files()

    def ensure_top_level_files(self) -> None:
        if not self.controller_state_path.exists():
            self.write_json(
                self.controller_state_path,
                CONTROLLER_STATE_SCHEMA_ID,
                {
                    "current_session_id": "",
                    "current_run_id": "",
                    "updated_at": utc_timestamp(),
                },
            )
        self.ensure_jsonl(self.sessions_log_path, RUN_HISTORY_LINE_SCHEMA_ID)

    def write_json(self, path: Path, schema_id: str, payload: dict[str, Any]) -> None:
        schema = self.schema_catalog.load(schema_id)
        document = {
            "schema_id": schema["schema_id"],
            "schema_version": schema["schema_version"],
            **payload,
        }
        document = normalize_payload_for_schema(schema_id, document)
        self.schema_catalog.validate(schema_id, document)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
        self.schema_catalog.copy_adjacent(schema_id, path)

    def read_json(self, path: Path, schema_id: str) -> dict[str, Any]:
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload = normalize_payload_for_schema(schema_id, payload)
        self.schema_catalog.validate(schema_id, payload)
        return payload

    def ensure_jsonl(self, path: Path, schema_id: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text("", encoding="utf-8")
        self.schema_catalog.copy_adjacent(schema_id, path)

    def append_jsonl(self, path: Path, schema_id: str, payload: dict[str, Any]) -> None:
        schema = self.schema_catalog.load(schema_id)
        document = {
            "schema_id": schema["schema_id"],
            "schema_version": schema["schema_version"],
            **payload,
        }
        document = normalize_payload_for_schema(schema_id, document)
        self.schema_catalog.validate(schema_id, document)
        self.ensure_jsonl(path, schema_id)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(document, sort_keys=True) + "\n")

    def read_jsonl(self, path: Path, schema_id: str) -> list[dict[str, Any]]:
        if not path.exists():
            return []
        records = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            payload = json.loads(line)
            payload = normalize_payload_for_schema(schema_id, payload)
            self.schema_catalog.validate(schema_id, payload)
            records.append(payload)
        return records

    def update_controller_state(self, current_session_id: str, current_run_id: str) -> None:
        self.write_json(
            self.controller_state_path,
            CONTROLLER_STATE_SCHEMA_ID,
            {
                "current_session_id": current_session_id,
                "current_run_id": current_run_id,
                "updated_at": utc_timestamp(),
            },
        )

    def create_session(self, workdir: Path, task: dict[str, Any], profile: dict[str, Any]) -> SessionContext:
        session_id = new_session_id()
        session_dir = self.sessions_dir / session_id
        session_dir.mkdir(parents=True, exist_ok=False)
        created_at = utc_timestamp()
        session = {
            "session_id": session_id,
            "created_at": created_at,
            "workdir": str(workdir),
            "profile_name": profile["profile_name"],
        }
        task_record = {
            "session_id": session_id,
            "created_at": created_at,
            "message_source_kind": task["message_source_kind"],
            "message_source_label": task["message_source_label"],
            "message_text": task["message_text"],
        }
        state = default_session_state_payload(session_id, created_at)
        completion = {
            "session_id": session_id,
            "accepted": False,
            "last_result": {},
            "last_reason": "",
            "rejections": [],
            "updated_at": created_at,
        }
        self.write_json(session_dir / "session.json", SESSION_SCHEMA_ID, session)
        self.write_json(session_dir / "task.json", TASK_SCHEMA_ID, task_record)
        self.write_json(session_dir / "profile.json", PROFILE_SCHEMA_ID, profile)
        self.write_json(session_dir / "session-state.json", SESSION_STATE_SCHEMA_ID, state)
        self.write_json(session_dir / "completion.json", COMPLETION_SCHEMA_ID, completion)
        self.ensure_jsonl(session_dir / "charter-history.jsonl", CHARTER_HISTORY_LINE_SCHEMA_ID)
        self.ensure_jsonl(session_dir / "turns.jsonl", TURN_LOG_LINE_SCHEMA_ID)
        self.ensure_jsonl(session_dir / "server-requests.jsonl", SERVER_REQUEST_LOG_LINE_SCHEMA_ID)
        self.ensure_jsonl(session_dir / "events.jsonl", EVENT_LOG_LINE_SCHEMA_ID)
        self.update_controller_state(session_id, "")
        return SessionContext(session_id, session_dir, session, task_record, profile, state, None, completion)

    def load_session(self, session_id: str) -> SessionContext:
        session_dir = self.sessions_dir / session_id
        if not session_dir.exists():
            raise RalphError(f"session not found: {session_id}")
        session = self.read_json(session_dir / "session.json", SESSION_SCHEMA_ID)
        task = self.read_json(session_dir / "task.json", TASK_SCHEMA_ID)
        profile = self.read_json(session_dir / "profile.json", PROFILE_SCHEMA_ID)
        state = self.read_json(session_dir / "session-state.json", SESSION_STATE_SCHEMA_ID)
        completion = self.read_json(session_dir / "completion.json", COMPLETION_SCHEMA_ID)
        charter_path = session_dir / "charter.json"
        charter = self.read_json(charter_path, CHARTER_SCHEMA_ID) if charter_path.exists() else None
        return SessionContext(session_id, session_dir, session, task, profile, state, charter, completion)

    def iter_session_ids(self) -> list[str]:
        session_ids = [
            path.name
            for path in self.sessions_dir.iterdir()
            if path.is_dir() and SESSION_ID_RE.match(path.name)
        ]
        return sorted(session_ids)

    def latest_resumable_session_id(self) -> str | None:
        for session_id in reversed(self.iter_session_ids()):
            if self.session_status(session_id) == "resumable":
                return session_id
        return None

    def session_status(self, session_id: str) -> str:
        session_dir = self.sessions_dir / session_id
        if not session_dir.exists():
            return "missing"
        if (session_dir / "finished.json").exists():
            return "completed"
        return "resumable"

    def resolve_resume_target(self, target: str | None) -> SessionContext:
        if not target:
            session_id = self.latest_resumable_session_id()
            if not session_id:
                raise RalphError("no resumable sessions found")
            return self.load_session(session_id)
        if target.isdigit():
            index = int(target)
            if index < 1:
                raise RalphError("session listing index must be >= 1")
            rows = self.list_run_rows()
            if index > len(rows):
                raise RalphError(f"session listing index out of range: {index}")
            session_id = rows[index - 1]["session_id"]
        else:
            session_id = target
        status = self.session_status(session_id)
        if status == "missing":
            raise RalphError(f"session not found: {session_id}")
        if status == "completed":
            raise RalphError(f"session is completed and cannot be resumed: {session_id}")
        return self.load_session(session_id)

    def save_state(self, session: SessionContext) -> None:
        session.state["updated_at"] = utc_timestamp()
        self.write_json(session.session_dir / "session-state.json", SESSION_STATE_SCHEMA_ID, session.state)

    def save_charter(
        self,
        session: SessionContext,
        planning_result: dict[str, Any],
        confirmed: bool,
        review_state: str,
        operator_feedback: str = "",
    ) -> None:
        prior_record = session.charter_record
        if prior_record and prior_record.get("charter_version") != session.state["charter_version"]:
            self.update_charter_history_state(
                session,
                prior_record["charter_version"],
                review_state="superseded",
                confirmed=False,
                locked=False,
            )
        record = {
            "session_id": session.session_id,
            "charter_version": session.state["charter_version"],
            "locked": review_state == "approved",
            "confirmed": confirmed,
            "review_state": review_state,
            "operator_feedback": operator_feedback,
            "updated_at": utc_timestamp(),
            "planning_result": planning_result,
            "charter": charter_from_program_board(planning_result.get("program_board")),
        }
        self.write_json(session.session_dir / "charter.json", CHARTER_SCHEMA_ID, record)
        self.upsert_charter_history(session, record)
        session.charter_record = record

    def approve_charter(self, session: SessionContext) -> None:
        if not session.charter_record:
            raise RalphError("cannot approve a missing charter")
        session.charter_record["confirmed"] = True
        session.charter_record["locked"] = True
        session.charter_record["review_state"] = "approved"
        session.charter_record["updated_at"] = utc_timestamp()
        self.write_json(session.session_dir / "charter.json", CHARTER_SCHEMA_ID, session.charter_record)
        self.upsert_charter_history(session, session.charter_record)

    def save_completion(self, session: SessionContext, result: dict[str, Any], accepted: bool, reason: str) -> None:
        record = {
            "session_id": session.session_id,
            "accepted": accepted,
            "last_result": result,
            "last_reason": reason,
            "rejections": session.state["completion_rejections"],
            "updated_at": utc_timestamp(),
        }
        self.write_json(session.session_dir / "completion.json", COMPLETION_SCHEMA_ID, record)
        session.completion_record = record

    def finish(self, session: SessionContext, status: str, summary: str) -> None:
        record = {
            "session_id": session.session_id,
            "status": status,
            "summary": summary,
            "finished_at": utc_timestamp(),
            "iterations": session.state["iteration"],
        }
        self.write_json(session.session_dir / "finished.json", FINISHED_SCHEMA_ID, record)
        session.state["status"] = "finished"
        self.save_state(session)

    def mark_active(self, session: SessionContext) -> None:
        session.state["status"] = "active"
        self.save_state(session)

    def mark_aborted(self, session: SessionContext, reason: str) -> None:
        session.state["status"] = "aborted"
        session.state["current_turn_id"] = ""
        if session.charter_record and not session.state["seed_confirmed"]:
            session.state["phase"] = "planning_review"
        else:
            session.state["phase"] = "planning"
        self.save_state(session)
        self.save_completion(
            session,
            session.completion_record.get("last_result", {}),
            False,
            reason,
        )

    def append_event(self, session: SessionContext, event_type: str, payload: dict[str, Any]) -> None:
        fingerprint = self.event_fingerprint(event_type, payload)
        if self.last_event_fingerprint(session) == fingerprint:
            return
        self.append_jsonl(
            session.session_dir / "events.jsonl",
            EVENT_LOG_LINE_SCHEMA_ID,
            {
                "session_id": session.session_id,
                "ts": utc_timestamp(),
                "event_type": event_type,
                "payload": payload,
            },
        )
        self._event_fingerprint_cache[session.session_id] = fingerprint

    def append_turn(self, session: SessionContext, phase: str, turn_id: str, status: str, summary: str) -> None:
        self.append_jsonl(
            session.session_dir / "turns.jsonl",
            TURN_LOG_LINE_SCHEMA_ID,
            {
                "session_id": session.session_id,
                "ts": utc_timestamp(),
                "phase": phase,
                "turn_id": turn_id,
                "status": status,
                "summary": summary,
            },
        )

    def append_server_request(
        self,
        session: SessionContext,
        request_id: str | int,
        method: str,
        action: str,
        payload: dict[str, Any],
    ) -> None:
        self.append_jsonl(
            session.session_dir / "server-requests.jsonl",
            SERVER_REQUEST_LOG_LINE_SCHEMA_ID,
            {
                "session_id": session.session_id,
                "ts": utc_timestamp(),
                "request_id": str(request_id),
                "method": method,
                "action": action,
                "payload": payload,
            },
        )

    def append_run_history(
        self,
        session: SessionContext,
        run_id: str,
        event: str,
        invocation_mode: str,
        summary: str,
    ) -> None:
        self.append_jsonl(
            self.sessions_log_path,
            RUN_HISTORY_LINE_SCHEMA_ID,
            {
                "session_id": session.session_id,
                "run_id": run_id,
                "ts": utc_timestamp(),
                "event": event,
                "invocation_mode": invocation_mode,
                "message_source_kind": session.task["message_source_kind"],
                "message_source_label": session.task["message_source_label"],
                "summary": summary,
            },
        )

    def list_run_rows(self, limit: int | None = None) -> list[dict[str, Any]]:
        records = self.read_jsonl(self.sessions_log_path, RUN_HISTORY_LINE_SCHEMA_ID)
        runs: dict[str, dict[str, Any]] = {}
        order: list[str] = []
        for record in records:
            run_id = record["run_id"]
            if run_id not in runs:
                runs[run_id] = {
                    "index": len(order) + 1,
                    "session_id": record["session_id"],
                    "run_id": run_id,
                    "started_at": record["ts"],
                    "finished_at": "",
                    "invocation_mode": record["invocation_mode"],
                    "message_source_kind": record["message_source_kind"],
                    "message_source_label": record["message_source_label"],
                    "outcome": "running",
                    "summary": "",
                }
                order.append(run_id)
            row = runs[run_id]
            row["summary"] = record["summary"] or row["summary"]
            if record["event"] == "run_completed":
                row["finished_at"] = record["ts"]
                row["outcome"] = "completed"
            elif record["event"] == "run_aborted":
                row["finished_at"] = record["ts"]
                row["outcome"] = "aborted"
            elif record["event"] == "run_failed":
                row["finished_at"] = record["ts"]
                row["outcome"] = "failed"
        rows = []
        for run_id in order:
            row = runs[run_id]
            row["session_status"] = self.session_status(row["session_id"])
            rows.append(row)
        if limit is not None:
            rows = rows[-limit:]
        return rows

    def last_event_fingerprint(self, session: SessionContext) -> str | None:
        if session.session_id in self._event_fingerprint_cache:
            return self._event_fingerprint_cache[session.session_id]
        path = session.session_dir / "events.jsonl"
        if not path.exists():
            self._event_fingerprint_cache[session.session_id] = None
            return None
        last_record: dict[str, Any] | None = None
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                last_record = json.loads(line)
        if not last_record:
            self._event_fingerprint_cache[session.session_id] = None
            return None
        fingerprint = self.event_fingerprint(last_record["event_type"], last_record["payload"])
        self._event_fingerprint_cache[session.session_id] = fingerprint
        return fingerprint

    @staticmethod
    def event_fingerprint(event_type: str, payload: dict[str, Any]) -> str:
        normalized = {"event_type": event_type, "payload": payload}
        return json.dumps(normalized, sort_keys=True, separators=(",", ":"))

    def latest_turn(self, session: SessionContext) -> dict[str, Any] | None:
        turns = self.read_jsonl(session.session_dir / "turns.jsonl", TURN_LOG_LINE_SCHEMA_ID)
        if not turns:
            return None
        return turns[-1]

    def command_trace_for_turn(self, session: SessionContext, turn_id: str) -> list[dict[str, Any]]:
        events = self.read_jsonl(session.session_dir / "events.jsonl", EVENT_LOG_LINE_SCHEMA_ID)
        rows_by_call_id: dict[str, dict[str, Any]] = {}
        ordered_call_ids: list[str] = []
        anonymous_index = 0
        for event in events:
            if event.get("event_type") != "notification":
                continue
            payload = event.get("payload") or {}
            if payload.get("turn_id") != turn_id:
                continue
            if payload.get("method") != "item/completed":
                continue
            item = payload.get("item") or {}
            if item.get("type") != "commandExecution":
                continue
            call_id = item.get("id")
            if not isinstance(call_id, str) or not call_id:
                anonymous_index += 1
                call_id = f"anonymous-command-{anonymous_index}"
            if call_id not in rows_by_call_id:
                rows_by_call_id[call_id] = {
                    "call_id": call_id,
                    "command": "",
                    "action": "",
                    "target": "",
                    "output_chars": None,
                    "exit_code": None,
                    "duration_ms": None,
                    "process_id": "",
                }
                ordered_call_ids.append(call_id)
            row = rows_by_call_id[call_id]
            if isinstance(item.get("command"), str) and item["command"].strip():
                row["command"] = item["command"]
            if isinstance(item.get("primary_action"), str) and item["primary_action"].strip():
                row["action"] = item["primary_action"]
            if isinstance(item.get("primary_target"), str) and item["primary_target"].strip():
                row["target"] = item["primary_target"]
            output_chars = item.get("aggregated_output_chars")
            if not isinstance(output_chars, int):
                output_chars = item.get("output_chars")
            if isinstance(output_chars, int):
                row["output_chars"] = output_chars
            if isinstance(item.get("exitCode"), int):
                row["exit_code"] = item["exitCode"]
            if isinstance(item.get("durationMs"), int):
                row["duration_ms"] = item["durationMs"]
            if isinstance(item.get("processId"), str) and item["processId"].strip():
                row["process_id"] = item["processId"]
        return [rows_by_call_id[call_id] for call_id in ordered_call_ids]

    def charter_history_path(self, session: SessionContext) -> Path:
        return session.session_dir / "charter-history.jsonl"

    def read_charter_history(self, session: SessionContext) -> list[dict[str, Any]]:
        return self.read_jsonl(self.charter_history_path(session), CHARTER_HISTORY_LINE_SCHEMA_ID)

    def write_jsonl_records(self, path: Path, schema_id: str, payloads: list[dict[str, Any]]) -> None:
        schema = self.schema_catalog.load(schema_id)
        documents = []
        for payload in payloads:
            document = {
                "schema_id": schema["schema_id"],
                "schema_version": schema["schema_version"],
                **payload,
            }
            document = normalize_payload_for_schema(schema_id, document)
            self.schema_catalog.validate(schema_id, document)
            documents.append(document)
        self.ensure_jsonl(path, schema_id)
        rendered = "".join(json.dumps(document, sort_keys=True) + "\n" for document in documents)
        path.write_text(rendered, encoding="utf-8")

    def upsert_charter_history(self, session: SessionContext, record: dict[str, Any]) -> None:
        history = self.read_charter_history(session)
        payload = {
            "session_id": session.session_id,
            "ts": record["updated_at"],
            "charter_version": record["charter_version"],
            "review_state": record["review_state"],
            "confirmed": record["confirmed"],
            "locked": record["locked"],
            "operator_feedback": record.get("operator_feedback", ""),
            "planning_result": record["planning_result"],
            "charter": record["charter"],
        }
        for index, existing in enumerate(history):
            if existing["charter_version"] == record["charter_version"]:
                history[index] = payload
                break
        else:
            history.append(payload)
        self.write_jsonl_records(self.charter_history_path(session), CHARTER_HISTORY_LINE_SCHEMA_ID, history)

    def update_charter_history_state(
        self,
        session: SessionContext,
        charter_version: int,
        review_state: str,
        confirmed: bool,
        locked: bool,
    ) -> None:
        history = self.read_charter_history(session)
        changed = False
        for entry in history:
            if entry["charter_version"] != charter_version:
                continue
            entry["review_state"] = review_state
            entry["confirmed"] = confirmed
            entry["locked"] = locked
            entry["ts"] = utc_timestamp()
            changed = True
            break
        if changed:
            self.write_jsonl_records(self.charter_history_path(session), CHARTER_HISTORY_LINE_SCHEMA_ID, history)


class EventRecorder:
    def __init__(
        self,
        store: SessionStore,
        session: SessionContext,
        verbose: bool,
        reporter: TerminalReporter | None = None,
        stdout: Any = sys.stdout,
        stderr: Any = sys.stderr,
    ):
        self.store = store
        self.session = session
        self.verbose = verbose
        self.reporter = reporter or TerminalReporter(verbose=verbose, stdout=stdout, stderr=stderr)
        self._reported_command_updates: dict[str, str] = {}

    def append(self, event_type: str, payload: dict[str, Any]) -> None:
        self.store.append_event(self.session, event_type, payload)

    def trace(self, event_type: str, payload: dict[str, Any]) -> None:
        self.reporter.verbose_trace(event_type, payload)

    def record_run_config(self, run_id: str, invocation_mode: str, workdir: Path) -> None:
        payload = {
            "run_id": run_id,
            "invocation_mode": invocation_mode,
            "verbose": self.verbose,
            "workdir": str(workdir),
        }
        self.append("run-config", payload)
        self.trace("run-config", payload)

    def record_client_event(self, payload: dict[str, Any]) -> None:
        event_type = payload.get("type", "event")
        if event_type == "wire":
            if self.verbose:
                self.append("wire", payload)
                if not self.is_command_execution_wire(payload):
                    self.trace("wire", payload)
            return
        compact_payload = {key: value for key, value in payload.items() if key != "type"}
        self.append(event_type, compact_payload)
        self.trace(event_type, compact_payload)
        self.report_client_event(event_type, compact_payload)

    def record_rpc_request(self, request_id: str | int, method: str, params: dict[str, Any] | None) -> None:
        payload = {
            "request_id": str(request_id),
            "method": method,
            "params": self.summarize_request_params(method, params or {}),
        }
        self.append("rpc-request", payload)
        self.trace("rpc-request", payload)

    def record_rpc_response(self, request_id: str | int, method: str, response: dict[str, Any]) -> None:
        payload: dict[str, Any] = {"request_id": str(request_id), "method": method}
        if "error" in response:
            payload["error"] = self.summarize_error(response["error"])
        else:
            payload["result"] = self.summarize_response_result(method, response.get("result", {}))
        self.append("rpc-response", payload)
        self.trace("rpc-response", payload)
        if "error" in payload:
            message = payload["error"].get("message", "unknown error")
            self.reporter.event(f"{method} failed: {message}", tone="error")

    def record_notification(self, method: str | None, params: dict[str, Any]) -> None:
        payload = self.summarize_notification(method or "", params)
        if self.should_persist_notification(payload):
            self.append("notification", payload)
            if not self.is_command_execution_notification(payload):
                self.trace("notification", payload)
        self.report_notification(payload)

    def record_server_request(
        self,
        request_id: str | int | None,
        method: str,
        action: str,
        payload: dict[str, Any],
    ) -> None:
        record = {
            "request_id": "" if request_id is None else str(request_id),
            "method": method,
            "action": action,
            "payload": self.summarize_server_request_payload(method, action, payload),
        }
        self.append("server-request", record)
        self.trace("server-request", record)
        self.report_server_request(record)

    def report_client_event(self, event_type: str, payload: dict[str, Any]) -> None:
        if event_type == "stderr":
            line = self.cap_human_text(payload.get("line", ""))
            self.reporter.event(f"app-server stderr: {line}", tone="error")
            return
        if event_type == "stdout-parse-error":
            line = self.cap_human_text(payload.get("line", ""))
            self.reporter.event(f"app-server stdout parse error: {line}", tone="warn")
            return
        if event_type == "stream-closed":
            stream = payload.get("stream", "unknown")
            self.reporter.event(f"app-server stream closed: {stream}", tone="warn")
            return
        if event_type == "orphan-response":
            response_id = payload.get("id", "")
            self.reporter.event(f"orphan app-server response ignored: id={response_id or 'unknown'}", tone="warn")

    def report_notification(self, payload: dict[str, Any]) -> None:
        method = payload.get("method")
        if method in {"item/started", "item/completed"}:
            item = payload.get("item") or {}
            if item.get("type") == "commandExecution":
                self.report_command_notification(payload)
            return
        if method == "mcpServer/startupStatus/updated" and self.verbose:
            name = payload.get("name", "server")
            status = payload.get("status", "")
            self.reporter.tool(f"mcp {name} {status}".strip())
            return
        turn = payload.get("turn") or {}
        turn_id = turn.get("id") or payload.get("turn_id", "")
        status = turn.get("status") or payload.get("status", "")
        if method == "turn/completed" and turn_id:
            prefix = f"{turn_id}:"
            stale_keys = [key for key in self._reported_command_updates if key.startswith(prefix)]
            for key in stale_keys:
                self._reported_command_updates.pop(key, None)
        if method == "turn/completed" and status == "failed":
            self.reporter.event(f"turn failed: {turn_id or 'unknown'}", tone="error")

    def report_command_notification(self, payload: dict[str, Any]) -> None:
        if payload.get("method") != "item/completed":
            return
        item = payload.get("item") or {}
        turn_id = str(payload.get("turn_id", "")).strip()
        call_id = str(item.get("id", "")).strip()
        dedupe_key = (
            f"{turn_id}:{call_id or item.get('command', '') or item.get('primary_target', '') or 'command'}"
        )
        command_row = {
            "command": item.get("command", ""),
            "action": item.get("primary_action", "exec"),
            "target": item.get("primary_target", ""),
            "output_chars": item.get("aggregated_output_chars", item.get("output_chars")),
            "exit_code": item.get("exitCode"),
            "duration_ms": item.get("durationMs"),
            "process_id": item.get("processId", ""),
        }
        detail = self.reporter.render_command_summary(command_row, include_pid=self.verbose)
        signature = json.dumps({"detail": detail}, sort_keys=True, separators=(",", ":"))
        if self._reported_command_updates.get(dedupe_key) == signature:
            return
        self._reported_command_updates[dedupe_key] = signature
        self.reporter.tool(detail, stream_name="stdout")

    def report_server_request(self, record: dict[str, Any]) -> None:
        method = record.get("method", "")
        action = record.get("action", "")
        payload = record.get("payload") or {}
        if method == "item/tool/requestUserInput":
            question_count = payload.get("question_count", 0)
            if action == "received":
                self.reporter.prompt(f"prompt request received: {question_count} question(s)")
                return
            if action == "answered":
                answer_ids = payload.get("answer_ids") or []
                self.reporter.prompt(f"prompt request answered: {len(answer_ids)} answer(s)")
                return
            if action == "rejected":
                self.reporter.event("prompt request rejected", tone="warn")
                return
        if self.verbose:
            self.reporter.event(f"server request {action}: {method}")

    def should_persist_notification(self, payload: dict[str, Any]) -> bool:
        method = payload.get("method")
        if method in {"turn/started", "turn/completed", "thread/status/changed", "mcpServer/startupStatus/updated"}:
            return True
        if method in {"item/started", "item/completed"}:
            item = payload.get("item") or {}
            return item.get("type") == "commandExecution"
        return False

    @staticmethod
    def cap_human_text(text: str, limit: int = 240) -> str:
        return TerminalReporter.cap_console_text(" ".join(text.split()), limit)

    @staticmethod
    def is_command_execution_notification(payload: dict[str, Any]) -> bool:
        if payload.get("method") not in {"item/started", "item/completed"}:
            return False
        item = payload.get("item") or {}
        return item.get("type") == "commandExecution"

    @staticmethod
    def is_command_execution_wire(payload: dict[str, Any]) -> bool:
        raw_payload = payload.get("payload") or {}
        if raw_payload.get("method") not in {"item/started", "item/completed"}:
            return False
        params = raw_payload.get("params") or {}
        item = params.get("item") or {}
        return item.get("type") == "commandExecution"

    @staticmethod
    def summarize_request_params(method: str, params: dict[str, Any]) -> dict[str, Any]:
        summary: dict[str, Any] = {"keys": sorted(params.keys())}
        if method == "initialize":
            client_info = params.get("clientInfo") or {}
            summary["client"] = {
                "name": client_info.get("name", ""),
                "version": client_info.get("version", ""),
            }
            summary["capability_keys"] = sorted((params.get("capabilities") or {}).keys())
            return summary
        if method in {"thread/start", "thread/resume"}:
            for key in ("threadId", "cwd", "approvalPolicy", "sandbox", "persistExtendedHistory", "model"):
                if key in params:
                    summary[key] = params[key]
            return summary
        if method == "turn/start":
            summary["threadId"] = params.get("threadId", "")
            summary["input_items"] = len(params.get("input") or [])
            summary["input_chars"] = sum(
                len(item.get("text", ""))
                for item in params.get("input") or []
                if isinstance(item, dict) and isinstance(item.get("text"), str)
            )
            collaboration_mode = params.get("collaborationMode") or {}
            settings = collaboration_mode.get("settings") or {}
            summary["collaboration_mode"] = collaboration_mode.get("mode", "")
            summary["reasoning_effort"] = settings.get("reasoning_effort", "")
            output_schema = params.get("outputSchema") or {}
            summary["output_schema"] = {
                "type": output_schema.get("type", ""),
                "required": len(output_schema.get("required") or []),
                "property_count": len((output_schema.get("properties") or {}).keys()),
            }
            return summary
        return summary

    @staticmethod
    def summarize_response_result(method: str, result: dict[str, Any]) -> dict[str, Any]:
        summary: dict[str, Any] = {"keys": sorted(result.keys())}
        if method in {"thread/start", "thread/resume"}:
            thread = result.get("thread") or {}
            summary["thread"] = {
                "id": thread.get("id", ""),
                "status": ((thread.get("status") or {}).get("type", "")),
            }
            for key in ("model", "reasoningEffort", "approvalPolicy"):
                if key in result:
                    summary[key] = result[key]
            sandbox = result.get("sandbox") or {}
            if isinstance(sandbox, dict):
                summary["sandbox"] = sandbox.get("type", "")
            return summary
        if method == "turn/start":
            summary["turn"] = EventRecorder.summarize_turn(result.get("turn") or {})
            return summary
        return summary

    @staticmethod
    def summarize_notification(method: str, params: dict[str, Any]) -> dict[str, Any]:
        summary: dict[str, Any] = {"method": method}
        if "threadId" in params:
            summary["thread_id"] = params.get("threadId", "")
        if "turnId" in params:
            summary["turn_id"] = params.get("turnId", "")
        if "item" in params and isinstance(params["item"], dict):
            summary["item"] = EventRecorder.summarize_item(params["item"])
        if "turn" in params and isinstance(params["turn"], dict):
            summary["turn"] = EventRecorder.summarize_turn(params["turn"])
        if "status" in params:
            summary["status"] = EventRecorder.summarize_scalar(params["status"])
        if "name" in params and isinstance(params["name"], str):
            summary["name"] = params["name"]
        if "error" in params and params["error"] is not None:
            summary["error"] = EventRecorder.summarize_error(params["error"])
        handled = {"threadId", "turnId", "item", "turn", "status", "name", "error"}
        remaining_keys = sorted(key for key in params.keys() if key not in handled)
        if remaining_keys:
            summary["keys"] = remaining_keys
        return summary

    @staticmethod
    def summarize_server_request_payload(method: str, action: str, payload: dict[str, Any]) -> dict[str, Any]:
        if method == "item/tool/requestUserInput":
            if action == "answered":
                answers = payload.get("answers") or {}
                return {"answer_ids": sorted(answers.keys())}
            questions = payload.get("questions") or []
            return {
                "question_ids": [question.get("id", "") for question in questions],
                "question_count": len(questions),
                "secret_count": sum(1 for question in questions if question.get("isSecret")),
                "option_counts": [len(question.get("options") or []) for question in questions],
            }
        return {"keys": sorted(payload.keys())}

    @staticmethod
    def summarize_item(item: dict[str, Any]) -> dict[str, Any]:
        summary: dict[str, Any] = {"type": item.get("type", "")}
        for key in ("id", "status", "role", "phase", "name", "call_id", "processId"):
            if key in item and item.get(key) not in {None, ""}:
                summary[key] = item[key]
        if isinstance(item.get("text"), str):
            summary["text_chars"] = len(item["text"])
        if isinstance(item.get("command"), str):
            summary["command"] = truncate_label(item["command"], 160)
        if isinstance(item.get("durationMs"), int):
            summary["durationMs"] = item["durationMs"]
        if isinstance(item.get("exitCode"), int):
            summary["exitCode"] = item["exitCode"]
        if isinstance(item.get("content"), list):
            summary["content_items"] = len(item["content"])
            content_text_chars = sum(
                len(content.get("text", ""))
                for content in item["content"]
                if isinstance(content, dict) and isinstance(content.get("text"), str)
            )
            if content_text_chars:
                summary["content_text_chars"] = content_text_chars
        if isinstance(item.get("summary"), list):
            summary["summary_parts"] = len(item["summary"])
        if "output" in item:
            summary["output_chars"] = len(EventRecorder.stringify(item.get("output")))
        if isinstance(item.get("aggregated_output_chars"), int):
            summary["aggregated_output_chars"] = item["aggregated_output_chars"]
        if isinstance(item.get("aggregatedOutput"), str):
            summary["aggregated_output_chars"] = len(item["aggregatedOutput"])
        if isinstance(item.get("command_actions"), int):
            summary["command_actions"] = item["command_actions"]
        if isinstance(item.get("commandActions"), list):
            summary["command_actions"] = len(item["commandActions"])
            if item["commandActions"]:
                first_action = item["commandActions"][0]
                if isinstance(first_action, dict):
                    action_type = str(first_action.get("type", "")).strip()
                    if action_type:
                        summary["primary_action"] = {
                            "listFiles": "list",
                            "searchText": "search",
                        }.get(action_type, action_type)
                    target = ""
                    if isinstance(first_action.get("path"), str) and first_action["path"].strip():
                        target = first_action["path"].strip()
                    if target:
                        path_obj = Path(target)
                        summary["primary_target"] = target if not path_obj.is_absolute() else path_obj.name
                    elif isinstance(first_action.get("name"), str) and first_action["name"].strip():
                        summary["primary_target"] = first_action["name"].strip()
        return summary

    @staticmethod
    def summarize_turn(turn: dict[str, Any]) -> dict[str, Any]:
        summary: dict[str, Any] = {}
        for key in ("id", "status", "startedAt", "completedAt", "durationMs"):
            if key in turn and turn.get(key) not in {None, ""}:
                summary[key] = turn[key]
        if isinstance(turn.get("items"), list):
            summary["item_count"] = len(turn["items"])
        if turn.get("error"):
            summary["error"] = EventRecorder.summarize_error(turn["error"])
        return summary

    @staticmethod
    def summarize_error(error: Any) -> dict[str, Any]:
        if isinstance(error, dict):
            summary = {}
            if "code" in error:
                summary["code"] = error["code"]
            if isinstance(error.get("message"), str):
                summary["message"] = truncate_label(error["message"], 160)
            if "type" in error:
                summary["type"] = error["type"]
            if "data" in error and isinstance(error["data"], dict):
                summary["data_keys"] = sorted(error["data"].keys())
            return summary or {"keys": sorted(error.keys())}
        return {"value": EventRecorder.stringify(error)}

    @staticmethod
    def summarize_scalar(value: Any) -> Any:
        if isinstance(value, dict):
            return {key: value[key] for key in sorted(value.keys()) if isinstance(value[key], (str, int, float, bool))}
        if isinstance(value, list):
            return {"count": len(value)}
        return value

    @staticmethod
    def stringify(value: Any) -> str:
        if isinstance(value, str):
            return value
        try:
            return json.dumps(value, sort_keys=True)
        except TypeError:
            return str(value)


class NullEventRecorder:
    def record_client_event(self, payload: dict[str, Any]) -> None:
        return None

    def record_rpc_request(self, request_id: str | int, method: str, params: dict[str, Any] | None) -> None:
        return None

    def record_rpc_response(self, request_id: str | int, method: str, response: dict[str, Any]) -> None:
        return None


class SubprocessAppServerClient:
    def __init__(
        self,
        runtime_config: RuntimeConfig,
        event_recorder: EventRecorder,
        session_log: PlainTextRunLog | None = None,
        enable_search: bool = False,
    ):
        self.runtime_config = runtime_config
        self.event_recorder = event_recorder
        self.session_log = session_log
        self.enable_search = enable_search
        self.process: subprocess.Popen[str] | None = None
        self._reader: threading.Thread | None = None
        self._stderr_reader: threading.Thread | None = None
        self._event_queue: queue.Queue[dict[str, Any]] = queue.Queue()
        self._response_waiters: dict[str | int, queue.Queue[dict[str, Any]]] = {}
        self._response_lock = threading.Lock()
        self._request_id = 0
        self._stderr_lines: deque[str] = deque(maxlen=STDERR_BUFFER_LINES)
        self._stdout_closed = False

    def start(self) -> None:
        if self.process is not None:
            return
        cmd = [CODEx_BIN]
        if self.enable_search:
            cmd.append("--search")
        cmd.extend(["app-server", "--listen", "stdio://"])
        self.process = subprocess.Popen(
            cmd,
            cwd=str(self.runtime_config.workdir),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        self._reader = threading.Thread(target=self._read_stdout, name="ralph-codex-stdout", daemon=True)
        self._stderr_reader = threading.Thread(target=self._read_stderr, name="ralph-codex-stderr", daemon=True)
        self._reader.start()
        self._stderr_reader.start()
        self.request(
            "initialize",
            {
                "clientInfo": {
                    "name": "ralph-codex.py",
                    "title": "Ralph Codex",
                    "version": VERSION,
                },
                "capabilities": {"experimentalApi": True},
            },
        )

    def close(self) -> None:
        if self.process is None:
            return
        try:
            if self.process.stdin:
                self.process.stdin.close()
        finally:
            if self.process.poll() is None:
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.process.kill()
                    self.process.wait(timeout=5)
        self.process = None

    def request(self, method: str, params: dict[str, Any] | None) -> dict[str, Any]:
        request_id = self._next_id()
        wait_queue: queue.Queue[dict[str, Any]] = queue.Queue()
        with self._response_lock:
            self._response_waiters[request_id] = wait_queue
        self.event_recorder.record_rpc_request(request_id, method, params)
        self._send_json({"id": request_id, "method": method, "params": params})
        deadline = time.monotonic() + APP_SERVER_REQUEST_TIMEOUT_SECS
        try:
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise RalphError(
                        self.diagnostic_error(
                            f"timed out waiting for {method} response after {APP_SERVER_REQUEST_TIMEOUT_SECS:.0f}s"
                        )
                    )
                try:
                    response = wait_queue.get(timeout=min(0.5, remaining))
                    break
                except queue.Empty:
                    self.raise_if_unavailable(f"while waiting for {method} response")
        finally:
            with self._response_lock:
                self._response_waiters.pop(request_id, None)
        self.event_recorder.record_rpc_response(request_id, method, response)
        if "error" in response:
            raise RalphError(f"{method} failed: {response['error'].get('message', 'unknown error')}")
        return response.get("result", {})

    def next_event(self, timeout: float = 0.1) -> dict[str, Any] | None:
        try:
            return self._event_queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def send_result(self, request_id: str | int, result: dict[str, Any]) -> None:
        self._send_json({"id": request_id, "result": result})

    def send_error(self, request_id: str | int, code: int, message: str, data: Any = None) -> None:
        payload: dict[str, Any] = {"id": request_id, "error": {"code": code, "message": message}}
        if data is not None:
            payload["error"]["data"] = data
        self._send_json(payload)

    def diagnostic_error(self, message: str) -> str:
        stderr_note = self.recent_stderr()
        if stderr_note:
            return f"{message}. Recent app-server stderr:\n{stderr_note}"
        return message

    def recent_stderr(self) -> str:
        if not self._stderr_lines:
            return ""
        return "\n".join(self._stderr_lines)

    def raise_if_unavailable(self, context: str) -> None:
        if self.process is None:
            raise RalphError(self.diagnostic_error(f"codex app-server is not running {context}"))
        exit_code = self.process.poll()
        if exit_code is not None:
            raise RalphError(self.diagnostic_error(f"codex app-server exited with code {exit_code} {context}"))
        if self._stdout_closed:
            raise RalphError(self.diagnostic_error(f"codex app-server stdout closed {context}"))

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    def _send_json(self, payload: dict[str, Any]) -> None:
        if self.process is None or self.process.stdin is None:
            raise RalphError("codex app-server is not running")
        rendered = json.dumps(payload, separators=(",", ":")) + "\n"
        self.process.stdin.write(rendered)
        self.process.stdin.flush()

    def _read_stdout(self) -> None:
        assert self.process is not None and self.process.stdout is not None
        for line in self.process.stdout:
            stripped = line.strip()
            if not stripped:
                continue
            try:
                payload = json.loads(stripped)
            except json.JSONDecodeError:
                self.event_recorder.record_client_event({"type": "stdout-parse-error", "line": stripped})
                continue
            self.event_recorder.record_client_event({"type": "wire", "payload": payload})
            if "id" in payload and ("result" in payload or "error" in payload) and "method" not in payload:
                with self._response_lock:
                    waiter = self._response_waiters.get(payload["id"])
                if waiter is not None:
                    waiter.put(payload)
                else:
                    self.event_recorder.record_client_event(
                        {"type": "orphan-response", "id": payload.get("id"), "keys": sorted(payload.keys())}
                    )
                continue
            if "id" in payload and "method" in payload:
                self._event_queue.put({"kind": "server-request", "payload": payload})
                continue
            self._event_queue.put({"kind": "notification", "payload": payload})
        self._stdout_closed = True
        self._fail_pending_requests("codex app-server stdout closed before responding")
        self.event_recorder.record_client_event({"type": "stream-closed", "stream": "stdout"})
        self._event_queue.put({"kind": "stream-closed", "payload": {"stream": "stdout"}})

    def _read_stderr(self) -> None:
        assert self.process is not None and self.process.stderr is not None
        for line in self.process.stderr:
            stripped = line.rstrip("\n")
            if stripped:
                self._stderr_lines.append(stripped)
                self.event_recorder.record_client_event({"type": "stderr", "line": stripped})

    def _fail_pending_requests(self, message: str) -> None:
        response = {"error": {"message": self.diagnostic_error(message)}}
        with self._response_lock:
            waiters = list(self._response_waiters.values())
        for waiter in waiters:
            waiter.put(response)


class RalphController:
    def __init__(
        self,
        runtime_config: RuntimeConfig,
        client: SubprocessAppServerClient,
        event_recorder: EventRecorder,
        store: SessionStore,
        schema_catalog: SchemaCatalog,
        session: SessionContext,
        input_func: Callable[[str], str] = input,
        terminal_reporter: TerminalReporter | None = None,
        monotonic_func: Callable[[], float] = time.monotonic,
    ):
        self.runtime_config = runtime_config
        self.client = client
        self.event_recorder = event_recorder
        self.store = store
        self.schema_catalog = schema_catalog
        self.session = session
        self.input_func = input_func
        self.terminal_reporter = terminal_reporter or event_recorder.reporter
        self.monotonic_func = monotonic_func

    def run(self) -> int:
        self.print_status("starting Codex app-server", badge="STARTING")
        self.client.start()
        self.print_status("Codex app-server ready", badge="STARTING")
        self.ensure_thread()
        if not self.session.charter_record:
            self.print_status("initial planning started", badge="PLANNING")
            needs_plan_review = (
                self.session.profile["seed_policy"]["require_confirmation"]
                and not self.session.profile["seed_policy"]["auto_confirm"]
                and not self.session.state["seed_confirmed"]
            )
            planning_result = self.plan_once(
                "initial planning",
                self.session.state["pending_feedback"],
                render_output=not needs_plan_review,
            )
            self.validate_planning_result(planning_result)
            self.refresh_program_state(planning_result)
            self.session.state["charter_version"] += 1
            initial_feedback = self.session.state["pending_feedback"]
            self.session.state["pending_feedback"] = ""
            self.session.state["phase"] = "planning_review"
            self.store.save_charter(
                self.session,
                planning_result,
                confirmed=False,
                review_state="draft",
                operator_feedback=initial_feedback,
            )
            self.store.append_event(self.session, "planning-result", planning_result)
            self.store.save_state(self.session)
            self.print_status(
                f"initial planning complete: {truncate_label(planning_result['summary'], 120)}",
                badge="PLANNING",
            )
        self.review_plan_if_needed()
        max_iterations = self.session.profile["runtime_limits"]["max_iterations"]
        while max_iterations == 0 or self.session.state["iteration"] < max_iterations:
            self.session.state["iteration"] += 1
            self.capture_iteration_repo_baseline()
            self.session.state["phase"] = "executing"
            self.store.save_state(self.session)
            self.print_status(f"execution iteration {self.session.state['iteration']} started", badge="WORKING")
            execution_result = self.execute_once()
            self.store.append_event(self.session, "execution-result", execution_result)
            audit = self.audit_execution_result(execution_result)
            self.store.append_event(
                self.session,
                "execution-audit",
                {
                    "ok": audit.ok,
                    "feedback": audit.feedback,
                    "total_files_changed": audit.total_files_changed,
                    "repeated_heading_file_count": audit.repeated_heading_file_count,
                    "meta_artifact_files": audit.meta_artifact_files,
                    "requires_checkpoint": audit.requires_checkpoint,
                    "checkpoint_reason": audit.checkpoint_reason,
                    "diff_samples": audit.diff_samples,
                    "novelty_score": audit.novelty_score,
                    "acceptance_progress_score": audit.acceptance_progress_score,
                    "acceptance_criteria_met": audit.acceptance_criteria_met or [],
                    "acceptance_criteria_remaining": audit.acceptance_criteria_remaining or [],
                },
            )
            self.refresh_execution_memory(execution_result, audit)
            self.session.state["phase"] = "evaluating"
            self.store.save_state(self.session)
            evaluation_result = self.evaluate_once(execution_result, audit)
            self.store.append_event(self.session, "evaluation-result", evaluation_result)
            self.refresh_evaluation_memory(evaluation_result, audit)
            self.print_status(
                "execution iteration "
                f"{self.session.state['iteration']} returned {execution_result['status']}: "
                f"{truncate_label(execution_result['summary'], 120)}",
                badge="WORKING",
            )
            loop_action, feedback = self.decide_next_action(execution_result, audit, evaluation_result)
            accepted = loop_action == "finish"
            completion_reason = "" if accepted else feedback
            if execution_result["status"] == "COMPLETE" and not accepted:
                self.session.state["completion_rejections"].append(completion_reason)
            self.store.save_completion(self.session, execution_result, accepted, completion_reason)
            if accepted:
                self.print_status("completion accepted; Ralph run finished", badge="DONE")
                self.store.finish(self.session, "completed", execution_result["summary"])
                return 0
            self.session.state["pending_feedback"] = feedback
            self.store.save_state(self.session)
            self.review_progress_if_needed(audit)
            self.store.save_state(self.session)
            if loop_action == "repair_same_tranche":
                self.session.state["phase"] = "executing"
                self.print_status(
                    f"same-tranche repair queued: {truncate_label(feedback, 120)}",
                    badge="WORKING",
                )
                continue
            self.session.state["same_tranche_repair_count"] = 0
            self.session.state["consecutive_replans"] += 1
            if self.session.state["consecutive_replans"] > self.loop_policy()["max_consecutive_replans"]:
                raise RalphError(
                    "exhausted max_consecutive_replans="
                    f"{self.loop_policy()['max_consecutive_replans']} without verified milestone completion"
                )
            self.session.state["phase"] = "planning"
            self.print_status("replanning started", badge="PLANNING")
            planning_result = self.plan_once("replanning", self.session.state["pending_feedback"])
            self.validate_planning_result(planning_result)
            self.refresh_program_state(planning_result)
            self.session.state["charter_version"] += 1
            replanning_feedback = self.session.state["pending_feedback"]
            self.session.state["pending_feedback"] = ""
            self.session.state["consecutive_replans"] = 0
            self.store.save_charter(
                self.session,
                planning_result,
                confirmed=self.session.state["seed_confirmed"],
                review_state="approved" if self.session.state["seed_confirmed"] else "draft",
                operator_feedback=replanning_feedback,
            )
            self.store.append_event(self.session, "planning-result", planning_result)
            self.store.save_state(self.session)
            self.print_status(
                f"replanning complete: {truncate_label(planning_result['summary'], 120)}",
                badge="PLANNING",
            )
        raise RalphError(f"reached max_iterations={max_iterations} without verified completion")

    def ensure_thread(self) -> None:
        model = self.session.profile["planning"]["model"]
        sandbox_mode = SANDBOX_BY_ACCESS_MODE[self.session.profile["thread_policy"]["access_mode"]]
        if self.session.state["thread_id"]:
            self.print_status(f"resuming thread {self.session.state['thread_id']}", badge="STARTING")
            result = self.client.request(
                "thread/resume",
                {
                    "threadId": self.session.state["thread_id"],
                    "cwd": str(self.runtime_config.workdir),
                    "approvalPolicy": "never",
                    "sandbox": sandbox_mode,
                    "persistExtendedHistory": True,
                },
            )
            self.session.state["thread_id"] = result["thread"]["id"]
            self.session.state["model"] = result.get("model", self.session.state["model"] or model)
            self.store.save_state(self.session)
            self.store.append_event(self.session, "thread-resumed", {"thread_id": self.session.state["thread_id"]})
            self.print_status(f"thread resumed: {self.session.state['thread_id']}", badge="STARTING")
            return
        self.print_status("starting new thread", badge="STARTING")
        result = self.client.request(
            "thread/start",
            {
                "cwd": str(self.runtime_config.workdir),
                "approvalPolicy": "never",
                "sandbox": sandbox_mode,
                "experimentalRawEvents": True,
                "persistExtendedHistory": True,
                "model": model,
            },
        )
        self.session.state["thread_id"] = result["thread"]["id"]
        self.session.state["model"] = result.get("model", model)
        self.store.save_state(self.session)
        self.store.append_event(self.session, "thread-started", {"thread_id": self.session.state["thread_id"]})
        self.print_status(f"thread started: {self.session.state['thread_id']}", badge="STARTING")

    def plan_once(self, phase_name: str, feedback: str | None, render_output: bool = True) -> dict[str, Any]:
        return self.run_turn(
            phase_name=phase_name,
            prompt=self.build_planning_prompt(phase_name, feedback),
            schema=self.schema_catalog.model_schema(self.session.profile["planning"]["output_schema_id"]),
            collaboration_mode=self.make_collaboration_mode(
                self.session.profile["planning"]["mode"],
                self.session.profile["planning"]["reasoning_effort"],
                self.planning_instructions(),
                model=self.session.profile["planning"]["model"],
            ),
            render_output=render_output,
        )

    def execute_once(self) -> dict[str, Any]:
        return self.run_turn(
            phase_name=f"execution-{self.session.state['iteration']}",
            prompt=self.build_execution_prompt(self.session.state["pending_feedback"]),
            schema=self.schema_catalog.model_schema(self.session.profile["execution"]["output_schema_id"]),
            collaboration_mode=self.make_collaboration_mode(
                self.session.profile["execution"]["mode"],
                self.session.profile["execution"]["reasoning_effort"],
                self.execution_instructions(),
                model=self.session.profile["execution"]["model"],
            ),
        )

    def evaluate_once(self, execution_result: dict[str, Any], audit: ExecutionAudit) -> dict[str, Any]:
        return self.run_turn(
            phase_name=f"evaluation-{self.session.state['iteration']}",
            prompt=self.build_evaluation_prompt(execution_result, audit),
            schema=self.schema_catalog.model_schema(self.session.profile["evaluation"]["output_schema_id"]),
            collaboration_mode=self.make_collaboration_mode(
                self.session.profile["evaluation"]["mode"],
                self.session.profile["evaluation"]["reasoning_effort"],
                self.evaluation_instructions(),
                model=self.session.profile["evaluation"]["model"],
            ),
        )

    def run_turn(
        self,
        phase_name: str,
        prompt: str,
        schema: dict[str, Any],
        collaboration_mode: dict[str, Any],
        render_output: bool = True,
    ) -> dict[str, Any]:
        result = self.client.request(
            "turn/start",
            {
                "threadId": self.session.state["thread_id"],
                "input": [self.make_text_input(prompt)],
                "outputSchema": schema,
                "collaborationMode": collaboration_mode,
            },
        )
        turn_id = result["turn"]["id"]
        self.session.state["current_turn_id"] = turn_id
        self.store.save_state(self.session)
        self.print_status(f"{phase_name} started", badge=self.phase_badge(phase_name))
        tracker = TurnOutputTracker()
        streamed_live = False
        turn_started_at = self.monotonic_func()
        next_heartbeat_at = turn_started_at + TURN_IDLE_HEARTBEAT_SECS
        while True:
            event = self.client.next_event(timeout=0.1)
            if event is None:
                self.client.raise_if_unavailable("while waiting for turn events")
                current_time = self.monotonic_func()
                if current_time >= next_heartbeat_at:
                    elapsed_seconds = max(1, int(current_time - turn_started_at))
                    self.terminal_reporter.wait(phase_name, elapsed_seconds, badge=self.phase_badge(phase_name))
                    next_heartbeat_at += TURN_IDLE_HEARTBEAT_SECS
                continue
            if event["kind"] == "server-request":
                self.handle_server_request(event["payload"])
                continue
            if event["kind"] == "stream-closed":
                raise RalphError(self.client.diagnostic_error("codex app-server stream closed during turn"))
            payload = event["payload"]
            method = payload.get("method")
            params = payload.get("params", {})
            self.event_recorder.record_notification(method, params)
            if method in {"item/agentMessage/delta", "item/plan/delta"} and params.get("turnId") == turn_id:
                delta = params.get("delta", "")
                if isinstance(delta, str) and delta:
                    streamed_live = self.terminal_reporter.stream_model_text(phase_name, delta) or streamed_live
                continue
            if method == "rawResponseItem/completed" and params.get("turnId") == turn_id:
                item = params.get("item", {})
                tracker.record_raw_item(item)
                if item.get("type") in {"function_call", "function_call_output"}:
                    self.store.append_event(
                        self.session,
                        "tool-item",
                        {
                            "turn_id": turn_id,
                            "item_type": item.get("type", ""),
                            "name": item.get("name", ""),
                            "call_id": item.get("call_id", ""),
                            "output_chars": len(EventRecorder.stringify(item.get("output", ""))),
                        },
                    )
                continue
            if method == "item/completed" and params.get("turnId") == turn_id:
                tracker.record_thread_item(params.get("item", {}))
                continue
            if method == "turn/completed" and params.get("turn", {}).get("id") == turn_id:
                turn = params.get("turn", {})
                status = turn.get("status")
                if status == "failed":
                    error = turn.get("error") or {}
                    raise RalphError(error.get("message", "Codex turn failed"))
                if status == "interrupted":
                    raise RalphError("Codex turn was interrupted")
                break
        self.terminal_reporter.finish_stdout_line()
        final_output = tracker.extract_final_output(schema)
        search_activity = tracker.summarize_search_activity()
        if search_activity["count"]:
            self.store.append_event(self.session, "turn-search-activity", {"turn_id": turn_id, **search_activity})
        if render_output:
            self.render_model_output(phase_name, final_output, streamed_live)
        self.store.append_turn(
            self.session,
            phase_name,
            turn_id,
            final_output.get("status", "UNKNOWN"),
            final_output.get("summary", ""),
        )
        self.session.state["current_turn_id"] = ""
        self.store.save_state(self.session)
        self.print_status(
            f"{phase_name} complete: "
            f"{final_output.get('status', 'UNKNOWN')}: {truncate_label(final_output.get('summary', ''), 120)}",
            badge=self.phase_badge(phase_name),
        )
        return final_output

    def handle_server_request(self, payload: dict[str, Any]) -> None:
        method = payload.get("method")
        request_id = payload.get("id")
        params = payload.get("params", {})
        if method == "item/tool/requestUserInput":
            self.store.append_server_request(self.session, request_id, method, "received", params)
            self.event_recorder.record_server_request(request_id, method, "received", params)
            answer = self.answer_request_user_input(params)
            self.client.send_result(request_id, answer)
            self.store.append_server_request(self.session, request_id, method, "answered", answer)
            self.event_recorder.record_server_request(request_id, method, "answered", answer)
            return
        self.client.send_error(request_id, -32601, f"Unsupported server request: {method}")
        self.store.append_server_request(self.session, request_id, method or "", "rejected", params)
        self.event_recorder.record_server_request(request_id, method or "", "rejected", params)

    def answer_request_user_input(self, params: dict[str, Any]) -> dict[str, Any]:
        policy = self.session.profile["prompt_answering"]
        answers: dict[str, Any] = {}
        for question in params.get("questions", []):
            question_id = question["id"]
            if policy["reject_secret_questions"] and question.get("isSecret"):
                raise UnsupportedPromptError(f"secret prompt cannot be auto-answered: {question_id}")
            options = question.get("options") or []
            if policy["require_selectable_options"] and not options:
                raise UnsupportedPromptError(f"prompt has no selectable options: {question_id}")
            answers[question_id] = {"answers": [self.select_prompt_option(options)]}
        return {"answers": answers}

    @staticmethod
    def select_prompt_option(options: list[dict[str, Any]]) -> str:
        for option in options:
            if "(Recommended)" in option.get("label", ""):
                return option["label"]
        return options[0]["label"]

    def validate_planning_result(self, planning_result: dict[str, Any]) -> dict[str, Any]:
        if planning_result.get("status") == "BLOCKED":
            raise RalphError("planner reported BLOCKED and cannot proceed to execution")
        self.validate_research_block(
            planning_result.get("research"),
            self.session.profile["research_policy"]["planning_min_sources"],
        )
        charter_policy = self.session.profile["charter_policy"]
        program_board = planning_result.get("program_board")
        if not isinstance(program_board, dict):
            raise RalphError("planner did not return a program_board object")
        milestones = program_board.get("milestones")
        if not isinstance(milestones, list) or not milestones:
            raise RalphError("planner program_board is missing milestones")
        if len(milestones) > self.session.profile["milestone_policy"]["max_active_milestones"]:
            active_count = sum(1 for item in milestones if item.get("status") == "active")
            if active_count > self.session.profile["milestone_policy"]["max_active_milestones"]:
                raise RalphError("planner returned too many active milestones")
        workstreams = [entry for milestone in milestones for entry in milestone.get("workstreams", [])]
        if not isinstance(workstreams, list) or len(workstreams) < charter_policy["min_workstreams"]:
            raise RalphError("planner program_board is too narrow")
        seen_ids: set[str] = set()
        for workstream in workstreams:
            identifier = workstream.get("id")
            if not identifier or not isinstance(identifier, str):
                raise RalphError("planner program_board contains a workstream with no id")
            if identifier in seen_ids:
                raise RalphError(f"planner program_board reused workstream id: {identifier}")
            seen_ids.add(identifier)
            if charter_policy["require_adjacent_surfaces"] and not workstream.get("required_adjacent_surfaces"):
                raise RalphError(f"workstream {identifier} is missing adjacent surfaces")
            if charter_policy["require_validation_for_each_workstream"] and not workstream.get("validation"):
                raise RalphError(f"workstream {identifier} is missing validation obligations")
        if charter_policy["require_validation_categories"] and not program_board.get("validation_categories"):
            raise RalphError("planner program_board is missing validation categories")
        active_milestone = self.validate_active_milestone(planning_result.get("active_milestone"), program_board)
        self.validate_current_tranche(planning_result.get("current_tranche"), program_board, active_milestone)
        return program_board

    def validate_research_block(self, research: Any, min_sources: int) -> None:
        if not isinstance(research, dict):
            raise RalphError("planner did not return a research block")
        status = research.get("status")
        if status not in {"completed", "blocked"}:
            raise RalphError("research status must be completed or blocked")
        if status == "blocked" and self.session.profile["research_policy"]["block_on_search_unavailable"]:
            raise RalphError("research is blocked and planning cannot proceed")
        if not isinstance(research.get("search_strategy"), str) or not research["search_strategy"].strip():
            raise RalphError("research block is missing search_strategy")
        findings = research.get("findings")
        if not isinstance(findings, list) or not findings:
            raise RalphError("research block must include findings")
        sources = research.get("sources")
        if not isinstance(sources, list):
            raise RalphError("research block must include sources")
        if status == "completed" and len(sources) < min_sources:
            raise RalphError(f"research block must include at least {min_sources} sources")
        if (
            status == "completed"
            and self.session.profile["research_policy"]["require_primary_sources_when_available"]
            and not any(isinstance(entry, dict) and entry.get("source_type") == "primary" for entry in sources)
        ):
            raise RalphError("completed research block must include a primary source when available")
        if status == "completed":
            latest_turn = self.store.latest_turn(self.session)
            search_count = self.latest_turn_search_count()
            required_searches = 2 if self.session.profile["research_policy"]["require_multi_step_search"] else 1
            if latest_turn and search_count < required_searches:
                raise RalphError(
                    "completed research block is not backed by enough observed live search activity "
                    f"(observed={search_count}, required={required_searches})"
                )

    def validate_active_milestone(self, milestone: Any, program_board: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(milestone, dict):
            raise RalphError("planner did not return an active_milestone")
        milestone_id = str(milestone.get("milestone_id", "")).strip()
        milestones = {entry.get("id"): entry for entry in program_board.get("milestones", [])}
        if milestone_id not in milestones:
            raise RalphError(f"active_milestone references unknown milestone id: {milestone_id}")
        if not isinstance(milestone.get("target_files"), list) or not milestone.get("target_files"):
            raise RalphError("active_milestone is missing target_files")
        if not isinstance(milestone.get("validation"), list) or not milestone.get("validation"):
            raise RalphError("active_milestone is missing validation")
        return milestone

    def validate_current_tranche(self, tranche: Any, program_board: dict[str, Any], active_milestone: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(tranche, dict):
            raise RalphError("planner did not return a current tranche")
        milestone_id = str(tranche.get("milestone_id", "")).strip()
        if milestone_id != str(active_milestone.get("milestone_id", "")).strip():
            raise RalphError("current tranche milestone_id must match active_milestone.milestone_id")
        workstream_ids = tranche.get("workstream_ids")
        if not isinstance(workstream_ids, list) or not workstream_ids:
            raise RalphError("current tranche is missing workstream_ids")
        tranche_policy = self.session.profile["tranche_policy"]
        if len(workstream_ids) > tranche_policy["max_active_workstreams"]:
            raise RalphError("current tranche exceeds max_active_workstreams")
        target_files = tranche.get("target_files")
        if tranche_policy["require_explicit_target_files"] and (not isinstance(target_files, list) or not target_files):
            raise RalphError("current tranche is missing target_files")
        if isinstance(target_files, list) and len(target_files) > tranche_policy["max_target_files"]:
            raise RalphError("current tranche exceeds max_target_files")
        known_ids = {
            entry.get("id")
            for milestone in program_board.get("milestones", [])
            for entry in milestone.get("workstreams", [])
            if milestone.get("id") == milestone_id
        }
        for identifier in workstream_ids:
            if identifier not in known_ids:
                raise RalphError(f"current tranche references unknown workstream id: {identifier}")
        validation = tranche.get("validation")
        if not isinstance(validation, list) or not validation:
            raise RalphError("current tranche is missing validation")
        return tranche

    def validate_verification_block(self, verification: Any) -> None:
        if not isinstance(verification, dict):
            raise RalphError("executor did not return a verification block")
        status = verification.get("status")
        if status not in {"completed", "blocked", "not_needed"}:
            raise RalphError("verification status must be completed, blocked, or not_needed")
        if not isinstance(verification.get("scope"), str) or not verification["scope"].strip():
            raise RalphError("verification block is missing scope")
        findings = verification.get("findings")
        if not isinstance(findings, list) or not findings:
            raise RalphError("verification block must include findings")
        sources = verification.get("sources")
        if not isinstance(sources, list):
            raise RalphError("verification block must include sources")
        min_sources = self.session.profile["research_policy"]["execution_min_sources"]
        if status == "completed" and len(sources) < min_sources:
            raise RalphError(f"verification block must include at least {min_sources} sources")
        if status == "completed" and self.store.latest_turn(self.session) and self.latest_turn_search_count() < 1:
            raise RalphError("completed verification block is not backed by observed live search activity")

    def current_tranche(self) -> dict[str, Any]:
        planning_result = (self.session.charter_record or {}).get("planning_result") or {}
        tranche = planning_result.get("current_tranche")
        if isinstance(tranche, dict):
            return tranche
        return default_tranche_payload(self.current_charter())

    def current_program_board(self) -> dict[str, Any]:
        planning_result = (self.session.charter_record or {}).get("planning_result") or {}
        program_board = planning_result.get("program_board")
        if isinstance(program_board, dict):
            return program_board
        return legacy_program_board_from_charter((self.session.charter_record or {}).get("charter"))

    def current_charter(self) -> dict[str, Any]:
        return charter_from_program_board(self.current_program_board())

    def active_milestone(self) -> dict[str, Any]:
        planning_result = (self.session.charter_record or {}).get("planning_result") or {}
        milestone = planning_result.get("active_milestone")
        if isinstance(milestone, dict):
            return milestone
        return default_active_milestone_payload(self.current_program_board())

    def milestone_by_id(self, milestone_id: str) -> dict[str, Any] | None:
        for milestone in self.current_program_board().get("milestones", []):
            if milestone.get("id") == milestone_id:
                return milestone
        return None

    def loop_policy(self) -> dict[str, Any]:
        policy = self.session.profile.get("loop_policy") or {}
        if isinstance(policy, dict):
            return policy
        return default_profile_baseline()["loop_policy"]

    def quality_policy(self) -> dict[str, Any]:
        policy = self.session.profile.get("quality_policy") or {}
        if isinstance(policy, dict):
            return policy
        return default_profile_baseline()["quality_policy"]

    def memory_policy(self) -> dict[str, Any]:
        policy = self.session.profile.get("memory_policy") or {}
        if isinstance(policy, dict):
            return policy
        return default_profile_baseline()["memory_policy"]

    def worker_policy(self) -> dict[str, Any]:
        policy = self.session.profile.get("worker_policy") or {}
        if isinstance(policy, dict):
            return policy
        return default_profile_baseline()["worker_policy"]

    def trim_memory_entries(self, items: list[Any], key: str, fallback: int) -> list[Any]:
        limit = self.memory_policy().get(key, fallback)
        if not isinstance(limit, int) or limit < 1:
            limit = fallback
        return items[-limit:]

    def record_worker_manifest(self, role: str, status: str, summary: str) -> None:
        manifests = self.session.state.get("worker_manifests") or []
        manifests.append({"role": role, "status": status, "summary": summary})
        self.session.state["worker_manifests"] = self.trim_memory_entries(
            manifests,
            "max_worker_manifests",
            8,
        )

    def latest_turn_search_count(self) -> int:
        latest_turn = self.store.latest_turn(self.session)
        if not latest_turn:
            return 0
        return self.turn_search_count(latest_turn.get("turn_id", ""))

    def turn_search_count(self, turn_id: str) -> int:
        if not turn_id:
            return 0
        events = self.store.read_jsonl(self.session.session_dir / "events.jsonl", EVENT_LOG_LINE_SCHEMA_ID)
        total = 0
        for event in events:
            if event.get("event_type") != "turn-search-activity":
                continue
            payload = event.get("payload") or {}
            if payload.get("turn_id") == turn_id:
                total += int(payload.get("count", 0))
        return total

    def refresh_program_state(self, planning_result: dict[str, Any]) -> None:
        program_board = planning_result.get("program_board") or legacy_program_board_from_charter(planning_result.get("charter"))
        active_milestone = planning_result.get("active_milestone") or default_active_milestone_payload(program_board)
        now = utc_timestamp()
        self.session.state["active_milestone_id"] = str(active_milestone.get("milestone_id", "")).strip()
        self.session.state["milestone_iteration_count"] = 0
        self.session.state["consecutive_low_novelty_iterations"] = 0
        self.session.state["program_memory"] = {
            "goal": program_board.get("goal", ""),
            "milestones": [
                {
                    "id": entry.get("id", ""),
                    "title": entry.get("title", ""),
                    "status": entry.get("status", ""),
                }
                for entry in program_board.get("milestones", [])
            ],
            "active_milestone_id": self.session.state["active_milestone_id"],
            "updated_at": now,
        }
        research = planning_result.get("research") or {}
        self.session.state["research_memory"] = {
            "search_strategy": str(research.get("search_strategy", "")).strip(),
            "open_questions": research.get("open_questions") or [],
            "last_refreshed_at": now,
        }
        self.register_evidence_sources(research.get("sources") or [], used_for_prefix="planning")

    def refresh_execution_memory(self, execution_result: dict[str, Any], audit: ExecutionAudit) -> None:
        self.session.state["milestone_iteration_count"] += 1
        if audit.novelty_score <= 0:
            self.session.state["consecutive_low_novelty_iterations"] += 1
        else:
            self.session.state["consecutive_low_novelty_iterations"] = 0
        execution_memory = self.session.state.get("execution_memory") or []
        execution_memory.append(
            {
                "iteration": self.session.state["iteration"],
                "summary": execution_result.get("summary", "") or "Execution update",
                "novelty_score": audit.novelty_score,
                "acceptance_progress_score": audit.acceptance_progress_score,
            }
        )
        max_entries = self.memory_policy()["max_execution_memory_entries"]
        self.session.state["execution_memory"] = execution_memory[-max_entries:]
        verification = execution_result.get("verification") or {}
        self.register_evidence_sources(verification.get("sources") or [], used_for_prefix="verification")
        self.register_evidence_updates(execution_result.get("evidence_updates") or [])
        self.refresh_skill_memory(execution_result)

    def refresh_evaluation_memory(self, evaluation_result: dict[str, Any], audit: ExecutionAudit) -> None:
        summary = str(evaluation_result.get("summary", "")).strip() or "Evaluation update"
        checkpoints = (self.session.state.get("checkpoint_summaries") or []) + [
            {"phase": "evaluation", "summary": summary, "ts": utc_timestamp()}
        ]
        self.session.state["checkpoint_summaries"] = self.trim_memory_entries(
            checkpoints,
            "max_checkpoint_summaries",
            8,
        )
        if evaluation_result.get("worker_fanout_recommended") and self.worker_policy()["enabled"]:
            self.record_worker_manifest(
                "research",
                "recommended",
                "Evaluator recommended bounded worker fan-out for the next step.",
            )
        if evaluation_result.get("milestone_status") in {"accepted", "closed"}:
            self.session.state["milestone_iteration_count"] = 0

    def register_evidence_sources(self, sources: list[dict[str, Any]], used_for_prefix: str) -> None:
        if not sources:
            return
        registry = self.session.state.get("evidence_registry") or []
        now = utc_timestamp()
        for source in sources:
            if not isinstance(source, dict):
                continue
            url = str(source.get("url", "")).strip()
            if not url:
                continue
            entry = {
                "claim": str(source.get("used_for", "")).strip() or f"{used_for_prefix} source",
                "url": url,
                "source_type": str(source.get("source_type", "secondary")).strip() or "secondary",
                "used_for": f"{used_for_prefix}:{str(source.get('used_for', '')).strip() or 'support'}",
                "status": "confirmed",
                "updated_at": now,
            }
            registry = [item for item in registry if item.get("url") != url]
            registry.append(entry)
        self.session.state["evidence_registry"] = self.trim_memory_entries(
            registry,
            "max_evidence_registry_entries",
            32,
        )

    def register_evidence_updates(self, updates: list[dict[str, Any]]) -> None:
        if not updates:
            return
        registry = self.session.state.get("evidence_registry") or []
        now = utc_timestamp()
        for update in updates:
            if not isinstance(update, dict):
                continue
            url = str(update.get("url", "")).strip()
            if not url:
                continue
            entry = {
                "claim": str(update.get("claim", "")).strip() or "execution evidence",
                "url": url,
                "source_type": str(update.get("source_type", "secondary")).strip() or "secondary",
                "used_for": str(update.get("used_for", "")).strip() or "execution update",
                "status": str(update.get("status", "new")).strip() or "new",
                "updated_at": now,
            }
            registry = [item for item in registry if item.get("url") != url]
            registry.append(entry)
        self.session.state["evidence_registry"] = self.trim_memory_entries(
            registry,
            "max_evidence_registry_entries",
            32,
        )

    def refresh_skill_memory(self, execution_result: dict[str, Any]) -> None:
        touched_files = execution_result.get("touched_files") or []
        validation_completed = execution_result.get("validation_completed") or []
        if not touched_files and not validation_completed:
            return
        entry = {
            "title": f"Iteration {self.session.state['iteration']} repair pattern",
            "summary": (
                f"Touched {len(touched_files)} files and completed {len(validation_completed)} validation checks "
                f"while advancing milestone {self.session.state.get('active_milestone_id', '') or '(none)'}."
            ),
        }
        skills = self.session.state.get("skill_memory") or []
        skills.append(entry)
        self.session.state["skill_memory"] = self.trim_memory_entries(
            skills,
            "max_skill_memory_entries",
            8,
        )

    def capture_iteration_repo_baseline(self) -> None:
        if not self.loop_policy()["require_iteration_repo_baseline"]:
            self.session.state["iteration_repo_baseline"] = []
            self.session.state["iteration_repo_after"] = []
            return
        self.session.state["iteration_repo_baseline"] = self.changed_repo_entries()
        self.session.state["iteration_repo_after"] = []

    def run_repo_command(self, args: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            args,
            cwd=self.runtime_config.workdir,
            check=False,
            capture_output=True,
            text=True,
        )

    def changed_repo_entries(self) -> list[dict[str, str]]:
        completed = self.run_repo_command(["git", "status", "--short"])
        if completed.returncode != 0:
            return []
        entries: list[dict[str, str]] = []
        for line in completed.stdout.splitlines():
            if len(line) < 4:
                continue
            index_status = line[0]
            worktree_status = line[1]
            path = line[3:].strip()
            if " -> " in path:
                path = path.split(" -> ", 1)[1].strip()
            if path.startswith('"') and path.endswith('"'):
                path = path[1:-1]
            if not path:
                continue
            operation = "modified"
            combined_status = f"{index_status}{worktree_status}"
            if "?" in combined_status:
                operation = "untracked"
            elif "A" in combined_status:
                operation = "added"
            elif "D" in combined_status:
                operation = "deleted"
            elif "R" in combined_status:
                operation = "renamed"
            elif "C" in combined_status:
                operation = "copied"
            entries.append(
                {
                    "path": path,
                    "index_status": index_status,
                    "worktree_status": worktree_status,
                    "operation": operation,
                }
            )
        return entries

    def diff_sample_paths(self, changed_entries: list[dict[str, str]], limit: int) -> list[str]:
        if not changed_entries:
            return []
        return [entry["path"] for entry in changed_entries[:limit] if entry.get("path")]

    @staticmethod
    def repo_entry_signature(entry: dict[str, str]) -> tuple[str, str, str, str]:
        return (
            str(entry.get("path", "")),
            str(entry.get("index_status", "")),
            str(entry.get("worktree_status", "")),
            str(entry.get("operation", "")),
        )

    def iteration_repo_entries(self) -> list[dict[str, str]]:
        after_entries = self.changed_repo_entries()
        self.session.state["iteration_repo_after"] = after_entries
        baseline_entries = self.session.state.get("iteration_repo_baseline") or []
        baseline_signatures = {self.repo_entry_signature(entry) for entry in baseline_entries if isinstance(entry, dict)}
        return [
            entry
            for entry in after_entries
            if self.repo_entry_signature(entry) not in baseline_signatures
        ]

    def find_meta_artifact_files(self, paths: list[str]) -> list[str]:
        matches: list[str] = []
        for path in paths:
            lowered = path.lower()
            if any(pattern in lowered for pattern in META_ARTIFACT_PATTERNS):
                matches.append(path)
        return matches

    @staticmethod
    def path_matches_target(path_text: str, target: str) -> bool:
        normalized_path = path_text.strip().strip("/")
        normalized_target = target.strip().strip("/")
        if not normalized_path or not normalized_target:
            return False
        return normalized_path == normalized_target or normalized_path.startswith(normalized_target + "/")

    def off_tranche_touched_files(self, touched_files: list[str]) -> list[str]:
        target_files = self.current_tranche().get("target_files") or []
        if not isinstance(target_files, list) or not target_files:
            return touched_files
        return [
            path_text
            for path_text in touched_files
            if not any(self.path_matches_target(path_text, target) for target in target_files)
        ]

    @staticmethod
    def off_tranche_justification_map(justifications: Any) -> dict[str, str]:
        result: dict[str, str] = {}
        if not isinstance(justifications, list):
            return result
        for entry in justifications:
            if not isinstance(entry, dict):
                continue
            path_text = str(entry.get("path", "")).strip()
            reason = str(entry.get("reason", "")).strip()
            if path_text and reason:
                result[path_text] = reason
        return result

    def count_repeated_heading_files(self, touched_files: list[str]) -> int:
        count = 0
        for path_text in touched_files:
            diff_completed = self.run_repo_command(["git", "diff", "--unified=0", "--", path_text])
            diff_text = diff_completed.stdout if diff_completed.returncode == 0 else ""
            added_lines = [
                line[1:].strip()
                for line in diff_text.splitlines()
                if line.startswith("+") and not line.startswith("+++")
            ]
            if any(line == heading for line in added_lines for heading in REPEATED_HEADING_PATTERNS):
                count += 1
        return count

    def recent_execution_results(self, limit: int) -> list[dict[str, Any]]:
        events = self.store.read_jsonl(self.session.session_dir / "events.jsonl", EVENT_LOG_LINE_SCHEMA_ID)
        results = [entry.get("payload") or {} for entry in events if entry.get("event_type") == "execution-result"]
        return results[-limit:]

    def is_execution_stagnating(self, execution_result: dict[str, Any]) -> bool:
        threshold = self.session.profile["quality_policy"]["pause_on_stagnation_after_iterations"]
        if threshold < 2:
            return False
        previous = self.recent_execution_results(threshold - 1)
        if len(previous) < threshold - 1:
            return False
        current_gaps = tuple(sorted(execution_result.get("remaining_gaps") or []))
        if not current_gaps:
            return False
        previous_gap_sets = [tuple(sorted(entry.get("remaining_gaps") or [])) for entry in previous]
        return all(gaps == current_gaps for gaps in previous_gap_sets)

    def audit_execution_result(self, execution_result: dict[str, Any]) -> ExecutionAudit:
        self.validate_verification_block(execution_result.get("verification"))
        touched_files = execution_result.get("touched_files")
        if not isinstance(touched_files, list) or not touched_files:
            raise RalphError("execution result is missing touched_files")
        created_files = execution_result.get("created_files")
        if not isinstance(created_files, list):
            raise RalphError("execution result is missing created_files")
        off_tranche_justifications = execution_result.get("off_tranche_justifications")
        if not isinstance(off_tranche_justifications, list):
            raise RalphError("execution result is missing off_tranche_justifications")
        quality_claims = execution_result.get("quality_claims")
        if not isinstance(quality_claims, dict):
            raise RalphError("execution result is missing quality_claims")
        milestone_progress = execution_result.get("milestone_progress")
        if not isinstance(milestone_progress, dict):
            raise RalphError("execution result is missing milestone_progress")
        acceptance_artifacts = execution_result.get("acceptance_artifacts")
        if not isinstance(acceptance_artifacts, list):
            raise RalphError("execution result is missing acceptance_artifacts")
        evidence_updates = execution_result.get("evidence_updates")
        if not isinstance(evidence_updates, list):
            raise RalphError("execution result is missing evidence_updates")
        tranche_policy = self.session.profile["tranche_policy"]
        quality_policy = self.session.profile["quality_policy"]
        feedback: list[str] = []
        if len(touched_files) > tranche_policy["max_target_files"]:
            feedback.append(
                f"execution touched {len(touched_files)} files, exceeding max_target_files={tranche_policy['max_target_files']}"
            )
        off_tranche_files = self.off_tranche_touched_files(touched_files)
        justification_map = self.off_tranche_justification_map(off_tranche_justifications)
        unjustified_off_tranche = [path_text for path_text in off_tranche_files if path_text not in justification_map]
        if unjustified_off_tranche:
            feedback.append(
                "execution touched files outside current_tranche.target_files without justification: "
                + ", ".join(unjustified_off_tranche[:5])
            )
        if len(created_files) > tranche_policy["max_new_files"]:
            feedback.append(
                f"execution created {len(created_files)} files, exceeding max_new_files={tranche_policy['max_new_files']}"
            )
        if quality_claims.get("tranche_followed") is not True:
            feedback.append("execution did not claim tranche_followed=true")
        repeated_heading_file_count = self.count_repeated_heading_files(touched_files)
        if repeated_heading_file_count > quality_policy["max_repeated_heading_additions_per_iteration"]:
            feedback.append(
                "execution introduced repeated stock headings across "
                f"{repeated_heading_file_count} files"
            )
        meta_artifact_files = self.find_meta_artifact_files(created_files)
        changed_entries = self.iteration_repo_entries()
        introduced_paths = [
            entry["path"]
            for entry in changed_entries
            if entry.get("operation") in {"added", "untracked", "renamed", "copied"}
        ]
        introduced_meta_artifact_files = self.find_meta_artifact_files(introduced_paths)
        total_meta_artifact_files = len(introduced_meta_artifact_files)
        if total_meta_artifact_files > quality_policy["max_meta_artifact_files_per_run"]:
            feedback.append(
                "repo changes include disallowed controller-serving meta artifacts: "
                + ", ".join(introduced_meta_artifact_files[:5])
            )
        total_files_changed = len(changed_entries)
        active_milestone = self.active_milestone()
        active_milestone_id = str(active_milestone.get("milestone_id", "")).strip()
        progress_milestone_id = str(milestone_progress.get("milestone_id", "")).strip()
        if progress_milestone_id != active_milestone_id:
            feedback.append("milestone_progress.milestone_id does not match the active milestone")
        criteria_met = milestone_progress.get("criteria_met")
        criteria_remaining = milestone_progress.get("criteria_remaining")
        if not isinstance(criteria_met, list) or not isinstance(criteria_remaining, list):
            raise RalphError("milestone_progress must include criteria_met and criteria_remaining arrays")
        milestone_definition = self.milestone_by_id(active_milestone_id) or {}
        required_criteria = milestone_definition.get("acceptance_criteria") or []
        met_set = {item for item in criteria_met if isinstance(item, str) and item.strip()}
        remaining_set = {item for item in criteria_remaining if isinstance(item, str) and item.strip()}
        required_set = {item for item in required_criteria if isinstance(item, str) and item.strip()}
        if self.session.profile["milestone_policy"]["require_acceptance_bundle"] and required_set and not (
            met_set or remaining_set
        ):
            feedback.append("milestone progress did not report acceptance criteria state")
        novelty_score = float(len(milestone_progress.get("novelty_notes") or []))
        acceptance_progress_score = 0.0
        if required_set:
            acceptance_progress_score = len(required_set & met_set) / max(1, len(required_set))
        elif not execution_result.get("remaining_gaps"):
            acceptance_progress_score = 1.0
        if (
            self.session.state.get("consecutive_low_novelty_iterations", 0) + (1 if novelty_score <= 0 else 0)
            >= self.loop_policy()["max_consecutive_low_novelty_iterations"]
        ):
            feedback.append("execution is adding too little novel milestone progress across consecutive iterations")
        checkpoint_reasons: list[str] = []
        if self.session.state["iteration"] >= quality_policy["max_iterations_before_checkpoint"]:
            checkpoint_reasons.append("iteration checkpoint reached")
        if total_files_changed >= quality_policy["max_total_files_changed_before_checkpoint"]:
            checkpoint_reasons.append("changed-file checkpoint reached")
        if self.is_execution_stagnating(execution_result):
            checkpoint_reasons.append("stagnation checkpoint reached")
        if (
            self.session.state.get("milestone_iteration_count", 0) + 1
            >= self.session.profile["milestone_policy"]["max_tranche_iterations_per_milestone"]
        ):
            checkpoint_reasons.append("milestone iteration checkpoint reached")
        if self.session.profile["milestone_policy"]["checkpoint_on_milestone_close"] and required_set and required_set <= met_set:
            checkpoint_reasons.append("milestone completion checkpoint reached")
        return ExecutionAudit(
            ok=not feedback,
            feedback="; ".join(feedback) if feedback else "",
            total_files_changed=total_files_changed,
            repeated_heading_file_count=repeated_heading_file_count,
            meta_artifact_files=meta_artifact_files,
            requires_checkpoint=bool(checkpoint_reasons),
            checkpoint_reason="; ".join(checkpoint_reasons),
            diff_samples=self.diff_sample_paths(changed_entries, quality_policy["require_diff_samples"]),
            novelty_score=novelty_score,
            acceptance_progress_score=acceptance_progress_score,
            acceptance_criteria_met=sorted(required_set & met_set) if required_set else sorted(met_set),
            acceptance_criteria_remaining=sorted((required_set - met_set) | remaining_set) if required_set else sorted(remaining_set),
            off_tranche_file_count=len(off_tranche_files),
        )

    def review_progress_if_needed(self, audit: ExecutionAudit) -> None:
        if not audit.requires_checkpoint:
            return
        self.store.append_event(
            self.session,
            "progress-checkpoint",
            {
                "iteration": self.session.state["iteration"],
                "reason": audit.checkpoint_reason,
                "total_files_changed": audit.total_files_changed,
                "diff_samples": audit.diff_samples,
            },
        )
        mode = str(self.quality_policy().get("progress_checkpoint_mode", "require_confirmation")).strip()
        auto_continue = self.session.state["seed_confirmed"] and mode == "record_only_after_seed"
        if auto_continue:
            self.store.append_event(
                self.session,
                "progress-checkpoint-continued",
                {
                    "iteration": self.session.state["iteration"],
                    "reason": audit.checkpoint_reason,
                    "auto_continued": True,
                },
            )
            self.terminal_reporter.status(
                f"progress checkpoint recorded and auto-continued: {truncate_label(audit.checkpoint_reason, 120)}",
                badge="REVIEW",
            )
            return
        if not sys.stdin.isatty():
            raise RalphError(f"progress checkpoint requires operator input: {audit.checkpoint_reason}")
        self.terminal_reporter.approval_prompt(
            "Progress checkpoint: [c]ontinue or [x] abort "
            f"({truncate_label(audit.checkpoint_reason, 96)})"
        )
        response = self.input_func("").strip().lower()
        self.terminal_reporter.console_input(response + "\n")
        if response in {"x", "abort", "q", "quit", "n", "no"}:
            raise ProgressReviewAborted()
        self.store.append_event(
            self.session,
            "progress-checkpoint-continued",
            {
                "iteration": self.session.state["iteration"],
                "reason": audit.checkpoint_reason,
            },
        )

    def review_plan_if_needed(self) -> None:
        if self.session.state["seed_confirmed"]:
            return
        seed_policy = self.session.profile["seed_policy"]
        if not seed_policy["require_confirmation"] or seed_policy["auto_confirm"]:
            self.approve_current_plan("plan review skipped by profile; continuing unattended")
            return
        if not sys.stdin.isatty():
            raise RalphError("plan review is required, but stdin is not interactive")
        while not self.session.state["seed_confirmed"]:
            self.session.state["phase"] = "planning_review"
            self.store.save_state(self.session)
            self.print_status("waiting for plan review", badge="REVIEW")
            self.render_plan_review()
            action = self.prompt_plan_review_action()
            if action == "approve":
                self.approve_current_plan("plan approved by operator; continuing unattended")
                return
            if action == "abort":
                raise PlanReviewAborted()
            feedback = self.collect_plan_change_wishes()
            if not feedback:
                self.terminal_reporter.event("plan review change request was empty; draft remains under review", tone="warn")
                continue
            self.session.state["pending_feedback"] = feedback
            self.store.append_event(self.session, "plan-review-change-requested", {"feedback": feedback})
            self.store.save_state(self.session)
            self.print_status(
                f"planning review revision v{self.session.state['charter_version'] + 1} started",
                badge="PLANNING",
            )
            planning_result = self.plan_once("planning review", feedback, render_output=False)
            self.validate_planning_result(planning_result)
            self.refresh_program_state(planning_result)
            self.session.state["charter_version"] += 1
            self.store.save_charter(
                self.session,
                planning_result,
                confirmed=False,
                review_state="draft",
                operator_feedback=feedback,
            )
            self.session.state["pending_feedback"] = ""
            self.store.append_event(self.session, "planning-result", planning_result)
            self.store.save_state(self.session)
            self.print_status(
                f"planning review revision complete: {truncate_label(planning_result['summary'], 120)}",
                badge="PLANNING",
            )

    @staticmethod
    def charter_summary(charter: dict[str, Any]) -> str:
        lines = ["Ralph execution charter:"]
        lines.append(f"Goal: {charter.get('goal', '(missing)')}")
        for workstream in charter.get("workstreams", []):
            lines.append(f"- {workstream.get('id')}: {workstream.get('title')}")
        return "\n".join(lines)

    def approve_current_plan(self, status_message: str) -> None:
        self.session.state["seed_confirmed"] = True
        self.session.state["phase"] = "executing"
        if self.session.charter_record:
            self.store.approve_charter(self.session)
        self.store.append_event(
            self.session,
            "plan-approved",
            {"charter_version": self.session.state["charter_version"]},
        )
        self.store.save_state(self.session)
        self.print_status(status_message, badge="REVIEW")

    def prompt_plan_review_action(self) -> str:
        self.terminal_reporter.approval_prompt("Plan review: [a]pprove, [c]hange, or [x] abort")
        response = self.input_func("").strip().lower()
        self.terminal_reporter.console_input(response + "\n")
        if response in {"a", "approve", "approved", "y", "yes"}:
            return "approve"
        if response in {"x", "abort", "q", "quit", "n", "no"}:
            return "abort"
        return "change"

    def collect_plan_change_wishes(self) -> str:
        self.terminal_reporter.approval_prompt("Enter plan changes. Finish with a single '.' line.")
        lines: list[str] = []
        while True:
            line = self.input_func("")
            self.terminal_reporter.console_input(line + "\n")
            if line.strip() == ".":
                break
            lines.append(line.rstrip())
        return "\n".join(lines).strip()

    def planning_instructions(self) -> str:
        return dedent(
            """
            You are the planner inside Ralph Codex.

            Your job is to broaden the task into a strong execution program before implementation,
            then choose one active milestone and cut a narrow execution tranche that is safe, bounded, and high-signal.
            You are running in real Codex Plan Mode. The controller may ask you to revise the plan multiple times.
            Widen narrow local fixes into holistic workstreams, adjacent-surface checks, and validation obligations,
            but do not send the executor an unbounded batch.
            Use ultrathink reasoning: examine one aspect from multiple angles, compare contradictory evidence,
            and refresh the search before every replan.

            Rules:
            - Never call update_plan. That tool is not allowed in this Plan Mode flow.
            - Use only plan-safe, non-mutating exploration while planning.
            - Mandatory live web research is part of planning and replanning.
            - Run multi-step web search before finalizing the plan.
            - Prefer primary sources when available and record them explicitly.
            - If critical intent is missing, use request_user_input rather than ad hoc prose prompts.
            - Ralph updates the plan by starting another planning turn with feedback, not by using update_plan.
            - Produce a hierarchical program_board with milestones and workstreams when the task supports it.
            - Every workstream must name adjacent surfaces and validation obligations.
            - Return a research block with findings, sources, and open questions.
            - Return one active_milestone and one current_tranche with at most five active workstreams and explicit target files.
            - Prefer root-cause and system-level improvements over local patching when the task benefits from them.
            - Output only a schema-valid JSON object.
            """
        ).strip()

    def execution_instructions(self) -> str:
        return dedent(
            """
            You are the executor inside Ralph Codex.

            Implement against Ralph's program board, but only execute the current tranche for this turn.
            Do not widen the tranche on your own.
            Mandatory verification is part of every execution turn.
            If the task involves unstable facts, standards, vendors, laws, products, or recommendations,
            use live web research before reporting progress.
            Avoid controller-serving meta artifacts unless the task explicitly asks for them.
            Avoid repeated stock headings and broad low-signal template spread.
            If you must touch files outside current_tranche.target_files, record them in off_tranche_justifications.
            Report milestone_progress, acceptance_artifacts, and evidence_updates explicitly.
            Only report COMPLETE when the whole job is truly complete and the result is holistic.
            Output only a schema-valid JSON object.
            """
        ).strip()

    def evaluation_instructions(self) -> str:
        return dedent(
            """
            You are the evaluator inside Ralph Codex.

            Judge the latest execution turn using the program summary, active milestone, current tranche, execution result,
            audit result, and observed evidence posture.
            Prefer same-tranche repair over broad replanning when the tranche is still sound.
            Recommend broad replanning only when the tranche is wrong, evidence is insufficient,
            or repair is unlikely to resolve the remaining gaps.
            Only treat a milestone as complete when the acceptance bundle is actually met.
            Output only a schema-valid JSON object.
            """
        ).strip()

    @staticmethod
    def compact_text_block(text: str, limit: int) -> str:
        normalized = " ".join(text.split())
        if limit <= 0 or len(normalized) <= limit:
            return normalized
        return normalized[: limit - 3] + "..."

    def compact_json_block(self, payload: dict[str, Any], limit: int = 2400) -> str:
        rendered = json.dumps(payload, indent=2, sort_keys=True)
        if len(rendered) <= limit:
            return rendered
        compacted = json.dumps(payload, sort_keys=True)
        if len(compacted) <= limit:
            return compacted
        return self.compact_text_block(compacted, limit)

    @staticmethod
    def prompt_sections_to_text(sections: list[tuple[str, str]]) -> str:
        rendered: list[str] = []
        for title, content in sections:
            if not title and not content:
                continue
            if title:
                rendered.extend(["", title])
            if content:
                rendered.append(content)
        return "\n".join(rendered).strip() + "\n"

    def fit_prompt_to_limit(
        self,
        mandatory_sections: list[tuple[str, str]],
        optional_sections: list[tuple[str, str]],
        max_prompt_chars: int,
        error_label: str,
    ) -> str:
        prompt = self.prompt_sections_to_text(mandatory_sections + optional_sections)
        if not max_prompt_chars or len(prompt) <= max_prompt_chars:
            return prompt
        reduced_sections = list(optional_sections)
        while reduced_sections:
            reduced_sections.pop(0)
            prompt = self.prompt_sections_to_text(mandatory_sections + reduced_sections)
            if len(prompt) <= max_prompt_chars:
                return prompt
        raise RalphError(f"{error_label} exceeds max_prompt_chars={max_prompt_chars}: total={len(prompt)}")

    def worker_enabled_for_role(self, role: str) -> bool:
        policy = self.worker_policy()
        allowed_roles = policy.get("allowed_roles") or []
        return bool(policy.get("enabled")) and role in allowed_roles

    def make_worker_prompt(self, role: str, payload: dict[str, Any]) -> str:
        guidance_by_role = {
            "research": dedent(
                """
                You are a bounded auxiliary research worker for Ralph.
                Use live web research, compare sources, prefer primary sources when available, and do not mutate the repo.
                Return only the requested structured JSON object.
                """
            ).strip(),
            "read_only_repo": dedent(
                """
                You are a bounded auxiliary repo-inspection worker for Ralph.
                Inspect the repository in read-only mode only. Do not mutate files or broaden scope.
                Return only the requested structured JSON object.
                """
            ).strip(),
            "evaluator_vote": dedent(
                """
                You are a bounded auxiliary evaluator for Ralph.
                Judge the latest tranche conservatively. Do not mutate files or broaden scope.
                Return only the requested structured JSON object.
                """
            ).strip(),
        }
        return (
            f"# Auxiliary Worker Role: {role}\n\n"
            f"{guidance_by_role[role]}\n\n"
            f"## Context\n{self.compact_json_block(payload, limit=5000)}\n"
        )

    def run_auxiliary_worker(
        self,
        role: str,
        payload: dict[str, Any],
        *,
        model: str,
        reasoning_effort: str,
    ) -> dict[str, Any] | None:
        if not self.worker_enabled_for_role(role):
            return None
        if not isinstance(self.client, SubprocessAppServerClient):
            return None
        sandbox_mode = SANDBOX_BY_ACCESS_MODE[self.session.profile["thread_policy"]["access_mode"]]
        worker_runtime = RuntimeConfig(workdir=self.runtime_config.workdir, state_root=self.runtime_config.state_root)
        client = SubprocessAppServerClient(
            worker_runtime,
            NullEventRecorder(),
            enable_search=role == "research",
        )
        try:
            client.start()
            started = client.request(
                "thread/start",
                {
                    "cwd": str(worker_runtime.workdir),
                    "approvalPolicy": "never",
                    "sandbox": sandbox_mode,
                    "experimentalRawEvents": True,
                    "persistExtendedHistory": False,
                    "model": model,
                },
            )
            thread_id = started["thread"]["id"]
            result = client.request(
                "turn/start",
                {
                    "threadId": thread_id,
                    "input": [self.make_text_input(self.make_worker_prompt(role, payload))],
                    "outputSchema": WORKER_SUMMARY_SCHEMA,
                    "collaborationMode": self.make_collaboration_mode("default", reasoning_effort, "", model=model),
                },
            )
            turn_id = result["turn"]["id"]
            tracker = TurnOutputTracker()
            while True:
                event = client.next_event(timeout=0.1)
                if event is None:
                    client.raise_if_unavailable("while waiting for worker turn events")
                    continue
                if event["kind"] == "server-request":
                    request = event["payload"]
                    client.send_error(request.get("id"), -32601, "Auxiliary workers cannot request user input.")
                    continue
                if event["kind"] == "stream-closed":
                    raise RalphError("codex app-server stream closed during worker turn")
                notification = event["payload"]
                method = notification.get("method")
                params = notification.get("params", {})
                if method == "rawResponseItem/completed" and params.get("turnId") == turn_id:
                    tracker.record_raw_item(params.get("item", {}))
                    continue
                if method == "item/completed" and params.get("turnId") == turn_id:
                    tracker.record_thread_item(params.get("item", {}))
                    continue
                if method == "turn/completed" and params.get("turn", {}).get("id") == turn_id:
                    status = params.get("turn", {}).get("status")
                    if status == "failed":
                        error = params.get("turn", {}).get("error") or {}
                        raise RalphError(error.get("message", "Auxiliary worker turn failed"))
                    if status == "interrupted":
                        raise RalphError("Auxiliary worker turn was interrupted")
                    break
            worker_output = tracker.extract_final_output(WORKER_SUMMARY_SCHEMA)
            self.record_worker_manifest(
                role,
                "completed",
                truncate_label(str(worker_output.get("summary", "")).strip() or f"{role} worker complete", 120),
            )
            return worker_output
        except RalphError as exc:
            self.record_worker_manifest(role, "failed", truncate_label(str(exc), 120))
            return None
        finally:
            client.close()

    def collect_auxiliary_worker_summaries(
        self,
        roles: list[str],
        payload: dict[str, Any],
        *,
        model: str,
        reasoning_effort: str,
    ) -> list[dict[str, Any]]:
        summaries: list[dict[str, Any]] = []
        if not self.worker_policy().get("enabled"):
            return summaries
        max_workers = self.worker_policy().get("max_parallel_workers", 0)
        if not isinstance(max_workers, int) or max_workers < 1:
            return summaries
        for role in roles[:max_workers]:
            summary = self.run_auxiliary_worker(role, payload, model=model, reasoning_effort=reasoning_effort)
            if summary:
                summaries.append(summary)
        return summaries

    def latest_event_payload(self, event_type: str) -> dict[str, Any] | None:
        events = self.store.read_jsonl(self.session.session_dir / "events.jsonl", EVENT_LOG_LINE_SCHEMA_ID)
        for entry in reversed(events):
            if entry.get("event_type") == event_type:
                payload = entry.get("payload")
                if isinstance(payload, dict):
                    return payload
        return None

    def build_planning_prompt(self, phase_name: str, feedback: str | None) -> str:
        compact_history_after_chars = self.loop_policy()["compact_history_after_chars"]
        mandatory_sections = [
            (f"# Ralph Planning Phase: {phase_name}", ""),
            (
                "## Ralph Plan Mode Contract",
                "\n".join(
                    [
                        "- You are in real Plan Mode for this turn.",
                        "- Do not call update_plan.",
                        "- Use non-mutating exploration only.",
                        "- Live web research is mandatory for planning and replanning.",
                        "- Use multi-step search and compare sources before committing to a plan.",
                        "- If you truly need operator input, request it through request_user_input.",
                        "- Plan revisions happen through repeated Ralph planning turns with controller feedback.",
                        "- Return a program_board, one active_milestone, and one bounded current_tranche.",
                    ]
                ),
            ),
            ("## Task", self.compact_text_block(self.session.task["message_text"].strip(), 4000)),
        ]
        optional_sections: list[tuple[str, str]] = []
        review_history = self.render_review_history()
        if len(review_history) > compact_history_after_chars:
            review_history = "\n".join(review_history.splitlines()[-5:])
        if review_history:
            optional_sections.append(("## Review History", review_history))
        if self.session.charter_record:
            current_charter = self.current_charter()
            mandatory_sections.append(
                (
                    "## Program Memory",
                    self.compact_json_block(
                        {
                            "program_memory": self.session.state.get("program_memory", {}),
                            "active_milestone": self.active_milestone(),
                            "success_criteria": current_charter.get("success_criteria", []),
                            "current_tranche": self.current_tranche(),
                        },
                        limit=2400,
                    ),
                )
            )
        research_memory = self.session.state.get("research_memory") or {}
        if research_memory:
            optional_sections.append(("## Research Memory", self.compact_json_block(research_memory, limit=1800)))
        if self.session.completion_record.get("last_result"):
            last_result = self.session.completion_record["last_result"]
            optional_sections.append(
                (
                    "## Compact Execution Memory",
                    self.compact_json_block(
                        {
                            "status": last_result.get("status", ""),
                            "summary": last_result.get("summary", ""),
                            "remaining_gaps": last_result.get("remaining_gaps", []),
                            "touched_files": last_result.get("touched_files", []),
                            "created_files": last_result.get("created_files", []),
                        },
                        limit=2000,
                    ),
                )
            )
        execution_memory = self.session.state.get("execution_memory") or []
        if execution_memory:
            optional_sections.append(
                (
                    "## Execution Memory",
                    self.compact_json_block({"recent_iterations": execution_memory[-4:]}, limit=1800),
                )
            )
        latest_evaluation = self.latest_event_payload("evaluation-result")
        if latest_evaluation:
            optional_sections.append(
                ("## Latest Evaluation Memory", self.compact_json_block(latest_evaluation, limit=1600))
            )
        worker_summaries = self.collect_auxiliary_worker_summaries(
            [role for role in ["research", "read_only_repo"] if self.worker_enabled_for_role(role)],
            {
                "phase": phase_name,
                "task": self.session.task["message_text"].strip(),
                "program_memory": self.session.state.get("program_memory", {}),
                "research_memory": research_memory,
                "current_tranche": self.current_tranche(),
            },
            model=self.session.profile["planning"]["model"],
            reasoning_effort=self.session.profile["planning"]["reasoning_effort"],
        )
        if worker_summaries:
            optional_sections.append(
                ("## Auxiliary Worker Summaries", self.compact_json_block({"workers": worker_summaries}, limit=2200))
            )
        if feedback:
            optional_sections.append(("## Controller Feedback", self.compact_text_block(feedback.strip(), 2000)))
        max_prompt_chars = self.loop_policy()["planning_max_prompt_chars"]
        return self.fit_prompt_to_limit(
            mandatory_sections,
            optional_sections,
            max_prompt_chars,
            f"planning prompt exceeds planning_max_prompt_chars={max_prompt_chars}",
        )

    def build_execution_prompt(self, feedback: str | None) -> str:
        if not self.session.charter_record:
            raise RalphError("execution cannot start before a charter is recorded")
        tranche = self.current_tranche()
        active_milestone = self.active_milestone()
        charter_summary = {
            "goal": self.current_charter().get("goal", ""),
            "success_criteria": self.current_charter().get("success_criteria", []),
            "validation_categories": self.current_charter().get("validation_categories", []),
        }
        mandatory_sections = [
            ("# Ralph Execution Phase", ""),
            ("## Program Summary", self.compact_json_block(charter_summary, limit=1400)),
            ("## Active Milestone", self.compact_json_block(active_milestone, limit=2200)),
            ("## Current Tranche", self.compact_json_block(tranche, limit=2200)),
            ("## Task", self.compact_text_block(self.session.task["message_text"].strip(), 4000)),
            (
                "## Execution Contract",
                "\n".join(
                    [
                        "- Stay inside the current tranche.",
                        "- Do not create controller-serving meta artifacts.",
                        "- Include verification, touched_files, created_files, off_tranche_justifications, quality_claims, milestone_progress, acceptance_artifacts, and evidence_updates in the result.",
                    ]
                ),
            ),
        ]
        optional_sections: list[tuple[str, str]] = []
        evidence_registry = self.session.state.get("evidence_registry") or []
        if evidence_registry:
            optional_sections.append(
                (
                    "## Evidence Registry",
                    self.compact_json_block({"entries": evidence_registry[-6:]}, limit=1800),
                )
            )
        if feedback:
            optional_sections.append(("## Controller Feedback", self.compact_text_block(feedback.strip(), 2000)))
        cap_candidates = [
            value
            for value in [
                self.loop_policy()["execution_max_prompt_chars"],
                self.session.profile["execution"]["max_prompt_chars"],
            ]
            if isinstance(value, int) and value > 0
        ]
        max_prompt_chars = min(cap_candidates) if cap_candidates else 0
        try:
            return self.fit_prompt_to_limit(
                mandatory_sections,
                optional_sections,
                max_prompt_chars,
                "execution prompt",
            )
        except RalphError as exc:
            current_charter = json.dumps(charter_summary, indent=2, sort_keys=True)
            current_tranche = json.dumps(tranche, indent=2, sort_keys=True)
            task_text = self.session.task["message_text"].strip()
            feedback_text = feedback.strip() if feedback else ""
            raise RalphError(
                f"{exc} "
                f"(charter={len(current_charter)}, tranche={len(current_tranche)}, "
                f"task={len(task_text)}, feedback={len(feedback_text)})"
            ) from exc

    def build_evaluation_prompt(self, execution_result: dict[str, Any], audit: ExecutionAudit) -> str:
        mandatory_sections = [
            ("# Ralph Evaluation Phase", ""),
            ("## Task", self.compact_text_block(self.session.task["message_text"].strip(), 3000)),
            (
                "## Program Summary",
                self.compact_json_block(
                    {
                        "goal": self.current_charter().get("goal", ""),
                        "success_criteria": self.current_charter().get("success_criteria", []),
                        "validation_categories": self.current_charter().get("validation_categories", []),
                        "active_milestone": self.active_milestone(),
                    },
                    limit=1800,
                ),
            ),
            ("## Current Tranche", self.compact_json_block(self.current_tranche(), limit=1800)),
            ("## Execution Result", self.compact_json_block(execution_result, limit=3200)),
            (
                "## Audit Summary",
                self.compact_json_block(
                    {
                        "ok": audit.ok,
                        "feedback": audit.feedback,
                        "total_files_changed": audit.total_files_changed,
                        "repeated_heading_file_count": audit.repeated_heading_file_count,
                        "meta_artifact_files": audit.meta_artifact_files,
                        "requires_checkpoint": audit.requires_checkpoint,
                        "checkpoint_reason": audit.checkpoint_reason,
                        "diff_samples": audit.diff_samples,
                        "observed_search_count": self.latest_turn_search_count(),
                        "novelty_score": audit.novelty_score,
                        "acceptance_progress_score": audit.acceptance_progress_score,
                        "acceptance_criteria_met": audit.acceptance_criteria_met or [],
                        "acceptance_criteria_remaining": audit.acceptance_criteria_remaining or [],
                    },
                    limit=2200,
                ),
            ),
            (
                "## Evaluation Contract",
                "\n".join(
                    [
                        "- Prefer repair_same_tranche when the current tranche can still resolve the gaps.",
                        "- Use replan when the tranche is wrong, evidence is insufficient, or repair is exhausted.",
                        "- Use accept only when the result is strong enough to advance without another broad plan.",
                        "- Use milestone_status to say whether the active milestone remains open, is ready for acceptance, or is accepted.",
                    ]
                ),
            ),
        ]
        optional_sections: list[tuple[str, str]] = []
        worker_votes = self.collect_auxiliary_worker_summaries(
            [role for role in ["evaluator_vote"] if self.worker_enabled_for_role(role)],
            {
                "task": self.session.task["message_text"].strip(),
                "active_milestone": self.active_milestone(),
                "current_tranche": self.current_tranche(),
                "execution_result": execution_result,
                "audit": {
                    "feedback": audit.feedback,
                    "novelty_score": audit.novelty_score,
                    "acceptance_progress_score": audit.acceptance_progress_score,
                    "diff_samples": audit.diff_samples,
                },
            },
            model=self.session.profile["evaluation"]["model"],
            reasoning_effort=self.session.profile["evaluation"]["reasoning_effort"],
        )
        if worker_votes:
            optional_sections.append(
                ("## Auxiliary Evaluator Votes", self.compact_json_block({"workers": worker_votes}, limit=1800))
            )
        return self.prompt_sections_to_text(mandatory_sections + optional_sections)

    def compose_replanning_feedback(self, execution_result: dict[str, Any]) -> str:
        gaps = execution_result.get("remaining_gaps") or []
        gap_text = ", ".join(gaps) if gaps else "none reported"
        return (
            f"Execution is not complete for milestone {self.session.state.get('active_milestone_id') or '(none)'}. "
            f"Summary: {execution_result['summary']}. "
            f"Remaining gaps: {gap_text}. "
            f"Next step proposed by the model: {execution_result['next_step']}."
        )

    def decide_next_action(
        self,
        execution_result: dict[str, Any],
        audit: ExecutionAudit,
        evaluation_result: dict[str, Any],
    ) -> tuple[str, str]:
        confidence_rank = {"low": 1, "medium": 2, "high": 3}
        disposition = str(evaluation_result.get("disposition", "")).strip()
        repair_limit = self.loop_policy()["same_tranche_retry_limit"]
        repair_instructions = evaluation_result.get("repair_instructions") or []
        repair_feedback = " ".join(
            item.strip() for item in repair_instructions if isinstance(item, str) and item.strip()
        )
        summary = str(evaluation_result.get("summary", "")).strip() or str(execution_result.get("summary", "")).strip()
        milestone_status = str(evaluation_result.get("milestone_status", "")).strip()
        if milestone_status == "ready_to_close":
            milestone_status = "ready_for_acceptance"
        elif milestone_status == "closed":
            milestone_status = "accepted"
        recommended_scope_change = str(evaluation_result.get("recommended_scope_change", "")).strip()
        confidence = str(evaluation_result.get("confidence", "")).strip() or "low"
        confidence_floor = self.session.profile["eval_policy"]["evaluator_confidence_floor"]
        if confidence_rank.get(confidence, 0) < confidence_rank.get(confidence_floor, 0):
            disposition = "replan"
            summary = summary or "evaluation confidence is below the configured floor"

        completion_accepted = False
        completion_reason = ""
        if execution_result["status"] == "COMPLETE":
            completion_accepted, completion_reason = self.evaluate_completion(execution_result)
            if not completion_accepted:
                summary = completion_reason

        if disposition == "accept" and audit.ok and execution_result["status"] == "COMPLETE" and completion_accepted:
            return "finish", ""

        if execution_result["status"] == "BLOCKED":
            return "replan", f"execution blocked: {execution_result['summary']} | {execution_result['gate_reasoning']}"

        if not audit.ok:
            return "replan", audit.feedback

        if milestone_status in {"ready_for_acceptance", "accepted"} and execution_result["status"] != "COMPLETE":
            return "replan", (
                f"Active milestone {self.session.state.get('active_milestone_id') or '(none)'} is ready to advance. "
                "Refresh the program board, select the next milestone if needed, and continue."
            )

        if disposition == "repair_same_tranche" and self.session.state["same_tranche_repair_count"] < repair_limit:
            self.session.state["same_tranche_repair_count"] += 1
            self.session.state["consecutive_replans"] = 0
            return "repair_same_tranche", repair_feedback or self.compose_replanning_feedback(execution_result)

        if disposition == "accept" and execution_result["status"] != "COMPLETE":
            if self.session.state["same_tranche_repair_count"] < repair_limit:
                self.session.state["same_tranche_repair_count"] += 1
                self.session.state["consecutive_replans"] = 0
                return "repair_same_tranche", repair_feedback or self.compose_replanning_feedback(execution_result)

        if execution_result["status"] == "COMPLETE" and not completion_accepted:
            return "replan", completion_reason

        if disposition == "blocked":
            return "replan", summary or "evaluation blocked further progress"

        if recommended_scope_change == "stay_on_tranche" and self.session.state["same_tranche_repair_count"] < repair_limit:
            self.session.state["same_tranche_repair_count"] += 1
            self.session.state["consecutive_replans"] = 0
            return "repair_same_tranche", repair_feedback or self.compose_replanning_feedback(execution_result)

        return "replan", repair_feedback or summary or self.compose_replanning_feedback(execution_result)

    def evaluate_completion(self, execution_result: dict[str, Any]) -> tuple[bool, str]:
        completion_policy = self.session.profile["completion_policy"]
        if execution_result.get("status") != "COMPLETE":
            return False, "model did not report COMPLETE"
        if not self.session.charter_record:
            return False, "no charter recorded"
        try:
            self.validate_verification_block(execution_result.get("verification"))
        except RalphError as exc:
            return False, str(exc)
        verification = execution_result.get("verification") or {}
        if verification.get("status") == "blocked":
            return False, "verification is blocked"
        updates = execution_result.get("workstream_updates") or []
        update_map = {entry.get("id"): entry for entry in updates}
        missing = []
        disallowed_deferred = []
        for workstream in self.current_charter().get("workstreams", []):
            status = update_map.get(workstream["id"], {}).get("status")
            if completion_policy["allow_deferred_workstreams"]:
                if status not in {"done", "deferred"}:
                    missing.append(workstream["id"])
            elif status != "done":
                if status == "deferred":
                    disallowed_deferred.append(workstream["id"])
                else:
                    missing.append(workstream["id"])
        if completion_policy["require_all_workstreams_resolved"] and missing:
            return False, f"charter workstreams remain incomplete: {', '.join(sorted(missing))}"
        if disallowed_deferred:
            return False, f"deferred workstreams are not allowed: {', '.join(sorted(disallowed_deferred))}"
        if completion_policy["require_no_remaining_gaps"] and execution_result.get("remaining_gaps"):
            return False, "remaining gaps were reported"
        if completion_policy["require_validation_categories_complete"]:
            required_validation = set(self.current_charter().get("validation_categories", []))
            completed_validation = set(execution_result.get("validation_completed") or [])
            missing_validation = sorted(required_validation - completed_validation)
            if missing_validation:
                return False, f"validation categories remain incomplete: {', '.join(missing_validation)}"
        milestone_status = execution_result.get("milestone_progress", {}).get("criteria_remaining", [])
        if self.session.profile["milestone_policy"]["require_acceptance_bundle"] and milestone_status:
            return False, "active milestone still reports remaining acceptance criteria"
        return True, ""

    @staticmethod
    def make_text_input(text: str) -> dict[str, Any]:
        return {"type": "text", "text": text, "text_elements": []}

    def make_collaboration_mode(
        self,
        mode: str,
        effort: str,
        developer_instructions: str,
        model: str | None = None,
    ) -> dict[str, Any]:
        selected_model = model or self.session.state["model"] or self.session.profile["model"]
        return {
            "mode": mode,
            "settings": {
                "model": selected_model,
                "reasoning_effort": effort,
                "developer_instructions": developer_instructions,
            },
        }

    def print_stream(self, text: str) -> None:
        self.terminal_reporter.model_text(self.session.state.get("phase", "model"), text)

    @staticmethod
    def phase_badge(phase_name: str) -> str:
        lowered = phase_name.lower()
        if "planning" in lowered or "replanning" in lowered:
            return "PLANNING"
        if "evaluation" in lowered:
            return "REVIEW"
        if "review" in lowered:
            return "REVIEW"
        return "WORKING"

    def print_status(self, text: str, badge: str = "STARTING") -> None:
        self.terminal_reporter.status(text, badge=badge)

    def render_model_output(self, phase_name: str, final_output: dict[str, Any], streamed_live: bool) -> None:
        self.terminal_reporter.model_result(phase_name, final_output)
        if streamed_live:
            return

    def render_plan_review(self) -> None:
        if not self.session.charter_record:
            return
        planning_result = self.session.charter_record.get("planning_result") or {}
        self.terminal_reporter.model_result("initial planning", planning_result, full=True)
        diff_lines = self.render_plan_diff_lines()
        if diff_lines:
            self.terminal_reporter.review_diff("plan changes since prior draft", diff_lines)
        latest_turn = self.store.latest_turn(self.session)
        if latest_turn:
            trace_rows = self.store.command_trace_for_turn(self.session, latest_turn["turn_id"])
            self.terminal_reporter.command_trace_context(trace_rows)

    def render_plan_diff_lines(self) -> list[str]:
        if not self.session.charter_record:
            return []
        history = self.store.read_charter_history(self.session)
        current_version = self.session.charter_record["charter_version"]
        previous = None
        for entry in reversed(history):
            if entry["charter_version"] < current_version:
                previous = entry
                break
        if not previous:
            return []
        lines: list[str] = []
        previous_result = previous.get("planning_result") or {}
        current_result = self.session.charter_record.get("planning_result") or {}
        previous_summary = " ".join(str(previous_result.get("summary", "")).split())
        current_summary = " ".join(str(current_result.get("summary", "")).split())
        if previous_summary != current_summary:
            lines.extend(
                self.terminal_reporter._wrap_detail(
                    f"summary: {truncate_label(previous_summary or '(empty)', 96)} -> "
                    f"{truncate_label(current_summary or '(empty)', 96)}",
                    width=CONSOLE_WRAP_WIDTH - 6,
                )
            )
        previous_workstreams = {
            str(workstream.get("id", "")): str(workstream.get("title", "")).strip()
            for workstream in (previous.get("charter") or {}).get("workstreams", [])
            if str(workstream.get("id", "")).strip()
        }
        current_workstreams = {
            str(workstream.get("id", "")): str(workstream.get("title", "")).strip()
            for workstream in (self.session.charter_record.get("charter") or {}).get("workstreams", [])
            if str(workstream.get("id", "")).strip()
        }
        if len(previous_workstreams) != len(current_workstreams):
            lines.append(f"workstreams: {len(previous_workstreams)} -> {len(current_workstreams)}")
        added_workstreams = sorted(set(current_workstreams) - set(previous_workstreams))
        removed_workstreams = sorted(set(previous_workstreams) - set(current_workstreams))
        if added_workstreams:
            lines.append(
                "added_workstreams: "
                + ", ".join(
                    f"{identifier} ({current_workstreams[identifier] or 'untitled'})" for identifier in added_workstreams
                )
            )
        if removed_workstreams:
            lines.append(
                "removed_workstreams: "
                + ", ".join(
                    f"{identifier} ({previous_workstreams[identifier] or 'untitled'})" for identifier in removed_workstreams
                )
            )
        previous_validation = set((previous.get("charter") or {}).get("validation_categories") or [])
        current_validation = set((self.session.charter_record.get("charter") or {}).get("validation_categories") or [])
        added_validation = sorted(current_validation - previous_validation)
        removed_validation = sorted(previous_validation - current_validation)
        if added_validation:
            lines.append(f"added_validation_categories: {', '.join(added_validation)}")
        if removed_validation:
            lines.append(f"removed_validation_categories: {', '.join(removed_validation)}")
        if not lines:
            lines.append("No structural changes from the prior draft.")
        return lines

    def render_review_history(self) -> str:
        history = self.store.read_charter_history(self.session)
        if not history:
            return ""
        lines = []
        for entry in history:
            line = (
                f"- v{entry['charter_version']} | {entry['review_state']} | "
                f"summary={truncate_label(str((entry.get('planning_result') or {}).get('summary', '')), 96)}"
            )
            feedback = str(entry.get("operator_feedback", "")).strip()
            if feedback:
                line += f" | feedback={truncate_label(' '.join(feedback.split()), 96)}"
            lines.append(line)
        return "\n".join(lines)


def resolve_start_task(command: Command) -> dict[str, str]:
    if command.kind == "message":
        text = command.value or ""
        if not text.strip():
            raise RalphError("message text cannot be empty")
        return {
            "message_source_kind": "inline",
            "message_source_label": f"inline: {truncate_label(text)}",
            "message_text": text,
        }
    if command.kind == "file":
        path = Path(command.value or "").expanduser().resolve()
        if not path.exists():
            raise RalphError(f"message file not found: {path}")
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            raise RalphError(f"message file is empty: {path}")
        return {
            "message_source_kind": "file",
            "message_source_label": str(path),
            "message_text": text,
        }
    raise RalphError(f"unsupported start command: {command.kind}")


def format_run_rows(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "No session runs recorded."
    lines = [
        "Idx  Session ID                    Run ID                        Mode    Outcome    Session     Source",
    ]
    for row in rows:
        lines.append(
            f"{row['index']:>3}  "
            f"{row['session_id']:<28} "
            f"{row['run_id']:<28} "
            f"{row['invocation_mode']:<7} "
            f"{row['outcome']:<10} "
            f"{row['session_status']:<11} "
            f"{row['message_source_label']}"
        )
    return "\n".join(lines)


def ensure_codex_available() -> None:
    if shutil.which(CODEx_BIN) is None:
        raise RalphError(f"{CODEx_BIN} binary not found on PATH")


def execute_run(
    runtime_config: RuntimeConfig,
    store: SessionStore,
    schema_catalog: SchemaCatalog,
    session: SessionContext,
    invocation_mode: str,
    verbose: bool,
) -> int:
    ensure_codex_available()
    run_id = new_run_id()
    store.mark_active(session)
    store.update_controller_state(session.session_id, run_id)
    store.append_run_history(session, run_id, "run_started", invocation_mode, "run started")
    client: SubprocessAppServerClient | None = None
    session_log = PlainTextRunLog(
        session.session_dir / "logs" / f"{run_id}.log",
        session.session_id,
        run_id,
        invocation_mode,
        verbose,
    )
    reporter = TerminalReporter(verbose=verbose, session_log=session_log)
    event_recorder = EventRecorder(store, session, verbose, reporter=reporter)
    try:
        event_recorder.record_run_config(run_id, invocation_mode, runtime_config.workdir)
        reporter.status(f"run started: session={session.session_id} mode={invocation_mode}", badge="STARTING")
        client = SubprocessAppServerClient(
            runtime_config,
            event_recorder,
            session_log=session_log,
            enable_search=session.profile.get("research_policy", {}).get("mode") == "required",
        )
        controller = RalphController(
            runtime_config,
            client,
            event_recorder,
            store,
            schema_catalog,
            session,
            terminal_reporter=reporter,
        )
        exit_code = controller.run()
        summary = controller.session.completion_record.get("last_result", {}).get("summary", "session completed")
        store.append_run_history(session, run_id, "run_completed", invocation_mode, summary)
        reporter.status(f"run completed: {truncate_label(summary, 120)}", badge="DONE")
        return exit_code
    except KeyboardInterrupt:
        resume_command = f"./scripts/ralph-codex.py --resume {session.session_id}"
        store.mark_aborted(session, ABORT_REASON)
        store.append_event(
            session,
            "run-aborted",
            {
                "run_id": run_id,
                "reason": ABORT_REASON,
                "resume_command": resume_command,
            },
        )
        store.append_run_history(session, run_id, "run_aborted", invocation_mode, ABORT_REASON)
        reporter.event("run aborted by operator", tone="warn")
        reporter.status(f"aborted. resume session with: {resume_command}", badge="ABORTED", tone="warn")
        return ABORT_EXIT_CODE
    except Exception as exc:
        store.append_run_history(session, run_id, "run_failed", invocation_mode, str(exc))
        reporter.event(f"run failed: {truncate_label(str(exc), 160)}", tone="error")
        raise
    finally:
        store.update_controller_state(session.session_id, "")
        if client is not None:
            client.close()
        session_log.close()


def main(argv: list[str] | None = None) -> int:
    parser, command = parse_command(argv or sys.argv[1:])
    if command.kind == "help":
        parser.print_help()
        return 0

    schema_catalog = SchemaCatalog(SCHEMA_FILES)
    runtime_root = Path.cwd().resolve()
    store = SessionStore(runtime_root / STATE_ROOT_NAME, schema_catalog)

    if command.kind == "sessions":
        limit = int(command.value) if command.value is not None else None
        print(format_run_rows(store.list_run_rows(limit)))
        return 0

    if command.kind in {"message", "file"}:
        profile = load_profile(schema_catalog, command.profile_path)
        task = resolve_start_task(command)
        runtime_config = RuntimeConfig(workdir=runtime_root, state_root=store.root)
        session = store.create_session(runtime_root, task, profile)
        return execute_run(runtime_config, store, schema_catalog, session, command.kind, command.verbose)

    if command.kind == "resume":
        session = store.resolve_resume_target(command.value)
        runtime_config = RuntimeConfig(workdir=Path(session.session["workdir"]).resolve(), state_root=store.root)
        return execute_run(runtime_config, store, schema_catalog, session, "resume", command.verbose)

    raise RalphError(f"unsupported command: {command.kind}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RalphError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
