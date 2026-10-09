---
name: nabu
version: 3.0.0
description: Trasforma testo tecnico verboso in output sintetico o strutturato su richiesta (keyword), preservando codice, dati e severity. Pensato per briefing e handoff tra agenti.
activation:
  type: both
  preprocess: false
  postprocess: false
allowed-tools:
  - Read
  - Write
  - Edit
---

# Nabu

## Regole

1. Attivazione: interviene solo con una keyword di lunghezza o di formato, o se l'utente chiede esplicitamente di sintetizzare un testo. Altrimenti non interviene.
2. Lunghezza: `sintetico` 5-8 righe; `ultrasintetico` 2-4 righe; `telegramma` una riga.
3. Formato: `in punti`, `in tabella`, `in json`, `schema`, `codice`. Il formato esplicito vince sul template. Nessun testo fuori dal formato.
4. Modalità: `ultra-compress` (default), `key-points-only`, `lossless-compact`, `executive-brief` (3-5 punti con priorità e next action).
5. Payload intatto: codice, JSON, YAML, XML, configurazioni, comandi, path, numeri e unità restano identici.
6. Mai eliminare negazioni o limiti: non, mai, nessuno, solo, tranne.
7. Mantieni le etichette di severity: BLOCKER, CRITICAL, HIGH, MEDIUM, LOW.
8. Fedeltà: solo fatti presenti nell'input. Niente cause, azioni, componenti o numeri inventati. Un'ipotesi è ammessa solo se l'input la contiene già.
9. Input sotto 100 token: restituiscilo invariato, salvo keyword di formato.
10. Obiettivo ambiguo: una sola domanda di chiarimento.
11. Sicurezza: prima di trasformare, sostituisci con `[REDACTED]` i pattern `sk-...`, `Bearer ...`, `password=...`, `token=...`, `key=...`, `secret=...`.
12. Se la forma compressa non è più corta di quella normale, usa quella normale.
13. Non usare se: codice da compilare (comprimi solo i commenti), testi legali o contratti, richiesta esplicita di output esteso.

## Template

Standard:

```markdown
## Key Points
- [concetto]
## Condensed Summary
[sintesi compatta, mai narrativa]
```

Executive-brief:

```markdown
## Executive Brief
- [punto operativo] — [severity/priorità]
**Next action:** [azione immediata]
```
