# Guida all'Installazione per MSR605 Lettore/Scrittore di Carte

## Prerequisiti

### Requisiti di Sistema
- **Sistema Operativo**: 
  - Windows 10/11 (64-bit)
  - Linux (Ubuntu 20.04 o successivi)
  - macOS 10.15 o successivi
- **Python**: 3.12 o superiore
- **Hardware**: Lettore MSR605

### Hardware Richiesto
- Lettore/Scrittore di Carte Magnetiche MSR605
- Adattatore USB-Seriale (se non incluso con MSR605)
- Carte a banda magnetica compatibili (ISO 7813)

## Passaggi di Installazione

### 1. Installazione di Python
1. Scarica Python 3.12+ dal [sito ufficiale di Python](https://www.python.org/downloads/)
2. Durante l'installazione, assicurati che "Aggiungi Python a PATH" sia selezionato
3. Verifica l'installazione:
   ```bash
   python --version
   pip --version
   ```

### 2. Clona il Repository
```bash
git clone https://github.com/Nsfr750/MSR605.git
cd MSR605
```

### 3. Ambiente Virtuale (Consigliato)
```bash
# Crea un ambiente virtuale
python -m venv venv

# Attiva l'ambiente virtuale
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### 4. Installa le Dipendenze
```bash
pip install -r requirements.txt
```

### 5. Configurazione Hardware
1. Collega l'MSR605 al computer tramite USB/Seriale
2. Installa eventuali driver del dispositivo necessari
3. Verifica il riconoscimento del dispositivo:
   ```bash
   python -m serial.tools.list_ports
   ```

### 6. Avvia l'Applicazione
```bash
python GUI.py
```

## Risoluzione dei Problemi
- Assicurati che tutte le dipendenze siano installate
- Controlla le connessioni della porta seriale
- Verifica la compatibilità della versione di Python
- Consulta le [Issue di GitHub](https://github.com/Nsfr750/MSR605/issues) per problemi noti

## Disinstallazione
```bash
# Disattiva l'ambiente virtuale
deactivate

# Rimuovi la directory del progetto
rm -rf MSR605
```

## Supporto
Per problemi di installazione, contatta nsfr750@yandex.com o apri una issue su GitHub.
