#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime
import re
from typing import List, Dict, Optional, Union, Tuple
from dataclasses import dataclass, field
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedFunctionsFrame(ttk.Frame):
    """Frame containing advanced card data processing functions."""
    
    def __init__(self, parent, tracks: List[str] = None, **kwargs):
        """Initialize the advanced functions frame.
        
        Args:
            parent: Parent widget
            tracks: List of track data strings [track1, track2, track3]
        """
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.tracks = tracks or ['', '', '']
        self.decryption_result = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the user interface."""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs
        self.setup_decode_tab()
        self.setup_decrypt_tab()
    
    def setup_decode_tab(self):
        """Set up the decode tab."""
        decode_frame = ttk.Frame(self.notebook)
        self.notebook.add(decode_frame, text="Decode Card")
        
        # Track selection
        ttk.Label(decode_frame, text="Select Tracks to Decode:").pack(pady=5)
        
        self.track_vars = []
        track_frame = ttk.Frame(decode_frame)
        track_frame.pack(pady=5)
        
        for i in range(3):
            var = tk.BooleanVar(value=True)
            self.track_vars.append(var)
            cb = ttk.Checkbutton(
                track_frame, 
                text=f"Track {i+1}", 
                variable=var
            )
            cb.pack(side=tk.LEFT, padx=10)
        
        # Decode button
        ttk.Button(
            decode_frame, 
            text="Decode Selected Tracks", 
            command=self.decode_selected_tracks
        ).pack(pady=10)
        
        # Results area
        ttk.Label(decode_frame, text="Decoded Data:").pack()
        self.decode_text = scrolledtext.ScrolledText(
            decode_frame, 
            width=80, 
            height=15,
            wrap=tk.WORD
        )
        self.decode_text.pack(pady=5, fill=tk.BOTH, expand=True)
    
    def setup_decrypt_tab(self):
        """Set up the decrypt tab."""
        decrypt_frame = ttk.Frame(self.notebook)
        self.notebook.add(decrypt_frame, text="Decrypt Data")
        
        # Key input
        key_frame = ttk.LabelFrame(decrypt_frame, text="Encryption Key")
        key_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(key_frame, text="Key (hex):").pack(side=tk.LEFT, padx=5)
        self.key_entry = ttk.Entry(key_frame, width=32)
        self.key_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Algorithm selection
        algo_frame = ttk.LabelFrame(decrypt_frame, text="Algorithm")
        algo_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.algo_var = tk.StringVar(value="DES")
        algorithms = ["DES", "3DES", "AES-128", "AES-192", "AES-256"]
        
        for algo in algorithms:
            rb = ttk.Radiobutton(
                algo_frame,
                text=algo,
                variable=self.algo_var,
                value=algo
            )
            rb.pack(side=tk.LEFT, padx=5)
        
        # Data to decrypt
        data_frame = ttk.LabelFrame(decrypt_frame, text="Data to Decrypt")
        data_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.data_text = scrolledtext.ScrolledText(
            data_frame,
            width=80,
            height=10,
            wrap=tk.WORD
        )
        self.data_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(decrypt_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            btn_frame,
            text="Load Track Data",
            command=self.load_track_data
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Decrypt",
            command=self.decrypt_data,
            style="Accent.TButton"
        ).pack(side=tk.RIGHT, padx=5)
        
        # Results area
        ttk.Label(decrypt_frame, text="Decryption Results:").pack()
        self.result_text = scrolledtext.ScrolledText(
            decrypt_frame,
            width=80,
            height=15,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def set_tracks(self, tracks: List[str]):
        """Update the track data.
        
        Args:
            tracks: List of track data strings [track1, track2, track3]
        """
        self.tracks = tracks or ['', '', '']
    
    def load_track_data(self):
        """Load track data into the decrypt text area."""
        selected_tracks = []
        for i, var in enumerate(self.track_vars):
            if var.get() and i < len(self.tracks):
                selected_tracks.append(f"Track {i+1}: {self.tracks[i]}")
        
        self.data_text.delete(1.0, tk.END)
        if selected_tracks:
            self.data_text.insert(tk.END, '\n'.join(selected_tracks))
    
    def decode_selected_tracks(self):
        """Decode the selected tracks and display results."""
        results = []
        for i, var in enumerate(self.track_vars):
            if var.get() and i < len(self.tracks):
                track_data = self.tracks[i]
                if not track_data:
                    continue
                    
                decoded = self._decode_track(track_data, i+1)
                if decoded:
                    results.append(decoded)
        
        self.decode_text.delete(1.0, tk.END)
        if results:
            self.decode_text.insert(tk.END, '\n\n'.join(results))
        else:
            self.decode_text.insert(tk.END, "No valid track data found in selected tracks.")
    
    def _decode_track(self, track_data: str, track_num: int) -> str:
        """Decode a single track's data.
        
        Args:
            track_data: Raw track data string
            track_num: Track number (1, 2, or 3)
            
        Returns:
            Formatted string with decoded track information
        """
        if not track_data:
            return ""
            
        result = [f"=== Track {track_num} ==="]
        
        # Try to parse track data based on format
        if track_num == 1 and '^' in track_data:
            # Track 1 format: %B1234567890123456^CARDHOLDER/NAME^YYMM...
            parts = track_data[2:].split('^')
            if len(parts) >= 3:
                result.append(f"Card Number: {parts[0]}")
                result.append(f"Cardholder: {parts[1].split('/')[0].strip()}")
                if len(parts[1].split('/')) > 1:
                    result.append(f"Last Name: {parts[1].split('/')[1].strip()}")
                if len(parts[2]) >= 4:
                    result.append(f"Expiration: {parts[2][2:4]}/{parts[2][:2]}")
                if len(parts[2]) >= 7:
                    result.append(f"Service Code: {parts[2][4:7]}")
        elif track_num in (2, 3) and '=' in track_data:
            # Track 2/3 format: ;1234567890123456=YYMM...
            parts = track_data[1:].split('=')
            if len(parts) >= 2:
                result.append(f"Card Number: {parts[0][:16]}")
                if len(parts[1]) >= 4:
                    result.append(f"Expiration: {parts[1][2:4]}/{parts[1][:2]}")
                if len(parts[1]) >= 7:
                    result.append(f"Service Code: {parts[1][4:7]}")
        
        # Add raw data
        result.append(f"\nRaw Data: {track_data}")
        return '\n'.join(result)
    
    def decrypt_data(self):
        """Decrypt the provided data using the specified key and algorithm."""
        key = self.key_entry.get().strip()
        algorithm = self.algo_var.get()
        data = self.data_text.get(1.0, tk.END).strip()
        
        if not key or not data:
            messagebox.showerror("Error", "Both key and data are required")
            return
        
        try:
            # TODO: Implement actual decryption using the decrypt.py module
            # For now, just show a placeholder
            result = f"Decrypted with {algorithm} and key {key}\n\n{data}"
            
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
            self.result_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Decryption Error", f"Failed to decrypt data: {str(e)}")


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Advanced Card Functions")
    
    # Sample track data for testing
    sample_tracks = [
        "%B1234567890123456^CARDHOLDER/NAME^24051010000000000000?",
        ";1234567890123456=24051010000000000000?",
        ";1234567890123456=24051010000000000000?"
    ]
    
    frame = AdvancedFunctionsFrame(root, tracks=sample_tracks)
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Set window size and center it
    window_width = 800
    window_height = 700
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    root.mainloop()
