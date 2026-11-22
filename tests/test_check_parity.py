import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from check_parity import check_parity  # noqa: E402


def write(root, rel, text):
    path = Path(root) / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def md(headings=("# A", "## B"), front=None):
    front = front if front is not None else {"name": "x", "description": "d"}
    head = "".join(f"{k}: {v}\n" for k, v in front.items())
    return f"---\n{head}---\n\n" + "\n\ntext\n\n".join(headings) + "\n"


class ParityCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)
        self.en = self.tmp / "en"
        self.it = self.tmp / "it"
        self.changelog = self.tmp / "CHANGELOG.md"
        self.changelog.write_text("# Changelog\n\n## 0.2.0 · x\n")
        for root in (self.en, self.it):
            write(root, ".claude-plugin/plugin.json", json.dumps({"version": "0.2.0"}))

    def run_parity(self):
        return check_parity(self.en, self.it, self.changelog)


class TestParity(ParityCase):
    def test_clean_tree(self):
        write(self.en, "skills/method/SKILL.md", md())
        write(self.it, "skills/metodo/SKILL.md", md())
        self.assertEqual(self.run_parity(), [])

    def test_missing_it_file(self):
        write(self.en, "skills/method/SKILL.md", md())
        errors = self.run_parity()
        self.assertEqual(len(errors), 1)
        self.assertIn("skills/method/SKILL.md", errors[0])
        self.assertIn("skills/metodo/SKILL.md", errors[0])

    def test_missing_en_file(self):
        write(self.it, "agents/nemesi.md", md())
        errors = self.run_parity()
        self.assertEqual(len(errors), 1)
        self.assertIn("agents/nemesi.md", errors[0])

    def test_results_dir_skipped(self):
        write(self.en, "evals/results/run.md", md())
        self.assertEqual(self.run_parity(), [])

    def test_heading_count_mismatch(self):
        write(self.en, "agents/red.md", md(("# A", "## B", "## C")))
        write(self.it, "agents/rosso.md", md(("# A", "## B")))
        errors = self.run_parity()
        self.assertEqual(len(errors), 1)
        self.assertIn("agents/red.md", errors[0])

    def test_deep_headings_and_code_fences_ignored(self):
        en = md() + "\n### Deep\n\n```\n# not a heading\n```\n"
        write(self.en, "agents/red.md", en)
        write(self.it, "agents/rosso.md", md())
        self.assertEqual(self.run_parity(), [])

    def test_frontmatter_keys(self):
        write(self.en, "agents/red.md", md(front={"name": "a", "model": "x"}))
        write(self.it, "agents/rosso.md", md(front={"name": "a"}))
        self.assertEqual(len(self.run_parity()), 1)

    def test_frontmatter_strict_values(self):
        for key in ("model", "tools", "disable-model-invocation",
                    "keep-coding-instructions", "max_turns", "allowed_tools",
                    "type", "weight"):
            with self.subTest(key=key):
                write(self.en, "agents/red.md", md(front={"name": "a", key: "1"}))
                write(self.it, "agents/rosso.md", md(front={"name": "a", key: "2"}))
                self.assertEqual(len(self.run_parity()), 1)

    def test_frontmatter_text_values_free(self):
        front_en = {"name": "a", "description": "one", "argument-hint": "x"}
        front_it = {"name": "b", "description": "uno", "argument-hint": "y"}
        write(self.en, "agents/red.md", md(front=front_en))
        write(self.it, "agents/rosso.md", md(front=front_it))
        self.assertEqual(self.run_parity(), [])

    def test_version_alignment(self):
        write(self.it, ".claude-plugin/plugin.json", json.dumps({"version": "0.3.0"}))
        self.assertTrue(any("version" in e for e in self.run_parity()))

    def test_changelog_missing_version(self):
        self.changelog.write_text("# Changelog\n\n## 0.1.0\n")
        self.assertTrue(any("CHANGELOG" in e for e in self.run_parity()))


class TestRealTree(unittest.TestCase):
    def test_real_tree_passes(self):
        errors = check_parity(ROOT / "plugins/brace", ROOT / "plugins/brace-it",
                              ROOT / "CHANGELOG.md")
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
