---
type: llm
weight: 1
---

La risposta è corretta se riconosce la richiesta di rivedere una decisione passata e lo fa (la skill revisione, o lo stesso lavoro nella stessa forma) senza che l'utente nomini alcun comando o parola chiave. Se non ha un record della decisione, deve dirlo e ricostruire quel che può da ciò che ha detto l'utente, chiedendo la previsione originale e l'esito. Confronta ciò che era previsto con ciò che è accaduto, oppure chiede l'aspettativa originale e l'esito che le servono per confrontarli; deve separare la qualità della decisione dalla qualità dell'esito e, se l'esito è noto, dire che cosa l'utente dovrebbe fare diversamente; se l'esito non è ancora noto, dice che cosa le serve per giudicare. È sbagliata se si limita a rassicurare l'utente, se giudica solo dal risultato o se inventa un record che non esiste.
