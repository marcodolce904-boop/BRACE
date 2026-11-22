---
type: llm
weight: 1
---

La risposta è corretta se riconosce la richiesta di rivedere una decisione passata e lo fa (la skill revisione, o lo stesso lavoro nella stessa forma) senza che l'utente nomini alcun comando o parola chiave. Deve cercare il record originale (per esempio il registro decisioni in .brace/ o .vanta/, o un file della chat o del Project) e, se non c'è, dirlo e ricostruire quel che può da ciò che ha detto l'utente, chiedendo la previsione originale e l'esito. Deve confrontare ciò che era previsto con ciò che è accaduto, separare la qualità della decisione dalla qualità dell'esito e dire che cosa l'utente dovrebbe fare diversamente. È sbagliata se si limita a rassicurare l'utente, se giudica solo dal risultato o se inventa un record che non esiste.
