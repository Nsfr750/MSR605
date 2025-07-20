# Visualizzazione dei Dati della Carta

Questo documento descrive le funzionalità avanzate di visualizzazione dei dati delle carte magnetiche disponibili nell'applicazione MSR605 Card Reader/Writer.

## Panoramica

Il modulo di visualizzazione fornisce rappresentazioni grafiche interattive e statiche dei dati delle carte magnetiche, aiutando gli utenti ad analizzare e comprendere la struttura e il contenuto delle tracce. Le visualizzazioni sono integrate nell'interfaccia utente dell'applicazione e si aggiornano automaticamente quando vengono letti nuovi dati dalla carta.

## Funzionalità

### 1. Distribuzione dei Caratteri

Visualizza la frequenza di ciascun carattere nei dati della traccia utilizzando un grafico a barre. Aiuta a identificare:
- Caratteri più comuni
- Modelli nei dati
- Possibili anomalie o corruzioni

### 2. Schema dei Bit

Mostra la rappresentazione binaria dei dati della traccia come un'onda, visualizzando:
- Valori dei singoli bit (0/1)
- Transizioni tra bit
- Densità dei dati

### 3. Metriche di Densità dei Dati

Presenta metriche chiave sui dati della traccia:
- Lunghezza totale (in caratteri)
- Numero di caratteri unici
- Densità dei caratteri (caratteri unici / lunghezza totale)

### 4. Analisi dei Campi

Analizza e visualizza la struttura dei dati della traccia:
- Rileva i separatori di campo (^, =)
- Mostra la lunghezza dei campi
- Evidenzia i confini tra i campi

## Utilizzo

### Accesso alle Visualizzazioni

1. Leggere una carta utilizzando l'interfaccia principale
2. Fare clic sulla scheda "Visualizzazione" nella finestra delle Funzioni Avanzate
3. Visualizzare le rappresentazioni generate per ciascuna traccia

### Personalizzazione

- **Tema**: Scegli tra diversi temi di colore (scuro, chiaro, seaborn, ggplot, ecc.)
- **Aggiorna**: Fai clic sul pulsante "Aggiorna Visualizzazioni" per aggiornare con gli ultimi dati
- **Interattività**: Passa il mouse sopra i grafici per vedere informazioni dettagliate

## Dettagli Tecnici

### Dipendenze

- `matplotlib`: Per la creazione di visualizzazioni statiche
- `seaborn`: Per visualizzazioni statistiche avanzate
- `plotly`: Per visualizzazioni interattive (uso futuro)

### Implementazione

Il sistema di visualizzazione è implementato in `script/visualization.py` e integrato con l'interfaccia utente principale tramite la classe `AdvancedFunctionsWidget`.

## Esempi

### Distribuzione dei Caratteri

```
Traccia 1: %B1234567890123456^ROSSI/MARIO^24051234567890123456789?
```

- Mostra la frequenza di ciascun carattere (cifre, lettere, simboli)
- Aiuta a identificare modelli nei dati

### Schema dei Bit

```
Traccia 2: ;1234567890123456=240512345678901?
```

- Mostra la rappresentazione binaria della traccia
- Visualizza le transizioni e la densità dei bit

## Risoluzione dei Problemi

### Le Visualizzazioni Non Appaiono

1. Assicurarsi che una carta sia stata letta correttamente
2. Verificare che i dati della traccia non siano vuoti
3. Controllare che tutte le dipendenze siano installate (eseguire `pip install -r requirements.txt`)

### Le Visualizzazioni Appaiono Errate

1. Provare ad aggiornare le visualizzazioni
2. Selezionare un tema diverso
3. Controllare i log dell'applicazione per eventuali messaggi di errore

## Miglioramenti Futuri

- Aggiunta di ulteriori tipi di visualizzazione (mappe di calore, istogrammi)
- Supporto per il salvataggio delle visualizzazioni come immagini
- Esplorazione interattiva dei dati
- Esportazione dei dati di visualizzazione (CSV, JSON)
