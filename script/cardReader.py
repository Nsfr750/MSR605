#!/usr/bin/env python3

"""cardReader.py

Description: This is an interface that allows manipulation of the MSR605 magnetic
             stripe card reader/writer. It supports ISO 7811 and ISO 7813 card formats.

"""


import serial
import time
import sys
import re
import json
from pathlib import Path
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union, Any

import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional, Tuple, Union, Any, Callable

from .card_formats import CardFormat, CardFormatManager, TrackSpecification
from .card_templates import TemplateManager, BatchProcessor, CardTemplate, TemplateType
from .card_validation import CardValidator, DeviceSyncManager, ValidationLevel
from .performance import LRUCache, measure_execution_time, memoize, CardOperationBatcher
from .api import start_api_server
from .isoStandardDictionary import iso_standard_track_check

# These constants are from the MSR605 Programming Manual under 'Section 6 Command and Response'
# I thought it would be easier if I used constants rather than putting hex in the code

# \x is the escape character for hex in python

# these three are used a lot, i think they are called control characters
ESCAPE = b"\x1b"
FILE_SEPERATOR = b"\x1c"
ACKNOWLEDGE = b"\x79"

# used when reading and writing
START_OF_HEADING = b"\x01"
START_OF_TEXT = b"\x02"
END_OF_TEXT = b"\x03"

# used to manipulate the MSR605
RESET = b"\x61"
READ = b"\x72"
WRITE = b"\x77"
COMMUNICATIONS_TEST = b"\x65"
ALL_LED_OFF = b"\x81"
ALL_LED_ON = b"\x82"
GREEN_LED_ON = b"\x83"
YELLOW_LED_ON = b"\x84"
RED_LED_ON = b"\x85"
SENSOR_TEST = b"\x86"
RAM_TEST = b"\x87"
ERASE_CARD = b"\x63"
DEVICE_MODEL = b"\x74"
FIRMWARE = b"\x76"
HI_CO = b"\x78"
LOW_CO = b"\x79"
HI_OR_LOW_CO = b"\x64"


class CardReader:
    """Allows interfacing with the MSR605 using the serial module"""

    def __init__(
        self,
        port: str = "COM3",
        baud_rate: int = 9600,
        timeout: float = 1.0,
        initial_format: CardFormat = CardFormat.ISO_7813,
        template_dir: Optional[str] = None,
        sync_enabled: bool = True,
        validation_level: ValidationLevel = ValidationLevel.STRICT,
        enable_api: bool = False,
        api_host: str = "0.0.0.0",
        api_port: int = 8000,
        max_workers: int = 4,
    ) -> None:
        """Initializes the CardReader instance.

        Args:
            port (str, optional): The COM port to connect to (e.g., 'COM5'). If None,
                                the class will try to auto-detect the port.
            baud_rate (int, optional): The baud rate for serial communication. Defaults to 9600.
            timeout (float, optional): The timeout for serial communication. Defaults to 1.0.
            initial_format (CardFormat, optional): Default card format to use for operations.
                                                Defaults to ISO_7813.
            template_dir (Optional[str], optional): Directory path for card templates. Defaults to None.

        Returns:
            Nothing

        Raises:
            MSR605ConnectError: An error occurred when connecting to the MSR605
        """
        self.__serialConn = None
        self.__port = port
        self.__default_format = initial_format
        self.__current_format = initial_format
        self.__last_written_tracks = ["", "", ""]  # For undo functionality
        self.__validation_level = validation_level
        
        # Initialize managers
        template_path = Path(template_dir) if template_dir else None
        self.template_manager = TemplateManager(template_path)
        self.batch_processor = BatchProcessor(self, self.template_manager)
        self.validator = CardValidator()
        
        # Initialize sync if enabled
        self.sync_manager = None
        if sync_enabled:
            self.sync_manager = DeviceSyncManager()
            self.sync_manager.start()
            self.sync_manager.register_callback(self._handle_sync_update)
            
        # Performance optimization
        self._cache = LRUCache(max_size=1000, ttl=300)  # 5 minute TTL
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._operation_batcher = CardOperationBatcher(self)
        
        # API server
        self._api_server = None
        if enable_api:
            self._start_api_server(api_host, api_port)

    def connect(self):
        """Connects to the MSR605 using the specified port or auto-detects it.

        Raises:
            MSR605ConnectError: If connection fails
        """
        print("\nATTEMPTING TO CONNECT TO MSR605")

        if self.__port:
            # Try to connect to the specified port
            try:
                self.__serialConn = serial.Serial(self.__port, 9600, timeout=1.0)
                print(f"Connected to specified port: {self.__port}")
            except (serial.SerialException, OSError) as e:
                raise cardReaderExceptions.MSR605ConnectError(
                    f"Failed to connect to {self.__port}: {str(e)}"
                )
        else:
            # Auto-detect the port
            for x in range(1, 256):
                port = f"COM{x}"
                try:
                    self.__serialConn = serial.Serial(port, 9600, timeout=1.0)
                    print(f"Auto-connected to port: {port}")
                    self.__port = port
                    break
                except (serial.SerialException, OSError):
                    continue

            if self.__serialConn is None:
                raise cardReaderExceptions.MSR605ConnectError(
                    "Could not find MSR605 on any COM port. "
                    "Please check the connection or specify the port manually."
                )

        try:
            # Initialize the MSR605
            print("\nINITIALIZING THE MSR605")

            # Reset the device
            self.reset()

            # Test communication
            self.communication_test()

            # Reset again after communication test
            self.reset()

            # Initialize the device with fallback coercivity mode
            self.initialize_device()

            print("\nCONNECTED TO MSR605")

        except Exception as e:
            # Close the connection if initialization fails
            if self.__serialConn and self.__serialConn.is_open:
                self.__serialConn.close()
            raise

    def _handle_sync_update(self, data: Dict) -> None:
        """Handle sync updates from other devices.
        
        Args:
            data: Dictionary containing sync data
        """
        try:
            # Example: Update card format if needed
            if 'card_format' in data:
                try:
                    self.set_card_format(CardFormat[data['card_format']])
                    print(f"Synced card format to {data['card_format']}")
                except (KeyError, ValueError):
                    pass
            
            # Add more sync handling as needed
            
        except Exception as e:
            print(f"Error handling sync update: {e}")
    
    def set_validation_level(self, level: ValidationLevel) -> None:
        """Set the validation level for card data.
        
        Args:
            level: Validation level to set
        """
        self.__validation_level = level
    
    def get_validation_level(self) -> ValidationLevel:
        """Get the current validation level.
        
        Returns:
            Current validation level
        """
        return self.__validation_level
    
    def validate_card_data(self, tracks: List[str], format: Optional[CardFormat] = None) -> Tuple[bool, Dict[int, List[str]]]:
        """Validate card data against the current validation rules.
        
        Args:
            tracks: List of track data (3 elements)
            format: Optional format to validate against. If None, uses current format.
            
        Returns:
            Tuple of (is_valid, error_dict) where error_dict maps track numbers to error messages
        """
        if format is None:
            format = self.__current_format
            
        return self.validator.validate_card(tracks, format, self.__validation_level)
    
    def sync_data(self, data: Dict) -> None:
        """Synchronize data with other devices.
        
        Args:
            data: Dictionary containing data to sync
        """
        if self.sync_manager:
            self.sync_manager.send_update(data)
    
    def _start_api_server(self, host: str, port: int) -> None:
        """Start the API server in a separate thread."""
        def run_server():
            server = start_api_server(host=host, port=port)
            server.run()
            
        self._api_thread = threading.Thread(target=run_server, daemon=True)
        self._api_thread.start()
        
    def enable_api(self, host: str = "0.0.0.0", port: int = 8000) -> None:
        """Enable the REST API server.
        
        Args:
            host: Host to bind the API server to
            port: Port to run the API server on
        """
        if not hasattr(self, '_api_thread') or not self._api_thread.is_alive():
            self._start_api_server(host, port)
    
    def shutdown(self) -> None:
        """Shut down the card reader and clean up resources."""
        # Stop sync manager if running
        if hasattr(self, 'sync_manager') and self.sync_manager:
            self.sync_manager.stop()
            
        # Shutdown the operation batcher
        if hasattr(self, '_operation_batcher'):
            self._operation_batcher.shutdown()
            
        # Shutdown thread pool
        if hasattr(self, '_executor'):
            self._executor.shutdown(wait=True)
            
    def __del__(self):
        """Clean up resources when the object is destroyed."""
        self.shutdown()
            
        # Close serial connection
        if hasattr(self, "_CardReader__serialConn") and self.__serialConn:
            self.__serialConn.close()
            raise

    def set_leading_zero(self, track=1, enable=True):
        """
        Set or clear leading zero for a track.
        track: 1, 2, or 3
        enable: True to set, False to clear
        """
        cmd = b"\x1bL" + bytes([track]) + (b"1" if enable else b"0")
        self.__serialConn.write(cmd)
        resp = self.__serialConn.read(1)
        if resp != b"\x0d":
            raise Exception("Failed to set leading zero")

    def check_leading_zero(self, track=1):
        """
        Check if leading zero is set for a track.
        Returns True if set, False otherwise.
        """
        cmd = b"\x1bM" + bytes([track])
        self.__serialConn.write(cmd)
        resp = self.__serialConn.read(2)
        # Expecting: b'1\r' or b'0\r'
        if resp[1:] != b"\r":
            raise Exception("Invalid response from check_leading_zero")
        return resp[0:1] == b"1"

    def select_bpi(self, track=1, bpi=210):
        """
        Select BPI (Bits Per Inch) for a track.
        bpi: 75 or 210
        """
        if bpi not in (75, 210):
            raise ValueError("BPI must be 75 or 210")
        cmd = b"\x1bB" + bytes([track]) + (b"1" if bpi == 210 else b"0")
        self.__serialConn.write(cmd)
        resp = self.__serialConn.read(1)
        if resp != b"\x0d":
            raise Exception("Failed to set BPI")

    def read_raw_data(self, track=1):
        """
        Read raw data from a track.
        Returns the raw bytes read from the track.
        """
        cmd = b"\x1bR" + bytes([track])
        self.__serialConn.write(cmd)
        # Read until carriage return (\r)
        data = b""
        while True:
            c = self.__serialConn.read(1)
            if c == b"\r":
                break
            data += c
        return data

    def write_raw_data(self, track=1, data=b""):
        """
        Write raw data to a track.
        data: bytes to write (should be properly formatted for the device)
        """
        cmd = b"\x1bW" + bytes([track]) + data + b"\r"
        self.__serialConn.write(cmd)
        resp = self.__serialConn.read(1)
        if resp != b"\x0d":
            raise Exception("Failed to write raw data")

    def set_bpc(self, track=1, bpc=7):
        """
        Set BPC (Bits Per Character) for a track.
        bpc: usually 5, 7, or 8 depending on the track
        """
        if bpc not in (5, 7, 8):
            raise ValueError("BPC must be 5, 7, or 8")
        cmd = b"\x1bC" + bytes([track]) + bytes([bpc])
        self.__serialConn.write(cmd)
        resp = self.__serialConn.read(1)
        if resp != b"\x0d":
            raise Exception("Failed to set BPC")

    def close_serial_connection(self):
        """closes the serial connection to the MSR605

        Allows other applications to use the MSR605

        Args:
            None

        Returns:
            Nothing

        Raises:
            Nothing
        """

        print("\nCLOSING COM PORT SERIAL CONNECTION")

        self.__serialConn.close()

    def reset(self):
        """This command reset the MSR605 to initial state.

        Args:
            None

        Returns:
            Nothing

        Raises:
            Nothing
        """

        print("\nATTEMPTING TO RESET THE MSR605")

        # Check if serial connection is established
        if self.__serialConn is None:
            print("WARNING: No serial connection established. Cannot reset MSR605.")
            print("Please connect to the MSR605 first using the connect() method.")
            return None

        # flusing the input and output solves the issue where the MSR605 app/gui would need
        # to be restarted if there was an issue like say swiping the card backwards, I
        # found out about the flushing input & output before the reset from this MSR605
        # project: https://github.com/steeve/msr605/blob/master/msr605.py
        # I assume before there would be data left on the buffer which would mess up
        # the reading and writing of commands since there would be extra data which
        # wasn't expected
        try:
            self.__serialConn.flushInput()
            self.__serialConn.flushOutput()
        except Exception as e:
            print(f"WARNING: Error flushing serial buffers: {e}")
            # Continue with reset attempt anyway

        # writes the command code for resetting the MSR605
        try:
            self.__serialConn.write(ESCAPE + RESET)
            
            # so i might be a noob here but from what i read, flush waits for the command above
            # to fully write and complete, I thought this was better than adding time delays
            self.__serialConn.flush()
        except Exception as e:
            print(f"WARNING: Error writing reset command: {e}")
            # Continue anyway - reset might still work

        print("MSR605 SHOULD'VE BEEN RESET")
        # there is no response from the MSR605

        return None

    # **************************************************
    #
    #        MSR605 Read/Write/Erase Card Functions
    #
    # **************************************************

    def set_card_format(self, card_format: CardFormat) -> None:
        """Set the card format for subsequent operations.

        Args:
            card_format: The card format to use (ISO_7811 or ISO_7813)

        Returns:
            None

        Raises:
            ValueError: If an invalid card format is provided
        """
        if not isinstance(card_format, CardFormat):
            raise ValueError("Invalid card format. Must be a CardFormat enum value.")
        self.__current_format = card_format

    def get_card_format(self) -> CardFormat:
        """Get the current card format.

        Returns:
            The current card format (ISO_7811 or ISO_7813)
        """
        return self.__current_format

    def validate_track_data(self, track_num: int, data: str) -> Tuple[bool, str]:
        """Validate track data against the current card format.

        Args:
            track_num: Track number (1, 2, or 3)
            data: The track data to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        return CardFormatManager.validate_track_data(
            self.__current_format, track_num, data
        )

    @measure_execution_time
    def read_card(
        self, 
        detect_format: bool = False, 
        validate: bool = True,
        use_cache: bool = True
    ) -> Dict[str, Union[str, Dict, bool, dict]]:
        """Read data from a magnetic stripe card.

        This command requests the MSR605 to read a swiped card and respond with
        the data read. It can optionally detect the card format automatically.

        The response format is as follows:

        ASCII:
            Response:[DataBlock]<ESC>[StatusByte]
                DataBlock: <ESC>s[Carddata]?<FS><ESC>[Status]
                    Carddata: <ESC>1[string1]<ESC>2[string2]<ESC>3[string3]
                Status:
                    OK: 0
                    Error, Write or read error: 1
                    Command format error: 2
                    Invalid command: 4
                    Invalid card swipe when in write mode: 9

        HEX:
            Response:[DataBlock] 1B [StatusByte]
                DataBlock: 1B 73 [Carddata] 3F 1C 1B [Status]
                    Carddata: 1B 01 [string1] 1B 02 [string2] 1B 03[string3]
                Status:
                    OK: 0x30h
                    Error, Write or read error: 0x31h
                    Command format error: 0x32h
                    Invalid command: 0x34h
                    Invalid card swipe when in write mode: 0x39h

        Args:
            detect_format: If True, attempt to automatically detect the card format.
                         If False, use the currently set format.

        Returns:
            A dictionary containing:
            - 'tracks': List of raw track data (3 elements, empty string if no data)
            - 'format': The detected or current card format
            - 'parsed': Dictionary of parsed track data if parsing was successful

        Example:
            {
                'tracks': [
                    '%B1234567890123456^CARDHOLDER/NAME^24011234567890123456789?',
                    ';1234567890123456=24011234567890123456?',
                    ''
                ],
                'format': 'ISO_7813',
                'parsed': {
                    'track1': {
                        'primary_account_number': '1234567890123456',
                        'name': 'CARDHOLDER/NAME',
                        'expiration_date': '2401',
                        'service_code': '123',
                        'discretionary_data': '4567890123456789'
                    },
                    'track2': {
                        'primary_account_number': '1234567890123456',
                        'expiration_date': '2401',
                        'service_code': '123',
                        'discretionary_data': '4567890123456789'
                    },
                    'track3': {}
                }
            }

        Raises:
            CardReadError: If an error occurs while reading the card
            StatusError: If the device reports an error status
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"\nATTEMPTING TO READ FROM CARD (SWIPE NOW) - Attempt {attempt + 1}")
                # read in track data will be stored in this array
                tracks = ["", "", ""]

                # command code for reading written to the MSR605
                self.__serialConn.write(ESCAPE + READ)
                self.__serialConn.flush()

                # Give the device a moment to process
                time.sleep(0.1)

                # response/output from the MSR605 - with retry logic
                response = self.__serialConn.read()
                if response != ESCAPE:
                    print(f"Attempt {attempt + 1}: Expected ESCAPE, got {response}")
                    if attempt < max_retries - 1:
                        print("Retrying...")
                        time.sleep(0.5)
                        continue
                    else:
                        raise cardReaderExceptions.CardReadError(
                            "[Datablock] READ ERROR, R/W Data Field, looking for ESCAPE(\\x1b)", None
                        )

                response = self.__serialConn.read()
                if response != b"s":
                    print(f"Attempt {attempt + 1}: Expected 's', got {response}")
                    if attempt < max_retries - 1:
                        print("Retrying...")
                        time.sleep(0.5)
                        continue
                    else:
                        raise cardReaderExceptions.CardReadError(
                            "[Datablock] READ ERROR, R/W Data Field, looking for s (\\x73)", None
                        )

                response = self.__serialConn.read()
                if response != ESCAPE:
                    print(f"Attempt {attempt + 1}: Expected ESCAPE, got {response}")
                    if attempt < max_retries - 1:
                        print("Retrying...")
                        time.sleep(0.5)
                        continue
                    else:
                        raise cardReaderExceptions.CardReadError(
                            "[Carddata] READ ERROR, R/W Data Field, looking for ESCAPE(\\x1b)", None
                        )

                # If we got here, the initial response was correct, continue with normal reading
                break

            except Exception as e:
                print(f"Attempt {attempt + 1}: Error during read: {e}")
                if attempt < max_retries - 1:
                    print("Retrying...")
                    time.sleep(0.5)
                    continue
                else:
                    raise e

        # track one data will be read in, this isn't raising an exception because the card
        # might not have track 1 data
        if self.__serialConn.read() != START_OF_HEADING:

            # could be changed to be stored in some sort of error data structure and returned
            # with track data array but lets keep it simple for now ;)
            print("This card might not have a TRACK 1")
            print(
                "[Carddata] READ ERROR, R/W Data Field, looking for START OF HEAD - SOH(\x01)"
            )

        # if there is a track 1 then the data is read and stored
        else:

            tracks[0] = self.read_until(ESCAPE, 1, True)
            print("TRACK 1: ", tracks[0])

            if len(tracks[0]) > 0:
                if tracks[0][-1] == "?":
                    tracks[0] = tracks[0][:-1]

                if tracks[0][0] == "%":
                    tracks[0] = tracks[0][1:]

            else:
                tracks[0] = ""

        # track 2
        if self.__serialConn.read() != START_OF_TEXT:
            print("This card might not have a TRACK 2")
            print(
                "[Carddata] READ ERROR, R/W Data Field, looking for START OF TEXT - STX(\x02)"
            )

        else:

            tracks[1] = self.read_until(ESCAPE, 2, True)
            print("TRACK 2: ", tracks[1])

            if len(tracks[1]) > 0:
                if tracks[1][-1] == "?":
                    tracks[1] = tracks[1][:-1]

                # removes any semicolons, these are added automatically when writing
                if tracks[1][0] == ";":
                    tracks[1] = tracks[1][1:]

            else:
                tracks[1] = ""

        # track 3
        try:
            response = self.__serialConn.read()
            print(f"Track 3 response: {response} (hex: {response.hex() if response else 'None'})")
            
            if response != END_OF_TEXT:
                print("This card might not have a TRACK 3")
                print(f"[Carddata] Expected END_OF_TEXT (ETX/\\x03), got: {response} (hex: {response.hex() if response else 'None'})")
                
                # Check if we got the FILE_SEPERATOR instead, which might indicate end of data
                if response == FILE_SEPERATOR:
                    print("Track 3 data appears to be empty (got FILE_SEPERATOR)")
                    tracks[2] = ""
                else:
                    # Try to read any remaining data that might be Track 3
                    print("Attempting to read Track 3 data anyway...")
                    try:
                        # Small timeout to see if there's more data
                        time.sleep(0.1)
                        if self.__serialConn.in_waiting > 0:
                            tracks[2] = self.read_until(FILE_SEPERATOR, 3, False)  # Don't validate ISO for potentially partial data
                            print(f"TRACK 3 (recovered): {tracks[2]}")
                        else:
                            tracks[2] = ""
                    except Exception as e:
                        print(f"Failed to recover Track 3 data: {e}")
                        tracks[2] = ""
            else:
                # Successfully got END_OF_TEXT, now read Track 3 data
                tracks[2] = self.read_until(FILE_SEPERATOR, 3, True)
                print("TRACK 3: ", tracks[2])

                if len(tracks[2]) > 0:
                    if tracks[2][-1] != "?":
                        tracks[2] += "?"

                    if tracks[2][0] == ";":
                        tracks[2] = tracks[2][1:]

                else:  # since track 3 requires a ? when writing
                    tracks[2] = "?"
                    
        except Exception as e:
            print(f"Error reading Track 3: {e}")
            tracks[2] = ""

        # Check for ending field - be more flexible with what we accept
        try:
            last_byte = self.__serialConn.read()
            print(f"Ending field byte: {last_byte} (hex: {last_byte.hex() if last_byte else 'None'})")
            
            if last_byte not in (ESCAPE, FILE_SEPERATOR):
                # This might not be a critical error - let's see if we can still read the status
                print(f"Warning: Unexpected ending field byte: {last_byte}")
                print("Attempting to continue with status reading...")
                
                # Put the byte back if it might be the status
                # Note: This is a workaround since serial doesn't support unread
                # We'll try to read status directly
                
        except Exception as e:
            print(f"Warning: Error reading ending field: {e}")
            print("Attempting to continue with status reading...")

        # this reads the status byte and raises exceptions
        try:
            self.status_read()
        except Exception as e:
            print(f"Status read error: {e}")
            # Don't raise the exception - we still have track data
            print("Continuing with available track data...")

        result = {"tracks": tracks, "format": self.__current_format.name}

        if detect_format:
            detected_format = self._detect_card_format(tracks)
            result["format"] = detected_format.name

        self._parse_track_data(result)

        # Generate a cache key if caching is enabled
        cache_key = None
        if use_cache and any(tracks):
            cache_key = f"read_card_{hash(tuple(tracks))}"
            cached_result = self._cache.get(cache_key)
            if cached_result is not None:
                return cached_result
        
        # Read the card data
        result = {
            "tracks": tracks,
            "format": self.__current_format.name,
            "valid": True,
            "validation_errors": {},
            "cached": False
        }
        
        if detect_format:
            detected_format = self._detect_card_format(tracks)
            result["format"] = detected_format.name
        else:
            detected_format = self.__current_format
            
        # Validate the card data if requested
        if validate and any(tracks):
            is_valid, errors = self.validate_card_data(tracks, detected_format)
            result["valid"] = is_valid
            result["validation_errors"] = errors
            
            # If we have a sync manager, share the card format
            if hasattr(self, 'sync_manager') and self.sync_manager and detect_format:
                self.sync_data({"card_format": detected_format.name})
        
        # Cache the result if caching is enabled
        if cache_key is not None and any(tracks):
            self._cache.set(cache_key, result)

        self._parse_track_data(result)

        return result

    @memoize(max_size=1000, ttl=300)  # Cache results for 5 minutes
    def _detect_card_format(self, tracks: List[str]) -> CardFormat:
        """Attempt to detect the card format based on the track data.

        This method checks the track data against all supported formats and
        returns the most specific format that matches the data.

        Args:
            tracks: List of track data (3 elements)

        Returns:
            The detected CardFormat (e.g., ISO_7813, AAMVA, IATA, etc.)
        """
        # Default to the current format
        detected_format = self.__current_format
        format_scores = {fmt: 0 for fmt in CardFormat}

        # Check each track that has data
        for i, track in enumerate(tracks):
            if not track:
                continue

            track_num = i + 1

            # Test against all supported formats
            for fmt in CardFormat:
                try:
                    is_valid, _ = CardFormatManager.validate_track_data(
                        fmt, track_num, track
                    )
                    if is_valid:
                        format_scores[fmt] += 1
                except ValueError:
                    # Skip formats that don't support this track number
                    continue

        # Find the format with the highest score
        if any(score > 0 for score in format_scores.values()):
            # Get format with maximum score, with RAW as fallback
            max_score = max(format_scores.values())
            if max_score > 0:
                # Prefer specific formats over RAW
                candidate_formats = [
                    fmt for fmt, score in format_scores.items()
                    if score == max_score and fmt != CardFormat.RAW
                ]
                if candidate_formats:
                    # If multiple formats have the same score, prefer more specific ones
                    if len(candidate_formats) > 1:
                        # Order of preference for formats with same score
                        preference_order = [
                            CardFormat.ISO_7813,
                            CardFormat.ISO_7811,
                            CardFormat.AAMVA,
                            CardFormat.IATA,
                            CardFormat.ABA,
                            CardFormat.RAW
                        ]
                        for fmt in preference_order:
                            if fmt in candidate_formats:
                                detected_format = fmt
                                break
                    else:
                        detected_format = candidate_formats[0]
                else:
                    detected_format = CardFormat.RAW

        return detected_format

    def process_batch(self, operations: List[Dict], parallel: bool = True) -> List[Dict]:
        """Process a batch of card operations.
        
        Args:
            operations: List of operation dictionaries with 'type' and other parameters.
                       Example operations:
                       - Read operation: {'type': 'read', 'detect_format': True}
                       - Write operation: {'type': 'write', 'tracks': ['%B123...', ';123...', ''], 'format': 'ISO_7813'}
                       - Apply template: {'type': 'apply_template', 'template_name': 'my_template'}
                       
        Returns:
            List of results for each operation.
        """
        return self.batch_processor.process_batch(operations)
    
    def save_template(self, name: str, description: str, template_type: str, 
                     tracks: List[str], format: str, **metadata) -> bool:
        """Save a card operation template.
        
        Args:
            name: Name of the template
            description: Description of the template
            template_type: Type of template ('read', 'write', or 'batch')
            tracks: List of track data (for write templates)
            format: Card format as string (e.g., 'ISO_7813')
            **metadata: Additional metadata for the template
            
        Returns:
            True if template was saved successfully, False otherwise
        """
        try:
            template = CardTemplate(
                name=name,
                description=description,
                template_type=TemplateType[template_type.upper()],
                tracks=tracks,
                format=CardFormat[format],
                metadata=metadata
            )
            self.template_manager.save_template(template)
            return True
        except Exception as e:
            print(f"Error saving template: {e}")
            return False
    
    def get_template(self, name: str) -> Optional[Dict]:
        """Get a template by name.
        
        Args:
            name: Name of the template to retrieve
            
        Returns:
            Template dictionary if found, None otherwise
        """
        template = self.template_manager.get_template(name)
        if template:
            return template.to_dict()
        return None
    
    def list_templates(self, template_type: Optional[str] = None) -> List[Dict]:
        """List all available templates, optionally filtered by type.
        
        Args:
            template_type: Optional filter for template type ('read', 'write', or 'batch')
            
        Returns:
            List of template dictionaries
        """
        type_enum = TemplateType[template_type.upper()] if template_type else None
        return [t.to_dict() for t in self.template_manager.list_templates(type_enum)]
    
    def delete_template(self, name: str) -> bool:
        """Delete a template.
        
        Args:
            name: Name of the template to delete
            
        Returns:
            True if template was deleted, False otherwise
        """
        return self.template_manager.delete_template(name)
    
    def export_batch_results(self, output_file: str, format: str = 'json') -> bool:
        """Export the results of the last batch operation.
        
        Args:
            output_file: Path to the output file
            format: Output format ('json' or 'csv')
            
        Returns:
            True if export was successful, False otherwise
        """
        return self.batch_processor.export_results(output_file, format)
    
    @memoize(max_size=1000, ttl=300)  # Cache results for 5 minutes
    def _parse_track_data(self, result: Dict) -> None:
        """Parse the track data according to the current format.

        Args:
            result: The result dictionary from read_card()
            
        Returns:
            The updated result dictionary with parsed data
        """
        parsed_data = {}
        result['parsed_data'] = parsed_data

        for i, track in enumerate(result["tracks"]):
            track_num = i + 1
            if not track:
                parsed_data[f"track{track_num}"] = {}
                continue

            try:
                parsed = CardFormatManager.parse_track_data(
                    CardFormat[result["format"]], track_num, track
                )
                parsed_data[f"track{track_num}"] = parsed
            except Exception as e:
                # If parsing fails, store the error and continue with other tracks
                parsed_data[f"track{track_num}"] = {"error": str(e), "raw": track}

        result["parsed"] = parsed_data

    @measure_execution_time
    def write_card(self, tracks, status_byte_check=True, format_override=None, use_cache: bool = True):
        """Write data to a magnetic stripe card.

        This command requests the MSR605 to write the provided track data to a
        swiped card. The data will be formatted according to the specified or
        detected card format.

        Args:
            tracks: A list of up to 3 strings containing track data to write.
                   Each element corresponds to a track (1-3). Empty strings
                   will skip writing to that track.
            status_byte_check: If True, verify the status byte after writing.
            format_override: Optional CardFormat to use instead of the current format.

        Returns:
            A dictionary with the following keys:
            - 'success': Boolean indicating if the write was successful
            - 'message': Status message
            - 'format': The card format used for writing

        Raises:
            CardWriteError: If an error occurs during writing
            ValueError: If the tracks parameter is invalid
        """

        print("\nWRITING TO CARD (SWIPE NOW)")

        # Validate tracks parameter
        if not isinstance(tracks, (list, tuple)) or len(tracks) != 3:
            raise ValueError("Tracks must be a list or tuple with 3 elements")

        # Convert all track data to strings
        tracks = [str(track) if track is not None else "" for track in tracks]

        # Determine the card format to use
        write_format = (
            format_override if format_override is not None else self.__current_format
        )

        # Validate track data against the selected format
        for i, track in enumerate(tracks):
            if not track:
                continue

            track_num = i + 1
            is_valid, error_msg = CardFormatManager.validate_track_data(
                write_format, track_num, track
            )

            if not is_valid:
                raise cardReaderExceptions.CardWriteError(
                    f"Invalid data for track {track_num} in {write_format.name} format: {error_msg}"
                )

        # Build the data block
        # Format: <ESC>s<ESC>1[track1 data]<ESC>2[track2 data]<ESC>3[track3 data]?<FS><ESC>0
        data_block = ESCAPE + b"s"

        # Add the track data
        for i, track in enumerate(tracks):
            if track:
                track_num = i + 1
                data_block += ESCAPE + str(track_num).encode("ascii")
                data_block += track.encode("ascii")

        # Add the end of the data block
        data_block += b"?" + FILE_SEPERATOR + ESCAPE + b"0"

        # Write the command code for writing to a card
        self.__serialConn.write(ESCAPE + WRITE)

        # Write the data block
        self.__serialConn.write(data_block)

        # Check the status byte if requested
        if status_byte_check:
            status_byte = self.__serialConn.read(1)

            if status_byte != b"0":
                status_code = int.from_bytes(status_byte, byteorder="big")
                raise cardReaderExceptions.StatusError(
                    f"Write failed with status: {status_code}", status_code
                )

        # Generate a cache key if caching is enabled
        cache_key = None
        if use_cache and any(tracks):
            cache_key = f"write_card_{hash(tuple(tracks))}"
            cached_result = self._cache.get(cache_key)
            if cached_result is not None:
                return cached_result
                
        # Store the tracks to be written for potential undo operation
        self.__last_written_tracks = tracks["", "", ""]  # For undo functionality
        
        result = {
            "success": True,
            "message": "Write command sent", 
            "format": write_format.name,
            "cached": False
        }
        
        # Cache the result if caching is enabled
        if cache_key is not None and any(tracks):
            self._cache.set(cache_key, result)
            
        return result,

    def erase_card(self, trackSelect):
        """This command is used to erase the card data when card swipe.

            NOTE** THAT ERASED CARDS CANNOT BE READ

        Args:
            trackSelect: is an integer between 0-7, this dictates which track(s) to delete


            ex:
                The [Select Byte] is what goes at the end of the command code, after the
                ESCAPE and 0x6C

                Binary:
                    *[Select Byte] format:
                                            00000000: Track 1 only
                                            00000010: Track 2 only
                                            00000100: Track 3 only
                                            00000011: Track 1 & 2
                                            00000101: Track 1 & 3
                                            00000110: Track 2 & 3
                                            00000111: Track 1, 2 & 3

                Decimal:
                    *[Select Byte] format:
                                            0: Track 1 only
                                            2: Track 2 only
                                            4: Track 3 only
                                            3: Track 1 & 2
                                            5: Track 1 & 3
                                            6: Track 2 & 3
                                            7: Track 1, 2 & 3


        Returns:
            Nothing

        Raises:
            EraseCardError: An error occurred while erasing the magstripe card
        """

        # checks if the track(s) that was choosen to be erased is/are valid track(s)
        if not (trackSelect >= 0 and trackSelect <= 7 and trackSelect != 1):
            raise cardReaderExceptions.EraseCardError(
                "Track selection provided is invalid, has to " "between 0-7"
            )

        print("\nERASING CARD (SWIPE NOW)")

        # command code for erasing a magstripe card
        self.__serialConn.write(ESCAPE + ERASE_CARD + (str(trackSelect)).encode())
        self.__serialConn.flush()

        # response/output from the MSR605
        if self.__serialConn.read() != ESCAPE:
            raise cardReaderExceptions.EraseCardError(
                "ERASE CARD ERROR, looking for ESCAPE(\x1b)"
            )

        eraseCardResponse = self.__serialConn.read()
        if eraseCardResponse != b"0":

            if eraseCardResponse != b"A":
                raise cardReaderExceptions.EraseCardError(
                    "ERASE CARD ERROR, looking for A(\x41), the "
                    "card was not erased but the erasing "
                    "didn't fail, so this is a weird case"
                )

            else:
                raise cardReaderExceptions.EraseCardError(
                    "ERASE CARD ERROR, the card might have not " "been erased"
                )

        print("CARD HAS BEEN SUCCESSFULLY ERASED")

        return None

    # **********************************
    #
    #        LED Functions
    #
    # **********************************

    def led_off(self):
        """This command is used to turn off all the LEDs.

        Args:
           None

        Returns:
           Nothing

        Raises:
           Nothing
        """
        try:
            self._check_connection()
            self.__serialConn.write(ESCAPE + ALL_LED_OFF)
            self.__serialConn.flush()
        except cardReaderExceptions.MSR605ConnectError:
            print("WARNING: Cannot turn off LEDs - no serial connection established")
        except Exception as e:
            print(f"WARNING: Error turning off LEDs: {e}")

    def led_on(self):
        """This command is used to turn on all the LEDs.


        Args:
           None

        Returns:
           Nothing

        Raises:
           Nothing
        """
        try:
            self._check_connection()
            self.__serialConn.write(ESCAPE + ALL_LED_ON)
            self.__serialConn.flush()
        except cardReaderExceptions.MSR605ConnectError:
            print("WARNING: Cannot turn on LEDs - no serial connection established")
        except Exception as e:
            print(f"WARNING: Error turning on LEDs: {e}")

    def green_led_on(self):
        """This command is used to turn on the green LEDs.

        Args:
           None

        Returns:
           Nothing

        Raises:
           Nothing
        """
        try:
            self._check_connection()
            self.__serialConn.write(ESCAPE + GREEN_LED_ON)
            self.__serialConn.flush()
        except cardReaderExceptions.MSR605ConnectError:
            print("WARNING: Cannot turn on green LED - no serial connection established")
        except Exception as e:
            print(f"WARNING: Error turning on green LED: {e}")

    def yellow_led_on(self):
        """This command is used to turn on the yellow LED.

        Args:
           None

        Returns:
           Nothing

        Raises:
           Nothing
        """
        try:
            self._check_connection()
            self.__serialConn.write(ESCAPE + YELLOW_LED_ON)
            self.__serialConn.flush()
        except cardReaderExceptions.MSR605ConnectError:
            print("WARNING: Cannot turn on yellow LED - no serial connection established")
        except Exception as e:
            print(f"WARNING: Error turning on yellow LED: {e}")

    def red_led_on(self):
        """This command is used to turn on the red LED.

        Args:
           None

        Returns:
           Nothing

        Raises:
           Nothing
        """
        try:
            self._check_connection()
            self.__serialConn.write(ESCAPE + RED_LED_ON)
            self.__serialConn.flush()
        except cardReaderExceptions.MSR605ConnectError:
            print("WARNING: Cannot turn on red LED - no serial connection established")
        except Exception as e:
            print(f"WARNING: Error turning on red LED: {e}")

    # ****************************************
    #
    #        MSR605 Hardware Test Functions
    #
    # ****************************************

    def communication_test(self):
        """This command is used to verify that the communication link between computer and
        MSR605 is up and good.

        Args:
            None

        Returns:
            None

        Raises:
            CommunicationTestError: An error occurred while testing the MSR605's communication
        """
        try:
            self._check_connection()
            
            print("\nCHECK COMMUNICATION LINK BETWEEN THE COMPUTER AND THE MSR605")

            # command code for testing the MSR605 Communication with the Computer
            self.__serialConn.write(ESCAPE + COMMUNICATIONS_TEST)
            self.__serialConn.flush()

            # response/output from the MSR605
            if self.__serialConn.read() != ESCAPE:
                raise cardReaderExceptions.CommunicationTestError(
                    "COMMUNICATION ERROR, looking for " "ESCAPE(\x1b)",
                    None,
                )

            if self.__serialConn.read() != b"y":
                raise cardReaderExceptions.CommunicationTestError(
                    "COMMUNICATION ERROR, looking for " "y(\x79)",
                    None,
                )

            print("COMMUNICATION IS GOOD")

        except cardReaderExceptions.MSR605ConnectError as e:
            raise cardReaderExceptions.CommunicationTestError(
                f"Cannot test communication - {e}"
            )
        except Exception as e:
            raise cardReaderExceptions.CommunicationTestError(
                f"Communication test failed: {e}"
            )

    def sensor_test(self):
        """This command is used to verify that the card sensing circuit of MSR605 is
        working properly. MSR605 will not response until a card is sensed or receive
        a RESET command.

        NOTE** A CARD NEEDS TO BE SWIPED AS STATED ABOVE

        Args:
           None

        Returns:
           Nothing

        Raises:
           SensorTestError: An error occurred while testing the MSR605's communication
        """
        try:
            self._check_connection()
            
            print("\nCHECK IF THE CARD SENSING CIRCUIT OF MSR605 IS WORKING")
            print("NOTE: A CARD NEEDS TO BE SWIPED FOR THIS TEST")

            # command code for sensor test written to the MSR605
            self.__serialConn.write(ESCAPE + SENSOR_TEST)
            self.__serialConn.flush()

            # response/output from the MSR605
            if self.__serialConn.read() != ESCAPE:
                raise cardReaderExceptions.SensorTestError(
                    "SENSOR TEST ERROR, looking for ESCAPE(\x1b)",
                    None,
                )

            if self.__serialConn.read() != b"0":
                raise cardReaderExceptions.SensorTestError(
                    "SENSOR TEST ERROR, looking for 0(\x30)",
                    None,
                )

            print("TESTS WERE SUCCESSFUL")

        except cardReaderExceptions.MSR605ConnectError as e:
            raise cardReaderExceptions.SensorTestError(
                f"Cannot test sensor - {e}"
            )
        except Exception as e:
            raise cardReaderExceptions.SensorTestError(
                f"Sensor test failed: {e}"
            )

    def ram_test(self):
        """This command is used to request MSR605 to perform a test on its on board RAM.

        Args:
            Nothing

        Returns:
            Nothing

        Raises:
            RamTestError: An error occurred accessing the bigtable.Table object.
        """
        try:
            self._check_connection()
            
            print("\nCHECK IF THE ON BOARD RAM OF MSR605 IS WORKING")

            # command code for RAM test written to the MSR605
            self.__serialConn.write(ESCAPE + RAM_TEST)
            self.__serialConn.flush()

            # response/output from the MSR605
            if self.__serialConn.read() != ESCAPE:
                raise cardReaderExceptions.RamTestError(
                    "RAM TEST ERROR, looking for ESCAPE(\x1b)",
                    None,
                )

            ramTestResponse = self.__serialConn.read()

            if ramTestResponse != b"0":

                if ramTestResponse != b"A":
                    raise cardReaderExceptions.RamTestError(
                        "RAM TEST ERROR, looking for A(\x41), the "
                        "RAM is not ok but the RAM hasn't failed a "
                        "test either, so this is a weird case"
                    )

                else:
                    raise cardReaderExceptions.RamTestError(
                        "RAM TEST ERROR, the RAM test has failed",
                        None,
                    )

            print("RAM TESTS SUCCESSFUL")

        except cardReaderExceptions.MSR605ConnectError as e:
            raise cardReaderExceptions.RamTestError(
                f"Cannot test RAM - {e}"
            )
        except Exception as e:
            raise cardReaderExceptions.RamTestError(
                f"RAM test failed: {e}"
            )

    # **********************************
    #
    #     MSR605 Coercivity functions
    #
    # **********************************

    def set_hi_co(self):
        """Set the MSR605 to high coercivity mode with retry logic."""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.__serialConn.write(ESCAPE + HI_CO)
                self.__serialConn.flush()

                first = self.__serialConn.read()

                if first != ESCAPE:
                    self.read_until("0", 4, False)
                    if self.__serialConn.read() != ESCAPE:
                        print(f"Attempt {attempt + 1}: Unexpected response: {first}")
                        if attempt < max_retries - 1:
                            print("Retrying...")
                            time.sleep(1)
                            continue
                        print(f"Failed to set Hi-Co after {max_retries} attempts")
                        print("Device might not support Hi-Co mode or there's a communication issue")
                        return False

                status = self.__serialConn.read()
                if status == b"0":
                    print("SUCCESSFULLY SET THE MSR605 TO HI-COERCIVITY")
                    return True

                print(f"Attempt {attempt + 1}: Unexpected response: {status}")
                if attempt < max_retries - 1:
                    print("Retrying...")
                    time.sleep(1)
                    continue

            except Exception as e:
                print(f"Attempt {attempt + 1}: Error setting Hi-Co: {e}")
                if attempt < max_retries - 1:
                    print("Retrying...")
                    time.sleep(1)
                    continue

        print(f"Failed to set Hi-Co after {max_retries} attempts")
        print("Device might not support Hi-Co mode or there's a communication issue")
        return False

    def set_low_co(self):
        """This command is used to set MSR605 status to write Low-Co card.

        Hi-Coercivity (Hi-Co) is just one kind of magstripe card, the other
        being Low-Coercivity (Low-Co), google for more info

        Args:
            None

        Returns:
            Nothing

        Raises:
            SetCoercivityError: An error occurred when setting the coercivity
        """

        print("\nSETTING THE MSR605 TO LOW-COERCIVITY")

        # command code for setting the MSR605 to Low-Coercivity
        self.__serialConn.write(ESCAPE + LOW_CO)
        self.__serialConn.flush()

        # response/output from the MSR605
        # for some reason i get this response before getting to the escape character EVU3.10

        # if this is false than move on to the next part of the response
        if self.__serialConn.read() != ESCAPE:

            # just read until the 0 of the EVU3.10 response
            self.read_until("0", 4, False)

            # after reading that weird response,i check if there is an ESCAPE character
            if self.__serialConn.read() != ESCAPE:
                raise cardReaderExceptions.SetCoercivityError(
                    "SETTING THE DEVICE TO LOW-CO " "ERROR, looking for ESCAPE(\x1b)",
                    "low",
                )

        if self.__serialConn.read() != b"0":
            raise cardReaderExceptions.SetCoercivityError(
                "SETTING THE DEVICE TO LOW-CO ERROR, "
                "looking for 0(\x30), Device might have "
                "not been set to Low-Co",
                "low",
            )

        print("SUCCESSFULLY SET THE MSR605 TO LOW-COERCIVITY")

        return None

    def get_hi_or_low_co(self):
        """This command is to get MSR605 write status, is it in Hi/Low Co

        Hi-Coercivity (Hi-Co) is just one kind of magstripe card, the other
        being Low-Coercivity (Low-Co), google for more info

        Args:
            None

        Returns:
            A string that contains what mode the MSR605 card reader/writer is in

            ex:
                HI-CO
                LOW-CO

        Raises:
            GetCoercivityError: An error occurred when setting the coercivity
        """

        print("\nGETTING THE MSR60 COERCIVITY (HI OR LOW)")

        # command code for getting the MSR605 Coercivity
        self.__serialConn.write(ESCAPE + HI_OR_LOW_CO)
        self.__serialConn.flush()

        # response/output from the MSR605
        # for some reason i get this response before getting to the escape character EVU3.10

        # if this is false than move on to the next part of the response
        if self.__serialConn.read() != ESCAPE:

            # just read until the 0 of the EVU3.10 response
            self.read_until("0", 4, False)

            # after reading that weird response,i check if there is an ESCAPE character
            if self.__serialConn.read() != ESCAPE:
                raise cardReaderExceptions.GetCoercivityError(
                    "HI-CO OR LOW-CO ERROR, looking" "for ESCAPE(\x1b)"
                )

        coMode = self.__serialConn.read()

        if coMode == b"h":
            print("COERCIVITY: HI-CO")
            return "HI-CO"

        elif coMode == b"l":
            print("COERCIVITY: LOW-CO")
            return "LOW-CO"

        else:
            raise cardReaderExceptions.GetCoercivityError(
                "HI-CO OR LOW-CO ERROR, looking for H(\x48) "
                "or L(\x4c), don't know if its in superposition "
                "or what lol"
            )

    # ***************************************************
    #
    #     Data Processing (lol idk what to call these)
    #
    # ***************************************************

    def read_until(self, endCharacter, trackNum, compareToISO):
        """This reads from the serial COM port and continues to read until it reaches
            the end character (endCharacter)


        Args:
            endCharacter: this is character (like a delimiter), the function returns all
                            the data up to this character, ex: ESCAPE, 's'


            trackNum: this is an integer between 1 and 3, the # represents a track #, it
                        is used to check if the track data fits the ISO standard, it is
                        sorta canonicalized, used in the iso_standard_track_check function

            compareToISO: this is a boolean that if True will use the trackNum provided and
                            compare the data provided with the ISO Standard for Magnetic Strip
                            cards, if False the ISO Standard check will not be run


        Returns:
            A string that contains all the data of a track upto a certain character

            ex of track #1:
                A1234568^John Snow^           0123,

        Raises:
            Nothing
        """

        # counter
        i = 0

        # track 3 can contain more characters than track 1 or 2, it being 107 characters
        # this is just a small check, doesn't need to be there but i thought might as well
        # conform to the ISO standard and make sure we don't have an infinite loop
        if trackNum == 1:
            cond = 79
        elif trackNum == 2:
            cond = 40
        else:
            cond = 107

        string = ""

        while i < cond:
            strCompare = self.__serialConn.read()
            str = strCompare.decode()

            # only runs the ISO checks if required
            if compareToISO:
                # checks if the track data is valid based on the track data
                if not (
                    strCompare == ESCAPE
                    or strCompare == FILE_SEPERATOR
                    or strCompare == ACKNOWLEDGE
                    or strCompare == START_OF_HEADING
                    or strCompare == START_OF_TEXT
                    or strCompare == END_OF_TEXT
                ):

                    if iso_standard_track_check(str, trackNum) == False:
                        continue

            # if the special End of Line character is read, usually is the control character (ex: ESCAPE)

            if isinstance(endCharacter, bytes):
                if str == endCharacter.decode():
                    return string

            else:
                if str == endCharacter:
                    return string

            if strCompare != ESCAPE:
                string += str  # keeps accumlating the track data

            i += 1

        # some cards i tried didn't follow the format/standard they were suppposed to, so rather than
        # adding special cases, i just return the data
        return string

    def status_read(self):
        """This reads the Status Byte of the response from the MSR605


        Args:
           None

        Returns:
           Nothing

        Raises:
            StatusError: An error occurred when the MSR605 was performing the function you
                            requested
        """

        # reads in the Status Byte
        status = (self.__serialConn.read()).decode()
        print("STATUS: ", status)
        # checks what the stauts byte coorelates with, based off of the info provided from the
        # MSR605  programming manual
        if status == "0":
            print("CARD SUCCESSFULLY READ")

        elif status == "1":
            print("[Datablock] Error: 1(0x30h), 'Error, Write, or read error'")
            raise cardReaderExceptions.StatusError(
                "[Datablock] Error, 'Error, Write, or read error'", 1
            )

        elif status == "2":
            print("[Datablock] Error: 2(0x32h), 'Command format error'")
            raise cardReaderExceptions.StatusError(
                "[Datablock] Error, 'Command format error'", 2
            )

        elif status == "4":
            print("[Datablock] Error: 4(0x34h), 'Invalid command'")
            raise cardReaderExceptions.StatusError(
                "[Datablock] Error, 'Invalid command'", 4
            )

        elif status == "9":
            print(
                "[Datablock] Error: 9(0x39h), 'Invalid card swipe when in write MODE'"
            )
            raise cardReaderExceptions.StatusError(
                "[Datablock] Error, 'Invalid card swipe when in write " "mode'", 9
            )

        else:
            print("UNKNOWN STATUS: " + status)

        return None

    # ***********************
    #
    #     Setter/Getters
    #
    # ***********************

    def getSerialConn(self):
        return self.__serialConn

    def setSerialConn(self, serialConn):
        self.__serialConn = serialConn

    def _check_connection(self):
        """Check if serial connection is established.
        
        Returns:
            bool: True if connection is established, False otherwise
            
        Raises:
            MSR605ConnectError: If no connection is established
        """
        if self.__serialConn is None:
            raise cardReaderExceptions.MSR605ConnectError(
                "No serial connection established. "
                "Please connect to the MSR605 first using the connect() method."
            )
        return True

    def get_device_model(self):
        """This command is used to get the model of MSR605.

        Args:
            None

        Returns:
            A string that contains the device model

            ex: 3

        Raises:
            GetDeviceModelError: An error occurred when obtaining the device model
        """

        print("\nGETTING THE DEVICE MODEL")

        # command code for getting the device model
        self.__serialConn.write(ESCAPE + DEVICE_MODEL)
        self.__serialConn.flush()

        # response/output from the MSR605
        if self.__serialConn.read() != ESCAPE:
            raise cardReaderExceptions.GetDeviceModelError(
                "GETTING DEVICE MODEL ERROR, looking " "for ESCAPE(\x1b)"
            )

        model = (self.__serialConn.read()).decode()
        print("MODEL: " + model)

        if self.__serialConn.read() != b"S":
            raise cardReaderExceptions.GetDeviceModelError(
                "GETTING DEVICE MODEL ERROR, looking for "
                "S(\x53), check the response, the model "
                "might be right"
            )

        print("SUCCESSFULLY RETRIEVED THE DEVICE MODEL")

        return model

    def get_firmware_version(self):
        """This command can get the firmware version of MSR605.
    
        Args:
            None
    
        Returns:
            A string that contains the firmware version
            
            ex: R
            
    
        Raises:
            GetFirmwareVersionError: An error occurred when getting the MSR605 firmware \
                                        version
        """

        print("\nGETTING THE FIRMWARE VERSION OF THE MSR605")

        # command code for getting the firmware version of the MSR605
        self.__serialConn.write(ESCAPE + FIRMWARE)
        self.__serialConn.flush()

        # response/output from the MSR605
        if self.__serialConn.read() != ESCAPE:
            raise cardReaderExceptions.GetFirmwareVersionError(
                "GETTING FIRMWARE VERSION ERROR, " "looking for ESCAPE(\x1b)"
            )

        firmware = (self.__serialConn.read()).decode()

        print("FIRMWARE: " + firmware)

        print("SUCCESSFULLY RETRIEVED THE FIRMWARE VERSION")
        return firmware

    def decode_tracks(self):
        """This command reads and decodes the data from all tracks on the card.

        Args:
            None

        Returns:
            None

        Raises:
            DecodeError: An error occurred when trying to decode the card data
        """
        try:
            print("[DEBUG] Starting decode_tracks")
            # First read the card to get the track data
            tracks = self.read_card()
            print(f"[DEBUG] Raw tracks data: {tracks}")
            if not isinstance(tracks, (list, tuple)):
                print(f"[ERROR] read_card did not return a list/tuple: {tracks}")
                raise cardReaderExceptions.DecodeError(
                    f"Failed to decode card data: {str(tracks)}"
                )
            for i, track in enumerate(tracks):
                print(f"[DEBUG] Track {i+1} raw: {track}")
                if track:
                    print(f"Track {i+1} decoded data:")
                    print(f"Raw data: {track}")
                    if i == 0:  # Track 1: %B1234567890123445^DOE/JOHN^YYMMDD...
                        # Format: %B[card number]^[NAME]^YYMMDD...
                        try:
                            if track.startswith("%B"):
                                parts = track[2:].split("^")
                                card_number = parts[0] if len(parts) > 0 else ""
                                name = parts[1].strip() if len(parts) > 1 else ""
                                exp = parts[2][:4] if len(parts) > 2 else ""
                                exp_fmt = (
                                    f"20{exp[0:2]}/{exp[2:4]}" if len(exp) == 4 else ""
                                )
                                print(f"  Card Number      : {card_number}")
                                print(f"  Cardholder Name  : {name}")
                                print(f"  Expiration Date  : {exp_fmt}")
                            else:
                                print("  Track 1 format not recognized.")
                        except Exception as e:
                            print(f"  Track 1 decode error: {e}")
                    elif i == 1:  # Track 2: ;1234567890123445=YYMMDDSSS...
                        # Format: ;[card number]=YYMMDDSSS...
                        try:
                            if track.startswith(";"):
                                parts = track[1:].split("=")
                                card_number = parts[0] if len(parts) > 0 else ""
                                exp = parts[1][:4] if len(parts) > 1 else ""
                                exp_fmt = (
                                    f"20{exp[0:2]}/{exp[2:4]}" if len(exp) == 4 else ""
                                )
                                service_code = (
                                    parts[1][4:7]
                                    if len(parts) > 1 and len(parts[1]) >= 7
                                    else ""
                                )
                                print(f"  Card Number      : {card_number}")
                                print(f"  Expiration Date  : {exp_fmt}")
                                print(f"  Service Code     : {service_code}")
                            else:
                                print("  Track 2 format not recognized.")
                        except Exception as e:
                            print(f"  Track 2 decode error: {e}")
                    elif i == 2:  # Track 3
                        print(
                            "  Track 3 data is typically proprietary format or bank use only."
                        )
                    print()
            print(f"[DEBUG] Finished decoding tracks. Returning: {tracks}")
            return tracks

        except (cardReaderExceptions.CardReadError, Exception) as e:
            print(f"[DEBUG] Exception in decode_tracks: {e}")
            import traceback

            traceback.print_exc()
            raise cardReaderExceptions.DecodeError(
                f"Failed to decode card data: {str(e)}"
            )

    def initialize_device(self):
        """Initialize the MSR605 device with fallback coercivity mode."""
        print("\nINITIALIZING THE MSR605")
        
        # Try Hi-Co first
        if self.set_hi_co():
            print("Device initialized in Hi-Co mode")
            return True
        else:
            print("Hi-Co mode failed, trying Low-Co mode...")
            if self.set_low_co():
                print("Device initialized in Low-Co mode")
                return True
            else:
                print("Failed to initialize device in any coercivity mode")
                return False
