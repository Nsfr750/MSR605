#!/usr/bin/env python3

"""test_card_reader.py

Unit tests for the cardReader.py module with ISO 7811 and ISO 7813 support.
"""

import unittest
import sys
import os
from unittest.mock import MagicMock, patch
from pathlib import Path

# Add the script directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "script"))

from script.cardReader import CardReader
from script.card_formats import CardFormat


class TestCardReader(unittest.TestCase):
    """Test the CardReader class with ISO 7811 and ISO 7813 support."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a mock serial connection
        self.mock_serial = MagicMock()
        self.mock_serial.read.side_effect = [
            b"\x1b",
            b"s",
            b"\x1b",
            b"1",
            b"%",
            b"B",
            b"1",
            b"2",
            b"3",
            b"4",
            b"5",
            b"6",
            b"7",
            b"8",
            b"9",
            b"0",
            b"1",
            b"2",
            b"3",
            b"4",
            b"5",
            b"6",
            b"^",
            b"T",
            b"E",
            b"S",
            b"T",
            b" ",
            b"C",
            b"A",
            b"R",
            b"D",
            b"^",
            b"2",
            b"4",
            b"0",
            b"1",
            b"1",
            b"2",
            b"3",
            b"4",
            b"5",
            b"6",
            b"7",
            b"8",
            b"9",
            b"0",
            b"1",
            b"2",
            b"3",
            b"4",
            b"5",
            b"6",
            b"7",
            b"8",
            b"9",
            b"?",
            b"\x1b",
            b"2",
            b";",
            b"1",
            b"2",
            b"3",
            b"4",
            b"5",
            b"6",
            b"7",
            b"8",
            b"9",
            b"0",
            b"1",
            b"2",
            b"3",
            b"4",
            b"5",
            b"6",
            b"=",
            b"2",
            b"4",
            b"0",
            b"1",
            b"1",
            b"2",
            b"3",
            b"4",
            b"5",
            b"6",
            b"7",
            b"8",
            b"9",
            b"0",
            b"1",
            b"2",
            b"3",
            b"4",
            b"5",
            b"6",
            b"?",
            b"\x1b",
            b"3",
            b";",
            b"1",
            b"2",
            b"3",
            b"4",
            b"5",
            b"6",
            b"7",
            b"8",
            b"9",
            b"0",
            b"1",
            b"2",
            b"3",
            b"4",
            b"5",
            b"6",
            b"7",
            b"8",
            b"9",
            b"0",
            b"1",
            b"2",
            b"3",
            b"4",
            b"5",
            b"6",
            b"7",
            b"8",
            b"9",
            b"0",
            b"1",
            b"2",
            b"3",
            b"4",
            b"5",
            b"6",
            b"7",
            b"8",
            b"9",
            b"0",
            b"1",
            b"2",
            b"3",
            b"4",
            b"5",
            b"6",
            b"7",
            b"8",
            b"9",
            b"0",
            b"?",
            b"\x1c",
            b"\x1b",
            b"0",
            b"\x1b",
            b"0",
        ]

        # Patch the serial.Serial class to return our mock
        self.patcher = patch("serial.Serial")
        self.mock_serial_class = self.patcher.start()
        self.mock_serial_class.return_value = self.mock_serial

        # Create a CardReader instance
        self.reader = CardReader(port="COM1")

    def tearDown(self):
        """Tear down test fixtures."""
        self.patcher.stop()

    def test_set_card_format(self):
        """Test setting the card format."""
        # Default format should be ISO_7811
        self.assertEqual(self.reader.get_card_format(), CardFormat.ISO_7811)

        # Change to ISO_7813
        self.reader.set_card_format(CardFormat.ISO_7813)
        self.assertEqual(self.reader.get_card_format(), CardFormat.ISO_7813)

        # Try setting an invalid format (should raise ValueError)
        with self.assertRaises(ValueError):
            self.reader.set_card_format("INVALID_FORMAT")

    def test_validate_track_data(self):
        """Test track data validation."""
        # Valid ISO 7813 track 1 data
        valid_track1 = "%B1234567890123456^CARDHOLDER/NAME^24011234567890123456789?"
        is_valid, msg = self.reader.validate_track_data(1, valid_track1)
        self.assertTrue(is_valid, msg=msg)

        # Invalid track data (wrong format)
        invalid_track1 = "INVALID_TRACK_DATA"
        is_valid, msg = self.reader.validate_track_data(1, invalid_track1)
        self.assertFalse(is_valid)
        self.assertNotEqual(msg, "")

    @patch("builtins.print")
    def test_read_card(self, mock_print):
        """Test reading a card with format detection."""
        # Configure the mock serial to return a valid card read response
        self.mock_serial.read.side_effect = [
            b"\x1b",
            b"s",  # Start of data block
            b"\x1b",
            b"1",  # Track 1 start
            b"%",
            b"B",
            b"1",
            b"2",
            b"3",
            b"4",
            b"5",
            b"6",
            b"7",
            b"8",
            b"9",
            b"0",  # Track 1 data
            b"^",
            b"T",
            b"E",
            b"S",
            b"T",
            b" ",
            b"C",
            b"A",
            b"R",
            b"D",  # More track 1 data
            b"^",
            b"2",
            b"4",
            b"0",
            b"1",
            b"1",
            b"2",
            b"3",
            b"4",
            b"5",
            b"6",
            b"7",
            b"8",
            b"9",  # More track 1 data
            b"0",
            b"1",
            b"2",
            b"3",
            b"4",
            b"5",
            b"6",
            b"7",
            b"8",
            b"9",
            b"?",  # End of track 1
            b"\x1b",
            b"2",  # Track 2 start
            b";",
            b"1",
            b"2",
            b"3",
            b"4",
            b"5",
            b"6",
            b"7",
            b"8",
            b"9",
            b"0",
            b"1",
            b"2",
            b"3",
            b"4",
            b"5",
            b"6",  # Track 2 data
            b"=",
            b"2",
            b"4",
            b"0",
            b"1",
            b"1",
            b"2",
            b"3",
            b"4",
            b"5",
            b"6",
            b"7",
            b"8",
            b"9",  # More track 2 data
            b"0",
            b"1",
            b"2",
            b"3",
            b"4",
            b"5",
            b"6",
            b"?",  # End of track 2
            b"\x1c",
            b"\x1b",
            b"0",  # End of data block
            b"\x1b",
            b"0",  # Status byte
        ]

        # Read the card with format detection
        result = self.reader.read_card(detect_format=True)

        # Check the result
        self.assertIn("tracks", result)
        self.assertIn("format", result)
        self.assertIn("parsed", result)

        # Check track data
        self.assertIn(
            "B1234567890123456^TEST CARD^24011234567890123456789", result["tracks"][0]
        )
        self.assertIn("1234567890123456=24011234567890123456", result["tracks"][1])

        # Check parsed data
        self.assertIn("track1", result["parsed"])
        self.assertEqual(
            result["parsed"]["track1"]["primary_account_number"], "B1234567890123456"
        )
        self.assertEqual(result["parsed"]["track1"]["name"], "TEST CARD")

    @patch("builtins.print")
    def test_write_card(self, mock_print):
        """Test writing to a card with format validation."""
        # Configure the mock serial to return success status
        self.mock_serial.read.return_value = b"0"  # Success status

        # Test data for ISO 7813 format
        tracks = [
            "%B1234567890123456^CARDHOLDER/NAME^24011234567890123456789?",
            ";1234567890123456=24011234567890123456?",
            ";1234567890123456789012345678901234567890=1234567890123456789012345678901234567890?",
        ]

        # Write the card with ISO 7813 format
        result = self.reader.write_card(tracks, format_override=CardFormat.ISO_7813)

        # Check the result
        self.assertTrue(result["success"])
        self.assertEqual(result["format"], "ISO_7813")

        # Verify the write command was sent
        self.mock_serial.write.assert_called()

    def test_detect_card_format(self):
        """Test automatic card format detection."""
        # ISO 7813 track 1 data
        iso7813_track1 = "%B1234567890123456^CARDHOLDER/NAME^24011234567890123456789?"

        # ISO 7811 track 1 data (with format code 'A' which is not in ISO 7813)
        iso7811_track1 = "%A1234567890123456^CARDHOLDER/NAME^24011234567890123456789?"

        # Test with ISO 7813 data
        self.reader._detect_card_format([iso7813_track1, "", ""])
        self.assertEqual(self.reader.get_card_format(), CardFormat.ISO_7813)

        # Test with ISO 7811 data
        self.reader._detect_card_format([iso7811_track1, "", ""])
        self.assertEqual(self.reader.get_card_format(), CardFormat.ISO_7811)

    def test_parse_track_data(self):
        """Test parsing of track data."""
        # Create a result dictionary with track data
        result = {
            "tracks": [
                "%B1234567890123456^CARDHOLDER/NAME^24011234567890123456789?",
                ";1234567890123456=24011234567890123456?",
                ";1234567890123456789012345678901234567890=1234567890123456789012345678901234567890?",
            ],
            "format": "ISO_7813",
        }

        # Parse the track data
        self.reader._parse_track_data(result)

        # Check that the parsed data was added to the result
        self.assertIn("parsed", result)
        self.assertIn("track1", result["parsed"])
        self.assertIn("track2", result["parsed"])
        self.assertIn("track3", result["parsed"])

        # Check some parsed values
        self.assertEqual(
            result["parsed"]["track1"]["primary_account_number"], "B1234567890123456"
        )
        self.assertEqual(result["parsed"]["track1"]["name"], "CARDHOLDER/NAME")
        self.assertEqual(
            result["parsed"]["track2"]["primary_account_number"], "1234567890123456"
        )


if __name__ == "__main__":
    unittest.main()
