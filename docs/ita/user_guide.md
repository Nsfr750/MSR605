# MSR605 Lettore/Scrittore di Carte - Guida Utente

Benvenuto nella guida utente di MSR605 Lettore/Scrittore di Carte! Questo documento ti aiuterà a iniziare a utilizzare l'applicazione per leggere e scrivere su carte a banda magnetica.

## Indice
1. [Installazione](#installazione)
2. [Per Iniziare](#per-iniziare)
3. [Lettura delle Carte](#lettura-delle-carte)
4. [Scrittura sulle Carte](#scrittura-sulle-carte)
5. [Configurazione](#configurazione)
6. [Risoluzione dei Problemi](#risoluzione-dei-problemi)

## Installazione

### Windows
1. Scarica l'ultima versione dell'installer dalla pagina [Release](https://github.com/Nsfr750/MSR605/releases)
2. Esegui l'installatore e segui le istruzioni a schermo
3. Collega il tuo dispositivo MSR605 a una porta USB disponibile
4. Avvia l'applicazione dal Menu Start o dal collegamento sul desktop

### Linux/macOS
1. Assicurati di avere Python 3.8+ installato
2. Installa le dipendenze richieste:
   ```bash
   pip install -r requirements.txt
   ```
3. Avvia l'applicazione:
   ```bash
   python main.py
   ```

## Per Iniziare

### Connessione del Dispositivo
1. Collega il tuo dispositivo MSR605 al computer utilizzando il cavo USB
2. L'applicazione dovrebbe rilevare automaticamente il dispositivo
3. La barra di stato mostrerà "Dispositivo Connesso" in caso di successo

### Interfaccia Principale
- **Visualizzazione Dati Carta**: Mostra i dati letti dalla carta
- **Selezione Tracce**: Sceggi quali tracce leggere/scrivere (1, 2 e/o 3)
- **Pulsanti Azione**: Funzioni di Lettura, Scrittura e Cancellazione
- **Barra di Stato**: Mostra lo stato della connessione e i risultati delle operazioni

## Lettura delle Carte

1. Inserisci una carta a banda magnetica nel lettore
2. Fai clic sul pulsante "Leggi"
3. I dati della carta verranno visualizzati nella finestra principale
4. Per salvare i dati, fai clic su "File" > "Salva con nome..."

## Scrittura sulle Carte

1. Inserisci una carta a banda magnetica scrivibile nel dispositivo
2. Inserisci o incolla i dati che desideri scrivere nei campi delle tracce appropriate
3. Seleziona quali tracce vuoi scrivere
4. Fai clic sul pulsante "Scrivi"
5. La barra di stato mostrerà il risultato dell'operazione

## Configurazione

### Impostazioni del Dispositivo
- **Velocità di Trasmissione (Baud Rate)**: Regola la velocità di comunicazione (predefinita: 9600)
- **Parità**: Imposta la parità (Nessuna, Pari, Dispari, Marchio, Spazio)
- **Bit di Dati**: Imposta il numero di bit di dati (predefinito: 8)
- **Bit di Stop**: Imposta il numero di bit di stop (predefinito: 1)

### Impostazioni dell'Applicazione
- **Rilevamento Automatico Dispositivo**: Attiva/disattiva il rilevamento automatico del dispositivo
- **Avvia Ridotto a Icona**: Avvia l'applicazione ridotta nell'area di notifica
- **Salva Log**: Attiva la registrazione delle operazioni su file

## Risoluzione dei Problemi

### Problemi Comuni

#### Dispositivo Non Rilevato
- Assicurati che il dispositivo sia correttamente collegato alla porta USB
- Prova una porta USB diversa
- Verifica se il dispositivo è riconosciuto nel Gestione Dispositivi del tuo sistema
- Riavvia l'applicazione

#### Lettura/Scrittura Fallita
- Assicurati che la carta sia inserita correttamente
- Pulisci la banda magnetica della carta
- Verifica che la carta non sia protetta da scrittura
- Controlla che la configurazione delle tracce corrisponda al formato della carta

#### Arresto Improvviso dell'Applicazione
- Assicurati di avere l'ultima versione installata
- Controlla il file di log per i dettagli dell'errore
- Prova a reinstallare l'applicazione

## Supporto

Per ulteriore assistenza, puoi:
- Consultare le [Domande Frequenti](FAQ.md)
- Cercare o aprire una segnalazione su [GitHub](https://github.com/Nsfr750/MSR605/issues)
- Contattare nsfr750@yandex.com
