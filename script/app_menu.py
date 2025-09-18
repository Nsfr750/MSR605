"""
Menu system for MSR605 application.
Provides a clean, robust menu system with proper language switching support.
"""

from PyQt6.QtWidgets import QMenuBar, QMenu, QDialog, QMessageBox, QApplication
from PyQt6.QtGui import QAction, QActionGroup
from PyQt6.QtCore import Qt, pyqtSignal, QTimer

# Import application modules
from script.logger import logger
from script.help import show_help
from script.log_viewer import LogViewer


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
    if language_manager:
        return language_manager.translate(key, **kwargs)
    return key


class AppMenuBar(QMenuBar):
    """Custom menu bar for the MSR605 application."""

    # Signal to update the status bar from the main thread
    status_message = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.language_manager = getattr(parent, "language_manager", None)
        self._is_rebuilding_menus = False  # Flag to prevent concurrent menu rebuilding
        
        # Initialize menus
        self._create_menus()
        self._create_actions()
        self._build_menu_structure()
        self._setup_connections()
        
        # Initial translation
        self.retranslate_ui()

    def _create_menus(self):
        """Create the main menu structure."""
        self.file_menu = self.addMenu(tr("menu_file", self.language_manager))
        self.tools_menu = self.addMenu(tr("menu_tools", self.language_manager))
        self.help_menu = self.addMenu(tr("menu_help", self.language_manager))

    def _create_actions(self):
        """Create all menu actions."""
        # File menu actions
        self.exit_action = QAction(tr("menu_exit", self.language_manager), self.parent)
        self.exit_action.setShortcut("Ctrl+Q")
        
        # Tools menu actions
        self.auto_save_action = QAction(tr("menu_auto_save", self.language_manager), self.parent, checkable=True)
        self.auto_save_action.setChecked(
            getattr(self.parent, "_GUI__auto_save_database", False)
        )
        
        self.allow_duplicates_action = QAction(tr("menu_allow_duplicates", self.language_manager), self.parent, checkable=True)
        self.allow_duplicates_action.setChecked(
            getattr(self.parent, "_GUI__enable_duplicates", False)
        )
        
        # Coercivity actions
        self.hi_coercivity_action = QAction(tr("settings_hi_coercivity", self.language_manager), self.parent, checkable=True)
        self.hi_coercivity_action.setChecked(True)
        
        self.lo_coercivity_action = QAction(tr("settings_lo_coercivity", self.language_manager), self.parent, checkable=True)
        self.lo_coercivity_action.setChecked(False)
        
        # Language actions
        self.english_action = QAction("English", self.parent, checkable=True)
        self.english_action.setData("en")
        
        self.italian_action = QAction("Italiano", self.parent, checkable=True)
        self.italian_action.setData("it")
        
        # Help menu actions
        self.help_action = QAction(tr("menu_help_contents", self.language_manager), self.parent)
        self.log_viewer_action = QAction(tr("menu_view_logs", self.language_manager), self.parent)
        self.about_action = QAction(tr("menu_about", self.language_manager), self.parent)
        self.sponsor_action = QAction(tr("menu_support", self.language_manager), self.parent)

    def _build_menu_structure(self):
        """Build the menu structure by adding actions to menus."""
        # File menu
        self.file_menu.addAction(self.exit_action)
        
        # Tools menu
        self.tools_menu.addAction(self.auto_save_action)
        self.tools_menu.addAction(self.allow_duplicates_action)
        self.tools_menu.addSeparator()
        self.tools_menu.addAction(self.hi_coercivity_action)
        self.tools_menu.addAction(self.lo_coercivity_action)
        self.tools_menu.addSeparator()
        self.tools_menu.addAction(self.english_action)
        self.tools_menu.addAction(self.italian_action)
        self.tools_menu.addSeparator()
        self.tools_menu.addAction(self.log_viewer_action)
        
        # Help menu
        self.help_menu.addAction(self.help_action)
        self.help_menu.addAction(self.about_action)
        self.help_menu.addAction(self.sponsor_action)

    def _setup_connections(self):
        """Setup signal connections for all actions."""
        # File menu connections
        self.exit_action.triggered.connect(self.parent.close)
        
        # Tools menu connections
        self.auto_save_action.triggered.connect(
            lambda checked: setattr(self.parent, "_GUI__auto_save_database", checked)
        )
        self.allow_duplicates_action.triggered.connect(
            lambda checked: setattr(self.parent, "_GUI__enable_duplicates", checked)
        )
        self.hi_coercivity_action.triggered.connect(
            lambda: self.parent.set_coercivity("hi")
        )
        self.lo_coercivity_action.triggered.connect(
            lambda: self.parent.set_coercivity("lo")
        )
        self.english_action.triggered.connect(self.change_language)
        self.italian_action.triggered.connect(self.change_language)
        
        # Help menu connections
        self.help_action.triggered.connect(
            lambda: show_help(self.parent, self.language_manager)
        )
        self.log_viewer_action.triggered.connect(self.show_log_viewer)
        self.about_action.triggered.connect(self.parent.show_about)
        self.sponsor_action.triggered.connect(self.parent.show_sponsor)
        
        # Create action groups
        self.coercivity_group = QActionGroup(self)
        self.coercivity_group.addAction(self.hi_coercivity_action)
        self.coercivity_group.addAction(self.lo_coercivity_action)
        self.coercivity_group.setExclusive(True)
        
        self.language_group = QActionGroup(self)
        self.language_group.addAction(self.english_action)
        self.language_group.addAction(self.italian_action)
        self.language_group.setExclusive(True)
        
        # Set default language
        if self.language_manager:
            lang_code = self.language_manager.current_language
            for action in self.language_group.actions():
                if action.data() == lang_code:
                    action.setChecked(True)
                    break
        else:
            self.english_action.setChecked(True)
        
        # Connect status message signal
        self.status_message.connect(self.parent.statusBar().showMessage)
        
        # Connect to language change signal
        if self.language_manager:
            self.language_manager.language_changed.connect(self.retranslate_ui)

    def retranslate_ui(self):
        """Retranslate all menu items by updating text only."""
        if self._is_rebuilding_menus:
            return
            
        self._is_rebuilding_menus = True
        
        try:
            # Update menu titles
            if self.language_manager:
                self.file_menu.setTitle(tr("menu_file", self.language_manager))
                self.tools_menu.setTitle(tr("menu_tools", self.language_manager))
                self.help_menu.setTitle(tr("menu_help", self.language_manager))
            else:
                self.file_menu.setTitle("File")
                self.tools_menu.setTitle("Tools")
                self.help_menu.setTitle("Help")
            
            # Update action texts
            if self.language_manager:
                self.exit_action.setText(tr("menu_exit", self.language_manager))
                self.auto_save_action.setText(tr("menu_auto_save", self.language_manager))
                self.allow_duplicates_action.setText(tr("menu_allow_duplicates", self.language_manager))
                self.hi_coercivity_action.setText(tr("settings_hi_coercivity", self.language_manager))
                self.lo_coercivity_action.setText(tr("settings_lo_coercivity", self.language_manager))
                self.help_action.setText(tr("menu_help_contents", self.language_manager))
                self.log_viewer_action.setText(tr("menu_view_logs", self.language_manager))
                self.about_action.setText(tr("menu_about", self.language_manager))
                self.sponsor_action.setText(tr("menu_support", self.language_manager))
            else:
                self.exit_action.setText("Exit")
                self.auto_save_action.setText("Auto Save")
                self.allow_duplicates_action.setText("Allow Duplicates")
                self.hi_coercivity_action.setText("Hi-Coercivity")
                self.lo_coercivity_action.setText("Lo-Coercivity")
                self.help_action.setText("Help")
                self.log_viewer_action.setText("Log Viewer")
                self.about_action.setText("About")
                self.sponsor_action.setText("Sponsor")
                
        except Exception as e:
            logger.error(f"Error retranslating menus: {e}")
        finally:
            self._is_rebuilding_menus = False

    def change_language(self):
        """Change the application language."""
        action = self.sender()
        if action and hasattr(self.parent, "language_manager"):
            lang_code = action.data()
            
            # Change the language first
            self.parent.language_manager.set_language(lang_code)

            # Save the language preference
            if hasattr(self.parent, "save_settings"):
                self.parent.save_settings()
            
            # Use a delay to ensure menus are closed before retranslation
            QTimer.singleShot(300, self._safe_retranslate_ui)
    
    def _safe_retranslate_ui(self):
        """Safely retranslate UI without causing mouse grab issues."""
        try:
            # Temporarily hide the menu bar to prevent mouse grab issues
            self.hide()
            
            # Process all pending events to ensure menus are fully closed
            QApplication.processEvents()
            
            # Wait a bit more for menus to settle
            QTimer.singleShot(100, self._perform_retranslation)
        except Exception as e:
            # If anything goes wrong, just show the menu bar again
            self.show()
            logger.error(f"Error in safe retranslation: {e}")
    
    def _perform_retranslation(self):
        """Perform the actual retranslation after menus are safely closed."""
        try:
            # Now call the main UI retranslation
            if hasattr(self.parent, "retranslate_ui"):
                self.parent.retranslate_ui()
        except Exception as e:
            logger.error(f"Error during retranslation: {e}")
        finally:
            # Always show the menu bar again
            self.show()

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
        self.allow_duplicates_action.setChecked(
            getattr(self.parent, "_GUI__enable_duplicates", False)
        )
