"""
Voice control module for MSR605 Card Reader.
This module provides voice command functionality using speech recognition.
"""

import queue
import sys
import threading
import time
from typing import Callable, Dict, Optional, TYPE_CHECKING, Any

# Import speech recognition at module level
import speech_recognition as sr
from speech_recognition import (
    Recognizer,
    Microphone,
    UnknownValueError,
    RequestError,
    AudioData
)

# Check if speech recognition is available
try:
    # Test if we can create a recognizer and microphone
    test_recognizer = Recognizer()
    test_microphone = Microphone()
    SPEECH_RECOGNITION_AVAILABLE = True
except Exception as e:
    SPEECH_RECOGNITION_AVAILABLE = False
    logger.warning(f"Speech recognition not available: {e}")

from PyQt6.QtCore import QObject, pyqtSignal

from .logger import logger


class VoiceControl(QObject):
    """Handles voice recognition and command execution."""

    # Signal emitted when a command is recognized
    command_received = pyqtSignal(str)
    
    # Signal emitted when a command execution fails
    command_error = pyqtSignal(str)
    
    # Signal emitted when an unknown command is received
    command_unknown = pyqtSignal(str)

    def __init__(self, parent=None, language_manager=None):
        """Initialize the voice control system.
        
        Args:
            parent: The parent QObject
            language_manager: Optional language manager for translations and language settings
        """
        super().__init__(parent)
        
        # Store language manager reference
        self.language_manager = language_manager
        
        # Initialize command storage and control flags
        self.commands: Dict[str, Callable] = {}
        self.is_listening = False
        self.audio_queue = queue.Queue()
        self.stop_event = threading.Event()
        
        # Initialize speech recognition if available
        self.recognizer = None
        self.microphone = None
        
        if not SPEECH_RECOGNITION_AVAILABLE:
            logger.warning(
                "Speech recognition not available. Install with: pip install SpeechRecognition"
            )
            return
            
        try:
            # Import here to ensure proper scoping
            from speech_recognition import Recognizer, Microphone, AudioData
            
            self.recognizer = Recognizer()
            self.microphone = Microphone()
            
            # Configure recognizer settings
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
            self.recognizer.phrase_threshold = 0.3
            
            logger.info("Speech recognition initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize speech recognition: {e}", exc_info=True)
            self.recognizer = None
            self.microphone = None
        
        # Set default language for speech recognition
        self._current_language = self._get_language_code()
        logger.debug(f"Initialized voice control with language: {self._current_language}")

    def register_command(self, phrase: str, callback: Callable) -> None:
        """Register a voice command and its handler.

        Args:
            phrase: The phrase to recognize (case-insensitive)
            callback: Function to call when the phrase is recognized
        """
        self.commands[phrase.lower()] = callback

    def start_listening(self) -> None:
        """Start listening for voice commands in a background thread."""
        if not self.recognizer or not self.microphone:
            logger.error(
                "Speech recognition not available. Install SpeechRecognition package."
            )
            return

        if self.is_listening:
            logger.warning("Voice control is already active")
            return

        self.is_listening = True
        self.stop_event.clear()

        # Start the background thread
        self.listener_thread = threading.Thread(
            target=self._listen_loop, daemon=True, name="VoiceControlListener"
        )
        self.listener_thread.start()

        logger.info("Voice control started")

    def stop_listening(self) -> None:
        """Stop listening for voice commands."""
        if not self.is_listening:
            return

        self.is_listening = False
        self.stop_event.set()

        # Wait for the listener thread to finish
        if hasattr(self, "listener_thread"):
            self.listener_thread.join(timeout=2)

        logger.info("Voice control stopped")

    def _listen_loop(self) -> None:
        """Main listening loop running in a background thread."""
        try:
            # Import speech recognition modules inside the method
            import speech_recognition as sr
            
            if not SPEECH_RECOGNITION_AVAILABLE or self.recognizer is None or self.microphone is None:
                logger.error(
                    "Speech recognition is not available. "
                    "Please install the required package with: pip install SpeechRecognition pyaudio"
                )
                return

            logger.info("Starting voice recognition loop...")
            
            # Initial adjustment for ambient noise
            try:
                with self.microphone as source:
                    logger.debug("Adjusting for ambient noise...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
            except Exception as e:
                logger.error(f"Failed to adjust for ambient noise: {e}")
                return

            while not self.stop_event.is_set():
                try:
                    # Listen for audio input
                    audio = None
                    try:
                        with self.microphone as source:
                            logger.debug("Listening for voice command...")
                            try:
                                audio = self.recognizer.listen(
                                    source,
                                    timeout=2,
                                    phrase_time_limit=3
                                )
                            except sr.WaitTimeoutError:
                                # No speech detected within timeout, continue listening
                                continue
                            except Exception as e:
                                logger.debug(f"Listening error: {e}")
                                time.sleep(0.5)
                                continue

                        if audio is None:
                            continue

                        # Get current language code for recognition
                        language_code = self._get_language_code()
                        
                        # Recognize speech using Google's speech recognition
                        try:
                            text = self.recognizer.recognize_google(
                                audio,
                                language=language_code
                            ).lower()
                            
                            logger.info(f"Recognized speech: {text}")
                            self.command_received.emit(text)
                            self._process_command(text)

                        except sr.UnknownValueError:
                            logger.debug("Speech was unintelligible")
                        except sr.RequestError as e:
                            logger.error(
                                "Could not request results from Google Speech Recognition "
                                f"service: {e}"
                            )
                            time.sleep(5)  # Longer delay on API errors
                        except Exception as e:
                            logger.error(f"Error in speech recognition: {e}", exc_info=True)
                            time.sleep(1)

                    except Exception as e:
                        logger.error(f"Error in audio capture: {e}", exc_info=True)
                        time.sleep(1)  # Prevent tight loop on errors
                        
                except Exception as e:
                    logger.error(
                        f"Unexpected error in voice recognition loop: {e}",
                        exc_info=True
                    )
                    time.sleep(1)  # Prevent tight loop on errors
                    
        except Exception as e:
            logger.error(f"Fatal error in voice recognition thread: {e}", exc_info=True)
    
    def _get_language_code(self) -> str:
        """Get the language code for speech recognition based on current settings."""
        # Default to English
        lang_code = "en-US"
        
        try:
            # Try to get language from language manager if available
            if hasattr(self, 'language_manager') and self.language_manager:
                current_lang = self.language_manager.current_language
                # Map application language codes to speech recognition language codes
                lang_map = {
                    'it': 'it-IT',
                    'en': 'en-US',
                    'es': 'es-ES',
                    'fr': 'fr-FR',
                    'de': 'de-DE'
                }
                lang_code = lang_map.get(current_lang, 'en-US')
        except Exception as e:
            logger.debug(f"Could not determine language code: {e}")
            
        return lang_code

    def _process_command(self, text: str) -> None:
        """Process the recognized text and execute matching commands.

        Args:
            text: The recognized speech text
        """
        if not text or not isinstance(text, str):
            logger.warning(f"Invalid command text: {text}")
            return

        # Clean and normalize the input text
        text = text.strip().lower()
        logger.debug(f"Processing command: {text}")
        
        # Emit the command for any UI updates
        self.command_received.emit(text)
        
        # Track if any command was matched and executed
        command_executed = False
        
        # Find and execute matching commands
        for phrase, callback in self.commands.items():
            if not phrase or not callable(callback):
                continue
                
            # Check for phrase in text (case-insensitive)
            if phrase.lower() in text:
                try:
                    logger.info(f"Executing command: {phrase}")
                    # Execute the callback
                    callback()
                    command_executed = True
                    
                    # Log successful command execution
                    logger.debug(f"Successfully executed command: {phrase}")
                    
                except Exception as e:
                    error_msg = f"Error executing command '{phrase}': {str(e)}"
                    logger.error(error_msg, exc_info=True)
                    
                    # Emit error for UI feedback if needed
                    if hasattr(self, 'command_error'):
                        self.command_error.emit(error_msg)
        
        # Log if no command was matched
        if not command_executed:
            logger.debug(f"No matching command found for: {text}")
            if hasattr(self, 'command_unknown'):
                self.command_unknown.emit(text)


def create_default_voice_controls(gui):
    """Create a VoiceControl instance with default commands for the MSR605 app.

    Args:
        gui: The main GUI instance to control

    Returns:
        VoiceControl: Configured voice control instance
    """
    # Get language manager if available
    language_manager = getattr(gui, 'language_manager', None)
    
    # Create voice control instance with language manager
    voice_control = VoiceControl(language_manager=language_manager)
    
    # Add GUI reference for command callbacks
    voice_control.gui = gui

    # Define command mappings with default English commands
    default_commands = {
        "read card": "read_card",
        "write card": "write_card",
        "erase card": "erase_card",
        "enable voice control": "enable_voice_control",
        "disable voice control": "disable_voice_control",
        "help": "show_voice_help",
        "exit": "close"
    }
    
    # Register default commands
    for phrase, method_name in default_commands.items():
        if hasattr(gui, method_name):
            voice_control.register_command(phrase, getattr(gui, method_name))
    
    # Add language-specific commands if language manager is available
    if language_manager:
        try:
            # Get translations for command phrases
            command_phrases = {
                "read_card": language_manager.translate("voice_commands.read_card", "read card"),
                "write_card": language_manager.translate("voice_commands.write_card", "write card"),
                "erase_card": language_manager.translate("voice_commands.erase_card", "erase card"),
                "enable_voice": language_manager.translate("voice_commands.enable_voice", "enable voice control"),
                "disable_voice": language_manager.translate("voice_commands.disable_voice", "disable voice control"),
                "help": language_manager.translate("voice_commands.help", "help"),
                "exit": language_manager.translate("voice_commands.exit", "exit")
            }
            
            # Register translated commands
            for key, phrase in command_phrases.items():
                method_name = key
                if hasattr(gui, method_name):
                    voice_control.register_command(phrase.lower(), getattr(gui, method_name))
                    
        except Exception as e:
            logger.error(f"Error registering translated voice commands: {e}", exc_info=True)
    
    logger.info(f"Voice control initialized with {len(voice_control.commands)} commands")
    return voice_control
