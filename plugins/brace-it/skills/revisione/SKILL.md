---
name: revisione
description: "Rivede le decisioni registrate in .brace/decisioni.md la cui data di revisione è passata: raccoglie gli esiti, confronta previsioni e realtà e misura la calibrazione per livello di confidenza. Usala quando l'utente vuole riguardare le decisioni passate o sapere quanto sono state accurate le sue previsioni: 'com'è andata con le decisioni?', 'avevo ragione?', 'quali decisioni sono da rivedere?', 'how did my past decisions go?', 'was I right?'. Parola chiave: REVISIONE."
argument-hint: "[ID decisione | tutte]"
---

# Revisione delle decisioni

Argomenti: $ARGUMENTS

## Dove stai lavorando

Verifica cosa puoi fare qui, non in quale prodotto ti trovi.

- **Puoi delegare a un sotto-agente?** Non serve: questa skill lavora sempre in questa conversazione.
- **Puoi leggere e scrivere una cartella di progetto persistente?** Significa uno strumento per i file sulla cartella del progetto dell'utente, dove i file restano dopo la fine di questa conversazione, come in Claude Code o Cowork; una sandbox che si azzera alla fine della chat non conta. Se sì, segui la procedura su `.brace/decisioni.md`. Leggi da `.brace/`, oppure da `.vanta/` se `.brace/` non esiste; un file chiamato `brace-decisioni.md` vale come `decisioni.md`. Prima della prima scrittura, se esiste `.vanta/` e non esiste `.brace/`, rinomina `.vanta/` in `.brace/` e dillo all'utente in una riga: "Ho rinominato `.vanta/` in `.brace/`." Se non c'è una cartella persistente, segui "Memoria in chat" e dillo in una riga: "Qui non c'è una cartella di progetto, quindi lavoro sul registro dalla conoscenza del Project."
- **È stato caricato uno stato all'avvio della sessione?** Se sono state elencate decisioni da rivedere, parti da quelle, leggendo comunque il registro per i dettagli. Se non è stato caricato nulla e non c'è una cartella persistente, cerca il registro come descritto in "Memoria in chat".

## Procedura

1. Leggi `.brace/decisioni.md` nella cartella di lavoro corrente. Se non esiste, dillo e proponi `/brace-it:decisione`.
2. Seleziona le decisioni da rivedere:
   - con un ID negli argomenti, solo quella;
   - con `tutte`, tutte quelle con `Stato: aperta`;
   - senza argomenti, quelle con `Stato: aperta` e data di revisione uguale o precedente a oggi.
3. Per ciascuna mostra decisione, previsione e confidenza, poi chiedi all'utente l'esito. Raggruppa le domande in un unico messaggio quando le decisioni sono più di una. Non dedurre l'esito al posto suo.
4. Con le risposte aggiorna ogni voce, modificando solo questi campi:
   - `Esito:` cosa è successo, in una frase;
   - `Previsione corretta:` sì, no oppure parziale, confrontando la previsione scritta con l'esito, non con le intenzioni;
   - `Lezione:` cosa cambierebbe nella prossima decisione simile, solo se l'utente la condivide o se emerge con chiarezza;
   - `Stato:` chiusa. Se l'esito non è ancora osservabile, lascia `aperta` e sposta `Revisione:` alla nuova data concordata.

## Calibrazione

Dopo l'aggiornamento, calcola su tutte le decisioni chiuse del registro la quota di previsioni corrette per ciascun livello di confidenza (conta "parziale" come mezzo punto). Esegui il conteggio leggendo il file, non a memoria.

```markdown
| Confidenza | Decisioni chiuse | Previsioni corrette | Quota |
|---|---|---|---|
| Alta | | | |
| Media | | | |
| Bassa | | | |
```

Commenta solo ciò che i numeri permettono di dire. Con meno di cinque decisioni per livello, scrivi che il campione è troppo piccolo per conclusioni. Il segnale utile è l'ordine: le decisioni ad alta confidenza dovrebbero risultare corrette più spesso di quelle a bassa confidenza; se non succede, la fiducia dell'utente non sta discriminando, ed è la lezione più importante del registro.

## Memoria in chat

Usa questa sezione quando non c'è una cartella di progetto persistente. Il formato del file è lo stesso di `.brace/`, così l'utente può spostare in seguito il file in una cartella `.brace/` e Claude Code o Cowork lo riprenderanno.

- **Lettura.** Al passo 1, cerca nella conoscenza del Project e negli eventuali file caricati `brace-decisioni.md` (o `decisioni.md`) e usalo come registro. Se non lo trovi, dillo, chiedi all'utente di caricarlo se lo conserva altrove e altrimenti proponi di registrare prima una decisione.
- **Scrittura.** Dopo aver aggiornato le voci, mostra il file aggiornato completo `brace-decisioni.md` in un unico blocco di codice. Poi dai una riga: "Sostituisci `brace-decisioni.md` nella conoscenza del Project con questo file." Dai sempre il registro intero, mai un frammento, così l'utente sostituisce un file invece di unire pezzi.
- **Fuori da un Project.** Se non c'è una conoscenza del Project da cui leggere o a cui aggiungere, di' una volta in questa chat che la memoria dura solo per questa chat e suggerisci di creare un Project e aggiungere il file alla sua conoscenza. Mostra comunque il file completo, così l'utente può conservarlo.
- **Calibrazione.** Conta dal file, voce per voce, non a memoria né dalla conversazione. Se è disponibile uno strumento per eseguire codice, fai il conteggio con il codice sul testo del file aggiornato e costruisci la tabella dal suo risultato.
