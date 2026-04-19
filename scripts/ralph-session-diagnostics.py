#!/usr/bin/env python3
"""Summarize local Ralph session diagnostics from .codex runtime state."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SESSION_ROOT = REPO_ROOT / ".codex" / "ralph-codex" / "sessions"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize Ralph session diagnostics.")
    parser.add_argument(
        "--session-root",
        default=str(DEFAULT_SESSION_ROOT),
        help="Root directory containing Ralph session folders.",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def summarize_session(session_dir: Path) -> dict[str, Any]:
    completion_path = session_dir / "completion.json"
    events_path = session_dir / "events.jsonl"
    charter_path = session_dir / "charter.json"
    if not completion_path.exists():
        return {"status": "missing"}
    completion = load_json(completion_path)
    events = load_jsonl(events_path)
    charter = load_json(charter_path) if charter_path.exists() else {}
    event_counts: dict[str, int] = {}
    for entry in events:
        event_type = str(entry.get("event_type", ""))
        event_counts[event_type] = event_counts.get(event_type, 0) + 1
    last_result = completion.get("last_result") or {}
    return {
        "status": "ok",
        "accepted": completion.get("accepted", False),
        "last_reason": completion.get("last_reason", ""),
        "last_status": last_result.get("status", ""),
        "remaining_gaps": len(last_result.get("remaining_gaps") or []),
        "planning_results": event_counts.get("planning-result", 0),
        "execution_results": event_counts.get("execution-result", 0),
        "evaluation_results": event_counts.get("evaluation-result", 0),
        "search_activity_events": event_counts.get("turn-search-activity", 0),
        "charter_version": charter.get("charter_version", 0),
    }


def main() -> int:
    args = parse_args()
    session_root = Path(args.session_root)
    rows: list[dict[str, Any]] = []
    if session_root.exists():
        for session_dir in sorted(path for path in session_root.iterdir() if path.is_dir()):
            rows.append({"session_id": session_dir.name, **summarize_session(session_dir)})
    print(json.dumps({"session_root": str(session_root), "sessions": rows}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
