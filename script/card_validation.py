"""card_validation.py

This module provides advanced data validation and multi-device synchronization
capabilities for the MSR605 application.
"""

import re
import json
import time
import hashlib
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any, Callable
from dataclasses import dataclass, field
from enum import Enum, auto

from .card_formats import CardFormat, CardFormatManager


class ValidationLevel(Enum):
    """Validation levels for card data."""
    NONE = auto()
    BASIC = auto()    # Basic format validation
    STRICT = auto()   # Strict format + checksum validation
    EXTENDED = auto() # Extended validation with external services


class ValidationRule:
    """Base class for validation rules."""
    
    def validate(self, track_data: str, track_num: int, format: CardFormat) -> Tuple[bool, str]:
        """Validate track data.
        
        Args:
            track_data: The track data to validate
            track_num: Track number (1, 2, or 3)
            format: The card format being validated
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        raise NotImplementedError


class RegexRule(ValidationRule):
    """Validates track data against a regular expression pattern."""
    
    def __init__(self, pattern: str, error_message: str = "Invalid format"):
        self.pattern = pattern
        self.error_message = error_message
        self._compiled = re.compile(pattern)
    
    def validate(self, track_data: str, track_num: int, format: CardFormat) -> Tuple[bool, str]:
        if not self._compiled.fullmatch(track_data):
            return False, self.error_message
        return True, ""


class ChecksumRule(ValidationRule):
    """Validates track data using a checksum algorithm."""
    
    def __init__(self, algorithm: str = 'luhn', field_indices: List[int] = None):
        self.algorithm = algorithm.lower()
        self.field_indices = field_indices or [0]  # Default to first field
    
    def _luhn_checksum(self, card_number: str) -> bool:
        """Validate a card number using the Luhn algorithm."""
        def digits_of(n):
            return [int(d) for d in str(n)]
            
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10 == 0
    
    def validate(self, track_data: str, track_num: int, format: CardFormat) -> Tuple[bool, str]:
        if self.algorithm == 'luhn':
            # Extract the PAN (Primary Account Number) from track data
            pan = ''
            if track_num == 1 and '^' in track_data:
                pan = track_data.split('^')[0][1:]  # Remove leading %
            elif track_num == 2 and '=' in track_data:
                pan = track_data.split('=')[0][1:]  # Remove leading ;
            
            if pan and not self._luhn_checksum(pan):
                return False, f"Invalid {self.algorithm.upper()} checksum for PAN: {pan}"
        
        return True, ""


class ExpirationRule(ValidationRule):
    """Validates card expiration date."""
    
    def __init__(self, format_str: str = '%y%m'):
        self.format_str = format_str
    
    def validate(self, track_data: str, track_num: int, format: CardFormat) -> Tuple[bool, str]:
        if track_num not in [1, 2]:  # Expiration date typically on tracks 1 and 2
            return True, ""
            
        try:
            # Extract expiration date (format depends on track and card format)
            exp_date_str = ""
            if track_num == 1 and '^' in track_data and len(track_data.split('^')) > 2:
                # Track 1 format: %B123...^LASTNAME/FIRST^YYMM...
                exp_date_str = track_data.split('^')[2][:4]  # YYMM
            elif track_num == 2 and '=' in track_data:
                # Track 2 format: ;123...=YYMM...
                exp_date_str = track_data.split('=')[1][:4]  # YYMM
            
            if not exp_date_str or len(exp_date_str) != 4:
                return True, ""  # No expiration date to validate
                
            # Parse expiration date (YYMM)
            exp_date = datetime.strptime(exp_date_str, '%y%m')
            
            # Get current date at start of month for comparison
            current_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            if exp_date < current_date:
                return False, f"Card expired on {exp_date.strftime('%m/%Y')}"
                
        except (ValueError, IndexError):
            # If we can't parse the date, assume it's valid (let other validators handle format)
            pass
            
        return True, ""


class CardValidator:
    """Manages validation rules for card data."""
    
    def __init__(self):
        self._rules = {
            CardFormat.ISO_7811: {
                1: [
                    RegexRule(r'^%[0-9]{1,19}\^[A-Z /]{2,26}\^[0-9]{4}.*\?$', 
                            "Invalid Track 1 format"),
                    ChecksumRule('luhn')
                ],
                2: [
                    RegexRule(r'^;[0-9]{1,19}=[0-9]{4}.*\?$', 
                            "Invalid Track 2 format"),
                    ChecksumRule('luhn')
                ]
            },
            CardFormat.ISO_7813: {
                1: [
                    RegexRule(r'^%[A-Z]([0-9]{1,19})\^([A-Z /]{2,26})\^([0-9]{4}).*\?$', 
                            "Invalid ISO 7813 Track 1 format"),
                    ChecksumRule('luhn'),
                    ExpirationRule()
                ],
                2: [
                    RegexRule(r'^;([0-9]{1,19})=([0-9]{4}).*\?$', 
                            "Invalid ISO 7813 Track 2 format"),
                    ChecksumRule('luhn'),
                    ExpirationRule()
                ]
            },
            # Add rules for other formats as needed
        }
    
    def validate_track(self, track_data: str, track_num: int, 
                      format: CardFormat, level: ValidationLevel = ValidationLevel.STRICT) -> Tuple[bool, List[str]]:
        """Validate track data against the specified format and validation level.
        
        Args:
            track_data: The track data to validate
            track_num: Track number (1, 2, or 3)
            format: The card format to validate against
            level: Validation strictness level
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        if not track_data or level == ValidationLevel.NONE:
            return True, []
            
        errors = []
        
        # Get rules for this format and track
        format_rules = self._rules.get(format, {})
        track_rules = format_rules.get(track_num, [])
        
        # Apply basic format validation (always done)
        for rule in track_rules:
            is_valid, error = rule.validate(track_data, track_num, format)
            if not is_valid and error:
                errors.append(error)
        
        # Additional validation based on level
        if level == ValidationLevel.EXTENDED:
            # Add extended validation rules (e.g., check against blacklists, etc.)
            pass
            
        return len(errors) == 0, errors
    
    def validate_card(self, tracks: List[str], format: CardFormat, 
                     level: ValidationLevel = ValidationLevel.STRICT) -> Tuple[bool, Dict[int, List[str]]]:
        """Validate all tracks of a card.
        
        Args:
            tracks: List of track data (3 elements)
            format: The card format to validate against
            level: Validation strictness level
            
        Returns:
            Tuple of (is_valid, error_dict) where error_dict maps track numbers to error messages
        """
        all_errors = {}
        all_valid = True
        
        for i, track in enumerate(tracks, 1):
            if not track:
                continue
                
            is_valid, errors = self.validate_track(track, i, format, level)
            if not is_valid:
                all_valid = False
                all_errors[i] = errors
        
        return all_valid, all_errors


class DeviceSyncManager:
    """Manages synchronization between multiple MSR605 devices."""
    
    def __init__(self, sync_interval: float = 5.0, sync_dir: Optional[Path] = None):
        """Initialize the sync manager.
        
        Args:
            sync_interval: How often to check for updates (seconds)
            sync_dir: Directory for sync files. If None, uses a default directory.
        """
        self.sync_interval = sync_interval
        self.sync_dir = sync_dir or (Path.home() / '.msr605' / 'sync')
        self.sync_dir.mkdir(parents=True, exist_ok=True)
        
        self._device_id = self._generate_device_id()
        self._last_sync = {}
        self._running = False
        self._thread = None
        self._callbacks = []
        self._lock = threading.Lock()
    
    def _generate_device_id(self) -> str:
        """Generate a unique ID for this device."""
        # Use a combination of hostname and MAC address for a reasonably unique ID
        import uuid
        import socket
        hostname = socket.gethostname()
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                       for elements in range(5, -1, -1)])
        return f"{hostname}_{mac}"
    
    def start(self) -> None:
        """Start the sync manager."""
        if self._running:
            return
            
        self._running = True
        self._thread = threading.Thread(target=self._sync_loop, daemon=True)
        self._thread.start()
    
    def stop(self) -> None:
        """Stop the sync manager."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)
            self._thread = None
    
    def register_callback(self, callback: Callable[[Dict], None]) -> None:
        """Register a callback for sync events.
        
        Args:
            callback: Function to call when sync data is received.
                     The function will be called with the sync data as a dict.
        """
        with self._lock:
            self._callbacks.append(callback)
    
    def unregister_callback(self, callback: Callable[[Dict], None]) -> None:
        """Unregister a sync callback."""
        with self._lock:
            if callback in self._callbacks:
                self._callbacks.remove(callback)
    
    def _notify_callbacks(self, data: Dict) -> None:
        """Notify all registered callbacks of new sync data."""
        with self._lock:
            for callback in self._callbacks:
                try:
                    callback(data)
                except Exception as e:
                    print(f"Error in sync callback: {e}")
    
    def _sync_loop(self) -> None:
        """Background thread that handles periodic sync."""
        while self._running:
            try:
                self.sync()
            except Exception as e:
                print(f"Error during sync: {e}")
                
            # Wait for the next sync interval
            time.sleep(self.sync_interval)
    
    def sync(self) -> None:
        """Perform a sync operation."""
        # Read all sync files
        sync_files = list(self.sync_dir.glob('*.json'))
        
        for sync_file in sync_files:
            try:
                # Skip our own sync files
                if sync_file.stem == self._device_id:
                    continue
                
                # Check if we've seen this file before
                last_modified = sync_file.stat().st_mtime
                if sync_file.name in self._last_sync and \
                   self._last_sync[sync_file.name] >= last_modified:
                    continue
                
                # Read and process the sync file
                with open(sync_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Update last sync time
                self._last_sync[sync_file.name] = last_modified
                
                # Notify callbacks
                self._notify_callbacks(data)
                
            except (json.JSONDecodeError, OSError) as e:
                print(f"Error reading sync file {sync_file}: {e}")
    
    def send_update(self, data: Dict) -> None:
        """Send an update to other devices.
        
        Args:
            data: Dictionary containing the data to sync
        """
        try:
            # Add metadata
            data['_timestamp'] = time.time()
            data['_device_id'] = self._device_id
            
            # Write to our sync file
            sync_file = self.sync_dir / f"{self._device_id}.json"
            with open(sync_file, 'w', encoding='utf-8') as f:
                json.dump(data, f)
                
        except Exception as e:
            print(f"Error sending sync update: {e}")
    
    def __del__(self):
        """Clean up resources."""
        self.stop()
