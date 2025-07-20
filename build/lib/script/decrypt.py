"""
Advanced Card Data Decryption Module

This module provides comprehensive functionality for decrypting sensitive card data
including PIN blocks and track data using various industry-standard encryption algorithms.
Supports DES, 3DES, and AES encryption schemes with multiple modes of operation.

Features:
- Multiple encryption algorithms (DES/3DES/AES)
- Support for various PIN block formats
- Track 1 and Track 2 data decryption
- Key derivation functions
- Comprehensive error handling and logging
"""

import binascii
import logging
import hmac
import hashlib
from enum import Enum
from typing import Union, Optional, Dict, Any, Tuple, List
from dataclasses import dataclass
from datetime import datetime

# Third-party imports
from Crypto.Cipher import DES, DES3, AES
from Crypto.Util.Padding import unpad
from Crypto.Protocol.KDF import PBKDF2

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KeyType(Enum):
    """Supported key types for encryption/decryption."""
    SINGLE_DES = 'single_des'
    DOUBLE_DES = 'double_des'
    TRIPLE_DES = 'triple_des'
    AES_128 = 'aes_128'
    AES_192 = 'aes_192'
    AES_256 = 'aes_256'

class PinBlockFormat(Enum):
    """Supported PIN block formats."""
    ISO9564_1 = 'ISO9564-1'  # ISO-0
    ISO9564_3 = 'ISO9564-3'  # ISO-3
    VISA1 = 'VISA1'
    VISA3 = 'VISA3'
    VISA4 = 'VISA4'
    ECI4 = 'ECI4'

@dataclass
class DecryptionResult:
    """
    Container for decryption results with enhanced display and formatting capabilities.
    
    Attributes:
        success: Whether the decryption was successful
        data: The decrypted data (can be string or bytes)
        algorithm: The encryption algorithm used
        key_type: Type of key used for decryption
        timestamp: When the decryption was performed
        error: Error message if decryption failed
        metadata: Additional metadata about the decryption
    """
    success: bool
    data: Optional[Union[str, bytes]]
    algorithm: str
    key_type: str
    timestamp: str
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize metadata if not provided."""
        if not hasattr(self, 'metadata') or self.metadata is None:
            self.metadata = {}

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the result to a dictionary with enhanced formatting.
        
        Returns:
            Dictionary containing all result data with proper formatting
        """
        result = {
            'status': 'SUCCESS' if self.success else 'ERROR',
            'timestamp': self.timestamp,
            'algorithm': self.algorithm,
            'key_type': self.key_type,
            'data': self._format_data_for_output(),
        }
        
        if not self.success:
            result['error'] = self.error
            
        # Add any additional metadata
        result.update(self.metadata)
        return result
    
    def _format_data_for_output(self) -> Union[str, Dict[str, Any]]:
        """Format the decrypted data for display."""
        if self.data is None:
            return "No data"
            
        # Convert bytes to string if needed
        if isinstance(self.data, bytes):
            try:
                data_str = self.data.decode('utf-8')
            except UnicodeDecodeError:
                data_str = self.data.hex(' ', 1)  # Show hex with spaces between bytes
        else:
            data_str = str(self.data)
            
        # Try to parse track data if it looks like it
        if any(track in self.algorithm.lower() for track in ['track', 'iso9564']):
            return self._format_track_data(data_str)
            
        return data_str
    
    def _format_track_data(self, track_data: str) -> Dict[str, Any]:
        """Format track data into a structured format."""
        if not track_data or not isinstance(track_data, str):
            return {"raw": track_data}
            
        result = {"raw": track_data}
        
        try:
            # Try to parse track 1 (format: %B1234567890123456^CARDHOLDER/NAME^YYMM...)
            if track_data.startswith('%B') and '^' in track_data:
                parts = track_data[2:].split('^')
                if len(parts) >= 3:
                    result.update({
                        'track_type': 'Track 1',
                        'card_number': parts[0],
                        'cardholder_name': parts[1].split('/')[0].strip(),
                        'expiration': f"{parts[2][2:4]}/{parts[2][:2]}" if len(parts[2]) >= 4 else None,
                        'service_code': parts[2][4:7] if len(parts[2]) >= 7 else None,
                    })
            
            # Try to parse track 2 (format: ;1234567890123456=YYMM...)
            elif track_data.startswith(';') and '=' in track_data:
                parts = track_data[1:].split('=')
                if len(parts) >= 2:
                    result.update({
                        'track_type': 'Track 2',
                        'card_number': parts[0][:16],
                        'expiration': f"{parts[1][2:4]}/{parts[1][:2]}" if len(parts[1]) >= 4 else None,
                        'service_code': parts[1][4:7] if len(parts[1]) >= 7 else None,
                    })
                    
        except Exception as e:
            logger.warning(f"Error parsing track data: {str(e)}")
            
        return result
    
    def format_for_display(self, include_metadata: bool = True) -> str:
        """
        Format the result for display in the UI.
        
        Args:
            include_metadata: Whether to include metadata in the output
            
        Returns:
            Formatted string ready for display
        """
        lines = [
            f"╔{'═' * 78}╗",
            f"║ {'DECRYPTION RESULT':^76} ║",
            f"╠{'═' * 78}╣",
            f"║ {'Status:':<15} {'✅ SUCCESS' if self.success else '❌ ERROR':<61} ║",
            f"║ {'Algorithm:':<15} {self.algorithm:<61} ║",
            f"║ {'Key Type:':<15} {self.key_type:<61} ║",
            f"║ {'Timestamp:':<15} {self.timestamp:<61} ║",
        ]
        
        if not self.success:
            lines.append(f"║ {'Error:':<15} {str(self.error)[:74]:<61} ║")
        
        # Add formatted data
        formatted_data = self._format_data_for_display()
        if formatted_data:
            lines.append(f"╠{'═' * 78}╣")
            lines.append(f"║ {'DECRYPTED DATA':^76} ║")
            lines.append(f"╠{'═' * 78}╣")
            lines.extend(formatted_data)
        
        # Add metadata if requested
        if include_metadata and self.metadata:
            lines.append(f"╠{'═' * 78}╣")
            lines.append(f"║ {'METADATA':^76} ║")
            lines.append(f"╠{'═' * 78}╣")
            for key, value in self.metadata.items():
                value_str = str(value)
                if len(value_str) > 60:
                    value_str = value_str[:57] + '...'
                lines.append(f"║ {key + ':':<20} {value_str:<54} ║")
        
        lines.append(f"╚{'═' * 78}╝")
        return '\n'.join(lines)
    
    def _format_data_for_display(self) -> List[str]:
        """Format the data for display in the UI."""
        if not self.data:
            return []
            
        formatted_data = self._format_data_for_output()
        
        if isinstance(formatted_data, dict):
            lines = []
            for key, value in formatted_data.items():
                if key == 'raw':
                    continue
                if isinstance(value, dict):
                    lines.append(f"║ {key.upper():<20} {'':<54} ║")
                    for subkey, subvalue in value.items():
                        lines.append(f"║   {subkey.replace('_', ' ').title():<17} {str(subvalue)[:52]:<54} ║")
                else:
                    lines.append(f"║ {key.replace('_', ' ').title():<20} {str(value)[:57]:<54} ║")
            
            # Add raw data at the bottom if present and not too long
            if 'raw' in formatted_data and formatted_data['raw']:
                raw_data = formatted_data['raw']
                if len(raw_data) > 60:
                    raw_data = raw_data[:57] + '...'
                lines.append(f"╠{'─' * 78}╣")
                lines.append(f"║ {'Raw Data:':<20} {raw_data:<54} ║")
                
            return lines
            
        # For non-dict data, just show it directly
        data_lines = []
        data_str = str(formatted_data)
        for i in range(0, len(data_str), 60):
            chunk = data_str[i:i+60]
            data_lines.append(f"║ {chunk:<76} ║")
            
        return data_lines

class CardDataDecryptor:
    """
    Advanced card data decryptor supporting multiple encryption standards.
    
    This class provides methods to decrypt various types of card data including
    PIN blocks and track data using industry-standard encryption algorithms.
    """
    
    def __init__(self, 
                 key: bytes, 
                 key_type: Union[KeyType, str] = KeyType.TRIPLE_DES,
                 iv: Optional[bytes] = None,
                 kcv: Optional[bytes] = None):
        """
        Initialize the decryptor with encryption key and parameters.
        
        Args:
            key: The encryption key in bytes
            key_type: Type of key (KeyType enum or string representation)
            iv: Initialization vector if required
            kcv: Key Check Value for key verification (optional)
            
        Raises:
            ValueError: If key validation fails
            TypeError: If key_type is invalid
        """
        # Convert string key_type to enum if needed
        if isinstance(key_type, str):
            try:
                key_type = KeyType(key_type.lower())
            except ValueError as e:
                raise ValueError(f"Invalid key_type: {key_type}") from e
                
        self.key = key
        self.key_type = key_type
        self.iv = iv
        self.kcv = kcv
        
        # Validate key length based on key type
        self._validate_key()
        
        # Verify key with KCV if provided
        if kcv:
            self.verify_kcv()
    
    def _validate_key(self) -> None:
        """Validate the key based on its type."""
        key_length = len(self.key)
        
        if self.key_type == KeyType.SINGLE_DES:
            if key_length != 8:
                raise ValueError(f"Single DES requires 8-byte key, got {key_length} bytes")
        elif self.key_type == KeyType.DOUBLE_DES:
            if key_length != 16:
                raise ValueError(f"Double-length 3DES requires 16-byte key, got {key_length} bytes")
        elif self.key_type == KeyType.TRIPLE_DES:
            if key_length != 24:
                raise ValueError(f"Triple-length 3DES requires 24-byte key, got {key_length} bytes")
        elif self.key_type == KeyType.AES_128:
            if key_length != 16:
                raise ValueError(f"AES-128 requires 16-byte key, got {key_length} bytes")
        elif self.key_type == KeyType.AES_192:
            if key_length != 24:
                raise ValueError(f"AES-192 requires 24-byte key, got {key_length} bytes")
        elif self.key_type == KeyType.AES_256:
            if key_length != 32:
                raise ValueError(f"AES-256 requires 32-byte key, got {key_length} bytes")
        else:
            raise ValueError(f"Unsupported key type: {self.key_type}")
    
    def verify_kcv(self) -> bool:
        """Verify the key using Key Check Value (KCV).
        
        Returns:
            bool: True if KCV verification passes
            
        Raises:
            ValueError: If KCV verification fails
        """
        if not self.kcv:
            logger.warning("No KCV provided for verification")
            return True
            
        # Calculate KCV by encrypting zeros
        if self.key_type in (KeyType.SINGLE_DES, KeyType.DOUBLE_DES, KeyType.TRIPLE_DES):
            cipher = self._get_des_cipher()
            result = cipher.encrypt(b'\x00' * 8)
            calculated_kcv = result[:3]  # First 3 bytes for DES/3DES
        else:  # AES
            cipher = AES.new(self.key, AES.MODE_ECB)
            result = cipher.encrypt(b'\x00' * 16)
            calculated_kcv = result[:3]  # First 3 bytes for AES
        
        if calculated_kcv != self.kcv:
            raise ValueError(
                f"KCV verification failed. Expected {self.kcv.hex().upper()}, "
                f"got {calculated_kcv.hex().upper()}"
            )
        
        logger.info("KCV verification successful")
        return True
    def _get_des_cipher(self, mode: str = 'ECB') -> Union[DES.DES3Cipher, DES.DESCipher]:
        """Get the appropriate DES/3DES cipher based on key type.
        
        Args:
            mode: Cipher mode ('ECB', 'CBC', etc.)
            
        Returns:
            Cipher object for encryption/decryption
            
        Raises:
            ValueError: If mode is not supported
        """
        mode = mode.upper()
        iv = self.iv or b'\x00' * 8
        
        if mode == 'ECB':
            if self.key_type in (KeyType.SINGLE_DES, KeyType.DOUBLE_DES, KeyType.TRIPLE_DES):
                if self.key_type == KeyType.SINGLE_DES:
                    return DES.new(self.key[:8], DES.MODE_ECB)
                return DES3.new(self.key, DES.MODE_ECB)
            else:
                raise ValueError(f"DES cipher not available for key type: {self.key_type}")
        elif mode == 'CBC':
            if self.key_type in (KeyType.SINGLE_DES, KeyType.DOUBLE_DES, KeyType.TRIPLE_DES):
                if self.key_type == KeyType.SINGLE_DES:
                    return DES.new(self.key[:8], DES.MODE_CBC, iv=iv)
                return DES3.new(self.key, DES.MODE_CBC, iv=iv)
            else:
                raise ValueError(f"DES cipher not available for key type: {self.key_type}")
        else:
            raise ValueError(f"Unsupported cipher mode: {mode}")

    @staticmethod
    def _pad_pkcs7(data: bytes, block_size: int) -> bytes:
        """Pad data using PKCS#7 padding.
        
        Args:
            data: Data to be padded
            block_size: Block size for padding
            
        Returns:
            Padded data as bytes
        """
        if not isinstance(data, bytes):
            raise TypeError(f"Data must be bytes, got {type(data).__name__}")
            
        padding_length = block_size - (len(data) % block_size)
        return data + bytes([padding_length] * padding_length)

    @staticmethod
    def _prepare_pan(pan: str, length: int = 12) -> bytes:
        """Prepare PAN for PIN block calculation.
        
        Args:
            pan: Primary Account Number (PAN)
            length: Desired length of PAN part (default: 12)
            
        Returns:
            Formatted PAN as bytes
            
        Raises:
            ValueError: If PAN is invalid
        """
        if not pan or not isinstance(pan, str) or not pan.isdigit():
            raise ValueError("PAN must be a non-empty numeric string")
            
        # Remove non-digit characters and get the PAN without check digit
        pan_digits = ''.join(c for c in pan if c.isdigit())
        if not pan_digits:
            raise ValueError("No valid digits found in PAN")
            
        pan_without_check = pan_digits[:-1]  # Remove check digit
        
        # Take rightmost 'length' digits or pad with zeros
        pan_part = pan_without_check[-length:].zfill(length)
        
        # Format: 0000 + pan_part (12 digits) = 16 hex digits (8 bytes)
        return bytes.fromhex(f"0000{pan_part}")

    def decrypt_pin_block(self, 
                         encrypted_pin_block: bytes, 
                         pan: str, 
                         pin_block_format: Union[PinBlockFormat, str] = PinBlockFormat.ISO9564_1) -> DecryptionResult:
        """
        Decrypt a PIN block using the specified format.
        
        Args:
            encrypted_pin_block: The encrypted PIN block
            pan: Primary Account Number (PAN) for PIN block validation
            pin_block_format: PIN block format (default: ISO9564-1)
            
        Returns:
            DecryptionResult object containing the decrypted PIN or error information
            
        Raises:
            ValueError: If input validation fails
            TypeError: If input types are incorrect
        """
        timestamp = datetime.utcnow().isoformat()
        
        try:
            # Input validation
            if not isinstance(encrypted_pin_block, bytes):
                raise TypeError(f"encrypted_pin_block must be bytes, got {type(encrypted_pin_block).__name__}")
                
            if not pan or not isinstance(pan, str) or not pan.isdigit():
                raise ValueError("PAN must be a non-empty numeric string")
            
            # Convert string format to enum if needed
            if isinstance(pin_block_format, str):
                try:
                    pin_block_format = PinBlockFormat(pin_block_format.upper())
                except ValueError as e:
                    raise ValueError(f"Unsupported PIN block format: {pin_block_format}") from e
            
            # Handle different PIN block formats
            if pin_block_format == PinBlockFormat.ISO9564_1:
                return self._decrypt_iso9564_1(encrypted_pin_block, pan, timestamp)
            elif pin_block_format == PinBlockFormat.ISO9564_3:
                return self._decrypt_iso9564_3(encrypted_pin_block, pan, timestamp)
            elif pin_block_format in (PinBlockFormat.VISA1, PinBlockFormat.VISA3, PinBlockFormat.VISA4):
                return self._decrypt_visa_format(encrypted_pin_block, pan, pin_block_format, timestamp)
            elif pin_block_format == PinBlockFormat.ECI4:
                return self._decrypt_eci4(encrypted_pin_block, pan, timestamp)
            else:
                error_msg = f"Unsupported PIN block format: {pin_block_format}"
                logger.error(error_msg)
                return DecryptionResult(
                    success=False,
                    data=None,
                    algorithm=str(self.key_type),
                    key_type=self.key_type.value,
                    timestamp=timestamp,
                    error=error_msg
                )
                
        except Exception as e:
            error_msg = f"PIN decryption failed: {str(e)}"
            logger.exception(error_msg)
            return DecryptionResult(
                success=False,
                data=None,
                algorithm=str(self.key_type),
                key_type=self.key_type.value,
                timestamp=timestamp,
                error=error_msg
            )
    
    def _decrypt_iso9564_1(self, 
                          encrypted_pin_block: bytes, 
                          pan: str,
                          timestamp: str) -> DecryptionResult:
        """Decrypt ISO 9564-1 (ISO-0) PIN block format."""
        try:
            # Decrypt the PIN block
            if len(encrypted_pin_block) % 8 != 0:
                encrypted_pin_block = self._pad_pkcs7(encrypted_pin_block, 8)
                
            cipher = self._get_des_cipher()
            pin_block = cipher.decrypt(encrypted_pin_block)
            
            # XOR with PAN to get clear PIN block
            pan_data = self._prepare_pan(pan)
            clear_pin_block = bytes(a ^ b for a, b in zip(pin_block, pan_data))
            
            # Extract PIN (format: 0x0N P1 P2 P3 P4 F...F where N is PIN length)
            pin_length = clear_pin_block[0] & 0x0F
            if pin_length < 4 or pin_length > 12:
                raise ValueError(f"Invalid PIN length: {pin_length}")
                
            pin_digits = clear_pin_block[1:1+pin_length]
            pin = ''.join(f"{d & 0x0F:01d}" for d in pin_digits)
            
            return DecryptionResult(
                success=True,
                data=pin,
                algorithm="3DES_ECB" if self.key_type in (KeyType.DOUBLE_DES, KeyType.TRIPLE_DES) else "DES_ECB",
                key_type=self.key_type.value,
                timestamp=timestamp
            )
            
        except Exception as e:
            error_msg = f"ISO9564-1 decryption failed: {str(e)}"
            logger.exception(error_msg)
            return DecryptionResult(
                success=False,
                data=None,
                algorithm=str(self.key_type),
                key_type=self.key_type.value,
                timestamp=timestamp,
                error=error_msg
            )
    
    def _decrypt_iso9564_3(self, 
                          encrypted_pin_block: bytes, 
                          pan: str,
                          timestamp: str) -> DecryptionResult:
        """Decrypt ISO 9564-3 (ISO-3) PIN block format."""
        try:
            # Implementation for ISO-3 format
            # (Similar structure to _decrypt_iso9564_1 but with different format)
            raise NotImplementedError("ISO9564-3 decryption not yet implemented")
            
        except Exception as e:
            error_msg = f"ISO9564-3 decryption failed: {str(e)}"
            logger.exception(error_msg)
            return DecryptionResult(
                success=False,
                data=None,
                algorithm=str(self.key_type),
                key_type=self.key_type.value,
                timestamp=timestamp,
                error=error_msg
            )
    
    def _decrypt_visa_format(self, 
                           encrypted_pin_block: bytes, 
                           pan: str,
                           format_type: PinBlockFormat,
                           timestamp: str) -> DecryptionResult:
        """Decrypt VISA format PIN blocks (VISA1, VISA3, VISA4)."""
        try:
            # Implementation for VISA formats
            # (Similar structure to _decrypt_iso9564_1 but with VISA-specific logic)
            raise NotImplementedError(f"{format_type.value} decryption not yet implemented")
            
        except Exception as e:
            error_msg = f"{format_type.value} decryption failed: {str(e)}"
            logger.exception(error_msg)
            return DecryptionResult(
                success=False,
                data=None,
                algorithm=str(self.key_type),
                key_type=self.key_type.value,
                timestamp=timestamp,
                error=error_msg
            )
    
    def _decrypt_eci4(self, 
                     encrypted_pin_block: bytes, 
                     pan: str,
                     timestamp: str) -> DecryptionResult:
        """Decrypt ECI-4 PIN block format."""
        try:
            # Implementation for ECI-4 format
            # (Similar structure to _decrypt_iso9564_1 but with ECI-4 specific logic)
            raise NotImplementedError("ECI-4 decryption not yet implemented")
            
        except Exception as e:
            error_msg = f"ECI-4 decryption failed: {str(e)}"
            logger.exception(error_msg)
            return DecryptionResult(
                success=False,
                data=None,
                algorithm=str(self.key_type),
                key_type=self.key_type.value,
                timestamp=timestamp,
                error=error_msg
            )
    
    def decrypt_track_data(self, encrypted_data: bytes, 
                          algorithm: str = '3DES_CBC') -> str:
        """
        Decrypt track data using the specified algorithm.
        
        Args:
            encrypted_data: The encrypted track data
            algorithm: Encryption algorithm to use (3DES_CBC, 3DES_ECB, AES_CBC, etc.)
            
        Returns:
            Decrypted track data as string
        """
        try:
            if algorithm.upper() == '3DES_CBC':
                cipher = DES3.new(self.key, DES3.MODE_CBC, iv=self.iv)
                decrypted = cipher.decrypt(encrypted_data)
                # Remove padding and decode
                return unpad(decrypted, DES3.block_size).decode('ascii', errors='replace')
                
            elif algorithm.upper() == '3DES_ECB':
                cipher = DES3.new(self.key, DES3.MODE_ECB)
                decrypted = cipher.decrypt(encrypted_data)
                return unpad(decrypted, DES3.block_size).decode('ascii', errors='replace')
                
            elif algorithm.upper() == 'AES_CBC':
                if len(self.key) not in (16, 24, 32):
                    raise ValueError("AES key must be 16, 24, or 32 bytes")
                cipher = AES.new(self.key, AES.MODE_CBC, iv=self.iv)
                decrypted = cipher.decrypt(encrypted_data)
                return unpad(decrypted, AES.block_size).decode('ascii', errors='replace')
                
            else:
                raise ValueError(f"Unsupported algorithm: {algorithm}")
                
        except Exception as e:
            raise ValueError(f"Track data decryption failed: {str(e)}")
    
    def _get_des_cipher(self):
        """Get the appropriate DES/3DES cipher based on key type."""
        if self.key_type == 'single':
            return DES.new(self.key[:8], DES.MODE_ECB)
        elif self.key_type == 'double':
            # Double-length 3DES: K1, K2, K1
            key = self.key + self.key[:8]
            return DES3.new(key, DES3.MODE_ECB)
        else:  # triple
            return DES3.new(self.key, DES3.MODE_ECB)
    
    @staticmethod
    def _prepare_pan(pan: str) -> bytes:
        """Prepare PAN for PIN block calculation."""
        # Take rightmost 12 digits of PAN, excluding check digit
        pan_digits = pan[-13:-1] if len(pan) > 12 else pan
        pan_digits = pan_digits.zfill(12)
        # Format: 0000 + pan_digits
        return binascii.unhexlify('0000' + pan_digits)
    
    @staticmethod
    def _pad_pkcs7(data: bytes, block_size: int) -> bytes:
        """Pad data using PKCS#7 padding."""
        padding_length = block_size - (len(data) % block_size)
        return data + bytes([padding_length] * padding_length)

# Example usage
if __name__ == "__main__":
    # Example key (in a real application, this should be securely stored/retrieved)
    # This is a double-length 3DES key (16 bytes)
    SAMPLE_KEY = b'\x01\x23\x45\x67\x89\xAB\xCD\xEF\xFE\xDC\xBA\x98\x76\x54\x32\x10'
    
    # Example encrypted PIN block (for ISO 9564-1 format)
    # This is just a sample - in reality, this would come from a PIN pad or HSM
    encrypted_pin = b'\x12\x34\x56\x78\x90\xAB\xCD\xEF'
    pan = "1234567890123456"  # Example PAN
    
    try:
        decryptor = CardDataDecryptor(SAMPLE_KEY, key_type='double')
        
        # Example: Decrypt PIN
        pin = decryptor.decrypt_pin_block(encrypted_pin, pan, 'ISO9564-1')
        print(f"Decrypted PIN: {pin}")
        
        # Example: Decrypt track data
        # encrypted_track = b'...'  # Actual encrypted track data
        # track_data = decryptor.decrypt_track_data(encrypted_track, '3DES_CBC')
        # print(f"Decrypted track data: {track_data}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
