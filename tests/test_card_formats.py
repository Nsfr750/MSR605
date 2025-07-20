#!/usr/bin/env python3

"""test_card_formats.py

Unit tests for the card_formats.py module which provides support for
ISO 7811 and ISO 7813 magnetic card formats.
"""

import unittest
import sys
import os
from pathlib import Path

# Add the script directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "script"))

from card_formats import CardFormat, CardFormatManager, TrackSpecification


class TestCardFormats(unittest.TestCase):
    def test_card_format_enum(self):
        """Test that the CardFormat enum is defined correctly."""
        self.assertEqual(len(CardFormat), 2)
        self.assertIn("ISO_7811", CardFormat.__members__)
        self.assertIn("ISO_7813", CardFormat.__members__)

    def test_track_specifications(self):
        """Test that track specifications are loaded correctly."""
        # Check that we have specs for both formats and all tracks
        for fmt in CardFormat:
            for track_num in [1, 2, 3]:
                if track_num == 3 and fmt == CardFormat.ISO_7811:
                    # ISO 7811 doesn't have track 3
                    with self.assertRaises(ValueError):
                        CardFormatManager.get_track_spec(fmt, track_num)
                else:
                    spec = CardFormatManager.get_track_spec(fmt, track_num)
                    self.assertIsInstance(spec, TrackSpecification)
                    self.assertEqual(spec.format_name, fmt.name)
                    self.assertGreater(spec.max_length, 0)
                    self.assertIsInstance(spec.allowed_chars, str)
                    self.assertGreater(len(spec.allowed_chars), 0)

    def test_iso_7811_track1_validation(self):
        """Test ISO 7811 track 1 validation."""
        fmt = CardFormat.ISO_7811
        track_num = 1

        # Valid track 1 data
        valid_track1 = "%B1234567890123456^CARDHOLDER/NAME^24011234567890123456789?"
        is_valid, msg = CardFormatManager.validate_track_data(
            fmt, track_num, valid_track1
        )
        self.assertTrue(is_valid, msg=msg)

        # Invalid start sentinel
        invalid1 = "#B1234567890123456^CARDHOLDER/NAME^24011234567890123456789?"
        is_valid, msg = CardFormatManager.validate_track_data(fmt, track_num, invalid1)
        self.assertFalse(is_valid)
        self.assertIn("must start with", msg)

        # Invalid character
        invalid2 = "%B1234567890123456^CARDHOLDER/NAME^2401123456789012345678~?"
        is_valid, msg = CardFormatManager.validate_track_data(fmt, track_num, invalid2)
        self.assertFalse(is_valid)
        self.assertIn("invalid character", msg)

    def test_iso_7813_track2_validation(self):
        """Test ISO 7813 track 2 validation."""
        fmt = CardFormat.ISO_7813
        track_num = 2

        # Valid track 2 data
        valid_track2 = ";1234567890123456=24011234567890123456?"
        is_valid, msg = CardFormatManager.validate_track_data(
            fmt, track_num, valid_track2
        )
        self.assertTrue(is_valid, msg=msg)

        # Invalid end sentinel
        invalid1 = ";1234567890123456=24011234567890123456#"
        is_valid, msg = CardFormatManager.validate_track_data(fmt, track_num, invalid1)
        self.assertFalse(is_valid)
        self.assertIn("must end with", msg)

    def test_iso_7813_track3_validation(self):
        """Test ISO 7813 track 3 validation."""
        fmt = CardFormat.ISO_7813
        track_num = 3

        # Valid track 3 data (simplified example)
        valid_track3 = ";1234567890123456789012345678901234567890=1234567890123456789012345678901234567890?"
        is_valid, msg = CardFormatManager.validate_track_data(
            fmt, track_num, valid_track3
        )
        self.assertTrue(is_valid, msg=msg)

        # Track 3 is only numeric in ISO 7813
        invalid1 = ";1234567890123456=ABC123?"
        is_valid, msg = CardFormatManager.validate_track_data(fmt, track_num, invalid1)
        self.assertFalse(is_valid)
        self.assertIn("invalid character", msg)

    def test_format_track_data(self):
        """Test formatting of track data."""
        fmt = CardFormat.ISO_7813
        track_num = 1

        # Test with missing sentinels
        raw_data = "B1234567890123456^CARDHOLDER/NAME^24011234567890123456789"
        formatted = CardFormatManager.format_track_data(fmt, track_num, raw_data)
        self.assertTrue(formatted.startswith("%"))
        self.assertTrue(formatted.endswith("?"))

        # Test with existing sentinels
        already_formatted = (
            "%B1234567890123456^CARDHOLDER/NAME^24011234567890123456789?"
        )
        reformatted = CardFormatManager.format_track_data(
            fmt, track_num, already_formatted
        )
        self.assertEqual(reformatted, already_formatted)

    def test_parse_track_data(self):
        """Test parsing of track data into fields."""
        fmt = CardFormat.ISO_7813

        # Test track 1 parsing
        track1 = "%B1234567890123456^CARDHOLDER/NAME^24011234567890123456789?"
        parsed = CardFormatManager.parse_track_data(fmt, 1, track1)
        self.assertEqual(parsed["format"], "ISO_7813")
        self.assertEqual(parsed["track"], 1)
        self.assertEqual(parsed["primary_account_number"], "B1234567890123456")
        self.assertEqual(parsed["name"], "CARDHOLDER/NAME")

        # Test track 2 parsing
        track2 = ";1234567890123456=24011234567890123456?"
        parsed = CardFormatManager.parse_track_data(fmt, 2, track2)
        self.assertEqual(parsed["primary_account_number"], "1234567890123456")
        self.assertEqual(parsed["additional_data"], "24011234567890123456")

    def test_invalid_track_number(self):
        """Test handling of invalid track numbers."""
        with self.assertRaises(ValueError):
            CardFormatManager.get_track_spec(
                CardFormat.ISO_7811, 4
            )  # Invalid track number

        with self.assertRaises(ValueError):
            CardFormatManager.get_track_spec(
                CardFormat.ISO_7811, 0
            )  # Invalid track number

    def test_format_detection(self):
        """Test automatic format detection based on track data."""
        # ISO 7813 track 1 with format code 'B' (banking)
        track1 = "%B1234567890123456^CARDHOLDER/NAME^24011234567890123456789?"

        # This should be detected as ISO 7813
        is_valid_7813, _ = CardFormatManager.validate_track_data(
            CardFormat.ISO_7813, 1, track1
        )
        self.assertTrue(is_valid_7813)

        # It should also be valid ISO 7811 (less strict)
        is_valid_7811, _ = CardFormatManager.validate_track_data(
            CardFormat.ISO_7811, 1, track1
        )
        self.assertTrue(is_valid_7811)

        # But a track with ISO 7811-specific characters shouldn't be valid in ISO 7813
        track1_7811 = "%A1234567890123456^CARDHOLDER/NAME^24011234567890123456789?"
        is_valid_7813, _ = CardFormatManager.validate_track_data(
            CardFormat.ISO_7813, 1, track1_7811
        )
        self.assertFalse(is_valid_7813)


if __name__ == "__main__":
    unittest.main()
