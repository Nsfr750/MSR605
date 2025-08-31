from PyQt6.QtWidgets import QMenuBar, QMenu, QDialog, QMessageBox, QApplication, QStyle
from PyQt6.QtGui import QAction, QActionGroup, QKeySequence
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
        """Initialize all menus and actions with QStyle standard icons and shortcuts."""
        style = QApplication.style()
        
        # Create a style for the menu bar to ensure text visibility
        self.setStyleSheet("""
            QMenuBar {
                background-color: #202020;
                spacing: 3px;
            }
            QMenuBar::item {
                padding: 5px 10px;
                background: transparent;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background: #cce0ff;
            }
            QMenuBar::item:pressed {
                background: #99c2ff;
            }
        """)
        
        # Create main menu items with text and icons
        self.file_menu = QMenu(tr("menu_file", self.language_manager), self)
        self.file_menu.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_FileDialogNewFolder))
        self.addMenu(self.file_menu)
        
        self.tools_menu = QMenu(tr("menu_tools", self.language_manager), self)
        self.tools_menu.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
        self.addMenu(self.tools_menu)
        
        self.help_menu = QMenu(tr("menu_help", self.language_manager), self)
        self.help_menu.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_MessageBoxQuestion))
        self.addMenu(self.help_menu)
        
        # Force non-native menu bar
        self.setNativeMenuBar(False)
        
        # Initialize actions with icons and shortcuts
        self.exit_action = QAction(
            style.standardIcon(QStyle.StandardPixmap.SP_DialogCloseButton),
            "",  # Text will be set in retranslate_ui
            self.parent
        )
        self.exit_action.setShortcut(QKeySequence.StandardKey.Quit)  # Standard quit shortcut
        self.exit_action.setStatusTip("Exit the application")
        self.exit_action.triggered.connect(self.parent.close)

        # Initialize auto-save action
        self.auto_save_action = QAction(
            style.standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton),
            "",  # Text will be set in retranslate_ui
            self.parent,
            checkable=True
        )
        self.auto_save_action.setShortcut("Ctrl+Shift+A")
        self.auto_save_action.setStatusTip("Toggle auto-save mode")
        self.auto_save_action.setChecked(
            getattr(self.parent, "_GUI__auto_save_database", False)
        )
        self.auto_save_action.triggered.connect(
            lambda checked: setattr(self.parent, "_GUI__auto_save_database", checked)
        )

        # Initialize duplicates action
        self.duplicates_action = QAction(
            style.standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView),
            "",  # Text will be set in retranslate_ui
            self.parent,
            checkable=True
        )
        self.duplicates_action.setShortcut("Ctrl+Shift+D")
        self.duplicates_action.setStatusTip("Toggle duplicate card handling")
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
        style = QApplication.style()
        
        # Update menu titles without clearing to prevent duplication
        self.file_menu.setTitle(tr("menu_file", self.language_manager))
        self.tools_menu.setTitle(tr("menu_tools", self.language_manager))
        self.help_menu.setTitle(tr("menu_help", self.language_manager))
        
        # Only update action texts, don't recreate them
        if hasattr(self, 'exit_action'):
            self.exit_action.setText(tr("menu_exit", self.language_manager))
            self.exit_action.setStatusTip(tr("menu_exit_tooltip", self.language_manager))

        if hasattr(self, 'auto_save_action'):
            self.auto_save_action.setText(tr("menu_auto_save", self.language_manager))

        if hasattr(self, 'duplicates_action'):
            self.duplicates_action.setText(tr("menu_allow_duplicates", self.language_manager))

        if hasattr(self, 'voice_enabled_action'):
            self.voice_enabled_action.setText(tr("menu_enable_voice", self.language_manager))

        if hasattr(self, 'voice_help_action'):
            self.voice_help_action.setText(tr("menu_voice_help", self.language_manager))

        if hasattr(self, 'log_viewer_action'):
            self.log_viewer_action.setText(tr("menu_view_logs", self.language_manager))

        if hasattr(self, 'help_action'):
            self.help_action.setText(tr("menu_help_contents", self.language_manager))

        if hasattr(self, 'about_action'):
            self.about_action.setText(tr("menu_about", self.language_manager))

        if hasattr(self, 'updates_action'):
            self.updates_action.setText(tr("menu_check_updates", self.language_manager))

        if hasattr(self, 'sponsor_action'):
            self.sponsor_action.setText(tr("menu_sponsor", self.language_manager))

        if hasattr(self, 'en_action'):
            self.en_action.setText("English")

        if hasattr(self, 'it_action'):
            self.it_action.setText("Italiano")

        # Database submenu with icon
        if not hasattr(self, 'database_menu'):
            self.database_menu = self.file_menu.addMenu(
                QApplication.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView),
                tr("menu_database", self.language_manager)
            )

        # View Database action with icon and shortcut
        if not hasattr(self, 'view_db_action'):
            self.view_db_action = QAction(
                QApplication.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogListView),
                tr("menu_view_database", self.language_manager),
                self.parent
            )
            self.view_db_action.setShortcut("Ctrl+D")
            self.view_db_action.setStatusTip("View card database")
            self.view_db_action.triggered.connect(self.parent.view_database)
            self.database_menu.addAction(self.view_db_action)

        # Export to CSV action with icon and shortcut
        if not hasattr(self, 'export_csv_action'):
            self.export_csv_action = QAction(
                QApplication.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton),
                "",  # Text will be set below
                self.parent
            )
            self.export_csv_action.setShortcut("Ctrl+E")
            self.export_csv_action.triggered.connect(self.parent.export_database_to_csv)
            self.database_menu.addAction(self.export_csv_action)
        
        # Update text and status tip
        self.export_csv_action.setText(tr("menu_export_csv", self.language_manager))
        self.export_csv_action.setStatusTip(tr("Export database to CSV file", self.language_manager))
        
        self.database_menu.addSeparator()

        # Auto-save action (already initialized with icon)
        self.auto_save_action.setText(tr("menu_auto_save", self.language_manager))
        self.database_menu.addAction(self.auto_save_action)

        # Allow duplicates action (already initialized with icon)
        self.duplicates_action.setText(tr("menu_allow_duplicates", self.language_manager))
        self.database_menu.addAction(self.duplicates_action)

        # Exit action at the bottom of File menu
        self.file_menu.addSeparator()
        self.exit_action.setText(tr("menu_exit", self.language_manager))
        self.file_menu.addAction(self.exit_action)

        # Tools menu title is already set in init_menus

        style = QApplication.style()
        
        # Language submenu with icon
        language_menu = self.tools_menu.addMenu(
            style.standardIcon(QStyle.StandardPixmap.SP_DesktopIcon),
            tr("menu_language", self.language_manager)
        )

        # Language actions
        if not hasattr(self, "language_group"):
            self.language_group = QActionGroup(self)
            self.language_group.setExclusive(True)

            # English
            self.en_action = QAction(
                style.standardIcon(QStyle.StandardPixmap.SP_DialogYesButton),
                "🇬🇧 English",  # UK flag emoji
                self.parent,
                checkable=True
            )
            self.en_action.setData("en")
            self.en_action.setShortcut("Ctrl+L E")
            self.en_action.triggered.connect(self.change_language)
            self.language_group.addAction(self.en_action)
            language_menu.addAction(self.en_action)

            # Italian
            self.it_action = QAction(
                style.standardIcon(QStyle.StandardPixmap.SP_DialogYesButton),
                "🇮🇹 Italiano",  # Italian flag emoji
                self.parent,
                checkable=True
            )
            self.it_action.setData("it")
            self.it_action.setShortcut("Ctrl+L I")
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

        style = QApplication.style()
        
        # Voice menu (under Tools) with icon
        voice_menu = self.tools_menu.addMenu(
            style.standardIcon(QStyle.StandardPixmap.SP_MediaVolume),
            tr("menu_voice", self.language_manager)
        )

        # Voice control actions
        if not hasattr(self, "voice_enabled_action"):
            self.voice_enabled_action = QAction(
                style.standardIcon(QStyle.StandardPixmap.SP_MediaVolume),
                "",  # Text will be set in retranslate_ui
                self.parent,
                checkable=True
            )
            self.voice_enabled_action.setShortcut("Ctrl+Shift+V")
            self.voice_enabled_action.setStatusTip("Enable/disable voice control")
            self.voice_enabled_action.setChecked(False)
            self.voice_enabled_action.triggered.connect(self.toggle_voice_control)
            voice_menu.addAction(self.voice_enabled_action)

            # Voice commands help
            self.voice_help_action = QAction(
                style.standardIcon(QStyle.StandardPixmap.SP_TitleBarContextHelpButton),
                "",  # Text will be set in retranslate_ui
                self.parent
            )
            self.voice_help_action.setShortcut("F8")
            self.voice_help_action.triggered.connect(self.show_voice_commands_help)
            voice_menu.addAction(self.voice_help_action)

        self.voice_enabled_action.setText(
            tr("menu_enable_voice", self.language_manager)
        )
        self.voice_help_action.setText(tr("menu_voice_help", self.language_manager))

        # Add Log Viewer action to Tools menu with icon and shortcut
        if not hasattr(self, "log_viewer_action"):
            self.log_viewer_action = QAction(
                QApplication.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView),
                "",  # Text will be set in retranslate_ui
                self.parent
            )
            self.log_viewer_action.setShortcut("Ctrl+L")
            self.log_viewer_action.setStatusTip("View application logs")
            self.log_viewer_action.triggered.connect(self.show_log_viewer)
            self.tools_menu.addAction(self.log_viewer_action)
        self.log_viewer_action.setText(tr("menu_view_logs", self.language_manager))

        # View menu has been removed

        # Help menu title is already set in init_menus

        style = QApplication.style()
        
        # Help Contents action with icon and shortcut
        if not hasattr(self, "help_action"):
            self.help_action = QAction(
                style.standardIcon(QStyle.StandardPixmap.SP_DialogHelpButton),
                "",  # Text will be set in retranslate_ui
                self.parent
            )
            self.help_action.setShortcut("F1")
            self.help_action.setStatusTip("Show help contents")
            self.help_action.triggered.connect(
                lambda: show_help(self.parent, self.language_manager)
            )
            self.help_menu.addAction(self.help_action)
        self.help_action.setText(tr("menu_help_contents", self.language_manager))

        self.help_menu.addSeparator()

        # About action with icon and shortcut
        if not hasattr(self, "about_action"):
            self.about_action = QAction(
                style.standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation),
                "",  # Text will be set in retranslate_ui
                self.parent
            )
            self.about_action.setShortcut("F2")
            self.about_action.setStatusTip("Show about information")
            self.about_action.triggered.connect(self.parent.show_about)
            self.help_menu.addAction(self.about_action)
        self.about_action.setText(tr("menu_about", self.language_manager))

        # Check for Updates action with icon and shortcut
        if not hasattr(self, "updates_action"):
            self.updates_action = QAction(
                style.standardIcon(QStyle.StandardPixmap.SP_BrowserReload),
                "",  # Text will be set in retranslate_ui
                self.parent
            )
            self.updates_action.setShortcut("F5")
            self.updates_action.setStatusTip("Check for application updates")
            self.updates_action.triggered.connect(self.parent.check_for_updates)
            self.help_menu.addAction(self.updates_action)
        self.updates_action.setText(tr("menu_check_updates", self.language_manager))

        # Sponsor action with icon and shortcut
        self.help_menu.addSeparator()
        if not hasattr(self, "sponsor_action"):
            self.sponsor_action = QAction(
                style.standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton),
                "",  # Text will be set in retranslate_ui
                self.parent
            )
            self.sponsor_action.setShortcut("F3")
            self.sponsor_action.setStatusTip("Support the project")
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
