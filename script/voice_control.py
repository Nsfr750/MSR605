"""
Voice control module for MSR605 Card Reader.
This module provides voice command functionality using speech recognition.
"""

import queue
import threading
import time
from typing import Callable, Dict, Any, Optional

from PyQt6.QtCore import QObject, pyqtSignal

from .logger import logger


class VoiceControl(QObject):
    """Handles voice recognition and command execution."""

    # Signal emitted when a command is recognized
    command_received = pyqtSignal(str)

    def __init__(self, parent=None):
        """Initialize the voice control system."""
        super().__init__(parent)

        try:
            import speech_recognition as sr

            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()

            # Adjust for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
        except ImportError:
            self.recognizer = None
            self.microphone = None
            logger.warning(
                "Speech recognition not available. Install with: pip install SpeechRecognition"
            )

        self.commands: Dict[str, Callable] = {}
        self.is_listening = False
        self.audio_queue = queue.Queue()
        self.stop_event = threading.Event()

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
        if not self.recognizer or not self.microphone:
            logger.error("Speech recognition not available in listener thread")
            return

        while not self.stop_event.is_set() and self.is_listening:
            try:
                # Listen for audio input
                with self.microphone as source:
                    logger.debug("Listening for voice command...")
                    try:
                        audio = self.recognizer.listen(
                            source, timeout=2, phrase_time_limit=3
                        )
                    except Exception as e:
                        logger.debug(f"Listening error: {e}")
                        continue

                # Recognize speech using Google's speech recognition
                try:
                    text = self.recognizer.recognize_google(audio).lower()
                    logger.info(f"Recognized speech: {text}")
                    self.command_received.emit(text)
                    self._process_command(text)

                except sr.UnknownValueError:
                    logger.debug("Could not understand audio")
                except sr.RequestError as e:
                    logger.error(f"Could not request results; {e}")

            except Exception as e:
                logger.error(f"Error in voice recognition: {e}", exc_info=True)
                time.sleep(1)  # Prevent tight loop on errors

    def _process_command(self, text: str) -> None:
        """Process the recognized text and execute matching commands.

        Args:
            text: The recognized speech text
        """
        # Emit the command for any UI updates
        self.command_received.emit(text)

        # Find and execute matching commands
        for phrase, callback in self.commands.items():
            if phrase in text.lower():
                try:
                    logger.info(f"Executing command: {phrase}")
                    callback()
                except Exception as e:
                    logger.error(f"Error executing command '{phrase}': {e}")


def create_default_voice_controls(gui) -> "VoiceControl":
    """Create a VoiceControl instance with default commands for the MSR605 app.

    Args:
        gui: The main GUI instance to control

    Returns:
        VoiceControl: Configured voice control instance
    """
    voice_control = VoiceControl()

    # Only register commands if speech recognition is available
    if voice_control.recognizer is not None:
        # Register default commands
        commands = {
            # Read/write commands
            "read card": gui.read_card,
            "write card": gui.write_card,
            "clear tracks": gui.clear_tracks,
            # Navigation commands
            "show read tab": lambda: getattr(gui, "tabs", None)
            and gui.tabs.setCurrentIndex(0),
            "show write tab": lambda: getattr(gui, "tabs", None)
            and gui.tabs.setCurrentIndex(1),
            "show database": lambda: getattr(gui, "tabs", None)
            and gui.tabs.setCurrentIndex(2),
            "show settings": lambda: getattr(gui, "tabs", None)
            and gui.tabs.setCurrentIndex(3),
            # Database commands
            "view database": getattr(gui, "view_database", lambda: None),
            "export database": getattr(gui, "export_database_to_csv", lambda: None),
            # Application commands
            "exit application": gui.close,
        }

        # Register all commands
        for phrase, callback in commands.items():
            if callable(callback):
                voice_control.register_command(phrase, callback)

    return voice_control
