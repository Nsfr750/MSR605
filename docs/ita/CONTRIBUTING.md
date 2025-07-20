# Contribuire a MSR605 Lettore/Scrittore di Carte

Grazie per il tuo interesse a contribuire al progetto MSR605 Lettore/Scrittore di Carte! Accogliamo con favore tutti i contributi, che si tratti di segnalazioni di bug, richieste di funzionalità, miglioramenti alla documentazione o contributi di codice.

## Indice

- [Codice di Condotta](#codice-di-condotta)
- [Come Contribuire](#come-contribuire)
  - [Segnalazione Bug](#segnalazione-bug)
  - [Richieste di Funzionalità](#richieste-di-funzionalità)
  - [Contributi di Codice](#contributi-di-codice)
- [Configurazione dello Sviluppo](#configurazione-dello-sviluppo)
  - [Prerequisiti](#prerequisiti)
  - [Configurazione dell'Ambiente](#configurazione-dellambiente)
- [Linee Guida per lo Sviluppo](#linee-guida-per-lo-sviluppo)
  - [Stile del Codice](#stile-del-codice)
  - [Test](#test)
  - [Documentazione](#documentazione)
  - [Controllo Versione](#controllo-versione)
- [Processo di Pull Request](#processo-di-pull-request)
- [Processo di Rilascio](#processo-di-rilascio)
- [Ottenere Aiuto](#ottenere-aiuto)
- [Licenza](#licenza)

## 👥 Codice di Condotta

Partecipando a questo progetto, accetti di rispettare il nostro [Codice di Condotta](CODE_OF_CONDUCT.md). Si prega di leggerlo prima di effettuare qualsiasi contributo.

## 🚀 Come Contribuire

### 🐛 Segnalazione Bug

1. **Controlla i Problemi Esistenti**: Prima di creare un nuovo problema, cerca tra le [issue](https://github.com/Nsfr750/MSR605/issues) per vedere se esiste già un problema simile.
2. **Crea una Nuova Issue**: Se hai trovato un bug, crea una nuova issue con i seguenti dettagli:
   - Un titolo chiaro e descrittivo (es. "Errore durante la lettura di una carta con caratteri speciali")
   - Passaggi per riprodurre il problema
   - Comportamento atteso vs. effettivo
   - Screenshot o messaggi di errore se applicabile
   - Le tue informazioni di sistema (sistema operativo, versione di Python, dettagli hardware)
   - Eventuali log rilevanti dalla directory `logs/`
   - Versione del firmware MSR605 (se nota)

### 💡 Richieste di Funzionalità

1. **Controlla le Funzionalità Esistenti**: Prima di richiedere una nuova funzionalità, controlla [ROADMAP.md](../ROADMAP.md) e le issue esistenti per vedere se è già pianificata.
2. **Crea una Richiesta di Funzionalità**: Se hai un'idea per una nuova funzionalità, crea una nuova issue con i seguenti dettagli:
   - Un titolo chiaro e descrittivo (es. "Aggiungi supporto per l'elaborazione in batch")
   - Una descrizione dettagliata della funzionalità e dei suoi vantaggi
   - Casi d'uso ed esempi
   - Eventuali implicazioni di sicurezza
   - Screenshot o mockup se applicabile
   - Riferimenti a standard rilevanti (es. ISO 7811, ISO 7813)

## 💻 Configurazione dello Sviluppo

### Prerequisiti

- Python 3.10+ (3.13.5 consigliato)
- Toolchain Rust (per il pacchetto cryptography)
- Git
- Hardware MSR605 (per i test hardware)
- Windows 10/11 (per sviluppo e test)

### Configurazione dell'Ambiente

1. **Fai un Fork e Clona il Repository**:
   ```bash
   git clone https://github.com/tuo-username/MSR605.git
   cd MSR605
   ```

2. **Configura un Ambiente Virtuale**:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Installa le Dipendenze**:
   ```bash
   # Installa le dipendenze di build
   pip install --upgrade pip setuptools wheel
   
   # Installa le dipendenze di sviluppo
   pip install -r requirements-dev.txt
   
   # Installa gli hook di pre-commit
   pre-commit install
   ```

4. **Configura gli Hook di Pre-commit**:
   ```bash
   pre-commit install
   ```

## 🛠 Linee Guida per lo Sviluppo

### Stile del Codice

- Segui [PEP 8](https://www.python.org/dev/peps/pep-0008/) per il codice Python
- Usa [Google Style Docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
- Lunghezza massima della riga: 88 caratteri (default di Black)
- Usa i type hint per tutte le funzioni e i metodi
- Ordina gli import usando `isort` (configurato in `pyproject.toml`)
- Formatta il codice usando `black` (configurato in `pyproject.toml`)
- Mantieni le funzioni piccole e mirate (preferibilmente < 50 righe)

### Test

- Scrivi test unitari per tutte le nuove funzionalità e correzioni di bug
- Usa `pytest` per i test
- Punta ad almeno l'80% di copertura dei test
- Inserisci i test nella directory `tests/`
- Esegui i test su più versioni di Python (3.10+)
- Esegui i test localmente prima di effettuare il push:
  ```bash
  # Esegui tutti i test
  pytest
  
  # Esegui i test con copertura
  pytest --cov=script --cov-report=term-missing
  
  # Esegui un file di test specifico
  pytest tests/test_card_reader.py -v
  ```

### Documentazione

- Aggiorna la documentazione pertinente quando aggiungi nuove funzionalità
- Segui lo stile di documentazione esistente
- Aggiungi docstring a tutte le funzioni e classi pubbliche
- Documenta tutti gli endpoint pubblici dell'API
- Aggiorna il file CHANGELOG.md con le modifiche significative
- Mantieni il file README.md aggiornato con le istruzioni di installazione e utilizzo

### Controllo Versione

1. **Crea un Branch per la Funzionalità**:
   ```bash
   git checkout -b feature/nome-della-tua-funzionalità
   ```

2. **Apporta le Tue Modifiche**:
   - Segui le linee guida di stile del codice
   - Aggiungi test per le nuove funzionalità
   - Aggiorna la documentazione se necessario

3. **Esegui i Controlli Prima del Commit**:
   ```bash
   # Esegui i linter
   black .
   isort .
   flake8
   
   # Esegui il controllo dei tipi
   mypy script/
   
   # Esegui i test
   pytest
   ```

4. **Esegui il Commit delle Tue Modifiche**:
   ```bash
   git add .
   git commit -m "feat: aggiungi la tua funzionalità"
   ```
   
   Usa i [messaggi di commit convenzionali](https://www.conventionalcommits.org/):
   - `feat:` per nuove funzionalità
   - `fix:` per correzioni di bug
   - `docs:` per modifiche alla documentazione
   - `style:` per modifiche di formattazione
   - `refactor:` per modifiche al codice che non correggono bug né aggiungono funzionalità
   - `test:` per aggiungere o modificare test
   - `chore:` per attività di manutenzione
   - `build:` per modifiche al sistema di build
   - `ci:` per modifiche alla configurazione CI
   - `perf:` per miglioramenti alle prestazioni
   - `revert:` per annullare commit

5. **Esegui il Push delle Tue Modifiche**:
   ```bash
   git push origin feature/nome-della-tua-funzionalità
   ```

6. **Crea una Pull Request**:
   - Vai al [repository originale](https://github.com/Nsfr750/MSR605)
   - Clicca su "New Pull Request"
   - Seleziona il tuo branch
   - Compila il template della PR
   - Richiedi una revisione ai manutentori

## Processo di Pull Request

1. Assicurati che il tuo codice sia aggiornato con il ramo `main`:
   ```bash
   git checkout main
   git pull upstream main
   git checkout feature/tua-funzionalità
   git rebase main
   ```

2. Risolvi eventuali conflitti e assicurati che tutti i test passino.

3. Spingi le tue modifiche al tuo fork:
   ```bash
   git push origin feature/tua-funzionalità --force-with-lease
   ```

4. Crea una Pull Request dal tuo fork al ramo `main` del repository principale.

5. Rispondi a eventuali feedback della revisione del codice e apporta le modifiche necessarie.

## Processo di Rilascio

1. **Preparazione del Rilascio**:
   - Assicurati che tutti i test siano verdi
   - Aggiorna il file CHANGELOG.md con le modifiche
   - Aggiorna la versione in `script/version.py` seguendo il versionamento semantico

2. **Crea un Tag di Rilascio**:
   ```bash
   git tag -a vX.Y.Z -m "Rilascio vX.Y.Z"
   git push origin vX.Y.Z
   ```

3. **Crea un Rilascio su GitHub**:
   - Vai a [Releases](https://github.com/Nsfr750/MSR605/releases)
   - Clicca su "Draft a new release"
   - Seleziona il tag appena creato
   - Inserisci un titolo e una descrizione del rilascio
   - Carica i file binari generati
   - Pubblica il rilascio

## Ottenere Aiuto

Se hai domande o hai bisogno di aiuto, puoi:

1. Controllare la [documentazione](https://github.com/Nsfr750/MSR605/wiki)
2. Aprire una [discussione](https://github.com/Nsfr750/MSR605/discussions)
3. Contattare i manutentori via email: [nsfr750@yandex.com](mailto:nsfr750@yandex.com)
4. Unirti al nostro [server Discord](https://discord.gg/BvvkUEP9)

## Licenza

Questo progetto è rilasciato sotto la licenza GPLv3. Vedere il file [LICENSE](../LICENSE) per i dettagli.
