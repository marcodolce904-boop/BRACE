#!/bin/sh
# BRACE (English) - SessionStart hook.
# If the working folder contains a BRACE state (.brace/, or the older .vanta/),
# it brings it into the session context: the latest Position Fix and the
# decisions due for review.
# If neither folder exists it prints nothing, so it uses no tokens.

base="${CLAUDE_PROJECT_DIR:-$PWD}"
if [ -d "$base/.brace" ]; then
  dir="$base/.brace"
elif [ -d "$base/.vanta" ]; then
  dir="$base/.vanta"
else
  exit 0
fi

# Resolve a state file: the plain name first, then the brace- prefixed name.
resolve() {
  if [ -f "$dir/$1" ]; then
    echo "$dir/$1"
  elif [ -f "$dir/brace-$1" ]; then
    echo "$dir/brace-$1"
  fi
}

pf=$(resolve position-fix.md)
log=$(resolve decisions.md)

if [ -n "$pf" ]; then
  echo "[BRACE] Latest Position Fix saved in this folder ($(basename "$dir")/$(basename "$pf")). Use it as context if the user resumes this work, checking with them that it is still valid:"
  echo
  head -c 4000 "$pf"
  echo
fi

if [ -n "$log" ]; then
  # BRACE_TODAY overrides the date; it exists for tests only.
  today="${BRACE_TODAY:-$(date +%Y-%m-%d)}"
  due=$(awk -v today="$today" '
    # Value of a field: the text after the first colon, spaces trimmed.
    function value(line) {
      sub(/^[^:]*:/, "", line)
      gsub(/^[ \t]+|[ \t]+$/, "", line)
      return line
    }
    function flush() {
      if (id != "" && status == "open" && rev != "" && rev <= today) {
        n++; ids = ids (ids == "" ? "" : ", ") id
      }
      id = ""; status = ""; rev = ""
    }
    { sub(/\r$/, "") }
    /^## / { flush(); id = $2; next }
    /^- Review:/ { rev = value($0); next }
    /^- Status:/ { status = value($0); next }
    END { flush(); if (n > 0) print n " (" ids ")" }
  ' "$log")
  if [ -n "$due" ]; then
    echo "[BRACE] Decisions with overdue review: $due. Remind the user once, at the start, and offer to review them; they can simply say \"let's review my decisions\"."
  fi
fi

exit 0
