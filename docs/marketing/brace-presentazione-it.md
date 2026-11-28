# BRACE: cos'è, come funziona, da dove nasce, perché interessa

Documento di presentazione in italiano. Aggiornato al 28 novembre 2026, versione 0.2.2 del plugin.
Le parti tra parentesi quadre `[...]` sono da completare a mano.

---

## In una frase

**BRACE è un consulente per le decisioni che vive dentro Claude.** È un plugin gratuito che cambia il modo in cui Claude ragiona con te quando c'è in gioco una scelta importante.

## Il problema

Gli assistenti AI hanno tre difetti proprio quando serve che ragionino bene:

1. **Ti danno ragione.** Se insisti, cedono, anche quando non porti un argomento nuovo.
2. **Sono troppo sicuri di sé.** Dicono "al 90%" senza alcun calcolo dietro.
3. **Dimenticano.** Chiudi la chat e il lavoro è perso, e nessuno controlla mai se le previsioni fatte si sono avverate.

## Come funziona

BRACE accompagna una decisione dall'inizio alla fine, con cinque strumenti.

| Strumento | Cosa fa |
|---|---|
| **Metodo** | Controlla le premesse della tua domanda, cerca l'obiezione più forte contro la propria conclusione e dichiara la confidenza (Alta, Media o Bassa) con ciò che la farebbe cambiare. Se insisti senza argomenti nuovi, te lo dice e non cede |
| **Punto Nave** | Una fotografia del lavoro: obiettivo, vincoli, decisioni, rischi e **una sola** prossima azione. Resta salvata e si ricarica nelle sessioni successive |
| **Stress test** | Un pre-mortem: si dà per scontato che il piano sia già fallito e se ne ricostruiscono le cause, i segnali d'allarme e le contromisure |
| **Wargame** | Due agenti separati, un avversario e un difensore, si scontrano sul tuo piano prima che lo faccia la realtà. Parte solo dopo che hai confermato il costo |
| **Registro e revisione** | Scrivi la decisione con una previsione verificabile. Alla scadenza BRACE confronta la previsione con l'esito e misura se la tua sicurezza era giustificata |

**Non servono comandi.** Parli normalmente ("questo piano regge?", "ho deciso di…", "facciamo il punto") e BRACE sceglie lo strumento giusto. Gli strumenti costosi chiedono il permesso prima di partire.

**Dove funziona.** In chat su claude.ai e nell'app, con la versione base. In Claude Code e Cowork con tutte le funzioni: agenti separati e memoria su file. In chat la memoria vive nella conoscenza di un Progetto di Claude.

### Un esempio

La stessa frase: *«Non ci capisco più niente, il cliente vuole tutto per lunedì, il lavoro è a metà e sono da solo. Che faccio?»*

- **Senza BRACE:** un piano lungo, con sei consigli e due domande.
- **Con BRACE:** tre passi chiari subito (elenca cosa manca in dieci minuti, avvisa il cliente oggi, lavora prima su ciò che sblocca la consegna) e una sola domanda.

## Origine

- BRACE è nato come **V.A.N.T.A.**, un prompt di sistema lungo (versione 3.0) pensato per far ragionare Claude come un consulente analitico.
- Quel prompt è stato rivisto alla luce di ricerche su cosa funziona davvero con i modelli di linguaggio: le persone decorative non migliorano l'accuratezza, la brevità non deve togliere le correzioni, le percentuali dichiarate dai modelli sono sovrastimate e l'autocritica senza un segnale esterno è poco affidabile.
- Da lì è diventato un **plugin**: una versione 0.1.0, pubblicata il 5 ottobre 2026, con sei strumenti, tre agenti e un registro delle decisioni.
- Il 22 novembre 2026 è stato rinominato **BRACE** e riscritto per l'uso in chat e senza comandi (versione 0.2). Nello stesso giorno è stato misurato per la prima volta, e le correzioni emerse dai test sono entrate nella 0.2.1 e nella 0.2.2.
- È sviluppato da **Marco Dolce**, con l'aiuto di Claude Code, ed è distribuito con licenza MIT.
- `[Perché l'ho costruito, in due frasi, con parole tue: qual è stato il momento o il problema da cui sei partito.]`

## Perché dovrebbe interessare

BRACE serve a chi usa l'AI per **scegliere**, non solo per scrivere:

- chi deve decidere se accettare un'offerta di lavoro, mettersi in proprio, assumere o investire;
- chi gestisce progetti e scadenze e vuole sapere come un piano potrebbe fallire prima che succeda;
- chi vuole tenere traccia delle proprie decisioni e capire, a distanza di mesi, se la propria sicurezza valeva qualcosa;
- chi si è accorto che l'AI tende a dargli ragione.

Il punto che lo distingue è l'ultimo strumento. Molti assistenti ti danno un parere. BRACE ti fa scrivere cosa ti aspetti e quanto ne sei sicuro, e poi ti mostra se avevi ragione.

## Cosa è provato e cosa no

- **Misurato:** su 42 risposte per lingua, 38 corrette in italiano e 34 in inglese, contro 18 e 16 senza il plugin. Prove fatte sulla versione 0.2.1 con due correzioni successive.
- **Limiti di quel dato:** test scritti da me, tre prove per caso, giudicati da un altro modello, in Claude Code e non nella chat di claude.ai. È un buon inizio, non una prova definitiva. Una validazione più rigorosa nella chat vera è in preparazione.
- **Dove può non partire da solo:** in chat l'attivazione automatica può non scattare con alcune frasi. In quel caso scrivi PUNTO NAVE, oppure scegli una skill di BRACE dal menu "/" o dal tasto "+".
- **Le basi teoriche** sono idee note di decisione e psicologia cognitiva e alcune ricerche sui modelli di linguaggio. BRACE non si basa su trattati o su un singolo studio, e non va presentato come "validato scientificamente".

## Come provarlo

1. In Claude (web o app) vai su **Personalizza → Plugin**.
2. Aggiungi il plugin da GitHub: `marcodolce904-boop/BRACE`.
3. Installa **`brace-it`** (la versione italiana). Ne basta una sola.
4. Apri una **chat nuova** e scrivi, per esempio: *«Sto pensando di lasciare il lavoro per mettermi in proprio. Non so se è una buona idea.»*

Serve un account Claude con i plugin abilitati. Il plugin è gratuito.

---

## Didascalia Instagram

Da abbinare al video verticale da 53 secondi (Reel). Il link va **nella bio**, perché nelle didascalie di Instagram non è cliccabile.

```text
Se insisti, l'AI ti dà ragione. Anche quando sbagli. 👀

Per una mail da correggere va bene.
Per una decisione importante, no.

Tra le cose che costruisco c'è BRACE: un plugin gratuito per Claude che lo fa ragionare come un consulente esigente.

✔️ controlla le premesse prima di rispondere
✔️ cerca l'obiezione più forte alla propria conclusione
✔️ dice quanto è sicuro e cosa gli farebbe cambiare idea
✔️ fa il pre-mortem dei piani: "è fallito, perché?"
✔️ registra le tue decisioni e, alla scadenza, ti dice se avevi ragione

Niente comandi: gli parli normalmente.
Nel video vedi la stessa domanda, con e senza BRACE.

🔗 Gratis, link in bio.
In Claude: Personalizza → Plugin.

💬 Qual è l'ultima decisione importante in cui avresti voluto qualcuno che ti contraddicesse?

🎙️ Voce del video generata con AI.

#brace #intelligenzaartificiale #claude #decisionmaking #produttività #aitools #pensierocritico
```

**Note per la pubblicazione**

- Le prime righe sono quelle che si leggono prima di "altro": per questo la didascalia apre con la frase del video.
- Metti `github.com/marcodolce904-boop/BRACE` nella **bio** del profilo prima di pubblicare.
- Il repository deve essere **pubblico**, altrimenti il link non funziona per chi lo apre.
- Rispondi ai commenti nelle prime ore: è quello che fa girare di più il post.
