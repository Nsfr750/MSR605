"""
Language management
"""

from typing import Dict, List, Optional, Any
from PyQt6.QtCore import QObject, pyqtSignal, QSettings


class LanguageManager(QObject):
    """
    Manages application language settings and translations.
    """

    # Signal emitted when language changes
    language_changed = pyqtSignal(str)  # language_code

    def __init__(self, default_lang: str = "en"):
        """
        Initialize the language manager.

        Args:
            default_lang: Default language code (e.g., 'en', 'it')
        """
        super().__init__()
        print("Initializing LanguageManager...")
        print(f"QSettings organization: MSR605, application: MSR605")
        self.settings = QSettings("MSR605", "MSR605")
        print(f"Settings file: {self.settings.fileName()}")
        self._current_lang = self.settings.value("language", default_lang)
        print(f"Current language from settings: {self._current_lang}")
        self._translations = {}
        self._load_translations()
        print("LanguageManager initialized")

    @property
    def current_language(self) -> str:
        """Get the current language code."""
        return self._current_lang

    @property
    def available_languages(self) -> Dict[str, str]:
        """Get a dictionary of available language codes and their display names."""
        return {
            "en": "English",
            "it": "Italiano",
            # Add more languages here as they become available
        }

    def _load_translations(self):
        """Load translations from the translations module."""
        from script.translations import TRANSLATIONS

        self._translations = TRANSLATIONS

    def set_language(self, lang_code: str) -> bool:
        """
        Set the application language.

        Args:
            lang_code: Language code to set (e.g., 'en', 'it')

        Returns:
            bool: True if language was changed, False otherwise
        """
        if lang_code not in self.available_languages:
            return False

        if lang_code != self._current_lang:
            self._current_lang = lang_code
            self.settings.setValue("language", lang_code)
            self.language_changed.emit(lang_code)
            return True
        return False

    def translate(self, key: str, **kwargs) -> str:
        """
        Get a translated string for the given key.

        Args:
            key: Translation key (can contain dots for nested keys, e.g., 'edit_menu.empty_trash')
            **kwargs: Format arguments for the translation string

        Returns:
            str: Translated string or the key if not found
        """
        try:

            def get_nested(d, keys):
                """Helper to get nested dictionary values using dot notation."""
                for k in keys.split("."):
                    if not isinstance(d, dict):
                        return None
                    d = d.get(k)
                return d

            # Try to get translation for current language
            lang_dict = self._translations.get(self._current_lang, {})
            translation = get_nested(lang_dict, key) or lang_dict.get(key, "")

            # If not found, fall back to English
            if not translation and self._current_lang != "en":
                en_dict = self._translations.get("en", {})
                translation = get_nested(en_dict, key) or en_dict.get(key, key)

            # Format the string if there are any kwargs and it's a string
            if translation and isinstance(translation, str) and kwargs:
                try:
                    return translation.format(**kwargs)
                except (KeyError, ValueError):
                    return translation

            return translation or key

        except Exception as e:
            print(f"Translation error for key '{key}': {e}")
            return key
