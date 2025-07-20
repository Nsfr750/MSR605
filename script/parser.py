"""
parser.py

Card data parser for MSR605. Provides functions to decode Track 1, Track 2, and Track 3 data.
"""


def parse_track1(track):
    """Parse Track 1 (ISO/IEC 7813) data: %B[card number]^[NAME]^YYMMDD..."""
    if not track or not track.startswith("%B"):
        return None
    try:
        parts = track[2:].split("^")
        card_number = parts[0] if len(parts) > 0 else ""
        name = parts[1].strip() if len(parts) > 1 else ""
        exp = parts[2][:4] if len(parts) > 2 else ""
        exp_fmt = f"20{exp[0:2]}/{exp[2:4]}" if len(exp) == 4 else ""
        return {
            "card_number": card_number,
            "name": name,
            "expiration": exp_fmt,
            "raw": track,
        }
    except Exception as e:
        return {"error": str(e), "raw": track}


def parse_track2(track):
    """Parse Track 2 (ISO/IEC 7813) data: ;[card number]=YYMMDDSSS..."""
    if not track or not track.startswith(";"):
        return None
    try:
        parts = track[1:].split("=")
        card_number = parts[0] if len(parts) > 0 else ""
        exp = parts[1][:4] if len(parts) > 1 else ""
        exp_fmt = f"20{exp[0:2]}/{exp[2:4]}" if len(exp) == 4 else ""
        service_code = parts[1][4:7] if len(parts) > 1 and len(parts[1]) >= 7 else ""
        return {
            "card_number": card_number,
            "expiration": exp_fmt,
            "service_code": service_code,
            "raw": track,
        }
    except Exception as e:
        return {"error": str(e), "raw": track}


import binascii


def parse_track3(track):
    """Parse Track 3 (proprietary/bank use). Show as raw, hex, length, and printable ASCII."""
    if not track:
        return None
    try:
        # Track 3 is often ';' delimited, may contain '=' and other symbols
        hexdata = binascii.hexlify(track.encode("utf-8")).decode("ascii")
        printable = "".join([c if 32 <= ord(c) <= 126 else "." for c in track])
        return {
            "raw": track,
            "hex": hexdata,
            "length": len(track),
            "printable": printable,
        }
    except Exception as e:
        return {"error": str(e), "raw": track}


def parse_all_tracks(tracks):
    """Parse all tracks and return a structured dict with detailed info for each track."""
    result = {}
    t1 = parse_track1(tracks[0]) if len(tracks) > 0 else None
    t2 = parse_track2(tracks[1]) if len(tracks) > 1 else None
    t3 = parse_track3(tracks[2]) if len(tracks) > 2 else None
    result["track1"] = t1
    result["track2"] = t2
    result["track3"] = t3
    # Add summary
    result["summary"] = {}
    if t1:
        result["summary"][
            "track1"
        ] = f"Card: {t1.get('card_number','')} | Name: {t1.get('name','')} | Exp: {t1.get('expiration','')}"
    if t2:
        result["summary"][
            "track2"
        ] = f"Card: {t2.get('card_number','')} | Exp: {t2.get('expiration','')} | Code: {t2.get('service_code','')}"
    if t3:
        result["summary"][
            "track3"
        ] = f"Len: {t3.get('length','')} | Raw: {t3.get('raw','')}"
    return result
