#!/usr/bin/env python3

"""visualization.py

This module provides advanced visualization capabilities for card data,
including track analysis, data distribution, and interactive charts.
"""

from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import re
import math
from collections import Counter

# Import visualization libraries
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QSizePolicy
from PyQt6.QtCore import Qt


class TrackVisualizationType(Enum):
    """Types of visualizations available for track data."""

    CHARACTER_DISTRIBUTION = "Character Distribution"
    BIT_PATTERN = "Bit Pattern"
    DATA_DENSITY = "Data Density"
    FIELD_ANALYSIS = "Field Analysis"


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

    def __init__(self):
        """Initialize the visualizer with default settings."""
        self.theme = "dark_background"  # Default theme
        self.figure_size = (8, 6)  # Default figure size in inches (width, height)
        self.dpi = 100  # Dots per inch for figures

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

        # Count character frequencies
        char_counts = Counter(track_data)

        if not char_counts:
            return None

        # Sort characters by frequency
        chars, counts = zip(
            *sorted(char_counts.items(), key=lambda x: x[1], reverse=True)
        )

        # Create figure
        with plt.style.context(self.theme):
            fig = Figure(figsize=self.figure_size, dpi=self.dpi)
            ax = fig.add_subplot(111)

            # Create bar chart
            bars = ax.bar(range(len(chars)), counts, color="skyblue")

            # Customize x-axis
            ax.set_xticks(range(len(chars)))
            ax.set_xticklabels([repr(c)[1:-1] for c in chars], rotation=45, ha="right")

            # Add value labels on top of bars
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height,
                    f"{int(height)}",
                    ha="center",
                    va="bottom",
                )

            # Set labels and title
            ax.set_xlabel("Character")
            ax.set_ylabel("Frequency")
            ax.set_title(f"Track {track_num} - Character Distribution")

            # Adjust layout to prevent label cutoff
            fig.tight_layout()

            return TrackVisualization(
                track_number=track_num,
                visualization_type=TrackVisualizationType.CHARACTER_DISTRIBUTION,
                title=f"Track {track_num} Character Distribution",
                description="Shows the frequency of each character in the track data.",
                data={"characters": chars, "counts": counts},
                figure=fig,
            )

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

        # Convert characters to binary representation
        binary_data = []
        for char in track_data:
            # Get 8-bit binary representation
            binary = format(ord(char), "08b")
            binary_data.extend([int(bit) for bit in binary])

        if not binary_data:
            return None

        # Create figure
        with plt.style.context(self.theme):
            fig = Figure(figsize=(10, 2), dpi=self.dpi)
            ax = fig.add_subplot(111)

            # Create a line plot of the bit pattern
            ax.step(range(len(binary_data)), binary_data, where="mid", color="lime")

            # Customize y-axis
            ax.set_yticks([0, 1])
            ax.set_yticklabels(["0", "1"])

            # Set labels and title
            ax.set_xlabel("Bit Position")
            ax.set_ylabel("Bit Value")
            ax.set_title(f"Track {track_num} - Bit Pattern")

            # Adjust layout
            fig.tight_layout()

            return TrackVisualization(
                track_number=track_num,
                visualization_type=TrackVisualizationType.BIT_PATTERN,
                title=f"Track {track_num} Bit Pattern",
                description="Shows the binary representation of the track data.",
                data={"binary_data": binary_data},
                figure=fig,
            )

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

        # Calculate density metrics
        length = len(track_data)
        unique_chars = len(set(track_data))
        char_density = unique_chars / length if length > 0 else 0

        # Create figure
        with plt.style.context(self.theme):
            fig = Figure(figsize=self.figure_size, dpi=self.dpi)
            ax = fig.add_subplot(111)

            # Create bar chart of metrics
            metrics = ["Length", "Unique Chars", "Density"]
            values = [length, unique_chars, char_density]

            bars = ax.bar(metrics, values, color=["skyblue", "lightgreen", "salmon"])

            # Add value labels on top of bars
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height,
                    f"{height:.2f}" if isinstance(height, float) else f"{int(height)}",
                    ha="center",
                    va="bottom",
                )

            # Set labels and title
            ax.set_ylabel("Value")
            ax.set_title(f"Track {track_num} - Data Density Metrics")

            # Adjust layout
            fig.tight_layout()

            return TrackVisualization(
                track_number=track_num,
                visualization_type=TrackVisualizationType.DATA_DENSITY,
                title=f"Track {track_num} Data Density",
                description="Shows metrics about the data density of the track.",
                data={
                    "length": length,
                    "unique_chars": unique_chars,
                    "char_density": char_density,
                },
                figure=fig,
            )

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

        # Try to parse fields (this is a simple approach, adjust based on actual format)
        fields = []

        # Try different field separators
        if "^" in track_data:
            fields = track_data.split("^")
            field_names = [f"Field {i+1}" for i in range(len(fields))]
        elif "=" in track_data:
            fields = track_data.split("=")
            field_names = [f"Field {i+1}" for i in range(len(fields))]
        else:
            # No clear field separators found
            return None

        if not fields:
            return None

        # Calculate field lengths
        field_lengths = [len(field) for field in fields]

        # Create figure
        with plt.style.context(self.theme):
            fig = Figure(figsize=self.figure_size, dpi=self.dpi)
            ax = fig.add_subplot(111)

            # Create bar chart of field lengths
            bars = ax.bar(field_names, field_lengths, color="lightblue")

            # Add value labels on top of bars
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height,
                    f"{int(height)}",
                    ha="center",
                    va="bottom",
                )

            # Set labels and title
            ax.set_ylabel("Length (chars)")
            ax.set_xlabel("Field")
            ax.set_title(f"Track {track_num} - Field Analysis")

            # Rotate x-axis labels for better readability
            plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

            # Adjust layout
            fig.tight_layout()

            return TrackVisualization(
                track_number=track_num,
                visualization_type=TrackVisualizationType.FIELD_ANALYSIS,
                title=f"Track {track_num} Field Analysis",
                description="Shows the length of each field in the track data.",
                data={
                    "field_names": field_names,
                    "field_lengths": field_lengths,
                    "fields": fields,
                },
                figure=fig,
            )


class VisualizationWidget(QWidget):
    """Qt widget for displaying card data visualizations."""

    def __init__(self, parent=None):
        """Initialize the visualization widget."""
        super().__init__(parent)
        self.visualizer = CardDataVisualizer()
        self.current_visualizations = []

        # Set up the UI
        self._setup_ui()

    def _setup_ui(self):
        """Set up the user interface."""
        # Main layout
        layout = QVBoxLayout(self)

        # Create tab widget for visualizations
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(False)
        self.tab_widget.setDocumentMode(True)

        layout.addWidget(self.tab_widget)

    def update_visualizations(self, tracks: List[str]):
        """Update the visualizations with new track data.

        Args:
            tracks: List of track data strings [track1, track2, track3]
        """
        # Clear existing visualizations
        self.clear_visualizations()

        # Generate new visualizations
        self.current_visualizations = self.visualizer.create_visualizations(tracks)

        # Add visualizations to tabs
        for vis in self.current_visualizations:
            if vis.figure:
                # Create a canvas for the figure
                canvas = FigureCanvas(vis.figure)
                canvas.setSizePolicy(
                    QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
                )

                # Add the canvas to a new tab
                self.tab_widget.addTab(canvas, vis.title)

    def clear_visualizations(self):
        """Clear all current visualizations."""
        # Clear tabs
        while self.tab_widget.count() > 0:
            widget = self.tab_widget.widget(0)
            self.tab_widget.removeTab(0)
            if widget:
                widget.deleteLater()

        # Clear visualization list
        self.current_visualizations = []

    def set_theme(self, theme: str):
        """Set the visualization theme.

        Args:
            theme: Theme name (e.g., 'dark_background', 'default')
        """
        self.visualizer.theme = theme

        # Update existing visualizations if any
        if self.current_visualizations:
            current_tracks = [
                vis.data.get("track_data", "") for vis in self.current_visualizations
            ]
            self.update_visualizations(current_tracks)


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
