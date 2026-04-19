import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from datetime import datetime, timezone
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "ralph-codex.py"
SPEC = importlib.util.spec_from_file_location("ralph_codex", SCRIPT_PATH)
ralph_codex = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = ralph_codex
SPEC.loader.exec_module(ralph_codex)
DEFAULT_MAX_EXECUTION_PROMPT_CHARS = ralph_codex.load_profile(
    ralph_codex.SchemaCatalog(ralph_codex.SCHEMA_FILES),
    None,
)["execution"]["max_prompt_chars"]


class FakeClient:
    def __init__(self, request_results, events):
        self.request_results = request_results
        self.events = list(events)
        self.sent_results = []
        self.sent_errors = []
        self.requests = []

    def start(self):
        return None

    def close(self):
        return None

    def request(self, method, params):
        self.requests.append((method, params))
        key = (method, len([item for item in self.requests if item[0] == method]))
        if key in self.request_results:
            return self.request_results[key]
        return self.request_results[method]

    def next_event(self, timeout=0.1):
        if self.events:
            return self.events.pop(0)
        return None

    def send_result(self, request_id, result):
        self.sent_results.append((request_id, result))

    def send_error(self, request_id, code, message, data=None):
        self.sent_errors.append((request_id, code, message, data))

    def diagnostic_error(self, message):
        return message

    def raise_if_unavailable(self, context):
        return None


class FakeProcess:
    def __init__(self, exit_code=None):
        self.stdin = io.StringIO()
        self._exit_code = exit_code

    def poll(self):
        return self._exit_code


class FakeTTYStream(io.StringIO):
    def isatty(self):
        return True


class CaptureReporter:
    def __init__(self, verbose, stdout=None, stderr=None):
        self.verbose = verbose
        self.stdout = stdout or io.StringIO()
        self.stderr = stderr or io.StringIO()

    def status(self, message, badge="STARTING", tone="status"):
        self.stdout.write(f"{badge} {message}\n")

    def event(self, message, tone="event"):
        self.stderr.write(message + "\n")

    def wait(self, phase_name, elapsed_seconds, command_rows=None, badge="WORKING"):
        self.stdout.write(f"{badge} {phase_name} {elapsed_seconds}\n")

    def tool(self, detail, stream_name="stderr"):
        stream = self.stdout if stream_name == "stdout" else self.stderr
        stream.write(f"TOOL {detail}\n")

    def prompt(self, message):
        self.stderr.write(message + "\n")

    def approval_prompt(self, message):
        self.stdout.write(message + "\n")

    def console_input(self, text):
        return None

    def command_trace_context(self, trace_rows):
        self.stdout.write(f"trace {len(trace_rows)}\n")

    def review_diff(self, title, detail_lines):
        self.stdout.write(f"{title}: {len(detail_lines)}\n")

    def model_result(self, phase_name, payload, full=False):
        self.stdout.write(f"{phase_name} result\n")

    def model_text(self, phase_name, text):
        self.stdout.write(text + "\n")

    def stream_model_text(self, phase_name, text):
        self.stdout.write(text)
        return True

    def finish_model_text_stream(self):
        return None

    def verbose_trace(self, event_type, payload):
        return None

    def finish_stdout_line(self):
        return None


class RalphCodexTests(unittest.TestCase):
    def make_temp_root(self):
        tempdir = tempfile.TemporaryDirectory()
        root = Path(tempdir.name)
        return tempdir, root

    def make_schema_catalog(self):
        return ralph_codex.SchemaCatalog(ralph_codex.SCHEMA_FILES)

    def make_store(self, root):
        return ralph_codex.SessionStore(root / ".codex" / "ralph-codex", self.make_schema_catalog())

    def default_profile(self):
        return ralph_codex.load_profile(self.make_schema_catalog(), None)

    def make_profile(self):
        profile = self.default_profile()
        profile["seed_policy"]["require_confirmation"] = False
        profile["seed_policy"]["auto_confirm"] = True
        profile["runtime_limits"]["max_iterations"] = 5
        return profile

    def make_task(self):
        return {
            "message_source_kind": "inline",
            "message_source_label": "inline: test task",
            "message_text": "Test message",
        }

    def make_session(self, root):
        store = self.make_store(root)
        session = store.create_session(root, self.make_task(), self.make_profile())
        return store, session

    def make_reporter(self, verbose=False, stdout=None, stderr=None):
        return ralph_codex.TerminalReporter(
            verbose=verbose,
            stdout=stdout or io.StringIO(),
            stderr=stderr or io.StringIO(),
        )

    def make_event_recorder(self, store, session, verbose=False, stdout=None, stderr=None, reporter=None):
        return ralph_codex.EventRecorder(
            store,
            session,
            verbose=verbose,
            reporter=reporter,
            stdout=stdout or io.StringIO(),
            stderr=stderr or io.StringIO(),
        )

    def make_controller(
        self,
        root,
        client=None,
        session=None,
        input_func=lambda _: "yes",
        verbose=False,
        stdout=None,
        stderr=None,
        reporter=None,
        monotonic_func=None,
    ):
        store, built_session = self.make_session(root)
        session = session or built_session
        client = client or FakeClient({}, [])
        runtime_config = ralph_codex.RuntimeConfig(workdir=root, state_root=store.root)
        reporter = reporter or self.make_reporter(verbose=verbose, stdout=stdout, stderr=stderr)
        event_recorder = self.make_event_recorder(store, session, verbose=verbose, reporter=reporter)
        return ralph_codex.RalphController(
            runtime_config,
            client,
            event_recorder,
            store,
            self.make_schema_catalog(),
            session,
            input_func=input_func,
            terminal_reporter=reporter,
            monotonic_func=monotonic_func or (lambda: 0.0),
        )

    def broad_charter(self):
        return {
            "goal": "Refactor Ralph holistically",
            "success_criteria": ["controller exists", "tests exist", "docs updated"],
            "validation_categories": ["unit", "integration", "gating"],
            "explicit_deferrals": [],
            "workstreams": [
                {
                    "id": "W1",
                    "title": "Controller",
                    "goal": "Replace shell loop",
                    "required_adjacent_surfaces": ["scripts", "schemas"],
                    "validation": ["unit tests"],
                    "status": "planned",
                },
                {
                    "id": "W2",
                    "title": "Docs",
                    "goal": "Update guidance",
                    "required_adjacent_surfaces": ["README", "AGENTS"],
                    "validation": ["doc review"],
                    "status": "planned",
                },
                {
                    "id": "W3",
                    "title": "State",
                    "goal": "Add sessions",
                    "required_adjacent_surfaces": [".codex/ralph-codex/sessions"],
                    "validation": ["session tests"],
                    "status": "planned",
                },
            ],
        }

    def save_charter(self, controller):
        planning_result = self.planning_result_payload()
        controller.session.state["charter_version"] = 1
        controller.store.save_charter(
            controller.session,
            planning_result,
            confirmed=True,
            review_state="approved",
        )

    def planning_result_payload(self, summary="ok", charter=None):
        charter = charter or self.broad_charter()
        program_board = ralph_codex.legacy_program_board_from_charter(charter)
        return {
            "status": "CHARTER_READY",
            "summary": summary,
            "broadening_rationale": "wide",
            "research": {
                "status": "completed",
                "search_strategy": "Compare repo facts with official references and current behavior.",
                "findings": ["Captured the bounded tranche and supporting sources."],
                "sources": [
                    {
                        "title": "Primary source A",
                        "url": "https://example.com/a",
                        "source_type": "primary",
                        "used_for": "baseline",
                    },
                    {
                        "title": "Primary source B",
                        "url": "https://example.com/b",
                        "source_type": "primary",
                        "used_for": "comparison",
                    },
                    {
                        "title": "Secondary source C",
                        "url": "https://example.com/c",
                        "source_type": "secondary",
                        "used_for": "context",
                    },
                    {
                        "title": "Secondary source D",
                        "url": "https://example.com/d",
                        "source_type": "secondary",
                        "used_for": "adjacent context",
                    },
                ],
                "open_questions": [],
            },
            "program_board": program_board,
            "active_milestone": {
                "milestone_id": "legacy-milestone",
                "rationale": "Focus the next tranche on the current milestone.",
                "success_checkpoint": "Land the highest-signal milestone slice.",
                "evidence_focus": ["baseline", "comparison"],
                "target_files": ["scripts/ralph-codex.py", "RALPH_CONTROLLER.md"],
                "validation": ["unit", "docs"],
            },
            "current_tranche": {
                "batch_id": "batch-1",
                "milestone_id": "legacy-milestone",
                "workstream_ids": ["W1", "W2"],
                "target_files": ["scripts/ralph-codex.py", "RALPH_CONTROLLER.md"],
                "intended_outcome": "Land the next bounded tranche without widening scope.",
                "validation": ["unit", "docs"],
            },
            "next_step": "execute",
            "gate_reasoning": "safe",
        }

    def execution_result_payload(self, status="IN_PROGRESS", summary="working", remaining_gaps=None, touched_files=None):
        return {
            "status": status,
            "summary": summary,
            "evidence": ["progress"],
            "verification": {
                "status": "completed" if status == "COMPLETE" else "not_needed",
                "scope": "Verification recorded for the current tranche.",
                "findings": ["Verified the relevant execution claims."],
                "sources": [
                    {
                        "title": "Verification source A",
                        "url": "https://example.com/verify-a",
                        "source_type": "primary",
                        "used_for": "verification",
                    },
                    {
                        "title": "Verification source B",
                        "url": "https://example.com/verify-b",
                        "source_type": "secondary",
                        "used_for": "verification",
                    },
                    {
                        "title": "Verification source C",
                        "url": "https://example.com/verify-c",
                        "source_type": "secondary",
                        "used_for": "verification corroboration",
                    },
                ] if status == "COMPLETE" else [],
            },
            "touched_files": touched_files or ["scripts/ralph-codex.py"],
            "created_files": [],
            "off_tranche_justifications": [],
            "quality_claims": {
                "tranche_followed": True,
                "user_facing_outcome": "Improved the current tranche target cleanly.",
                "avoided_meta_artifacts": True,
                "repeated_heading_risk": "low",
            },
            "milestone_progress": {
                "milestone_id": "legacy-milestone",
                "criteria_met": ["controller exists"] if status == "COMPLETE" else [],
                "criteria_remaining": [] if status == "COMPLETE" else ["docs updated"],
                "novelty_notes": ["Added net-new milestone progress."] if status != "BLOCKED" else [],
                "completion_notes": ["Milestone criteria are moving toward completion."],
            },
            "acceptance_artifacts": ["scripts/ralph-codex.py"] if status == "COMPLETE" else [],
            "evidence_updates": [
                {
                    "claim": "Execution is moving the milestone forward.",
                    "url": "https://example.com/evidence",
                    "source_type": "secondary",
                    "used_for": "execution progress",
                    "status": "confirmed",
                }
            ],
            "workstream_updates": [{"id": "W1", "status": "in_progress" if status != "COMPLETE" else "done", "evidence": ["ok"]}],
            "remaining_gaps": remaining_gaps if remaining_gaps is not None else ["docs"],
            "validation_completed": ["unit"],
            "explicit_deferrals": [],
            "next_step": "continue",
            "next_tranche_recommendation": "Keep the next tranche bounded.",
            "gate_reasoning": "more work" if status != "COMPLETE" else "safe",
        }

    def evaluation_result_payload(self, disposition="repair_same_tranche", summary="tighten the tranche"):
        return {
            "disposition": disposition,
            "milestone_status": "accepted" if disposition == "accept" else "open",
            "acceptance_criteria_met": ["controller exists"] if disposition == "accept" else [],
            "evidence_sufficiency": "sufficient" if disposition == "accept" else "partial",
            "novelty_assessment": "The latest tranche added useful novelty." if disposition != "blocked" else "No useful novelty landed.",
            "recommended_scope_change": "advance_milestone" if disposition == "accept" else "stay_on_tranche",
            "worker_fanout_recommended": False,
            "summary": summary,
            "repair_instructions": ["Tighten the current tranche and verify remaining gaps directly."],
            "evidence_findings": ["Evidence is still incomplete for the current tranche."],
            "confidence": "high",
            "research_refresh_required": False,
            "gate_reasoning": "Prefer bounded repair before widening scope.",
        }

    def test_parse_command_defaults_to_help(self):
        parser, command = ralph_codex.parse_command([])
        self.assertIsNotNone(parser)
        self.assertEqual(command.kind, "help")

    def test_parse_command_accepts_message_and_profile(self):
        _, command = ralph_codex.parse_command(["--message", "fix this", "--profile", "profile.json"])
        self.assertEqual(command.kind, "message")
        self.assertEqual(command.value, "fix this")
        self.assertEqual(command.profile_path.name, "profile.json")
        self.assertFalse(command.verbose)

    def test_parse_command_accepts_verbose(self):
        _, command = ralph_codex.parse_command(["--verbose", "--resume"])
        self.assertEqual(command.kind, "resume")
        self.assertTrue(command.verbose)

    def test_parse_command_accepts_file(self):
        _, command = ralph_codex.parse_command(["--file", "task.md"])
        self.assertEqual(command.kind, "file")
        self.assertEqual(command.value, "task.md")

    def test_parse_command_accepts_sessions_count(self):
        _, command = ralph_codex.parse_command(["--sessions", "7"])
        self.assertEqual(command.kind, "sessions")
        self.assertEqual(command.value, "7")

    def test_parse_command_accepts_resume_without_target(self):
        _, command = ralph_codex.parse_command(["--resume"])
        self.assertEqual(command.kind, "resume")
        self.assertIsNone(command.value)

    def test_parse_command_rejects_profile_without_message_or_file(self):
        with self.assertRaises(SystemExit):
            ralph_codex.parse_command(["--resume", "--profile", "profile.json"])

    def test_parse_command_rejects_legacy_prompt_and_config_flags(self):
        with self.assertRaises(SystemExit):
            ralph_codex.parse_command(["--prompt", "fix this"])
        with self.assertRaises(SystemExit):
            ralph_codex.parse_command(["--file", "task.md", "--config", "profile.json"])

    def test_parse_command_rejects_zero_sessions_count(self):
        with self.assertRaises(SystemExit):
            ralph_codex.parse_command(["--sessions", "0"])

    def test_direct_script_help_runs_via_shebang(self):
        completed = subprocess.run(
            [str(SCRIPT_PATH), "--help"],
            cwd=SCRIPT_PATH.parents[1],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("Universal, session-driven Ralph controller for Codex.", completed.stdout)

    def test_new_session_id_uses_utc_millis_and_uid(self):
        moment = datetime(2026, 4, 19, 12, 30, 45, 123000, tzinfo=timezone.utc)
        session_id = ralph_codex.new_session_id(moment, "a1b2c3d4e5f6")
        self.assertEqual(session_id, "20260419T123045123Z_a1b2c3d4e5f6")
        self.assertTrue(ralph_codex.SESSION_ID_RE.match(session_id))

    def test_schema_files_use_expected_versions(self):
        for path in sorted(ralph_codex.SCHEMA_ROOT.rglob("*.schema.json")):
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(payload["schema_version"], "0.1.0")
            self.assertIn("schema_id", payload)
            self.assertIn("-v0.1.0.schema.json", path.name)

    def test_schema_files_all_live_under_ralph_codex_schema_dir(self):
        expected_root = ralph_codex.SCHEMA_ROOT / "ralph-codex"
        for path in ralph_codex.SCHEMA_FILES.values():
            self.assertEqual(path.parent, expected_root)
        self.assertEqual(
            ralph_codex.SCHEMA_FILES[ralph_codex.PROFILE_SCHEMA_ID],
            expected_root / "profile-v0.1.0.schema.json",
        )

    def test_default_profile_validates_against_profile_schema(self):
        profile = self.default_profile()
        self.make_schema_catalog().validate(ralph_codex.PROFILE_SCHEMA_ID, profile)
        self.assertEqual(profile["profile_name"], "restricted")
        self.assertEqual(profile["thread_policy"]["access_mode"], "restricted")
        self.assertEqual(profile["runtime_limits"]["max_iterations"], 0)
        self.assertEqual(profile["execution"]["max_prompt_chars"], DEFAULT_MAX_EXECUTION_PROMPT_CHARS)
        self.assertEqual(profile["planning"]["reasoning_effort"], "xhigh")
        self.assertEqual(profile["execution"]["reasoning_effort"], "xhigh")
        self.assertEqual(profile["planning"]["model"], "gpt-5.4")
        self.assertEqual(profile["evaluation"]["model"], "gpt-5.4")
        self.assertEqual(profile["execution"]["model"], "gpt-5.4")
        self.assertEqual(profile["research_policy"]["mode"], "required")
        self.assertIn("loop_policy", profile)

    def test_default_profile_loads_from_restricted_profile_path(self):
        profile = self.default_profile()
        self.assertEqual(ralph_codex.DEFAULT_PROFILE_PATH.name, "restricted.json")
        self.assertEqual(profile["profile_name"], "restricted")

    def test_shipped_profiles_use_long_run_quality_defaults(self):
        schema_catalog = self.make_schema_catalog()
        restricted = ralph_codex.load_profile(schema_catalog, ralph_codex.REPO_ROOT / "profiles" / "restricted.json")
        unrestricted = ralph_codex.load_profile(
            schema_catalog,
            ralph_codex.REPO_ROOT / "profiles" / "dangerously-unrestricted.json",
        )
        self.assertFalse(restricted["completion_policy"]["allow_deferred_workstreams"])
        self.assertEqual(restricted["quality_policy"]["progress_checkpoint_mode"], "record_only_after_seed")
        self.assertEqual(restricted["loop_policy"]["planning_max_prompt_chars"], 22000)
        self.assertEqual(restricted["execution"]["max_prompt_chars"], 16000)
        self.assertEqual(restricted["memory_policy"]["max_execution_memory_entries"], 16)
        self.assertEqual(restricted["memory_policy"]["max_evidence_registry_entries"], 128)
        self.assertEqual(unrestricted["thread_policy"]["access_mode"], "dangerously-unrestricted")
        self.assertEqual(unrestricted["loop_policy"]["planning_max_prompt_chars"], 24000)
        self.assertEqual(unrestricted["execution"]["max_prompt_chars"], 18000)
        self.assertEqual(unrestricted["worker_policy"]["max_parallel_workers"], 3)
        self.assertNotIn("disjoint_execution", unrestricted["worker_policy"]["allowed_roles"])

    def test_load_profile_backfills_legacy_profile_fields(self):
        with tempfile.TemporaryDirectory() as tempdir:
            path = Path(tempdir) / "profile.json"
            legacy = {
                "schema_id": ralph_codex.PROFILE_SCHEMA_ID,
                "schema_version": "0.1.0",
                "profile_name": "legacy",
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
                    "output_schema_id": ralph_codex.PLANNING_OUTPUT_SCHEMA_ID,
                },
                "execution": {
                    "mode": "default",
                    "reasoning_effort": "high",
                    "output_schema_id": ralph_codex.EXECUTION_OUTPUT_SCHEMA_ID,
                    "max_prompt_chars": 0,
                },
            }
            path.write_text(json.dumps(legacy), encoding="utf-8")
            loaded = ralph_codex.load_profile(self.make_schema_catalog(), path)
            self.assertEqual(loaded["schema_version"], "0.1.0")
            self.assertIn("research_policy", loaded)
            self.assertIn("tranche_policy", loaded)
            self.assertIn("quality_policy", loaded)
            self.assertIn("loop_policy", loaded)
            self.assertEqual(loaded["quality_policy"]["progress_checkpoint_mode"], "record_only_after_seed")
            self.assertEqual(loaded["memory_policy"]["max_skill_memory_entries"], 24)
            self.assertEqual(loaded["planning"]["model"], "gpt-5.4")
            self.assertEqual(loaded["evaluation"]["model"], "gpt-5.4")
            self.assertEqual(loaded["execution"]["model"], "gpt-5.4")

    def test_load_profile_removes_legacy_disjoint_execution_role(self):
        with tempfile.TemporaryDirectory() as tempdir:
            path = Path(tempdir) / "profile.json"
            legacy = self.default_profile()
            legacy["worker_policy"]["allowed_roles"] = [
                "research",
                "read_only_repo",
                "disjoint_execution",
                "evaluator_vote",
            ]
            path.write_text(json.dumps(legacy), encoding="utf-8")
            loaded = ralph_codex.load_profile(self.make_schema_catalog(), path)
            self.assertEqual(
                loaded["worker_policy"]["allowed_roles"],
                ["research", "read_only_repo", "evaluator_vote"],
            )

    def test_load_profile_normalizes_local_v0_2_0_profile_to_v0_1_0(self):
        with tempfile.TemporaryDirectory() as tempdir:
            path = Path(tempdir) / "profile.json"
            local_profile = self.default_profile()
            local_profile["schema_version"] = "0.2.0"
            path.write_text(json.dumps(local_profile), encoding="utf-8")
            loaded = ralph_codex.load_profile(self.make_schema_catalog(), path)
            self.assertEqual(loaded["schema_version"], "0.1.0")

    def test_load_profile_propagates_legacy_top_level_model_to_phase_models(self):
        with tempfile.TemporaryDirectory() as tempdir:
            path = Path(tempdir) / "profile.json"
            legacy = self.default_profile()
            legacy["model"] = "gpt-5.4-mini"
            for section_name in ("planning", "evaluation", "execution"):
                legacy[section_name].pop("model", None)
            path.write_text(json.dumps(legacy), encoding="utf-8")
            loaded = ralph_codex.load_profile(self.make_schema_catalog(), path)
            self.assertEqual(loaded["planning"]["model"], "gpt-5.4-mini")
            self.assertEqual(loaded["evaluation"]["model"], "gpt-5.4-mini")
            self.assertEqual(loaded["execution"]["model"], "gpt-5.4-mini")

    def test_normalize_session_state_renames_legacy_closure_score(self):
        session_id = "20260420T000000000Z_123456789abc"
        payload = {
            "schema_id": ralph_codex.SESSION_STATE_SCHEMA_ID,
            "schema_version": "0.1.0",
            "session_id": session_id,
            "started_at": "2026-04-20T00:00:00Z",
            "execution_memory": [
                {
                    "iteration": 1,
                    "summary": "Legacy iteration",
                    "novelty_score": 1.0,
                    "closure_score": 0.5,
                }
            ],
        }
        normalized = ralph_codex.normalize_payload_for_schema(ralph_codex.SESSION_STATE_SCHEMA_ID, payload)
        memory = normalized["execution_memory"][0]
        self.assertEqual(memory["acceptance_progress_score"], 0.5)
        self.assertNotIn("closure_score", memory)
        self.make_schema_catalog().validate(ralph_codex.SESSION_STATE_SCHEMA_ID, normalized)

    def test_normalize_completion_payload_renames_legacy_closure_notes(self):
        session_id = "20260420T000000000Z_123456789abc"
        payload = {
            "schema_id": ralph_codex.COMPLETION_SCHEMA_ID,
            "schema_version": "0.1.0",
            "session_id": session_id,
            "accepted": False,
            "last_result": {
                "status": "IN_PROGRESS",
                "summary": "Legacy result",
                "evidence": ["legacy"],
                "milestone_progress": {
                    "milestone_id": "legacy-milestone",
                    "criteria_met": [],
                    "criteria_remaining": ["docs updated"],
                    "novelty_notes": ["Legacy progress"],
                    "closure_notes": ["Legacy closure note"],
                },
            },
            "last_reason": "",
            "rejections": [],
            "updated_at": "2026-04-20T00:00:00Z",
        }
        normalized = ralph_codex.normalize_payload_for_schema(ralph_codex.COMPLETION_SCHEMA_ID, payload)
        progress = normalized["last_result"]["milestone_progress"]
        self.assertEqual(progress["completion_notes"], ["Legacy closure note"])
        self.assertNotIn("closure_notes", progress)
        self.make_schema_catalog().validate(ralph_codex.COMPLETION_SCHEMA_ID, normalized)

    def test_custom_profile_invalid_is_rejected(self):
        with tempfile.TemporaryDirectory() as tempdir:
            path = Path(tempdir) / "profile.json"
            invalid = self.default_profile()
            invalid["planning"]["reasoning_effort"] = "extreme"
            path.write_text(json.dumps(invalid), encoding="utf-8")
            with self.assertRaises(ralph_codex.RalphError):
                ralph_codex.load_profile(self.make_schema_catalog(), path)

    def test_custom_profile_rejects_invalid_thread_access_mode(self):
        with tempfile.TemporaryDirectory() as tempdir:
            path = Path(tempdir) / "profile.json"
            invalid = self.default_profile()
            invalid["thread_policy"]["access_mode"] = "unsafe"
            path.write_text(json.dumps(invalid), encoding="utf-8")
            with self.assertRaises(ralph_codex.RalphError):
                ralph_codex.load_profile(self.make_schema_catalog(), path)

    def test_custom_profile_rejects_negative_execution_prompt_limit(self):
        with tempfile.TemporaryDirectory() as tempdir:
            path = Path(tempdir) / "profile.json"
            invalid = self.default_profile()
            invalid["execution"]["max_prompt_chars"] = -1
            path.write_text(json.dumps(invalid), encoding="utf-8")
            with self.assertRaises(ralph_codex.RalphError):
                ralph_codex.load_profile(self.make_schema_catalog(), path)

    def test_session_store_initializes_structured_files_and_schemas(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        self.assertTrue(store.controller_state_path.exists())
        for name in [
            "session.json",
            "task.json",
            "profile.json",
            "session-state.json",
            "completion.json",
            "charter-history.jsonl",
            "turns.jsonl",
            "server-requests.jsonl",
            "events.jsonl",
        ]:
            path = session.session_dir / name
            self.assertTrue(path.exists())
            self.assertTrue(ralph_codex.adjacent_schema_path(path).exists())

    def test_ensure_jsonl_skips_rewriting_identical_adjacent_schema_copy(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store = self.make_store(root)
        path = store.sessions_log_path
        schema_copy = ralph_codex.adjacent_schema_path(path)
        schema_copy.chmod(0o444)
        store.ensure_jsonl(path, ralph_codex.RUN_HISTORY_LINE_SCHEMA_ID)
        self.assertTrue(schema_copy.exists())

    def test_list_run_rows_collapses_events_per_run(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        run_1 = ralph_codex.new_run_id(datetime(2026, 4, 19, 12, 0, 0, 0, tzinfo=timezone.utc), "a1b2c3d4e5f6")
        run_2 = ralph_codex.new_run_id(datetime(2026, 4, 19, 12, 1, 0, 0, tzinfo=timezone.utc), "0a1b2c3d4e5f")
        store.append_run_history(session, run_1, "run_started", "message", "run started")
        store.append_run_history(session, run_1, "run_failed", "message", "failed")
        store.append_run_history(session, run_2, "run_started", "resume", "run started")
        rows = store.list_run_rows()
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["index"], 1)
        self.assertEqual(rows[0]["outcome"], "failed")
        self.assertEqual(rows[1]["outcome"], "running")
        self.assertEqual(rows[1]["session_status"], "resumable")

    def test_list_run_rows_marks_aborted_runs(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        run_1 = ralph_codex.new_run_id(datetime(2026, 4, 19, 12, 0, 0, 0, tzinfo=timezone.utc), "a1b2c3d4e5f6")
        store.append_run_history(session, run_1, "run_started", "message", "run started")
        store.append_run_history(session, run_1, "run_aborted", "message", "aborted by operator")
        rows = store.list_run_rows()
        self.assertEqual(rows[0]["outcome"], "aborted")
        self.assertEqual(rows[0]["session_status"], "resumable")

    def test_resolve_resume_target_accepts_index_and_id(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        run_1 = ralph_codex.new_run_id(datetime(2026, 4, 19, 12, 0, 0, 0, tzinfo=timezone.utc), "a1b2c3d4e5f6")
        store.append_run_history(session, run_1, "run_started", "message", "run started")
        by_index = store.resolve_resume_target("1")
        by_id = store.resolve_resume_target(session.session_id)
        self.assertEqual(by_index.session_id, session.session_id)
        self.assertEqual(by_id.session_id, session.session_id)

    def test_resolve_resume_target_rejects_completed_session(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        store.finish(session, "completed", "done")
        with self.assertRaisesRegex(ralph_codex.RalphError, "cannot be resumed"):
            store.resolve_resume_target(session.session_id)

    def test_ensure_thread_uses_restricted_sandbox_by_default(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        client = FakeClient(
            {
                "thread/start": {
                    "thread": {"id": "thread-1", "status": {"type": "ready"}},
                    "model": "gpt-5.4",
                    "approvalPolicy": "never",
                    "sandbox": {"type": "workspace-write"},
                }
            },
            [],
        )
        controller = ralph_codex.RalphController(
            ralph_codex.RuntimeConfig(workdir=root, state_root=store.root),
            client,
            self.make_event_recorder(store, session),
            store,
            self.make_schema_catalog(),
            session,
        )
        controller.ensure_thread()
        method, params = client.requests[0]
        self.assertEqual(method, "thread/start")
        self.assertEqual(params["approvalPolicy"], "never")
        self.assertEqual(params["sandbox"], "workspace-write")

    def test_ensure_thread_uses_dangerously_unrestricted_when_configured(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        session.profile["thread_policy"]["access_mode"] = "dangerously-unrestricted"
        client = FakeClient(
            {
                "thread/start": {
                    "thread": {"id": "thread-1", "status": {"type": "ready"}},
                    "model": "gpt-5.4",
                    "approvalPolicy": "never",
                    "sandbox": {"type": "danger-full-access"},
                }
            },
            [],
        )
        controller = ralph_codex.RalphController(
            ralph_codex.RuntimeConfig(workdir=root, state_root=store.root),
            client,
            self.make_event_recorder(store, session),
            store,
            self.make_schema_catalog(),
            session,
        )
        controller.ensure_thread()
        method, params = client.requests[0]
        self.assertEqual(method, "thread/start")
        self.assertEqual(params["approvalPolicy"], "never")
        self.assertEqual(params["sandbox"], "danger-full-access")

    def test_request_fails_when_app_server_exits_before_responding(self):
        runtime_config = ralph_codex.RuntimeConfig(workdir=SCRIPT_PATH.parents[1], state_root=SCRIPT_PATH.parents[1])
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        client = ralph_codex.SubprocessAppServerClient(runtime_config, self.make_event_recorder(store, session))
        client.process = FakeProcess(exit_code=3)
        client._stderr_lines.append("fatal: app-server crashed")
        original_timeout = ralph_codex.APP_SERVER_REQUEST_TIMEOUT_SECS
        self.addCleanup(setattr, ralph_codex, "APP_SERVER_REQUEST_TIMEOUT_SECS", original_timeout)
        ralph_codex.APP_SERVER_REQUEST_TIMEOUT_SECS = 0.01
        with self.assertRaisesRegex(ralph_codex.RalphError, "exited with code 3"):
            client.request("turn/start", {})

    def test_subprocess_app_server_start_enables_search_when_configured(self):
        runtime_config = ralph_codex.RuntimeConfig(workdir=SCRIPT_PATH.parents[1], state_root=SCRIPT_PATH.parents[1])
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        client = ralph_codex.SubprocessAppServerClient(
            runtime_config,
            self.make_event_recorder(store, session),
            enable_search=True,
        )
        popen_calls = []

        class StubPopen:
            def __init__(self, cmd, **kwargs):
                popen_calls.append((cmd, kwargs))
                self.stdin = io.StringIO()
                self.stdout = io.StringIO()
                self.stderr = io.StringIO()

            def poll(self):
                return None

        with mock.patch.object(ralph_codex.shutil, "which", return_value="/usr/bin/codex"), mock.patch.object(
            ralph_codex.subprocess, "Popen", StubPopen
        ), mock.patch.object(ralph_codex.threading, "Thread", autospec=True) as thread_mock, mock.patch.object(
            ralph_codex.SubprocessAppServerClient, "request", return_value={"ok": True}
        ):
            client.start()

        self.assertTrue(popen_calls)
        self.assertEqual(
            popen_calls[0][0],
            [ralph_codex.CODEx_BIN, "--search", "app-server", "--listen", "stdio://"],
        )
        self.assertEqual(thread_mock.call_count, 2)

    def test_event_recorder_normal_notification_trims_large_output(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        recorder = self.make_event_recorder(store, session, verbose=False)
        recorder.record_notification(
            "rawResponseItem/completed",
            {
                "threadId": "thread-1",
                "turnId": "turn-1",
                "item": {
                    "type": "function_call_output",
                    "call_id": "call-1",
                    "output": "x" * 120,
                },
            },
        )
        events = store.read_jsonl(session.session_dir / "events.jsonl", ralph_codex.EVENT_LOG_LINE_SCHEMA_ID)
        self.assertEqual(events, [])

    def test_event_recorder_normal_console_is_human_readable(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        stderr = io.StringIO()
        reporter = self.make_reporter(verbose=False, stderr=stderr)
        recorder = self.make_event_recorder(store, session, reporter=reporter)
        recorder.record_client_event({"type": "stderr", "line": "fatal: app-server crashed"})
        console = stderr.getvalue()
        self.assertIn("app-server stderr: fatal: app-server crashed", console)
        self.assertIn("ERROR", console)
        self.assertNotIn('{"line"', console)

    def test_event_recorder_verbose_wire_keeps_raw_output(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        recorder = self.make_event_recorder(store, session, verbose=True)
        recorder.record_client_event(
            {
                "type": "wire",
                "payload": {
                    "method": "rawResponseItem/completed",
                    "params": {"item": {"type": "function_call_output", "output": "abc"}},
                },
            }
        )
        events = store.read_jsonl(session.session_dir / "events.jsonl", ralph_codex.EVENT_LOG_LINE_SCHEMA_ID)
        wire = events[-1]
        self.assertEqual(wire["event_type"], "wire")
        self.assertEqual(wire["payload"]["payload"]["params"]["item"]["output"], "abc")

    def test_event_recorder_verbose_console_caps_output_but_events_keep_full_wire(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        stderr = io.StringIO()
        reporter = self.make_reporter(verbose=True, stderr=stderr)
        recorder = self.make_event_recorder(store, session, verbose=True, reporter=reporter)
        long_output = "x" * 1400
        recorder.record_client_event(
            {
                "type": "wire",
                "payload": {
                    "method": "rawResponseItem/completed",
                    "params": {"item": {"type": "function_call_output", "output": long_output}},
                },
            }
        )
        console = stderr.getvalue()
        self.assertEqual(console, "")
        events = store.read_jsonl(session.session_dir / "events.jsonl", ralph_codex.EVENT_LOG_LINE_SCHEMA_ID)
        wire = events[-1]
        self.assertEqual(wire["payload"]["payload"]["params"]["item"]["output"], long_output)

    def test_event_recorder_verbose_keeps_traces_out_of_console(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        stderr = io.StringIO()
        recorder = self.make_event_recorder(store, session, verbose=True, stderr=stderr)
        recorder.record_rpc_request(3, "turn/start", {"threadId": "thread-1", "input": [], "outputSchema": {}})
        self.assertEqual(stderr.getvalue(), "")

    def test_terminal_reporter_uses_color_on_tty(self):
        stdout = FakeTTYStream()
        stderr = FakeTTYStream()
        reporter = ralph_codex.TerminalReporter(verbose=False, stdout=stdout, stderr=stderr)
        reporter.status("colored status")
        reporter.event("colored event")
        self.assertIn("\x1b[", stdout.getvalue())
        self.assertIn("\x1b[", stderr.getvalue())

    def test_terminal_reporter_full_model_result_does_not_truncate_seed_review(self):
        stdout = io.StringIO()
        reporter = self.make_reporter(stdout=stdout)
        long_summary = "This is a very long planning summary " * 20
        payload = {
            "status": "CHARTER_READY",
            "summary": long_summary.strip(),
            "broadening_rationale": "Wide enough for operator review.",
            "research": {
                "status": "completed",
                "search_strategy": "Review the repo and current contract.",
                "findings": ["Research captured enough grounding for review."],
                "sources": [
                    {
                        "title": "Primary source A",
                        "url": "https://example.com/a",
                        "source_type": "primary",
                        "used_for": "review",
                    },
                    {
                        "title": "Primary source B",
                        "url": "https://example.com/b",
                        "source_type": "primary",
                        "used_for": "review",
                    },
                    {
                        "title": "Secondary source C",
                        "url": "https://example.com/c",
                        "source_type": "secondary",
                        "used_for": "review",
                    }
                ],
                "open_questions": []
            },
            "charter": {
                "goal": "Review the whole charter before unattended execution.",
                "success_criteria": ["Criterion " + ("x" * 80)],
                "validation_categories": ["unit", "integration"],
                "explicit_deferrals": ["None"],
                "workstreams": [
                    {
                        "id": "WS1",
                        "title": "Audit",
                        "goal": "Inspect everything",
                        "required_adjacent_surfaces": ["docs/", "tests/"],
                        "validation": ["unit tests", "doc review"],
                        "status": "planned",
                    }
                ],
            },
            "current_tranche": {
                "batch_id": "batch-1",
                "workstream_ids": ["WS1"],
                "target_files": ["scripts/ralph-codex.py"],
                "intended_outcome": "Keep the next execution turn bounded.",
                "validation": ["unit tests", "doc review"]
            },
            "next_step": "Ask the operator for approval.",
            "gate_reasoning": "The operator must be able to read the full charter.",
        }
        reporter.model_result("initial planning", payload, full=True)
        console = stdout.getvalue()
        self.assertIn("This is a very long planning summary", console)
        self.assertNotIn("truncated for console", console)
        self.assertIn("goal:", console)
        self.assertIn("validation_categories:", console)
        self.assertIn("WS1: Audit", console)

    def test_session_store_extracts_command_trace_rows_for_turn(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        store.append_event(
            session,
            "notification",
            {
                "method": "item/started",
                "turn_id": "turn-1",
                "item": {
                    "type": "commandExecution",
                    "id": "call-1",
                    "command": "/bin/zsh -lc 'echo hi'",
                    "status": "inProgress",
                    "command_actions": 1,
                    "processId": "123",
                },
            },
        )
        store.append_event(
            session,
            "notification",
            {
                "method": "item/completed",
                "turn_id": "turn-1",
                "item": {
                    "type": "commandExecution",
                    "id": "call-1",
                    "command": "/bin/zsh -lc 'echo hi'",
                    "status": "completed",
                    "aggregated_output_chars": 17,
                    "command_actions": 1,
                    "processId": "123",
                },
            },
        )
        rows = store.command_trace_for_turn(session, "turn-1")
        self.assertEqual(
            rows,
            [
                {
                    "call_id": "call-1",
                    "command": "/bin/zsh -lc 'echo hi'",
                    "action": "",
                    "target": "",
                    "output_chars": 17,
                    "exit_code": None,
                    "duration_ms": None,
                    "process_id": "123",
                }
            ],
        )

    def test_session_store_deduplicates_identical_events(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        store.append_event(session, "notification", {"method": "turn/started", "turn": {"id": "turn-1", "status": "inProgress"}})
        store.append_event(session, "notification", {"method": "turn/started", "turn": {"id": "turn-1", "status": "inProgress"}})
        events = store.read_jsonl(session.session_dir / "events.jsonl", ralph_codex.EVENT_LOG_LINE_SCHEMA_ID)
        self.assertEqual(len(events), 1)

    def test_execute_run_keyboard_interrupt_marks_session_aborted_and_resumable(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        runtime_config = ralph_codex.RuntimeConfig(workdir=root, state_root=store.root)
        schema_catalog = self.make_schema_catalog()
        stdout = io.StringIO()
        stderr = io.StringIO()
        client_instances = []

        class InterruptingClient:
            def __init__(self, runtime_config, event_recorder, session_log=None, enable_search=False):
                self.runtime_config = runtime_config
                self.event_recorder = event_recorder
                self.closed = False
                self.enable_search = enable_search
                client_instances.append(self)

            def close(self):
                self.closed = True

        class InterruptingController:
            def __init__(self, runtime_config, client, event_recorder, store, schema_catalog, session, terminal_reporter=None):
                self.session = session

            def run(self):
                raise KeyboardInterrupt

        original_ensure = ralph_codex.ensure_codex_available
        original_client = ralph_codex.SubprocessAppServerClient
        original_controller = ralph_codex.RalphController
        original_reporter = ralph_codex.TerminalReporter
        self.addCleanup(setattr, ralph_codex, "ensure_codex_available", original_ensure)
        self.addCleanup(setattr, ralph_codex, "SubprocessAppServerClient", original_client)
        self.addCleanup(setattr, ralph_codex, "RalphController", original_controller)
        self.addCleanup(setattr, ralph_codex, "TerminalReporter", original_reporter)
        ralph_codex.ensure_codex_available = lambda: None
        ralph_codex.SubprocessAppServerClient = InterruptingClient
        ralph_codex.RalphController = InterruptingController
        ralph_codex.TerminalReporter = lambda verbose, **kwargs: CaptureReporter(verbose, stdout=stdout, stderr=stderr)

        exit_code = ralph_codex.execute_run(runtime_config, store, schema_catalog, session, "message", verbose=False)

        self.assertEqual(exit_code, ralph_codex.ABORT_EXIT_CODE)
        self.assertTrue(client_instances[0].closed)
        self.assertTrue(client_instances[0].enable_search)
        state = store.read_json(session.session_dir / "session-state.json", ralph_codex.SESSION_STATE_SCHEMA_ID)
        self.assertEqual(state["status"], "aborted")
        self.assertEqual(state["current_turn_id"], "")
        completion = store.read_json(session.session_dir / "completion.json", ralph_codex.COMPLETION_SCHEMA_ID)
        self.assertEqual(completion["last_reason"], ralph_codex.ABORT_REASON)
        controller_state = store.read_json(store.controller_state_path, ralph_codex.CONTROLLER_STATE_SCHEMA_ID)
        self.assertEqual(controller_state["current_session_id"], session.session_id)
        self.assertEqual(controller_state["current_run_id"], "")
        self.assertFalse((session.session_dir / "finished.json").exists())
        rows = store.list_run_rows()
        self.assertEqual(rows[-1]["outcome"], "aborted")
        self.assertEqual(rows[-1]["session_status"], "resumable")
        events = store.read_jsonl(session.session_dir / "events.jsonl", ralph_codex.EVENT_LOG_LINE_SCHEMA_ID)
        aborted = [event for event in events if event["event_type"] == "run-aborted"]
        self.assertEqual(len(aborted), 1)
        self.assertIn(f"./scripts/ralph-codex.py --resume {session.session_id}", aborted[0]["payload"]["resume_command"])
        self.assertIn("aborted. resume session with:", stdout.getvalue())

    def test_execute_run_creates_per_run_plain_text_log(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        runtime_config = ralph_codex.RuntimeConfig(workdir=root, state_root=store.root)
        schema_catalog = self.make_schema_catalog()
        client_instances = []

        class QuietClient:
            def __init__(self, runtime_config, event_recorder, session_log=None, enable_search=False):
                self.closed = False
                self.enable_search = enable_search
                client_instances.append(self)

            def close(self):
                self.closed = True

        class QuietController:
            def __init__(self, runtime_config, client, event_recorder, store, schema_catalog, session, terminal_reporter=None):
                self.session = session

            def run(self):
                self.session.completion_record["last_result"] = {"summary": "session completed"}
                return 0

        original_ensure = ralph_codex.ensure_codex_available
        original_client = ralph_codex.SubprocessAppServerClient
        original_controller = ralph_codex.RalphController
        self.addCleanup(setattr, ralph_codex, "ensure_codex_available", original_ensure)
        self.addCleanup(setattr, ralph_codex, "SubprocessAppServerClient", original_client)
        self.addCleanup(setattr, ralph_codex, "RalphController", original_controller)
        ralph_codex.ensure_codex_available = lambda: None
        ralph_codex.SubprocessAppServerClient = QuietClient
        ralph_codex.RalphController = QuietController

        exit_code = ralph_codex.execute_run(runtime_config, store, schema_catalog, session, "message", verbose=False)

        self.assertEqual(exit_code, 0)
        self.assertTrue(client_instances[0].closed)
        self.assertTrue(client_instances[0].enable_search)
        log_paths = sorted((session.session_dir / "logs").glob("*.log"))
        self.assertEqual(len(log_paths), 1)
        rendered = log_paths[0].read_text(encoding="utf-8")
        self.assertIn("# Ralph Codex run log", rendered)
        self.assertIn("invocation_mode: message", rendered)
        self.assertIn("STDOUT", rendered)
        self.assertIn("run started: session=", rendered)
        self.assertIn("run completed: session completed", rendered)

    def test_plain_text_run_log_captures_terminal_streams_only(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        session_log = ralph_codex.PlainTextRunLog(
            session.session_dir / "logs" / "run-1.log",
            session.session_id,
            "run-1",
            "message",
            verbose=False,
        )
        self.addCleanup(session_log.close)
        reporter = ralph_codex.TerminalReporter(
            verbose=False,
            stdout=io.StringIO(),
            stderr=io.StringIO(),
            session_log=session_log,
        )
        reporter.status("hello status", badge="STARTING")
        reporter.event("hello event")
        reporter.console_input("approve\n")
        session_log.close()

        rendered = (session.session_dir / "logs" / "run-1.log").read_text(encoding="utf-8")
        self.assertIn("STDOUT", rendered)
        self.assertIn("hello status", rendered)
        self.assertIn("STDERR", rendered)
        self.assertIn("hello event", rendered)
        self.assertIn("STDIN approve", rendered)
        self.assertNotIn("APP-STDIN", rendered)
        self.assertNotIn("APP-STDOUT", rendered)
        self.assertNotIn("APP-STDERR", rendered)

    def test_plain_text_run_log_writes_visible_before_close(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        session_log = ralph_codex.PlainTextRunLog(
            session.session_dir / "logs" / "run-1.log",
            session.session_id,
            "run-1",
            "message",
            verbose=False,
        )
        self.addCleanup(session_log.close)
        session_log.write_console_output("stdout", "partial status")

        rendered = (session.session_dir / "logs" / "run-1.log").read_text(encoding="utf-8")
        self.assertIn("# Ralph Codex run log", rendered)
        self.assertIn("STDOUT partial status", rendered)

    def test_select_prompt_option_prefers_recommended(self):
        choice = ralph_codex.RalphController.select_prompt_option(
            [
                {"label": "A", "description": "x"},
                {"label": "B (Recommended)", "description": "y"},
            ]
        )
        self.assertEqual(choice, "B (Recommended)")

    def test_answer_request_user_input_raises_on_secret(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        with self.assertRaises(ralph_codex.UnsupportedPromptError):
            controller.answer_request_user_input(
                {
                    "questions": [
                        {
                            "id": "secret",
                            "isSecret": True,
                            "options": [{"label": "A", "description": "x"}],
                        }
                    ]
                }
            )

    def test_validate_planning_result_rejects_narrow_charter(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        narrow = self.broad_charter()
        narrow["workstreams"] = narrow["workstreams"][:2]
        planning_result = self.planning_result_payload(summary="ok", charter=narrow)
        with self.assertRaises(ralph_codex.RalphError):
            controller.validate_planning_result(planning_result)

    def test_validate_planning_result_rejects_unknown_tranche_workstream(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        planning_result = self.planning_result_payload(summary="ok")
        planning_result["current_tranche"]["workstream_ids"] = ["W9"]
        with self.assertRaisesRegex(ralph_codex.RalphError, "unknown workstream id"):
            controller.validate_planning_result(planning_result)

    def test_validate_planning_result_rejects_blocked_status(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        planning_result = self.planning_result_payload(summary="blocked")
        planning_result["status"] = "BLOCKED"
        with self.assertRaisesRegex(ralph_codex.RalphError, "planner reported BLOCKED"):
            controller.validate_planning_result(planning_result)

    def test_validate_planning_result_rejects_blocked_research_when_required(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        planning_result = self.planning_result_payload(summary="blocked research")
        planning_result["research"]["status"] = "blocked"
        with self.assertRaisesRegex(ralph_codex.RalphError, "research is blocked"):
            controller.validate_planning_result(planning_result)

    def test_run_turn_handles_request_user_input_and_logs_turn(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        stdout = io.StringIO()
        stderr = io.StringIO()
        reporter = self.make_reporter(stdout=stdout, stderr=stderr)
        result_payload = self.execution_result_payload()
        client = FakeClient(
            {"turn/start": {"turn": {"id": "turn-1"}}},
            [
                {
                    "kind": "server-request",
                    "payload": {
                        "id": 41,
                        "method": "item/tool/requestUserInput",
                        "params": {
                            "questions": [
                                {
                                    "id": "mode",
                                    "header": "Mode",
                                    "question": "Choose",
                                    "isOther": False,
                                    "isSecret": False,
                                    "options": [
                                        {"label": "Default", "description": "x"},
                                        {"label": "Plan (Recommended)", "description": "y"},
                                    ],
                                }
                            ]
                        },
                    },
                },
                {
                    "kind": "notification",
                    "payload": {
                        "method": "rawResponseItem/completed",
                        "params": {
                            "threadId": "thread-1",
                            "turnId": "turn-1",
                            "item": {
                                "type": "message",
                                "role": "assistant",
                                "phase": "final_answer",
                                "content": [{"type": "output_text", "text": json.dumps(result_payload)}],
                            },
                        },
                    },
                },
                {
                    "kind": "notification",
                    "payload": {
                        "method": "turn/completed",
                        "params": {"threadId": "thread-1", "turn": {"id": "turn-1", "status": "completed"}},
                    },
                },
            ],
        )
        runtime_config = ralph_codex.RuntimeConfig(workdir=root, state_root=store.root)
        controller = ralph_codex.RalphController(
            runtime_config,
            client,
            self.make_event_recorder(store, session, reporter=reporter),
            store,
            self.make_schema_catalog(),
            session,
            terminal_reporter=reporter,
        )
        session.state["thread_id"] = "thread-1"
        session.state["model"] = "gpt-5.4"
        store.save_state(session)
        result = controller.run_turn(
            phase_name="test",
            prompt="hello",
            schema={"type": "object"},
            collaboration_mode=controller.make_collaboration_mode("default", "high", "instructions"),
        )
        self.assertEqual(result["status"], "IN_PROGRESS")
        self.assertEqual(client.sent_results[0][1]["answers"]["mode"]["answers"], ["Plan (Recommended)"])
        turns = (session.session_dir / "turns.jsonl").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(turns), 1)
        self.assertIn("prompt request received: 1 question(s)", stderr.getvalue())
        self.assertIn("prompt request answered: 1 answer(s)", stderr.getvalue())
        self.assertIn("test started", stdout.getvalue())
        self.assertIn("test complete: IN_PROGRESS: working", stdout.getvalue())
        self.assertIn("test result", stdout.getvalue())
        self.assertIn("summary:", stdout.getvalue())

    def test_run_turn_waits_through_silence_and_completes(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        stdout = io.StringIO()
        reporter = self.make_reporter(stdout=stdout)
        result_payload = self.execution_result_payload(remaining_gaps=[])

        class DelayedEventClient(FakeClient):
            def __init__(self):
                super().__init__({"turn/start": {"turn": {"id": "turn-1"}}}, [])
                self.poll_count = 0

            def next_event(self, timeout=0.1):
                self.poll_count += 1
                if self.poll_count == 1:
                    return None
                if self.poll_count == 2:
                    return {
                        "kind": "notification",
                        "payload": {
                            "method": "rawResponseItem/completed",
                            "params": {
                                "threadId": "thread-1",
                                "turnId": "turn-1",
                                "item": {
                                    "type": "message",
                                    "role": "assistant",
                                    "phase": "final_answer",
                                    "content": [{"type": "output_text", "text": json.dumps(result_payload)}],
                                },
                            },
                        },
                    }
                if self.poll_count == 3:
                    return {
                        "kind": "notification",
                        "payload": {
                            "method": "turn/completed",
                            "params": {"threadId": "thread-1", "turn": {"id": "turn-1", "status": "completed"}},
                        },
                    }
                return None

        client = DelayedEventClient()
        runtime_config = ralph_codex.RuntimeConfig(workdir=root, state_root=store.root)
        controller = ralph_codex.RalphController(
            runtime_config,
            client,
            self.make_event_recorder(store, session, reporter=reporter),
            store,
            self.make_schema_catalog(),
            session,
            terminal_reporter=reporter,
            monotonic_func=iter([0.0, 11.0, 12.0, 13.0]).__next__,
        )
        session.state["thread_id"] = "thread-1"
        session.state["model"] = "gpt-5.4"
        store.save_state(session)
        result = controller.run_turn(
            phase_name="test",
            prompt="hello",
            schema=self.make_schema_catalog().model_schema(ralph_codex.EXECUTION_OUTPUT_SCHEMA_ID),
            collaboration_mode=controller.make_collaboration_mode("default", "high", "instructions"),
        )
        self.assertEqual(result["status"], "IN_PROGRESS")
        self.assertEqual(client.poll_count, 3)
        self.assertIn("WORKING", stdout.getvalue())
        self.assertIn("test running for 11s", stdout.getvalue())

    def test_event_recorder_prints_command_updates_once_as_they_arrive(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        stdout = io.StringIO()
        reporter = self.make_reporter(stdout=stdout)
        recorder = self.make_event_recorder(store, session, reporter=reporter)

        started_params = {
            "threadId": "thread-1",
            "turnId": "turn-1",
            "item": {
                "type": "commandExecution",
                "id": "call-1",
                "command": "/bin/zsh -lc 'echo hi'",
                "status": "inProgress",
                "commandActions": [{"type": "exec"}],
                "processId": 123,
            },
        }
        completed_params = {
            "threadId": "thread-1",
            "turnId": "turn-1",
            "item": {
                "type": "commandExecution",
                "id": "call-1",
                "command": "/bin/zsh -lc 'echo hi'",
                "status": "completed",
                "aggregated_output_chars": 17,
                "command_actions": 1,
                "processId": 123,
            },
        }

        recorder.record_notification("item/started", started_params)
        recorder.record_notification("item/started", started_params)
        recorder.record_notification("item/completed", completed_params)
        recorder.record_notification("item/completed", completed_params)

        console = stdout.getvalue()
        self.assertIn("TOOL", console)
        self.assertEqual(console.count("echo hi"), 1)
        self.assertIn("exec /bin/zsh -lc 'echo hi' | output=17 chars", console)

    def test_run_turn_wait_stays_thin_while_commands_print_live(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        stdout = io.StringIO()
        reporter = self.make_reporter(stdout=stdout)
        result_payload = self.execution_result_payload(remaining_gaps=[])

        class CommandWaitClient(FakeClient):
            def __init__(self):
                super().__init__({"turn/start": {"turn": {"id": "turn-1"}}}, [])
                self.poll_count = 0

            def next_event(self, timeout=0.1):
                self.poll_count += 1
                if self.poll_count == 1:
                    return {
                        "kind": "notification",
                        "payload": {
                            "method": "item/started",
                            "params": {
                                "threadId": "thread-1",
                                "turnId": "turn-1",
                                "item": {
                                    "type": "commandExecution",
                                    "id": "call-1",
                                    "command": "/bin/zsh -lc 'echo hi'",
                                    "status": "inProgress",
                                    "commandActions": [{"type": "exec"}],
                                    "processId": 123,
                                },
                            },
                        },
                    }
                if self.poll_count == 2:
                    return None
                if self.poll_count == 3:
                    return {
                        "kind": "notification",
                        "payload": {
                            "method": "item/completed",
                            "params": {
                                "threadId": "thread-1",
                                "turnId": "turn-1",
                                "item": {
                                    "type": "commandExecution",
                                    "id": "call-1",
                                    "command": "/bin/zsh -lc 'echo hi'",
                                    "status": "completed",
                                    "aggregated_output_chars": 17,
                                    "command_actions": 1,
                                    "processId": 123,
                                },
                            },
                        },
                    }
                if self.poll_count == 4:
                    return None
                if self.poll_count == 5:
                    return {
                        "kind": "notification",
                        "payload": {
                            "method": "rawResponseItem/completed",
                            "params": {
                                "threadId": "thread-1",
                                "turnId": "turn-1",
                                "item": {
                                    "type": "message",
                                    "role": "assistant",
                                    "phase": "final_answer",
                                    "content": [{"type": "output_text", "text": json.dumps(result_payload)}],
                                },
                            },
                        },
                    }
                if self.poll_count == 6:
                    return {
                        "kind": "notification",
                        "payload": {
                            "method": "turn/completed",
                            "params": {"threadId": "thread-1", "turn": {"id": "turn-1", "status": "completed"}},
                        },
                    }
                return None

        client = CommandWaitClient()
        controller = ralph_codex.RalphController(
            ralph_codex.RuntimeConfig(workdir=root, state_root=store.root),
            client,
            self.make_event_recorder(store, session, reporter=reporter),
            store,
            self.make_schema_catalog(),
            session,
            terminal_reporter=reporter,
            monotonic_func=iter([0.0, 11.0, 12.0, 21.0, 22.0, 23.0]).__next__,
        )
        session.state["thread_id"] = "thread-1"
        session.state["model"] = "gpt-5.4"
        store.save_state(session)

        result = controller.run_turn(
            phase_name="execution-1",
            prompt="hello",
            schema=self.make_schema_catalog().model_schema(ralph_codex.EXECUTION_OUTPUT_SCHEMA_ID),
            collaboration_mode=controller.make_collaboration_mode("default", "high", "instructions"),
        )

        self.assertEqual(result["status"], "IN_PROGRESS")
        console = stdout.getvalue()
        self.assertIn("exec /bin/zsh -lc 'echo hi' | output=17 chars", console)
        self.assertIn("execution-1 running for 11s", console)
        self.assertNotIn("commands: ", console)
        self.assertEqual(console.count("/bin/zsh -lc 'echo hi'"), 1)

    def test_run_turn_verbose_mode_avoids_duplicate_command_console_output(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        stdout = io.StringIO()
        stderr = io.StringIO()
        reporter = self.make_reporter(verbose=True, stdout=stdout, stderr=stderr)
        result_payload = self.execution_result_payload(remaining_gaps=[])

        class VerboseCommandWaitClient(FakeClient):
            def __init__(self):
                super().__init__({"turn/start": {"turn": {"id": "turn-1"}}}, [])
                self.poll_count = 0

            def next_event(self, timeout=0.1):
                self.poll_count += 1
                if self.poll_count == 1:
                    return {
                        "kind": "notification",
                        "payload": {
                            "method": "item/started",
                            "params": {
                                "threadId": "thread-1",
                                "turnId": "turn-1",
                                "item": {
                                    "type": "commandExecution",
                                    "id": "call-1",
                                    "command": "/bin/zsh -lc 'echo verbose'",
                                    "status": "inProgress",
                                    "commandActions": [{"type": "exec"}],
                                    "processId": 321,
                                },
                            },
                        },
                    }
                if self.poll_count == 2:
                    return None
                if self.poll_count == 3:
                    return {
                        "kind": "notification",
                        "payload": {
                            "method": "rawResponseItem/completed",
                            "params": {
                                "threadId": "thread-1",
                                "turnId": "turn-1",
                                "item": {
                                    "type": "message",
                                    "role": "assistant",
                                    "phase": "final_answer",
                                    "content": [{"type": "output_text", "text": json.dumps(result_payload)}],
                                },
                            },
                        },
                    }
                if self.poll_count == 4:
                    return {
                        "kind": "notification",
                        "payload": {
                            "method": "turn/completed",
                            "params": {"threadId": "thread-1", "turn": {"id": "turn-1", "status": "completed"}},
                        },
                    }
                return None

        client = VerboseCommandWaitClient()
        controller = ralph_codex.RalphController(
            ralph_codex.RuntimeConfig(workdir=root, state_root=store.root),
            client,
            self.make_event_recorder(store, session, verbose=True, reporter=reporter),
            store,
            self.make_schema_catalog(),
            session,
            terminal_reporter=reporter,
            monotonic_func=iter([0.0, 11.0, 12.0, 13.0]).__next__,
        )
        session.state["thread_id"] = "thread-1"
        session.state["model"] = "gpt-5.4"
        store.save_state(session)

        result = controller.run_turn(
            phase_name="planning review",
            prompt="hello",
            schema=self.make_schema_catalog().model_schema(ralph_codex.EXECUTION_OUTPUT_SCHEMA_ID),
            collaboration_mode=controller.make_collaboration_mode("plan", "high", "instructions"),
        )

        self.assertEqual(result["status"], "IN_PROGRESS")
        self.assertNotIn("/bin/zsh -lc 'echo verbose'", stdout.getvalue())
        self.assertNotIn("/bin/zsh -lc 'echo verbose'", stderr.getvalue())

    def test_run_turn_raises_when_app_server_stream_closes(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        client = FakeClient(
            {"turn/start": {"turn": {"id": "turn-1"}}},
            [{"kind": "stream-closed", "payload": {"stream": "stdout"}}],
        )
        runtime_config = ralph_codex.RuntimeConfig(workdir=root, state_root=store.root)
        controller = ralph_codex.RalphController(
            runtime_config,
            client,
            self.make_event_recorder(store, session),
            store,
            self.make_schema_catalog(),
            session,
        )
        session.state["thread_id"] = "thread-1"
        session.state["model"] = "gpt-5.4"
        store.save_state(session)
        with self.assertRaisesRegex(ralph_codex.RalphError, "stream closed during turn"):
            controller.run_turn(
                phase_name="test",
                prompt="hello",
                schema={"type": "object"},
                collaboration_mode=controller.make_collaboration_mode("default", "high", "instructions"),
            )

    def test_run_turn_formats_structured_model_output_instead_of_raw_json(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        stdout = io.StringIO()
        reporter = self.make_reporter(stdout=stdout)
        result_payload = self.planning_result_payload(summary="ready")
        client = FakeClient(
            {"turn/start": {"turn": {"id": "turn-1"}}},
            [
                {
                    "kind": "notification",
                    "payload": {
                        "method": "item/agentMessage/delta",
                        "params": {"threadId": "thread-1", "turnId": "turn-1", "delta": "Working..."},
                    },
                },
                {
                    "kind": "notification",
                    "payload": {
                        "method": "rawResponseItem/completed",
                        "params": {
                            "threadId": "thread-1",
                            "turnId": "turn-1",
                            "item": {
                                "type": "message",
                                "role": "assistant",
                                "phase": "final_answer",
                                "content": [{"type": "output_text", "text": json.dumps(result_payload)}],
                            },
                        },
                    },
                },
                {
                    "kind": "notification",
                    "payload": {
                        "method": "turn/completed",
                        "params": {"threadId": "thread-1", "turn": {"id": "turn-1", "status": "completed"}},
                    },
                },
            ],
        )
        controller = ralph_codex.RalphController(
            ralph_codex.RuntimeConfig(workdir=root, state_root=store.root),
            client,
            self.make_event_recorder(store, session, reporter=reporter),
            store,
            self.make_schema_catalog(),
            session,
            terminal_reporter=reporter,
        )
        session.state["thread_id"] = "thread-1"
        session.state["model"] = "gpt-5.4"
        store.save_state(session)
        result = controller.run_turn(
            phase_name="planning",
            prompt="hello",
            schema=self.make_schema_catalog().model_schema(ralph_codex.PLANNING_OUTPUT_SCHEMA_ID),
            collaboration_mode=controller.make_collaboration_mode("plan", "high", "instructions"),
        )
        self.assertEqual(result["status"], "CHARTER_READY")
        console = stdout.getvalue()
        self.assertIn("planning result", console)
        self.assertIn("status:", console)
        self.assertNotIn(json.dumps(result_payload), console)
        self.assertIn("Working...", console)
        self.assertEqual(console.count("Working..."), 1)

    def test_review_plan_if_needed_renders_full_review_and_exec_context(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        session.profile["seed_policy"]["require_confirmation"] = True
        session.profile["seed_policy"]["auto_confirm"] = False
        long_summary = "Operator review summary " * 18
        planning_result = self.planning_result_payload(summary=long_summary.strip())
        planning_result["broadening_rationale"] = "Review before unattended execution."
        planning_result["next_step"] = "Await operator approval."
        planning_result["gate_reasoning"] = "The operator must approve the broadened charter."
        session.state["charter_version"] = 1
        store.save_charter(session, planning_result, confirmed=False, review_state="draft")
        store.append_turn(session, "initial planning", "turn-1", "CHARTER_READY", "ready")
        store.append_event(
            session,
            "notification",
            {
                "method": "item/started",
                "turn_id": "turn-1",
                "item": {
                    "type": "commandExecution",
                    "id": "call-1",
                    "command": "/bin/zsh -lc \"sed -n '1,240p' MISSION.md\"",
                    "status": "inProgress",
                    "command_actions": 1,
                    "processId": "51660",
                },
            },
        )
        store.append_event(
            session,
            "notification",
            {
                "method": "item/completed",
                "turn_id": "turn-1",
                "item": {
                    "type": "commandExecution",
                    "id": "call-1",
                    "command": "/bin/zsh -lc \"sed -n '1,240p' MISSION.md\"",
                    "status": "completed",
                    "aggregated_output_chars": 2091,
                    "command_actions": 1,
                    "processId": "51660",
                },
            },
        )
        stdout = io.StringIO()
        prompts = []
        original_stdin = sys.stdin
        self.addCleanup(setattr, sys, "stdin", original_stdin)
        sys.stdin = FakeTTYStream()
        controller = self.make_controller(
            root,
            session=session,
            input_func=lambda prompt: prompts.append(prompt) or "yes",
            stdout=stdout,
        )
        controller.review_plan_if_needed()
        console = stdout.getvalue()
        self.assertIn("Operator review summary", console)
        self.assertNotIn("truncated for console", console)
        self.assertIn("exec log context", console)
        self.assertIn("/bin/zsh -lc \"sed -n '1,240p' MISSION.md\"", console)
        self.assertIn("output=2091 chars", console)
        self.assertIn("Plan review: [a]pprove, [c]hange, or [x] abort", console)
        self.assertEqual(prompts, [""])
        self.assertEqual(session.state["phase"], "executing")
        self.assertTrue(session.state["seed_confirmed"])

    def test_review_plan_if_needed_revises_and_versions_drafts(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        session.profile["seed_policy"]["require_confirmation"] = True
        session.profile["seed_policy"]["auto_confirm"] = False
        session.state["charter_version"] = 1
        initial_result = self.planning_result_payload(summary="initial draft")
        store.save_charter(session, initial_result, confirmed=False, review_state="draft")
        revised_charter = self.broad_charter()
        revised_charter["validation_categories"] = ["unit", "integration", "gating", "docs"]
        revised_charter["workstreams"].append(
            {
                "id": "W4",
                "title": "Validation",
                "goal": "Deepen review coverage",
                "required_adjacent_surfaces": ["tests"],
                "validation": ["review tests"],
                "status": "planned",
            }
        )
        revised_result = self.planning_result_payload(summary="revised draft", charter=revised_charter)
        revised_result["broadening_rationale"] = "broader"
        prompts = []
        answers = iter(["change", "Add stronger validation coverage", ".", "approve"])
        original_stdin = sys.stdin
        self.addCleanup(setattr, sys, "stdin", original_stdin)
        sys.stdin = FakeTTYStream()
        controller = self.make_controller(
            root,
            session=session,
            input_func=lambda prompt: prompts.append(prompt) or next(answers),
        )
        controller.plan_once = lambda phase_name, feedback, render_output=True: revised_result
        controller.review_plan_if_needed()
        history = store.read_jsonl(
            session.session_dir / "charter-history.jsonl",
            ralph_codex.CHARTER_HISTORY_LINE_SCHEMA_ID,
        )
        self.assertEqual([entry["charter_version"] for entry in history], [1, 2])
        self.assertEqual(history[0]["review_state"], "superseded")
        self.assertEqual(history[1]["review_state"], "approved")
        self.assertEqual(history[1]["operator_feedback"], "Add stronger validation coverage")
        self.assertEqual(session.state["charter_version"], 2)
        self.assertTrue(session.state["seed_confirmed"])
        self.assertEqual(session.charter_record["review_state"], "approved")
        self.assertTrue(session.charter_record["locked"])
        self.assertEqual(prompts, ["", "", "", ""])

    def test_build_planning_prompt_includes_plan_mode_contract_and_history(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        planning_result = self.planning_result_payload(summary="first draft")
        planning_result["next_step"] = "review"
        controller.session.state["charter_version"] = 1
        controller.store.save_charter(
            controller.session,
            planning_result,
            confirmed=False,
            review_state="draft",
            operator_feedback="Need broader validation",
        )
        prompt = controller.build_planning_prompt("planning review", "Tighten docs")
        self.assertIn("## Ralph Plan Mode Contract", prompt)
        self.assertIn("Do not call update_plan.", prompt)
        self.assertIn("request_user_input", prompt)
        self.assertIn("## Review History", prompt)
        self.assertIn("feedback=Need broader validation", prompt)

    def test_build_planning_prompt_drops_optional_sections_before_failing_cap(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        controller.session.profile["loop_policy"]["planning_max_prompt_chars"] = 6000
        controller.session.task["message_text"] = "Task " + ("x" * 3500)
        controller.session.state["research_memory"] = {
            "search_strategy": "widen",
            "open_questions": ["q1", "q2", "q3"],
            "last_refreshed_at": "2026-04-20T00:00:00Z",
        }
        controller.session.state["execution_memory"] = [
            {"iteration": index, "summary": f"Iteration {index}", "novelty_score": 1.0, "acceptance_progress_score": 0.2}
            for index in range(1, 10)
        ]
        controller.store.append_event(
            controller.session,
            "evaluation-result",
            self.evaluation_result_payload(summary="Need more tranche work"),
        )
        self.save_charter(controller)
        prompt = controller.build_planning_prompt("replanning", "Keep pushing")
        self.assertLessEqual(len(prompt), 6000)
        self.assertIn("## Program Memory", prompt)
        self.assertIn("## Task", prompt)

    def test_planning_instructions_forbid_update_plan(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        instructions = controller.planning_instructions()
        self.assertIn("Never call update_plan", instructions)
        self.assertIn("request_user_input", instructions)
        self.assertIn("real Codex Plan Mode", instructions)

    def test_run_turn_extracts_plan_thread_item_output(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        result_payload = self.planning_result_payload(summary="ready")
        client = FakeClient(
            {"turn/start": {"turn": {"id": "turn-1"}}},
            [
                {
                    "kind": "notification",
                    "payload": {
                        "method": "item/completed",
                        "params": {
                            "threadId": "thread-1",
                            "turnId": "turn-1",
                            "item": {"type": "plan", "id": "plan-1", "text": json.dumps(result_payload)},
                        },
                    },
                },
                {
                    "kind": "notification",
                    "payload": {
                        "method": "turn/completed",
                        "params": {"threadId": "thread-1", "turn": {"id": "turn-1", "status": "completed"}},
                    },
                },
            ],
        )
        runtime_config = ralph_codex.RuntimeConfig(workdir=root, state_root=store.root)
        controller = ralph_codex.RalphController(
            runtime_config,
            client,
            self.make_event_recorder(store, session),
            store,
            self.make_schema_catalog(),
            session,
        )
        session.state["thread_id"] = "thread-1"
        session.state["model"] = "gpt-5.4"
        store.save_state(session)
        result = controller.run_turn(
            phase_name="test",
            prompt="hello",
            schema=self.make_schema_catalog().model_schema(ralph_codex.PLANNING_OUTPUT_SCHEMA_ID),
            collaboration_mode=controller.make_collaboration_mode("plan", "high", "instructions"),
        )
        self.assertEqual(result["status"], "CHARTER_READY")

    def test_turn_search_count_reads_recorded_search_activity(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        self.save_charter(controller)
        controller.store.append_turn(controller.session, "planning", "turn-1", "CHARTER_READY", "ok")
        controller.store.append_event(
            controller.session,
            "turn-search-activity",
            {"turn_id": "turn-1", "count": 2, "names": ["web_search"]},
        )
        self.assertEqual(controller.turn_search_count("turn-1"), 2)

    def test_run_turn_records_search_activity_from_raw_command_actions(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        result_payload = self.planning_result_payload(summary="ready")
        client = FakeClient(
            {"turn/start": {"turn": {"id": "turn-1"}}},
            [
                {
                    "kind": "notification",
                    "payload": {
                        "method": "item/completed",
                        "params": {
                            "threadId": "thread-1",
                            "turnId": "turn-1",
                            "item": {
                                "type": "commandExecution",
                                "id": "call-1",
                                "command": "/bin/zsh -lc 'rg -n needle docs'",
                                "status": "completed",
                                "commandActions": [{"type": "searchText", "path": "docs/19-reference-architectures"}],
                            },
                        },
                    },
                },
                {
                    "kind": "notification",
                    "payload": {
                        "method": "rawResponseItem/completed",
                        "params": {
                            "threadId": "thread-1",
                            "turnId": "turn-1",
                            "item": {
                                "type": "message",
                                "role": "assistant",
                                "phase": "final_answer",
                                "content": [{"type": "output_text", "text": json.dumps(result_payload)}],
                            },
                        },
                    },
                },
                {
                    "kind": "notification",
                    "payload": {
                        "method": "turn/completed",
                        "params": {"threadId": "thread-1", "turn": {"id": "turn-1", "status": "completed"}},
                    },
                },
            ],
        )
        controller = ralph_codex.RalphController(
            ralph_codex.RuntimeConfig(workdir=root, state_root=store.root),
            client,
            self.make_event_recorder(store, session),
            store,
            self.make_schema_catalog(),
            session,
        )
        session.state["thread_id"] = "thread-1"
        session.state["model"] = "gpt-5.4"
        store.save_state(session)

        result = controller.run_turn(
            phase_name="planning",
            prompt="hello",
            schema=self.make_schema_catalog().model_schema(ralph_codex.PLANNING_OUTPUT_SCHEMA_ID),
            collaboration_mode=controller.make_collaboration_mode("plan", "high", "instructions"),
        )

        self.assertEqual(result["status"], "CHARTER_READY")
        latest_turn = store.latest_turn(session)
        self.assertIsNotNone(latest_turn)
        self.assertEqual(controller.turn_search_count(latest_turn["turn_id"]), 1)

    def test_validate_planning_result_accepts_searches_from_raw_command_actions(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        result_payload = self.planning_result_payload(summary="ready")
        client = FakeClient(
            {"turn/start": {"turn": {"id": "turn-1"}}},
            [
                {
                    "kind": "notification",
                    "payload": {
                        "method": "item/completed",
                        "params": {
                            "threadId": "thread-1",
                            "turnId": "turn-1",
                            "item": {
                                "type": "commandExecution",
                                "id": "call-1",
                                "command": "/bin/zsh -lc 'rg -n notes docs/19-reference-architectures'",
                                "status": "completed",
                                "commandActions": [{"type": "searchText", "path": "docs/19-reference-architectures"}],
                            },
                        },
                    },
                },
                {
                    "kind": "notification",
                    "payload": {
                        "method": "item/completed",
                        "params": {
                            "threadId": "thread-1",
                            "turnId": "turn-1",
                            "item": {
                                "type": "commandExecution",
                                "id": "call-2",
                                "command": "/bin/zsh -lc 'rg -n overlap docs/03-enterprise-ai-stack-map'",
                                "status": "completed",
                                "commandActions": [{"type": "searchText", "path": "docs/03-enterprise-ai-stack-map"}],
                            },
                        },
                    },
                },
                {
                    "kind": "notification",
                    "payload": {
                        "method": "rawResponseItem/completed",
                        "params": {
                            "threadId": "thread-1",
                            "turnId": "turn-1",
                            "item": {
                                "type": "message",
                                "role": "assistant",
                                "phase": "final_answer",
                                "content": [{"type": "output_text", "text": json.dumps(result_payload)}],
                            },
                        },
                    },
                },
                {
                    "kind": "notification",
                    "payload": {
                        "method": "turn/completed",
                        "params": {"threadId": "thread-1", "turn": {"id": "turn-1", "status": "completed"}},
                    },
                },
            ],
        )
        controller = ralph_codex.RalphController(
            ralph_codex.RuntimeConfig(workdir=root, state_root=store.root),
            client,
            self.make_event_recorder(store, session),
            store,
            self.make_schema_catalog(),
            session,
        )
        session.state["thread_id"] = "thread-1"
        session.state["model"] = "gpt-5.4"
        store.save_state(session)

        result = controller.run_turn(
            phase_name="planning",
            prompt="hello",
            schema=self.make_schema_catalog().model_schema(ralph_codex.PLANNING_OUTPUT_SCHEMA_ID),
            collaboration_mode=controller.make_collaboration_mode("plan", "high", "instructions"),
        )

        controller.validate_planning_result(result)
        self.assertEqual(controller.latest_turn_search_count(), 2)

    def test_rejected_completion_is_persisted_immediately(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        self.save_charter(controller)
        controller.session.profile["runtime_limits"]["max_iterations"] = 1
        controller.client.start = lambda: None
        controller.ensure_thread = lambda: None
        controller.review_plan_if_needed = lambda: None
        controller.execute_once = lambda: {
            **self.execution_result_payload(status="COMPLETE", summary="done", remaining_gaps=[]),
            "workstream_updates": [{"id": "W1", "status": "done", "evidence": ["ok"]}],
            "validation_completed": ["unit"],
            "next_step": "none",
        }
        controller.evaluate_once = lambda execution_result, audit: self.evaluation_result_payload(disposition="replan")
        controller.plan_once = lambda phase_name, feedback: self.planning_result_payload(summary="retry")
        with self.assertRaisesRegex(ralph_codex.RalphError, "max_iterations=1"):
            controller.run()
        completion = json.loads((controller.session.session_dir / "completion.json").read_text(encoding="utf-8"))
        self.assertIn("charter workstreams remain incomplete", completion["rejections"][-1])
        self.assertEqual(completion["last_reason"], completion["rejections"][-1])

    def test_evaluate_completion_requires_all_workstreams_and_validation(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        self.save_charter(controller)
        accepted, reason = controller.evaluate_completion(
            {
                **self.execution_result_payload(status="COMPLETE", summary="done", remaining_gaps=[]),
                "workstream_updates": [{"id": "W1", "status": "done", "evidence": ["ok"]}],
                "validation_completed": ["unit"],
                "next_step": "none",
            }
        )
        self.assertFalse(accepted)
        self.assertTrue("W2" in reason or "validation" in reason)

    def test_evaluate_completion_accepts_generic_completion(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        self.save_charter(controller)
        updates = [
            {"id": "W1", "status": "done", "evidence": ["ok"]},
            {"id": "W2", "status": "done", "evidence": ["ok"]},
            {"id": "W3", "status": "done", "evidence": ["ok"]},
        ]
        accepted, reason = controller.evaluate_completion(
            {
                **self.execution_result_payload(status="COMPLETE", summary="done", remaining_gaps=[]),
                "workstream_updates": updates,
                "validation_completed": ["unit", "integration", "gating"],
                "next_step": "none",
            }
        )
        self.assertTrue(accepted)
        self.assertEqual(reason, "")

    def test_build_execution_prompt_contains_program_summary_and_feedback(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        self.save_charter(controller)
        prompt = controller.build_execution_prompt("Need broader validation")
        self.assertIn("Current Tranche", prompt)
        self.assertIn("Program Summary", prompt)
        self.assertIn("Active Milestone", prompt)
        self.assertIn("Need broader validation", prompt)

    def test_build_execution_prompt_uses_profile_prompt_cap(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        controller.session.task["message_text"] = "Test message " + ("x" * 5000)
        self.save_charter(controller)
        prompt = controller.build_execution_prompt("Need broader validation")
        self.assertGreater(len(prompt), 4000)
        self.assertEqual(controller.session.profile["execution"]["max_prompt_chars"], DEFAULT_MAX_EXECUTION_PROMPT_CHARS)

    def test_build_execution_prompt_drops_optional_sections_before_failing_cap(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        self.save_charter(controller)
        controller.session.profile["execution"]["max_prompt_chars"] = 5000
        controller.session.profile["loop_policy"]["execution_max_prompt_chars"] = 5000
        controller.session.state["evidence_registry"] = [
            {
                "claim": f"claim {index}",
                "url": f"https://example.com/{index}",
                "source_type": "secondary",
                "used_for": "execution update",
                "status": "confirmed",
                "updated_at": "2026-04-20T00:00:00Z",
            }
            for index in range(12)
        ]
        controller.session.task["message_text"] = "Task " + ("x" * 3500)
        prompt = controller.build_execution_prompt("Need broader validation")
        self.assertLessEqual(len(prompt), 5000)
        self.assertIn("## Current Tranche", prompt)
        self.assertIn("## Task", prompt)

    def test_build_execution_prompt_rejects_when_over_custom_limit(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        self.save_charter(controller)
        controller.session.profile["execution"]["max_prompt_chars"] = 100
        with self.assertRaisesRegex(ralph_codex.RalphError, "tranche="):
            controller.build_execution_prompt("Need broader validation")

    def test_build_execution_prompt_allows_unlimited_when_limit_is_zero(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        large_task = "Test message " + ("x" * (DEFAULT_MAX_EXECUTION_PROMPT_CHARS + 5000))
        controller.session.task["message_text"] = large_task
        controller.session.profile["execution"]["max_prompt_chars"] = 0
        controller.session.profile["loop_policy"]["execution_max_prompt_chars"] = 0
        self.save_charter(controller)
        prompt = controller.build_execution_prompt("Need broader validation")
        self.assertGreater(len(prompt), 5000)

    def test_run_with_zero_max_iterations_treats_limit_as_unbounded(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        self.save_charter(controller)
        controller.session.profile["runtime_limits"]["max_iterations"] = 0
        controller.client.start = lambda: None
        controller.ensure_thread = lambda: None
        controller.review_plan_if_needed = lambda: None
        calls = {"execute": 0}

        def execute_once():
            calls["execute"] += 1
            status = "COMPLETE" if calls["execute"] == 2 else "IN_PROGRESS"
            return {
                **self.execution_result_payload(
                    status=status,
                    summary="done" if status == "COMPLETE" else "working",
                    remaining_gaps=[],
                ),
                "workstream_updates": [
                    {"id": "W1", "status": "done", "evidence": ["ok"]},
                    {"id": "W2", "status": "done", "evidence": ["ok"]},
                    {"id": "W3", "status": "done", "evidence": ["ok"]},
                ],
                "validation_completed": ["unit", "integration", "gating"],
                "next_step": "none",
            }

        controller.execute_once = execute_once
        controller.evaluate_once = lambda execution_result, audit: self.evaluation_result_payload(
            disposition="accept" if execution_result["status"] == "COMPLETE" else "repair_same_tranche"
        )
        controller.plan_once = lambda phase_name, feedback: self.planning_result_payload(summary="retry")
        result = controller.run()
        self.assertEqual(result, 0)
        self.assertEqual(calls["execute"], 2)

    def test_run_prefers_same_tranche_repair_before_replanning(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        self.save_charter(controller)
        controller.session.profile["runtime_limits"]["max_iterations"] = 0
        controller.client.start = lambda: None
        controller.ensure_thread = lambda: None
        controller.review_plan_if_needed = lambda: None
        calls = {"execute": 0, "plan": 0}

        def execute_once():
            calls["execute"] += 1
            status = "COMPLETE" if calls["execute"] == 2 else "IN_PROGRESS"
            return {
                **self.execution_result_payload(status=status, summary="done" if status == "COMPLETE" else "working", remaining_gaps=[]),
                "workstream_updates": [
                    {"id": "W1", "status": "done", "evidence": ["ok"]},
                    {"id": "W2", "status": "done", "evidence": ["ok"]},
                    {"id": "W3", "status": "done", "evidence": ["ok"]},
                ],
                "validation_completed": ["unit", "integration", "gating"],
                "next_step": "none",
            }

        controller.execute_once = execute_once
        controller.evaluate_once = lambda execution_result, audit: self.evaluation_result_payload(
            disposition="accept" if execution_result["status"] == "COMPLETE" else "repair_same_tranche"
        )
        controller.plan_once = lambda phase_name, feedback: calls.__setitem__("plan", calls["plan"] + 1) or self.planning_result_payload(summary="retry")
        result = controller.run()
        self.assertEqual(result, 0)
        self.assertEqual(calls["execute"], 2)
        self.assertEqual(calls["plan"], 0)

    def test_run_rejects_blocked_initial_planning_before_execution(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        controller.client.start = lambda: None
        controller.ensure_thread = lambda: None
        blocked_result = self.planning_result_payload(summary="blocked")
        blocked_result["status"] = "BLOCKED"
        controller.plan_once = lambda phase_name, feedback, render_output=True: blocked_result
        controller.execute_once = lambda: self.fail("execution should not start from blocked planning")
        with self.assertRaisesRegex(ralph_codex.RalphError, "planner reported BLOCKED"):
            controller.run()

    def test_run_persists_pending_feedback_before_progress_checkpoint_abort(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        self.save_charter(controller)
        controller.client.start = lambda: None
        controller.ensure_thread = lambda: None
        controller.review_plan_if_needed = lambda: None
        controller.execute_once = lambda: self.execution_result_payload(status="IN_PROGRESS", summary="working", remaining_gaps=["docs"])
        controller.audit_execution_result = lambda execution_result: ralph_codex.ExecutionAudit(
            ok=True,
            feedback="",
            total_files_changed=42,
            repeated_heading_file_count=0,
            meta_artifact_files=[],
            requires_checkpoint=True,
            checkpoint_reason="changed-file checkpoint reached",
            diff_samples=["scripts/ralph-codex.py"],
        )
        controller.evaluate_once = lambda execution_result, audit: self.evaluation_result_payload(disposition="repair_same_tranche")
        with self.assertRaisesRegex(ralph_codex.RalphError, "progress checkpoint requires operator input"):
            controller.run()
        state = controller.store.read_json(
            controller.session.session_dir / "session-state.json",
            ralph_codex.SESSION_STATE_SCHEMA_ID,
        )
        self.assertIn("Tighten the current tranche", state["pending_feedback"])

    def test_audit_execution_result_rejects_meta_artifact_sprawl(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        self.save_charter(controller)
        controller.changed_repo_entries = lambda: [
            {"path": "docs/scoreboard.md", "operation": "added"},
            {"path": "scripts/ralph-codex.py", "operation": "modified"},
        ]
        controller.count_repeated_heading_files = lambda touched_files: 0
        audit = controller.audit_execution_result(
            self.execution_result_payload(
                touched_files=["scripts/ralph-codex.py"],
            )
        )
        self.assertFalse(audit.ok)
        self.assertIn("controller-serving meta artifacts", audit.feedback)
        self.assertEqual(audit.meta_artifact_files, [])

    def test_audit_execution_result_allows_deleted_meta_artifact_cleanup(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        self.save_charter(controller)
        controller.changed_repo_entries = lambda: [
            {"path": "docs/scoreboard.md", "operation": "deleted"},
            {"path": "scripts/ralph-codex.py", "operation": "modified"},
        ]
        controller.count_repeated_heading_files = lambda touched_files: 0
        audit = controller.audit_execution_result(
            self.execution_result_payload(
                touched_files=["scripts/ralph-codex.py"],
            )
        )
        self.assertTrue(audit.ok)
        self.assertEqual(audit.feedback, "")

    def test_audit_execution_result_does_not_flag_generic_closure_word(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        self.save_charter(controller)
        controller.changed_repo_entries = lambda: [
            {"path": "docs/closure-plan.md", "operation": "added"},
            {"path": "scripts/ralph-codex.py", "operation": "modified"},
        ]
        controller.count_repeated_heading_files = lambda touched_files: 0
        audit = controller.audit_execution_result(
            self.execution_result_payload(
                touched_files=["scripts/ralph-codex.py"],
            )
        )
        self.assertTrue(audit.ok)
        self.assertEqual(audit.feedback, "")

    def test_audit_execution_result_uses_iteration_repo_baseline(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        self.save_charter(controller)
        controller.session.state["iteration_repo_baseline"] = [
            {"path": "docs/scoreboard.md", "index_status": "?", "worktree_status": "?", "operation": "untracked"}
        ]
        controller.changed_repo_entries = lambda: [
            {"path": "docs/scoreboard.md", "index_status": "?", "worktree_status": "?", "operation": "untracked"},
            {"path": "scripts/ralph-codex.py", "index_status": "M", "worktree_status": " ", "operation": "modified"},
        ]
        controller.count_repeated_heading_files = lambda touched_files: 0
        audit = controller.audit_execution_result(
            self.execution_result_payload(touched_files=["scripts/ralph-codex.py"])
        )
        self.assertTrue(audit.ok)
        self.assertEqual(audit.total_files_changed, 1)

    def test_audit_execution_result_rejects_unjustified_off_tranche_file(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        self.save_charter(controller)
        controller.session.state["iteration_repo_baseline"] = []
        controller.changed_repo_entries = lambda: [
            {"path": "README.md", "index_status": "M", "worktree_status": " ", "operation": "modified"},
        ]
        controller.count_repeated_heading_files = lambda touched_files: 0
        audit = controller.audit_execution_result(
            self.execution_result_payload(touched_files=["README.md"])
        )
        self.assertFalse(audit.ok)
        self.assertIn("outside current_tranche.target_files", audit.feedback)

    def test_count_repeated_heading_files_ignores_preexisting_headings_without_added_diff(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        controller.run_repo_command = lambda args: subprocess.CompletedProcess(
            args,
            0,
            stdout="@@ -1,1 +1,1 @@\n unchanged\n+Some other line\n",
            stderr="",
        )
        self.assertEqual(controller.count_repeated_heading_files(["docs/example.md"]), 0)

    def test_count_repeated_heading_files_counts_only_newly_added_headings(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        controller.run_repo_command = lambda args: subprocess.CompletedProcess(
            args,
            0,
            stdout="@@ -1,1 +1,2 @@\n unchanged\n+## Rejected Defaults\n",
            stderr="",
        )
        self.assertEqual(controller.count_repeated_heading_files(["docs/example.md"]), 1)

    def test_review_progress_if_needed_raises_without_tty(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        audit = ralph_codex.ExecutionAudit(
            ok=True,
            feedback="",
            total_files_changed=42,
            repeated_heading_file_count=0,
            meta_artifact_files=[],
            requires_checkpoint=True,
            checkpoint_reason="changed-file checkpoint reached",
            diff_samples=["scripts/ralph-codex.py"],
        )
        with self.assertRaisesRegex(ralph_codex.RalphError, "progress checkpoint requires operator input"):
            controller.review_progress_if_needed(audit)

    def test_review_progress_if_needed_auto_continues_after_seed_when_profile_allows(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        controller.session.state["seed_confirmed"] = True
        controller.session.profile["quality_policy"]["progress_checkpoint_mode"] = "record_only_after_seed"
        audit = ralph_codex.ExecutionAudit(
            ok=True,
            feedback="",
            total_files_changed=42,
            repeated_heading_file_count=0,
            meta_artifact_files=[],
            requires_checkpoint=True,
            checkpoint_reason="changed-file checkpoint reached",
            diff_samples=["scripts/ralph-codex.py"],
        )
        controller.review_progress_if_needed(audit)
        events = controller.store.read_jsonl(
            controller.session.session_dir / "events.jsonl",
            ralph_codex.EVENT_LOG_LINE_SCHEMA_ID,
        )
        progress_events = [entry for entry in events if entry["event_type"] == "progress-checkpoint-continued"]
        self.assertEqual(len(progress_events), 1)
        self.assertTrue(progress_events[0]["payload"]["auto_continued"])

    def test_review_progress_if_needed_still_requires_input_before_seed(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        controller.session.state["seed_confirmed"] = False
        controller.session.profile["quality_policy"]["progress_checkpoint_mode"] = "record_only_after_seed"
        audit = ralph_codex.ExecutionAudit(
            ok=True,
            feedback="",
            total_files_changed=42,
            repeated_heading_file_count=0,
            meta_artifact_files=[],
            requires_checkpoint=True,
            checkpoint_reason="changed-file checkpoint reached",
            diff_samples=["scripts/ralph-codex.py"],
        )
        with self.assertRaisesRegex(ralph_codex.RalphError, "progress checkpoint requires operator input"):
            controller.review_progress_if_needed(audit)

    def test_memory_retention_uses_profile_caps(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        controller.session.profile["memory_policy"]["max_checkpoint_summaries"] = 3
        controller.session.profile["memory_policy"]["max_worker_manifests"] = 2
        controller.session.profile["memory_policy"]["max_evidence_registry_entries"] = 4
        controller.session.profile["memory_policy"]["max_skill_memory_entries"] = 2
        for index in range(5):
            controller.refresh_evaluation_memory(
                {
                    **self.evaluation_result_payload(summary=f"Evaluation {index}"),
                    "worker_fanout_recommended": True,
                },
                ralph_codex.ExecutionAudit(
                    ok=True,
                    feedback="",
                    total_files_changed=0,
                    repeated_heading_file_count=0,
                    meta_artifact_files=[],
                    requires_checkpoint=False,
                    checkpoint_reason="",
                    diff_samples=[],
                ),
            )
        controller.register_evidence_sources(
            [
                {
                    "title": f"Source {index}",
                    "url": f"https://example.com/source-{index}",
                    "source_type": "primary" if index % 2 == 0 else "secondary",
                    "used_for": "planning",
                }
                for index in range(6)
            ],
            used_for_prefix="planning",
        )
        for index in range(4):
            controller.refresh_skill_memory(
                {
                    "touched_files": [f"docs/{index}.md"],
                    "validation_completed": ["unit"],
                }
            )
        self.assertEqual(len(controller.session.state["checkpoint_summaries"]), 3)
        self.assertEqual(len(controller.session.state["worker_manifests"]), 2)
        self.assertEqual(len(controller.session.state["evidence_registry"]), 4)
        self.assertEqual(len(controller.session.state["skill_memory"]), 2)

    def test_collect_auxiliary_worker_summaries_respects_max_parallel_workers(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        controller.session.profile["worker_policy"]["max_parallel_workers"] = 2
        seen = []

        def fake_worker(role, payload, *, model, reasoning_effort):
            seen.append((role, model, reasoning_effort))
            return {"role": role, "summary": f"{role} ok", "findings": ["ok"], "confidence": "high"}

        controller.run_auxiliary_worker = fake_worker
        summaries = controller.collect_auxiliary_worker_summaries(
            ["research", "read_only_repo", "evaluator_vote"],
            {"task": "inspect"},
            model="gpt-5.4",
            reasoning_effort="xhigh",
        )
        self.assertEqual([entry["role"] for entry in summaries], ["research", "read_only_repo"])
        self.assertEqual([role for role, _, _ in seen], ["research", "read_only_repo"])

    def test_finish_writes_finished_marker(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        store.finish(session, "completed", "done")
        finished = json.loads((session.session_dir / "finished.json").read_text(encoding="utf-8"))
        self.assertEqual(finished["status"], "completed")

    def test_script_has_no_env_var_or_pips_defaults(self):
        script_text = SCRIPT_PATH.read_text(encoding="utf-8")
        self.assertNotIn("os.environ", script_text)
        self.assertNotIn("DEFAULT_PIPS_DIR", script_text)
        self.assertNotIn("PROMPT_FILE", script_text)


if __name__ == "__main__":
    unittest.main()
