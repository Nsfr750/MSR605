"""
Voice command utilities for MSR605 application.

This module provides functionality for managing and displaying
voice command help in different languages.
"""

import json
import os
from typing import Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .language_manager import LanguageManager

class VoiceCommandHelper:
    def __init__(self, language_manager: 'LanguageManager' = None, lang_dir: str = "lang"):
        """Initialize the voice command helper with language manager and directory.
        
        Args:
            language_manager: The application's language manager
            lang_dir: Directory containing language files
        """
        self.lang_dir = lang_dir
        self.language_manager = language_manager
        self.current_lang = "en"  # Default language
        self.translations = {}
        self._load_translations()

    def _load_translations(self) -> None:
        """Load all available language translations."""
        try:
            for filename in os.listdir(self.lang_dir):
                if filename.endswith('.json'):
                    lang_code = os.path.splitext(filename)[0]
                    with open(os.path.join(self.lang_dir, filename), 'r', encoding='utf-8') as f:
                        self.translations[lang_code] = json.load(f)
        except Exception as e:
            print(f"Error loading voice command translations: {e}")

    def set_language(self, lang_code: str) -> bool:
        """Set the current language for voice commands."""
        if lang_code in self.translations:
            self.current_lang = lang_code
            return True
        return False

    def tr(self, key: str, default: str = None, **kwargs) -> str:
        """Translate a string using the language manager if available."""
        if self.language_manager and hasattr(self.language_manager, 'translate'):
            return self.language_manager.translate(key, **kwargs)
        return default or key

    def get_help_text(self) -> str:
        """Get the help text for voice commands in the current language."""
        try:
            # Get translations for the help text using the correct keys
            title = self.tr("voice_commands.help.title", "Voice Commands Help")
            description = self.tr("voice_commands.help.description", 
                               "You can control the application using the following voice commands:")
            note = self.tr("voice_commands.help.note", 
                         "Note: Voice control must be enabled in the Voice menu.")
            
            # Get the commands from the current language or fall back to English
            commands = []
            try:
                # First try to get from the nested structure
                if (self.current_lang in self.translations and 
                    "voice_commands" in self.translations[self.current_lang] and
                    "help" in self.translations[self.current_lang]["voice_commands"] and
                    "commands" in self.translations[self.current_lang]["voice_commands"]["help"]):
                    
                    commands = self.translations[self.current_lang]["voice_commands"]["help"]["commands"]
                
                # Fall back to English if no commands found in current language
                if not commands and ("en" in self.translations and 
                                   "voice_commands" in self.translations["en"] and
                                   "help" in self.translations["en"]["voice_commands"] and
                                   "commands" in self.translations["en"]["voice_commands"]["help"]):
                    
                    commands = self.translations["en"]["voice_commands"]["help"]["commands"]
            except (KeyError, TypeError) as e:
                logger.warning(f"Error accessing voice commands: {str(e)}")
            
            # Build the help text
            help_lines = []
            
            # Add title and underline
            if title:
                help_lines.append(title)
                help_lines.append("=" * len(title))
                help_lines.append("")
            
            # Add description
            if description:
                help_lines.append(description)
                help_lines.append("")
            
            # Add commands
            if commands:
                for cmd in commands:
                    if isinstance(cmd, dict) and "command" in cmd and "description" in cmd:
                        help_lines.append(f"• {cmd['command']}: {cmd['description']}")
                help_lines.append("")  # Add a blank line after commands
            
            # Add note if available
            if note:
                help_lines.append(note)
            
            # Join all lines with newlines and return
            return "\n".join(line for line in help_lines if line is not None)
            
        except Exception as e:
            logger.error(f"Error generating help text: {str(e)}", exc_info=True)
            # Fallback to a simple error message
            return "Error: Could not load voice command help. Please check the logs for more details."

    def get_available_languages(self) -> List[str]:
        """Get a list of available language codes."""
        return list(self.translations.keys())

# Global instance that will be initialized with the language manager
_voice_command_helper = None

def init_voice_commands(language_manager):
    """Initialize the voice command helper with the language manager.
    
    This should be called once at application startup.
    """
    global _voice_command_helper
    _voice_command_helper = VoiceCommandHelper(language_manager=language_manager)

def get_voice_command_help() -> str:
    """Get the voice command help text in the current language."""
    if _voice_command_helper is None:
        # Lazy initialization as fallback
        from .language_manager import get_language_manager
        init_voice_commands(get_language_manager())
    return _voice_command_helper.get_help_text()

def set_voice_command_language(lang_code: str) -> bool:
    """Set the language for voice command help."""
    if _voice_command_helper is None:
        return False
    return _voice_command_helper.set_language(lang_code)

def get_available_languages() -> List[str]:
    """Get a list of available language codes for voice commands."""
    if _voice_command_helper is None:
        return []
    return _voice_command_helper.get_available_languages()
