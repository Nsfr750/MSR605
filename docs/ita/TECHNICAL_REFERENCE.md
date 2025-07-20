# Riferimento Tecnico per MSR605 Lettore/Scrittore di Carte

## Panoramica dell'Architettura

### Componenti del Sistema
- **Modulo GUI**: `GUI.py`
- **Interfaccia Lettore Carte**: `cardReader.py`
- **Gestione Database**: SQLite integrato
- **Controllo Versione**: `version.py`
- **Gestione Sponsor**: `sponsor.py`
- **Informazioni**: `about.py`

## Progettazione del Software

### Principi di Progettazione
- Architettura modulare
- Separazione delle responsabilità
- Alta coesione
- Basso accoppiamento

### Responsabilità dei Moduli

#### Modulo GUI
- Gestione dell'interazione utente
- Gestione delle finestre
- Elaborazione degli eventi

#### Modulo Lettore Carte
- Comunicazione con l'hardware
- Lettura/scrittura a basso livello
- Gestione degli errori
- Elaborazione dei dati delle tracce

#### Modulo Database
- Persistenza dei dati
- Operazioni CRUD
- Gestione delle query

## Protocolli di Comunicazione

### Comunicazione Seriale
- Velocità di trasmissione: 9600 baud
- Bit di dati: 8
- Bit di stop: 1
- Parità: Nessuna
- Controllo di flusso: Nessuno

## Supporto dei Formati di Carta

### ISO 7811

#### Panoramica
Lo standard ISO 7811 definisce le caratteristiche fisiche e di registrazione per le carte a banda magnetica. L'implementazione supporta tutte e tre le tracce definite dallo standard.

#### Specifiche Tecniche

**Traccia 1 (IATA - Alfanumerica)**
- **Capacità**: Fino a 79 caratteri
- **Densità**: 210 bpi (bit per pollice)
- **Caratteri Supportati**:
  - Lettere maiuscole (A-Z)
  - Numeri (0-9)
  - Caratteri speciali: spazio, ! " % & ' ( ) * + , - . / : ; < = > ?
- **Struttura**:
  ```
  %[codice formato][numero conto primario]^[cognome]/[nome]^[data scadenza][codice servizio][dati discrezionali]?
  ```

**Traccia 2 (ABA - Numerica)**
- **Capacità**: Fino a 40 caratteri
- **Densità**: 75 bpi
- **Caratteri Supportati**: Solo numeri (0-9) e carattere di separatore '='
- **Struttura**:
  ```
  ;[numero conto primario]=[data scadenza][codice servizio][dati discrezionali]?
  ```

**Traccia 3 (THRIFT - Numerica)**
- **Capacità**: Fino a 107 caratteri
- **Densità**: 210 bpi
- **Utilizzo**: Principalmente per transazioni finanziarie e aggiornamenti

### ISO 7813

#### Panoramica
ISO 7813 è un sottoinsieme specifico di ISO 7811 progettato per le carte di transazione finanziaria.

#### Differenze Chiave da ISO 7811

**Traccia 1**
- **Codice Formato**: Deve essere 'B' (banking)
- **Lunghezze Fisse**:
  - Codice Paese: 3 caratteri
  - Nome: 2-26 caratteri
  - Data di Scadenza: 4 caratteri (YYMM)
- **Caratteri Non Consentiti**: ^ = ?

**Traccia 2**
- **Struttura Rigida**:
  - Primo Separatore: ';'
  - Secondo Separatore: '='
  - Carattere Finale: '?'
  
#### Validazione Aggiuntiva
- Verifica del codice di controllo (LRC)
- Validazione della data di scadenza
- Verifica del codice di servizio

### Implementazione

#### Classi Principali

**`CardFormat` (Classe Base Astratta)**
```python
class CardFormat(ABC):
    @abstractmethod
    def validate_track1(self, data: str) -> bool:
        pass
        
    @abstractmethod
    def validate_track2(self, data: str) -> bool:
        pass
        
    @abstractmethod
    def validate_track3(self, data: str) -> bool:
        pass
```

**`ISO7811Format`**
Implementa la validazione per lo standard ISO 7811 con regole generiche.

**`ISO7813Format`**
Estende `ISO7811Format` con regole aggiuntive specifiche per le transazioni finanziarie.

#### Gestione della Selezione del Formato
Il formato può essere impostato manualmente o rilevato automaticamente in base al contenuto delle tracce.

### Errori Comuni
1. **Formato Non Riconosciuto**: Verificare che i dati corrispondano a uno degli standard supportati
2. **Caratteri Non Validi**: Utilizzare solo i caratteri consentiti per la traccia specifica
3. **Lunghezza Eccessiva**: Rispettare i limiti di lunghezza per ciascuna traccia
4. **Formato Data Non Valido**: Utilizzare il formato YYMM per le date

### Best Practice
1. Utilizzare sempre la validazione prima della scrittura
2. Implementare il rilevamento automatico del formato quando possibile
3. Fornire messaggi di errore chiari per gli utenti finali
4. Registrare i tentativi di scrittura non validi a scopo di audit

## Protocolli di Comunicazione

### Comunicazione Seriale
- Velocità di trasmissione: 9600 baud
- Bit di dati: 8
- Bit di stop: 1
- Parità: Nessuna
- Controllo di flusso: Nessuno
- Traccia 2: formato ABA
- Traccia 3: formato personalizzato/esteso

## Metriche di Prestazione

### Velocità di Lettura/Scrittura
- Tempo medio di lettura: <500ms
- Tempo medio di scrittura: <1000ms
- Numero massimo di tracce: 3

### Utilizzo delle Risorse
- Memoria occupata: <100MB
- Utilizzo CPU: Da basso a moderato
- Spazio su disco: <500MB

## Gestione degli Errori

### Categorie di Errori
- Errori hardware
- Errori di comunicazione
- Errori di analisi dati
- Errori del database

### Registrazione Errori
- Timestamp
- Tipo di errore
- Descrizione dettagliata
- Soluzione suggerita

## Considerazioni sulla Sicurezza

### Protezione dei Dati
- Nessun dato della carta viene memorizzato senza consenso
- Database crittografato (opzionale)
- Politiche di conservazione dati configurabili

### Conformità
- Considerazioni sul GDPR
- Linee guida PCI DSS
- Principi di minimizzazione dei dati

## Estensibilità

### Architettura a Plugin
- Supporto per parser di tracce personalizzati
- Backend database estensibili
- Interfacce hardware configurabili

## Ambiente di Sviluppo

### Strumenti Consigliati
- Python 3.12+
- Visual Studio Code
- PyCharm
- Git
- Ambiente virtuale

### Estensioni Consigliate
- Python
- Pylance
- GitLens
- Markdown All in One

## Compilazione e Distribuzione

### Processo di Compilazione
- Utilizza `pyinstaller` per l'eseguibile
- Crea installer specifici per piattaforma
- Firma gli eseguibili

### Integrazione Continua
- GitHub Actions
- Test automatizzati
- Controlli di compatibilità delle versioni

## API ed Estensibilità

### Metodi Pubblici
- `read_card()`
- `write_card()`
- `decode_track()`
- `export_database()`

### Opzioni di Configurazione
- Impostazioni hardware
- Preferenze del database
- Regole di decodifica
- Personalizzazione dell'interfaccia utente

## Roadmap e Sviluppo Futuro
- Analisi delle carte con machine learning
- Sincronizzazione cloud
- Supporto multilingua
- Compatibilità hardware avanzata
