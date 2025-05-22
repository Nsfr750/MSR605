"""
Module for decrypting card data including PIN blocks and track data.
This module provides functionality to decrypt sensitive card information
that might be encrypted using various industry-standard algorithms.
"""

import binascii
from Crypto.Cipher import DES, DES3, AES
from Crypto.Util.Padding import unpad
from typing import Union, Optional, Dict, Any

class CardDataDecryptor:
    """
    A class to handle decryption of card data including PIN blocks and track data.
    Supports various encryption algorithms commonly used in payment systems.
    """
    
    def __init__(self, key: bytes, key_type: str = 'single', iv: Optional[bytes] = None):
        """
        Initialize the decryptor with encryption key(s).
        
        Args:
            key: The encryption key in bytes
            key_type: Type of key ('single', 'double', 'triple' for DES/3DES)
            iv: Initialization vector if required
        """
        self.key = key
        self.key_type = key_type.lower()
        self.iv = iv or b'\x00' * 8  # Default IV if not provided
        
        # Validate key length based on key type
        if self.key_type == 'single' and len(key) not in (8, 16, 24):
            raise ValueError("For single DES, key must be 8, 16, or 24 bytes")
        elif self.key_type == 'double' and len(key) != 16:
            raise ValueError("For double-length 3DES, key must be 16 bytes")
        elif self.key_type == 'triple' and len(key) != 24:
            raise ValueError("For triple-length 3DES, key must be 24 bytes")
    def _get_des_cipher(self):
        """Get the appropriate DES/3DES cipher based on key type."""
        if self.key_type == 'single':
            return DES.new(self.key, DES.MODE_ECB)
        elif self.key_type in ('double', 'triple'):
            return DES3.new(self.key, DES3.MODE_ECB)
        else:
            raise ValueError(f"Unsupported key type: {self.key_type}")

    def _pad_pkcs7(self, data, block_size):
        """Pad data using PKCS#7 padding."""
        padding_length = block_size - (len(data) % block_size)
        return data + bytes([padding_length] * padding_length)

    def _prepare_pan(self, pan):
        """Prepare PAN for PIN block calculation."""
        # Get the PAN without the check digit and with 12 zeros
        pan = pan[:-1]  # Remove check digit
        pan = pan.zfill(12)  # Pad with leading zeros to 12 digits
        return bytes.fromhex(f"0000{pan}")

    def decrypt_pin_block(self, encrypted_pin_block: bytes, pan: str, 
                         pin_block_format: str = 'ISO9564-1') -> str:
        """
        Decrypt a PIN block using the specified format.
        
        Args:
            encrypted_pin_block: The encrypted PIN block
            pan: Primary Account Number (PAN) for PIN block validation
            pin_block_format: PIN block format (ISO9564-1, ISO9564-3, etc.)
            
        Returns:
            Decrypted PIN as string
        """
        try:
            # Decrypt the PIN block
            if self.key_type in ('single', 'double', 'triple'):
                if len(encrypted_pin_block) % 8 != 0:
                    encrypted_pin_block = self._pad_pkcs7(encrypted_pin_block, 8)
                cipher = self._get_des_cipher()
                pin_block = cipher.decrypt(encrypted_pin_block)
                
                # For ISO 9564-1 format
                if pin_block_format.upper() == 'ISO9564-1':
                    # XOR with PAN to get clear PIN block
                    pan_data = self._prepare_pan(pan)
                    clear_pin_block = bytes(a ^ b for a, b in zip(pin_block, pan_data))
                    # Extract PIN (format: 0x0N P1 P2 P3 P4 F...F where N is PIN length)
                    pin_length = clear_pin_block[0] & 0x0F
                    pin_digits = clear_pin_block[1:1+pin_length]
                    return ''.join(f"{d & 0x0F:01d}" for d in pin_digits)
                    
            # Add support for other PIN block formats here
            
            raise ValueError(f"Unsupported PIN block format: {pin_block_format}")
            
        except Exception as e:
            raise ValueError(f"PIN decryption failed: {str(e)}")
    
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
