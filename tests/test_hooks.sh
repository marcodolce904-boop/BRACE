#!/bin/sh
# Tests for the SessionStart hooks of both plugins (POSIX sh).
# Run from the repository root: sh tests/test_hooks.sh

root=$(cd "$(dirname "$0")/.." && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
fail=0

BRACE_TODAY=2026-12-01
export BRACE_TODAY

ok() { echo "PASS $1"; }
bad() { echo "FAIL $1"; fail=1; }

# run_hook <script> <project dir>
run_hook() {
  CLAUDE_PROJECT_DIR="$2" sh "$1"
}

# entry <id> <review date> <status> <review field> <status field>
entry() {
  printf '## %s · Title\n- Date: 2026-10-01\n%s%s: %s%s\n%s%s: %s%s\n\n' \
    "$1" "- " "$4" "$2" "" "- " "$5" "$3" ""
}

run_suite() {
  lang=$1 script=$2 pf=$3 dec=$4 rf=$5 sf=$6 open=$7 closed=$8

  # empty_dir_silent
  d="$tmp/$lang-empty"; mkdir -p "$d"
  out=$(run_hook "$script" "$d")
  if [ -z "$out" ]; then ok "$lang empty_dir_silent"; else bad "$lang empty_dir_silent"; fi

  # brace_position_fix
  d="$tmp/$lang-bpf"; mkdir -p "$d/.brace"
  printf 'FIRSTLINE-BRACE\nsecond\n' > "$d/.brace/$pf"
  out=$(run_hook "$script" "$d")
  if echo "$out" | grep -q '\[BRACE\]' && echo "$out" | grep -q 'FIRSTLINE-BRACE'; then ok "$lang brace_position_fix"; else bad "$lang brace_position_fix"; fi

  # vanta_fallback
  d="$tmp/$lang-vf"; mkdir -p "$d/.vanta"
  printf 'FIRSTLINE-VANTA\nsecond\n' > "$d/.vanta/$pf"
  out=$(run_hook "$script" "$d")
  if echo "$out" | grep -q '\[BRACE\]' && echo "$out" | grep -q 'FIRSTLINE-VANTA'; then ok "$lang vanta_fallback"; else bad "$lang vanta_fallback"; fi

  # brace_wins
  d="$tmp/$lang-bw"; mkdir -p "$d/.brace" "$d/.vanta"
  printf 'FROM-BRACE\n' > "$d/.brace/$pf"
  printf 'FROM-VANTA\n' > "$d/.vanta/$pf"
  out=$(run_hook "$script" "$d")
  if [ "$(echo "$out" | grep -c 'FROM-BRACE')" -eq 1 ] && ! echo "$out" | grep -q 'FROM-VANTA'; then ok "$lang brace_wins"; else bad "$lang brace_wins"; fi

  # prefixed_names
  d="$tmp/$lang-pre"; mkdir -p "$d/.brace"
  entry D-20261004-01 2026-11-03 "$open" "$rf" "$sf" > "$d/.brace/brace-$dec"
  printf 'PREFIXED-PF\n' > "$d/.brace/brace-$pf"
  out=$(run_hook "$script" "$d")
  if echo "$out" | grep -q 'D-20261004-01' && echo "$out" | grep -q 'PREFIXED-PF'; then ok "$lang prefixed_names"; else bad "$lang prefixed_names"; fi

  # due_detection
  d="$tmp/$lang-due"; mkdir -p "$d/.brace"
  {
    entry D-20261004-01 2026-11-03 "$open" "$rf" "$sf"
    entry D-20261005-02 2027-01-01 "$open" "$rf" "$sf"
    entry D-20261006-03 2026-11-03 "$closed" "$rf" "$sf"
  } > "$d/.brace/$dec"
  out=$(run_hook "$script" "$d")
  if echo "$out" | grep -q '1 (D-20261004-01)'; then ok "$lang due_detection"; else bad "$lang due_detection"; fi

  # messy_log: double spaces after the colon and CRLF line endings
  d="$tmp/$lang-messy"; mkdir -p "$d/.brace"
  printf '## D-20261004-01 · Title\r\n- %s:   2026-11-03  \r\n- %s:   %s  \r\n' \
    "$rf" "$sf" "$open" > "$d/.brace/$dec"
  out=$(run_hook "$script" "$d")
  if echo "$out" | grep -q '1 (D-20261004-01)'; then ok "$lang messy_log"; else bad "$lang messy_log"; fi
}

run_suite en "$root/plugins/brace/scripts/session-start.sh" \
  position-fix.md decisions.md Review Status open closed
run_suite it "$root/plugins/brace-it/scripts/session-start.sh" \
  punto-nave.md decisioni.md Revisione Stato aperta chiusa

exit $fail
