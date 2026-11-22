---
name: stress-test
description: "Pre-mortem di un piano, una tesi o una decisione: assume che sia già fallito e ne ricostruisce le cause, con segnali precoci e contromisure. Usala quando l'utente vuole sapere come potrebbe fallire un piano o chiede di trovarne i punti deboli: 'come potrebbe andare storto?', 'trova i punti deboli', 'cosa mi sfugge?', 'dove può crollare?', 'how could this go wrong?', 'poke holes in this'. Parole chiave: STRESS TEST, pre-mortem."
argument-hint: "[piano, tesi o file] [indipendente]"
---

# Stress Test (pre-mortem)

Oggetto da testare: $ARGUMENTS

Se l'oggetto non è chiaro dagli argomenti né dalla conversazione, chiedi in una frase quale piano o tesi testare e fermati.

## Dove stai lavorando

Verifica cosa puoi fare qui, non in quale prodotto ti trovi.

- **Puoi delegare a un sotto-agente?** Se sì, la modalità indipendente delega all'agente `nemesi` come descritto sotto. Se no e la modalità indipendente è richiesta o accettata, esegui tu la sua procedura, in questa conversazione, giudicando soltanto il testo del piano, il criterio di successo e i vincoli dichiarati, e di' in una riga: "Qui la critica è meno indipendente: in Cowork o Claude Code la farebbe un agente separato." La modalità standard non ha bisogno di sotto-agenti.
- **Puoi leggere e scrivere una cartella di progetto persistente?** Significa uno strumento per i file sulla cartella del progetto dell'utente, dove i file restano dopo la fine di questa conversazione, come in Claude Code o Cowork; una sandbox che si azzera alla fine della chat non conta. Questa skill non scrive stato. Se esiste un Punto Nave in `.brace/` (o nella vecchia `.vanta/`), usalo come contesto per il piano.
- **È stato caricato uno stato all'avvio della sessione?** Se è stato caricato un Punto Nave, usalo come contesto e verifica con l'utente che sia ancora valido. Se no, e non c'è una cartella persistente, cerca `brace-punto-nave.md` nella conoscenza del Project e nei file caricati.

## Modalità

- **Standard (predefinita).** Esegui il pre-mortem tu, in questa conversazione. Costo basso. Limite: la critica nasce dallo stesso contesto che ha prodotto il piano, quindi tende a non vedere gli stessi punti ciechi.
- **Indipendente.** Se gli argomenti contengono `indipendente` (o l'utente chiede un critico esterno), delega all'agente `nemesi`. Passagli soltanto il testo del piano, il criterio di successo e i vincoli dichiarati dall'utente; non passargli il tuo ragionamento né le tue opinioni sul piano, altrimenti perde l'indipendenza. Poi riporta la sua critica e aggiungi, separato, il tuo commento su cosa condividi e cosa no. Costo più alto: avvisa l'utente in una riga; se la modalità indipendente non è stata chiesta esplicitamente, aspetta un sì prima di partire.

## Procedura

1. **Riformula** il piano in una frase e il criterio di successo misurabile. Se il criterio non esiste, segnalalo: è già un primo rischio.
2. **Assumi il fallimento.** "Sono passati 12 mesi (o l'orizzonte pertinente) e il piano è fallito." Genera le cause in quattro categorie: esecuzione, mercato e avversari, risorse, assunzioni errate. Usa la checklist in `${CLAUDE_PLUGIN_ROOT}/skills/stress-test/references/bias.md` per cercare le assunzioni errate.
3. **Ordina** le cause per probabilità × impatto e tieni le prime cinque.
4. Per ciascuna indica il **segnale precoce** (cosa vedresti presto se stesse succedendo) e la **contromisura** (cosa fare adesso o quando compare il segnale).
5. **Chiudi** con la modifica al piano che riduce di più il rischio complessivo e con il caso peggiore sopportabile: se il piano fallisce, quanto si perde e si può recuperare?

## Formato

```markdown
**Piano:** …  ·  **Criterio di successo:** …

| # | Causa del fallimento | Prob. | Impatto | Segnale precoce | Contromisura |
|---|---|---|---|---|---|

**Modifica consigliata:** …
**Caso peggiore:** …
**Confidenza:** Alta/Media/Bassa — cosa la cambierebbe.
```

Probabilità e impatto si esprimono come Alta/Media/Bassa, non come percentuali inventate. Se il piano è solido su un punto, dillo: una causa di fallimento fabbricata per riempire la tabella è un errore.
