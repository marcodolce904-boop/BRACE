---
name: punto-nave
description: "Fotografia dello stato del lavoro (obiettivo, vincoli, variabili, decisioni, questioni aperte, prossima azione) salvata su file e ricaricata nelle sessioni successive. Usala quando l'utente scrive PUNTO NAVE o STOP, quando vuole fare il punto della situazione o fermare il lavoro, oppure quando una conversazione lunga ha cambiato direzione più volte: 'facciamo il punto', 'riassumi dove siamo', 'riprendiamo domani', 'where are we?', 'sum up where we stand'. Parole chiave: PUNTO NAVE, STOP."
argument-hint: "[focus opzionale]"
---

# Punto Nave

Produci una fotografia dello stato del lavoro in questa conversazione. Se l'utente ha indicato un focus ($ARGUMENTS), limita il Punto Nave a quel tema.

## Dove stai lavorando

Verifica cosa puoi fare qui, non in quale prodotto ti trovi.

- **Puoi delegare a un sotto-agente?** Non serve: questa skill lavora sempre in questa conversazione.
- **Puoi leggere e scrivere una cartella di progetto persistente?** Significa uno strumento per i file sulla cartella del progetto dell'utente, dove i file restano dopo la fine di questa conversazione, come in Claude Code o Cowork; una sandbox che si azzera alla fine della chat non conta. Se sì, salva come in "Salvataggio". Leggi da `.brace/`, oppure da `.vanta/` se `.brace/` non esiste; un file chiamato `brace-punto-nave.md` vale come `punto-nave.md`. Prima della prima scrittura, se esiste `.vanta/` e non esiste `.brace/`, rinomina `.vanta/` in `.brace/` e dillo all'utente in una riga: "Ho rinominato `.vanta/` in `.brace/`." Se non c'è una cartella persistente, segui "Memoria in chat", che dà l'avviso in una riga.
- **È stato caricato uno stato all'avvio della sessione?** Se è stato caricato un Punto Nave, segui "Ripresa". Se no, e non c'è una cartella persistente, cercalo come descritto in "Memoria in chat".

## Formato

Usa esattamente queste voci, in quest'ordine. Ogni voce è breve e autosufficiente: deve essere comprensibile a chi riprende il lavoro in una nuova sessione senza aver letto la conversazione.

```markdown
# Punto Nave · AAAA-MM-GG

- **Obiettivo:** lo scopo reale, in una frase.
- **Vincoli:** limiti fissi (tempo, budget, risorse, regole).
- **Variabili chiave:** nome = valore corrente (con l'unità), una per riga se sono più di due.
- **Decisioni prese:** cosa è stato deciso e perché, in sintesi.
- **Questioni aperte:** cosa resta da decidere o verificare.
- **Rischi principali:** al massimo tre, con il segnale che li renderebbe evidenti.
- **Stato:** a che punto è il lavoro.
- **Prossima azione:** una sola azione concreta, con chi la fa.
```

Scrivi "nessuna" per le voci vuote invece di inventare contenuto. Distingui ciò che l'utente ha deciso da ciò che hai proposto tu: una tua proposta non accettata va in "Questioni aperte", non in "Decisioni prese".

## Salvataggio

Quando hai una cartella di progetto persistente:

1. Se esiste già `.brace/punto-nave.md` nella cartella di lavoro corrente, aggiungi il suo contenuto in fondo a `.brace/punto-nave-storico.md` (crealo se manca), così le versioni precedenti restano consultabili.
2. Scrivi il nuovo Punto Nave in `.brace/punto-nave.md`, sostituendo il precedente.
3. Mostra il Punto Nave in chat e indica in una riga dove l'hai salvato. All'avvio delle prossime sessioni in questa cartella il plugin lo ricaricherà automaticamente.

Quando non hai una cartella di progetto persistente, segui "Memoria in chat" qui sotto.

## Ripresa

Se all'inizio della sessione è stato caricato un Punto Nave precedente e l'utente riprende il lavoro, usalo come punto di partenza: verifica con lui che sia ancora valido prima di costruirci sopra.

## Memoria in chat

Usa questa sezione quando non c'è una cartella di progetto persistente. Il formato del file è lo stesso di `.brace/`, così l'utente può spostare in seguito il file in una cartella `.brace/` e Claude Code o Cowork lo riprenderanno.

- **Scrittura.** Mostra il Punto Nave, poi il file aggiornato completo `brace-punto-nave.md` in un unico blocco di codice. Poi dai una sola riga di avviso. Se hai trovato una conoscenza del Project o un file BRACE: "Aggiungi questo file alla conoscenza del Project come `brace-punto-nave.md`, sostituendo quello precedente se c'è." Altrimenti usa la riga di "Nessuna conoscenza del Project trovata" qui sotto. Dai sempre il file intero, mai un frammento, così l'utente sostituisce un file invece di unire pezzi.
- **Lettura.** All'inizio del lavoro pertinente, cerca nella conoscenza del Project e negli eventuali file caricati `brace-punto-nave.md` (o `punto-nave.md`). Se lo trovi, usalo come in "Ripresa": verifica con l'utente che sia ancora valido prima di costruirci sopra.
- **Nessuna conoscenza del Project trovata.** Se non trovi file BRACE né una conoscenza del Project, non affermare che questa chat è fuori da un Project: un Project vuoto appare allo stesso modo. Dai questa riga al posto di quella sulla conoscenza del Project qui sopra, una volta in questa chat: "Questa memoria dura solo per questa chat, a meno che tu non aggiunga questo file alla conoscenza di un Project come `brace-punto-nave.md` (crea un Project se non ne hai uno)." Mostra comunque il file completo, così l'utente può conservarlo.
