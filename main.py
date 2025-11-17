#!/usr/bin/env python3
"""
MSR605 v 2.4.5 - Main Entry Point

This is the main entry point for the MSR605 Card Reader/Writer application.
It initializes and starts the PyQt6 application with the main window.
"""

"""
Main Imports
"""
import sys
from PyQt6.QtWidgets import QApplication, QStyleFactory
from PyQt6.QtGui import QPalette, QColor

# Import the GUI module
from script.UI import GUI


def main():
    """
    Main function that initializes and starts the application.
    """
    # Create the application
    app = QApplication(sys.argv)

    # Set Fusion style for consistent look across platforms
    app.setStyle("Fusion")

    # Create and set dark palette
    dark_palette = QPalette()

    # Base colors
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
    dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))

    # Set the palette
    app.setPalette(dark_palette)

    # Additional styling for dark mode
    app.setStyleSheet(
        """
        QToolTip { 
            color: #ffffff; 
            background-color: #2a82da; 
            border: 1px solid #2a82da; 
            padding: 5px;
            border-radius: 3px;
            opacity: 230;
        }
        QMenuBar::item:selected {
            background: #3a3a3a;
        }
        QMenu::item:selected {
            background: #2a82da;
        }
        QTabBar::tab:selected {
            background: #3a3a3a;
            border-bottom: 2px solid #2a82da;
        }
        QTabBar::tab:!selected {
            background: #2a2a2a;
        }
        QStatusBar {
            background: #2a2a2a;
            color: white;
        }
        QGroupBox {
            border: 1px solid #3a3a3a;
            border-radius: 4px;
            margin-top: 1em;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px;
        }
    """
    )

    # Set application information
    app.setApplicationName("MSR605 Reader/Writer")
    app.setApplicationDisplayName("MSR605 Card Reader/Writer")

    # Create and show the main window
    window = GUI()
    window.show()

    # Start the event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
