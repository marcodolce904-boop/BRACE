# BRACE

**Bias · Risks · Assumptions · Confidence · Evidence**

**Italiano** · [English](README.md)

BRACE è un plugin per Claude che lo trasforma in un consulente analitico per decisioni: controlla le premesse, cerca l'obiezione più forte, dichiara la confidenza, mette sotto stress i piani e tiene traccia di ciò che hai deciso per confrontarlo, più avanti, con ciò che è successo davvero. Funziona in chat (claude.ai, app desktop), in Cowork e in Claude Code.

Questo repository è un marketplace di plugin con due versioni dello stesso plugin, con contenuti equivalenti:

| Versione | Cartella | Id del plugin | Skill |
|---|---|---|---|
| Italiano | [`plugins/brace-it`](plugins/brace-it) | `brace-it` | `metodo`, `punto-nave`, `stress-test`, `wargame`, `decisione`, `revisione` |
| English | [`plugins/brace`](plugins/brace) | `brace` | `method`, `position-fix`, `stress-test`, `wargame`, `decision`, `review` |

Installane **una sola**: entrambe hanno un hook di avvio e usano la stessa cartella `.brace/`, quindi installate insieme farebbero il lavoro due volte.

> Stato: versione 0.2.0, sperimentale. Il metodo segue le raccomandazioni attuali di Anthropic sul prompting e la letteratura su persona, brevità e autocorrezione, ma non è ancora stato misurato sul campo. La sezione [Verificare che funzioni](#verificare-che-funzioni) spiega come farlo.

## Installazione in chat

Per claude.ai e l'app desktop di Claude:

1. Apri **Customize → Plugins**.
2. Aggiungi il marketplace da GitHub: `marcodolce904-boop/V.A.N.T.A.`
3. Installa `brace-it` (italiano) o `brace` (inglese).

I passaggi possono cambiare: quelli aggiornati sono nell'articolo ufficiale [Manage plugins, skills and connectors from one Plugins page](https://support.claude.com/en/articles/17740565-manage-plugins-skills-and-connectors-from-one-plugins-page).

In chat sub-agenti e hook non girano, quindi il critico indipendente e il wargame si svolgono dentro la conversazione (e lo dicono), e la memoria sta in un Progetto di Claude: vedi [Memoria in chat](#memoria-in-chat).

## Installazione in Claude Code

```
/plugin marketplace add marcodolce904-boop/V.A.N.T.A.
/plugin install brace-it@brace
```

Per la versione inglese, al secondo comando usa `/plugin install brace@brace`. Ricorda: installane una sola.

Per provarlo in locale, o per verificare la struttura prima di pubblicare:

```bash
claude --plugin-dir ./plugins/brace-it
claude plugin validate ./plugins/brace-it
```

## Parlaci e basta

Non servono comandi. Descrivi ciò che ti serve: parte la skill giusta, oppure viene proposta quando costa di più. Per esempio:

- "Non so se accettare questa offerta." (parte `metodo`)
- "Come potrebbe andare storto? Trova i punti deboli di questo piano." (parte `stress-test`)
- "Ho deciso: vado con la seconda opzione, segnatelo." (parte `decisione`)
- "Facciamo il punto: a che siamo?" (parte `punto-nave`)
- "Come reagirebbero i concorrenti se abbassassimo il prezzo?" (propone `wargame`, dopo un controllo dei costi)

L'inglese funziona in entrambi i plugin, qualunque tu abbia installato. Le parole chiave restano come attivatori aggiuntivi: `BRACE`, `PUNTO NAVE` (o `STOP`), `STRESS TEST`, `WARGAME`, `DECISIONE`, `REVISIONE`. Sono disponibili anche i comandi slash (`/brace-it:metodo`, `/brace-it:punto-nave`, `/brace-it:stress-test`, `/brace-it:wargame`, `/brace-it:decisione`, `/brace-it:revisione`).

Le domande tecniche di routine ("libreria X o Y?", "questo codice va bene?") ricevono una risposta normale: il metodo serve per decisioni, piani e scelte difficili da disfare.

## Cosa contiene

| Componente | A cosa serve |
|---|---|
| Skill `metodo` | Analisi critica con priorità esplicite (accuratezza > utilità > forma), checklist di ragionamento, confidenza Alta/Media/Bassa. È il punto d'ingresso e propone lo strumento successivo quando serve |
| Skill `punto-nave` | Fotografia dello stato del lavoro, salvata in `.brace/punto-nave.md` |
| Skill `stress-test` | Pre-mortem: cinque cause di fallimento con segnali precoci e contromisure; modalità indipendente con un critico separato |
| Skill `wargame` | Simulazione Rosso contro Blu con sintesi finale; chiede un sì prima della modalità costosa con agenti |
| Skill `decisione` | Registro decisioni con previsione verificabile e data di revisione |
| Skill `revisione` | Confronto tra previsioni ed esiti, con calibrazione per livello di confidenza |
| Agente `nemesi` (Opus) | Critico indipendente a contesto pulito |
| Agenti `rosso` e `blu` (Sonnet) | Avversario e difensore nel wargame |
| Stile di output `BRACE` | Il tono asciutto e le priorità del metodo in ogni risposta, attivabile a scelta: `/config` → Output style |
| Hook di avvio | Ricarica l'ultimo Punto Nave e ricorda le decisioni da rivedere |

## Tre livelli, un solo plugin

Ogni skill rileva ciò che l'ambiente sa fare e usa il percorso più ricco disponibile. Quando ripiega su un'alternativa, te lo dice in una riga.

| | Chat (web, app) | Cowork | Claude Code |
|---|---|---|---|
| Metodo, stress test, decisione, revisione | sì | sì | sì |
| Critico indipendente | nella conversazione, dichiarato | agente | agente |
| Wargame | rapido, dichiarato | agenti | agenti |
| Memoria | knowledge del Progetto | `.brace/` | `.brace/` |
| Ripresa automatica e promemoria revisioni | no | sì | sì |
| Stile di output, comandi slash | solo slash | solo slash | entrambi |

## Memoria in chat

La chat non ha una cartella di progetto, quindi BRACE tiene la memoria in un Progetto di Claude:

1. Crea un Progetto (o aprine uno esistente) e lavora al suo interno.
2. Quando `punto-nave`, `decisione` o `revisione` producono qualcosa da conservare, BRACE mostra il risultato e poi il **file completo aggiornato** in un unico blocco di codice, con un'istruzione di una riga.
3. Aggiungi quel contenuto alla knowledge del Progetto, o sostituisci il file esistente, come `brace-punto-nave.md` (inglese: `brace-position-fix.md`) e `brace-decisioni.md` (inglese: `brace-decisions.md`). Il file viene sempre dato per intero, così sostituisci un solo file invece di unire frammenti.
4. Nelle chat successive dello stesso Progetto, BRACE cerca quei file, li usa e conferma con te che il Punto Nave sia ancora valido. `revisione` legge da lì il registro decisioni e calcola la calibrazione contando dal file.

Fuori da un Progetto, BRACE dice una volta che la memoria dura solo per quella chat e mostra comunque il contenuto, così puoi conservarlo. I file hanno lo stesso formato di `.brace/`: puoi spostarli in una cartella più avanti e Claude Code li riprende. La funzione di memoria di Claude non viene usata, perché il suo formato non è controllabile e la calibrazione diventerebbe inaffidabile.

### File creati nel progetto (Claude Code, Cowork)

```
.brace/
├── punto-nave.md          stato corrente
├── punto-nave-storico.md  versioni precedenti
└── decisioni.md           registro decisioni
```

Nella versione inglese i file si chiamano `position-fix.md`, `position-fix-history.md` e `decisions.md`. Se il registro contiene informazioni personali o riservate, aggiungi `.brace/` al `.gitignore` del progetto.

## Aggiornare da V.A.N.T.A.

BRACE 0.2.0 è il nuovo nome di V.A.N.T.A. 0.1.0. I cambi di nome non sono retrocompatibili:

- Id dei plugin: `vanta-en` diventa `brace`, `vanta` diventa `brace-it`; il marketplace è `brace`. Disinstalla il vecchio plugin e installa il nuovo (`/plugin install brace-it@brace`), uno solo dei due.
- Comandi: `/vanta:metodo` diventa `/brace-it:metodo`, e così le altre skill; l'inglese `/vanta-en:method` diventa `/brace:method`. I nomi di skill e agenti non cambiano.
- Stile di output: `V.A.N.T.A.` diventa `BRACE` (`"outputStyle": "brace-it:BRACE"`).
- Cartella di stato: `.vanta/` diventa `.brace/`. Non devi spostare nulla: BRACE legge `.vanta/` se `.brace/` non esiste e, alla prima scrittura dello stato, rinomina `.vanta/` in `.brace/` e te lo dice in una riga. Se avevi messo `.vanta/` nel `.gitignore`, aggiungi anche `.brace/`.
- Per ora il repository mantiene il suo indirizzo GitHub, quindi le righe di installazione qui sopra usano ancora `marcodolce904-boop/V.A.N.T.A.`.

## Costi indicativi

| Azione | Costo rispetto a una risposta normale |
|---|---|
| Metodo, Punto Nave, decisione, revisione | circa 1x |
| Stress test standard | circa 1x |
| Stress test indipendente | circa 2-3x (una chiamata Opus in più) |
| Wargame rapido | circa 1-2x |
| Wargame con agenti | circa 3-6x |

Sono stime da verificare con l'uso: `/cost` in Claude Code mostra il consumo reale della sessione. Lo stress test indipendente e il wargame con agenti aspettano sempre il tuo sì.

## Scelte di progetto

Il plugin nasce dalla revisione di un prompt di sistema più lungo. Cosa è cambiato e perché:

- **Niente identità decorativa.** Le persona nel prompt non migliorano l'accuratezza dei modelli (Zheng et al., 2024; Wharton Generative AI Labs, 2025). Restano le regole operative.
- **Moduli trasformati in checklist.** Nomi come Sophia, Nemesi e Kairos sono diventati domande di controllo concrete.
- **Brevità subordinata all'accuratezza.** Le istruzioni di concisione aumentano le risposte errate quando la domanda contiene una premessa falsa (Giskard, benchmark Phare, 2025).
- **Confidenza a livelli, non in percentuale.** Le percentuali verbalizzate dai modelli sono sistematicamente sovrastimate (Xiong et al., ICLR 2024).
- **Critica separata dall'autore.** Senza un segnale esterno l'autocorrezione è poco affidabile (Huang et al., ICLR 2024): da qui l'agente `nemesi` a contesto pulito.
- **Multi-agente solo su richiesta.** I sistemi multi-agente consumano molti più token di una chat (Anthropic, *How we built our multi-agent research system*, 2025) e il dibattito tra agenti non batte in modo affidabile metodi più semplici: per questo è riservato al wargame, dove serve un vero punto di vista avversario, e aspetta il tuo sì.
- **Pre-mortem.** La tecnica di Gary Klein si basa sulla ricerca sulla "prospective hindsight" (Mitchell, Russo e Pennington, 1989). L'evidenza riguarda il numero di cause individuate più che la loro qualità.

## Verificare che funzioni

Ogni versione contiene 14 casi di prova in `evals/`: sei sul metodo (premessa falsa, obiezione forzata, utente sotto pressione, dati sconosciuti, insistenza senza argomenti, Punto Nave) e otto casi `route-*` che verificano l'instradamento in linguaggio naturale (parte o viene proposta la skill giusta, una richiesta vaga entra in `metodo`, una domanda di codice di routine no). Si eseguono con:

```bash
claude plugin eval ./plugins/brace-it
```

Il comando confronta le risposte con e senza il plugin e assegna un punteggio con un modello giudice. Ogni caso viene eseguito più volte, quindi consuma crediti: per un primo giro usa `--runs 1`, oppure scegli un solo caso con `--case premessa-falsa`.

Il repository ha anche controlli strutturali che non consumano crediti e girano in CI (`.github/workflows/ci.yml`):

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_plugin.py plugins/brace en
python3 scripts/check_plugin.py plugins/brace-it it
python3 scripts/check_parity.py
sh tests/test_hooks.sh
```

## Struttura del repository

```
.claude-plugin/marketplace.json   elenca le due versioni
plugins/
├── brace-it/   versione italiana
└── brace/      versione inglese
scripts/        controlli (check_plugin.py, check_parity.py)
tests/          test unitari e degli hook
```

## Licenza

MIT. Vedi [LICENSE](LICENSE).
