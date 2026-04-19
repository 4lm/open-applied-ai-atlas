import unittest
from pathlib import Path


MAX_AGENTS_MD_CHARS = 4000
AGENTS_PATH = Path(__file__).resolve().parents[1] / "AGENTS.md"


class AgentsMdGuardTests(unittest.TestCase):
    def test_agents_md_stays_under_max_chars(self):
        text = AGENTS_PATH.read_text(encoding="utf-8")
        self.assertLessEqual(
            len(text),
            MAX_AGENTS_MD_CHARS,
            f"AGENTS.md is {len(text)} chars; limit is {MAX_AGENTS_MD_CHARS}",
        )


if __name__ == "__main__":
    unittest.main()
