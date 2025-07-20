#!/usr/bin/env python3

"""card_formats.py

This module provides support for different magnetic card formats including
ISO 7811 and ISO 7813 standards. It handles encoding, decoding, and validation
of card data according to these standards.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


class CardFormat(Enum):
    """Enumeration of supported card formats."""

    ISO_7811 = auto()  # ISO 7811: Magnetic stripe cards
    ISO_7813 = auto()  # ISO 7813: Financial transaction cards


@dataclass
class TrackSpecification:
    """Specification for a magnetic track format."""

    name: str
    format_name: str
    start_sentinel: str
    end_sentinel: str
    field_separator: str
    max_length: int
    allowed_chars: str
    lrc_required: bool = False
    lrc_length: int = 1


class CardFormatManager:
    """Manages card format specifications and operations."""

    # Track specifications for different formats
    _track_specs = {
        # ISO 7811 Format (Basic magnetic stripe cards)
        (CardFormat.ISO_7811, 1): TrackSpecification(
            name="Track 1 (ISO 7811)",
            format_name="ISO 7811",
            start_sentinel="%",
            end_sentinel="?",
            field_separator="^",
            max_length=79,
            allowed_chars=(
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ "  # Uppercase letters and space
                "0123456789:;<=>?@"  # Numbers and special chars
                "!\"#&'()*+,-./"  # Additional special chars
                "[\\]^_"  # More special chars
            ),
            lrc_required=True,
        ),
        (CardFormat.ISO_7811, 2): TrackSpecification(
            name="Track 2 (ISO 7811)",
            format_name="ISO 7811",
            start_sentinel=";",
            end_sentinel="?",
            field_separator="=",
            max_length=40,
            allowed_chars="0123456789:;<=>?",
            lrc_required=True,
        ),
        # ISO 7813 Format (Financial transaction cards)
        (CardFormat.ISO_7813, 1): TrackSpecification(
            name="Track 1 (ISO 7813)",
            format_name="ISO 7813",
            start_sentinel="%",
            end_sentinel="?",
            field_separator="^",
            max_length=79,
            allowed_chars=(
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ "  # Uppercase letters and space
                "0123456789"  # Numbers
                "!\"#&'()*+,-./:;<=>?@[\\]^_"  # Special chars
            ),
            lrc_required=True,
        ),
        (CardFormat.ISO_7813, 2): TrackSpecification(
            name="Track 2 (ISO 7813)",
            format_name="ISO 7813",
            start_sentinel=";",
            end_sentinel="?",
            field_separator="=",
            max_length=40,
            allowed_chars="0123456789:;<=>?",
            lrc_required=True,
        ),
        (CardFormat.ISO_7813, 3): TrackSpecification(
            name="Track 3 (ISO 7813)",
            format_name="ISO 7813",
            start_sentinel=";",
            end_sentinel="?",
            field_separator="=",
            max_length=107,
            allowed_chars="0123456789",
            lrc_required=True,
        ),
    }

    @classmethod
    def get_track_spec(
        cls, format_type: CardFormat, track_num: int
    ) -> TrackSpecification:
        """Get the track specification for a given format and track number."""
        key = (format_type, track_num)
        if key not in cls._track_specs:
            raise ValueError(
                f"Unsupported format/track combination: {format_type.name}/Track {track_num}"
            )
        return cls._track_specs[key]

    @classmethod
    def validate_track_data(
        cls, format_type: CardFormat, track_num: int, data: str
    ) -> Tuple[bool, str]:
        """Validate track data against the specified format.

        Args:
            format_type: The card format (ISO_7811 or ISO_7813)
            track_num: Track number (1, 2, or 3)
            data: The track data to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            spec = cls.get_track_spec(format_type, track_num)
        except ValueError as e:
            return False, str(e)

        # Check length
        if len(data) > spec.max_length:
            return (
                False,
                f"Track {track_num} data exceeds maximum length of {spec.max_length} characters",
            )

        # Check start sentinel
        if not data.startswith(spec.start_sentinel):
            return False, f"Track {track_num} must start with '{spec.start_sentinel}'"

        # Check end sentinel and LRC if required
        if spec.lrc_required:
            if not data.endswith(spec.end_sentinel):
                return False, f"Track {track_num} must end with '{spec.end_sentinel}'"

            # Extract data without sentinels for LRC check
            data_without_sentinels = data[1:-1]

            # Simple LRC check (XOR of all characters)
            lrc = 0
            for c in data_without_sentinels:
                lrc ^= ord(c)

            # The last character before the end sentinel should be the LRC
            expected_lrc = data[-2:-1]
            if expected_lrc and ord(expected_lrc) != lrc:
                return False, f"Track {track_num} LRC check failed"

        # Check allowed characters
        for c in data[1:-1]:  # Skip sentinels for character validation
            if c not in spec.allowed_chars:
                return False, f"Track {track_num} contains invalid character: '{c}'"

        return True, ""

    @classmethod
    def format_track_data(
        cls, format_type: CardFormat, track_num: int, data: str
    ) -> str:
        """Format track data according to the specified format.

        Args:
            format_type: The card format (ISO_7811 or ISO_7813)
            track_num: Track number (1, 2, or 3)
            data: The track data to format

        Returns:
            Formatted track data string
        """
        spec = cls.get_track_spec(format_type, track_num)

        # Add start sentinel if not present
        if not data.startswith(spec.start_sentinel):
            data = spec.start_sentinel + data

        # Add end sentinel if not present
        if not data.endswith(spec.end_sentinel):
            if spec.lrc_required:
                # Calculate LRC (XOR of all characters except sentinels)
                lrc = 0
                for c in data[1:]:  # Skip start sentinel
                    lrc ^= ord(c)
                data = data + chr(lrc) + spec.end_sentinel
            else:
                data = data + spec.end_sentinel

        # Truncate if necessary
        if len(data) > spec.max_length:
            data = data[: spec.max_length - 1] + spec.end_sentinel

        return data

    @classmethod
    def parse_track_data(
        cls, format_type: CardFormat, track_num: int, data: str
    ) -> Dict[str, str]:
        """Parse track data into its component fields.

        Args:
            format_type: The card format (ISO_7811 or ISO_7813)
            track_num: Track number (1, 2, or 3)
            data: The track data to parse

        Returns:
            Dictionary of parsed fields
        """
        spec = cls.get_track_spec(format_type, track_num)

        # Remove sentinels and LRC if present
        if data.startswith(spec.start_sentinel):
            data = data[1:]  # Remove start sentinel

        if data.endswith(spec.end_sentinel):
            if spec.lrc_required and len(data) > 1:  # Has LRC before end sentinel
                data = data[:-2]  # Remove LRC and end sentinel
            else:
                data = data[:-1]  # Just remove end sentinel

        # Split into fields
        fields = data.split(spec.field_separator)

        # Create result dictionary
        result = {
            "raw": data,
            "format": format_type.name,
            "track": track_num,
            "fields": fields,
        }

        # Add specific field names based on track number and format
        if track_num == 1 and len(fields) >= 3:
            result.update(
                {
                    "format_code": fields[0] if len(fields[0]) > 0 else "",
                    "primary_account_number": fields[1] if len(fields) > 1 else "",
                    "name": fields[2] if len(fields) > 2 else "",
                    "additional_data": fields[3] if len(fields) > 3 else "",
                }
            )
        elif track_num in (2, 3) and len(fields) >= 2:
            result.update(
                {
                    "primary_account_number": fields[0] if len(fields[0]) > 0 else "",
                    "additional_data": fields[1] if len(fields) > 1 else "",
                }
            )

        return result
