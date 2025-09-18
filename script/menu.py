from PyQt6.QtWidgets import QMenuBar, QMenu, QDialog, QMessageBox, QApplication
from PyQt6.QtGui import QAction, QActionGroup
from PyQt6.QtCore import Qt, pyqtSignal, QTimer

# Import application modules
from .log_viewer import LogViewer
from .logger import logger
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
        self.language_manager = getattr(parent, "language_manager", None)
        self._is_rebuilding_menus = False  # Flag to prevent concurrent menu rebuilding
        self._language_menu_to_close = None  # Reference to language menu being closed
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
        # Prevent concurrent menu rebuilding
        if self._is_rebuilding_menus:
            return
        
        self._is_rebuilding_menus = True
        
        try:
            # Process any pending events to ensure menus are properly closed
            QApplication.processEvents()
            
            # Clear existing actions to prevent duplicates
            self.file_menu.clear()
            self.tools_menu.clear()
            self.help_menu.clear()

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
            
        finally:
            # Reset the rebuilding flag
            self._is_rebuilding_menus = False

    def change_language(self):
        """Change the application language."""
        action = self.sender()
        if action and hasattr(self.parent, "language_manager"):
            lang_code = action.data()
            self.parent.language_manager.set_language(lang_code)

            # Save the language preference
            if hasattr(self.parent, "save_settings"):
                self.parent.save_settings()
            
            # Find the language menu and connect to its aboutToHide signal
            # This ensures we only rebuild after the menu is fully closed
            language_menu = None
            for action in self.tools_menu.actions():
                if action.menu() and "language" in action.text().lower():
                    language_menu = action.menu()
                    break
            
            if language_menu:
                # Connect to the menu's aboutToHide signal
                language_menu.aboutToHide.connect(self._on_language_menu_closed)
                # Store the language menu reference
                self._language_menu_to_close = language_menu
            else:
                # Fallback: use a longer delay if we can't find the language menu
                QTimer.singleShot(200, self._delayed_retranslate_ui)
    
    def _on_language_menu_closed(self):
        """Called when the language menu is fully closed."""
        # Disconnect the signal to prevent multiple calls
        if hasattr(self, '_language_menu_to_close') and self._language_menu_to_close:
            try:
                self._language_menu_to_close.aboutToHide.disconnect(self._on_language_menu_closed)
            except:
                pass  # Ignore if already disconnected
            self._language_menu_to_close = None
        
        # Use a small delay to ensure the menu is fully processed
        QTimer.singleShot(50, self._delayed_retranslate_ui)
    
    def _delayed_retranslate_ui(self):
        """Retranslate UI after a delay to allow menus to close properly."""
        # Close any open menus before rebuilding
        self._close_all_menus()
        
        # Now rebuild the menus
        if hasattr(self.parent, "retranslate_ui"):
            self.parent.retranslate_ui()
    
    def _close_all_menus(self):
        """Close all open menus to prevent mouse grab issues."""
        # Close all menu actions
        for menu in [self.file_menu, self.tools_menu, self.help_menu]:
            if menu and menu.isVisible():
                menu.close()
        
        # Also close any submenus that might be open
        for action in self.actions():
            if hasattr(action, 'menu') and action.menu():
                submenu = action.menu()
                if submenu.isVisible():
                    submenu.close()

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

    def update_menu_states(self):
        """Update the state of menu items based on application state."""
        # Update auto-save toggle state
        self.auto_save_action.setChecked(
            getattr(self.parent, "_GUI__auto_save_database", False)
        )
        self.duplicates_action.setChecked(
            getattr(self.parent, "_GUI__enable_duplicates", False)
        )
