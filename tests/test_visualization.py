#!/usr/bin/env python3

"""
Test cases for the visualization module.
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add the parent directory to the path to allow importing from the script directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the module to test
from script.visualization import (
    CardDataVisualizer,
    TrackVisualization,
    TrackVisualizationType,
    VisualizationWidget,
)
from PyQt6.QtWidgets import QApplication

# Sample track data for testing
SAMPLE_TRACK_1 = "%B1234567890123456^DOE/JOHN^24051234567890123456789?"
SAMPLE_TRACK_2 = ";1234567890123456=240512345678901?"
SAMPLE_TRACK_3 = ";123=4567890123456789012345678901234567890?"


class TestCardDataVisualizer(unittest.TestCase):
    """Test cases for CardDataVisualizer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.visualizer = CardDataVisualizer()
        self.tracks = [SAMPLE_TRACK_1, SAMPLE_TRACK_2, SAMPLE_TRACK_3]

    def test_create_visualizations(self):
        """Test creating visualizations from track data."""
        visualizations = self.visualizer.create_visualizations(self.tracks)

        # Should create visualizations for each track
        self.assertGreaterEqual(len(visualizations), 3)

        # Check that we have at least one of each visualization type
        vis_types = set(v.visualization_type for v in visualizations)
        self.assertIn(TrackVisualizationType.CHARACTER_DISTRIBUTION, vis_types)
        self.assertIn(TrackVisualizationType.BIT_PATTERN, vis_types)
        self.assertIn(TrackVisualizationType.DATA_DENSITY, vis_types)
        self.assertIn(TrackVisualizationType.FIELD_ANALYSIS, vis_types)

    def test_character_distribution(self):
        """Test character distribution visualization."""
        vis = self.visualizer._create_character_distribution(SAMPLE_TRACK_1, 1)
        self.assertIsNotNone(vis)
        self.assertEqual(vis.track_number, 1)
        self.assertEqual(
            vis.visualization_type, TrackVisualizationType.CHARACTER_DISTRIBUTION
        )
        self.assertIn("characters", vis.data)
        self.assertIn("counts", vis.data)
        self.assertIsNotNone(vis.figure)

    def test_bit_pattern(self):
        """Test bit pattern visualization."""
        vis = self.visualizer._create_bit_pattern(SAMPLE_TRACK_2, 2)
        self.assertIsNotNone(vis)
        self.assertEqual(vis.track_number, 2)
        self.assertEqual(vis.visualization_type, TrackVisualizationType.BIT_PATTERN)
        self.assertIn("binary_data", vis.data)
        self.assertIsNotNone(vis.figure)

    def test_data_density(self):
        """Test data density visualization."""
        vis = self.visualizer._create_data_density(SAMPLE_TRACK_3, 3)
        self.assertIsNotNone(vis)
        self.assertEqual(vis.track_number, 3)
        self.assertEqual(vis.visualization_type, TrackVisualizationType.DATA_DENSITY)
        self.assertIn("length", vis.data)
        self.assertIn("unique_chars", vis.data)
        self.assertIn("char_density", vis.data)
        self.assertIsNotNone(vis.figure)

    def test_field_analysis(self):
        """Test field analysis visualization."""
        vis = self.visualizer._create_field_analysis(SAMPLE_TRACK_1, 1)
        self.assertIsNotNone(vis)
        self.assertEqual(vis.track_number, 1)
        self.assertEqual(vis.visualization_type, TrackVisualizationType.FIELD_ANALYSIS)
        self.assertIn("field_names", vis.data)
        self.assertIn("field_lengths", vis.data)
        self.assertIn("fields", vis.data)
        self.assertIsNotNone(vis.figure)

    def test_empty_track(self):
        """Test with empty track data."""
        vis = self.visualizer._create_character_distribution("", 1)
        self.assertIsNone(vis)


class TestVisualizationWidget(unittest.TestCase):
    """Test cases for VisualizationWidget class."""

    @classmethod
    def setUpClass(cls):
        """Set up the QApplication instance for testing."""
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication([])

    def setUp(self):
        """Set up test fixtures."""
        self.widget = VisualizationWidget()

    def test_initialization(self):
        """Test widget initialization."""
        self.assertIsNotNone(self.widget.visualizer)
        self.assertEqual(len(self.widget.current_visualizations), 0)

    def test_update_visualizations(self):
        """Test updating visualizations with track data."""
        tracks = [SAMPLE_TRACK_1, SAMPLE_TRACK_2, SAMPLE_TRACK_3]
        self.widget.update_visualizations(tracks)

        # Should have visualizations for each track
        self.assertGreater(len(self.widget.current_visualizations), 0)

        # Tab widget should have tabs for each visualization
        self.assertGreater(self.widget.tab_widget.count(), 0)

    def test_clear_visualizations(self):
        """Test clearing visualizations."""
        # First add some visualizations
        self.widget.update_visualizations([SAMPLE_TRACK_1])
        self.assertGreater(len(self.widget.current_visualizations), 0)

        # Then clear them
        self.widget.clear_visualizations()
        self.assertEqual(len(self.widget.current_visualizations), 0)
        self.assertEqual(self.widget.tab_widget.count(), 0)

    def test_set_theme(self):
        """Test changing the visualization theme."""
        # This is a simple test that just verifies the method runs
        self.widget.set_theme("dark_background")
        self.assertEqual(self.widget.visualizer.theme, "dark_background")

        # Change to a different theme
        self.widget.set_theme("default")
        self.assertEqual(self.widget.visualizer.theme, "default")


if __name__ == "__main__":
    unittest.main()
