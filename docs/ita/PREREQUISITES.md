# Prerequisiti

Prima di poter utilizzare questo progetto, assicurati di avere installato quanto segue sul tuo sistema:

## Requisiti di Sistema

- Python 3.8 o superiore
- pip (installatore di pacchetti Python)
- Git

## Dipendenze Python

Installa i pacchetti Python richiesti eseguendo:

```bash
pip install -r requirements.txt
```

## Requisiti Hardware (se applicabile)

- Lettore/Codificatore di Carte a Banda Magnetica MSR605
- Porta USB per la connessione del dispositivo

## Configurazione dell'Ambiente

1. Clona il repository:
   ```bash
   git clone https://github.com/Nsfr750/MSR605.git
   cd MSR605
   ```

2. (Facoltativo) Crea e attiva un ambiente virtuale:
   ```bash
   # Su Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Su Unix o MacOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Installa le dipendenze di sviluppo:
   ```bash
   pip install -r requirements-dev.txt
   ```

## Configurazione

1. Copia il file di configurazione di esempio e aggiornalo con le tue impostazioni:
   ```bash
   cp config.example.ini config.ini
   ```

2. Modifica il file `config.ini` con le tue impostazioni preferite.

## Verifica dell'Installazione

Esegui la suite di test per verificare che tutto funzioni correttamente:

```bash
pytest tests/
```

## Risoluzione dei Problemi

- Se incontri problemi di autorizzazione, prova a eseguire il comando con `sudo` (Unix/Linux/MacOS) o come Amministratore (Windows)
- Assicurati che tutti i driver USB necessari siano installati per il tuo dispositivo MSR605
- Consulta la guida [Risoluzione dei Problemi](TROUBLESHOOTING.md) per problemi comuni e soluzioni
