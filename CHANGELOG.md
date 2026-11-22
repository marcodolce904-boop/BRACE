# Changelog

## 0.2.0 · unreleased

### English

V.A.N.T.A. is now BRACE.

- **Rename (breaking).** Plugin ids: `vanta-en` is now `brace`, `vanta` is now `brace-it`; the marketplace is `brace`. Commands change accordingly (`/brace:method`, `/brace-it:metodo`, ...); skill and agent names are unchanged. The output style is now `BRACE`.
- **State folder.** `.vanta/` is now `.brace/`. `.vanta/` is still read, and the first state write renames it to `.brace/` and says so in one line.
- **Natural-language activation.** Skill descriptions are rewritten around what people actually say, in English and Italian; keywords remain as extra triggers. `method` is the entry point and proposes the next tool when it adds value. Routine technical questions are not routed to it. `PUNTO NAVE` and `STOP` work as before; the English plugin also accepts `POSITION FIX`.
- **Wargame unlocked, with a cost gate.** The model can now start `wargame` by itself, but the agent mode states its cost and waits for a yes; the independent stress test does the same when it was not explicitly requested.
- **Three levels.** Each skill detects what the environment supports: sub-agents or an in-conversation fallback (stated in one line), a project folder or Project memory.
- **Project memory in chat.** Where there is no folder, `position-fix`, `decision` and `review` give the full updated file to add to a Claude Project as `brace-position-fix.md` / `brace-decisions.md` (Italian: `brace-punto-nave.md` / `brace-decisioni.md`), and read it back from the Project knowledge.
- **Hook fallback.** If the startup hook did not run, skills look for the BRACE files themselves.
- **Checkers and CI.** `scripts/check_plugin.py`, `scripts/check_parity.py`, unit tests, `tests/test_hooks.sh` and a GitHub Actions workflow.
- **Routing evals.** Eight new `route-*` cases per plugin (14 in total), including a negative case for routine code questions.
- **Docs.** New README with chat and Claude Code install, levels table and migration notes; the section on the name clash is removed.

### Italiano

V.A.N.T.A. diventa BRACE.

- **Nuovo nome (non retrocompatibile).** Id dei plugin: `vanta-en` diventa `brace`, `vanta` diventa `brace-it`; il marketplace è `brace`. I comandi cambiano di conseguenza (`/brace:method`, `/brace-it:metodo`, ...); i nomi di skill e agenti non cambiano. Lo stile di output è ora `BRACE`.
- **Cartella di stato.** `.vanta/` diventa `.brace/`. `.vanta/` viene ancora letta e la prima scrittura dello stato la rinomina in `.brace/` dicendolo in una riga.
- **Attivazione in linguaggio naturale.** Le descrizioni delle skill sono riscritte attorno a ciò che le persone dicono davvero, in italiano e in inglese; le parole chiave restano come attivatori aggiuntivi. `metodo` è il punto d'ingresso e propone lo strumento successivo quando serve. Le domande tecniche di routine non vi entrano. `PUNTO NAVE` e `STOP` funzionano come prima; il plugin inglese accetta anche `POSITION FIX`.
- **Wargame sbloccato, con controllo dei costi.** Il modello può ora avviare `wargame` da solo, ma la modalità con agenti dichiara il costo e aspetta un sì; lo stress test indipendente fa lo stesso se non è stato richiesto esplicitamente.
- **Tre livelli.** Ogni skill rileva cosa supporta l'ambiente: sub-agenti o ripiego nella conversazione (dichiarato in una riga), cartella di progetto o memoria del Progetto.
- **Memoria del Progetto in chat.** Dove non c'è una cartella, `punto-nave`, `decisione` e `revisione` danno il file completo aggiornato da aggiungere a un Progetto di Claude come `brace-punto-nave.md` / `brace-decisioni.md` (inglese: `brace-position-fix.md` / `brace-decisions.md`) e lo rileggono dalla knowledge del Progetto.
- **Ripiego dell'hook.** Se l'hook di avvio non è girato, le skill cercano da sole i file BRACE.
- **Controlli e CI.** `scripts/check_plugin.py`, `scripts/check_parity.py`, test unitari, `tests/test_hooks.sh` e un workflow GitHub Actions.
- **Eval di instradamento.** Otto nuovi casi `route-*` per plugin (14 in totale), incluso un caso negativo per le domande di codice di routine.
- **Documentazione.** Nuovo README con installazione in chat e in Claude Code, tabella dei livelli e note di migrazione; rimossa la sezione sul conflitto di nome.

## 0.1.0 · 2026-10-05

Prima versione pubblica · First public release.

- Skill: `metodo`, `punto-nave`, `stress-test`, `wargame`, `decisione`, `revisione`.
- Agenti: `nemesi` (Opus), `rosso` e `blu` (Sonnet).
- Stile di output `V.A.N.T.A.`, attivabile da `/config`.
- Hook di avvio che ricarica il Punto Nave e segnala le decisioni con revisione scaduta.
- Sei casi di prova in `evals/`.
- Versione inglese `vanta-en` (`method`, `position-fix`, `stress-test`, `wargame`, `decision`, `review`; agenti `nemesis`, `red`, `blue`), con README in inglese.
- Repository organizzato come marketplace con le due versioni in `plugins/`.
