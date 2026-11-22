#!/usr/bin/env python3
"""EN/IT parity checker for the BRACE plugins (Python stdlib only).

Usage: python3 scripts/check_parity.py
Compares plugins/brace with plugins/brace-it and CHANGELOG.md.
Prints one error per line and exits 1 if there are any.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_plugin import parse_frontmatter  # noqa: E402

# Path segments (joined by "/") rewritten in each EN relative path to get its IT path.
EN_TO_IT = {
    "skills/method": "skills/metodo",
    "skills/position-fix": "skills/punto-nave",
    "skills/decision": "skills/decisione",
    "skills/review": "skills/revisione",
    "references/biases.md": "references/bias.md",
    "agents/nemesis.md": "agents/nemesi.md",
    "agents/red.md": "agents/rosso.md",
    "agents/blue.md": "agents/blu.md",
    "evals/false-premise": "evals/premessa-falsa",
    "evals/forced-objection": "evals/obiezione-forzata",
    "evals/insistence-without-arguments": "evals/insistenza-senza-argomenti",
    "evals/position-fix": "evals/punto-nave",
    "evals/unknown-data": "evals/dati-sconosciuti",
    "evals/user-under-pressure": "evals/utente-sotto-pressione",
}

# Frontmatter keys whose values must be identical in EN and IT.
STRICT_KEYS = {
    "model", "tools", "disable-model-invocation", "keep-coding-instructions",
    "max_turns", "allowed_tools", "type", "weight",
}
SKIPPED_PREFIX = ("evals", "results")
_HEADING = re.compile(r"^#{1,2}\s")


def map_path(rel):
    """Map an EN relative path (posix string) to its IT relative path."""
    parts = rel.split("/")
    keys = [(tuple(k.split("/")), tuple(v.split("/"))) for k, v in EN_TO_IT.items()]
    out, i = [], 0
    while i < len(parts):
        for src, dst in keys:
            if tuple(parts[i:i + len(src)]) == src:
                out.extend(dst)
                i += len(src)
                break
        else:
            out.append(parts[i])
            i += 1
    return "/".join(out)


def _files(root):
    found = set()
    for path in root.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        rel = path.relative_to(root)
        if rel.parts[:2] == SKIPPED_PREFIX:
            continue
        found.add(rel.as_posix())
    return found


def count_headings(path):
    """Count `#` and `##` headings outside frontmatter and fenced code."""
    lines = path.read_text(encoding="utf-8").splitlines()
    start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                start = i + 1
                break
    count, fence = 0, None
    for line in lines[start:]:
        stripped = line.lstrip()
        if fence:
            if stripped.startswith(fence):
                fence = None
        elif stripped.startswith("```") or stripped.startswith("~~~"):
            fence = stripped[:3]
        elif _HEADING.match(line):
            count += 1
    return count


def _version(root):
    try:
        data = json.loads((root / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data.get("version")


def check_parity(en_root, it_root, changelog):
    en_root, it_root, changelog = Path(en_root), Path(it_root), Path(changelog)
    errors = []
    en_files, it_files = _files(en_root), _files(it_root)
    mapped = {map_path(rel): rel for rel in en_files}

    for rel in sorted(en_files):
        it_rel = map_path(rel)
        if it_rel not in it_files:
            errors.append(f"missing IT file for {rel}: expected {it_rel}")
    for rel in sorted(it_files):
        if rel not in mapped:
            errors.append(f"IT file {rel} has no EN source")

    for it_rel in sorted(it_files & set(mapped)):
        en_rel = mapped[it_rel]
        if not en_rel.endswith(".md"):
            continue
        en_path, it_path = en_root / en_rel, it_root / it_rel
        en_n, it_n = count_headings(en_path), count_headings(it_path)
        if en_n != it_n:
            errors.append(f"{en_rel} vs {it_rel}: heading count {en_n} != {it_n}")
        en_fm, it_fm = parse_frontmatter(en_path), parse_frontmatter(it_path)
        if set(en_fm) != set(it_fm):
            diff = sorted(set(en_fm) ^ set(it_fm))
            errors.append(f"{en_rel} vs {it_rel}: frontmatter keys differ ({', '.join(diff)})")
        for key in sorted(STRICT_KEYS & set(en_fm) & set(it_fm)):
            if en_fm[key] != it_fm[key]:
                errors.append(f"{en_rel} vs {it_rel}: frontmatter '{key}' differs "
                              f"({en_fm[key]!r} != {it_fm[key]!r})")

    en_v, it_v = _version(en_root), _version(it_root)
    if en_v != it_v:
        errors.append(f"plugin.json version mismatch: EN {en_v!r} != IT {it_v!r}")
    if en_v:
        prefix = f"## {en_v}"
        try:
            lines = changelog.read_text(encoding="utf-8").splitlines()
        except OSError:
            lines = []
        if not any(line.startswith(prefix) for line in lines):
            errors.append(f"CHANGELOG.md has no line starting '{prefix}'")
    return errors


def main():
    root = Path(__file__).resolve().parent.parent
    errors = check_parity(root / "plugins/brace", root / "plugins/brace-it",
                          root / "CHANGELOG.md")
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
