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


class FakeTTYStream(io.StringIO):
    def isatty(self):
        return True


class CaptureReporter:
    def __init__(self, verbose, stdout=None, stderr=None):
        self.verbose = verbose
        self.stdout = stdout or io.StringIO()
        self.stderr = stderr or io.StringIO()

    def status(self, message):
        self.stdout.write(message + "\n")

    def event(self, message, tone="event"):
        self.stderr.write(message + "\n")

    def wait(self, phase_name, elapsed_seconds, command_rows=None):
        self.stdout.write(f"wait {phase_name} {elapsed_seconds}\n")
        for row in command_rows or []:
            self.stdout.write(f"cmd {row.get('status')}: {row.get('command')}\n")

    def tool(self, action, detail, stream_name="stderr"):
        stream = self.stdout if stream_name == "stdout" else self.stderr
        stream.write(f"tool {action}: {detail}\n")

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
        planning_result = {
            "status": "CHARTER_READY",
            "summary": "ok",
            "broadening_rationale": "wide",
            "charter": self.broad_charter(),
            "next_step": "execute",
            "gate_reasoning": "safe",
        }
        controller.session.state["charter_version"] = 1
        controller.store.save_charter(
            controller.session,
            planning_result,
            confirmed=True,
            review_state="approved",
        )

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

    def test_schema_files_all_live_under_ralph_codex_schema_dir(self):
        expected_root = ralph_codex.SCHEMA_ROOT / "ralph-codex"
        for path in ralph_codex.SCHEMA_FILES.values():
            self.assertEqual(path.parent, expected_root)
        self.assertEqual(
            ralph_codex.SCHEMA_FILES[ralph_codex.PROFILE_SCHEMA_ID],
            expected_root / "profile-v0.1.0.schema.json",
        )

    def test_default_profile_validates_against_profile_schema(self):
        self.make_schema_catalog().validate(ralph_codex.PROFILE_SCHEMA_ID, ralph_codex.DEFAULT_PROFILE)
        self.assertEqual(ralph_codex.DEFAULT_PROFILE["thread_policy"]["access_mode"], "restricted")
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

    def test_custom_profile_rejects_invalid_thread_access_mode(self):
        with tempfile.TemporaryDirectory() as tempdir:
            path = Path(tempdir) / "profile.json"
            invalid = ralph_codex.deep_copy_json(ralph_codex.DEFAULT_PROFILE)
            invalid["thread_policy"]["access_mode"] = "unsafe"
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
        self.assertIn("EVENT", console)
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
        self.assertIn("TRACE", console)
        self.assertIn("truncated for", console)
        self.assertLessEqual(max(len(line) for line in console.splitlines()), 120)
        events = store.read_jsonl(session.session_dir / "events.jsonl", ralph_codex.EVENT_LOG_LINE_SCHEMA_ID)
        wire = events[-1]
        self.assertEqual(wire["payload"]["payload"]["params"]["item"]["output"], long_output)

    def test_event_recorder_verbose_traces_to_stderr(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        stderr = io.StringIO()
        recorder = self.make_event_recorder(store, session, verbose=True, stderr=stderr)
        recorder.record_rpc_request(3, "turn/start", {"threadId": "thread-1", "input": [], "outputSchema": {}})
        self.assertIn("rpc-request", stderr.getvalue())

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
                    "status": "completed",
                    "output_chars": 17,
                    "command_actions": 1,
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
            def __init__(self, runtime_config, event_recorder, session_log=None):
                self.runtime_config = runtime_config
                self.event_recorder = event_recorder
                self.closed = False
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
            def __init__(self, runtime_config, event_recorder, session_log=None):
                self.closed = False
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
        log_paths = sorted((session.session_dir / "logs").glob("*.log"))
        self.assertEqual(len(log_paths), 1)
        rendered = log_paths[0].read_text(encoding="utf-8")
        self.assertIn("# Ralph Codex run log", rendered)
        self.assertIn("invocation_mode: message", rendered)
        self.assertIn("CONSOLE-STDOUT", rendered)
        self.assertIn("run started: session=", rendered)
        self.assertIn("run completed: session completed", rendered)

    def test_plain_text_run_log_captures_console_and_app_stdio(self):
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
        reporter.status("hello status")
        reporter.event("hello event")
        reporter.console_input("approve\n")

        client = ralph_codex.SubprocessAppServerClient(
            ralph_codex.RuntimeConfig(workdir=root, state_root=store.root),
            self.make_event_recorder(store, session, reporter=reporter),
            session_log=session_log,
        )
        client.process = FakeProcess()
        client._send_json({"id": 7, "method": "ping"})
        client.session_log.write_app_stdout('{"ok":true}\n')
        client.session_log.write_app_stderr("warn line\n")
        session_log.close()

        rendered = (session.session_dir / "logs" / "run-1.log").read_text(encoding="utf-8")
        self.assertIn("CONSOLE-STDOUT", rendered)
        self.assertIn("hello status", rendered)
        self.assertIn("CONSOLE-STDERR", rendered)
        self.assertIn("hello event", rendered)
        self.assertIn("CONSOLE-STDIN approve", rendered)
        self.assertIn('APP-STDIN {"id":7,"method":"ping"}', rendered)
        self.assertIn('APP-STDOUT {"ok":true}', rendered)
        self.assertIn("APP-STDERR warn line", rendered)

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
        stdout = io.StringIO()
        stderr = io.StringIO()
        reporter = self.make_reporter(stdout=stdout, stderr=stderr)
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
        self.assertIn("test: turn started turn-1", stdout.getvalue())
        self.assertIn("test: turn completed turn-1 -> IN_PROGRESS: working", stdout.getvalue())
        self.assertIn("test result", stdout.getvalue())
        self.assertIn("summary:", stdout.getvalue())

    def test_run_turn_waits_through_silence_and_completes(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        stdout = io.StringIO()
        reporter = self.make_reporter(stdout=stdout)
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
        self.assertIn("WAIT", stdout.getvalue())
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
        self.assertEqual(console.count("/bin/zsh -lc 'echo hi'"), 2)
        self.assertIn("inProgress: /bin/zsh -lc 'echo hi' | actions=1 | pid=123", console)
        self.assertIn("completed: /bin/zsh -lc 'echo hi' | output=17 chars | actions=1 | pid=123", console)

    def test_run_turn_wait_stays_thin_while_commands_print_live(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        stdout = io.StringIO()
        reporter = self.make_reporter(stdout=stdout)
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
        self.assertIn("inProgress: /bin/zsh -lc 'echo hi' | actions=1 | pid=123", console)
        self.assertIn("completed: /bin/zsh -lc 'echo hi' | output=17 chars | actions=1 | pid=123", console)
        self.assertIn("execution-1 running for 11s", console)
        self.assertNotIn("commands: ", console)
        self.assertEqual(console.count("/bin/zsh -lc 'echo hi'"), 2)

    def test_run_turn_verbose_mode_avoids_duplicate_command_console_output(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        stdout = io.StringIO()
        stderr = io.StringIO()
        reporter = self.make_reporter(verbose=True, stdout=stdout, stderr=stderr)
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
        self.assertIn("inProgress: /bin/zsh -lc 'echo verbose' | actions=1 | pid=321", stdout.getvalue())
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

    def test_review_plan_if_needed_renders_full_review_and_exec_context(self):
        tempdir, root = self.make_temp_root()
        self.addCleanup(tempdir.cleanup)
        store, session = self.make_session(root)
        session.profile["seed_policy"]["require_confirmation"] = True
        session.profile["seed_policy"]["auto_confirm"] = False
        long_summary = "Operator review summary " * 18
        planning_result = {
            "status": "CHARTER_READY",
            "summary": long_summary.strip(),
            "broadening_rationale": "Review before unattended execution.",
            "charter": self.broad_charter(),
            "next_step": "Await operator approval.",
            "gate_reasoning": "The operator must approve the broadened charter.",
        }
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
        initial_result = {
            "status": "CHARTER_READY",
            "summary": "initial draft",
            "broadening_rationale": "wide",
            "charter": self.broad_charter(),
            "next_step": "review",
            "gate_reasoning": "safe",
        }
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
        revised_result = {
            "status": "CHARTER_READY",
            "summary": "revised draft",
            "broadening_rationale": "broader",
            "charter": revised_charter,
            "next_step": "review",
            "gate_reasoning": "safe",
        }
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
        planning_result = {
            "status": "CHARTER_READY",
            "summary": "first draft",
            "broadening_rationale": "wide",
            "charter": self.broad_charter(),
            "next_step": "review",
            "gate_reasoning": "safe",
        }
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
        controller.review_plan_if_needed = lambda: None
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
        controller.review_plan_if_needed = lambda: None
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


if __name__ == "__main__":
    unittest.main()
