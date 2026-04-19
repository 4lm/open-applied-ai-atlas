import importlib.util
import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRIBUTING_PATH = ROOT / "CONTRIBUTING.md"
README_PATH = ROOT / "README.md"
RALPH_CONTROLLER_PATH = ROOT / "RALPH_CONTROLLER.md"
RALPH_SCRIPT_PATH = ROOT / "scripts" / "ralph-codex.py"
ROOT_DOC_MAP_PATH = ROOT / "docs" / "01-scope-and-principles" / "01-03-01-root-docs-and-topic-chapters.md"
PIPS_DIR = ROOT / "pips"

SPEC = importlib.util.spec_from_file_location("ralph_codex_repo_contracts", RALPH_SCRIPT_PATH)
ralph_codex = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = ralph_codex
SPEC.loader.exec_module(ralph_codex)


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    frontmatter: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return frontmatter
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip()
    return frontmatter


def extract_markdown_section(text: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if not match:
        raise AssertionError(f"missing section: {heading}")
    return match.group(1).strip()


def parse_markdown_table(section_text: str) -> list[dict[str, str]]:
    table_lines = [line.strip() for line in section_text.splitlines() if line.strip().startswith("|")]
    if len(table_lines) < 2:
        raise AssertionError("expected markdown table")

    headers = [cell.strip() for cell in table_lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in table_lines[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != len(headers):
            raise AssertionError(f"table row does not match header width: {line}")
        rows.append(dict(zip(headers, cells)))
    return rows


def extract_link_label(markdown_cell: str) -> str:
    match = re.search(r"\[([^\]]+)\]\([^)]+\)", markdown_cell)
    if not match:
        raise AssertionError(f"expected markdown link cell, got: {markdown_cell}")
    return match.group(1)


class RepoContractTests(unittest.TestCase):
    def test_root_doc_map_covers_actual_root_markdown_docs(self):
        root_markdown_docs = {path.name for path in ROOT.glob("*.md")}
        root_doc_map_text = ROOT_DOC_MAP_PATH.read_text(encoding="utf-8")
        root_docs_map = extract_markdown_section(root_doc_map_text, "Root Docs Map")
        mapped_docs = {
            extract_link_label(row["Root doc"])
            for row in parse_markdown_table(root_docs_map)
        }
        self.assertEqual(root_markdown_docs, mapped_docs)

    def test_readme_stays_entrypoint_and_links_chapter_owned_orientation(self):
        readme_text = README_PATH.read_text(encoding="utf-8")
        self.assertNotIn("## Role-Based Reading Paths", readme_text)
        self.assertIn("01-02-01-role-based-reading-paths.md", readme_text)
        self.assertIn("01-03-01-root-docs-and-topic-chapters.md", readme_text)

    def test_contributing_documents_pip_contract(self):
        contributing_text = CONTRIBUTING_PATH.read_text(encoding="utf-8")
        for required_text in [
            "pips/PIP_*.md",
            "pip-status",
            "live",
            "archived",
            "superseded",
            "superseded_by",
            "retention_reason",
        ]:
            self.assertIn(required_text, contributing_text)

    def test_ralph_controller_documents_canonical_contract(self):
        ralph_text = RALPH_CONTROLLER_PATH.read_text(encoding="utf-8")
        help_result = subprocess.run(
            [sys.executable, str(RALPH_SCRIPT_PATH), "--help"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(help_result.returncode, 0, help_result.stderr)

        for flag in ["--message", "--file", "--profile", "--verbose", "--sessions", "--resume"]:
            self.assertIn(flag, help_result.stdout)
            self.assertIn(flag, ralph_text)

        self.assertIn("./scripts/ralph-codex.py --resume 3", ralph_text)
        self.assertNotIn("--prompt", ralph_text)
        self.assertNotIn("--config", ralph_text)

        for relative_path in [
            "prompts/fix-tests.md",
            "profiles/cautious.json",
            "profiles/dangerously-unrestricted.json",
        ]:
            self.assertIn(relative_path, ralph_text)
            self.assertTrue((ROOT / relative_path).exists(), relative_path)
        self.assertIn("schemas/ralph-codex/", ralph_text)
        self.assertTrue((ROOT / "schemas" / "ralph-codex").is_dir())

        default_access_mode = ralph_codex.DEFAULT_PROFILE["thread_policy"]["access_mode"]
        default_sandbox = ralph_codex.SANDBOX_BY_ACCESS_MODE[default_access_mode]
        self.assertIn(f'thread_policy.access_mode: "{default_access_mode}"', ralph_text)
        self.assertIn(default_sandbox, ralph_text)
        self.assertIn("dangerously-unrestricted", ralph_text)
        self.assertIn("danger-full-access", ralph_text)
        self.assertIn("approvalPolicy", ralph_text)
        self.assertIn("`never`", ralph_text)
        self.assertIn("max_iterations", ralph_text)
        self.assertIn("execution.max_prompt_chars", ralph_text)
        self.assertIn("events.jsonl", ralph_text)

        self.assertIn(
            "python3 -m py_compile scripts/ralph-codex.py tests/test_ralph_codex.py tests/test_repo_contracts.py",
            ralph_text,
        )
        self.assertIn(
            "python3 -m unittest tests.test_repo_contracts tests.test_ralph_codex",
            ralph_text,
        )

    def test_all_pips_have_valid_pip_status_frontmatter(self):
        pip_paths = sorted(PIPS_DIR.glob("PIP_*.md"))
        self.assertTrue(pip_paths, "expected at least one PIP file")
        for path in pip_paths:
            frontmatter = parse_frontmatter(path.read_text(encoding="utf-8"))
            self.assertIn("pip-status", frontmatter, f"{path.name} missing pip-status frontmatter")
            self.assertIn(
                frontmatter["pip-status"],
                {"live", "archived", "superseded"},
                f"{path.name} has invalid pip-status",
            )
            if frontmatter["pip-status"] == "superseded":
                self.assertIn("superseded_by", frontmatter, f"{path.name} missing superseded_by")
            if frontmatter["pip-status"] == "archived":
                self.assertIn("retention_reason", frontmatter, f"{path.name} missing retention_reason")


if __name__ == "__main__":
    unittest.main()
