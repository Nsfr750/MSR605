"""
Settings Manager for MSR605 Card Reader/Writer

This module provides a simple interface for managing application settings
using a JSON file stored in the config directory.
"""

import os
import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

class SettingsManager:
    """Manages application settings using a JSON file."""
    
    def __init__(self, config_dir: str = None, filename: str = "settings.json"):
        """Initialize the settings manager.
        
        Args:
            config_dir: Directory to store the settings file. If None, uses 'config' in the project root.
            filename: Name of the settings file.
        """
        self.logger = logging.getLogger(__name__)
        
        # Set up config directory
        if config_dir is None:
            # Default to project_root/config
            project_root = Path(__file__).parent.parent
            self.config_dir = project_root / "config"
        else:
            self.config_dir = Path(config_dir)
            
        # Create config directory if it doesn't exist
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up settings file path
        self.settings_file = self.config_dir / filename
        self.settings: Dict[str, Any] = {}
        
        # Default settings
        self.default_settings = {
            "auto_save": False,
            "allow_duplicates": False,
            "coercivity": "hi",
            "geometry": None,
            "windowState": None,
            "language": "en",
            "theme": "dark",
            "recent_files": [],
            "max_recent_files": 10,
        }
        
        # Load settings
        self.load()
    
    def load(self) -> None:
        """Load settings from the JSON file."""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
                self.logger.info(f"Loaded settings from {self.settings_file}")
            else:
                self.logger.info("No settings file found, using defaults")
                self.settings = self.default_settings.copy()
                self.save()
        except Exception as e:
            self.logger.error(f"Error loading settings: {e}")
            self.settings = self.default_settings.copy()
    
    def save(self) -> None:
        """Save current settings to the JSON file."""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, sort_keys=True)
            self.logger.debug(f"Saved settings to {self.settings_file}")
        except Exception as e:
            self.logger.error(f"Error saving settings: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value by key.
        
        Args:
            key: The setting key to retrieve.
            default: Default value if key doesn't exist.
            
        Returns:
            The setting value or default if not found.
        """
        return self.settings.get(key, self.default_settings.get(key, default))
    
    def set(self, key: str, value: Any, auto_save: bool = True) -> None:
        """Set a setting value.
        
        Args:
            key: The setting key to set.
            value: The value to set.
            auto_save: If True, save settings after updating.
        """
        self.settings[key] = value
        if auto_save:
            self.save()
    
    def remove(self, key: str, auto_save: bool = True) -> None:
        """Remove a setting.
        
        Args:
            key: The setting key to remove.
            auto_save: If True, save settings after updating.
        """
        if key in self.settings:
            del self.settings[key]
            if auto_save:
                self.save()
    
    def reset_to_defaults(self) -> None:
        """Reset all settings to their default values."""
        self.settings = self.default_settings.copy()
        self.save()


# Global instance for easy access
settings_manager = SettingsManager()
