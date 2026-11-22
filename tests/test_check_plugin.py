import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from check_plugin import VERSION, check_plugin  # noqa: E402


def make_plugin(tmp, lang="en", name=None, display="BRACE", version=VERSION,
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
DECISION_EN = "Records a decision. Use it when the user says i've decided, Ho deciso, or DECISION."
PF_IT = "Usala per PUNTO NAVE, STOP, facciamo il punto, where are we."
ENV_EN = "\n## Where you are running\n\nCheck capabilities.\n"
ENV_IT = "\n## Dove stai lavorando\n\nControlla le capacità.\n"


def add_eval(root, name, prompt, grader=True):
    """Create evals/<name>/ with an optional prompt.md and graders/criteria.md."""
    case = Path(root) / "evals" / name
    (case / "graders").mkdir(parents=True, exist_ok=True)
    if prompt is not None:
        (case / "prompt.md").write_text(prompt)
    if grader:
        (case / "graders" / "criteria.md").write_text("---\ntype: llm\nweight: 1\n---\n\nOk.\n")


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

    def test_evals_old_name_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_plugin(tmp)
            add_eval(root, "case", "Use the V.A.N.T.A. method.\n")
            errs = check_plugin(root, "en")
            self.assertTrue(any("evals/case/prompt.md" in e and "old name" in e for e in errs), errs)

    def test_evals_missing_grader(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_plugin(tmp)
            add_eval(root, "case", "Plain.\n", grader=False)
            errs = check_plugin(root, "en")
            self.assertTrue(any("evals/case" in e and "criteria.md" in e for e in errs), errs)

    def test_evals_missing_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_plugin(tmp)
            add_eval(root, "case", None)
            errs = check_plugin(root, "en")
            self.assertTrue(any("evals/case" in e and "prompt.md" in e for e in errs), errs)

    def test_evals_route_keyword_rejected(self):
        for text in ("Please do a STRESS TEST of my plan.", "Run a WARGAME.",
                     "DECISIONE presa.", "Use BRACE here.", "Say STOP now."):
            with tempfile.TemporaryDirectory() as tmp:
                root = make_plugin(tmp)
                add_eval(root, "route-x", "---\nmax_turns: 4\n---\n\n%s\n" % text)
                errs = check_plugin(root, "en")
                self.assertTrue(any("route-x" in e and "keyword" in e for e in errs), (text, errs))

    def test_evals_route_slash_command_rejected(self):
        for text in ("Try /brace:decision please.", "Run /stress-test now.", "/review this"):
            with tempfile.TemporaryDirectory() as tmp:
                root = make_plugin(tmp)
                add_eval(root, "route-x", "%s\n" % text)
                errs = check_plugin(root, "en")
                self.assertTrue(any("route-x" in e and "slash" in e for e in errs), (text, errs))

    def test_evals_route_natural_prompt_passes(self):
        text = ("Should I take the job and/or stay? See https://example.com/a/b. "
                "I made a decision and want a review of the plan, 50/50 odds, 3/4 sure.\n")
        with tempfile.TemporaryDirectory() as tmp:
            root = make_plugin(tmp)
            add_eval(root, "route-x", text)
            self.assertEqual(check_plugin(root, "en"), [])

    def test_evals_route_punto_nave_exempt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_plugin(tmp)
            add_eval(root, "route-punto-nave", "Summary. PUNTO NAVE\n")
            self.assertEqual(check_plugin(root, "en"), [])

    def test_evals_non_route_may_use_keywords(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_plugin(tmp)
            add_eval(root, "position-fix", "Summary. POSITION FIX\n")
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
        mem_en = ENV_EN + "\n## Memory in chat\n\nUse `brace-decisions.md`.\n"
        mem_it = ENV_IT + "\n## Memoria in chat\n\nUsa `brace-punto-nave.md`.\n"
        self.assertEqual(self.errors(skill="decision", description=DECISION_EN, body=mem_en), [])
        self.assertEqual(self.errors("it", skill="punto-nave", description=PF_IT, body=mem_it), [])

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
        good = "# W\n\n## Cost check\n\nAsk.\n" + ENV_EN + "\n## Preparation\n\nSet.\n"
        self.assertEqual(self.errors(skill="wargame", description=WARGAME_EN, body=good), [])
        bad = "# W\n\n## Preparation\n\nSet.\n\n## Cost check\n\nAsk.\n"
        errs = self.errors(skill="wargame", description=WARGAME_EN, body=bad)
        self.assertTrue(any("Cost check" in e for e in errs), errs)
        good_it = ("# W\n\n## Controllo del costo\n\nChiedi.\n" + ENV_IT
                   + "\n## Preparazione\n\nFissa.\n")
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
        good = ENV_EN + "## Modes\n\n- **Standard.** Cheap.\n- **Independent.** Warn in one line and wait for a yes.\n"
        self.assertEqual(self.errors(skill="stress-test", description=STRESS, body=good), [])
        bad = "## Modes\n\n- **Standard.** Cheap.\n- **Independent.** Higher cost: warn the user in one line.\n"
        errs = self.errors(skill="stress-test", description=STRESS, body=bad)
        self.assertTrue(any("wait for a yes" in e for e in errs), errs)
        good_it = ENV_IT + "## Modalità\n\n- **Indipendente.** Avvisa in una riga e aspetta un sì.\n"
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

    # Task 6: levels and memory in chat

    def test_environment_section_required(self):
        for lang, skill, desc in (("en", "stress-test", STRESS), ("en", "wargame", WARGAME_EN),
                                  ("it", "stress-test", STRESS), ("it", "wargame", WARGAME_IT)):
            cost = "## Cost check\n\nAsk.\n" if lang == "en" else "## Controllo del costo\n\nChiedi.\n"
            indep = ("- **Independent.** wait for a yes\n" if lang == "en"
                     else "- **Indipendente.** aspetta un sì\n")
            body = cost + indep
            errs = self.errors(lang, skill=skill, description=desc, body=body)
            heading = "Where you are running" if lang == "en" else "Dove stai lavorando"
            self.assertTrue(any(heading in e for e in errs), (lang, skill, errs))
            env = ENV_EN if lang == "en" else ENV_IT
            self.assertEqual(self.errors(lang, skill=skill, description=desc, body=body + env), [])

    def test_environment_heading_in_code_block_ignored(self):
        body = "```markdown\n## Where you are running\n```\n"
        errs = self.errors(skill="stress-test", description=STRESS,
                           body=body + "- **Independent.** wait for a yes\n")
        self.assertTrue(any("Where you are running" in e for e in errs), errs)

    def test_memory_section_required(self):
        cases = (
            ("en", "position-fix", "POSITION FIX, PUNTO NAVE, STOP, where are we, facciamo il punto",
             ENV_EN, "## Memory in chat", "brace-position-fix.md"),
            ("en", "decision", DECISION_EN, ENV_EN, "## Memory in chat", "brace-decisions.md"),
            ("en", "review", "REVIEW, was I right, avevo ragione",
             ENV_EN, "## Memory in chat", "brace-decisions.md"),
            ("it", "punto-nave", PF_IT, ENV_IT, "## Memoria in chat", "brace-punto-nave.md"),
            ("it", "decisione", "DECISIONE, ho deciso, I've decided",
             ENV_IT, "## Memoria in chat", "brace-decisioni.md"),
            ("it", "revisione", "REVISIONE, avevo ragione, was I right",
             ENV_IT, "## Memoria in chat", "brace-decisioni.md"),
        )
        for lang, skill, desc, env, heading, name in cases:
            # Missing section.
            errs = self.errors(lang, skill=skill, description=desc, body=env)
            self.assertTrue(any(heading[3:] in e for e in errs), (skill, errs))
            # Section present but without the file name; the name elsewhere does not count.
            body = env + "\n%s\n\nPaste it.\n\n## Other\n\n`%s`\n" % (heading, name)
            errs = self.errors(lang, skill=skill, description=desc, body=body)
            self.assertTrue(any(name in e for e in errs), (skill, errs))
            # Section with the file name passes.
            body = env + "\n%s\n\nAdd it as `%s`.\n" % (heading, name)
            self.assertEqual(self.errors(lang, skill=skill, description=desc, body=body), [])

    def test_memory_names_are_per_language(self):
        body = ENV_IT + "\n## Memoria in chat\n\nUsa `brace-decisions.md`.\n"
        errs = self.errors("it", skill="decisione",
                           description="DECISIONE, ho deciso, I've decided", body=body)
        self.assertTrue(any("brace-decisioni.md" in e for e in errs), errs)

    def test_real_plugins_pass(self):
        self.assertEqual(check_plugin(ROOT / "plugins" / "brace", "en"), [])
        self.assertEqual(check_plugin(ROOT / "plugins" / "brace-it", "it"), [])


if __name__ == "__main__":
    unittest.main()
