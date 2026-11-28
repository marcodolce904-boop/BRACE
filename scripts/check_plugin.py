#!/usr/bin/env python3
"""Static checker for the BRACE plugins (Python stdlib only).

Usage: python3 scripts/check_plugin.py <plugin_root> <en|it>
Prints one error per line and exits 1 if there are any.
"""
import json
import re
import sys
from pathlib import Path

VERSION = "0.2.3"
DISPLAY_NAME = "BRACE"
PLUGIN_NAMES = {"en": "brace", "it": "brace-it"}
MAX_DESCRIPTION = 1024
MIGRATION_PATH = ".vanta/"
# Directories the checker does not scan.
IGNORED_DIRS = set()

# lang -> skill directory -> substrings its description must contain
# (case-insensitive). Skills absent from the plugin are not checked.
REQUIRED_TRIGGERS = {
    "en": {
        "method": ["BRACE", "not sure whether", "non so se", "is this a good idea"],
        "stress-test": ["STRESS TEST", "how could this go wrong", "come potrebbe andare storto"],
        "decision": ["DECISION", "I've decided", "ho deciso"],
        "review": ["REVIEW", "was I right", "avevo ragione"],
        "position-fix": ["POSITION FIX", "PUNTO NAVE", "STOP", "where are we", "facciamo il punto"],
        "wargame": ["WARGAME", "how would competitors react", "come reagirebbe"],
    },
    "it": {
        "metodo": ["BRACE", "non so se", "not sure whether", "è una buona idea"],
        "stress-test": ["STRESS TEST", "how could this go wrong", "come potrebbe andare storto"],
        "decisione": ["DECISIONE", "ho deciso", "I've decided"],
        "revisione": ["REVISIONE", "avevo ragione", "was I right"],
        "punto-nave": ["PUNTO NAVE", "STOP", "facciamo il punto", "where are we"],
        "wargame": ["WARGAME", "come reagirebbe", "how would competitors react"],
    },
}

# Pinned headings and phrases for routing and cost gates (Task 5).
METHOD_SKILL = {"en": "method", "it": "metodo"}
NEXT_TOOL_HEADING = {"en": "## Next tool", "it": "## Strumento successivo"}
COST_GATE_HEADING = {"en": "## Cost check", "it": "## Controllo del costo"}
INDEPENDENT_BULLET = {"en": "- **Independent.**", "it": "- **Indipendente.**"}
INDEPENDENT_WAIT = {"en": "wait for a yes", "it": "aspetta un sì"}
_COMMAND = re.compile(r"/brace(-it)?:")

# Levels and memory in chat (Task 6).
ENV_HEADING = {"en": "## Where you are running", "it": "## Dove stai lavorando"}
MEMORY_HEADING = {"en": "## Memory in chat", "it": "## Memoria in chat"}
ENV_SKILLS = {
    "en": ["stress-test", "wargame", "position-fix", "decision", "review"],
    "it": ["stress-test", "wargame", "punto-nave", "decisione", "revisione"],
}
# lang -> skill -> chat/Project file names its memory section must name.
MEMORY_FILES = {
    "en": {"position-fix": ["brace-position-fix.md"],
           "decision": ["brace-decisions.md"],
           "review": ["brace-decisions.md"]},
    "it": {"punto-nave": ["brace-punto-nave.md"],
           "decisione": ["brace-decisioni.md"],
           "revisione": ["brace-decisioni.md"]},
}

_OLD_NAME = re.compile(r"V\.A\.N\.T\.A\.|\bvanta\b", re.IGNORECASE)


def _split_frontmatter(text):
    """Return the frontmatter block of text, or None if absent."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i]
    return None


def _strip_quotes(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(path):
    """Parse top-level `key: value` scalars and inline lists from a file's frontmatter.

    Scalars are returned as strings with surrounding quotes stripped; inline
    lists (`[a, b]`) are returned as the raw string. Returns {} if there is
    no frontmatter.
    """
    block = _split_frontmatter(Path(path).read_text(encoding="utf-8"))
    result = {}
    for line in block or []:
        if not line.strip() or line[0] in " \t#" or ":" not in line:
            continue
        key, _, value = line.partition(":")
        result[key.strip()] = _strip_quotes(value)
    return result


def _scanned_files(root, suffixes):
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix not in suffixes:
            continue
        if IGNORED_DIRS & set(path.relative_to(root).parts[:-1]):
            continue
        yield path


def _rule_old_name(root, lang):
    errors = []
    for path in _scanned_files(root, {".md", ".json"}):
        text = path.read_text(encoding="utf-8").replace(MIGRATION_PATH, "")
        for n, line in enumerate(text.splitlines(), 1):
            m = _OLD_NAME.search(line)
            if m:
                errors.append("%s:%d: old name %r" % (path.relative_to(root), n, m.group(0)))
    return errors


def _rule_plugin_json(root, lang):
    path = root / ".claude-plugin" / "plugin.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return ["%s: cannot read plugin.json (%s)" % (path, exc)]
    errors = []
    for key, expected in (("name", PLUGIN_NAMES[lang]),
                          ("displayName", DISPLAY_NAME),
                          ("version", VERSION)):
        if data.get(key) != expected:
            errors.append("plugin.json: %s must be %r, found %r" % (key, expected, data.get(key)))
    return errors


def _rule_description_length(root, lang):
    errors = []
    for path in _scanned_files(root, {".md"}):
        description = parse_frontmatter(path).get("description")
        if description is not None and len(description) > MAX_DESCRIPTION:
            errors.append("%s: description is %d characters (max %d)"
                          % (path.relative_to(root), len(description), MAX_DESCRIPTION))
    return errors


def _rule_triggers(root, lang):
    errors = []
    for skill, phrases in REQUIRED_TRIGGERS[lang].items():
        path = root / "skills" / skill / "SKILL.md"
        if not path.is_file():
            continue
        description = parse_frontmatter(path).get("description", "").casefold()
        for phrase in phrases:
            if phrase.casefold() not in description:
                errors.append("skills/%s/SKILL.md: description of %s lacks trigger %r"
                              % (skill, skill, phrase))
    return errors


def _body_lines(path):
    """Return the lines of a file after its frontmatter."""
    lines = path.read_text(encoding="utf-8").splitlines()
    block = _split_frontmatter("\n".join(lines))
    return lines[len(block) + 2:] if block is not None else lines


def _rule_routing(root, lang):
    errors = []
    method = root / "skills" / METHOD_SKILL[lang] / "SKILL.md"
    if method.is_file():
        heading = NEXT_TOOL_HEADING[lang]
        if heading not in [line.rstrip() for line in _body_lines(method)]:
            errors.append("skills/%s/SKILL.md: missing section %r"
                          % (METHOD_SKILL[lang], heading))
    stress = root / "skills" / "stress-test" / "SKILL.md"
    if stress.is_file():
        bullets = [line for line in _body_lines(stress)
                   if line.startswith(INDEPENDENT_BULLET[lang])]
        if not any(INDEPENDENT_WAIT[lang] in line for line in bullets):
            errors.append("skills/stress-test/SKILL.md: %r mode bullet lacks %r"
                          % (INDEPENDENT_BULLET[lang], INDEPENDENT_WAIT[lang]))
    styles = root / "output-styles"
    if styles.is_dir():
        for path in sorted(styles.glob("*.md")):
            for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                m = _COMMAND.search(line)
                if m:
                    errors.append("%s:%d: output style names a command (%r)"
                                  % (path.relative_to(root), n, m.group(0)))
    return errors


def _rule_cost_gate(root, lang):
    path = root / "skills" / "wargame" / "SKILL.md"
    if not path.is_file():
        return []
    errors = []
    if "disable-model-invocation" in parse_frontmatter(path):
        errors.append("skills/wargame/SKILL.md: disable-model-invocation must be absent")
    headings = [line.rstrip() for line in _body_lines(path) if line.startswith("## ")]
    if not headings or headings[0] != COST_GATE_HEADING[lang]:
        errors.append("skills/wargame/SKILL.md: first ## heading must be %r, found %r"
                      % (COST_GATE_HEADING[lang], headings[0] if headings else None))
    return errors


def _sections(path):
    """Map each `## ` heading of a file's body to its text, ignoring fenced code."""
    sections, current, fenced = {}, None, False
    for line in _body_lines(path):
        if line.lstrip().startswith("```"):
            fenced = not fenced
        elif not fenced and line.startswith("#"):
            current = line.rstrip() if line.startswith("## ") else None
            if current is not None:
                sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line)
    return {heading: "\n".join(lines) for heading, lines in sections.items()}


def _rule_environment(root, lang):
    errors = []
    for skill in ENV_SKILLS[lang]:
        path = root / "skills" / skill / "SKILL.md"
        if not path.is_file():
            continue
        sections = _sections(path)
        if ENV_HEADING[lang] not in sections:
            errors.append("skills/%s/SKILL.md: missing section %r" % (skill, ENV_HEADING[lang]))
        names = MEMORY_FILES[lang].get(skill)
        if names is None:
            continue
        memory = sections.get(MEMORY_HEADING[lang])
        if memory is None:
            errors.append("skills/%s/SKILL.md: missing section %r"
                          % (skill, MEMORY_HEADING[lang]))
            continue
        for name in names:
            if name not in memory:
                errors.append("skills/%s/SKILL.md: section %r lacks file name %r"
                              % (skill, MEMORY_HEADING[lang], name))
    return errors


# Eval cases (Task 7). Routing prompts must be natural language: no skill
# keyword (ALL-CAPS, case-sensitive: lowercase "decision" is ordinary prose)
# and no slash command (a token starting with "/" plus a letter, so "and/or",
# "3/4" and URLs are not flagged). `route-punto-nave` tests the keyword itself.
ROUTE_KEYWORD_EXEMPT = {"route-punto-nave"}
_ROUTE_KEYWORDS = sorted({"BRACE"} | {p for skills in REQUIRED_TRIGGERS.values()
                                      for phrases in skills.values()
                                      for p in phrases if p.isupper()})
_KEYWORD = re.compile(r"\b(%s)\b" % "|".join(re.escape(k) for k in _ROUTE_KEYWORDS))
_SLASH_COMMAND = re.compile(r"(?:^|[\s(\"'`])/[A-Za-z]")


def _rule_evals(root, lang):
    evals = root / "evals"
    if not evals.is_dir():
        return []
    errors = []
    for case in sorted(p for p in evals.iterdir() if p.is_dir()):
        prompt = case / "prompt.md"
        for required in (prompt, case / "graders" / "criteria.md"):
            if not required.is_file():
                errors.append("evals/%s: missing %s"
                              % (case.name, required.relative_to(case)))
        if (not case.name.startswith("route-") or case.name in ROUTE_KEYWORD_EXEMPT
                or not prompt.is_file()):
            continue
        for n, line in enumerate(_body_lines(prompt), 1):
            m = _KEYWORD.search(line)
            if m:
                errors.append("evals/%s/prompt.md: routing prompt contains keyword %r (line %d)"
                              % (case.name, m.group(0), n))
            m = _SLASH_COMMAND.search(line)
            if m:
                errors.append("evals/%s/prompt.md: routing prompt contains slash command %r (line %d)"
                              % (case.name, m.group(0).strip(), n))
    return errors


def check_plugin(root, lang):
    """Return a list of error strings for the plugin at root; empty means pass."""
    root = Path(root)
    errors = []
    for rule in (_rule_old_name, _rule_plugin_json, _rule_description_length,
                 _rule_triggers, _rule_routing, _rule_cost_gate, _rule_environment,
                 _rule_evals):
        errors.extend(rule(root, lang))
    return errors


def main(argv):
    if len(argv) != 3 or argv[2] not in PLUGIN_NAMES:
        print("usage: check_plugin.py <plugin_root> <en|it>", file=sys.stderr)
        return 2
    errors = check_plugin(Path(argv[1]), argv[2])
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
