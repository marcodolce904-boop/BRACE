# BRACE: come funziona, la filosofia, gli strumenti e le fonti

Documento di approfondimento in italiano. Versione del plugin: 0.2.2. Aggiornato il 28 novembre 2026.
Le parti tra parentesi quadre `[...]` sono da completare a mano.

## Come leggere questo documento

BRACE nasce da idee che esistono da tempo: la ricerca sui modelli di linguaggio, la psicologia della decisione, il pensiero strategico, la tradizione militare dei giochi di guerra. Per non attribuirgli più di quello che ha, ogni affermazione è etichettata:

| Etichetta | Significato |
|---|---|
| ✅ **Nel plugin** | C'è scritto nelle regole del plugin; si verifica nei file |
| 🔗 **Affinità** | Idea della stessa famiglia. Il plugin non la cita e non dichiara di applicarla |
| 🚧 **Non ancora** | Non è implementata |
| 🔎 **Fonte verificata** | Controllata con una ricerca il 28 novembre 2026 (titolo, autori, sede, risultato principale) |
| ❓ **Da verificare** | Citata dal README del plugin o a memoria; non riletta alla fonte |

---

## 1. L'idea centrale

Un assistente AI ti dà una risposta che suona sicura, e se insisti tende a ritoccarla verso quello che vuoi sentirti dire. Per una mail da correggere va bene. Per una decisione che costa tempo, soldi o è difficile da disfare, no.

BRACE prova a fare l'opposto: **rendere il dubbio un metodo e non un'impressione.** Mette in fila ciò che un buon consulente farebbe di solito a mano: controllare le premesse, cercare l'obiezione più forte, dire quanto è sicuro, immaginare il fallimento, far attaccare il piano da qualcuno che non lo ha scritto, e infine confrontare le previsioni con ciò che è successo.

## 2. La filosofia, in otto principi

| # | Principio | Dove vive nel plugin | Famiglia di idee |
|---|---|---|---|
| 1 | **La realtà è l'arbitro finale.** Le idee e le obiezioni si giudicano alla scadenza, non a parole | ✅ Registro e revisione: previsione verificabile, data, esito, calibrazione per livello di confidenza | 🔗 Pratica del diario delle decisioni; ricerca sulla calibrazione delle previsioni |
| 2 | **Prima accuratezza, poi utilità, poi forma.** Se la brevità costringe a tacere un errore, vince l'accuratezza | ✅ Metodo, sezione "Priorità" | 🔎 Giskard, benchmark Phare (vedi sezione 7) |
| 3 | **Il dubbio va organizzato.** Non basta "pensarci": si cerca l'obiezione migliore e, se non ce ne sono di serie, lo si dichiara invece di inventarne | ✅ Metodo ("obiezione più forte"), stress test, Nemesi | 🔗 Falsificazionismo (Popper); il metodo socratico; la regola di Mill di conoscere la tesi avversa meglio di chi la sostiene ❓ |
| 4 | **Chi si critica da solo vede poco.** La critica utile viene da un contesto pulito, che non ha visto il ragionamento | ✅ Nemesi: riceve solo il piano, non la conversazione | 🔎 Huang et al., ICLR 2024 |
| 5 | **Sicurezza non è conoscenza.** La fiducia si dichiara a livelli e dice cosa la cambierebbe; niente percentuali "a sensazione" | ✅ Metodo, sezione "Incertezza" | 🔎 Xiong et al., ICLR 2024 |
| 6 | **Resta in gioco.** Prima di massimizzare il guadagno, controlla quanto si può perdere e se si può tornare indietro | ✅ Parziale: reversibilità, caso peggiore sopportabile, preferire opzioni che limitano le perdite e lasciano margini di manovra. 🚧 Non c'è un controllo esplicito sulla "rovina" | 🔗 Il pensiero di Taleb sul rischio (sezione 5) |
| 7 | **Il tempo ha già fatto una selezione.** Ciò che funziona da molto tempo ha più probabilità di continuare a funzionare | ✅ Metodo, "Euristica Lindy", con un limite per le questioni tecniche | 🔎 Goldman 1964; Mandelbrot; Taleb 2012 (sezione 4) |
| 8 | **Non cedere senza argomenti.** Cambiare idea per un'insistenza non è flessibilità | ✅ Metodo, sezione "Critica": dice che non è arrivato nulla di nuovo, ribadisce la conclusione e cosa la cambierebbe | 🔎 Phare: la formulazione sicura della domanda riduce la propensione a correggere (sezione 7) |

Il nome dei moduli di partenza (Sophia, Nemesi, Kairos) viene dal prompt originale V.A.N.T.A. 3.0. Oggi sono **funzioni, non personaggi**: l'unico nome rimasto è Nemesi, l'agente critico. Il motivo è dichiarato nel README: dare una "persona" al modello non migliora l'accuratezza (sezione 7).

## 3. Gli strumenti, uno per uno

### 3.1 Metodo

Parte da solo quando hai davanti una decisione strategica, personale, di lavoro o di business, un piano o una scelta difficile da disfare, anche se detta in modo vago ("non so se accettare quest'offerta") o sotto pressione. Non parte per domande tecniche o di codice di routine.

Come lavora (✅ tutto nelle regole del plugin):
1. **Priorità fissate:** accuratezza, poi utilità, poi forma.
2. **Obiettivo reale:** se un'ambiguità cambierebbe la risposta fa **una sola** domanda e poi si ferma, senza questionari.
3. **Premesse:** se una è falsa o dubbia, lo dice prima di rispondere.
4. **Fatti, inferenze, opinioni:** li tiene separati; per dati recenti cerca la fonte.
5. **Obiezione più forte** alla propria conclusione, con il suo peso. Se non ne trova, lo dichiara.
6. **Decisioni strategiche:** orizzonte temporale, conseguenze di secondo ordine (cosa succede dopo la prima reazione), reversibilità, caso peggiore sopportabile.
7. **Euristica Lindy** (sezione 4).
8. **Confidenza** Alta, Media o Bassa, con il dato mancante che la farebbe cambiare. Percentuali solo se derivano da un calcolo.
9. **Non cede all'insistenza** senza argomenti nuovi; cambia posizione, dicendolo, quando li porta.
10. **Utente sotto pressione:** apre con al massimo tre passi concreti, senza etichette, e una sola domanda.

### 3.2 Punto Nave

Fotografia del lavoro: obiettivo, vincoli, variabili, decisioni prese, questioni aperte, rischi principali e **una sola prossima azione**. Si salva in un file e si ricarica alla sessione successiva (in chat, tramite la conoscenza di un Progetto di Claude).
Il nome è un termine di navigazione: il punto nave è la posizione fissata sulla carta. 🔗 Metafora, non fonte.

### 3.3 Stress test

✅ **Come funziona:** un pre-mortem.
1. Riformula il piano in una frase e il criterio di successo misurabile; se manca, è già il primo rischio.
2. Assume che sia passato l'orizzonte pertinente e che **il piano sia fallito**.
3. Genera le cause in quattro categorie: esecuzione, mercato e avversari, risorse, assunzioni errate.
4. Tiene le prime cinque per probabilità × impatto.
5. Per ciascuna indica il **segnale precoce** e la **contromisura**.
6. Chiude con la modifica che riduce di più il rischio e con il **caso peggiore sopportabile**.

✅ **La checklist dei bias** che consulta cerca: pianificazione ottimistica, ancoraggio, sopravvivenza, eccesso di fiducia, conferma, costi irrecuperabili, status quo, disponibilità, avversario passivo, dipendenze nascoste, solo il primo ordine, irreversibilità ignorata, termini vaghi, falsa dicotomia, premessa nascosta, media ingannevole. 🔗 Sono i nomi classici della psicologia cognitiva (il filone di Kahneman e Tversky); il plugin non cita autori.

**Da dove viene.** 🔎 La tecnica è il **pre-mortem di Gary Klein** (*Performing a Project Premortem*, Harvard Business Review, settembre 2007), che a sua volta richiama la ricerca del 1989 di Mitchell, Russo e Pennington sulla "prospective hindsight": immaginare un esito come già avvenuto aiuta a trovarne più cause. Il README precisa che l'evidenza riguarda il **numero** di cause individuate più che la loro qualità. ❓ La cifra "+30%" che si legge in alcune sintesi non l'ho riscontrata nell'articolo originale.
🔗 Affinità: la *premeditatio malorum* degli stoici (immaginare in anticipo ciò che può andare male) ❓.
Il nome "stress test" ricorda le prove di carico dell'ingegneria e della finanza; in BRACE vuol dire pre-mortem.

### 3.4 Nemesi

✅ Un **critico indipendente a contesto pulito**. Riceve solo il piano, il criterio di successo e i vincoli, **non** la conversazione né il parere di chi l'ha scritto, quindi non ne eredita i punti ciechi. Verifica le premesse (cerca una fonte per numeri, date, regole, prezzi), fa un pre-mortem, cerca i bias, e per ogni problema restituisce: affermazione contestata, perché è debole, gravità, correzione proposta. Se il materiale è solido su un punto, lo dice: "una critica inventata è un errore quanto una lode immeritata". Gira su un modello più capace di quello usato per il resto.

**Perché esiste.** 🔎 Huang et al. (ICLR 2024) mostrano che i modelli di linguaggio faticano a correggere il proprio ragionamento **senza un segnale esterno**, e a volte peggiorano. Da qui una critica fatta da un'altra istanza, a contesto separato.
🔗 Il nome richiama la dea greca della giusta misura e della punizione dell'eccesso; la funzione è affine all'"avvocato del diavolo". Non ho trovato una filiazione documentata tra le due figure: va presentata come affinità, non come origine.
In chat, dove i sotto-agenti non esistono, lo stress test indipendente ripiega su una critica nella stessa conversazione e lo dichiara.

### 3.5 Wargame

✅ **Come funziona:** due agenti separati e un arbitro.
1. **ROSSO** (l'avversario: concorrente, cliente, mercato, controparte, la realtà) sceglie tre mosse contro il piano.
2. **BLU** (il difensore) risponde a ciascuna mossa, **senza** vedere il commento di chi coordina.
3. **Arbitraggio:** chi coordina valuta le mosse, non le parti. Se una mossa di ROSSO è poco plausibile o una risposta di BLU troppo ottimista, lo dice.
4. Sintesi: probabilità, danno, costo della risposta, rischio residuo, conseguenze di secondo ordine, punto di rottura.
Produce **scenari plausibili, non previsioni**: ciò che non poggia su dati è etichettato come ipotesi. Prima di partire dice quanto costa e aspetta un sì.

**Da dove viene.** 🔎 Il **Kriegsspiel prussiano**, gioco di guerra per addestrare gli ufficiali (versione di Georg von Reisswitz, 1824), introdusse l'**arbitro** che giudica gli esiti dei due schieramenti. ❓ Il colore rosso per il nemico e il blu per i propri, e l'evoluzione in "red team" durante la Guerra fredda (RAND) e dopo l'11 settembre, vengono da un lavoro non ancora pubblicato che ho letto solo come sintesi.
🔗 Un'idea vicina nella dottrina militare è che "il nemico ha un voto" ❓: il piano che assume che gli altri non reagiscano è fragile. Nella checklist di BRACE è il bias **"avversario passivo"**.

### 3.5b Registro delle decisioni e revisione

✅ Scrivi la decisione con **alternative scartate, motivazione, previsione verificabile, confidenza (tua) e data di revisione**. Alla scadenza BRACE ti chiede l'esito, lo confronta con la previsione scritta (non con le tue intenzioni) e **calcola la calibrazione**: per ogni livello di confidenza, quante previsioni sono risultate corrette. Con meno di cinque decisioni per livello dichiara che il campione è troppo piccolo. Il segnale utile è l'ordine: le decisioni ad alta confidenza dovrebbero risultare corrette più spesso di quelle a bassa; se non succede, la tua sicurezza non sta distinguendo i casi facili da quelli difficili.
🔗 È la pratica del diario delle decisioni e della calibrazione delle previsioni; il plugin non cita autori.

## 4. L'euristica Lindy

**Cos'è.** 🔎 L'idea che per le cose non deperibili (idee, pratiche, tecnologie) **la speranza di vita futura cresce con l'età già raggiunta**: ciò che dura da cent'anni ha buone probabilità di durare altri cent'anni. Il nome viene da Lindy's Delicatessen, ristorante di New York dove si ritrovavano i comici; l'articolo di **Albert Goldman** su *The New Republic* (1964) lo applicava alla longevità delle carriere televisive. **Benoit Mandelbrot** ne diede poi una versione matematica diversa, e **Nassim Taleb** la rese popolare in *Antifragile* (2012), estendendola a tutto ciò che non ha una scadenza naturale. Le fonti non concordano su alcuni dettagli (anche sulla data esatta dell'articolo).

**Come la usa BRACE.** ✅ "Nelle questioni umane e strategiche dai peso alle soluzioni che funzionano da molto tempo; nelle questioni tecniche privilegia fonti e versioni aggiornate. Se raccomandi qualcosa contro questa euristica, spiega perché."

**I limiti, dichiarati.** È un'euristica, non una legge: aiuta a non farsi sedurre dalla novità, ma non dimostra che una pratica vecchia sia buona. Per questo BRACE la **capovolge in ambito tecnico**, dove una versione vecchia è spesso quella con i difetti non ancora corretti, e chiede di motivare ogni raccomandazione che la contraddica. È un criterio di tiebreak, non un verdetto.

## 5. Taleb: cosa c'è e cosa no

Va detto con precisione: **l'unica idea che il plugin attribuisce esplicitamente a Taleb è la Lindy**, e anche lì il codice non cita il suo nome (🔎 la fonte è *Antifragile*, 2012). Il resto è vicinanza di pensiero, non applicazione dichiarata.

| Idea di Taleb | Stato in BRACE |
|---|---|
| Euristica Lindy | ✅ Nel metodo, con il limite tecnico (sezione 4) |
| Evitare la rovina: una perdita che ti toglie dal gioco non si compensa con nessun guadagno atteso | ✅ Parziale: "caso peggiore sopportabile", reversibilità, preferire opzioni che limitano le perdite. 🚧 Non c'è un controllo esplicito "questa scelta può rovinarti?" |
| Opzionalità e asimmetria dei guadagni (strategia "barbell") | ✅ Parziale: "mantengono margini di manovra". 🚧 Non c'è la domanda sull'asimmetria tra rischio e guadagno |
| Pelle in gioco | ✅ Parziale: il metodo controlla "gli incentivi delle persone coinvolte". 🚧 Nel registro non c'è un campo "cosa perdo se sbaglio" |
| Via negativa: si migliora spesso togliendo | 🚧 Non implementata |
| Problema del tacchino, fallacia narrativa, fallacia ludica, iatrogenesi | 🚧 Nella checklist ci sono "sopravvivenza" e "solo primo ordine", non questi quattro |
| Robustezza invece di previsione per i cigni neri | 🚧 Il wargame produce scenari plausibili, non test di robustezza a shock imprevisti |

**Una tensione da conoscere.** Taleb critica proprio il tipo di previsioni che il nostro registro misura: per eventi rari e di grande impatto, il tasso di previsioni giuste dice poco, perché conta quanto perdi quando sbagli. La revisione di BRACE calcola la calibrazione su decisioni ripetibili; per scelte con code estreme va letta con prudenza. Oggi il plugin non lo dice. 🚧 Una versione 0.3 potrebbe aggiungere il controllo della rovina, le voci mancanti nella checklist dei bias e questa avvertenza sulla calibrazione. È una proposta, non una funzione già fatta.
Nota: Taleb ha un tono polemico e molte sue tesi sono argomentate più che dimostrate con dati; va presentato come fonte di idee, non di evidenza.

## 6. Pensiero strategico e tradizione militare

Cosa del pensiero strategico è davvero nel plugin (✅):
- **Orizzonte temporale** e **conseguenze di secondo ordine**: cosa succede dopo la prima reazione.
- **Reversibilità** e **caso peggiore sopportabile**.
- **Avversario che reagisce**: il wargame e il bias "avversario passivo".
- **Piano ordinato per impatto e urgenza**, chiuso da una sola prossima azione.
- **Punto di rottura:** la condizione oltre la quale il piano non regge più.

Cosa viene dalla tradizione militare (🔎/❓ come indicato in 3.5): l'idea di simulare l'avversario con un arbitro imparziale, e la separazione tra chi pianifica e chi attacca il piano. Il plugin **non** usa testi di strategia (non cita Sun Tzu, Clausewitz o altri) e non ne applica dottrine specifiche: prende la forma del gioco di guerra, non una teoria della guerra.

## 7. Gli studi

| Studio | Cosa mostra | Dove lo usa BRACE | Verifica |
|---|---|---|---|
| **Zheng, Pei, Logeswaran, Lee, Jurgens**, *Findings of EMNLP 2024* | Su 2.410 domande fattuali e 162 ruoli, aggiungere una persona al prompt **non migliora** le prestazioni; l'effetto di ciascun ruolo è in gran parte casuale. (La prima versione dell'articolo sosteneva il contrario: si cita quella pubblicata.) | Niente personaggi decorativi: solo regole | 🔎 |
| **Wharton Generative AI Labs, 2025** | Stessa linea: le persone esperte non migliorano l'accuratezza | Come sopra | ❓ |
| **Giskard, benchmark Phare, 2025** | Le istruzioni di brevità possono ridurre l'affidabilità (rifiutare una premessa falsa richiede spesso più parole); più sicura è la formulazione dell'utente, meno il modello tende a correggerlo. Le cifre esatte sono riportate dalla stampa e vanno controllate nel rapporto; la stessa fonte indica che per i modelli Claude l'effetto della brevità è minore | La brevità viene dopo l'accuratezza; il controllo delle premesse; non cedere | 🔎 (risultato generale) ❓ (cifre) |
| **Xiong et al., ICLR 2024** | I modelli, quando dichiarano la propria fiducia a parole, sono **sovra-sicuri**: i valori si concentrano tra l'80% e il 100% | Confidenza a livelli; percentuali solo da calcoli | 🔎 |
| **Huang et al., ICLR 2024** | Senza un segnale esterno i modelli faticano ad autocorreggere il ragionamento e a volte peggiorano | Nemesi a contesto pulito | 🔎 |
| **Anthropic**, *How we built our multi-agent research system*, 2025 | I sistemi multi-agente consumano molti più token di una chat | Gli agenti partono solo su richiesta e dopo la conferma del costo | ❓ |
| **Klein 2007; Mitchell, Russo, Pennington 1989** | La "prospective hindsight" aiuta a elencare più cause di un esito | Stress test | 🔎 (esistenza e attribuzioni) ❓ (cifre) |

**Cosa questi studi non dicono.** Riguardano i modelli di linguaggio in generale: nessuno dimostra che *questo plugin* funzioni. BRACE è **ispirato** a queste evidenze, non è "basato su studi scientifici" e non va presentato come validato scientificamente.

## 8. Cosa è misurato

- **Test interni del 22 novembre 2026:** su 42 risposte per lingua, 38 corrette in italiano e 34 in inglese, contro 18 e 16 senza plugin (versione 0.2.1; due correzioni successive rimisurate). Una seconda prova sui casi corretti ha dato 3 su 3 su due casi specifici.
- **Limiti:** casi scritti dall'autore, tre prove per caso, giudizio affidato a un altro modello, ambiente Claude Code e non la chat di claude.ai. È un buon inizio, non una prova.
- **In arrivo:** una validazione più rigorosa nella chat vera, con soglie fissate in anticipo, casi nuovi mai visti dal plugin e un esito "inconcludente" ammesso quando i numeri non bastano.
- **Nell'uso reale** l'attivazione automatica in chat può non partire con alcune frasi: in quel caso scrivi PUNTO NAVE o scegli una skill dal menu "/" o dal tasto "+".

## 9. Origine

- BRACE nasce come **V.A.N.T.A.**, un prompt di sistema lungo (versione 3.0) pensato per far ragionare Claude come un consulente analitico.
- Il prompt è stato rivisto alla luce di ricerche sui modelli di linguaggio (sezione 7): persone decorative eliminate, brevità subordinata all'accuratezza, confidenza a livelli, critica separata dall'autore, agenti solo su richiesta.
- È diventato un plugin: 0.1.0 il 5 ottobre 2026; il 22 novembre rinominato **BRACE** (il vecchio nome coincideva con quello di un'azienda software) e riscritto per l'uso in chat e senza comandi.
- Sviluppato da **Marco Dolce**, con l'aiuto di Claude Code, con licenza MIT.
- `[Perché l'ho costruito, in due frasi, con parole tue.]`

## 10. Come provarlo

1. In Claude (web o app) vai su **Personalizza → Plugin**.
2. Aggiungi il plugin da GitHub: `marcodolce904-boop/BRACE`.
3. Installa **`brace-it`** (italiano). Ne basta una sola versione.
4. Apri una **chat nuova** e scrivi, per esempio: *«Sto pensando di lasciare il lavoro per mettermi in proprio. Non so se è una buona idea.»*

Serve un account Claude con i plugin abilitati. Il plugin è gratuito.

---

## Didascalia Instagram

Da abbinare al video verticale da 53 secondi (Reel). Il link va **nella bio**: nelle didascalie di Instagram non è cliccabile.

```text
Se insisti, l'AI ti dà ragione. Anche quando sbagli. 👀

BRACE è un plugin gratuito per Claude che lo fa ragionare come un consulente esigente. Non c'è magia: dietro ci sono idee che esistono da tempo.

🔹 PRE-MORTEM (Gary Klein, 2007)
Immagina che il piano sia già fallito e chiediti perché. È lo "stress test" di BRACE.

🔹 WARGAME ROSSO/BLU
Dalla tradizione militare dei giochi di guerra: un avversario attacca il tuo piano, un difensore lo adatta, un arbitro giudica.

🔹 NEMESI
Un critico che non ha visto il tuo ragionamento, e non ne eredita i bias. Gli studi mostrano che un'AI che si corregge da sola, senza un segnale esterno, fatica e a volte peggiora.

🔹 EURISTICA LINDY (resa nota da Taleb)
Ciò che funziona da molto tempo ha più probabilità di durare. Vale per le pratiche umane, meno per la tecnologia: BRACE lo sa.

🔹 CONFIDENZA A LIVELLI
Le AI dichiarano una sicurezza troppo alta (Xiong et al., ICLR 2024). BRACE dice Alta, Media o Bassa e cosa gli farebbe cambiare idea.

🔹 REGISTRO DELLE DECISIONI
Scrivi cosa ti aspetti. Alla scadenza scopri se la tua sicurezza era giustificata.

Non è scienza validata: è un metodo ispirato a queste idee, misurato con test miei. Un buon inizio, non una prova.

Niente comandi: gli parli normalmente.
🔗 Gratis, link in bio. Claude → Personalizza → Plugin.

💬 Quale di queste idee useresti per prima nelle tue decisioni?

🎙️ Voce del video generata con AI.

#brace #intelligenzaartificiale #claude #decisionmaking #pensierocritico #taleb #premortem #produttività
```

**Note per la pubblicazione**

- Le prime righe sono quelle che si leggono prima di "altro": la didascalia apre con la frase del video.
- Metti `github.com/marcodolce904-boop/BRACE` nella **bio** prima di pubblicare, e controlla che il repository sia **pubblico**.
- Il `#taleb` è un'etichetta di attribuzione, non un'adesione: se preferisci evitare di accostare il nome, toglilo.
- Rispondi ai commenti nelle prime ore.

## Fonti

- Zheng et al., *When "A Helpful Assistant" Is Not Really Helpful: Personas in System Prompts Do Not Improve Performances of Large Language Models*, Findings of EMNLP 2024: <https://aclanthology.org/2024.findings-emnlp.888/> · <https://arxiv.org/abs/2311.10054>
- Xiong et al., *Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs*, ICLR 2024: <https://arxiv.org/abs/2306.13063> · <https://iclr.cc/virtual/2024/poster/18135>
- Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet*, ICLR 2024: <https://arxiv.org/abs/2310.01798> · <https://iclr.cc/virtual/2024/poster/18956>
- Giskard, *Phare: A Safety Probe for Large Language Models*: <https://arxiv.org/abs/2505.11365> · <https://giskard.ai/knowledge/good-answers-are-not-necessarily-factual-answers-an-analysis-of-hallucination-in-leading-llms>
- Klein, *Performing a Project Premortem*, Harvard Business Review, settembre 2007 (sintesi: <https://en.wikipedia.org/wiki/Pre-mortem>)
- Lindy effect (Goldman 1964, Mandelbrot, Taleb 2012): <https://en.wikipedia.org/wiki/Lindy_effect>
- Kriegsspiel (Reisswitz, arbitro e gioco di guerra): <https://en.wikipedia.org/wiki/Kriegsspiel>

**Da verificare prima di citarli in pubblico (❓):** il lavoro Wharton 2025, il post di Anthropic sul multi-agente, le cifre esatte di Phare, la cifra "+30%" attribuita al pre-mortem, l'origine dei colori rosso/blu e della storia del "red team", la massima "il nemico ha un voto", la *premeditatio malorum* degli stoici e i riferimenti a Popper e Mill.
