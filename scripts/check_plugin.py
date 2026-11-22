#!/usr/bin/env python3
"""Static checker for the BRACE plugins (Python stdlib only).

Usage: python3 scripts/check_plugin.py <plugin_root> <en|it>
Prints one error per line and exits 1 if there are any.
"""
import json
import re
import sys
from pathlib import Path

VERSION = "0.2.0"
DISPLAY_NAME = "BRACE"
PLUGIN_NAMES = {"en": "brace", "it": "brace-it"}
MAX_DESCRIPTION = 1024
MIGRATION_PATH = ".vanta/"
# Directories the checker does not scan (Task 7 removes "evals").
IGNORED_DIRS = {"evals"}

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


def check_plugin(root, lang):
    """Return a list of error strings for the plugin at root; empty means pass."""
    root = Path(root)
    errors = []
    for rule in (_rule_old_name, _rule_plugin_json, _rule_description_length,
                 _rule_triggers):
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
