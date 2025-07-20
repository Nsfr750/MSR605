# Domande Frequenti (FAQ)

## Domande Generali

### Cos'è il Lettore/Scrittore di Carte MSR605?
Il MSR605 è un'applicazione software che ti permette di leggere e scrivere su carte a banda magnetica utilizzando dispositivi compatibili di lettura/scrittura. Fornisce un'interfaccia intuitiva per la gestione dei dati delle carte.

### Quali sistemi operativi sono supportati?
L'applicazione è progettata per funzionare su:
- Windows 10/11 (64-bit)
- Linux (la maggior parte delle distribuzioni)
- macOS (sia Intel che Apple Silicon)

### Dove posso scaricare l'ultima versione?
Puoi scaricare l'ultima versione dalla nostra pagina [GitHub Releases](https://github.com/Nsfr750/MSR605/releases).

## Installazione

### Quali sono i requisiti di sistema?
- Python 3.8 o superiore
- Porta USB per il lettore di schede
- 100MB di spazio libero su disco
- Minimo 2GB di RAM (4GB consigliati)

### Come installo i driver necessari?
- **Windows**: I driver dovrebbero installarsi automaticamente quando colleghi il dispositivo
- **Linux**: La maggior parte delle distribuzioni include i driver necessari
- **macOS**: In genere non sono necessari driver aggiuntivi

### Perché il mio dispositivo non viene rilevato?
1. Assicurati che il dispositivo sia correttamente collegato a una porta USB
2. Prova una diversa porta USB
3. Controlla se il dispositivo appare nel gestore dispositivi del tuo sistema
4. Riavvia l'applicazione
5. Assicurati che nessun'altra applicazione stia utilizzando il dispositivo

## Utilizzo

### Come leggo una carta?
1. Inserisci la carta nel lettore
2. Fai clic sul pulsante "Leggi"
3. I dati della carta verranno visualizzati nella finestra principale

### Come scrivo su una carta?
1. Inserisci una carta scrivibile
2. Inserisci i dati che desideri scrivere
3. Seleziona quali tracce scrivere
4. Fai clic sul pulsante "Scrivi"

### Quali formati di carta sono supportati?
L'applicazione supporta i formati standard per banda magnetica:
- Traccia 1 (IATA): Fino a 79 caratteri alfanumerici
- Traccia 2 (ABA): Fino a 40 caratteri numerici
- Traccia 3 (THRIFT): Fino a 107 caratteri numerici

### Perché la mia carta non viene letta?
- La carta potrebbe essere danneggiata o smagnetizzata
- La carta potrebbe essere inserita in modo errato
- La banda magnetica potrebbe essere sporca (puliscila con un panno morbido)
- Il formato della carta potrebbe non essere supportato

## Risoluzione dei Problemi

### L'applicazione si blocca all'avvio
1. Assicurati di avere installate tutte le dipendenze richieste
2. Controlla il file di log per i messaggi di errore
3. Prova a reinstallare l'applicazione
4. Contatta l'assistenza con i dettagli dell'errore

### Ricevo errori "Dispositivo non trovato"
1. Scollega e riconnetti il dispositivo
2. Prova una diversa porta USB
3. Riavvia il computer
4. Verifica se il dispositivo è riconosciuto dal tuo sistema operativo

### I dati scritti sulla carta non vengono letti correttamente
1. Verifica che il formato dei dati corrisponda alle specifiche della traccia
2. Prova a scrivere su una traccia diversa
3. Prova con una carta diversa
4. Controlla se la testina di scrittura necessita di pulizia

## Sicurezza

### I miei dati della carta sono al sicuro?
L'applicazione elabora tutti i dati localmente sul tuo computer. Nessun dato della carta viene trasmesso su Internet a meno che tu non scelga esplicitamente di esportarlo o condividerlo.

### Posso crittografare i dati della carta?
Sì, l'applicazione supporta la crittografia dei dati della carta prima della scrittura. Abilita questa opzione nelle impostazioni.

### Quali funzionalità di sicurezza sono disponibili?
- Crittografia dei dati
- Protezione con password per i file salvati
- Cancellazione sicura dei dati
- Registro di controllo

## Sviluppo

### Come posso contribuire al progetto?
Accogliamo con favore i contributi! Consulta le nostre [Linee Guida per i Contributi](CONTRIBUTING.md) per maggiori informazioni.

### È disponibile un'API?
Sì, l'applicazione fornisce un'API Python per l'integrazione con altre applicazioni. Consulta la [Documentazione dell'API](API.md) per i dettagli.

### Come segnalo un bug?
Apri una segnalazione sulla nostra pagina [GitHub Issues](https://github.com/Nsfr750/MSR605/issues) con le seguenti informazioni:
- Passaggi per riprodurre il problema
- Comportamento atteso
- Comportamento effettivo
- Screenshot (se applicabile)
- Informazioni sul sistema

## Supporto

### Dove posso ottenere aiuto?
- Consulta la [Guida Utente](user_guide.md) per istruzioni dettagliate
- Cerca o pubblica nelle nostre [Discussioni GitHub](https://github.com/Nsfr750/MSR605/discussions)
- Invia un'email a nsfr750@yandex.com per assistenza diretta

### C'è un forum della comunità?
Sì, puoi unirti al nostro server Discord [qui](https://discord.gg/BvvkUEP9) per fare domande e condividere esperienze con altri utenti.

## Aspetti Legali

### Quali sono i termini di licenza?
Questo software è concesso in licenza con la licenza GPLv3. Vedi il file [LICENSE](../LICENSE) per i dettagli.

### Posso usarlo per scopi commerciali?
Sì, la licenza GPLv3 consente l'uso commerciale, ma tieni presente i requisiti della licenza riguardanti la distribuzione del codice sorgente per eventuali modifiche apportate.

### Dove posso trovare il codice sorgente?
Il codice sorgente completo è disponibile su [GitHub](https://github.com/Nsfr750/MSR605).
