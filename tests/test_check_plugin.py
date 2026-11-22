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


METHOD_EN = "BRACE: not sure whether, non so se, is this a good idea."
METHOD_IT = "BRACE: non so se, not sure whether, è una buona idea."
WARGAME_EN = "WARGAME: how would competitors react, come reagirebbe."
WARGAME_IT = "WARGAME: come reagirebbe, how would competitors react."
STRESS = "STRESS TEST: how could this go wrong, come potrebbe andare storto."


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

    # Task 5: routing and cost gates

    def test_method_next_tool_section(self):
        self.assertEqual(self.errors(skill="method", description=METHOD_EN,
                                     body="## Next tool\n\nOffer it.\n"), [])
        errs = self.errors(skill="method", description=METHOD_EN,
                           body="## Plugin tools\n\n- `/brace:decision`\n")
        self.assertTrue(any("Next tool" in e for e in errs), errs)
        self.assertEqual(self.errors("it", skill="metodo", description=METHOD_IT,
                                     body="## Strumento successivo\n\nProponilo.\n"), [])
        errs = self.errors("it", skill="metodo", description=METHOD_IT,
                           body="## Strumenti del plugin\n\nTesto.\n")
        self.assertTrue(any("Strumento successivo" in e for e in errs), errs)

    def test_wargame_cost_gate_first(self):
        good = "# W\n\n## Cost check\n\nAsk.\n\n## Preparation\n\nSet.\n"
        self.assertEqual(self.errors(skill="wargame", description=WARGAME_EN, body=good), [])
        bad = "# W\n\n## Preparation\n\nSet.\n\n## Cost check\n\nAsk.\n"
        errs = self.errors(skill="wargame", description=WARGAME_EN, body=bad)
        self.assertTrue(any("Cost check" in e for e in errs), errs)
        good_it = "# W\n\n## Controllo del costo\n\nChiedi.\n\n## Preparazione\n\nFissa.\n"
        self.assertEqual(self.errors("it", skill="wargame", description=WARGAME_IT,
                                     body=good_it), [])
        errs = self.errors("it", skill="wargame", description=WARGAME_IT,
                           body="# W\n\n## Preparazione\n\nFissa.\n")
        self.assertTrue(any("Controllo del costo" in e for e in errs), errs)

    def test_wargame_model_invocation_enabled(self):
        good = "# W\n\n## Cost check\n\nAsk.\n"
        errs = self.errors(skill="wargame", body=good,
                           description=WARGAME_EN + "\ndisable-model-invocation: true")
        self.assertTrue(any("disable-model-invocation" in e for e in errs), errs)

    def test_stress_test_independent_waits(self):
        good = "## Modes\n\n- **Standard.** Cheap.\n- **Independent.** Warn in one line and wait for a yes.\n"
        self.assertEqual(self.errors(skill="stress-test", description=STRESS, body=good), [])
        bad = "## Modes\n\n- **Standard.** Cheap.\n- **Independent.** Higher cost: warn the user in one line.\n"
        errs = self.errors(skill="stress-test", description=STRESS, body=bad)
        self.assertTrue(any("wait for a yes" in e for e in errs), errs)
        good_it = "## Modalità\n\n- **Indipendente.** Avvisa in una riga e aspetta un sì.\n"
        self.assertEqual(self.errors("it", skill="stress-test", description=STRESS,
                                     body=good_it), [])
        bad_it = "## Modalità\n\n- **Indipendente.** Avvisa in una riga.\n"
        errs = self.errors("it", skill="stress-test", description=STRESS, body=bad_it)
        self.assertTrue(any("aspetta un sì" in e for e in errs), errs)

    def test_output_style_without_commands(self):
        for lang, cmd in (("en", "/brace:decision"), ("it", "/brace-it:decisione")):
            with tempfile.TemporaryDirectory() as tmp:
                root = make_plugin(tmp, lang)
                (root / "output-styles").mkdir()
                style = root / "output-styles" / "brace.md"
                style.write_text("---\nname: BRACE\n---\n\nJust ask for a stress test.\n")
                self.assertEqual(check_plugin(root, lang), [])
                style.write_text("---\nname: BRACE\n---\n\nSuggest `%s`.\n" % cmd)
                errs = check_plugin(root, lang)
                self.assertTrue(any("output-styles/brace.md" in e for e in errs), errs)

    def test_real_plugins_pass(self):
        self.assertEqual(check_plugin(ROOT / "plugins" / "brace", "en"), [])
        self.assertEqual(check_plugin(ROOT / "plugins" / "brace-it", "it"), [])


if __name__ == "__main__":
    unittest.main()
