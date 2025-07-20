# MSR605 Lettore/Scrittore di Carte - Documentazione API

Questo documento fornisce informazioni dettagliate sull'API del Lettore/Scrittore di Carte MSR605 per gli sviluppatori che desiderano estendere o integrare l'applicazione.

## Indice
1. [Panoramica](#panoramica)
2. [Moduli Principali](#moduli-principali)
3. [Comunicazione con il Dispositivo](#comunicazione-con-il-dispositivo)
4. [Operazioni sulle Carte](#operazioni-sulle-carte)
5. [Formati Dati](#formati-dati)
6. [Gestione degli Errori](#gestione-degli-errori)
7. [Esempi](#esempi)

## Panoramica

L'API MSR605 fornisce un'interfaccia Python per interagire con i lettori/scrittori di bande magnetiche. L'API è progettata per essere facile da usare fornendo al contempo accesso a tutte le funzionalità del dispositivo.

## Moduli Principali

### `msr605`
Il modulo principale che contiene le funzionalità di base.

#### Classe `MSR605`
```python
class MSR605:
    def __init__(self, port=None, baudrate=9600, timeout=1):
        """Inizializza la connessione al dispositivo MSR605.
        
        Args:
            port (str, opzionale): Nome della porta seriale. Se None, tenta il rilevamento automatico.
            baudrate (int, opzionale): Velocità di comunicazione. Default a 9600.
            timeout (int, opzionale): Timeout di lettura in secondi. Default a 1.
        """
        pass
    
    def connect(self):
        """Stabilisce la connessione con il dispositivo."""
        pass
    
    def disconnect(self):
        """Chiude la connessione con il dispositivo."""
        pass
    
    def is_connected(self):
        """Verifica se il dispositivo è connesso.
        
        Returns:
            bool: True se connesso, False altrimenti.
        """
        pass
    
    def read_card(self, tracks=[1, 2, 3]):
        """Legge i dati da una carta a banda magnetica.
        
        Args:
            tracks (list, opzionale): Lista delle tracce da leggere (1, 2, 3). Di default legge tutte le tracce.
            
        Returns:
            dict: Dizionario contenente i dati delle tracce con i numeri di traccia come chiavi.
        """
        pass
    
    def write_card(self, track_data, verify=True):
        """Scrive dati su una carta a banda magnetica.
        
        Args:
            track_data (dict): Dizionario con i numeri di traccia come chiavi e i dati come valori.
            verify (bool, opzionale): Se verificare i dati scritti. Default a True.
            
        Returns:
            bool: True se la scrittura è avvenuta con successo, False altrimenti.
        """
        pass
```

## Comunicazione con il Dispositivo

### Protocollo Seriale

#### Comandi
| Comando | Descrizione | Formato |
|---------|-------------|---------|
| `ESC e` | Resetta il dispositivo | `\x1be` |
| `ESC s` | Leggi carta | `\x1bs` |
| `ESC w` | Scrivi carta | `\x1bw` |
| `ESC x` | Imposta livello di sicurezza | `\x1bx` |

#### Risposte
| Risposta | Descrizione |
|----------|-------------|
| `\x1b1` | Comando eseguito con successo |
| `\x1b2` | Comando fallito |
| `\x1b3` | Nessuna carta presente |
| `\x1b4` | Errore di protezione in scrittura |

## Operazioni sulle Carte

### Lettura Dati
```python
from msr605 import MSR605

# Inizializza e connetti al dispositivo
device = MSR605()
device.connect()

# Leggi tutte le tracce
data = device.read_card()
print(f"Traccia 1: {data.get(1, 'Nessun dato')}")
print(f"Traccia 2: {data.get(2, 'Nessun dato')}")
print(f"Traccia 3: {data.get(3, 'Nessun dato')}")

# Leggi tracce specifiche
data = device.read_card(tracks=[1, 2])

# Disconnetti
device.disconnect()
```

### Scrittura Dati
```python
from msr605 import MSR605

# Inizializza e connetti al dispositivo
device = MSR605()
device.connect()

# Prepara i dati delle tracce
track_data = {
    1: "%B1234567890123456^INTESTATARIO/NOME^25121010000000000000000000000000000?",
    2: ";1234567890123456=25121010000000000000?",
    3: ""  # Traccia 3 vuota
}

# Scrivi sulla carta
success = device.write_card(track_data)
print(f"Scrittura {'riuscita' if success else 'fallita'}")

# Disconnetti
device.disconnect()
```

## Formati Dati

### Formati delle Tracce
- **Traccia 1 (IATA)**: Fino a 79 caratteri alfanumerici
- **Traccia 2 (ABA)**: Fino a 40 caratteri numerici
- **Traccia 3 (THRIFT)**: Fino a 107 caratteri numerici

### Caratteri Speciali
| Carattere | Descrizione |
|-----------|-------------|
| `%` | Carattere di inizio (Traccia 1) |
| `;` | Carattere di inizio (Tracce 2 e 3) |
| `?` | Carattere di fine |
| `^` | Separatore (Traccia 1) |
| `=` | Separatore (Traccia 2) |
| `\\` | Carattere di escape |

## Gestione degli Errori

### Eccezioni
| Eccezione | Descrizione |
|-----------|-------------|
| `MSR605Error` | Eccezione base per tutti gli errori MSR605 |
| `MSR605ConnectionError` | Errori relativi alla connessione |
| `MSR605CommandError` | Errori nell'esecuzione dei comandi |
| `MSR605CardError` | Errori nelle operazioni sulla carta |

### Esempio
```python
from msr605 import MSR605, MSR605Error

try:
    device = MSR605()
    device.connect()
    data = device.read_card()
    print(data)
except MSR605Error as e:
    print(f"Errore: {e}")
finally:
    if 'device' in locals():
        device.disconnect()
```

## Esempi

### Utilizzo di Base
```python
from msr605 import MSR605

def main():
    try:
        # Inizializza e connetti
        device = MSR605()
        print("Connessione al dispositivo in corso...")
        device.connect()
        
        if not device.is_connected():
            print("Impossibile connettersi al dispositivo")
            return
```

### Lettura Avanzata
```python
from msr605 import MSR605

def read_specific_tracks():
    try:
        device = MSR605()
        device.connect()
        
        # Leggi solo le tracce 1 e 2
        data = device.read_card(tracks=[1, 2])
        
        # Elabora i dati
        for track_num, track_data in data.items():
            print(f"Traccia {track_num}: {track_data}")
            
    except Exception as e:
        print(f"Errore durante la lettura: {e}")
    finally:
        if 'device' in locals():
            device.disconnect()

if __name__ == "__main__":
    read_specific_tracks()
```

### Scrittura Avanzata
```python
from msr605 import MSR605

def write_custom_data():
    try:
        device = MSR605()
        device.connect()
        
        # Dati personalizzati per la scrittura
        track_data = {
            1: "%TESTCARD^ESEMPIO/SCRITTURA^25123112345987654321?",
            2: ";1234567890123456=2512?"
        }
        
        # Scrivi senza verifica
        success = device.write_card(track_data, verify=False)
        print(f"Scrittura {'riuscita' if success else 'fallita'}")
        
    except Exception as e:
        print(f"Errore durante la scrittura: {e}")
    finally:
        if 'device' in locals():
            device.disconnect()

if __name__ == "__main__":
    write_custom_data()
```

### Gestione Avanzata degli Errori
```python
from msr605 import MSR605, MSR605Error, MSR605CardError, MSR605ConnectionError

def safe_card_operations():
    device = None
    try:
        device = MSR605()
        device.connect()
        
        # Prova a leggere la carta
        print("Leggo la carta...")
        data = device.read_card()
        
        # Stampa i dati letti
        for track_num in sorted(data.keys()):
            print(f"Traccia {track_num}: {data[track_num]}")
            
    except MSR605ConnectionError as e:
        print(f"Errore di connessione: {e}")
    except MSR605CardError as e:
        print(f"Errore nella lettura della carta: {e}")
    except MSR605Error as e:
        print(f"Errore generico: {e}")
    except Exception as e:
        print(f"Errore imprevisto: {e}")
    finally:
        if device and hasattr(device, 'is_connected') and device.is_connected():
            device.disconnect()
            print("Disconnesso dal dispositivo")

if __name__ == "__main__":
    safe_card_operations()
```

### Utilizzo in un'Applicazione GUI
```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QTextEdit, QWidget
from msr605 import MSR605

class CardReaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.device = MSR605()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Lettore Carte MSR605")
        self.setGeometry(100, 100, 600, 400)
        
        # Widget principali
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        
        # Pulsanti
        self.btn_connect = QPushButton("Connetti")
        self.btn_read = QPushButton("Leggi Carta")
        self.btn_clear = QPushButton("Pulisci")
        
        # Disabilita i pulsanti finché non si è connessi
        self.btn_read.setEnabled(False)
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_display)
        layout.addWidget(self.btn_connect)
        layout.addWidget(self.btn_read)
        layout.addWidget(self.btn_clear)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        # Connessioni
        self.btn_connect.clicked.connect(self.toggle_connection)
        self.btn_read.clicked.connect(self.read_card)
        self.btn_clear.clicked.connect(self.text_display.clear)
        
    def toggle_connection(self):
        try:
            if not self.device.is_connected():
                self.device.connect()
                self.btn_connect.setText("Disconnetti")
                self.btn_read.setEnabled(True)
                self.log("Dispositivo connesso")
            else:
                self.device.disconnect()
                self.btn_connect.setText("Connetti")
                self.btn_read.setEnabled(False)
                self.log("Dispositivo disconnesso")
        except Exception as e:
            self.log(f"Errore: {str(e)}")
    
    def read_card(self):
        try:
            if not self.device.is_connected():
                self.log("Errore: dispositivo non connesso")
                return
                
            self.log("Lettura carta in corso...")
            data = self.device.read_card()
            
            self.log("\nDati letti:")
            for track_num in sorted(data.keys()):
                self.log(f"\nTraccia {track_num}:")
                self.log(data[track_num])
                
        except Exception as e:
            self.log(f"Errore durante la lettura: {str(e)}")
    
    def log(self, message):
        self.text_display.append(str(message))
        self.text_display.verticalScrollBar().setValue(
            self.text_display.verticalScrollBar().maximum()
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CardReaderApp()
    window.show()
    sys.exit(app.exec())
```

### Gestione dei Dati Avanzata
```python
import json
from datetime import datetime
from msr605 import MSR605

class CardDataManager:
    def __init__(self, device):
        self.device = device
        self.data_history = []
    
    def read_and_save(self, description=""):
        """Legge i dati dalla carta e li salva nella cronologia."""
        try:
            if not self.device.is_connected():
                self.device.connect()
            
            data = self.device.read_card()
            
            # Aggiungi metadati
            entry = {
                'timestamp': datetime.now().isoformat(),
                'description': description,
                'data': data
            }
            
            self.data_history.append(entry)
            return entry
            
        except Exception as e:
            print(f"Errore durante la lettura: {e}")
            return None
    
    def save_to_file(self, filename):
        """Salva la cronologia dei dati su file JSON."""
        try:
            with open(filename, 'w') as f:
                json.dump(self.data_history, f, indent=2)
            print(f"Dati salvati in {filename}")
            return True
        except Exception as e:
            print(f"Errore durante il salvataggio: {e}")
            return False
    
    def load_from_file(self, filename):
        """Carica la cronologia dei dati da file JSON."""
        try:
            with open(filename, 'r') as f:
                self.data_history = json.load(f)
            print(f"Caricati {len(self.data_history)} record da {filename}")
            return True
        except Exception as e:
            print(f"Errore durante il caricamento: {e}")
            return False

# Esempio di utilizzo
if __name__ == "__main__":
    device = MSR605()
    manager = CardDataManager(device)
    
    try:
        # Leggi una carta
        print("Leggo la carta...")
        entry = manager.read_and_save("Lettura di prova")
        
        if entry:
            print(f"Dati letti: {entry['data']}")
            
            # Salva su file
            manager.save_to_file("card_data.json")
            
            # Carica da file (esempio)
            # manager.load_from_file("card_data.json")
            
    finally:
        if device.is_connected():
            device.disconnect()
```

### Monitoraggio in Tempo Reale
```python
import time
from threading import Thread, Event
from queue import Queue
from msr605 import MSR605

class CardMonitor(Thread):
    def __init__(self, device, callback=None):
        super().__init__()
        self.device = device
        self.callback = callback
        self.running = Event()
        self.data_queue = Queue()
        self.setDaemon(True)
    
    def run(self):
        self.running.set()
        last_card = None
        
        while self.running.is_set():
            try:
                if not self.device.is_connected():
                    self.device.connect()
                
                # Leggi la carta
                data = self.device.read_card()
                
                # Verifica se è una nuova carta
                if data != last_card and any(data.values()):
                    last_card = data
                    if self.callback:
                        self.callback(data)
                    self.data_queue.put(data)
                
                time.sleep(0.5)  # Riduci il carico della CPU
                
            except Exception as e:
                print(f"Errore nel monitoraggio: {e}")
                time.sleep(2)  # Aspetta prima di riprovare
    
    def stop(self):
        self.running.clear()
        self.join()

def on_card_detected(card_data):
    print("\nNuova carta rilevata!")
    for track_num, track_data in card_data.items():
        if track_data:  # Mostra solo le tracce con dati
            print(f"Traccia {track_num}: {track_data}")
    print("-" * 50)

# Esempio di utilizzo
if __name__ == "__main__":
    device = MSR605()
    monitor = CardMonitor(device, on_card_detected)
    
    try:
        print("Monitoraggio carte attivo. Premi Ctrl+C per interrompere.")
        monitor.start()
        
        # Il thread principale resta in esecuzione
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nInterruzione del monitoraggio...")
        monitor.stop()
        if device.is_connected():
            device.disconnect()
        print("Monitoraggio terminato.")
```

### Gestione dei Profili di Scrittura
```python
import json
from msr605 import MSR605

class CardProfileManager:
    def __init__(self, profile_file="card_profiles.json"):
        self.profile_file = profile_file
        self.profiles = {}
        self.load_profiles()
    
    def load_profiles(self):
        """Carica i profili da file."""
        try:
            with open(self.profile_file, 'r') as f:
                self.profiles = json.load(f)
            print(f"Caricati {len(self.profiles)} profili da {self.profile_file}")
            return True
        except FileNotFoundError:
            print("Nessun file profili trovato. Verrà creato un nuovo file al salvataggio.")
            return False
        except Exception as e:
            print(f"Errore durante il caricamento dei profili: {e}")
            return False
    
    def save_profiles(self):
        """Salva i profili su file."""
        try:
            with open(self.profile_file, 'w') as f:
                json.dump(self.profiles, f, indent=2)
            print(f"Profili salvati in {self.profile_file}")
            return True
        except Exception as e:
            print(f"Errore durante il salvataggio dei profili: {e}")
            return False
    
    def add_profile(self, name, track_data, description=""):
        """Aggiungi un nuovo profilo."""
        self.profiles[name] = {
            'description': description,
            'track_data': track_data,
            'created_at': datetime.now().isoformat()
        }
        self.save_profiles()
    
    def get_profile(self, name):
        """Ottieni i dati di un profilo specifico."""
        return self.profiles.get(name, {}).get('track_data')
    
    def list_profiles(self):
        """Elenca tutti i profili disponibili."""
        return list(self.profiles.keys())

# Esempio di utilizzo
if __name__ == "__main__":
    # Crea un gestore di profili
    profile_manager = CardProfileManager()
    
    # Aggiungi alcuni profili di esempio
    profile_manager.add_profile(
        "Carta di Prova",
        {
            1: "%TESTCARD^PROFILO/DI PROVA^25123112345987654321?",
            2: ";1234567890123456=2512?"
        },
        "Profilo di prova per test"
    )
    
    # Elenca i profili disponibili
    print("Profili disponibili:")
    for profile in profile_manager.list_profiles():
        print(f"- {profile}")
    
    # Utilizza un profilo per scrivere su una carta
    device = MSR605()
    try:
        device.connect()
        
        # Ottieni i dati del profilo
        profile_name = "Carta di Prova"
        track_data = profile_manager.get_profile(profile_name)
        
        if track_data:
            print(f"\nScrittura profilo: {profile_name}")
            success = device.write_card(track_data)
            print(f"Scrittura {'riuscita' if success else 'fallita'}")
        else:
            print(f"Profilo '{profile_name}' non trovato")
            
    except Exception as e:
        print(f"Errore: {e}")
    finally:
        if device.is_connected():
            device.disconnect()
```
