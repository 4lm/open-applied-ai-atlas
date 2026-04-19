#!/usr/bin/env python3
"""Evaluate Ralph benchmark result bundles against durable repo-owned fixtures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SUITE = REPO_ROOT / "evals" / "ralph" / "suites" / "quality-first.json"
DEFAULT_RESULTS_ROOT = REPO_ROOT / ".codex" / "ralph-codex" / "eval-results"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize Ralph benchmark sessions.")
    parser.add_argument("--suite", default=str(DEFAULT_SUITE), help="Benchmark suite JSON file.")
    parser.add_argument(
        "--results-dir",
        default=str(DEFAULT_RESULTS_ROOT),
        help="Root directory containing Ralph eval result bundles keyed by case id.",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def summarize_result_bundle(case: dict[str, Any], fixture: dict[str, Any], bundle_dir: Path) -> dict[str, Any]:
    result_path = bundle_dir / "result.json"
    if not result_path.exists():
        return {"status": "missing-result"}
    result = load_json(result_path)
    metrics = result.get("metrics") or {}
    grades = result.get("grades") or {}
    expected = fixture.get("expected") or {}
    checks = {
        "require_trace_grade": (not expected.get("require_trace_grade")) or bool(grades.get("trace_grade")),
        "require_evaluation_phase": (not expected.get("require_evaluation_phase")) or bool(metrics.get("evaluation_results", 0)),
        "require_search_activity": (not expected.get("require_search_activity")) or bool(metrics.get("search_activity_events", 0)),
    }
    return {
        "status": "ok",
        "accepted": bool(result.get("accepted", False)),
        "trace_grade": grades.get("trace_grade", ""),
        "metrics": metrics,
        "checks": checks,
    }


def main() -> int:
    args = parse_args()
    suite_path = Path(args.suite)
    suite = load_json(suite_path)
    results_root = Path(args.results_dir)
    rows: list[dict[str, Any]] = []
    for case in suite.get("cases", []):
        case_id = str(case.get("case_id", "")).strip()
        label = str(case.get("label", case_id or "case")).strip()
        fixture_ref = str(case.get("fixture", "")).strip()
        if not case_id or not fixture_ref:
            rows.append({"label": label, "status": "invalid-case"})
            continue
        fixture = load_json((suite_path.parent.parent / fixture_ref).resolve())
        rows.append({"label": label, "case_id": case_id, **summarize_result_bundle(case, fixture, results_root / case_id)})
    print(json.dumps({"suite": str(suite_path), "cases": rows}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
