#!/bin/bash
# Windows checks for the BRACE startup hook. Run in CI under Git Bash:
#   bash tests/test_hooks_windows.sh
# It reproduces what Claude Code does on Windows: it takes the command string
# from hooks.json, puts a Windows-style path (backslashes, a space) in place of
# ${CLAUDE_PLUGIN_ROOT}, and runs it through Git Bash with a Windows-style
# CLAUDE_PROJECT_DIR. It also checks that the scripts have LF line endings
# after a Windows checkout (core.autocrlf), since a CR breaks sh.

set -u
root=$(cd "$(dirname "$0")/.." && pwd)
failures=0

check() { # check <name> <condition-result: 0 ok>
  if [ "$2" -eq 0 ]; then echo "PASS $1"; else echo "FAIL $1"; failures=$((failures + 1)); fi
}

cr=$(printf '\r')
for p in brace brace-it; do
  ! grep -q "$cr" "$root/plugins/$p/scripts/session-start.sh"
  check "$p lf_line_endings" $?
done

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
proj="$tmp/My Project"
mkdir -p "$proj/.brace"
printf 'FIRSTLINE-WIN\n' > "$proj/.brace/position-fix.md"
printf 'FIRSTLINE-WIN\n' > "$proj/.brace/punto-nave.md"
printf '# Decision log\n\n## D-20261101-01 · t\n- Review: 2026-11-03\n- Status: open\n' > "$proj/.brace/decisions.md"
printf '# Registro decisioni\n\n## D-20261101-01 · t\n- Revisione: 2026-11-03\n- Stato: aperta\n' > "$proj/.brace/decisioni.md"

if command -v cygpath >/dev/null 2>&1; then
  winproj=$(cygpath -w "$proj")
else
  winproj="$proj" # not on Windows: the test still runs, with POSIX paths
fi

for p in brace brace-it; do
  if command -v cygpath >/dev/null 2>&1; then
    winroot=$(cygpath -w "$root/plugins/$p")
  else
    winroot="$root/plugins/$p"
  fi
  # The command string exactly as written in hooks.json, JSON escapes removed.
  cmd=$(grep '"command":' "$root/plugins/$p/hooks/hooks.json" \
    | sed 's/.*"command": "//; s/",\{0,1\}$//; s/\\"/"/g')
  # shellcheck disable=SC2016 # the literal placeholder text, not an expansion
  placeholder='${CLAUDE_PLUGIN_ROOT}'
  cmd=${cmd//"$placeholder"/$winroot}
  out=$(cd "$tmp" && CLAUDE_PROJECT_DIR="$winproj" BRACE_TODAY=2026-12-01 bash -c "$cmd" 2>&1)
  echo "$out" | grep -qF '[BRACE]' && echo "$out" | grep -qF 'FIRSTLINE-WIN'
  check "$p windows_path_position_fix" $?
  echo "$out" | grep -qF 'D-20261101-01'
  check "$p windows_path_due_review" $?
done

if [ "$failures" -gt 0 ]; then
  echo "$failures check(s) failed"
  exit 1
fi
echo "all Windows hook checks passed"
