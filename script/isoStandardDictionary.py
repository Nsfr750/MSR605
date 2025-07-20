#!/usr/bin/env python3

"""isoStandardDictionary.py

Description: This module provides backward compatibility for the original ISO standard
            character set validation and integrates with the new card format system.

            The new implementation uses the CardFormatManager from card_formats.py
            which provides support for ISO 7811 and ISO 7813 formats.
"""

from .card_formats import CardFormat, CardFormatManager

# Backward compatibility dictionaries
# These are maintained for compatibility with existing code
isoDictionaryTrackOne = {}
isoDictionaryTrackTwoThree = {}

# Initialize the compatibility dictionaries with ISO 7811 characters
# This ensures backward compatibility with code that directly uses these dictionaries
for char in (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ "  # Uppercase letters and space
    "0123456789:;<=>?@"  # Numbers and special chars
    "!\"#&'()*+,-./"  # Additional special chars
    "[\\]^_"  # More special chars
):
    isoDictionaryTrackOne[char] = True

for char in "0123456789:;<=>?":
    isoDictionaryTrackTwoThree[char] = True


def iso_standard_track_check(char, track_num, format_type=CardFormat.ISO_7811):
    """Check if a character meets the ISO standard for a specific track.

    This is a backward-compatible wrapper around the new CardFormatManager.

    Args:
        char: A single character to check.
        track_num: Track number (1, 2, or 3).
        format_type: The card format (ISO_7811 or ISO_7813). Defaults to ISO_7811
                    for backward compatibility.

    Returns:
        bool: True if the character is valid for the specified track and format,
              False otherwise.
    """
    try:
        char = str(char)
        track_num = int(track_num)

        # Use the new CardFormatManager for validation
        spec = CardFormatManager.get_track_spec(format_type, track_num)
        return char in spec.allowed_chars

    except (ValueError, KeyError):
        # If there's an error, fall back to the old behavior for backward compatibility
        if track_num == 1:
            return char in isoDictionaryTrackOne
        elif track_num in (2, 3):
            return char in isoDictionaryTrackTwoThree
        else:
            print(f"ISO STANDARD CHECK, INVALID TRACK #: {track_num}")
            return True


# Backward compatibility function that matches the original signature
def iso_standard_track_check_legacy(char, track_num):
    """Legacy function that matches the original signature for backward compatibility."""
    return iso_standard_track_check(char, track_num, CardFormat.ISO_7811)


# For backward compatibility, assign the legacy function to the original name
# This ensures existing imports continue to work
iso_standard_track_check = iso_standard_track_check_legacy
