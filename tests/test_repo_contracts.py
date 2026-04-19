import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"
PIPS_DIR = ROOT / "pips"


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
    return {}


class RepoContractTests(unittest.TestCase):
    def test_readme_example_paths_exist(self):
        readme_text = README_PATH.read_text(encoding="utf-8")
        for relative_path in [
            "prompts/fix-tests.md",
            "profiles/cautious.json",
            "profiles/dangerously-unrestricted.json",
        ]:
            self.assertIn(relative_path, readme_text)
            self.assertTrue((ROOT / relative_path).exists(), relative_path)

    def test_all_pips_have_valid_status_frontmatter(self):
        pip_paths = sorted(PIPS_DIR.glob("PIP_*.md"))
        self.assertTrue(pip_paths, "expected at least one PIP file")
        for path in pip_paths:
            frontmatter = parse_frontmatter(path.read_text(encoding="utf-8"))
            self.assertIn("status", frontmatter, f"{path.name} missing status frontmatter")
            self.assertIn(
                frontmatter["status"],
                {"live", "archived", "superseded"},
                f"{path.name} has invalid status",
            )
            if frontmatter["status"] == "superseded":
                self.assertIn("superseded_by", frontmatter, f"{path.name} missing superseded_by")
            if frontmatter["status"] == "archived":
                self.assertIn("retention_reason", frontmatter, f"{path.name} missing retention_reason")

    def test_readme_documents_ralph_access_modes(self):
        readme_text = README_PATH.read_text(encoding="utf-8")
        self.assertIn("approvalPolicy", readme_text)
        self.assertIn("`never`", readme_text)
        self.assertIn("workspace-write", readme_text)
        self.assertIn("dangerously-unrestricted", readme_text)
        self.assertIn("danger-full-access", readme_text)


if __name__ == "__main__":
    unittest.main()
