## Hardware Description
The MSR605 is a versatile magnetic stripe card reader/writer compatible with standard magstripe cards (credit cards, debit cards, ID cards, etc.). It supports reading and writing on all three tracks of magnetic stripe cards.

## Technical Details
- Follows ISO standards for magnetic stripe encoding
- Supports all three tracks (Track 1, 2, and 3)
- PIN block decoding (ISO 9564-0/1/3, VISA-1/3/4, ECI-4) with DES/3DES
- Encrypted PIN block extraction from Track 2 discretionary data
- Includes comprehensive error handling
- Built-in hardware diagnostic tools
- Raw serial diagnostic script (`diag_read.py`)