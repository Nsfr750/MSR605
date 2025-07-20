#!/usr/bin/env python3

"""visualization.py

This module provides advanced visualization capabilities for card data,
including track analysis, data distribution, and interactive charts.
"""

import os
import sys
import math
import re
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from collections import Counter

# Set the Qt backend before importing PyQt6
os.environ['QT_API'] = 'pyqt6'

# Import visualization libraries
import matplotlib
# Set the backend before importing pyplot
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Import Qt modules
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QSizePolicy,
    QScrollArea, QApplication, QLabel, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from script.language_manager import LanguageManager

class TrackVisualizationType(Enum):
    """Types of visualizations available for track data."""
    
    def __new__(cls, value, translation_key, description_key=None):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.translation_key = translation_key
        obj.description_key = description_key or f"{translation_key}_desc"
        return obj
        
    def get_display_name(self, language_manager=None):
        if language_manager:
            return language_manager.translate(self.translation_key, default=self._value_.replace('_', ' ').title())
        return self._value_.replace('_', ' ').title()
        
    def get_description(self, language_manager=None, default=""):
        if language_manager and hasattr(self, 'description_key'):
            return language_manager.translate(self.description_key, default=default)
        return default

    CHARACTER_DISTRIBUTION = ("character_distribution", "viz_char_dist", "viz_char_dist_desc")
    BIT_PATTERN = ("bit_pattern", "viz_bit_pattern", "viz_bit_pattern_desc")
    DATA_DENSITY = ("data_density", "viz_data_density", "viz_data_density_desc")
    FIELD_ANALYSIS = ("field_analysis", "viz_field_analysis", "viz_field_analysis_desc")


@dataclass
class TrackVisualization:
    """Container for track visualization data and metadata."""

    track_number: int
    visualization_type: TrackVisualizationType
    title: str
    description: str
    data: Any
    figure: Optional[Figure] = None


class CardDataVisualizer:
    """Main class for generating visualizations of card data."""

    def __init__(self, language_manager=None):
        """Initialize the visualizer with default settings.
        
        Args:
            language_manager: Optional LanguageManager instance for translations
        """
        self.theme = "dark_background"  # Default theme
        self.figure_size = (8, 6)  # Default figure size in inches (width, height)
        self.dpi = 100  # Dots per inch for figures
        self.language_manager = language_manager

    def set_theme(self, theme: str):
        """Set the visualization theme.

        Args:
            theme: Theme name (e.g., 'dark_background', 'default')
        """
        self.theme = theme

    def create_visualizations(self, tracks: List[str]) -> List[TrackVisualization]:
        """Create visualizations for the given track data.

        Args:
            tracks: List of track data strings [track1, track2, track3]

        Returns:
            List of TrackVisualization objects
        """
        visualizations = []

        for i, track in enumerate(tracks, 1):
            if not track:
                continue

            # Create character distribution visualization
            char_dist = self._create_character_distribution(track, i)
            if char_dist:
                visualizations.append(char_dist)

            # Create bit pattern visualization
            bit_pattern = self._create_bit_pattern(track, i)
            if bit_pattern:
                visualizations.append(bit_pattern)

            # Create data density visualization
            density = self._create_data_density(track, i)
            if density:
                visualizations.append(density)

            # Create field analysis visualization if track has fields
            if any(sep in track for sep in ["^", "="]):
                field_analysis = self._create_field_analysis(track, i)
                if field_analysis:
                    visualizations.append(field_analysis)

        return visualizations

    def _create_character_distribution(
        self, track_data: str, track_num: int
    ) -> Optional[TrackVisualization]:
        """Create a character distribution visualization.

        Args:
            track_data: The track data string
            track_num: Track number (1, 2, or 3)

        Returns:
            TrackVisualization object or None if no data
        """
        if not track_data:
            return None

        try:
            # Count character frequencies
            char_counts = Counter(track_data)

            if not char_counts:
                return None

            # Sort characters by frequency
            sorted_items = sorted(char_counts.items(), key=lambda x: x[1], reverse=True)
            chars, counts = zip(*sorted_items)

            # Create figure with a larger size for better visibility
            with plt.style.context(self.theme):
                fig = Figure(figsize=(10, 6), dpi=self.dpi)
                ax = fig.add_subplot(111)

                # Create bar chart with a more appealing style
                bars = ax.bar(range(len(chars)), counts, color="#4b8bbe", alpha=0.8, 
                            edgecolor='#4b8bbe', linewidth=0.7)

                # Customize x-axis
                ax.set_xticks(range(len(chars)))
                ax.set_xticklabels([repr(c)[1:-1] for c in chars], 
                                 rotation=45, ha="right", fontsize=9)

                # Add value labels on top of bars
                for bar in bars:
                    height = bar.get_height()
                    ax.text(
                        bar.get_x() + bar.get_width() / 2.0,
                        height + 0.1,
                        f"{int(height)}",
                        ha="center",
                        va="bottom",
                        fontsize=8,
                        color='#333333'
                    )

                # Customize the plot appearance
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_alpha(0.3)
                ax.spines['bottom'].set_alpha(0.3)
                ax.grid(axis='y', linestyle='--', alpha=0.3)

                # Set labels and title with improved styling
                xlabel = self.language_manager.translate("viz_char_xlabel", default="Character") if self.language_manager else "Character"
                ylabel = self.language_manager.translate("viz_frequency", default="Frequency") if self.language_manager else "Frequency"
                
                ax.set_xlabel(xlabel, fontsize=10, labelpad=10)
                ax.set_ylabel(ylabel, fontsize=10, labelpad=10)
                
                # Get translated title
                title = self.language_manager.translate("viz_char_title", default="Track {track_num} - Character Distribution")
                ax.set_title(
                    title.format(track_num=track_num),
                    fontsize=12, 
                    pad=15,
                    fontweight='bold'
                )

                # Adjust layout to prevent label cutoff
                fig.tight_layout()

                # Get translated description
                description = TrackVisualizationType.CHARACTER_DISTRIBUTION.get_description(
                    self.language_manager,
                    "Shows the frequency of each character in the track data."
                )
                
                # Return the visualization with track data included
                return TrackVisualization(
                    track_number=track_num,
                    visualization_type=TrackVisualizationType.CHARACTER_DISTRIBUTION,
                    title=self.language_manager.translate(
                        "viz_char_full_title", 
                        default="Track {track_num} Character Distribution"
                    ).format(track_num=track_num) if self.language_manager else f"Track {track_num} Character Distribution",
                    description=description,
                    data={
                        "characters": chars, 
                        "counts": counts,
                        "track_data": track_data  # Include the original track data
                    },
                    figure=fig,
                )
                
        except Exception as e:
            print(f"Error creating character distribution visualization: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def _create_bit_pattern(
        self, track_data: str, track_num: int
    ) -> Optional[TrackVisualization]:
        """Create a bit pattern visualization.

        Args:
            track_data: The track data string
            track_num: Track number (1, 2, or 3)

        Returns:
            TrackVisualization object or None if no data
        """
        if not track_data:
            return None

        try:
            # Convert characters to binary representation
            binary_data = []
            for char in track_data:
                # Get 8-bit binary representation
                binary = format(ord(char), "08b")
                binary_data.extend([int(bit) for bit in binary])

            if not binary_data:
                return None

            # Create figure with a better size for the bit pattern
            with plt.style.context(self.theme):
                fig = Figure(figsize=(12, 3), dpi=self.dpi)
                ax = fig.add_subplot(111)

                # Create a step plot of the bit pattern with better styling
                ax.step(
                    range(len(binary_data)), 
                    binary_data, 
                    where="mid", 
                    color="#4daf4a",  # A nice green color
                    linewidth=1.5,
                    alpha=0.9
                )

                # Customize y-axis
                ax.set_yticks([0, 1])
                ax.set_yticklabels(["0", "1"], fontsize=9)
                ax.set_ylim(-0.2, 1.2)  # Add some padding

                # Customize x-axis with translated labels
                xlabel = self.language_manager.translate("viz_bitpos_label", default="Bit Position") if self.language_manager else "Bit Position"
                ylabel = self.language_manager.translate("viz_bitval_label", default="Bit Value") if self.language_manager else "Bit Value"
                
                ax.set_xlabel(xlabel, fontsize=10, labelpad=8)
                ax.set_ylabel(ylabel, fontsize=10, labelpad=8)
                
                # Get translated title
                title = self.language_manager.translate("viz_bit_title", default="Track {track_num} - Bit Pattern")
                ax.set_title(
                    title.format(track_num=track_num),
                    fontsize=12,
                    pad=12,
                    fontweight='bold'
                )

                # Customize the plot appearance
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_alpha(0.3)
                ax.spines['bottom'].set_alpha(0.3)
                
                # Add grid for better readability
                ax.grid(True, axis='y', linestyle='--', alpha=0.3)
                ax.grid(True, axis='x', linestyle=':', alpha=0.2)

                # Add bit position markers every 8 bits (for bytes)
                if len(binary_data) > 8:
                    for i in range(0, len(binary_data), 8):
                        ax.axvline(x=i, color='gray', linestyle='--', alpha=0.3, linewidth=0.8)

                # Adjust layout to prevent label cutoff
                fig.tight_layout()

                # Get translated description
                description = TrackVisualizationType.BIT_PATTERN.get_description(
                    self.language_manager,
                    "Shows the binary representation of the track data."
                )

                return TrackVisualization(
                    track_number=track_num,
                    visualization_type=TrackVisualizationType.BIT_PATTERN,
                    title=self.language_manager.translate(
                        "viz_bit_full_title",
                        default="Track {track_num} Bit Pattern"
                    ).format(track_num=track_num) if self.language_manager else self.language_manager.translate("viz_bit_full_title", default="Track {track_num} Bit Pattern").format(track_num=track_num),
                    description=description,
                    data={
                        "binary_data": binary_data,
                        "track_data": track_data  # Include the original track data
                    },
                    figure=fig,
                )
                
        except Exception as e:
            print(f"Error creating bit pattern visualization: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def _create_data_density(
        self, track_data: str, track_num: int
    ) -> Optional[TrackVisualization]:
        """Create a data density visualization.

        Args:
            track_data: The track data string
            track_num: Track number (1, 2, or 3)

        Returns:
            TrackVisualization object or None if no data
        """
        if not track_data:
            return None

        try:
            # Calculate character frequencies and get unique characters
            char_freq = {}
            for char in track_data:
                char_freq[char] = char_freq.get(char, 0) + 1

            if not char_freq:
                return None

            # Get character codes and their frequencies
            char_codes = [ord(c) for c in track_data]
            unique_codes = sorted(set(char_codes))
            
            # Create figure with a good size for the histogram
            with plt.style.context(self.theme):
                fig = Figure(figsize=(10, 5), dpi=self.dpi)
                ax = fig.add_subplot(111)

                # Calculate optimal number of bins
                num_bins = min(30, len(unique_codes) or 1)
                if num_bins < 1:
                    num_bins = 1

                # Create a histogram of character frequencies with better styling
                n, bins, patches = ax.hist(
                    char_codes,
                    bins=num_bins,
                    color="#984ea3",  # A nice purple color
                    alpha=0.8,
                    edgecolor='#984ea3',
                    linewidth=0.7,
                    density=False  # Show actual counts, not density
                )

                # Customize the plot appearance
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_alpha(0.3)
                ax.spines['bottom'].set_alpha(0.3)
                
                # Add grid for better readability
                ax.grid(True, axis='y', linestyle='--', alpha=0.3)

                # Set labels and title with better styling
                xlabel = self.language_manager.translate("viz_charcode_label", default="Character Code") if self.language_manager else "Character Code"
                ylabel = self.language_manager.translate("viz_frequency", default="Frequency") if self.language_manager else "Frequency"
                
                ax.set_xlabel(xlabel, fontsize=10, labelpad=8)
                ax.set_ylabel(ylabel, fontsize=10, labelpad=8)
                
                # Get translated title
                title = self.language_manager.translate("viz_density_title", default="Track {track_num} - Data Density")
                ax.set_title(
                    title.format(track_num=track_num),
                    fontsize=12,
                    pad=12,
                    fontweight='bold'
                )

                # Add value labels on top of bars if there are few enough
                if len(unique_codes) <= 15:
                    for i in range(len(patches)):
                        height = patches[i].get_height()
                        if height > 0:  # Only label non-zero bars
                            ax.text(
                                patches[i].get_x() + patches[i].get_width() / 2.,
                                height + 0.1,
                                f"{int(height)}",
                                ha='center',
                                va='bottom',
                                fontsize=8,
                                color='#333333'
                            )

                # Add character codes on x-axis if there are few enough
                if len(unique_codes) <= 20:
                    ax.set_xticks(unique_codes)
                    ax.set_xticklabels(
                        [f"{c}\n({chr(c) if 32 <= c <= 126 else ' '})" for c in unique_codes],
                        fontsize=8,
                        rotation=45,
                        ha='right'
                    )
                else:
                    ax.tick_params(axis='x', labelsize=8)

                # Adjust layout to prevent label cutoff
                fig.tight_layout()

                # Get translated description
                description = TrackVisualizationType.DATA_DENSITY.get_description(
                    self.language_manager,
                    "Shows the distribution of character codes in the track data."
                )

                return TrackVisualization(
                    track_number=track_num,
                    visualization_type=TrackVisualizationType.DATA_DENSITY,
                    title=self.language_manager.translate(
                        "viz_density_full_title", 
                        default="Track {track_num} Data Density"
                    ).format(track_num=track_num) if self.language_manager else f"Track {track_num} Data Density",
                    description=description,
                    data={
                        "char_freq": char_freq,
                        "track_data": track_data  # Include the original track data
                    },
                    figure=fig,
                )
                
        except Exception as e:
            print(f"Error creating data density visualization: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    def _create_field_analysis(
        self, track_data: str, track_num: int
    ) -> Optional[TrackVisualization]:
        """Create a field analysis visualization.

        Args:
            track_data: The track data string
            track_num: Track number (1, 2, or 3)

        Returns:
            TrackVisualization object or None if no fields found
        """
        if not track_data:
            return None

        try:
            # Try to parse fields (this is a simple approach, adjust based on actual format)
            fields = []

            # Try different field separators
            if "^" in track_data:
                fields = [f for f in track_data.split("^") if f]  # Filter out empty fields
                field_names = [f"Field {i+1}" for i in range(len(fields))]
            elif "=" in track_data:
                fields = [f for f in track_data.split("=") if f]  # Filter out empty fields
                field_names = [f"Field {i+1}" for i in range(len(fields))]
            else:
                # No clear field separators found
                return None

            if not fields:
                return None

            # Calculate field lengths
            field_lengths = [len(field) for field in fields]

            # Create figure with better sizing
            with plt.style.context(self.theme):
                fig = Figure(figsize=(max(8, len(fields) * 0.8), 6), dpi=self.dpi)
                ax = fig.add_subplot(111)

                # Create bar chart of field lengths with better styling
                bars = ax.bar(
                    field_names, 
                    field_lengths, 
                    color="#4daf4a",  # A nice green color
                    alpha=0.8,
                    edgecolor='#4daf4a',
                    linewidth=0.7
                )

                # Add value labels on top of bars
                for bar in bars:
                    height = bar.get_height()
                    if height > 0:  # Only label non-zero bars
                        ax.text(
                            bar.get_x() + bar.get_width() / 2.0,
                            height + 0.2,  # Slight offset from the top of the bar
                            f"{int(height)}",
                            ha="center",
                            va="bottom",
                            fontsize=9,
                            fontweight='bold',
                            color='#333333'
                        )

                # Customize the plot appearance
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_alpha(0.3)
                ax.spines['bottom'].set_alpha(0.3)
                
                # Add grid for better readability
                ax.grid(True, axis='y', linestyle='--', alpha=0.3)

                # Set labels and title with better styling
                ylabel = self.language_manager.translate("viz_field_length", default="Length (characters)") if self.language_manager else "Length (characters)"
                xlabel = self.language_manager.translate("viz_field_label", default="Field") if self.language_manager else "Field"
                
                ax.set_ylabel(ylabel, fontsize=10, labelpad=8)
                ax.set_xlabel(xlabel, fontsize=10, labelpad=8)
                
                # Get translated title
                title = self.language_manager.translate("viz_field_title", default="Track {track_num} - Field Analysis")
                ax.set_title(
                    title.format(track_num=track_num),
                    fontsize=12,
                    pad=12,
                    fontweight='bold'
                )

                # Rotate x-axis labels for better readability
                plt.setp(
                    ax.get_xticklabels(), 
                    rotation=45, 
                    ha="right",
                    rotation_mode="anchor",
                    fontsize=9
                )

                # Adjust layout to prevent label cutoff
                fig.tight_layout()

                # Get translated description
                description = TrackVisualizationType.FIELD_ANALYSIS.get_description(
                    self.language_manager,
                    "Shows the length of each field in the track data."
                )

                return TrackVisualization(
                    track_number=track_num,
                    visualization_type=TrackVisualizationType.FIELD_ANALYSIS,
                    title=self.language_manager.translate(
                        "viz_field_full_title", 
                        default="Track {track_num} Field Analysis"
                    ).format(track_num=track_num) if self.language_manager else f"Track {track_num} Field Analysis",
                    description=description,
                    data={
                        "field_names": field_names,
                        "field_lengths": field_lengths,
                        "fields": fields,
                        "track_data": track_data  # Include the original track data
                    },
                    figure=fig,
                )
                
        except Exception as e:
            print(f"Error creating field analysis visualization: {str(e)}")
            import traceback
            traceback.print_exc()
            return None


class VisualizationWidget(QWidget):
    """Qt widget for displaying card data visualizations."""
    
    # Signal to request a card read from the parent
    read_card_requested = pyqtSignal()

    def __init__(self, parent=None, language_manager=None):
        """Initialize the visualization widget.
        
        Args:
            parent: Parent widget
            language_manager: Instance of LanguageManager for translations
        """
        super().__init__(parent)
        self.visualizer = CardDataVisualizer()
        self.current_visualizations = []
        self.figure_canvases = []  # Keep track of figure canvases
        self.language_manager = language_manager or LanguageManager()
        
        # Connect language change signal
        if hasattr(self.language_manager, 'language_changed'):
            self.language_manager.language_changed.connect(self.retranslate_ui)

        # Set up the UI
        self._setup_ui()
        
    def set_language_manager(self, language_manager):
        """Set the language manager for translations.
        
        Args:
            language_manager: Instance of LanguageManager
        """
        # Disconnect previous language manager if it exists
        if hasattr(self, 'language_manager') and hasattr(self.language_manager, 'language_changed'):
            try:
                self.language_manager.language_changed.disconnect(self.retranslate_ui)
            except (TypeError, RuntimeError):
                pass
                
        self.language_manager = language_manager
        
        # Connect to new language manager
        if hasattr(self.language_manager, 'language_changed'):
            self.language_manager.language_changed.connect(self.retranslate_ui)
            
        # Update UI with new translations
        self.retranslate_ui()

    def _setup_ui(self):
        """Set up the user interface."""
        # Create main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(self.main_layout)

        # Create button layout
        self.button_layout = QHBoxLayout()
        self.button_layout.setContentsMargins(0, 0, 0, 10)
        
        # Add Read Card button
        self.read_card_button = QPushButton()
        self.read_card_button.setToolTip(self.language_manager.translate("read_card_tooltip", default="Read data from a magnetic stripe card"))
        self.read_card_button.clicked.connect(self.read_card_requested.emit)
        self.button_layout.addWidget(self.read_card_button)
        
        # Add stretch to push button to the right
        self.button_layout.addStretch()
        
        # Add button layout to main layout
        self.main_layout.addLayout(self.button_layout)
        
        # Create tab widget for visualizations with a minimum size
        self.tab_widget = QTabWidget()
        self.tab_widget.setMinimumSize(800, 600)
        self.main_layout.addWidget(self.tab_widget)
        
        # Create status label
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.status_label)
        
        # Add a label for when no visualizations are available
        self.no_visualizations_label = QLabel()
        self.no_visualizations_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_visualizations_label.setStyleSheet("""
            QLabel {
                color: #666666;
                font-style: italic;
                font-size: 14px;
                padding: 20px;
            }
        """)
        self.main_layout.addWidget(self.no_visualizations_label)
        self.no_visualizations_label.setVisible(True)
        
        # Initialize UI text
        self.retranslate_ui()
        
    def retranslate_ui(self):
        """Update all UI text with current translations."""
        self.read_card_button.setText(self.language_manager.translate("btn_read_card", default="Read Card"))
        self.read_card_button.setToolTip(self.language_manager.translate("read_card_tooltip", default="Read data from a magnetic stripe card"))
        self.status_label.setText(self.language_manager.translate("lbl_status_ready", default="Ready to read card..."))
        self.no_visualizations_label.setText(self.language_manager.translate(
            "no_visualizations_available", 
            default="No visualizations available. Read a card to see visualizations."
        ))
        
        # Update tab names if they exist
        if hasattr(self, 'tab_widget') and self.tab_widget.count() > 0:
            for i in range(self.tab_widget.count()):
                tab_text = self.tab_widget.tabText(i)
                # Try to find a translation for the tab text
                translation_key = f"tab_{tab_text.lower().replace(' ', '_').replace('(', '').replace(')', '')}"
                translated_text = self.language_manager.translate(translation_key, default=tab_text)
                self.tab_widget.setTabText(i, translated_text)

    def update_visualizations(self, tracks: List[str]):
        """Update the visualizations with new track data.

        Args:
            tracks: List of track data strings [track1, track2, track3]
        """
        # Clear existing visualizations
        self.clear_visualizations()
        
        if not tracks or all(not track for track in tracks):
            self.status_label.setText(self.language_manager.translate("no_data_available", default="No data available"))
            self.no_visualizations_label.setVisible(True)
            return
            
        self.status_label.setText(self.language_manager.translate("processing_data", default="Processing card data..."))
        QApplication.processEvents()  # Update UI
        
        try:
            # Generate new visualizations
            self.current_visualizations = self.visualizer.create_visualizations(tracks)
            
            # If no visualizations were created, show message and return
            if not self.current_visualizations:
                self.no_visualizations_label.setVisible(True)
                self.no_visualizations_label.setText(self.language_manager.translate(
                    "no_visualizations_available", 
                    default="No visualizations available for the current track data."
                ))
                return
                
            # Hide the no visualizations label
            self.no_visualizations_label.setVisible(False)
            
            # Track if we've added any visualizations
            visualizations_added = False
            
            # Add visualizations to tabs
            for vis in self.current_visualizations:
                if vis and vis.figure:
                    try:
                        # Create a container widget with layout
                        container = QWidget()
                        layout = QVBoxLayout(container)
                        layout.setContentsMargins(10, 10, 10, 10)
                        layout.setSpacing(10)
                        
                        # Add a title label
                        title_text = self.language_manager.translate(
                            f"viz_{vis.visualization_type.value[0]}_title".lower(),
                            default=vis.visualization_type.get_display_name()
                        )
                        title_label = QLabel(title_text)
                        title_label.setStyleSheet("""
                            QLabel {
                                font-size: 14px;
                                font-weight: bold;
                                padding: 5px;
                                border-bottom: 1px solid #444444;
                                margin-bottom: 10px;
                            }
                        """)
                        layout.addWidget(title_label)
                        layout.addWidget(desc_label)
                        
                        # Create the matplotlib canvas with a frame
                        canvas_frame = QFrame()
                        canvas_frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
                        canvas_frame.setStyleSheet("""
                            QFrame {
                                background-color: #ffffff;
                                border: 1px solid #dddddd;
                                border-radius: 4px;
                            }
                        """)
                        canvas_layout = QVBoxLayout(canvas_frame)
                        canvas_layout.setContentsMargins(5, 5, 5, 5)
                        
                        canvas = FigureCanvas(vis.figure)
                        canvas.setSizePolicy(
                            QSizePolicy.Policy.Expanding, 
                            QSizePolicy.Policy.Expanding
                        )
                        
                        # Add the canvas to the frame layout
                        canvas_layout.addWidget(canvas)
                        
                        # Add the frame to the main layout
                        layout.addWidget(canvas_frame, 1)  # 1 is stretch factor
                        
                        # Create a scroll area for the widget
                        scroll = QScrollArea()
                        scroll.setWidgetResizable(True)
                        scroll.setWidget(container)
                        
                        # Add the scroll area to a new tab
                        self.tab_widget.addTab(scroll, f"{vis.visualization_type.value} (T{vis.track_number})")
                        
                        # Store the canvas to prevent garbage collection
                        self.figure_canvases.append({
                            'canvas': canvas,
                            'figure': vis.figure
                        })
                        
                        # Force a draw of the canvas
                        canvas.draw()
                        
                        # Mark that we've added at least one visualization
                        visualizations_added = True
                        
                        # Process events to ensure the canvas is displayed
                        QApplication.processEvents()
                        
                    except Exception as e:
                        print(f"Error creating visualization tab: {str(e)}")
                        import traceback
                        traceback.print_exc()
                        continue
            
            # If no visualizations were successfully added, show the message
            if not visualizations_added:
                self.no_visualizations_label.setVisible(True)
                self.no_visualizations_label.setText("Failed to create any visualizations. See console for errors.")
            
            # If we have tabs, make sure the first one is selected
            if self.tab_widget.count() > 0:
                self.tab_widget.setCurrentIndex(0)
                
        except Exception as e:
            print(f"Error updating visualizations: {str(e)}")
            import traceback
            traceback.print_exc()
            self.no_visualizations_label.setVisible(True)
            self.no_visualizations_label.setText(f"Error creating visualizations: {str(e)}")
            import traceback
            traceback.print_exc()
            self.no_visualizations_label.setText(f"Error generating visualizations: {str(e)}")
            self.no_visualizations_label.setVisible(True)

    def clear_visualizations(self):
        """Clear all current visualizations."""
        # Remove all tabs
        while self.tab_widget.count() > 0:
            widget = self.tab_widget.widget(0)
            self.tab_widget.removeTab(0)
            if widget:
                widget.deleteLater()
        
        # Clear the list of visualizations and canvases
        self.current_visualizations = []
        self.figure_canvases = []
        
        # Show the "no visualizations" message
        self.no_visualizations_label.setVisible(True)

    def set_theme(self, theme: str):
        """Set the visualization theme.

        Args:
            theme: Theme name (e.g., 'dark_background', 'default')
        """
        try:
            self.visualizer.set_theme(theme)
            
            # If we have visualizations, update them with the new theme
            if self.current_visualizations:
                # Extract track data from existing visualizations
                track_data = ["", "", ""]
                for vis in self.current_visualizations:
                    if hasattr(vis, 'data') and 'track_data' in vis.data:
                        track_num = vis.track_number - 1  # Convert to 0-based index
                        if 0 <= track_num < 3:
                            track_data[track_num] = vis.data['track_data']
                
                # Only update if we have track data
                if any(track_data):
                    self.update_visualizations(track_data)
        except Exception as e:
            print(f"Error setting theme: {str(e)}")


# Example usage
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    # Sample track data for testing
    sample_tracks = [
        "%B1234567890123456^DOE/JOHN^24051234567890123456789?",  # Track 1
        ";1234567890123456=240512345678901?",  # Track 2
        ";123=4567890123456789012345678901234567890?",  # Track 3
    ]

    # Create application
    app = QApplication(sys.argv)

    # Create and show visualization widget
    widget = VisualizationWidget()
    widget.update_visualizations(sample_tracks)
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
