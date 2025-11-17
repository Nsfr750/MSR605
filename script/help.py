"""
Help dialog for the MSR605 application.
"""

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QDialogButtonBox, QLabel
from PyQt6.QtCore import Qt


class HelpDialog(QDialog):
    """A dialog that displays help information for the MSR605 application."""

    def __init__(self, parent=None, language_manager=None):
        """Initialize the help dialog.

        Args:
            parent: The parent widget
            language_manager: An instance of LanguageManager for translations
        """
        super().__init__(parent)
        self.language_manager = language_manager
        self.setWindowTitle(f"{self.translate('dlg_help_title')} (v2.4.5)")
        self.setMinimumSize(700, 600)  # Slightly larger to accommodate more content

        # Initialize UI
        self.setup_ui()

        # Connect language changed signal if language_manager is provided
        if self.language_manager:
            self.language_manager.language_changed.connect(self.retranslate_ui)

    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)

        # Create text browser for help content
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)
        self.text_browser.setStyleSheet(
            """
            QTextBrowser {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3a3a3a;
                border-radius: 4px;
                padding: 10px;
                selection-background-color: #3a3a3a;
            }
            a {
                color: #4a9cff;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            h2 {
                color: #4a9cff;
                margin-top: 0;
                font-size: 1.5em;
            }
            p, li {
                color: #e0e0e0;
                line-height: 1.5;
            }
            code {
                background-color: #3a3a3a;
                color: #f8f8f8;
                padding: 2px 5px;
                border-radius: 3px;
                font-family: monospace;
                border: 1px solid #4a4a4a;
            }
            h3 {
                color: #6bb9ff;
                margin-bottom: 5px;
            }
            ul {
                margin-top: 5px;
                margin-bottom: 15px;
                padding-left: 20px;
            }
            li {
                margin-bottom: 5px;
            }
        """
        )

        # Add a close button
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        self.button_box.rejected.connect(self.reject)

        layout.addWidget(self.text_browser)
        layout.addWidget(self.button_box)

        # Set the help content
        self.retranslate_ui()

    def retranslate_ui(self):
        """Retranslate the UI elements."""
        if hasattr(self, "text_browser"):
            self.text_browser.setHtml(self.get_help_content())

        if hasattr(self, "button_box"):
            self.button_box.clear()
            close_button = self.button_box.addButton(
                QDialogButtonBox.StandardButton.Close
            )
            close_button.setText(self.translate("btn_close"))

    def get_help_content(self):
        """Get the help content in the current language."""
        # Try to get the help content from translations
        if self.language_manager:
            help_content = self.language_manager.translate("help_content")
            if (
                help_content and help_content != "help_content"
            ):  # Ensure we got a valid translation
                return help_content

        # Fallback to English help content with dark mode compatible colors
        help_text = """
        <style>
            body {
                color: #e0e0e0;
                background-color: #2d2d2d;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 10px 0;
            }
            th, td {
                border: 1px solid #4a4a4a;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #3a3a3a;
                color: #4a9cff;
            }
            tr:nth-child(even) {
                background-color: #2d2d2d;
            }
            tr:nth-child(odd) {
                background-color: #252525;
            }
        </style>
        <h2>MSR605 Card Reader - Help (v2.4.5)</h2>
        
        <h3>What's New in v2.4.5</h3>
        <ul>
            <li><b>CI/CD Integration</b>: Automated testing and deployment pipeline for more reliable updates</li>
            <li><b>Enhanced Security</b>: Improved encryption and secure settings storage</li>
            <li><b>Better Performance</b>: Optimized card reading and writing operations</li>
            <li><b>Automatic Updates</b>: Get notified of new versions directly in the application</li>
        </ul>
        
        <h3>Basic Usage:</h3>
        <ul>
            <li><b>Read Card</b>: Click the 'Read Card' button and swipe a card through the reader.</li>
            <li><b>Write Card</b>: Enter data in the track fields and click 'Write Card'.</li>
            <li><b>Clear Tracks</b>: Click 'Clear Tracks' to clear all track data.</li>
            <li><b>Save Settings</b>: Connection settings are now saved automatically when changed.</li>
        </ul>
        
        <h3>Database Features:</h3>
        <ul>
            <li><b>View Database</b>: View all previously read cards in the database.</li>
            <li><b>Export to CSV</b>: Export the card database to a CSV file.</li>
            <li><b>Auto-save</b>: Enable auto-save to automatically save read cards to the database.</li>
            <li><b>Search & Filter</b>: Quickly find specific cards in your database.</li>
        </ul>
        
        <h3>Advanced Features:</h3>
        <ul>
            <li><b>Coercivity Settings</b>: Switch between high and low coercivity modes.</li>
            <li><b>Auto-connect</b>: The application will automatically connect to the MSR605 reader on startup.</li>
            <li><b>Custom Commands</b>: Send custom commands to the reader for advanced operations.</li>
            <li><b>Logging</b>: Detailed logging for troubleshooting and debugging.</li>
        </ul>
        
        <h3>Support & Resources</h3>
        <ul>
            <li><b>Documentation</b>: <a href='https://github.com/Nsfr750/MSR605/tree/main/docs'>Online Documentation</a></li>
            <li><b>Report Issues</b>: <a href='https://github.com/Nsfr750/MSR605/issues'>GitHub Issues</a></li>
            <li><b>Version</b>: 2.4.5 (November 2025)</li>
            <li><b>System Requirements</b>: Windows 10/11, Linux, or macOS with Python 3.8+</li>
        </ul>
        
        <p>For more detailed information, please refer to the full documentation.</p>
        """

    def translate(self, key, **kwargs):
        """Translate a key using the language manager if available.

        Args:
            key: The translation key
            **kwargs: Format arguments for the translation string

        Returns:
            The translated string or the key if no translation is found
        """
        if self.language_manager:
            return self.language_manager.translate(key, **kwargs)
        return key


def show_help(parent=None, language_manager=None):
    """Show the help dialog.

    Args:
        parent: The parent widget
        language_manager: An instance of LanguageManager for translations
    """
    dialog = HelpDialog(parent, language_manager)
    dialog.exec()


# For testing
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    from language_manager import LanguageManager

    app = QApplication(sys.argv)

    # Test with language manager
    language_manager = LanguageManager()
    language_manager.set_language("it")  # Test with Italian

    dialog = HelpDialog(language_manager=language_manager)
    dialog.show()

    sys.exit(app.exec())
