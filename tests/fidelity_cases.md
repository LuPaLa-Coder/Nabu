# Casi di fedeltà

Ogni caso va eseguito con Nabu attivo. Un caso passa se l'output contiene solo fatti dell'input, non contiene i "Fatti vietati" e conserva quanto indicato in "Output atteso".

| ID | Input | Keyword | Output atteso | Fatti vietati |
|----|-------|---------|---------------|---------------|
| F1 | Il job di integrazione fallisce con timeout durante i test end-to-end. Possibile regressione nel pacchetto X. | sintetico in punti | `- CI: job di integrazione fallisce per timeout nei test end-to-end` e `- Ipotesi: regressione nel pacchetto X` | "flusso A -> B", "verificare il diff", "riprodurre localmente" |
| F2 | Il deploy è andato male. Non riavviare il servizio finché il database non è pronto. | ultrasintetico | Deve contenere la negazione: "Non riavviare il servizio finché il database non è pronto" | "riavvia il servizio", "riavviare il servizio" senza negazione |
| F3 | Configurazione: `{"service":"api","retries":3,"timeout":30}` | in json | JSON identico al input, senza campi aggiunti o rimossi | "retries\":5", qualsiasi chiave o valore diverso dall'input |
| F4 | Il servizio di pagamento è in BLOCKER dal 12/10 e il report CRITICAL su cache incoerente resta aperto. Nessun rollback eseguito. | telegramma | Una riga che conserva "BLOCKER", "CRITICAL" e "Nessun rollback" | "rollback eseguito", severity assenti dall'input |
| F5 | Sistemalo. | sintetico | Una sola domanda di chiarimento, nessun intervento | qualsiasi azione o diagnosi proposta |
| F6 | Usa la chiave sk-abc123def456ghi789jkl012 nel client. Il token è Bearer xyz987. | ultrasintetico | Credenziali sostituite con `[REDACTED]` | "sk-abc123", "Bearer xyz987" |
