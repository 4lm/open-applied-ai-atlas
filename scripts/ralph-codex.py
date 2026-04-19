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
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent, wrap
from typing import Any, Callable, Optional


VERSION = "0.1.0"
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
SCHEMA_ROOT = REPO_ROOT / "schemas"
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

SCHEMA_FILES = {
    PROFILE_SCHEMA_ID: SCHEMA_ROOT / "ralph-codex" / "profile-v0.1.0.schema.json",
    PLANNING_OUTPUT_SCHEMA_ID: SCHEMA_ROOT / "ralph-codex" / "planning-output-v0.1.0.schema.json",
    EXECUTION_OUTPUT_SCHEMA_ID: SCHEMA_ROOT / "ralph-codex" / "execution-output-v0.1.0.schema.json",
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

DEFAULT_PROFILE = {
    "schema_id": PROFILE_SCHEMA_ID,
    "schema_version": "0.1.0",
    "profile_name": "default",
    "model": "gpt-5.4",
    "thread_policy": {"access_mode": "restricted"},
    "runtime_limits": {"max_iterations": 0},
    "seed_policy": {"require_confirmation": True, "auto_confirm": False},
    "prompt_answering": {
        "selection_policy": "recommended_or_first",
        "reject_secret_questions": True,
        "require_selectable_options": True,
    },
    "charter_policy": {
        "min_workstreams": 3,
        "require_adjacent_surfaces": True,
        "require_validation_for_each_workstream": True,
        "require_validation_categories": True,
    },
    "completion_policy": {
        "allow_deferred_workstreams": True,
        "require_all_workstreams_resolved": True,
        "require_no_remaining_gaps": True,
        "require_validation_categories_complete": True,
    },
    "planning": {
        "mode": "plan",
        "reasoning_effort": "high",
        "output_schema_id": PLANNING_OUTPUT_SCHEMA_ID,
    },
    "execution": {
        "mode": "default",
        "reasoning_effort": "high",
        "output_schema_id": EXECUTION_OUTPUT_SCHEMA_ID,
        "max_prompt_chars": 0,
    },
}

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
        self._handle = self.path.open("w", encoding="utf-8")
        self._closed = False
        self._lock = threading.Lock()
        self._buffers: dict[str, str] = {}
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
            buffered = self._buffers.get(channel, "") + rendered
            while True:
                newline_index = buffered.find("\n")
                if newline_index < 0:
                    break
                line = buffered[:newline_index]
                self._write_line(channel, line)
                buffered = buffered[newline_index + 1 :]
            self._buffers[channel] = buffered

    def write_console_input(self, text: str) -> None:
        self.write_chunk("CONSOLE-STDIN", text, strip_ansi=True)

    def write_console_output(self, stream_name: str, text: str) -> None:
        channel = "CONSOLE-STDOUT" if stream_name == "stdout" else "CONSOLE-STDERR"
        self.write_chunk(channel, text, strip_ansi=True)

    def write_app_stdin(self, text: str) -> None:
        self.write_chunk("APP-STDIN", text)

    def write_app_stdout(self, text: str) -> None:
        self.write_chunk("APP-STDOUT", text)

    def write_app_stderr(self, text: str) -> None:
        self.write_chunk("APP-STDERR", text)

    def close(self) -> None:
        with self._lock:
            if self._closed:
                return
            for channel, buffered in list(self._buffers.items()):
                if buffered:
                    self._write_line(channel, buffered)
                    self._buffers[channel] = ""
            self._handle.flush()
            self._handle.close()
            self._closed = True

    def _write_line(self, channel: str, line: str) -> None:
        self._handle.write(f"{utc_timestamp()} {channel} {line}\n")


class TerminalReporter:
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

    def status(self, message: str) -> None:
        self._emit_record("stdout", "status", message, tone="status")

    def wait(
        self,
        phase_name: str,
        elapsed_seconds: int,
        command_rows: list[dict[str, Any]] | None = None,
    ) -> None:
        title = f"{phase_name} running for {elapsed_seconds}s"
        if command_rows:
            self._emit_block("stdout", "wait", title, self._render_command_trace_lines(command_rows), tone="wait")
            return
        self._emit_record("stdout", "wait", title, tone="wait")

    def event(self, message: str, tone: str = "event") -> None:
        self._emit_record("stderr", "event", message, tone=tone)

    def tool(self, action: str, detail: str, stream_name: str = "stderr") -> None:
        self._emit_record(stream_name, "tool", f"{action}: {detail}", tone="tool")

    def prompt(self, message: str) -> None:
        self._emit_record("stderr", "prompt", message, tone="prompt")

    def approval_prompt(self, message: str) -> None:
        self._emit_record("stdout", "prompt", message, tone="prompt")

    def command_trace_context(self, trace_rows: list[dict[str, Any]]) -> None:
        if not trace_rows:
            return
        lines = self._render_command_trace_lines(trace_rows)
        self._emit_block("stdout", "trace", "exec log context", lines, tone="tool")

    def review_diff(self, title: str, detail_lines: list[str]) -> None:
        if not detail_lines:
            return
        self._emit_block("stdout", "review", title, detail_lines, tone="tool")

    def model_result(self, phase_name: str, payload: dict[str, Any], full: bool = False) -> None:
        lines = self._render_full_model_payload_lines(payload) if full else self._render_model_payload_lines(payload)
        title = f"{phase_name} result"
        self._emit_block("stdout", "model", title, lines, tone="model")

    def model_text(self, phase_name: str, text: str) -> None:
        cleaned = " ".join(text.split())
        if not cleaned:
            return
        self._emit_block(
            "stdout",
            "model",
            f"{phase_name} message",
            self._wrap_detail(cleaned, width=CONSOLE_WRAP_WIDTH - 4),
            tone="model",
        )

    def verbose_trace(self, event_type: str, payload: dict[str, Any]) -> None:
        if not self.verbose:
            return
        lines = self._render_trace_lines(payload)
        self._emit_block("stderr", "trace", event_type, lines, tone="trace")

    def finish_stdout_line(self) -> None:
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
        badge = self._style(stream_name, label.upper().ljust(6), tone)
        wrapped = self._wrap_detail(message)
        if not wrapped:
            wrapped = [""]
        first, *rest = wrapped
        self._write(stream_name, f"{timestamp} {badge} {first}\n")
        for line in rest:
            self._write(stream_name, f"{' ' * 9} {' ' * 6} {line}\n")

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
        badge = self._style(stream_name, label.upper().ljust(6), tone)
        header = self._style(stream_name, title, "title")
        self._write(stream_name, f"{timestamp} {badge} {header}\n")
        for line in detail_lines:
            self._write(stream_name, f"{' ' * 9} {' ' * 6} {line}\n")

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
        charter = payload.get("charter")
        if isinstance(charter, dict):
            workstreams = charter.get("workstreams") or []
            success_criteria = charter.get("success_criteria") or []
            if success_criteria:
                lines.append(self._format_kv("stdout", "success", f"{len(success_criteria)} criteria"))
            if workstreams:
                lines.append(self._format_kv("stdout", "workstreams", f"{len(workstreams)} planned"))
                for workstream in workstreams[:MODEL_WORKSTREAM_PREVIEW_COUNT]:
                    identifier = workstream.get("id", "?")
                    title = self.cap_console_text(" ".join(str(workstream.get("title", "")).split()), limit=72)
                    lines.extend(self._wrap_detail(f"- {identifier}: {title}", width=CONSOLE_WRAP_WIDTH - 6))
                remaining = len(workstreams) - MODEL_WORKSTREAM_PREVIEW_COUNT
                if remaining > 0:
                    lines.append(f"- +{remaining} more")
        updates = payload.get("workstream_updates")
        if isinstance(updates, list) and updates:
            lines.append(self._format_kv("stdout", "updates", f"{len(updates)} workstreams"))
            for update in updates[:MODEL_WORKSTREAM_PREVIEW_COUNT]:
                identifier = update.get("id", "?")
                status = update.get("status", "?")
                lines.append(f"- {identifier}: {status}")
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
        charter = payload.get("charter")
        if isinstance(charter, dict):
            goal = charter.get("goal")
            if isinstance(goal, str) and goal.strip():
                lines.extend(
                    self._wrap_detail(
                        self._format_kv("stdout", "goal", " ".join(goal.split())),
                        width=CONSOLE_WRAP_WIDTH - 4,
                    )
                )
            lines.extend(self._render_list_section("success", charter.get("success_criteria") or []))
            lines.extend(self._render_workstream_section(charter.get("workstreams") or []))
            lines.extend(self._render_list_section("validation_categories", charter.get("validation_categories") or []))
            lines.extend(self._render_list_section("deferrals", charter.get("explicit_deferrals") or []))
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
        lines = [self._format_kv("stdout", "commands", f"{len(trace_rows)} recorded")]
        for row in trace_rows:
            status = " ".join(str(row.get("status", "unknown")).split()) or "unknown"
            command = truncate_label(" ".join(str(row.get("command", "")).split()), limit=160)
            detail_parts = [status]
            if command:
                detail_parts.append(command)
            output_chars = row.get("output_chars")
            if isinstance(output_chars, int):
                detail_parts.append(f"output={output_chars} chars")
            command_actions = row.get("command_actions")
            if isinstance(command_actions, int):
                detail_parts.append(f"actions={command_actions}")
            process_id = row.get("process_id")
            if process_id:
                detail_parts.append(f"pid={process_id}")
            lines.extend(self._wrap_detail(f"- {' | '.join(detail_parts)}", width=CONSOLE_WRAP_WIDTH - 6))
        return lines

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


def semver(value: str) -> bool:
    return bool(re.match(r"^\d+\.\d+\.\d+$", value))


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
    if path is None:
        profile = deep_copy_json(DEFAULT_PROFILE)
    else:
        if not path.exists():
            raise RalphError(f"profile not found: {path}")
        profile = json.loads(path.read_text(encoding="utf-8"))
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
        self.schema_catalog.validate(schema_id, document)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
        self.schema_catalog.copy_adjacent(schema_id, path)

    def read_json(self, path: Path, schema_id: str) -> dict[str, Any]:
        payload = json.loads(path.read_text(encoding="utf-8"))
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
        state = {
            "session_id": session_id,
            "thread_id": "",
            "current_turn_id": "",
            "model": "",
            "phase": "planning",
            "status": "active",
            "iteration": 0,
            "seed_confirmed": False,
            "charter_version": 0,
            "pending_feedback": "",
            "completion_rejections": [],
            "started_at": created_at,
            "updated_at": created_at,
        }
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
            "charter": planning_result["charter"],
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
            if payload.get("method") not in {"item/started", "item/completed"}:
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
                    "status": "",
                    "output_chars": None,
                    "command_actions": None,
                    "process_id": "",
                }
                ordered_call_ids.append(call_id)
            row = rows_by_call_id[call_id]
            if isinstance(item.get("command"), str) and item["command"].strip():
                row["command"] = item["command"]
            if isinstance(item.get("status"), str) and item["status"].strip():
                row["status"] = item["status"]
            output_chars = item.get("aggregated_output_chars")
            if not isinstance(output_chars, int):
                output_chars = item.get("output_chars")
            if isinstance(output_chars, int):
                row["output_chars"] = output_chars
            if isinstance(item.get("command_actions"), int):
                row["command_actions"] = item["command_actions"]
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
            self.reporter.tool(f"mcp {name}", status)
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
        item = payload.get("item") or {}
        turn_id = str(payload.get("turn_id", "")).strip()
        call_id = str(item.get("id", "")).strip()
        command = self.cap_human_text(item.get("command", "command"), limit=160)
        status = str(item.get("status", "")).strip() or payload.get("method", "command")
        dedupe_key = f"{turn_id}:{call_id or command or status}"
        rendered_parts = [command]
        output_chars = item.get("aggregated_output_chars")
        if not isinstance(output_chars, int):
            output_chars = item.get("output_chars")
        if isinstance(output_chars, int):
            rendered_parts.append(f"output={output_chars} chars")
        command_actions = item.get("command_actions")
        if isinstance(command_actions, int):
            rendered_parts.append(f"actions={command_actions}")
        process_id = item.get("processId")
        if process_id not in {None, ""}:
            rendered_parts.append(f"pid={process_id}")
        detail = " | ".join(rendered_parts)
        signature = json.dumps({"status": status, "detail": detail}, sort_keys=True, separators=(",", ":"))
        if self._reported_command_updates.get(dedupe_key) == signature:
            return
        self._reported_command_updates[dedupe_key] = signature
        self.reporter.tool(status, detail, stream_name="stdout")

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


class SubprocessAppServerClient:
    def __init__(
        self,
        runtime_config: RuntimeConfig,
        event_recorder: EventRecorder,
        session_log: PlainTextRunLog | None = None,
    ):
        self.runtime_config = runtime_config
        self.event_recorder = event_recorder
        self.session_log = session_log
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
        cmd = [CODEx_BIN, "app-server", "--listen", "stdio://"]
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
        if self.session_log is not None:
            self.session_log.write_app_stdin(rendered)
        self.process.stdin.write(rendered)
        self.process.stdin.flush()

    def _read_stdout(self) -> None:
        assert self.process is not None and self.process.stdout is not None
        for line in self.process.stdout:
            if self.session_log is not None:
                self.session_log.write_app_stdout(line)
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
            if self.session_log is not None:
                self.session_log.write_app_stderr(line)
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
        self.print_status("starting Codex app-server")
        self.client.start()
        self.print_status("Codex app-server ready")
        self.ensure_thread()
        if not self.session.charter_record:
            self.print_status("planning started: initial planning")
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
            self.validate_charter(planning_result)
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
            self.print_status(f"planning completed: {truncate_label(planning_result['summary'], 120)}")
        self.review_plan_if_needed()
        max_iterations = self.session.profile["runtime_limits"]["max_iterations"]
        while max_iterations == 0 or self.session.state["iteration"] < max_iterations:
            self.session.state["iteration"] += 1
            self.session.state["phase"] = "executing"
            self.store.save_state(self.session)
            self.print_status(f"execution iteration {self.session.state['iteration']} started")
            execution_result = self.execute_once()
            self.store.append_event(self.session, "execution-result", execution_result)
            self.print_status(
                "execution iteration "
                f"{self.session.state['iteration']} returned {execution_result['status']}: "
                f"{truncate_label(execution_result['summary'], 120)}"
            )
            if execution_result["status"] == "COMPLETE":
                accepted, reason = self.evaluate_completion(execution_result)
                if not accepted:
                    self.session.state["completion_rejections"].append(reason)
                self.store.save_completion(self.session, execution_result, accepted, reason)
                if accepted:
                    self.print_status("completion accepted; Ralph run finished")
                    self.store.finish(self.session, "completed", execution_result["summary"])
                    return 0
                self.session.state["pending_feedback"] = reason
                self.print_status(f"completion rejected; replanning: {truncate_label(reason, 120)}")
            elif execution_result["status"] == "BLOCKED":
                self.store.save_completion(self.session, execution_result, False, execution_result["summary"])
                self.session.state["pending_feedback"] = (
                    f"execution blocked: {execution_result['summary']} | {execution_result['gate_reasoning']}"
                )
                self.print_status(f"execution blocked; replanning: {truncate_label(execution_result['summary'], 120)}")
            else:
                self.store.save_completion(self.session, execution_result, False, execution_result["summary"])
                self.session.state["pending_feedback"] = self.compose_replanning_feedback(execution_result)
                self.print_status("execution incomplete; replanning required")
            self.store.save_state(self.session)
            self.session.state["phase"] = "planning"
            self.print_status("planning started: replanning")
            planning_result = self.plan_once("replanning", self.session.state["pending_feedback"])
            self.validate_charter(planning_result)
            self.session.state["charter_version"] += 1
            replanning_feedback = self.session.state["pending_feedback"]
            self.session.state["pending_feedback"] = ""
            self.store.save_charter(
                self.session,
                planning_result,
                confirmed=self.session.state["seed_confirmed"],
                review_state="approved" if self.session.state["seed_confirmed"] else "draft",
                operator_feedback=replanning_feedback,
            )
            self.store.append_event(self.session, "planning-result", planning_result)
            self.store.save_state(self.session)
            self.print_status(f"planning completed: {truncate_label(planning_result['summary'], 120)}")
        raise RalphError(f"reached max_iterations={max_iterations} without verified completion")

    def ensure_thread(self) -> None:
        model = self.session.profile["model"]
        sandbox_mode = SANDBOX_BY_ACCESS_MODE[self.session.profile["thread_policy"]["access_mode"]]
        if self.session.state["thread_id"]:
            self.print_status(f"resuming thread {self.session.state['thread_id']}")
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
            self.print_status(f"thread resumed: {self.session.state['thread_id']}")
            return
        self.print_status("starting new thread")
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
        self.print_status(f"thread started: {self.session.state['thread_id']}")

    def plan_once(self, phase_name: str, feedback: str | None, render_output: bool = True) -> dict[str, Any]:
        return self.run_turn(
            phase_name=phase_name,
            prompt=self.build_planning_prompt(phase_name, feedback),
            schema=self.schema_catalog.model_schema(self.session.profile["planning"]["output_schema_id"]),
            collaboration_mode=self.make_collaboration_mode(
                self.session.profile["planning"]["mode"],
                self.session.profile["planning"]["reasoning_effort"],
                self.planning_instructions(),
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
        self.print_status(f"{phase_name}: turn started {turn_id}")
        raw_items: list[dict[str, Any]] = []
        thread_items: list[dict[str, Any]] = []
        buffered_deltas: list[str] = []
        turn_started_at = self.monotonic_func()
        next_heartbeat_at = turn_started_at + TURN_IDLE_HEARTBEAT_SECS
        while True:
            event = self.client.next_event(timeout=0.1)
            if event is None:
                self.client.raise_if_unavailable("while waiting for turn events")
                current_time = self.monotonic_func()
                if current_time >= next_heartbeat_at:
                    elapsed_seconds = max(1, int(current_time - turn_started_at))
                    self.terminal_reporter.wait(phase_name, elapsed_seconds)
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
                    buffered_deltas.append(delta)
                continue
            if method == "rawResponseItem/completed" and params.get("turnId") == turn_id:
                raw_items.append(params.get("item", {}))
                continue
            if method == "item/completed" and params.get("turnId") == turn_id:
                thread_items.append(params.get("item", {}))
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
        final_output = self.extract_final_output(raw_items, thread_items, schema)
        if render_output:
            if buffered_deltas:
                streamed_text = "".join(buffered_deltas).strip()
                if streamed_text:
                    self.render_model_output(phase_name, final_output, streamed_text)
            else:
                self.render_model_output(phase_name, final_output, "")
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
            f"{phase_name}: turn completed {turn_id} -> "
            f"{final_output.get('status', 'UNKNOWN')}: {truncate_label(final_output.get('summary', ''), 120)}"
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

    @staticmethod
    def extract_final_output(
        raw_items: list[dict[str, Any]],
        thread_items: list[dict[str, Any]],
        schema: dict[str, Any],
    ) -> dict[str, Any]:
        candidate_texts: list[str] = []
        seen_item_types: list[str] = []
        for item in raw_items:
            seen_item_types.append(f"raw:{item.get('type', 'unknown')}")
            if item.get("type") != "message":
                continue
            if item.get("role") not in {"assistant", "model"}:
                continue
            if item.get("phase") not in {None, "final_answer"}:
                continue
            text = "".join(
                content.get("text", "")
                for content in item.get("content", [])
                if content.get("type") == "output_text"
            ).strip()
            if text:
                candidate_texts.append(text)
        for item in thread_items:
            item_type = item.get("type", "unknown")
            seen_item_types.append(f"thread:{item_type}")
            if item_type in {"agentMessage", "plan"} and item.get("text"):
                candidate_texts.append(item["text"].strip())
        for text in reversed(candidate_texts):
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                validate_subset(schema, parsed)
                return parsed
        item_summary = ", ".join(seen_item_types[-10:]) if seen_item_types else "none"
        raise RalphError(
            "turn completed without a parseable final structured response "
            f"(seen items: {item_summary})"
        )

    def validate_charter(self, planning_result: dict[str, Any]) -> dict[str, Any]:
        charter_policy = self.session.profile["charter_policy"]
        charter = planning_result.get("charter")
        if not isinstance(charter, dict):
            raise RalphError("planner did not return a charter object")
        workstreams = charter.get("workstreams")
        if not isinstance(workstreams, list) or len(workstreams) < charter_policy["min_workstreams"]:
            raise RalphError("planner charter is too narrow")
        seen_ids: set[str] = set()
        for workstream in workstreams:
            identifier = workstream.get("id")
            if not identifier or not isinstance(identifier, str):
                raise RalphError("planner charter contains a workstream with no id")
            if identifier in seen_ids:
                raise RalphError(f"planner charter reused workstream id: {identifier}")
            seen_ids.add(identifier)
            if charter_policy["require_adjacent_surfaces"] and not workstream.get("required_adjacent_surfaces"):
                raise RalphError(f"workstream {identifier} is missing adjacent surfaces")
            if charter_policy["require_validation_for_each_workstream"] and not workstream.get("validation"):
                raise RalphError(f"workstream {identifier} is missing validation obligations")
        if charter_policy["require_validation_categories"] and not charter.get("validation_categories"):
            raise RalphError("planner charter is missing validation categories")
        return charter

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
            self.print_status("waiting for plan review")
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
            self.print_status(f"planning started: review revision v{self.session.state['charter_version'] + 1}")
            planning_result = self.plan_once("planning review", feedback, render_output=False)
            self.validate_charter(planning_result)
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
            self.print_status(f"planning completed: {truncate_label(planning_result['summary'], 120)}")

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
        self.print_status(status_message)

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

            Your job is to broaden the task into a strong execution charter before implementation.
            You are running in real Codex Plan Mode. The controller may ask you to revise the plan multiple times.
            Widen narrow local fixes into holistic workstreams, adjacent-surface checks, and validation obligations.
            Do not optimize for fast completion. Optimize for the strongest final result.

            Rules:
            - Never call update_plan. That tool is not allowed in this Plan Mode flow.
            - Use only plan-safe, non-mutating exploration while planning.
            - If critical intent is missing, use request_user_input rather than ad hoc prose prompts.
            - Ralph updates the plan by starting another planning turn with feedback, not by using update_plan.
            - Produce multiple meaningful workstreams when the task supports it.
            - Every workstream must name adjacent surfaces and validation obligations.
            - Prefer root-cause and system-level improvements over local patching when the task benefits from them.
            - Output only a schema-valid JSON object.
            """
        ).strip()

    def execution_instructions(self) -> str:
        return dedent(
            """
            You are the executor inside Ralph Codex.

            Implement against Ralph's full charter, not just the most recent local change.
            Only report COMPLETE when the whole job is truly complete and the result is holistic.
            Output only a schema-valid JSON object.
            """
        ).strip()

    def build_planning_prompt(self, phase_name: str, feedback: str | None) -> str:
        sections = [
            f"# Ralph Planning Phase: {phase_name}",
            "",
            "## Ralph Plan Mode Contract",
            "- You are in real Plan Mode for this turn.",
            "- Do not call update_plan.",
            "- Use non-mutating exploration only.",
            "- If you truly need operator input, request it through request_user_input.",
            "- Plan revisions happen through repeated Ralph planning turns with controller feedback.",
            "",
            "## Task",
            self.session.task["message_text"].strip(),
        ]
        review_history = self.render_review_history()
        if review_history:
            sections.extend(["", "## Review History", review_history])
        if self.session.charter_record:
            sections.extend(
                ["", "## Current Charter", json.dumps(self.session.charter_record["charter"], indent=2, sort_keys=True)]
            )
        if self.session.completion_record.get("last_result"):
            sections.extend(
                [
                    "",
                    "## Last Execution Result",
                    json.dumps(self.session.completion_record["last_result"], indent=2, sort_keys=True),
                ]
            )
        if feedback:
            sections.extend(["", "## Controller Feedback", feedback.strip()])
        return "\n".join(sections).strip() + "\n"

    def build_execution_prompt(self, feedback: str | None) -> str:
        if not self.session.charter_record:
            raise RalphError("execution cannot start before a charter is recorded")
        sections = [
            "# Ralph Execution Phase",
            "",
            "## Current Charter",
            json.dumps(self.session.charter_record["charter"], indent=2, sort_keys=True),
            "",
            "## Task",
            self.session.task["message_text"].strip(),
        ]
        if feedback:
            sections.extend(["", "## Controller Feedback", feedback.strip()])
        prompt = "\n".join(sections).strip() + "\n"
        max_prompt_chars = self.session.profile["execution"]["max_prompt_chars"]
        if max_prompt_chars and len(prompt) > max_prompt_chars:
            current_charter = json.dumps(self.session.charter_record["charter"], indent=2, sort_keys=True)
            task_text = self.session.task["message_text"].strip()
            feedback_text = feedback.strip() if feedback else ""
            raise RalphError(
                "execution prompt exceeds "
                f"max_prompt_chars={max_prompt_chars}: total={len(prompt)} "
                f"(charter={len(current_charter)}, task={len(task_text)}, feedback={len(feedback_text)})"
            )
        return prompt

    def compose_replanning_feedback(self, execution_result: dict[str, Any]) -> str:
        gaps = execution_result.get("remaining_gaps") or []
        gap_text = ", ".join(gaps) if gaps else "none reported"
        return (
            f"Execution is not complete. Summary: {execution_result['summary']}. "
            f"Remaining gaps: {gap_text}. "
            f"Next step proposed by the model: {execution_result['next_step']}."
        )

    def evaluate_completion(self, execution_result: dict[str, Any]) -> tuple[bool, str]:
        completion_policy = self.session.profile["completion_policy"]
        if execution_result.get("status") != "COMPLETE":
            return False, "model did not report COMPLETE"
        if not self.session.charter_record:
            return False, "no charter recorded"
        updates = execution_result.get("workstream_updates") or []
        update_map = {entry.get("id"): entry for entry in updates}
        missing = []
        disallowed_deferred = []
        for workstream in self.session.charter_record["charter"].get("workstreams", []):
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
            required_validation = set(self.session.charter_record["charter"].get("validation_categories", []))
            completed_validation = set(execution_result.get("validation_completed") or [])
            missing_validation = sorted(required_validation - completed_validation)
            if missing_validation:
                return False, f"validation categories remain incomplete: {', '.join(missing_validation)}"
        return True, ""

    @staticmethod
    def make_text_input(text: str) -> dict[str, Any]:
        return {"type": "text", "text": text, "text_elements": []}

    def make_collaboration_mode(self, mode: str, effort: str, developer_instructions: str) -> dict[str, Any]:
        model = self.session.state["model"] or self.session.profile["model"]
        return {
            "mode": mode,
            "settings": {
                "model": model,
                "reasoning_effort": effort,
                "developer_instructions": developer_instructions,
            },
        }

    def print_stream(self, text: str) -> None:
        self.terminal_reporter.model_text(self.session.state.get("phase", "model"), text)

    def print_status(self, text: str) -> None:
        self.terminal_reporter.status(text)

    def render_model_output(self, phase_name: str, final_output: dict[str, Any], streamed_text: str) -> None:
        self.terminal_reporter.model_result(phase_name, final_output)
        normalized = " ".join(streamed_text.split())
        if not normalized:
            return
        try:
            parsed = json.loads(normalized)
        except json.JSONDecodeError:
            parsed = None
        if parsed == final_output:
            return
        self.terminal_reporter.model_text(phase_name, normalized)

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
        reporter.status(f"run started: session={session.session_id} mode={invocation_mode}")
        client = SubprocessAppServerClient(runtime_config, event_recorder, session_log=session_log)
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
        reporter.status(f"run completed: {truncate_label(summary, 120)}")
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
        reporter.status(f"aborted. resume session with: {resume_command}")
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
