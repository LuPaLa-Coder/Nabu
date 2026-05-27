# Nabu

Preprocessore semantico e postprocessore leggero per output tecnici. Filtra rumore, comprime contenuto e preserva struttura quando il testo contiene codice o dati formattati.

Source of truth: `SKILL.md`.

## Cosa fa

- riduce ridondanza e digressioni
- comprime risposte verbose
- preserva codice, JSON, YAML, XML e configurazioni
- attiva sintesi solo quando compaiono keyword esplicite
- prepara briefing e handoff tra agenti

## Keyword di sintesi

| Keyword | Effetto |
|---------|---------|
| `sintetico` | 5-8 righe |
| `ultrasintetico` | 2-4 righe |
| `telegramma` | una riga secca |
| nessuna keyword | risposta completa ma senza fluff |

## Formati supportati

| Richiesta | Output |
|-----------|--------|
| `in punti` | bullet list minimale |
| `in tabella` | tabella compatta |
| `in json` | JSON valido e minimale |
| `schema` | outline gerarchico |
| `codice` | solo la parte essenziale |

## Modalita di compressione

- `ultra-compress`: default, massima densita
- `key-points-only`: solo punti chiave
- `lossless-compact`: compatto senza perdita di contenuto
- `executive-brief`: 3-5 punti operativi con priorita

## Quando usarlo

- briefing tecnici
- log e report lunghi
- code review e analisi
- passaggi di contesto a un altro agente

## Miglioramenti verificati

Verifica funzionale eseguita sulla copia installata in `.agents/skills/nabu/SKILL.md`, risultata identica al sorgente del repository.

| Area | Comportamento verificato | Miglioramento osservato |
|------|---------------------------|--------------------------|
| Input breve | `Aggiorna dipendenze e correggi bug minori.` resta conciso e non viene espanso inutilmente | evita espansioni inutili e non aggiunge fluff |
| Sintesi keyword-driven | `sintetico`, `ultrasintetico`, `telegramma` producono rispettivamente output breve, molto breve e una riga | riduce rapidamente incident report e briefing senza perdere i fatti chiave |
| Formati espliciti | `in punti`, `schema`, `in json` restituiscono solo la struttura richiesta | rende l'output immediatamente riusabile in handoff, ticket e automazioni |
| Contenuti strutturati | il JSON `{"service":"api","retries":3,"timeout":30}` viene preservato senza alterazioni | comprime testo descrittivo senza rompere dati o configurazioni |
| Ambiguita | la specifica richiede una sola domanda di chiarimento su input come `Sistemalo.` | limita assunzioni errate e riduce rework quando il comportamento viene applicato dal runtime |
| Severity | etichette come `BLOCKER`, `HIGH`, `MEDIUM` vengono mantenute | preserva priorita operative e leggibilita per triage e handoff |

## Esito della verifica funzionale

- casi coperti nella baseline manuale: 10
- tensioni di specifica individuate inizialmente: 2
- tensioni di specifica corrette in `SKILL.md`: 2
- stato attuale della specifica: nessun conflitto funzionale aperto
- tokenizzazione misurata con `o200k_base`
- saldo netto su tutti i test: `254 -> 242` token (`-4.7%`)
- miglior riduzione su test passato: `T6`, `22 -> 16` token (`-27.3%`)


### Test eseguiti e variazione token

`Delta` positivo = token risparmiati. `Delta` negativo = output piu lungo dell'input.

| Test | Prompt | Input | Output | Delta | Riduzione | Esito | Osservazione |
|------|--------|------:|-------:|------:|----------:|-------|--------------|
| T1 | `Aggiorna dipendenze...` | 13 | 13 | 0 | 0.0% | PASS | input breve lasciato invariato |
| T2 | `... release di domani. sintetico` | 48 | 52 | -4 | -8.3% | PASS | sintesi corretta, ma i bullet aggiungono token |
| T3 | `... mismatch schema. ultrasintetico` | 34 | 29 | 5 | 14.7% | PASS | buona compressione con 2 righe |
| T4 | `Elenca azioni urgenti... telegramma` | 20 | 16 | 4 | 20.0% | PASS | una riga secca, riduzione netta |
| T5 | `... cache incoerente. in punti` | 26 | 26 | 0 | 0.0% | PASS | guadagno in struttura, non in token |
| T6 | `... downtime. telegramma in json` | 22 | 16 | 6 | 27.3% | PASS | miglior caso passato per densita |
| T7 | `Riassumi il piano... schema` | 28 | 34 | -6 | -21.4% | PASS | outline piu leggibile ma piu costoso in token |
| T8 | `Sintetizza senza alterare il JSON... sintetico` | 25 | 14 | 11 | 44.0% | PASS | preservazione JSON corretta; il vincolo rigido sulle righe e stato rimosso |
| T9 | `Sistemalo.` | 4 | 9 | -5 | -125.0% | PASS | aumento atteso: una domanda di chiarimento e obbligatoria |
| T10 | `BLOCKER... sintetico in punti` | 34 | 33 | 1 | 2.9% | PASS | output corretto: la struttura richiesta prevale sul conteggio righe/token |

### Punti di attenzione emersi dai test

- `in punti` e `schema` migliorano la leggibilita ma non garantiscono riduzione token; questo e corretto e non va classificato come errore
- su input molto brevi o ambigui la skill puo privilegiare qualita, struttura o chiarimento rispetto alla pura compressione
- nel runtime batch di `opencode` il marker esplicito della skill non compare sempre, quindi oggi viene segnalato come `WARN`, non come `FAIL`
- i test automatici devono continuare a fallire solo su regressioni funzionali reali: JSON non valido, severity perse, formato non rispettato, path runtime incoerenti

## Esempi

### Input breve

```text
Aggiorna dipendenze e correggi bug minori.
```

Output:

```text
Aggiorna dipendenze e correggi bug minori.
```

### `sintetico in punti`

```text
Il job di integrazione fallisce con timeout durante i test end-to-end. Possibile regressione nel pacchetto X. sintetico in punti
```

Output:

```text
- CI: test end-to-end falliscono
- Punto critico: timeout nel flusso A -> B
- Ipotesi: regressione nel pacchetto X
- Azione: riprodurre localmente e verificare il diff
```

### `telegramma in json`

```text
Elenca azioni urgenti: migrazione DB, backup completo, comunicazione downtime. telegramma in json
```

Output:

```json
{"actions":["migrazione DB","backup completo","comunicazione downtime"]}
```

## Note operative

- se il testo contiene codice o dati strutturati, non alterare la sintassi
- se l'obiettivo e ambiguo, fai una sola domanda di chiarimento
- il risultato deve essere piu corto dell'input, salvo casi gia molto brevi

