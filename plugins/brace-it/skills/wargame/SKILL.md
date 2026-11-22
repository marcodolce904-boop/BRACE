---
name: wargame
description: "Simulazione Rosso contro Blu su un piano o una decisione: un avversario attacca il piano, un difensore lo adatta, poi una sintesi indica conseguenze di secondo ordine e punto di rottura. Usala quando l'esito dipende da come reagiranno gli altri (concorrenti, mercato, controparte) e la posta in gioco è alta, oppure quando l'utente chiede una simulazione avversaria: 'come reagirebbe il mercato?', 'come reagirebbero i concorrenti?', 'simula la controparte', 'how would competitors react?', 'simulate the other side'. Parola chiave: WARGAME."
argument-hint: "[scenario] [rapido]"
---

# Wargame Rosso / Blu

Scenario: $ARGUMENTS

## Controllo del costo

Fallo prima di ogni altra cosa, con un'eccezione: se la Preparazione richiede una domanda di chiarimento, fai prima quella domanda e chiedi del costo quando lo scenario è chiaro.

- **Sotto-agenti disponibili.** Se gli argomenti non contengono `rapido`, di' in una riga che la modalità con agenti costa diverse risposte normali, proponi la modalità rapida e aspetta un sì. Esempio: "Il wargame con agenti costa diverse risposte normali; in alternativa posso farne una versione rapida qui. Procedo con gli agenti?" Se l'utente sceglie la rapida o non conferma, usa la modalità rapida.
- **Sotto-agenti non disponibili.** Passa alla modalità rapida e dillo in una riga, aggiungendo che in Cowork o Claude Code ogni parte sarebbe un agente separato. Esempio: "Qui gli agenti non sono disponibili, quindi simulo io entrambe le parti; in Cowork o Claude Code ogni parte sarebbe un agente separato."

## Dove stai lavorando

Verifica cosa puoi fare qui, non in quale prodotto ti trovi.

- **Puoi delegare a un sotto-agente?** Se sì, la modalità con agenti usa gli agenti `rosso` e `blu`, dopo il sì nel controllo del costo. Se no, il controllo del costo qui sopra ti manda già alla modalità rapida con il suo avviso in una riga, che deve dire che in Cowork o Claude Code ogni parte sarebbe un agente separato.
- **Puoi leggere e scrivere una cartella di progetto persistente?** Significa uno strumento per i file sulla cartella del progetto dell'utente, dove i file restano dopo la fine di questa conversazione, come in Claude Code o Cowork; una sandbox che si azzera alla fine della chat non conta. Questa skill non scrive stato. Se esiste un Punto Nave in `.brace/` (o nella vecchia `.vanta/`), usalo come contesto per il piano BLU.
- **È stato caricato uno stato all'avvio della sessione?** Se è stato caricato un Punto Nave, usalo come contesto e verifica con l'utente che sia ancora valido. Se no, e non c'è una cartella persistente, cerca `brace-punto-nave.md` nella conoscenza del Project e nei file caricati.

## Preparazione

Prima di lanciare gli agenti, fissa in poche righe:

- **Piano BLU:** cosa vuole fare l'utente e con quale obiettivo misurabile.
- **ROSSO:** chi o cosa reagisce (concorrente, cliente, mercato, ente, la realtà fisica) e quali sono i suoi incentivi.
- **Orizzonte:** il periodo simulato.

Se uno di questi elementi manca e cambierebbe il risultato, fai una sola domanda e fermati. Altrimenti esplicita le assunzioni e procedi.

## Modalità

- **Con agenti (predefinita).** ROSSO e BLU sono agenti separati, ciascuno con il proprio contesto. Costa diverse volte una risposta normale: avviala solo dopo il sì nel controllo del costo.
- **Rapida.** Se gli argomenti contengono `rapido`, simula entrambe le parti tu, in questa conversazione, con lo stesso formato. Costo basso, ma le due parti condividono lo stesso punto di vista.

## Procedura con agenti

1. **Turno ROSSO.** Delega all'agente `rosso`. Passagli il piano BLU, l'identità e gli incentivi di ROSSO, l'orizzonte. Chiedi tre mosse.
2. **Turno BLU.** Delega all'agente `blu`. Passagli il piano BLU e le tre mosse di ROSSO, senza il tuo commento. Chiedi una risposta per ogni mossa.
3. **Arbitraggio.** Fai tu la sintesi finale, con il formato sotto. Valuti le mosse, non le parti: se una mossa di ROSSO è poco plausibile o una risposta di BLU è troppo ottimista, dillo.

## Formato della sintesi

```markdown
**BLU:** … · **ROSSO:** … · **Orizzonte:** …

| Mossa ROSSO | Prob. | Danno per BLU | Risposta BLU | Costo | Rischio residuo |
|---|---|---|---|---|---|

**Conseguenze di secondo ordine:** cosa succede dopo le prime reazioni.
**Punto di rottura:** la condizione in cui il piano non regge più.
**Modifica che rende BLU più robusto:** …
**Ipotesi:** elenco di ciò che è speculativo.
**Confidenza:** Alta/Media/Bassa — cosa la cambierebbe.
```

Il wargame produce scenari plausibili, non previsioni: etichetta come ipotesi tutto ciò che non poggia su dati. Se dalla simulazione esce una scelta da registrare, chiudi proponendo di registrare la decisione.
