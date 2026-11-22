---
name: decisione
description: "Registra una decisione nel registro decisioni (.brace/decisioni.md) con alternative scartate, motivazione, previsione verificabile, confidenza e data di revisione. Usala quando l'utente chiede di registrare o annotare una scelta, oppure ha appena preso una decisione importante e accetta di registrarla: 'ho deciso di...', 'segnati questa scelta', 'andiamo con X', 'mettilo agli atti', 'I've decided to...', 'let's go with X'. Parola chiave: DECISIONE."
argument-hint: "[decisione]"
---

# Registra una decisione

Decisione: $ARGUMENTS

Il registro serve a confrontare in seguito ciò che l'utente si aspettava con ciò che è successo. Funziona solo se la previsione è verificabile, quindi la qualità della voce "Previsione" è il punto più importante.

## Dove stai lavorando

Verifica cosa puoi fare qui, non in quale prodotto ti trovi.

- **Puoi delegare a un sotto-agente?** Non serve: questa skill lavora sempre in questa conversazione.
- **Puoi leggere e scrivere una cartella di progetto persistente?** Significa uno strumento per i file sulla cartella del progetto dell'utente, dove i file restano dopo la fine di questa conversazione, come in Claude Code o Cowork; una sandbox che si azzera alla fine della chat non conta. Se sì, salva come in "Salvataggio". Leggi da `.brace/`, oppure da `.vanta/` se `.brace/` non esiste; un file chiamato `brace-decisioni.md` vale come `decisioni.md`. Prima della prima scrittura, se esiste `.vanta/` e non esiste `.brace/`, rinomina `.vanta/` in `.brace/` e dillo all'utente in una riga: "Ho rinominato `.vanta/` in `.brace/`." Se non c'è una cartella persistente, segui "Memoria in chat" e dillo in una riga: "Qui non c'è una cartella di progetto, quindi il registro va nella conoscenza del Project."
- **È stato caricato uno stato all'avvio della sessione?** Se sono state elencate decisioni da rivedere, puoi ricordarle all'utente dopo la registrazione. Se non è stato caricato nulla e non c'è una cartella persistente, cerca il registro come descritto in "Memoria in chat".

## Procedura

1. Ricava i campi dalla conversazione. Per quelli mancanti fai una sola domanda che li raccolga tutti; non inventare motivazioni o alternative che l'utente non ha espresso.
2. Rendi la previsione **verificabile**: cosa deve essere vero, misurabile, entro quale data. "Andrà bene" non è una previsione; "Entro il 30 novembre almeno 3 clienti su 10 contattati accettano il preventivo" lo è. Se la previsione dell'utente è vaga, proponi una versione misurabile e chiedi conferma.
3. La **confidenza** è dell'utente (Alta, Media o Bassa), non tua. Se vuoi, dai la tua stima separatamente, nel testo della risposta.
4. La **data di revisione** predefinita è a 30 giorni da oggi; usa quella indicata dall'utente o quella in cui l'esito sarà osservabile.
5. Assegna un identificativo `D-AAAAMMGG-NN`, dove NN è il progressivo del giorno.

## Salvataggio

Aggiungi la voce in fondo a `.brace/decisioni.md` nella cartella di lavoro corrente (crea il file e la cartella se mancano, con il titolo `# Registro decisioni`). Mantieni esattamente questo formato, perché il plugin lo legge per ricordare le revisioni scadute:

```markdown
## D-20261004-01 · Titolo breve
- Data: 2026-10-04
- Decisione: …
- Alternative scartate: …
- Motivazione: …
- Previsione: …
- Confidenza: Media
- Revisione: 2026-11-03
- Stato: aperta
- Esito:
- Previsione corretta:
- Lezione:
```

Senza una cartella di progetto persistente, segui "Memoria in chat" qui sotto.

Chiudi con una riga di conferma che indica l'identificativo e la data di revisione.

## Memoria in chat

Usa questa sezione quando non c'è una cartella di progetto persistente. Il formato del file è lo stesso di `.brace/`, così l'utente può spostare in seguito il file in una cartella `.brace/` e Claude Code o Cowork lo riprenderanno.

- **Lettura.** Prima di assegnare l'identificativo, cerca nella conoscenza del Project e negli eventuali file caricati `brace-decisioni.md` (o `decisioni.md`). Usalo come registro esistente, così la nuova voce va in fondo e il progressivo del giorno è corretto.
- **Scrittura.** Mostra la nuova voce, poi il file aggiornato completo `brace-decisioni.md` in un unico blocco di codice: il registro esistente con la nuova voce in fondo oppure, se non c'è, un nuovo registro con il titolo `# Registro decisioni`. Poi dai una riga: "Aggiungi questo file alla conoscenza del Project come `brace-decisioni.md`, sostituendo quello precedente se c'è." Dai sempre il registro intero, mai un frammento, così l'utente sostituisce un file invece di unire pezzi.
- **Fuori da un Project.** Se non c'è una conoscenza del Project da cui leggere o a cui aggiungere, di' una volta in questa chat che la memoria dura solo per questa chat e suggerisci di creare un Project e aggiungere il file alla sua conoscenza. Mostra comunque il file completo, così l'utente può conservarlo.
