"""
Update checking functionality for the MSR605 application.
"""
import logging
import time
from typing import Optional, Tuple, Callable, Dict, Any

# Import local modules
from . import version
import requests
import json
from pathlib import Path
import os

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QProgressBar, QMessageBox,
    QDialogButtonBox, QTextEdit, QApplication
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

# Get the application directory
APP_DIR = Path(__file__).parent.parent
UPDATES_FILE = APP_DIR / 'config' / 'updates.json'

# Configure logger
logger = logging.getLogger(__name__)

class UpdateChecker(QDialog):
    """Handles checking for application updates."""
    
    def __init__(self, parent=None, current_version: str = version.get_version(), config_path: Optional[Path] = None):
        """Initialize the update checker.
        
        Args:
            parent: Parent widget for this dialog.
            current_version: The current version of the application.
            config_path: Path to the configuration file (optional).
        """
        super().__init__(parent)
        self.current_version = current_version
        self.config_path = config_path or UPDATES_FILE
        self.update_available = False
        self.latest_version = ""
        self.release_notes = ""
        self.download_url = ""
        
        self.setWindowTitle("Check for Updates")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Status label
        self.status_label = QLabel("Checking for updates...")
        layout.addWidget(self.status_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        layout.addWidget(self.progress_bar)
        
        # Buttons
        self.button_box = QDialogButtonBox()
        self.update_button = QPushButton("Update Now")
        self.update_button.setVisible(False)
        self.update_button.clicked.connect(self._open_download)
        
        self.later_button = QPushButton("Remind Me Later")
        self.later_button.setVisible(False)
        self.later_button.clicked.connect(self.reject)
        
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.accept)
        
        self.button_box.addButton(self.update_button, QDialogButtonBox.ButtonRole.AcceptRole)
        self.button_box.addButton(self.later_button, QDialogButtonBox.ButtonRole.RejectRole)
        self.button_box.addButton(self.close_button, QDialogButtonBox.ButtonRole.RejectRole)
        
        layout.addWidget(self.button_box)
        
        # Start the update check in a separate thread
        self._start_update_check()
    
    def _start_update_check(self):
        """Start the update check in a separate thread."""
        self.thread = UpdateCheckThread(self.current_version, self.config_path)
        self.thread.finished.connect(self._on_update_check_complete)
        self.thread.error_occurred.connect(self._on_update_check_error)
        self.thread.start()
    
    def _on_update_check_complete(self, result):
        """Handle completion of the update check."""
        self.progress_bar.setRange(0, 1)  # Reset progress bar
        self.progress_bar.setValue(1)
        
        update_available, latest_version, release_notes, download_url = result
        self.update_available = update_available
        self.latest_version = latest_version
        self.release_notes = release_notes
        self.download_url = download_url
        
        if update_available:
            self.status_label.setText(
                f"A new version {latest_version} is available!\n\n"
                f"Current version: {self.current_version}\n"
                f"New version: {latest_version}"
            )
            
            # Show release notes if available
            if release_notes:
                notes_dialog = QDialog(self)
                notes_dialog.setWindowTitle(f"What's New in Version {latest_version}")
                notes_dialog.setMinimumSize(500, 300)
                
                layout = QVBoxLayout(notes_dialog)
                text_edit = QTextEdit()
                text_edit.setReadOnly(True)
                text_edit.setMarkdown(release_notes)
                
                button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
                button_box.accepted.connect(notes_dialog.accept)
                
                layout.addWidget(QLabel(f"<h3>What's New in Version {latest_version}</h3>"))
                layout.addWidget(text_edit)
                layout.addWidget(button_box)
                
                notes_dialog.exec()
            
            self.update_button.setVisible(True)
            self.later_button.setVisible(True)
            self.close_button.setVisible(False)
        else:
            self.status_label.setText("You are using the latest version.")
            self.close_button.setVisible(True)
    
    def _on_update_check_error(self, error_message):
        """Handle errors during the update check."""
        self.progress_bar.setRange(0, 1)  # Reset progress bar
        self.progress_bar.setValue(1)
        
        self.status_label.setText(f"Error checking for updates: {error_message}")
        self.close_button.setVisible(True)
    
    def _open_download(self):
        """Open the download URL in the default web browser."""
        if self.download_url:
            import webbrowser
            webbrowser.open(self.download_url)
        self.accept()


class UpdateCheckThread(QThread):
    """Thread for performing the update check in the background."""
    
    finished = pyqtSignal(tuple)  # (update_available, latest_version, release_notes, download_url)
    error_occurred = pyqtSignal(str)  # error_message
    
    def __init__(self, current_version: str, config_path: Path):
        super().__init__()
        self.current_version = current_version
        self.config_path = config_path
    
    def run(self):
        """Run the update check."""
        try:
            self.config = self._load_config()
            self.update_url = "https://api.github.com/repos/Nsfr750/MSR605/releases/latest"
            result = check_for_updates_impl(self.current_version, self.config_path)
            self.finished.emit(result)
        except Exception as e:
            logger.exception("Error checking for updates")
            self.error_occurred.emit(str(e))
    
    def _load_config(self) -> dict:
        """Load the update configuration."""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading update config: {e}")
        return {
            'last_checked': None,
            'last_version': None,
            'dont_ask_until': None
        }
    
    def _save_config(self) -> None:
        """Save the update configuration."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving update config: {e}")
    
    def check_for_updates(self, parent: Optional[object] = None, force_check: bool = False) -> Tuple[bool, Optional[dict]]:
        """Check for available updates.
        
        Args:
            parent: Parent window for dialogs.
            force_check: If True, skip the cache and force a check.
            
        Returns:
            Tuple of (update_available, update_info)
        """
        try:
            logger.info("Checking for updates...")
            response = requests.get(self.update_url, timeout=10)
            response.raise_for_status()
            release = response.json()
            
            latest_version = release['tag_name'].lstrip('v')
            self.config['last_checked'] = release['published_at']
            self.config['last_version'] = latest_version
            self._save_config()
            
            if self._version_compare(latest_version, self.current_version) > 0:
                logger.info(f"Update available: {latest_version}")
                return True, {
                    'version': latest_version,
                    'url': release['html_url'],
                    'notes': release['body'],
                    'published_at': release['published_at']
                }
            else:
                logger.info("No updates available")
                return False, None
                
        except requests.RequestException as e:
            logger.error(f"Error checking for updates: {e}")
            return False, None
    
    def _version_compare(self, v1: str, v2: str) -> int:
        """Compare two version strings.
        
        Returns:
            1 if v1 > v2, -1 if v1 < v2, 0 if equal
        """
        def parse_version(v: str) -> list:
            return [int(x) for x in v.split('.')]
            
        try:
            v1_parts = parse_version(v1)
            v2_parts = parse_version(v2)
            
            # Pad with zeros if versions have different lengths
            max_len = max(len(v1_parts), len(v2_parts))
            v1_parts += [0] * (max_len - len(v1_parts))
            v2_parts += [0] * (max_len - len(v2_parts))
            
            for i in range(max_len):
                if v1_parts[i] > v2_parts[i]:
                    return 1
                elif v1_parts[i] < v2_parts[i]:
                    return -1
            return 0
            
        except (ValueError, AttributeError):
            # Fallback to string comparison if version format is invalid
            return (v1 > v2) - (v1 < v2)


def check_for_updates(parent=None, current_version: str = version.get_version(), force_check: bool = False) -> bool:
    """Check for application updates and show a dialog if an update is available.
    
    Args:
        parent: Parent window for dialogs.
        current_version: Current application version.
        force_check: If True, skip the cache and force a check.
        
    Returns:
        bool: True if an update is available and the user chose to update, False otherwise.
    """
    dialog = UpdateChecker(parent, current_version, UPDATES_FILE)
    return dialog.exec() == QDialog.DialogCode.Accepted


def check_for_updates_impl(current_version: str = version.get_version(), config_path: Path = UPDATES_FILE, force: bool = False) -> Tuple[bool, str, str, str]:
    """Check for updates.
    
    Args:
        current_version: The current version of the application.
        config_path: Path to the configuration file.
        force: If True, skip the cache and force a check.
        
    Returns:
        Tuple of (update_available, latest_version, release_notes, download_url)
    """
    # Check if we should use cached data
    if not force and _is_cache_valid(config_path):
        cached_data = _load_cached_data(config_path)
        if cached_data:
            latest_version = cached_data.get('latest_version', '')
            update_available = _is_newer_version(current_version, latest_version)
            return (
                update_available,
                latest_version,
                cached_data.get('release_notes', ''),
                cached_data.get('download_url', '')
            )
    
    # If we get here, we need to check for updates
    try:
        # In a real implementation, this would make an API call to check for updates
        # For now, we'll simulate a successful check with a random result
        import random
        if random.choice([True, False]):
            latest_version = f"{random.randint(1, 2)}.{random.randint(0, 9)}.{random.randint(0, 9)}"
            update_available = _is_newer_version(current_version, latest_version)
            release_notes = "## What's New\n\n- Bug fixes and performance improvements"
            download_url = "https://github.com/Nsfr750/MSR605/releases/latest"
            
            # Cache the result
            _cache_update_info(config_path, latest_version, release_notes, download_url)
            
            return (update_available, latest_version, release_notes, download_url)
        else:
            # No updates available
            _cache_no_updates(config_path)
            return (False, current_version, "", "")
            
    except Exception as e:
        logger.error(f"Error checking for updates: {e}")
        raise


def _load_cached_data(config_path: Path) -> dict:
    """Load cached update data."""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Ensure all required keys are present
            if all(k in data for k in ['last_checked', 'latest_version']):
                return data
    except (json.JSONDecodeError, OSError) as e:
        logger.error(f"Error loading cached update data: {e}")
    return {}


def _cache_update_info(config_path: Path, version: str, release_notes: str, download_url: str):
    """Cache update information."""
    import time
    data = {
        'last_checked': time.time(),
        'latest_version': version,
        'release_notes': release_notes,
        'download_url': download_url
    }
    _save_cache(config_path, data)


def _cache_no_updates(config_path: Path):
    """Cache the fact that no updates are available."""
    import time
    data = {
        'last_checked': time.time(),
        'latest_version': '',
        'release_notes': '',
        'download_url': ''
    }
    _save_cache(config_path, data)


def _save_cache(config_path: Path, data: dict):
    """Save data to the cache file."""
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except OSError as e:
        logger.error(f"Error saving cache: {e}")


def _is_cache_valid(config_path: Path) -> bool:
    """Check if the cache is valid."""
    try:
        with open(config_path, 'r') as f:
            data = json.load(f)
        
        # Get the last_checked value
        last_checked = data.get('last_checked')
        if not last_checked:
            return False
            
        # Handle both numeric timestamps and ISO 8601 strings
        if isinstance(last_checked, (int, float)):
            last_checked_ts = float(last_checked)
        elif isinstance(last_checked, str):
            # Try to parse ISO 8601 format
            from datetime import datetime
            try:
                dt = datetime.fromisoformat(last_checked.replace('Z', '+00:00'))
                last_checked_ts = dt.timestamp()
            except (ValueError, AttributeError):
                return False
        else:
            return False
            
        return last_checked_ts > time.time() - 86400  # 24 hours
    except (json.JSONDecodeError, OSError) as e:
        logger.error(f"Error checking cache validity: {e}")
    return False


def _is_newer_version(current_version: str = version.get_version(), new_version: str = "") -> bool:
    """Check if the given version is newer than the current version."""
    if not new_version:
        return False
        
    try:
        # Simple version comparison (assumes semantic versioning)
        current_parts = [int(part) for part in current_version.split('.')]
        new_parts = [int(part) for part in new_version.split('.')]
        
        # Pad with zeros if versions have different numbers of parts
        max_parts = max(len(current_parts), len(new_parts))
        current_parts.extend([0] * (max_parts - len(current_parts)))
        new_parts.extend([0] * (max_parts - len(new_parts)))
        
        # Compare each part
        for curr, new in zip(current_parts, new_parts):
            if new > curr:
                return True
            elif new < curr:
                return False
                
        return False  # Versions are equal
        
    except (ValueError, AttributeError):
        # If version parsing fails, do a simple string comparison
        return new_version > current_version


if __name__ == "__main__":
    # Example usage
    import sys
    
    app = QApplication(sys.argv)
    
    # Example: Check for updates
    check_for_updates(current_version=version.get_version())
    
    sys.exit(app.exec())
