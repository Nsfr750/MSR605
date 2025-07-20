from PyQt6.QtWidgets import QMenuBar, QMenu, QDialog, QMessageBox
from PyQt6.QtGui import QAction, QActionGroup
from PyQt6.QtCore import Qt, pyqtSignal

# Import application modules
from .log_viewer import LogViewer
from .logger import logger
from .voice_control import create_default_voice_controls
from .help import show_help
from .updates import check_for_updates
from .language_manager import LanguageManager


# Translation function
def tr(key, language_manager=None, **kwargs):
    """
    Helper function to translate text using the language manager.

    Args:
        key: The translation key to look up
        language_manager: The LanguageManager instance to use for translation
        **kwargs: Format arguments for the translation string

    Returns:
        str: The translated string or the key if not found
    """
    if language_manager and hasattr(language_manager, "translate"):
        return language_manager.translate(key, **kwargs)
    return key


class MenuBar(QMenuBar):
    """Custom menu bar for the MSR605 application."""

    # Signal to update the status bar from the main thread
    status_message = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.voice_control = None
        self.language_manager = getattr(parent, "language_manager", None)
        self.init_menus()

        # Connect status message signal
        self.status_message.connect(self._update_status_bar)

        # Connect to language change signal
        if self.language_manager:
            self.language_manager.language_changed.connect(self.retranslate_ui)

    def _update_status_bar(self, message):
        """Update the status bar with a message (thread-safe)."""
        if hasattr(self.parent, "statusBar") and self.parent.statusBar():
            self.parent.statusBar().showMessage(message, 5000)  # Show for 5 seconds

    def init_menus(self):
        """Initialize all menus and actions."""
        # Create menus
        self.file_menu = self.addMenu("")
        self.tools_menu = self.addMenu("")
        self.help_menu = self.addMenu("")

        # Initialize actions first
        self.exit_action = QAction("", self.parent)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.parent.close)

        # Initialize other actions
        self.auto_save_action = QAction("", self.parent, checkable=True)
        self.auto_save_action.setChecked(
            getattr(self.parent, "_GUI__auto_save_database", False)
        )
        self.auto_save_action.triggered.connect(
            lambda checked: setattr(self.parent, "_GUI__auto_save_database", checked)
        )

        self.duplicates_action = QAction("", self.parent, checkable=True)
        self.duplicates_action.setChecked(
            getattr(self.parent, "_GUI__enable_duplicates", False)
        )
        self.duplicates_action.triggered.connect(
            lambda checked: setattr(self.parent, "_GUI__enable_duplicates", checked)
        )

        # Initialize all menu items after actions are created
        self.retranslate_ui()

    def retranslate_ui(self):
        """Retranslate all menu items."""
        # Clear existing actions to prevent duplicates
        self.file_menu.clear()

        # Set File menu title
        self.file_menu.setTitle(tr("menu_file", self.language_manager))

        # Database submenu
        database_menu = self.file_menu.addMenu(
            tr("menu_database", self.language_manager)
        )

        # View Database action
        view_db_action = QAction(
            tr("menu_view_database", self.language_manager), self.parent
        )
        view_db_action.triggered.connect(self.parent.view_database)
        database_menu.addAction(view_db_action)

        # Export to CSV action
        export_csv_action = QAction(
            tr("menu_export_csv", self.language_manager), self.parent
        )
        export_csv_action.triggered.connect(self.parent.export_database_to_csv)
        database_menu.addAction(export_csv_action)

        database_menu.addSeparator()

        # Auto-save action
        self.auto_save_action.setText(tr("menu_auto_save", self.language_manager))
        database_menu.addAction(self.auto_save_action)

        # Allow duplicates action
        self.duplicates_action.setText(
            tr("menu_allow_duplicates", self.language_manager)
        )
        database_menu.addAction(self.duplicates_action)

        # Exit action at the bottom of File menu
        self.file_menu.addSeparator()
        self.exit_action.setText(tr("menu_exit", self.language_manager))
        self.file_menu.addAction(self.exit_action)

        # Tools menu
        self.tools_menu.setTitle(tr("menu_tools", self.language_manager))

        # Language submenu
        language_menu = self.tools_menu.addMenu(
            tr("menu_language", self.language_manager)
        )

        # Language actions
        if not hasattr(self, "language_group"):
            self.language_group = QActionGroup(self)
            self.language_group.setExclusive(True)

            # English
            self.en_action = QAction("English", self.parent, checkable=True)
            self.en_action.setData("en")
            self.en_action.triggered.connect(self.change_language)
            self.language_group.addAction(self.en_action)
            language_menu.addAction(self.en_action)

            # Italian
            self.it_action = QAction("Italiano", self.parent, checkable=True)
            self.it_action.setData("it")
            self.it_action.triggered.connect(self.change_language)
            self.language_group.addAction(self.it_action)
            language_menu.addAction(self.it_action)

        # Set default language
        if self.language_manager:
            lang_code = self.language_manager.current_language
            for action in self.language_group.actions():
                if action.data() == lang_code:
                    action.setChecked(True)
                    break
        else:
            self.en_action.setChecked(True)

        # Voice menu (under Tools)
        voice_menu = self.tools_menu.addMenu(tr("menu_voice", self.language_manager))

        # Voice control actions
        if not hasattr(self, "voice_enabled_action"):
            self.voice_enabled_action = QAction("", self.parent, checkable=True)
            self.voice_enabled_action.setChecked(False)
            self.voice_enabled_action.triggered.connect(self.toggle_voice_control)
            voice_menu.addAction(self.voice_enabled_action)

            # Voice commands help
            self.voice_help_action = QAction("", self.parent)
            self.voice_help_action.triggered.connect(self.show_voice_commands_help)
            voice_menu.addAction(self.voice_help_action)

        self.voice_enabled_action.setText(
            tr("menu_enable_voice", self.language_manager)
        )
        self.voice_help_action.setText(tr("menu_voice_help", self.language_manager))

        # Add Log Viewer action to Tools menu
        if not hasattr(self, "log_viewer_action"):
            self.log_viewer_action = QAction("", self.parent)
            self.log_viewer_action.triggered.connect(self.show_log_viewer)
            self.tools_menu.addAction(self.log_viewer_action)
        self.log_viewer_action.setText(tr("menu_view_logs", self.language_manager))

        # View menu has been removed

        # Help menu
        self.help_menu.setTitle(tr("menu_help", self.language_manager))

        # About action
        if not hasattr(self, "about_action"):
            self.about_action = QAction("", self.parent)
            self.about_action.triggered.connect(self.parent.show_about)
            self.help_menu.addAction(self.about_action)
        self.about_action.setText(tr("menu_about", self.language_manager))

        # Help Contents action
        if not hasattr(self, "help_action"):
            self.help_action = QAction("", self.parent)
            self.help_action.triggered.connect(
                lambda: show_help(self.parent, self.language_manager)
            )
            self.help_menu.addAction(self.help_action)
        self.help_action.setText(tr("menu_help_contents", self.language_manager))

        self.help_menu.addSeparator()

        # Check for Updates action
        if not hasattr(self, "updates_action"):
            self.updates_action = QAction("", self.parent)
            self.updates_action.triggered.connect(self.parent.check_for_updates)
            self.help_menu.addAction(self.updates_action)
        self.updates_action.setText(tr("menu_check_updates", self.language_manager))

        # Sponsor action (under Help menu)
        self.help_menu.addSeparator()
        if not hasattr(self, "sponsor_action"):
            self.sponsor_action = QAction("", self.parent)
            self.sponsor_action.triggered.connect(self.parent.show_sponsor)
            self.help_menu.addAction(self.sponsor_action)
        self.sponsor_action.setText(tr("menu_support", self.language_manager))

    def change_language(self):
        """Change the application language."""
        action = self.sender()
        if action and hasattr(self.parent, "language_manager"):
            lang_code = action.data()
            self.parent.language_manager.set_language(lang_code)

            # Update the UI to reflect the new language
            if hasattr(self.parent, "retranslate_ui"):
                self.parent.retranslate_ui()

            # Save the language preference
            if hasattr(self.parent, "save_settings"):
                self.parent.save_settings()

    def show_log_viewer(self):
        """Show the log viewer dialog."""
        try:
            # Create and show the log viewer dialog
            log_viewer = LogViewer(self.parent, self.parent.language_manager)
            log_viewer.setWindowModality(Qt.WindowModality.ApplicationModal)
            log_viewer.show()
        except Exception as e:
            logger.error(f"Failed to open log viewer: {str(e)}")
            QMessageBox.critical(
                self.parent, "Error", f"Failed to open log viewer: {str(e)}"
            )

    def toggle_voice_control(self, checked):
        """Toggle voice control on or off."""
        try:
            if checked:
                # Check if speech recognition is available
                try:
                    import speech_recognition as sr

                    # Test microphone availability
                    with sr.Microphone() as mic:
                        pass
                    self.start_voice_control()
                except ImportError:
                    QMessageBox.critical(
                        self.parent,
                        "Speech Recognition Not Available",
                        "The speech recognition package is not installed.\n"
                        "Please install it with: pip install SpeechRecognition",
                    )
                    self.voice_enabled_action.setChecked(False)
                except OSError as e:
                    QMessageBox.critical(
                        self.parent,
                        "Microphone Not Available",
                        f"Could not access microphone: {str(e)}\n\n"
                        "Please check your microphone connection and permissions.",
                    )
                    self.voice_enabled_action.setChecked(False)
                except Exception as e:
                    QMessageBox.critical(
                        self.parent,
                        "Voice Control Error",
                        f"Failed to start voice control: {str(e)}",
                    )
                    self.voice_enabled_action.setChecked(False)
            else:
                self.stop_voice_control()
        except Exception as e:
            logger.error(f"Error toggling voice control: {str(e)}")
            self.voice_enabled_action.setChecked(False)
            self.status_message.emit("Error toggling voice control")

    def start_voice_control(self):
        """Start voice control functionality."""
        try:
            # Initialize voice control if not already done
            if self.voice_control is None:
                self.voice_control = create_default_voice_controls(self.parent)
                self.voice_control.command_received.connect(
                    lambda cmd: self.status_message.emit(f"Heard: {cmd}")
                )

            # Start listening for voice commands
            self.voice_control.start_listening()
            logger.info("Voice control enabled")
            self.status_message.emit("Voice control enabled. Say a command...")
        except Exception as e:
            logger.error(f"Failed to start voice control: {str(e)}")
            raise

    def stop_voice_control(self):
        """Stop voice control functionality."""
        try:
            if self.voice_control is not None:
                self.voice_control.stop_listening()
                logger.info("Voice control disabled")
                self.status_message.emit("Voice control disabled")
        except Exception as e:
            logger.error(f"Error stopping voice control: {str(e)}")
            raise

    def show_voice_commands_help(self):
        """Show help for voice commands."""
        help_text = """
        <h2>Voice Commands</h2>
        <p>You can control the application using the following voice commands:</p>
        <ul>
            <li><b>Read card</b> - Start reading a card</li>
            <li><b>Write card</b> - Write data to a card</li>
            <li><b>Clear tracks</b> - Clear all track data</li>
            <li><b>View database</b> - Open the card database</li>
            <li><b>Export to CSV</b> - Export the database to CSV</li>
            <li><b>Switch to read mode</b> - Switch to the Read tab</li>
            <li><b>Switch to write mode</b> - Switch to the Write tab</li>
            <li><b>Show settings</b> - Open the Settings tab</li>
            <li><b>Exit application</b> - Close the application</li>
        </ul>
        <p>Note: Voice control must be enabled in the Voice menu.</p>
        """

        msg_box = QMessageBox()
        msg_box.setWindowTitle("Voice Commands Help")
        msg_box.setTextFormat(Qt.TextFormat.RichText)
        msg_box.setText(help_text)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def update_menu_states(self):
        """Update the state of menu items based on application state."""
        # Update auto-save toggle state
        self.auto_save_action.setChecked(
            getattr(self.parent, "_GUI__auto_save_database", False)
        )
        self.duplicates_action.setChecked(
            getattr(self.parent, "_GUI__enable_duplicates", False)
        )
