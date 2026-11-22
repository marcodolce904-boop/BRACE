import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from check_plugin import check_plugin  # noqa: E402


def make_plugin(tmp, lang="en", name=None, display="BRACE", version="0.2.0",
                body="Body.\n", description="Short description.", skill="demo"):
    root = Path(tmp)
    (root / ".claude-plugin").mkdir(parents=True)
    (root / ".claude-plugin" / "plugin.json").write_text(json.dumps({
        "name": name or ("brace" if lang == "en" else "brace-it"),
        "displayName": display,
        "version": version,
        "description": "Plugin description.",
    }))
    skill_dir = root / "skills" / skill
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "---\nname: %s\ndescription: %s\n---\n\n%s" % (skill, description, body))
    return root


class CheckPluginTests(unittest.TestCase):
    def errors(self, lang="en", **kw):
        with tempfile.TemporaryDirectory() as tmp:
            return check_plugin(make_plugin(tmp, lang, **kw), lang)

    def test_clean_plugin_passes(self):
        self.assertEqual(self.errors(), [])

    def test_old_name_rejected(self):
        for body in ("Uses V.A.N.T.A. here.\n", "Run /vanta: now.\n",
                     "The vanta plugin.\n"):
            errs = self.errors(body=body)
            self.assertTrue(errs, body)
            self.assertTrue(any("SKILL.md" in e for e in errs), errs)

    def test_migration_path_allowed(self):
        self.assertEqual(self.errors(body="Move `.vanta/` to `.brace/`.\n"), [])

    def test_plugin_json_identity(self):
        self.assertTrue(self.errors("en", name="brace-it"))
        self.assertTrue(self.errors("it", name="brace"))
        self.assertEqual(self.errors("it"), [])
        self.assertTrue(self.errors(display="BRACE (English)"))
        self.assertTrue(self.errors(version="0.1.0"))

    def test_description_length(self):
        self.assertTrue(self.errors(description="x" * 1025))
        self.assertEqual(self.errors(description="x" * 1024), [])
        self.assertEqual(self.errors(description='"%s"' % ("x" * 1024)), [])
        self.assertTrue(self.errors(description='"%s"' % ("x" * 1025)))

    def test_evals_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_plugin(tmp)
            (root / "evals").mkdir()
            (root / "evals" / "p.md").write_text("V.A.N.T.A. vanta\n")
            self.assertEqual(check_plugin(root, "en"), [])

    def test_triggers_missing(self):
        errs = self.errors(skill="decision",
                           description="Records a DECISION. Use it when the user says I've decided.")
        self.assertTrue(any("decision" in e and "ho deciso" in e for e in errs), errs)
        errs = self.errors("it", skill="decisione",
                           description="Registra una scelta. Usala quando l'utente dice ho deciso.")
        self.assertTrue(any("decisione" in e and "DECISIONE" in e for e in errs), errs)
        self.assertTrue(any("I've decided" in e for e in errs), errs)

    def test_triggers_present(self):
        self.assertEqual(self.errors(
            skill="decision",
            description="Records a decision. Use it when the user says i've decided, Ho deciso, or DECISION."), [])
        self.assertEqual(self.errors(
            "it", skill="punto-nave",
            description="Usala per PUNTO NAVE, STOP, facciamo il punto, where are we."), [])

    def test_real_plugins_pass(self):
        self.assertEqual(check_plugin(ROOT / "plugins" / "brace", "en"), [])
        self.assertEqual(check_plugin(ROOT / "plugins" / "brace-it", "it"), [])


if __name__ == "__main__":
    unittest.main()
