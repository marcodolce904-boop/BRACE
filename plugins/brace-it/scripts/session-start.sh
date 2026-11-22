#!/bin/sh
# BRACE - SessionStart hook.
# Se la cartella di lavoro contiene uno stato BRACE (.brace/, o la vecchia
# .vanta/), lo porta nel contesto della sessione: l'ultimo Punto Nave e le
# decisioni da rivedere.
# Se nessuna delle due cartelle esiste non stampa nulla, quindi non consuma token.

base="${CLAUDE_PROJECT_DIR:-$PWD}"
if [ -d "$base/.brace" ]; then
  dir="$base/.brace"
elif [ -d "$base/.vanta" ]; then
  dir="$base/.vanta"
else
  exit 0
fi

# Risolve un file di stato: prima il nome semplice, poi quello con prefisso brace-.
resolve() {
  if [ -f "$dir/$1" ]; then
    echo "$dir/$1"
  elif [ -f "$dir/brace-$1" ]; then
    echo "$dir/brace-$1"
  fi
}

pn=$(resolve punto-nave.md)
reg=$(resolve decisioni.md)

if [ -n "$pn" ]; then
  echo "[BRACE] Ultimo Punto Nave salvato in questa cartella ($(basename "$dir")/$(basename "$pn")). Usalo come contesto se l'utente riprende questo lavoro, verificando con lui che sia ancora valido:"
  echo
  head -c 4000 "$pn"
  echo
fi

if [ -n "$reg" ]; then
  # BRACE_TODAY sostituisce la data; esiste solo per i test.
  today="${BRACE_TODAY:-$(date +%Y-%m-%d)}"
  due=$(awk -v today="$today" '
    # Valore di un campo: il testo dopo il primo due punti, senza spazi ai bordi.
    function value(line) {
      sub(/^[^:]*:/, "", line)
      gsub(/^[ \t]+|[ \t]+$/, "", line)
      return line
    }
    function flush() {
      if (id != "" && stato == "aperta" && rev != "" && rev <= today) {
        n++; ids = ids (ids == "" ? "" : ", ") id
      }
      id = ""; stato = ""; rev = ""
    }
    { sub(/\r$/, "") }
    /^## / { flush(); id = $2; next }
    /^- Revisione:/ { rev = value($0); next }
    /^- Stato:/ { stato = value($0); next }
    END { flush(); if (n > 0) print n " (" ids ")" }
  ' "$reg")
  if [ -n "$due" ]; then
    echo "[BRACE] Decisioni con revisione scaduta: $due. Ricordalo all'utente una sola volta, all'inizio, e proponi di rivederle; può dire semplicemente \"rivediamo le decisioni\"."
  fi
fi

exit 0
