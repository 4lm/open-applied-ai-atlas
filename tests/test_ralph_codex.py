import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "ralph-codex.py"
DEFAULT_MAX_EXECUTION_PROMPT_CHARS = 0
SPEC = importlib.util.spec_from_file_location("ralph_codex", SCRIPT_PATH)
ralph_codex = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = ralph_codex
SPEC.loader.exec_module(ralph_codex)


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


class RalphCodexTests(unittest.TestCase):
    def make_temp_root(self):
        tempdir = tempfile.TemporaryDirectory()
        root = Path(tempdir.name)
        return tempdir, root

    def make_schema_catalog(self):
        return ralph_codex.SchemaCatalog(ralph_codex.SCHEMA_FILES)

    def make_store(self, root):
        return ralph_codex.SessionStore(root / ".codex" / "ralph-codex", self.make_schema_catalog())

    def make_profile(self):
        profile = ralph_codex.deep_copy_json(ralph_codex.DEFAULT_PROFILE)
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

    def make_event_recorder(self, store, session, verbose=False, stderr=None):
        return ralph_codex.EventRecorder(store, session, verbose=verbose, stderr=stderr or io.StringIO())

    def make_controller(self, root, client=None, session=None, input_func=lambda _: "yes"):
        store, built_session = self.make_session(root)
        session = session or built_session
        client = client or FakeClient({}, [])
        runtime_config = ralph_codex.RuntimeConfig(workdir=root, state_root=store.root)
        event_recorder = self.make_event_recorder(store, session)
        return ralph_codex.RalphController(
            runtime_config,
            client,
            event_recorder,
            store,
            self.make_schema_catalog(),
            session,
            input_func=input_func,
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
        planning_result = {
            "status": "CHARTER_READY",
            "summary": "ok",
            "broadening_rationale": "wide",
            "charter": self.broad_charter(),
            "next_step": "execute",
            "gate_reasoning": "safe",
        }
        controller.session.state["charter_version"] = 1
        controller.store.save_charter(controller.session, planning_result, confirmed=True)

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

    def test_schema_files_are_v0_1_0_only(self):
        for path in sorted(ralph_codex.SCHEMA_ROOT.rglob("*.schema.json")):
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(payload["schema_version"], "0.1.0")
            self.assertIn("schema_id", payload)
            self.assertIn("-v0.1.0.schema.json", path.name)

    def test_default_profile_validates_against_profile_schema(self):
        self.make_schema_catalog().validate(ralph_codex.PROFILE_SCHEMA_ID, ralph_codex.DEFAULT_PROFILE)
        self.assertEqual(ralph_codex.DEFAULT_PROFILE["runtime_limits"]["max_iterations"], 0)
        self.assertEqual(ralph_codex.DEFAULT_PROFILE["execution"]["max_prompt_chars"], 0)

    def test_custom_profile_invalid_is_rejected(self):
        with tempfile.TemporaryDirectory() as tempdir:
            path = Path(tempdir) / "profile.json"
            invalid = ralph_codex.deep_copy_json(ralph_codex.DEFAULT_PROFILE)
            invalid["planning"]["reasoning_effort"] = "extreme"
            path.write_text(json.dumps(invalid), encoding="utf-8")
            with self.assertRaises(ralph_codex.RalphError):
                ralph_codex.load_profile(self.make_schema_catalog(), path)

    def test_custom_profile_rejects_negative_execution_prompt_limit(self):
        with tempfile.TemporaryDirectory() as tempdir:
            path = Path(tempdir) / "profile.json"
            invalid = ralph_codex.deep_copy_json(ralph_codex.DEFAULT_PROFILE)
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
        notification = events[-1]
        self.assertEqual(notification["event_type"], "notification")
        self.assertEqual(notification["payload"]["item"]["output_chars"], 120)
        self.assertNotIn("output", notification["payload"]["item"])

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

    def test_event_recorder_verbose_traces_to_stderr(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        stderr = io.StringIO()
        recorder = self.make_event_recorder(store, session, verbose=True, stderr=stderr)
        recorder.record_rpc_request(3, "turn/start", {"threadId": "thread-1", "input": [], "outputSchema": {}})
        self.assertIn("[ralph][rpc-request]", stderr.getvalue())

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

    def test_validate_charter_rejects_narrow_charter(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        narrow = self.broad_charter()
        narrow["workstreams"] = narrow["workstreams"][:2]
        planning_result = {
            "status": "CHARTER_READY",
            "summary": "ok",
            "broadening_rationale": "too narrow",
            "charter": narrow,
            "next_step": "execute",
            "gate_reasoning": "safe",
        }
        with self.assertRaises(ralph_codex.RalphError):
            controller.validate_charter(planning_result)

    def test_run_turn_handles_request_user_input_and_logs_turn(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        result_payload = {
            "status": "IN_PROGRESS",
            "summary": "working",
            "evidence": ["progress"],
            "workstream_updates": [{"id": "W1", "status": "in_progress", "evidence": ["ok"]}],
            "remaining_gaps": ["docs"],
            "validation_completed": ["unit"],
            "explicit_deferrals": [],
            "next_step": "continue",
            "gate_reasoning": "more work",
        }
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
            schema={"type": "object"},
            collaboration_mode=controller.make_collaboration_mode("default", "high", "instructions"),
        )
        self.assertEqual(result["status"], "IN_PROGRESS")
        self.assertEqual(client.sent_results[0][1]["answers"]["mode"]["answers"], ["Plan (Recommended)"])
        turns = (session.session_dir / "turns.jsonl").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(turns), 1)

    def test_run_turn_waits_through_silence_and_completes(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        result_payload = {
            "status": "IN_PROGRESS",
            "summary": "working",
            "evidence": ["progress"],
            "workstream_updates": [{"id": "W1", "status": "in_progress", "evidence": ["ok"]}],
            "remaining_gaps": [],
            "validation_completed": ["unit"],
            "explicit_deferrals": [],
            "next_step": "continue",
            "gate_reasoning": "more work",
        }

        class DelayedEventClient(FakeClient):
            def __init__(self):
                super().__init__({"turn/start": {"turn": {"id": "turn-1"}}}, [])
                self.poll_count = 0

            def next_event(self, timeout=0.1):
                self.poll_count += 1
                if self.poll_count <= 3:
                    return None
                if self.poll_count == 4:
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
                if self.poll_count == 5:
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
            schema=self.make_schema_catalog().model_schema(ralph_codex.EXECUTION_OUTPUT_SCHEMA_ID),
            collaboration_mode=controller.make_collaboration_mode("default", "high", "instructions"),
        )
        self.assertEqual(result["status"], "IN_PROGRESS")
        self.assertGreaterEqual(client.poll_count, 5)

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

    def test_run_turn_extracts_plan_thread_item_output(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        result_payload = {
            "status": "CHARTER_READY",
            "summary": "ready",
            "broadening_rationale": "wide enough",
            "charter": self.broad_charter(),
            "next_step": "execute",
            "gate_reasoning": "safe",
        }
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

    def test_rejected_completion_is_persisted_immediately(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        self.save_charter(controller)
        controller.session.profile["runtime_limits"]["max_iterations"] = 1
        controller.client.start = lambda: None
        controller.ensure_thread = lambda: None
        controller.confirm_seed_if_needed = lambda: None
        controller.execute_once = lambda: {
            "status": "COMPLETE",
            "summary": "done",
            "workstream_updates": [{"id": "W1", "status": "done", "evidence": ["ok"]}],
            "remaining_gaps": [],
            "validation_completed": ["unit"],
            "explicit_deferrals": [],
            "next_step": "none",
            "evidence": ["ok"],
            "gate_reasoning": "safe",
        }
        controller.plan_once = lambda phase_name, feedback: {
            "status": "CHARTER_READY",
            "summary": "retry",
            "broadening_rationale": "keep going",
            "charter": self.broad_charter(),
            "next_step": "execute",
            "gate_reasoning": "safe",
        }
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
                "status": "COMPLETE",
                "summary": "done",
                "workstream_updates": [{"id": "W1", "status": "done", "evidence": ["ok"]}],
                "remaining_gaps": [],
                "validation_completed": ["unit"],
                "explicit_deferrals": [],
                "next_step": "none",
                "evidence": ["ok"],
                "gate_reasoning": "safe",
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
                "status": "COMPLETE",
                "summary": "done",
                "workstream_updates": updates,
                "remaining_gaps": [],
                "validation_completed": ["unit", "integration", "gating"],
                "explicit_deferrals": [],
                "next_step": "none",
                "evidence": ["ok"],
                "gate_reasoning": "safe",
            }
        )
        self.assertTrue(accepted)
        self.assertEqual(reason, "")

    def test_build_execution_prompt_contains_charter_and_feedback(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        self.save_charter(controller)
        prompt = controller.build_execution_prompt("Need broader validation")
        self.assertIn("Current Charter", prompt)
        self.assertIn("Need broader validation", prompt)

    def test_build_execution_prompt_default_cap_is_unlimited(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        controller.session.task["message_text"] = "Test message " + ("x" * 5000)
        self.save_charter(controller)
        prompt = controller.build_execution_prompt("Need broader validation")
        self.assertGreater(len(prompt), 4000)
        self.assertEqual(controller.session.profile["execution"]["max_prompt_chars"], DEFAULT_MAX_EXECUTION_PROMPT_CHARS)

    def test_build_execution_prompt_rejects_when_over_custom_limit(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        self.save_charter(controller)
        controller.session.profile["execution"]["max_prompt_chars"] = 100
        with self.assertRaisesRegex(ralph_codex.RalphError, "charter="):
            controller.build_execution_prompt("Need broader validation")

    def test_build_execution_prompt_allows_unlimited_when_limit_is_zero(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        large_task = "Test message " + ("x" * 5000)
        controller.session.task["message_text"] = large_task
        controller.session.profile["execution"]["max_prompt_chars"] = 0
        self.save_charter(controller)
        prompt = controller.build_execution_prompt("Need broader validation")
        self.assertGreater(len(prompt), DEFAULT_MAX_EXECUTION_PROMPT_CHARS)

    def test_run_with_zero_max_iterations_treats_limit_as_unbounded(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        controller = self.make_controller(root)
        self.save_charter(controller)
        controller.session.profile["runtime_limits"]["max_iterations"] = 0
        controller.client.start = lambda: None
        controller.ensure_thread = lambda: None
        controller.confirm_seed_if_needed = lambda: None
        calls = {"execute": 0}

        def execute_once():
            calls["execute"] += 1
            return {
                "status": "COMPLETE" if calls["execute"] == 2 else "IN_PROGRESS",
                "summary": "done" if calls["execute"] == 2 else "working",
                "workstream_updates": [
                    {"id": "W1", "status": "done", "evidence": ["ok"]},
                    {"id": "W2", "status": "done", "evidence": ["ok"]},
                    {"id": "W3", "status": "done", "evidence": ["ok"]},
                ],
                "remaining_gaps": [],
                "validation_completed": ["unit", "integration", "gating"],
                "explicit_deferrals": [],
                "next_step": "none",
                "evidence": ["ok"],
                "gate_reasoning": "safe",
            }

        controller.execute_once = execute_once
        controller.plan_once = lambda phase_name, feedback: {
            "status": "CHARTER_READY",
            "summary": "retry",
            "broadening_rationale": "keep going",
            "charter": self.broad_charter(),
            "next_step": "execute",
            "gate_reasoning": "safe",
        }
        result = controller.run()
        self.assertEqual(result, 0)
        self.assertEqual(calls["execute"], 2)

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

    def test_readme_documents_new_cli_surface(self):
        readme_text = (Path(__file__).resolve().parents[1] / "README.md").read_text(encoding="utf-8")
        self.assertIn("--message", readme_text)
        self.assertIn("--profile", readme_text)
        self.assertIn("--file", readme_text)
        self.assertIn("--verbose", readme_text)
        self.assertIn("--sessions", readme_text)
        self.assertIn("--resume", readme_text)
        self.assertIn("does not use turn inactivity timeouts", readme_text)
        self.assertIn("`max_iterations` uses `0` to mean unlimited", readme_text)
        self.assertIn("events.jsonl", readme_text)
        self.assertIn("python3 -m py_compile scripts/ralph-codex.py tests/test_ralph_codex.py", readme_text)
        self.assertNotIn("--prompt", readme_text)
        self.assertNotIn("--config", readme_text)
        self.assertNotIn("PROMPT_FILE", readme_text)

    def test_root_mission_replaces_pips_mission(self):
        root = Path(__file__).resolve().parents[1]
        self.assertTrue((root / "MISSION.md").exists())
        self.assertFalse((root / "pips" / "MISSION.md").exists())
        readme_text = (root / "README.md").read_text(encoding="utf-8")
        self.assertIn("[MISSION.md](./MISSION.md)", readme_text)
        self.assertNotIn("pips/MISSION.md", readme_text)


if __name__ == "__main__":
    unittest.main()
